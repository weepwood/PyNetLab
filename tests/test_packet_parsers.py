from __future__ import annotations

import unittest

from pynetlab.packet.arp import ArpPacket
from pynetlab.packet.checksum import internet_checksum
from pynetlab.packet.ethernet import EthernetFrame
from pynetlab.packet.icmp import IcmpEcho
from pynetlab.packet.ipv4 import IPv4Packet
from pynetlab.packet.tcp import TcpSegment
from pynetlab.packet.udp import UdpDatagram


class PacketTests(unittest.TestCase):
    def test_checksum_known_vector(self) -> None:
        self.assertEqual(internet_checksum(bytes.fromhex("0001f203f4f5f6f7")), 0x220D)

    def test_ethernet_round_trip(self) -> None:
        frame = EthernetFrame("ff:ff:ff:ff:ff:ff", "02:00:00:00:00:01", 0x0800, b"abc")
        self.assertEqual(EthernetFrame.parse(frame.build()), frame)

    def test_arp_round_trip(self) -> None:
        packet = ArpPacket(1, "02:00:00:00:00:01", "10.0.0.1", "00:00:00:00:00:00", "10.0.0.2")
        self.assertEqual(ArpPacket.parse(packet.build()), packet)

    def test_ipv4_icmp_round_trip(self) -> None:
        echo = IcmpEcho(8, 0, 7, 9, b"hello")
        ip = IPv4Packet("10.0.0.1", "10.0.0.2", 1, echo.build(), identification=42)
        parsed_ip = IPv4Packet.parse(ip.build())
        parsed_echo = IcmpEcho.parse(parsed_ip.payload)
        self.assertEqual((parsed_ip.source, parsed_ip.destination), ("10.0.0.1", "10.0.0.2"))
        self.assertEqual(parsed_echo, echo)

    def test_udp_round_trip(self) -> None:
        udp = UdpDatagram(1000, 2000, b"payload")
        self.assertEqual(UdpDatagram.parse(udp.build("10.0.0.1", "10.0.0.2")), udp)

    def test_tcp_parse(self) -> None:
        raw = bytes.fromhex("04d2005000000001000000025018123400000000") + b"data"
        segment = TcpSegment.parse(raw)
        self.assertEqual(segment.source_port, 1234)
        self.assertEqual(segment.flag_names, ("ACK", "PSH"))
        self.assertEqual(segment.payload, b"data")

    def test_truncated_packets(self) -> None:
        for parser in (
            EthernetFrame.parse,
            ArpPacket.parse,
            IPv4Packet.parse,
            IcmpEcho.parse,
            UdpDatagram.parse,
            TcpSegment.parse,
        ):
            with self.subTest(parser=parser.__qualname__), self.assertRaises(ValueError):
                parser(b"\x00")


if __name__ == "__main__":
    unittest.main()
