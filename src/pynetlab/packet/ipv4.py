from __future__ import annotations

import ipaddress
import struct
from dataclasses import dataclass

from pynetlab.packet.checksum import internet_checksum

_BASE = struct.Struct("!BBHHHBBH4s4s")


@dataclass(frozen=True, slots=True)
class IPv4Packet:
    source: str
    destination: str
    protocol: int
    payload: bytes
    ttl: int = 64
    identification: int = 0
    flags_fragment: int = 0
    tos: int = 0
    options: bytes = b""

    @classmethod
    def parse(cls, data: bytes) -> IPv4Packet:
        if len(data) < _BASE.size:
            raise ValueError("truncated IPv4 header")
        (
            version_ihl,
            tos,
            total_length,
            identification,
            flags_fragment,
            ttl,
            protocol,
            _checksum,
            source,
            destination,
        ) = _BASE.unpack_from(data)
        version = version_ihl >> 4
        ihl = (version_ihl & 0x0F) * 4
        if version != 4 or ihl < 20 or len(data) < ihl:
            raise ValueError("invalid IPv4 header")
        if total_length < ihl or total_length > len(data):
            raise ValueError("invalid IPv4 total length")
        return cls(
            str(ipaddress.ip_address(source)),
            str(ipaddress.ip_address(destination)),
            protocol,
            data[ihl:total_length],
            ttl,
            identification,
            flags_fragment,
            tos,
            data[20:ihl],
        )

    def build(self) -> bytes:
        if len(self.options) % 4:
            raise ValueError("IPv4 options must be aligned to 4 bytes")
        ihl_words = 5 + len(self.options) // 4
        version_ihl = (4 << 4) | ihl_words
        total_length = ihl_words * 4 + len(self.payload)
        header = (
            _BASE.pack(
                version_ihl,
                self.tos,
                total_length,
                self.identification,
                self.flags_fragment,
                self.ttl,
                self.protocol,
                0,
                ipaddress.ip_address(self.source).packed,
                ipaddress.ip_address(self.destination).packed,
            )
            + self.options
        )
        checksum = internet_checksum(header)
        header = bytearray(header)
        struct.pack_into("!H", header, 10, checksum)
        return bytes(header) + self.payload
