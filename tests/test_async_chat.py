from __future__ import annotations

import asyncio
import contextlib
import unittest

from pynetlab.common.framing import read_json, write_json
from pynetlab.lesson04_async_chat.server import ROOM, handle_client


class AsyncChatTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        async with ROOM.lock:
            ROOM.clients.clear()
        self.server = await asyncio.start_server(handle_client, "127.0.0.1", 0)
        socket = self.server.sockets[0]
        self.port = socket.getsockname()[1]
        self.serve_task = asyncio.create_task(self.server.serve_forever())

    async def asyncTearDown(self) -> None:
        self.server.close()
        await self.server.wait_closed()
        self.serve_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self.serve_task
        async with ROOM.lock:
            clients = list(ROOM.clients)
            ROOM.clients.clear()
        for client in clients:
            client.writer.close()
            with contextlib.suppress(Exception):
                await client.writer.wait_closed()

    async def connect(self, name: str):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)
        await write_json(writer, {"type": "hello", "name": name})
        ready = await asyncio.wait_for(read_json(reader), timeout=1)
        self.assertEqual(ready["type"], "ready")
        return reader, writer

    async def test_two_clients_can_exchange_message(self) -> None:
        alice_reader, alice_writer = await self.connect("alice")
        self.assertEqual((await read_json(alice_reader))["type"], "system")

        bob_reader, bob_writer = await self.connect("bob")
        self.assertEqual((await read_json(alice_reader))["text"], "bob joined")
        self.assertEqual((await read_json(bob_reader))["text"], "bob joined")

        await write_json(alice_writer, {"type": "chat", "text": "hello"})
        alice_message = await asyncio.wait_for(read_json(alice_reader), timeout=1)
        bob_message = await asyncio.wait_for(read_json(bob_reader), timeout=1)
        self.assertEqual(alice_message["text"], "hello")
        self.assertEqual(bob_message["from"], "alice")

        alice_writer.close()
        bob_writer.close()
        await alice_writer.wait_closed()
        await bob_writer.wait_closed()

    async def test_duplicate_name_is_rejected(self) -> None:
        first_reader, first_writer = await self.connect("same")
        self.assertEqual((await read_json(first_reader))["type"], "system")

        second_reader, second_writer = await asyncio.open_connection("127.0.0.1", self.port)
        await write_json(second_writer, {"type": "hello", "name": "same"})
        error = await asyncio.wait_for(read_json(second_reader), timeout=1)
        self.assertEqual(error["type"], "error")

        first_writer.close()
        second_writer.close()
        await first_writer.wait_closed()
        await second_writer.wait_closed()


if __name__ == "__main__":
    unittest.main()
