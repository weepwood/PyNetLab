#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
DEV=${1:-eth0}
DELAY=${DELAY:-100ms}
LOSS=${LOSS:-2%}
RATE=${RATE:-10mbit}
tc qdisc replace dev "$DEV" root netem delay "$DELAY" loss "$LOSS" rate "$RATE"
echo "Applied to $DEV: delay=$DELAY loss=$LOSS rate=$RATE"
