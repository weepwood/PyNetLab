# 练习题

## 基础

1. 修改 TCP Echo，使客户端一次发送 1 MiB，服务端每次只读取 37 字节，记录 `recv` 次数。
2. 给长度前缀协议增加版本、消息类型、请求 ID 和 CRC32。
3. 使用 `shutdown(SHUT_WR)` 实现半关闭，并观察 FIN。
4. 分别设置 `SO_SNDBUF` 和 `SO_RCVBUF`，比较实际内核值。

## epoll

1. 将示例从 ET 改为 LT，比较通知次数。
2. 故意只读取一次，不读到 `EAGAIN`，复现 ET 饥饿问题。
3. 增加输出缓冲区，正确处理非阻塞部分发送和 `EPOLLOUT`。
4. 增加定时器：连接 30 秒无数据自动关闭。

## 数据包

1. 为 IPv4 解析器验证 Header Checksum。
2. 实现 IPv4 分片字段解析。
3. 为 TCP 实现伪首部 Checksum。
4. 解析 TCP MSS、Window Scale、SACK Permitted 和 Timestamp 选项。

## 虚拟网络

1. 创建三个 namespace：client、router、server。
2. 禁用 router 的 `ip_forward`，解释 ping 为什么失败。
3. 在 router 两侧分别抓包，证明 TTL 变化。
4. 使用 nftables 对 ICMP 限速。

## 用户态协议栈

1. 在 TUN responder 中加入 UDP Echo。
2. 维护用户态端口表并拒绝未绑定端口。
3. 实现简化 TCP 三次握手状态机。
4. 实现超时重传队列，但暂不处理拥塞控制。
