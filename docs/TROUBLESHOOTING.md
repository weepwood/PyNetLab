# 故障排查

## Permission denied

Raw Socket 需要 root 或 `CAP_NET_RAW`；TUN、namespace、路由、nftables 通常需要 root 或 `CAP_NET_ADMIN`。

## `/dev/net/tun` 不存在

```bash
sudo modprobe tun
ls -l /dev/net/tun
```

若在受限容器或虚拟机中仍不存在，需要启用 TUN 设备或改用完整 Linux VM。

## epoll 示例连接后无响应

ET 模式必须循环 `accept`/`recv` 直到 `EAGAIN`。同时检查输出端是否出现部分发送；教学示例的 `send_all` 更适合小消息，扩展到生产模型时应维护 per-connection 输出缓冲区。

## namespace 无法访问外网

检查：

```bash
ip netns exec NAME ip addr
ip netns exec NAME ip route
sysctl net.ipv4.ip_forward
sudo nft list ruleset
```

## bpftrace 找不到 tracepoint

```bash
sudo bpftrace -l 'tracepoint:tcp:*'
sudo bpftrace -lv 'tracepoint:tcp:tcp_retransmit_skb'
```

内核版本不同，字段和可用 tracepoint 可能不同。
