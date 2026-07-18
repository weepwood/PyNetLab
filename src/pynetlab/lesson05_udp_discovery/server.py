from __future__ import annotations

import argparse
import json
import logging
import socket

from pynetlab.common.config import DEFAULT_DISCOVERY_PORT
from pynetlab.common.logging import configure_logging

DISCOVERY_MAGIC = b"PYNETLAB_DISCOVER_V1"
LOGGER = logging.getLogger("discovery-server")


def serve(bind_host: str, port: int, service_port: int, name: str) -> None:
    response = json.dumps(
        {"protocol": "pynetlab-discovery-v1", "name": name, "service_port": service_port}
    ).encode("utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind_host, port))
        LOGGER.info("waiting for discovery packets on udp://%s:%s", bind_host, port)
        while True:
            data, address = sock.recvfrom(1024)
            if data == DISCOVERY_MAGIC:
                LOGGER.info("discovery request from %s:%s", *address)
                sock.sendto(response, address)


def main() -> None:
    parser = argparse.ArgumentParser(description="LAN UDP service discovery responder")
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=DEFAULT_DISCOVERY_PORT)
    parser.add_argument("--service-port", type=int, default=9010)
    parser.add_argument("--name", default=socket.gethostname())
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    configure_logging(args.verbose)
    try:
        serve(args.bind, args.port, args.service_port, args.name)
    except KeyboardInterrupt:
        LOGGER.info("server stopped")


if __name__ == "__main__":
    main()
