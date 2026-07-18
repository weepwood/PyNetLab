from __future__ import annotations

import argparse
import socket
import ssl
from urllib.parse import urlsplit


def fetch(url: str) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL must start with http:// or https://")
    use_tls = parsed.scheme == "https"
    port = parsed.port or (443 if use_tls else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {parsed.hostname}\r\n"
        "User-Agent: PyNetLab/0.1\r\n"
        "Accept: */*\r\n"
        "Connection: close\r\n\r\n"
    ).encode("ascii")

    with socket.create_connection((parsed.hostname, port), timeout=10) as raw:
        if use_tls:
            context = ssl.create_default_context()
            sock = context.wrap_socket(raw, server_hostname=parsed.hostname)
        else:
            sock = raw
        with sock:
            sock.sendall(request)
            chunks: list[bytes] = []
            while chunk := sock.recv(65_536):
                chunks.append(chunk)
    return b"".join(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal HTTP/1.1 client built on socket + ssl")
    parser.add_argument("url", nargs="?", default="https://example.com/")
    args = parser.parse_args()
    response = fetch(args.url)
    print(response.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
