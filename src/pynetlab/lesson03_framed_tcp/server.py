from __future__ import annotations

import argparse
import logging
import socket
import threading
import time

from pynetlab.common.config import DEFAULT_HOST
from pynetlab.common.framing import ProtocolError, recv_json, send_json
from pynetlab.common.logging import configure_logging

PORT = 9002
LOGGER = logging.getLogger("framed-tcp-server")


def handle_client(conn: socket.socket, address: tuple[str, int]) -> None:
    with conn:
        LOGGER.info("connected: %s:%s", *address)
        try:
            while True:
                message = recv_json(conn)
                response = {
                    "type": "ack",
                    "request_id": message.get("request_id"),
                    "received": message,
                    "server_time_ns": time.time_ns(),
                }
                send_json(conn, response)
        except EOFError:
            LOGGER.info("disconnected: %s:%s", *address)
        except ProtocolError as exc:
            LOGGER.warning("protocol error from %s:%s: %s", *address, exc)


def serve(host: str, port: int) -> None:
    with socket.create_server((host, port)) as server:
        LOGGER.info("listening on tcp://%s:%s", host, port)
        while True:
            conn, address = server.accept()
            threading.Thread(target=handle_client, args=(conn, address), daemon=True).start()


def main() -> None:
    parser = argparse.ArgumentParser(description="Length-prefixed JSON TCP server")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    configure_logging(args.verbose)
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        LOGGER.info("server stopped")


if __name__ == "__main__":
    main()
