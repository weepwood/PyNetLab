#define _POSIX_C_SOURCE 200809L
#include "net.h"
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    const char *port = argc > 1 ? argv[1] : "9100";
    struct addrinfo hints = {0}, *result = NULL;
    hints.ai_family = AF_INET; hints.ai_socktype = SOCK_STREAM;
    if (getaddrinfo("127.0.0.1", port, &hints, &result) != 0) return 1;
    int fd = socket(result->ai_family, result->ai_socktype | SOCK_CLOEXEC, result->ai_protocol);
    if (fd < 0 || connect(fd, result->ai_addr, result->ai_addrlen) < 0) { perror("connect"); return 1; }
    freeaddrinfo(result);
    char line[4096];
    while (fgets(line, sizeof(line), stdin) != NULL) {
        size_t length = strlen(line);
        if (send_all(fd, line, length) < 0) { perror("send"); break; }
        ssize_t n = recv(fd, line, sizeof(line) - 1, 0);
        if (n <= 0) break;
        line[n] = '\0'; fputs(line, stdout);
    }
    close(fd);
    return 0;
}
