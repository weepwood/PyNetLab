# Wireshark 与 tcpdump

## 常用捕获

```bash
sudo tcpdump -i lo -nn -s 0 -w tcp-echo.pcap 'tcp port 9000'
sudo tcpdump -i any -nn -e 'arp or icmp'
sudo tcpdump -i eth0 -nn -vvv -X 'udp port 9001'
```

## Wireshark 过滤器

```text
tcp.port == 9000
tcp.flags.syn == 1
tcp.analysis.retransmission
icmp
arp
udp.port == 9001
```

## 必做观察

1. TCP 三次握手的 Seq/Ack。
2. 客户端发送两次 `send` 后，对端可能一次 `recv`。
3. 主动关闭方进入 TIME_WAIT。
4. `tc netem` 丢包后 TCP 重传。
5. UDP 服务端关闭后客户端只有超时，没有连接建立失败。
