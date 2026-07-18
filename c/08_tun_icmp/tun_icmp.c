#define _GNU_SOURCE
#include <arpa/inet.h>
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

static unsigned short checksum(const void *data, size_t length) {
    const unsigned short *words = data; unsigned long sum = 0;
    while (length > 1) { sum += *words++; length -= 2; }
    if (length) sum += *(const unsigned char *)words;
    while (sum >> 16) sum = (sum & 0xffffU) + (sum >> 16);
    return (unsigned short)~sum;
}

int main(void) {
    int fd = open("/dev/net/tun", O_RDWR | O_CLOEXEC); if (fd < 0) { perror("open /dev/net/tun"); return 1; }
    struct ifreq request = {0}; request.ifr_flags = IFF_TUN | IFF_NO_PI; strncpy(request.ifr_name, "pynetc0", IFNAMSIZ - 1);
    if (ioctl(fd, TUNSETIFF, &request) < 0) { perror("TUNSETIFF"); return 1; }
    printf("Created %s. Configure in another shell: sudo ip addr add 10.98.0.1/24 dev %s && sudo ip link set %s up\n", request.ifr_name, request.ifr_name, request.ifr_name);
    unsigned char buffer[65535];
    for (;;) {
        ssize_t n = read(fd, buffer, sizeof(buffer));
        if (n < (ssize_t)(sizeof(struct iphdr) + sizeof(struct icmphdr))) continue;
        struct iphdr *ip = (struct iphdr *)buffer;
        if (ip->version != 4 || ip->protocol != IPPROTO_ICMP) continue;
        size_t header_length = (size_t)ip->ihl * 4;
        if ((size_t)n < header_length + sizeof(struct icmphdr)) continue;
        struct icmphdr *icmp = (struct icmphdr *)(buffer + header_length);
        if (icmp->type != ICMP_ECHO) continue;
        uint32_t address = ip->saddr; ip->saddr = ip->daddr; ip->daddr = address; ip->ttl = 64; ip->check = 0; ip->check = checksum(ip, header_length);
        icmp->type = ICMP_ECHOREPLY; icmp->checksum = 0; icmp->checksum = checksum(icmp, (size_t)n - header_length);
        if (write(fd, buffer, (size_t)n) < 0) { perror("write"); break; }
    }
    close(fd); return 0;
}
