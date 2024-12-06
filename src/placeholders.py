"""Dummy module."""

import asyncio


async def some_logic() -> None:
    """Do some abstract logic."""
    await asyncio.sleep(0)


some_int: int = 1
some_string: str = ''
some_bytes: bytes = bytes(0)
