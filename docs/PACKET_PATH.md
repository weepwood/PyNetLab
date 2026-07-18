# Linux 数据包路径

## 发送路径

```text
应用程序
  -> send()/sendmsg()
  -> Socket 发送缓冲区
  -> TCP/UDP
  -> IPv4/IPv6 路由
  -> Netfilter hooks
  -> qdisc
  -> 驱动队列
  -> DMA / 网卡
```

## 接收路径

```text
网卡
  -> DMA ring
  -> IRQ / NAPI poll
  -> 驱动创建 skb
  -> Ethernet
  -> Netfilter hooks
  -> IPv4/IPv6
  -> TCP/UDP
  -> Socket 接收缓冲区
  -> 唤醒进程
  -> recv()/recvmsg()
```

## 观察点

| 层次 | 工具 |
|---|---|
| 应用系统调用 | `strace` |
| Socket 状态 | `ss -tinmp` |
| 路由 | `ip route get` |
| 邻居/ARP | `ip neigh` |
| 数据包 | `tcpdump`、Wireshark |
| 队列与丢包 | `tc -s qdisc`、`ethtool -S` |
| 内核函数/事件 | bpftrace、bpftool |

不要把 `send()` 成功解释为“对端已经收到”。通常它只表示数据已被复制或排队到本机内核的发送路径。
