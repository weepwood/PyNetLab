from __future__ import annotations

import fcntl
import os
import struct

TUNSETIFF = 0x400454CA
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000


def open_tun(name: str = "pynet0") -> tuple[int, str]:
    fd = os.open("/dev/net/tun", os.O_RDWR)
    ifreq = struct.pack("16sH", name.encode("ascii"), IFF_TUN | IFF_NO_PI)
    result = fcntl.ioctl(fd, TUNSETIFF, ifreq)
    actual_name = result[:16].split(b"\x00", 1)[0].decode("ascii")
    return fd, actual_name
