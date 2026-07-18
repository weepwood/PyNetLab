#include "net.h"
#include <errno.h>
#include <poll.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_CLIENTS 1024
int main(void) {
    int listener = create_tcp_listener("127.0.0.1", "9103", 128);
    if (listener < 0) return 1;
    struct pollfd fds[MAX_CLIENTS];
    for (size_t i = 0; i < MAX_CLIENTS; ++i) fds[i].fd = -1;
    fds[0] = (struct pollfd){.fd = listener, .events = POLLIN};
    puts("poll echo listening on 127.0.0.1:9103");
    for (;;) {
        int ready = poll(fds, MAX_CLIENTS, -1);
        if (ready < 0) { if (errno == EINTR) continue; perror("poll"); break; }
        if (fds[0].revents & POLLIN) {
            int client = accept(listener, NULL, NULL);
            if (client >= 0) for (size_t i = 1; i < MAX_CLIENTS; ++i) if (fds[i].fd < 0) { fds[i] = (struct pollfd){.fd = client, .events = POLLIN}; break; }
        }
        for (size_t i = 1; i < MAX_CLIENTS; ++i) {
            if (fds[i].fd < 0 || !(fds[i].revents & (POLLIN | POLLHUP | POLLERR))) continue;
            char buffer[4096]; ssize_t n = recv(fds[i].fd, buffer, sizeof(buffer), 0);
            if (n <= 0 || send_all(fds[i].fd, buffer, (size_t)n) < 0) { close(fds[i].fd); fds[i].fd = -1; }
        }
    }
    close(listener); return 0;
}
