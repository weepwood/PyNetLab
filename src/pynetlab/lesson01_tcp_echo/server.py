from __future__ import annotations

import argparse
import logging
import socket
import threading

from pynetlab.common.config import DEFAULT_HOST, DEFAULT_TCP_PORT
from pynetlab.common.logging import configure_logging

LOGGER = logging.getLogger("tcp-echo-server")


def handle_client(conn: socket.socket, address: tuple[str, int]) -> None:
    with conn:
        LOGGER.info("connected: %s:%s", *address)
        file = conn.makefile("rwb")
        while line := file.readline():
            LOGGER.info("received %r from %s:%s", line.rstrip(), *address)
            file.write(b"echo: " + line)
            file.flush()
        LOGGER.info("disconnected: %s:%s", *address)


def serve(host: str, port: int) -> None:
    with socket.create_server((host, port), reuse_port=False) as server:
        LOGGER.info("listening on tcp://%s:%s", host, port)
        while True:
            conn, address = server.accept()
            threading.Thread(target=handle_client, args=(conn, address), daemon=True).start()


def main() -> None:
    parser = argparse.ArgumentParser(description="Threaded newline-delimited TCP echo server")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_TCP_PORT)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    configure_logging(args.verbose)
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        LOGGER.info("server stopped")


if __name__ == "__main__":
    main()
