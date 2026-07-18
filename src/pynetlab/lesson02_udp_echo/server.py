from __future__ import annotations

import argparse
import logging
import socket

from pynetlab.common.config import DEFAULT_HOST, DEFAULT_UDP_PORT
from pynetlab.common.logging import configure_logging

LOGGER = logging.getLogger("udp-echo-server")


def serve(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        LOGGER.info("listening on udp://%s:%s", host, port)
        while True:
            data, address = sock.recvfrom(65_507)
            LOGGER.info("received %d bytes from %s:%s", len(data), *address)
            sock.sendto(b"echo: " + data, address)


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP echo server")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_UDP_PORT)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    configure_logging(args.verbose)
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        LOGGER.info("server stopped")


if __name__ == "__main__":
    main()
