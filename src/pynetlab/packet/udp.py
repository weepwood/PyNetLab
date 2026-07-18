from __future__ import annotations

import ipaddress
import struct
from dataclasses import dataclass

from pynetlab.packet.checksum import internet_checksum

_HEADER = struct.Struct("!HHHH")


@dataclass(frozen=True, slots=True)
class UdpDatagram:
    source_port: int
    destination_port: int
    payload: bytes

    @classmethod
    def parse(cls, data: bytes) -> UdpDatagram:
        if len(data) < _HEADER.size:
            raise ValueError("truncated UDP header")
        source, destination, length, _checksum = _HEADER.unpack_from(data)
        if length < _HEADER.size or length > len(data):
            raise ValueError("invalid UDP length")
        return cls(source, destination, data[_HEADER.size : length])

    def build(self, source_ip: str | None = None, destination_ip: str | None = None) -> bytes:
        length = _HEADER.size + len(self.payload)
        header = _HEADER.pack(self.source_port, self.destination_port, length, 0)
        if source_ip is None or destination_ip is None:
            return header + self.payload
        pseudo = (
            ipaddress.ip_address(source_ip).packed
            + ipaddress.ip_address(destination_ip).packed
            + struct.pack("!BBH", 0, 17, length)
        )
        checksum = internet_checksum(pseudo + header + self.payload) or 0xFFFF
        return (
            _HEADER.pack(self.source_port, self.destination_port, length, checksum) + self.payload
        )
