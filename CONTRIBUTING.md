# Contributing

1. 每个实验必须有明确的学习目标、运行命令和清理命令。
2. 涉及 root、CAP_NET_RAW、CAP_NET_ADMIN 或修改路由/防火墙时，文档必须显著标注。
3. 网络解析代码需要包含边界检查，不能直接信任包头中的长度字段。
4. C 代码使用 `-Wall -Wextra -Wpedantic -Werror` 编译。
5. 新增 Python 代码需要通过 `make test` 和 `make lint`。
6. Shell 脚本默认启用 `set -Eeuo pipefail`，并尽可能实现幂等清理。
