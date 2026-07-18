#include "net.h"
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    int listener = create_tcp_listener("127.0.0.1", "9101", 16);
    if (listener < 0) return 1;
    puts("Partial-I/O lab listening on 127.0.0.1:9101");
    int client = accept(listener, NULL, NULL);
    if (client < 0) { perror("accept"); return 1; }
    int size = 1024;
    (void)setsockopt(client, SOL_SOCKET, SO_RCVBUF, &size, sizeof(size));
    uint64_t total = 0;
    unsigned char buffer[257];
    for (;;) {
        ssize_t n = recv(client, buffer, sizeof(buffer), 0);
        if (n > 0) { total += (uint64_t)n; printf("recv=%zd total=%llu\n", n, (unsigned long long)total); continue; }
        if (n < 0 && errno == EINTR) continue;
        break;
    }
    close(client); close(listener);
    return 0;
}
