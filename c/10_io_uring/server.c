#define _GNU_SOURCE
#include "net.h"
#include <liburing.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    int listener = create_tcp_listener("127.0.0.1", "9106", 128);
    if (listener < 0) return 1;
    struct io_uring ring;
    if (io_uring_queue_init(64, &ring, 0) < 0) { perror("io_uring_queue_init"); return 1; }
    puts("minimal io_uring accept lab on 127.0.0.1:9106");
    for (;;) {
        struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
        io_uring_prep_accept(sqe, listener, NULL, NULL, SOCK_CLOEXEC);
        io_uring_submit(&ring);
        struct io_uring_cqe *cqe = NULL;
        if (io_uring_wait_cqe(&ring, &cqe) < 0) break;
        int client = cqe->res; io_uring_cqe_seen(&ring, cqe);
        if (client < 0) continue;
        char buffer[4096]; ssize_t n = recv(client, buffer, sizeof(buffer), 0);
        if (n > 0) (void)send_all(client, buffer, (size_t)n);
        close(client);
    }
    io_uring_queue_exit(&ring); close(listener); return 0;
}
