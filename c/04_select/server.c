#include "net.h"
#include <errno.h>
#include <stdio.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    int listener = create_tcp_listener("127.0.0.1", "9102", 128);
    if (listener < 0) return 1;
    fd_set master, readable; FD_ZERO(&master); FD_SET(listener, &master); int max_fd = listener;
    puts("select echo listening on 127.0.0.1:9102");
    for (;;) {
        readable = master;
        if (select(max_fd + 1, &readable, NULL, NULL, NULL) < 0) { if (errno == EINTR) continue; perror("select"); break; }
        for (int fd = 0; fd <= max_fd; ++fd) {
            if (!FD_ISSET(fd, &readable)) continue;
            if (fd == listener) {
                int client = accept(listener, NULL, NULL);
                if (client >= 0) { FD_SET(client, &master); if (client > max_fd) max_fd = client; }
            } else {
                char buffer[4096]; ssize_t n = recv(fd, buffer, sizeof(buffer), 0);
                if (n <= 0 || send_all(fd, buffer, (size_t)n) < 0) { close(fd); FD_CLR(fd, &master); }
            }
        }
    }
    close(listener); return 0;
}
