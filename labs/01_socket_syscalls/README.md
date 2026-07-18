# Lab 01: Socket Syscalls

主命令：

```bash
strace -ff -e trace=network,read,write,close python -m pynetlab.lesson01_tcp_echo.server
```

请按 `docs/LAB_GUIDE.md` 的“运行 → 观察 → 故障注入 → 解释 → 清理”流程完成实验。
