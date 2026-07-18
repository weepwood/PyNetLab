#ifndef PYNETLAB_NET_H
#define PYNETLAB_NET_H

#include <stddef.h>
#include <sys/types.h>

int create_tcp_listener(const char *host, const char *port, int backlog);
ssize_t send_all(int fd, const void *buffer, size_t length);
int set_nonblocking(int fd);

#endif
