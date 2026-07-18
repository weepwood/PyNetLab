from __future__ import annotations

import ipaddress
import struct
from dataclasses import dataclass

from pynetlab.packet.utils import format_mac, parse_mac

_HEADER = struct.Struct("!HHBBH6s4s6s4s")


@dataclass(frozen=True, slots=True)
class ArpPacket:
    operation: int
    sender_mac: str
    sender_ip: str
    target_mac: str
    target_ip: str
    hardware_type: int = 1
    protocol_type: int = 0x0800

    @classmethod
    def parse(cls, data: bytes) -> ArpPacket:
        if len(data) < _HEADER.size:
            raise ValueError("truncated ARP packet")
        htype, ptype, hlen, plen, op, smac, sip, tmac, tip = _HEADER.unpack_from(data)
        if hlen != 6 or plen != 4:
            raise ValueError("unsupported ARP address sizes")
        return cls(
            op,
            format_mac(smac),
            str(ipaddress.ip_address(sip)),
            format_mac(tmac),
            str(ipaddress.ip_address(tip)),
            htype,
            ptype,
        )

    def build(self) -> bytes:
        return _HEADER.pack(
            self.hardware_type,
            self.protocol_type,
            6,
            4,
            self.operation,
            parse_mac(self.sender_mac),
            ipaddress.ip_address(self.sender_ip).packed,
            parse_mac(self.target_mac),
            ipaddress.ip_address(self.target_ip).packed,
        )
