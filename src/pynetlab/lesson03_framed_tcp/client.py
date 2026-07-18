from __future__ import annotations

import argparse
import socket
import uuid

from pynetlab.common.config import DEFAULT_HOST
from pynetlab.common.framing import recv_json, send_json

PORT = 9002


def request(host: str, port: int, text: str) -> None:
    message = {"type": "message", "request_id": uuid.uuid4().hex, "text": text}
    with socket.create_connection((host, port), timeout=5) as sock:
        send_json(sock, message)
        print(recv_json(sock))


def main() -> None:
    parser = argparse.ArgumentParser(description="Length-prefixed JSON TCP client")
    parser.add_argument("text", nargs="?", default="hello framed protocol")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    request(args.host, args.port, args.text)


if __name__ == "__main__":
    main()
