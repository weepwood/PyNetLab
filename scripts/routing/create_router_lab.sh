#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
"$(dirname "$0")/../netns/cleanup.sh" >/dev/null 2>&1 || true

for ns in pynet-client pynet-router pynet-server; do ip netns add "$ns"; done
ip link add c-veth type veth peer name r-left
ip link add s-veth type veth peer name r-right
ip link set c-veth netns pynet-client
ip link set r-left netns pynet-router
ip link set s-veth netns pynet-server
ip link set r-right netns pynet-router

ip -n pynet-client addr add 10.30.1.2/24 dev c-veth
ip -n pynet-router addr add 10.30.1.1/24 dev r-left
ip -n pynet-router addr add 10.30.2.1/24 dev r-right
ip -n pynet-server addr add 10.30.2.2/24 dev s-veth

for pair in 'pynet-client c-veth' 'pynet-router r-left' 'pynet-router r-right' 'pynet-server s-veth'; do
  read -r ns dev <<<"$pair"
  ip -n "$ns" link set lo up
  ip -n "$ns" link set "$dev" up
done

ip -n pynet-client route add default via 10.30.1.1
ip -n pynet-server route add default via 10.30.2.1
ip netns exec pynet-router sysctl -q -w net.ipv4.ip_forward=1

echo 'Router lab ready.'
echo 'Test: sudo ip netns exec pynet-client ping -c 2 10.30.2.2'
