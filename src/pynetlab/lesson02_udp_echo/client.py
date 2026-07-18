from __future__ import annotations

import argparse
import socket

from pynetlab.common.config import DEFAULT_HOST, DEFAULT_UDP_PORT


def request(host: str, port: int, message: str, timeout: float) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(message.encode("utf-8"), (host, port))
        try:
            data, address = sock.recvfrom(65_507)
        except TimeoutError:
            raise SystemExit("No UDP response before timeout") from None
        print(f"{address[0]}:{address[1]} -> {data.decode('utf-8', errors='replace')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP echo client")
    parser.add_argument("message", nargs="?", default="hello udp")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_UDP_PORT)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()
    request(args.host, args.port, args.message, args.timeout)


if __name__ == "__main__":
    main()
