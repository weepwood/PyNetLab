#define _GNU_SOURCE
#include "net.h"
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    const char *port = argc > 1 ? argv[1] : "9100";
    int listener = create_tcp_listener("127.0.0.1", port, 128);
    if (listener < 0) { perror("listen"); return 1; }
    printf("C TCP echo listening on 127.0.0.1:%s\n", port);
    for (;;) {
        int client = accept4(listener, NULL, NULL, SOCK_CLOEXEC);
        if (client < 0) { if (errno == EINTR) continue; perror("accept4"); break; }
        char buffer[4096];
        for (;;) {
            ssize_t n = recv(client, buffer, sizeof(buffer), 0);
            if (n > 0 && send_all(client, buffer, (size_t)n) >= 0) continue;
            if (n < 0 && errno == EINTR) continue;
            break;
        }
        close(client);
    }
    close(listener);
    return 0;
}
