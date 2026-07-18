from __future__ import annotations

import argparse
import os
import select
import socket
import struct
import time

from pynetlab.packet.icmp import IcmpEcho


def ping(host: str, timeout: float, sequence: int) -> bool:
    destination = socket.gethostbyname(host)
    identifier = os.getpid() & 0xFFFF
    sent_at = time.monotonic()
    payload = struct.pack("!d", sent_at) + b"PyNetLab" * 4
    request = IcmpEcho(8, 0, identifier, sequence, payload).build()

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        sock.sendto(request, (destination, 0))
        deadline = sent_at + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                print(f"timeout from {destination}")
                return False
            readable, _, _ = select.select([sock], [], [], remaining)
            if not readable:
                print(f"timeout from {destination}")
                return False
            packet, address = sock.recvfrom(65535)
            ihl = (packet[0] & 0x0F) * 4
            reply = IcmpEcho.parse(packet[ihl:])
            if reply.type == 0 and reply.identifier == identifier and reply.sequence == sequence:
                elapsed = (time.monotonic() - sent_at) * 1000
                print(f"reply from {address[0]}: seq={sequence} time={elapsed:.2f} ms")
                return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Raw ICMP echo client")
    parser.add_argument("host")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    try:
        ok = ping(args.host, args.timeout, 1)
    except PermissionError:
        raise SystemExit("Permission denied. Run with sudo or grant CAP_NET_RAW.") from None
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
