#define _GNU_SOURCE
#include <arpa/inet.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <net/if.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    const char *interface = argc > 1 ? argv[1] : "lo";
    int fd = socket(AF_PACKET, SOCK_RAW | SOCK_CLOEXEC, htons(ETH_P_ALL));
    if (fd < 0) { perror("socket (try sudo)"); return 1; }
    unsigned int index = if_nametoindex(interface);
    if (index == 0) { perror("if_nametoindex"); return 1; }
    struct sockaddr_ll address = {0};
    address.sll_family = AF_PACKET; address.sll_protocol = htons(ETH_P_ALL); address.sll_ifindex = (int)index;
    if (bind(fd, (struct sockaddr *)&address, sizeof(address)) < 0) { perror("bind"); return 1; }
    unsigned char buffer[65536];
    for (int packet = 0; packet < 20; ++packet) {
        ssize_t n = recv(fd, buffer, sizeof(buffer), 0);
        if (n < (ssize_t)sizeof(struct ethhdr)) continue;
        struct ethhdr *eth = (struct ethhdr *)buffer;
        printf("len=%zd src=%02x:%02x:%02x:%02x:%02x:%02x dst=%02x:%02x:%02x:%02x:%02x:%02x type=0x%04x\n",
            n, eth->h_source[0], eth->h_source[1], eth->h_source[2], eth->h_source[3], eth->h_source[4], eth->h_source[5],
            eth->h_dest[0], eth->h_dest[1], eth->h_dest[2], eth->h_dest[3], eth->h_dest[4], eth->h_dest[5], ntohs(eth->h_proto));
    }
    close(fd); return 0;
}
