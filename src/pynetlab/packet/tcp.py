from __future__ import annotations

import struct
from dataclasses import dataclass

_BASE = struct.Struct("!HHIIHHHH")


@dataclass(frozen=True, slots=True)
class TcpSegment:
    source_port: int
    destination_port: int
    sequence: int
    acknowledgement: int
    flags: int
    window: int
    payload: bytes
    options: bytes = b""

    @classmethod
    def parse(cls, data: bytes) -> TcpSegment:
        if len(data) < _BASE.size:
            raise ValueError("truncated TCP header")
        source, destination, sequence, acknowledgement, offset_flags, window, _checksum, _urgent = (
            _BASE.unpack_from(data)
        )
        data_offset = ((offset_flags >> 12) & 0x0F) * 4
        if data_offset < 20 or data_offset > len(data):
            raise ValueError("invalid TCP data offset")
        flags = offset_flags & 0x01FF
        return cls(
            source,
            destination,
            sequence,
            acknowledgement,
            flags,
            window,
            data[data_offset:],
            data[20:data_offset],
        )

    @property
    def flag_names(self) -> tuple[str, ...]:
        mapping = (
            (0x100, "NS"),
            (0x080, "CWR"),
            (0x040, "ECE"),
            (0x020, "URG"),
            (0x010, "ACK"),
            (0x008, "PSH"),
            (0x004, "RST"),
            (0x002, "SYN"),
            (0x001, "FIN"),
        )
        return tuple(name for bit, name in mapping if self.flags & bit)
