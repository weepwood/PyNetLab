from __future__ import annotations

import socket
import unittest

from pynetlab.common.framing import ProtocolError, decode_json, encode_json, recv_json


class FramingTests(unittest.TestCase):
    def test_encode_and_receive_json(self) -> None:
        left, right = socket.socketpair()
        try:
            left.sendall(encode_json({"type": "test", "value": 42}))
            self.assertEqual(recv_json(right), {"type": "test", "value": 42})
        finally:
            left.close()
            right.close()

    def test_invalid_json_is_rejected(self) -> None:
        with self.assertRaises(ProtocolError):
            decode_json(b"not-json")

    def test_json_root_must_be_object(self) -> None:
        with self.assertRaises(ProtocolError):
            decode_json(b"[1, 2, 3]")


if __name__ == "__main__":
    unittest.main()
