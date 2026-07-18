#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <poll.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    const char *host = argc > 1 ? argv[1] : "example.com";
    const char *port = argc > 2 ? argv[2] : "80";
    struct addrinfo hints = {0}, *result = NULL;
    hints.ai_family = AF_UNSPEC; hints.ai_socktype = SOCK_STREAM;
    int error = getaddrinfo(host, port, &hints, &result);
    if (error != 0) { fprintf(stderr, "%s\n", gai_strerror(error)); return 1; }
    int fd = socket(result->ai_family, result->ai_socktype | SOCK_NONBLOCK | SOCK_CLOEXEC, result->ai_protocol);
    if (fd < 0) { perror("socket"); return 1; }
    if (connect(fd, result->ai_addr, result->ai_addrlen) < 0 && errno != EINPROGRESS) { perror("connect"); return 1; }
    struct pollfd pfd = {.fd = fd, .events = POLLOUT};
    int ready = poll(&pfd, 1, 3000);
    int socket_error = 0; socklen_t length = sizeof(socket_error);
    if (ready <= 0 || getsockopt(fd, SOL_SOCKET, SO_ERROR, &socket_error, &length) < 0 || socket_error != 0) {
        fprintf(stderr, "connect failed: %s\n", ready == 0 ? "timeout" : strerror(socket_error)); return 1;
    }
    printf("connected to %s:%s without blocking\n", host, port);
    freeaddrinfo(result); close(fd); return 0;
}
