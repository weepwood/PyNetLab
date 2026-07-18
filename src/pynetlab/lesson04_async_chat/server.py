from __future__ import annotations

import argparse
import asyncio
import contextlib
import logging
import time
from dataclasses import dataclass, field

from pynetlab.common.config import DEFAULT_CHAT_PORT, DEFAULT_HOST
from pynetlab.common.framing import ProtocolError, read_json, write_json
from pynetlab.common.logging import configure_logging

LOGGER = logging.getLogger("async-chat-server")


@dataclass(eq=False, slots=True)
class Client:
    name: str
    writer: asyncio.StreamWriter
    send_lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def send(self, message: dict[str, object]) -> None:
        async with self.send_lock:
            await write_json(self.writer, message)


class ChatRoom:
    def __init__(self) -> None:
        self.clients: set[Client] = set()
        self.lock = asyncio.Lock()

    async def join(self, client: Client) -> bool:
        async with self.lock:
            if any(item.name == client.name for item in self.clients):
                return False
            self.clients.add(client)
        return True

    async def leave(self, client: Client) -> None:
        async with self.lock:
            existed = client in self.clients
            self.clients.discard(client)
        if existed:
            await self.broadcast({"type": "system", "text": f"{client.name} left"})

    async def broadcast(self, message: dict[str, object]) -> None:
        async with self.lock:
            recipients = list(self.clients)
        if not recipients:
            return
        results = await asyncio.gather(
            *(client.send(message) for client in recipients), return_exceptions=True
        )
        for client, result in zip(recipients, results, strict=True):
            if isinstance(result, Exception):
                LOGGER.debug("send to %s failed: %s", client.name, result)


ROOM = ChatRoom()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    peer = writer.get_extra_info("peername")
    client: Client | None = None
    try:
        hello = await asyncio.wait_for(read_json(reader), timeout=10)
        if hello.get("type") != "hello" or not isinstance(hello.get("name"), str):
            raise ProtocolError("first message must be {'type':'hello','name':'...'}")
        name = hello["name"].strip()[:32]
        if not name:
            raise ProtocolError("name cannot be empty")
        client = Client(name=name, writer=writer)
        if not await ROOM.join(client):
            await client.send({"type": "error", "text": "name already in use"})
            return
        await client.send({"type": "ready", "name": name})
        await ROOM.broadcast({"type": "system", "text": f"{name} joined"})
        LOGGER.info("%s connected from %s", name, peer)

        while True:
            message = await read_json(reader)
            match message.get("type"):
                case "chat":
                    text = str(message.get("text", "")).strip()
                    if text:
                        await ROOM.broadcast(
                            {
                                "type": "chat",
                                "from": name,
                                "text": text[:2_000],
                                "timestamp": time.time(),
                            }
                        )
                case "ping":
                    await client.send({"type": "pong", "timestamp": time.time()})
                case _:
                    await client.send({"type": "error", "text": "unknown message type"})
    except (asyncio.IncompleteReadError, ConnectionResetError):
        pass
    except (ProtocolError, TimeoutError) as exc:
        LOGGER.warning("protocol error from %s: %s", peer, exc)
        if client is not None:
            with contextlib.suppress(Exception):
                await client.send({"type": "error", "text": str(exc)})
    finally:
        if client is not None:
            await ROOM.leave(client)
        writer.close()
        with contextlib.suppress(Exception):
            await writer.wait_closed()


async def run(host: str, port: int) -> None:
    server = await asyncio.start_server(handle_client, host, port)
    addresses = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
    LOGGER.info("listening on %s", addresses)
    async with server:
        await server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Asyncio length-prefixed chat server")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_CHAT_PORT)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    configure_logging(args.verbose)
    try:
        asyncio.run(run(args.host, args.port))
    except KeyboardInterrupt:
        LOGGER.info("server stopped")


if __name__ == "__main__":
    main()
