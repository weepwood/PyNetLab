#define _POSIX_C_SOURCE 200809L
#include "net.h"

#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int create_tcp_listener(const char *host, const char *port, int backlog) {
    struct addrinfo hints = {0};
    struct addrinfo *result = NULL;
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;
    int error = getaddrinfo(host, port, &hints, &result);
    if (error != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(error));
        return -1;
    }

    int listener = -1;
    for (struct addrinfo *item = result; item != NULL; item = item->ai_next) {
        listener = socket(item->ai_family, item->ai_socktype | SOCK_CLOEXEC, item->ai_protocol);
        if (listener < 0) continue;
        int one = 1;
        (void)setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));
        if (bind(listener, item->ai_addr, item->ai_addrlen) == 0 && listen(listener, backlog) == 0) break;
        close(listener);
        listener = -1;
    }
    freeaddrinfo(result);
    return listener;
}

ssize_t send_all(int fd, const void *buffer, size_t length) {
    const char *cursor = buffer;
    size_t sent = 0;
    while (sent < length) {
        ssize_t result = send(fd, cursor + sent, length - sent, MSG_NOSIGNAL);
        if (result > 0) {
            sent += (size_t)result;
            continue;
        }
        if (result < 0 && errno == EINTR) continue;
        return -1;
    }
    return (ssize_t)sent;
}

int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags < 0) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}
