from __future__ import annotations

import argparse
import os
import subprocess

from pynetlab.packet.icmp import IcmpEcho
from pynetlab.packet.ipv4 import IPv4Packet
from pynetlab.tun.device import open_tun


def configure(name: str, address: str) -> None:
    subprocess.run(["ip", "addr", "replace", address, "dev", name], check=True)
    subprocess.run(["ip", "link", "set", name, "up"], check=True)


def serve(name: str, address: str) -> None:
    fd, actual_name = open_tun(name)
    configure(actual_name, address)
    print(f"TUN {actual_name} ready at {address}; press Ctrl+C to stop")
    try:
        while True:
            packet_data = os.read(fd, 65535)
            try:
                packet = IPv4Packet.parse(packet_data)
            except ValueError:
                continue
            if packet.protocol != 1:
                continue
            try:
                echo = IcmpEcho.parse(packet.payload)
            except ValueError:
                continue
            if echo.type != 8:
                continue
            reply = IcmpEcho(0, 0, echo.identifier, echo.sequence, echo.payload).build()
            response = IPv4Packet(
                packet.destination, packet.source, 1, reply, identification=packet.identification
            ).build()
            os.write(fd, response)
    finally:
        os.close(fd)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Userspace ICMP echo responder backed by Linux TUN"
    )
    parser.add_argument("--name", default="pynet0")
    parser.add_argument("--address", default="10.99.0.1/24")
    args = parser.parse_args()
    try:
        serve(args.name, args.address)
    except PermissionError:
        raise SystemExit("Run with sudo or grant CAP_NET_ADMIN.") from None


if __name__ == "__main__":
    main()
