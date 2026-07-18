from __future__ import annotations

import argparse
import socket
import ssl
import time
from urllib.parse import urlsplit


def dns_lookup(host: str) -> int:
    started = time.perf_counter()
    records = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    elapsed_ms = (time.perf_counter() - started) * 1000
    addresses = sorted({record[4][0] for record in records})
    print(f"DNS {host} ({elapsed_ms:.1f} ms)")
    for address in addresses:
        print(f"  {address}")
    return 0


def tcp_check(host: str, port: int, timeout: float) -> int:
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except OSError as exc:
        print(f"TCP {host}:{port} failed: {exc}")
        return 1
    elapsed_ms = (time.perf_counter() - started) * 1000
    print(f"TCP {host}:{port} connected in {elapsed_ms:.1f} ms")
    return 0


def tls_check(host: str, port: int, timeout: float) -> int:
    context = ssl.create_default_context()
    started = time.perf_counter()
    try:
        with (
            socket.create_connection((host, port), timeout=timeout) as raw,
            context.wrap_socket(raw, server_hostname=host) as secure,
        ):
            cert = secure.getpeercert()
            cipher = secure.cipher()
            version = secure.version()
    except OSError as exc:
        print(f"TLS {host}:{port} failed: {exc}")
        return 1
    elapsed_ms = (time.perf_counter() - started) * 1000
    print(f"TLS {host}:{port} connected in {elapsed_ms:.1f} ms")
    print(f"  version: {version}")
    print(f"  cipher: {cipher}")
    print(f"  subject: {cert.get('subject')}")
    print(f"  expires: {cert.get('notAfter')}")
    return 0


def url_check(url: str, timeout: float) -> int:
    parsed = urlsplit(url)
    if not parsed.hostname:
        print("Invalid URL")
        return 2
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if parsed.scheme == "https":
        return tls_check(parsed.hostname, port, timeout)
    return tcp_check(parsed.hostname, port, timeout)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small cross-platform network diagnosis utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dns = subparsers.add_parser("dns", help="resolve a hostname")
    dns.add_argument("host")

    tcp = subparsers.add_parser("tcp", help="test a TCP port")
    tcp.add_argument("host")
    tcp.add_argument("port", type=int)
    tcp.add_argument("--timeout", type=float, default=5.0)

    tls = subparsers.add_parser("tls", help="perform a TLS handshake")
    tls.add_argument("host")
    tls.add_argument("--port", type=int, default=443)
    tls.add_argument("--timeout", type=float, default=5.0)

    url = subparsers.add_parser("url", help="test the network endpoint of a URL")
    url.add_argument("url")
    url.add_argument("--timeout", type=float, default=5.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "dns":
        code = dns_lookup(args.host)
    elif args.command == "tcp":
        code = tcp_check(args.host, args.port, args.timeout)
    elif args.command == "tls":
        code = tls_check(args.host, args.port, args.timeout)
    else:
        code = url_check(args.url, args.timeout)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
