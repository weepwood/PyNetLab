from __future__ import annotations

from dataclasses import asdict
from typing import Any

from pynetlab.packet.arp import ArpPacket
from pynetlab.packet.ethernet import EthernetFrame
from pynetlab.packet.icmp import IcmpEcho
from pynetlab.packet.ipv4 import IPv4Packet
from pynetlab.packet.tcp import TcpSegment
from pynetlab.packet.udp import UdpDatagram


def decode_ethernet(data: bytes) -> dict[str, Any]:
    frame = EthernetFrame.parse(data)
    result: dict[str, Any] = {
        "ethernet": {
            "source": frame.source,
            "destination": frame.destination,
            "ether_type": hex(frame.ether_type),
        }
    }
    if frame.ether_type == 0x0806:
        result["arp"] = asdict(ArpPacket.parse(frame.payload))
    elif frame.ether_type == 0x0800:
        ip = IPv4Packet.parse(frame.payload)
        result["ipv4"] = {key: value for key, value in asdict(ip).items() if key != "payload"}
        if ip.protocol == 1:
            result["icmp"] = asdict(IcmpEcho.parse(ip.payload))
        elif ip.protocol == 6:
            tcp = TcpSegment.parse(ip.payload)
            item = asdict(tcp)
            item["flag_names"] = tcp.flag_names
            result["tcp"] = item
        elif ip.protocol == 17:
            result["udp"] = asdict(UdpDatagram.parse(ip.payload))
    return result
