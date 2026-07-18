from __future__ import annotations

import argparse
import json
import socket

from pynetlab.packet.decode import decode_ethernet
from pynetlab.packet.utils import hexdump

ETH_P_ALL = 0x0003


def sniff(interface: str, count: int, dump: bool) -> None:
    if not hasattr(socket, "AF_PACKET"):
        raise SystemExit("AF_PACKET is Linux-only")
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL)) as sock:
        sock.bind((interface, 0))
        for index in range(count):
            data, address = sock.recvfrom(65535)
            try:
                decoded = decode_ethernet(data)
            except ValueError as exc:
                decoded = {"error": str(exc)}
            print(f"#{index + 1} interface={address[0]} length={len(data)}")
            print(
                json.dumps(
                    decoded,
                    ensure_ascii=False,
                    indent=2,
                    default=lambda value: value.hex() if isinstance(value, bytes) else str(value),
                )
            )
            if dump:
                print(hexdump(data))


def main() -> None:
    parser = argparse.ArgumentParser(description="Linux AF_PACKET educational sniffer")
    parser.add_argument("--interface", required=True)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    if args.count <= 0:
        parser.error("--count must be positive")
    try:
        sniff(args.interface, args.count, args.dump)
    except PermissionError:
        raise SystemExit("Permission denied. Run with sudo or grant CAP_NET_RAW.") from None


if __name__ == "__main__":
    main()
