# 实验手册

每个实验遵循五步：

1. **运行**：先运行最小示例，不修改代码。
2. **观察**：同时使用 `strace`、`ss`、`tcpdump`、`ip` 或 eBPF。
3. **故障注入**：断开客户端、缩小缓冲区、增加延迟或丢包。
4. **解释**：记录系统调用返回值、Socket 状态和抓包之间的对应关系。
5. **清理**：删除 namespace、qdisc、TUN 设备和临时 capability。

## 建议实验记录模板

```markdown
# 实验名称

- 日期：
- 内核版本：`uname -a`
- 命令：
- 预期：
- 实际观察：
- 抓包过滤器：
- 系统调用：
- 异常与解释：
- 清理命令：
```

## 故障注入示例

```bash
sudo DELAY=200ms LOSS=5% RATE=2mbit ./scripts/netem/add_impairment.sh eth0
sudo ./scripts/netem/reset.sh eth0
```

在 namespace 中应用时：

```bash
sudo ip netns exec pynet-a tc qdisc replace dev veth-a root netem delay 100ms loss 2%
```
