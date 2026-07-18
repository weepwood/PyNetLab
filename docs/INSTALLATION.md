# 安装与运行环境

## 推荐配置

- Ubuntu 24.04 LTS x86_64 或 ARM64
- 2 CPU、4 GB 内存、30 GB 磁盘
- Linux 内核 6.8 或更新版本
- 可使用物理机，也可使用 VMware、UTM、Parallels、VirtualBox 或云主机

涉及 TUN、namespace、eBPF 和 nftables 时，虚拟机必须允许相应内核能力。容器并不适合作为所有实验的唯一环境，因为默认会隔离或移除 `CAP_NET_ADMIN`、`CAP_NET_RAW`、BPF 和 TUN 设备。

## 安装

```bash
./scripts/setup_ubuntu.sh
source .venv/bin/activate
./scripts/check_environment.sh
make test
make c
```

## 最小权限

Raw Socket 可临时使用：

```bash
sudo setcap cap_net_raw+ep .venv/bin/python3
getcap .venv/bin/python3
```

这会给该解释器中的所有 Python 程序授予原始套接字能力。学习结束后建议删除：

```bash
sudo setcap -r .venv/bin/python3
```

TUN、namespace、路由和防火墙实验通常直接使用 `sudo`，并在实验后执行清理脚本。
