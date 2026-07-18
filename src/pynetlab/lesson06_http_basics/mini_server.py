from __future__ import annotations

import argparse
import json
import socket
from datetime import UTC, datetime


def serve(host: str, port: int) -> None:
    with socket.create_server((host, port)) as server:
        print(f"Listening on http://{host}:{port}")
        while True:
            conn, address = server.accept()
            with conn:
                request = conn.recv(8192)
                first_line = request.split(b"\r\n", 1)[0].decode("ascii", errors="replace")
                body = json.dumps(
                    {
                        "message": "hello from a raw socket HTTP server",
                        "request_line": first_line,
                        "client": f"{address[0]}:{address[1]}",
                        "time": datetime.now(UTC).isoformat(),
                    },
                    ensure_ascii=False,
                    indent=2,
                ).encode("utf-8")
                headers = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json; charset=utf-8\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Connection: close\r\n\r\n"
                ).encode("ascii")
                conn.sendall(headers + body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal educational HTTP/1.1 server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    main()
