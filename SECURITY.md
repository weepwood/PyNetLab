# Security

本仓库用于本地实验与教学，不是经过安全审计的生产网络栈。

- 只在自己拥有或明确获准使用的设备和网络中运行抓包、Raw Socket、扫描与 eBPF 实验。
- namespace、路由、nftables 与 `tc netem` 实验优先在虚拟机中运行。
- 不建议在远程生产服务器上直接执行 `scripts/netns`、`scripts/routing` 或 `scripts/netem`。
- 示例中的协议解析器会做基础边界检查，但不应直接作为不可信流量的生产解析器。

发现安全问题时，请通过 GitHub Security Advisory 私下报告，不要公开提交可直接利用的细节。
