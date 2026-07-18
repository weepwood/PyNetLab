#define _GNU_SOURCE
#include "net.h"
#include <errno.h>
#include <stdio.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_EVENTS 128
int main(void) {
    int listener = create_tcp_listener("127.0.0.1", "9104", 512);
    if (listener < 0 || set_nonblocking(listener) < 0) return 1;
    int epfd = epoll_create1(EPOLL_CLOEXEC); if (epfd < 0) return 1;
    struct epoll_event event = {.events = EPOLLIN, .data.fd = listener};
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, listener, &event) < 0) return 1;
    puts("epoll ET echo listening on 127.0.0.1:9104");
    struct epoll_event events[MAX_EVENTS];
    for (;;) {
        int count = epoll_wait(epfd, events, MAX_EVENTS, -1);
        if (count < 0) { if (errno == EINTR) continue; perror("epoll_wait"); break; }
        for (int i = 0; i < count; ++i) {
            int fd = events[i].data.fd;
            if (fd == listener) {
                for (;;) {
                    int client = accept4(listener, NULL, NULL, SOCK_NONBLOCK | SOCK_CLOEXEC);
                    if (client < 0) { if (errno == EAGAIN || errno == EWOULDBLOCK) break; perror("accept4"); break; }
                    struct epoll_event client_event = {.events = EPOLLIN | EPOLLET | EPOLLRDHUP, .data.fd = client};
                    if (epoll_ctl(epfd, EPOLL_CTL_ADD, client, &client_event) < 0) close(client);
                }
            } else {
                int close_client = 0;
                for (;;) {
                    char buffer[4096]; ssize_t n = recv(fd, buffer, sizeof(buffer), 0);
                    if (n > 0) { if (send_all(fd, buffer, (size_t)n) < 0) close_client = 1; continue; }
                    if (n == 0) close_client = 1;
                    else if (errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR) close_client = 1;
                    break;
                }
                if (close_client || (events[i].events & (EPOLLERR | EPOLLHUP | EPOLLRDHUP))) { epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL); close(fd); }
            }
        }
    }
    close(epfd); close(listener); return 0;
}
