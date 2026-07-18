#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $EUID -ne 0 ]]; then
  echo 'Run with sudo.' >&2
  exit 1
fi

for ns in pynet-a pynet-b pynet-client pynet-router pynet-server; do
  ip netns del "$ns" 2>/dev/null || true
done
ip link del pynet-br0 2>/dev/null || true
