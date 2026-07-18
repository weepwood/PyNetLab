# eBPF 网络可观测性

```bash
sudo bpftrace ebpf/tcp_connect.bt
sudo bpftrace ebpf/tcp_retransmit.bt
```

先使用 tracepoint 学习稳定的内核观测点，再进入 libbpf CO-RE 与 XDP。不同内核版本暴露的 tracepoint 字段可能不同，可用 `bpftrace -lv 'tracepoint:tcp:*'` 检查。
