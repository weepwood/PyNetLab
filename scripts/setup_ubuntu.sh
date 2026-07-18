#!/usr/bin/env bash
set -Eeuo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This setup script targets Ubuntu/Debian (apt-get not found)." >&2
  exit 1
fi

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential clang cmake gdb git make pkg-config \
  python3 python3-venv python3-pip \
  strace ltrace tcpdump iproute2 iputils-ping traceroute \
  net-tools dnsutils ethtool nftables socat netcat-openbsd curl jq \
  libpcap-dev liburing-dev bpftrace bpftool

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -e '.[dev]'

printf '\nSetup complete. Run:\n  source .venv/bin/activate\n  make test\n  make c\n'
