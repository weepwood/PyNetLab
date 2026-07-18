CC ?= cc
CFLAGS ?= -std=c17 -O2 -g -Wall -Wextra -Wpedantic -Werror
BIN := bin
CORE := \
  $(BIN)/tcp-echo-server $(BIN)/tcp-echo-client \
  $(BIN)/partial-io-server $(BIN)/nonblocking-connect \
  $(BIN)/select-echo-server $(BIN)/poll-echo-server $(BIN)/epoll-echo-server \
  $(BIN)/raw-sniffer $(BIN)/tun-icmp $(BIN)/sendfile-server

.PHONY: all optional clean
all: $(CORE)
optional: $(BIN)/io-uring-echo-server

$(BIN):
	mkdir -p $(BIN)

$(BIN)/tcp-echo-server: 01_tcp_echo/server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/tcp-echo-client: 01_tcp_echo/client.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/partial-io-server: 02_partial_io/server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/nonblocking-connect: 03_nonblocking/connect.c | $(BIN)
	$(CC) $(CFLAGS) $< -o $@
$(BIN)/select-echo-server: 04_select/server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/poll-echo-server: 05_poll/server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/epoll-echo-server: 06_epoll/server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/raw-sniffer: 07_raw_packet/sniffer.c | $(BIN)
	$(CC) $(CFLAGS) $< -o $@
$(BIN)/tun-icmp: 08_tun_icmp/tun_icmp.c | $(BIN)
	$(CC) $(CFLAGS) $< -o $@
$(BIN)/sendfile-server: 09_zero_copy/sendfile_server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -o $@
$(BIN)/io-uring-echo-server: 10_io_uring/server.c common/net.c common/net.h | $(BIN)
	$(CC) $(CFLAGS) -Icommon $< common/net.c -luring -o $@

clean:
	rm -rf $(BIN)
