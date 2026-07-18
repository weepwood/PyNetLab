from __future__ import annotations

import struct
from dataclasses import dataclass

from pynetlab.packet.checksum import internet_checksum

_HEADER = struct.Struct("!BBHHH")


@dataclass(frozen=True, slots=True)
class IcmpEcho:
    type: int
    code: int
    identifier: int
    sequence: int
    payload: bytes

    @classmethod
    def parse(cls, data: bytes) -> IcmpEcho:
        if len(data) < _HEADER.size:
            raise ValueError("truncated ICMP echo packet")
        type_, code, _checksum, identifier, sequence = _HEADER.unpack_from(data)
        return cls(type_, code, identifier, sequence, data[_HEADER.size :])

    def build(self) -> bytes:
        packet = (
            _HEADER.pack(self.type, self.code, 0, self.identifier, self.sequence) + self.payload
        )
        checksum = internet_checksum(packet)
        return (
            _HEADER.pack(self.type, self.code, checksum, self.identifier, self.sequence)
            + self.payload
        )
