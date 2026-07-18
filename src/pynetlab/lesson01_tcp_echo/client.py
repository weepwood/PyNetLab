from __future__ import annotations

import argparse
import socket

from pynetlab.common.config import DEFAULT_HOST, DEFAULT_TCP_PORT


def chat(host: str, port: int) -> None:
    with socket.create_connection((host, port), timeout=5) as sock:
        file = sock.makefile("rwb")
        print("Connected. Enter text; Ctrl+C/Ctrl+Z ends the client.")
        while True:
            try:
                message = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                return
            file.write(message.encode("utf-8") + b"\n")
            file.flush()
            response = file.readline()
            if not response:
                raise ConnectionError("server closed the connection")
            print(response.decode("utf-8").rstrip())


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP echo client")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_TCP_PORT)
    args = parser.parse_args()
    chat(args.host, args.port)


if __name__ == "__main__":
    main()
