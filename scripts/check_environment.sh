#!/usr/bin/env bash
set -Eeuo pipefail

required=(python3 cc make ip ss tcpdump strace)
optional=(nft bpftrace bpftool clang)
failed=0

printf 'Kernel: %s\n' "$(uname -srmo)"
printf 'User:   %s (uid=%s)\n\n' "$(id -un)" "$(id -u)"

for command in "${required[@]}"; do
  if command -v "$command" >/dev/null 2>&1; then
    printf '[ok]      %s -> %s\n' "$command" "$(command -v "$command")"
  else
    printf '[missing] %s\n' "$command"
    failed=1
  fi
done

for command in "${optional[@]}"; do
  if command -v "$command" >/dev/null 2>&1; then
    printf '[optional ok] %s\n' "$command"
  else
    printf '[optional --] %s\n' "$command"
  fi
done

if [[ -r /dev/net/tun ]]; then
  echo '[ok]      /dev/net/tun'
else
  echo '[missing] /dev/net/tun (load tun module or use a VM with TUN support)'
fi

if [[ $failed -ne 0 ]]; then
  exit 1
fi
