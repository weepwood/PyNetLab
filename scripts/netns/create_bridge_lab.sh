#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
"$(dirname "$0")/cleanup.sh" >/dev/null 2>&1 || true

ip link add pynet-br0 type bridge
ip link set pynet-br0 up

for n in a b; do
  ip netns add "pynet-$n"
  ip link add "veth-$n" type veth peer name "eth-$n"
  ip link set "eth-$n" netns "pynet-$n"
  ip link set "veth-$n" master pynet-br0
  ip link set "veth-$n" up
  ip -n "pynet-$n" link set lo up
  ip -n "pynet-$n" link set "eth-$n" up
done

ip -n pynet-a addr add 10.20.0.1/24 dev eth-a
ip -n pynet-b addr add 10.20.0.2/24 dev eth-b

echo 'Bridge lab ready. Capture: sudo tcpdump -i pynet-br0 -nn -e'
