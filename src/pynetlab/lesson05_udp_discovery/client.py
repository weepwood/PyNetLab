from __future__ import annotations

import argparse
import json
import socket
import time

from pynetlab.common.config import DEFAULT_DISCOVERY_PORT
from pynetlab.lesson05_udp_discovery.server import DISCOVERY_MAGIC


def discover(port: int, timeout: float) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    seen: set[tuple[str, int]] = set()
    deadline = time.monotonic() + timeout
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(0.2)
        sock.bind(("0.0.0.0", 0))
        sock.sendto(DISCOVERY_MAGIC, ("255.255.255.255", port))
        while time.monotonic() < deadline:
            try:
                data, address = sock.recvfrom(4096)
            except TimeoutError:
                continue
            if address in seen:
                continue
            seen.add(address)
            try:
                metadata = json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if isinstance(metadata, dict):
                metadata["address"] = address[0]
                found.append(metadata)
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover PyNetLab services on the LAN")
    parser.add_argument("--port", type=int, default=DEFAULT_DISCOVERY_PORT)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    results = discover(args.port, args.timeout)
    if not results:
        print("No services found. Check firewall and local network broadcast settings.")
        return
    for item in results:
        print(item)


if __name__ == "__main__":
    main()
