#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
DEV=${1:-eth0}
tc qdisc del dev "$DEV" root 2>/dev/null || true
echo "Cleared qdisc on $DEV"
