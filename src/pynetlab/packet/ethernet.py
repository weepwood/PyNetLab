from __future__ import annotations

import struct
from dataclasses import dataclass

from pynetlab.packet.utils import format_mac, parse_mac

_HEADER = struct.Struct("!6s6sH")


@dataclass(frozen=True, slots=True)
class EthernetFrame:
    destination: str
    source: str
    ether_type: int
    payload: bytes

    @classmethod
    def parse(cls, data: bytes) -> EthernetFrame:
        if len(data) < _HEADER.size:
            raise ValueError("truncated Ethernet frame")
        destination, source, ether_type = _HEADER.unpack_from(data)
        return cls(format_mac(destination), format_mac(source), ether_type, data[_HEADER.size :])

    def build(self) -> bytes:
        return (
            _HEADER.pack(parse_mac(self.destination), parse_mac(self.source), self.ether_type)
            + self.payload
        )
