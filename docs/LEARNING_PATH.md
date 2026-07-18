# 学习路线

## 第一阶段：应用层与 TCP 字节流

1. TCP Echo：连接、监听、`accept`、字节流。
2. UDP Echo：数据报、无连接、超时。
3. 长度前缀：粘包、半包、协议边界。
4. asyncio：事件循环、任务、背压。
5. HTTP/TLS：从 Socket 发送 HTTP/1.1 请求。

完成标准：能够解释为什么一次 `send` 不对应对端一次 `recv`。

## 第二阶段：系统调用与 C

1. 用 `strace` 观察 Python 服务端。
2. 使用 C 重写 Echo。
3. 主动缩小 Socket 缓冲区，观察部分读写。
4. 理解 `errno`、`EINTR`、`EAGAIN`、`EINPROGRESS`。

完成标准：能够写出正确循环处理部分发送和中断的代码。

## 第三阶段：I/O 多路复用

依次运行并比较：

```text
thread-per-connection -> select -> poll -> epoll LT/ET
```

完成标准：能够解释就绪通知、边缘触发为何必须读到 `EAGAIN`。

## 第四阶段：数据包

解析 Ethernet、ARP、IPv4、ICMP、UDP 和 TCP Header；验证长度、字节序与校验和。

完成标准：可以从一段十六进制数据中找出源/目的地址、端口、TCP Flags 和 Payload。

## 第五阶段：虚拟网络

使用 namespace、veth、bridge 和路由模拟：两台主机、交换机、路由器和故障链路。

完成标准：能够从路由表解释数据包选择哪个出口，并使用 tcpdump 在每个跳点验证。

## 第六阶段：用户态协议栈

1. TUN 读取 IPv4 包。
2. 用户态 ICMP Echo Reply。
3. UDP Header、端口表和 Echo。
4. 简化 TCP 状态机：LISTEN、SYN-RECEIVED、ESTABLISHED、FIN。

## 第七阶段：内核可观测性与高性能 I/O

1. bpftrace tracepoint。
2. eBPF Map、kprobe/tracepoint、libbpf CO-RE。
3. XDP 数据包路径。
4. `sendfile` 零拷贝。
5. `io_uring` SQ/CQ 和批处理。
