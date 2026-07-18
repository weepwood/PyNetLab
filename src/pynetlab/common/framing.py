from __future__ import annotations

import asyncio
import json
import socket
import struct
from collections.abc import Mapping
from typing import Any

from pynetlab.common.config import MAX_FRAME_SIZE

_HEADER = struct.Struct("!I")


class ProtocolError(Exception):
    """Raised when a peer sends an invalid application frame."""


def encode_payload(payload: bytes) -> bytes:
    if len(payload) > MAX_FRAME_SIZE:
        raise ProtocolError(f"frame exceeds {MAX_FRAME_SIZE} bytes")
    return _HEADER.pack(len(payload)) + payload


def encode_json(message: Mapping[str, Any]) -> bytes:
    payload = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return encode_payload(payload)


def decode_json(payload: bytes) -> dict[str, Any]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("frame body is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ProtocolError("JSON frame must contain an object")
    return value


def recv_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise EOFError("peer closed the connection")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def recv_frame(sock: socket.socket) -> bytes:
    header = recv_exact(sock, _HEADER.size)
    (size,) = _HEADER.unpack(header)
    if size > MAX_FRAME_SIZE:
        raise ProtocolError(f"declared frame size {size} exceeds limit")
    return recv_exact(sock, size)


def recv_json(sock: socket.socket) -> dict[str, Any]:
    return decode_json(recv_frame(sock))


def send_json(sock: socket.socket, message: Mapping[str, Any]) -> None:
    sock.sendall(encode_json(message))


async def read_frame(reader: asyncio.StreamReader) -> bytes:
    header = await reader.readexactly(_HEADER.size)
    (size,) = _HEADER.unpack(header)
    if size > MAX_FRAME_SIZE:
        raise ProtocolError(f"declared frame size {size} exceeds limit")
    return await reader.readexactly(size)


async def read_json(reader: asyncio.StreamReader) -> dict[str, Any]:
    return decode_json(await read_frame(reader))


async def write_json(writer: asyncio.StreamWriter, message: Mapping[str, Any]) -> None:
    writer.write(encode_json(message))
    await writer.drain()
