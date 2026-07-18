# PyNetLab

PyNetLab 是一套以 **Linux 网络系统** 为主线的可运行学习项目。它从 Python TCP/UDP 开始，逐步深入到 C Socket、非阻塞 I/O、`epoll`、原始数据包、网络命名空间、TUN/TAP、用户态协议栈、eBPF 与 `io_uring`。

> 目标不是只会调用网络库，而是能够解释：一次 `send()` 调用如何经过系统调用、内核缓冲区、TCP/IP 协议栈、队列和网卡。

## 技术选择

- **Python**：协议构造、数据包解析、自动化实验、快速验证。
- **C**：系统调用、文件描述符、缓冲区、非阻塞 I/O、`epoll`、零拷贝、`io_uring`。
- **Shell**：network namespace、veth、bridge、路由、NAT、流量控制和故障注入。
- **Linux**：项目唯一主运行平台。推荐 Ubuntu 24.04 LTS 或更新版本。

## 课程地图

| 阶段 | 主题 | 主要目录 | 权限 |
|---|---|---|---|
| 01 | TCP/UDP、分帧、HTTP/TLS | `src/pynetlab/lesson*` | 普通用户 |
| 02 | C Socket、部分读写 | `c/01_tcp_echo`、`c/02_partial_io` | 普通用户 |
| 03 | 非阻塞、select、poll、epoll | `c/03_*` 至 `c/06_*` | 普通用户 |
| 04 | Ethernet/IP/ICMP/TCP/UDP 解析 | `src/pynetlab/packet` | 普通用户 |
| 05 | AF_PACKET 与 Raw Socket | `src/pynetlab/raw`、`c/07_raw_packet` | root/CAP_NET_RAW |
| 06 | namespace、veth、bridge、路由、NAT | `labs/08_*` 至 `labs/10_*` | root |
| 07 | TUN/TAP 与用户态 ICMP/UDP | `src/pynetlab/tun`、`c/08_tun_icmp` | root/CAP_NET_ADMIN |
| 08 | eBPF 网络可观测性 | `ebpf/` | root、内核支持 |
| 09 | sendfile 与 io_uring | `c/09_zero_copy`、`c/10_io_uring` | 普通用户 |

完整路线见 [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md)。

## 快速开始

```bash
git clone https://github.com/weepwood/PyNetLab.git
cd PyNetLab
./scripts/setup_ubuntu.sh
source .venv/bin/activate
make test
make c
```

检查环境：

```bash
./scripts/check_environment.sh
```

## 第一个实验：同时观察三层

终端 1，启动 Python TCP 服务端：

```bash
python -m pynetlab.lesson01_tcp_echo.server
```

终端 2，追踪系统调用：

```bash
sudo strace -ff -e trace=network,read,write,close \
  -p "$(pgrep -n -f lesson01_tcp_echo.server)"
```

终端 3，抓包并观察 Socket：

```bash
sudo tcpdump -i lo -nn -X 'tcp port 9000'
ss -lntp '( sport = :9000 )'
```

终端 4，运行客户端：

```bash
python -m pynetlab.lesson01_tcp_echo.client
```

同一次通信中，你会看到：

```text
Python socket API
  -> Linux 系统调用
  -> 内核 Socket 状态
  -> TCP 数据包
```

## 常用命令

```bash
make help           # 查看所有命令
make test           # Python 测试
make lint           # Ruff 检查
make c              # 编译基础 C 实验
make c-optional     # 编译需要 liburing 的可选实验
make clean
```

运行协议解析测试：

```bash
python -m unittest discover -s tests -v
```

运行 AF_PACKET 抓包器：

```bash
sudo .venv/bin/python -m pynetlab.raw.sniffer --interface eth0 --count 20
```

运行原始 ICMP ping：

```bash
sudo .venv/bin/python -m pynetlab.raw.ping 1.1.1.1
```

创建隔离网络实验：

```bash
sudo ./scripts/netns/create_two_hosts.sh
sudo ip netns exec pynet-a ping -c 2 10.10.0.2
sudo ./scripts/netns/cleanup.sh
```

## 文档

- [安装与环境](docs/INSTALLATION.md)
- [完整学习路线](docs/LEARNING_PATH.md)
- [实验手册](docs/LAB_GUIDE.md)
- [Linux 数据包路径](docs/PACKET_PATH.md)
- [抓包指南](docs/WIRESHARK.md)
- [练习题](docs/EXERCISES.md)
- [故障排查](docs/TROUBLESHOOTING.md)
- [安全边界](SECURITY.md)

## 安全说明

Raw Socket、网络命名空间、TUN/TAP、nftables、eBPF 实验会使用较高权限。只在你拥有或明确获准使用的主机和网络中运行。优先使用独立虚拟机或测试 namespace，不要直接修改生产机器的路由和防火墙规则。

## License

MIT
