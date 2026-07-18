#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $EUID -ne 0 ]]; then
  echo 'Run with sudo.' >&2
  exit 1
fi

"$(dirname "$0")/cleanup.sh" >/dev/null 2>&1 || true
ip netns add pynet-a
ip netns add pynet-b
ip link add veth-a type veth peer name veth-b
ip link set veth-a netns pynet-a
ip link set veth-b netns pynet-b
ip -n pynet-a addr add 10.10.0.1/24 dev veth-a
ip -n pynet-b addr add 10.10.0.2/24 dev veth-b
ip -n pynet-a link set lo up
ip -n pynet-b link set lo up
ip -n pynet-a link set veth-a up
ip -n pynet-b link set veth-b up

echo 'Created pynet-a(10.10.0.1) <-> pynet-b(10.10.0.2)'
echo 'Test: sudo ip netns exec pynet-a ping -c 2 10.10.0.2'
