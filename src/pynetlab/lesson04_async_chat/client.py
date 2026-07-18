from __future__ import annotations

import argparse
import asyncio
import contextlib

from pynetlab.common.config import DEFAULT_CHAT_PORT, DEFAULT_HOST
from pynetlab.common.framing import read_json, write_json


async def read_input(prompt: str = "") -> str:
    return await asyncio.to_thread(input, prompt)


async def receive_messages(reader: asyncio.StreamReader) -> None:
    while True:
        message = await read_json(reader)
        kind = message.get("type")
        if kind == "chat":
            print(f"\n[{message.get('from')}] {message.get('text')}")
        elif kind == "system":
            print(f"\n* {message.get('text')}")
        elif kind == "error":
            print(f"\n! {message.get('text')}")
        elif kind != "pong":
            print(f"\n{message}")


async def run(host: str, port: int, name: str) -> None:
    reader, writer = await asyncio.open_connection(host, port)
    receiver: asyncio.Task[None] | None = None
    try:
        await write_json(writer, {"type": "hello", "name": name})
        first = await read_json(reader)
        if first.get("type") == "error":
            raise RuntimeError(str(first.get("text")))
        print(f"Connected as {name}. Enter /quit to leave.")
        receiver = asyncio.create_task(receive_messages(reader))
        while True:
            text = await read_input("> ")
            if text.strip() == "/quit":
                return
            await write_json(writer, {"type": "chat", "text": text})
    finally:
        if receiver is not None:
            receiver.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await receiver
        writer.close()
        await writer.wait_closed()


def main() -> None:
    parser = argparse.ArgumentParser(description="Asyncio chat client")
    parser.add_argument("name")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_CHAT_PORT)
    args = parser.parse_args()
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(run(args.host, args.port, args.name))


if __name__ == "__main__":
    main()
