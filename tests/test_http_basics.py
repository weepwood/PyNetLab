from __future__ import annotations

import unittest
from unittest.mock import patch

from pynetlab.lesson06_http_basics.raw_client import fetch


class HttpClientTests(unittest.TestCase):
    def test_invalid_scheme(self) -> None:
        with self.assertRaises(ValueError):
            fetch("ftp://example.com/file")

    @patch("pynetlab.lesson06_http_basics.raw_client.socket.create_connection")
    def test_connection_errors_propagate(self, create_connection) -> None:
        create_connection.side_effect = TimeoutError("timeout")
        with self.assertRaises(TimeoutError):
            fetch("http://example.com/")


if __name__ == "__main__":
    unittest.main()
