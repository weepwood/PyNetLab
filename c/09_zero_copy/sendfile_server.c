#define _GNU_SOURCE
#include "net.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/sendfile.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s FILE [PORT]\n", argv[0]); return 2; }
    const char *port = argc > 2 ? argv[2] : "9105";
    int file = open(argv[1], O_RDONLY | O_CLOEXEC); if (file < 0) { perror("open"); return 1; }
    struct stat info; if (fstat(file, &info) < 0) return 1;
    int listener = create_tcp_listener("127.0.0.1", port, 16); if (listener < 0) return 1;
    printf("sendfile server: nc 127.0.0.1 %s > received.bin\n", port);
    int client = accept(listener, NULL, NULL); if (client < 0) return 1;
    off_t offset = 0;
    while (offset < info.st_size) {
        ssize_t n = sendfile(client, file, &offset, (size_t)(info.st_size - offset));
        if (n <= 0) { perror("sendfile"); break; }
    }
    close(client); close(listener); close(file); return 0;
}
