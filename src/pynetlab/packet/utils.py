from __future__ import annotations


def format_mac(value: bytes) -> str:
    if len(value) != 6:
        raise ValueError("MAC address must be 6 bytes")
    return ":".join(f"{part:02x}" for part in value)


def parse_mac(value: str) -> bytes:
    parts = value.split(":")
    if len(parts) != 6:
        raise ValueError("MAC address must contain six octets")
    try:
        result = bytes(int(part, 16) for part in parts)
    except ValueError as exc:
        raise ValueError("invalid MAC address") from exc
    if len(result) != 6:
        raise ValueError("invalid MAC address")
    return result


def hexdump(data: bytes, width: int = 16) -> str:
    lines: list[str] = []
    for offset in range(0, len(data), width):
        chunk = data[offset : offset + width]
        hex_part = " ".join(f"{value:02x}" for value in chunk)
        ascii_part = "".join(chr(value) if 32 <= value < 127 else "." for value in chunk)
        lines.append(f"{offset:04x}  {hex_part:<{width * 3}}  {ascii_part}")
    return "\n".join(lines)
