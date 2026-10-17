"""Sortable, namespaced identities for OreoFlow control-plane records."""

from __future__ import annotations

import secrets
import time
from typing import Literal

IdKind = Literal["building", "floor", "room", "run", "task", "message", "correlation", "artifact"]

_PREFIXES: dict[IdKind, str] = {
    "building": "bld",
    "floor": "flr",
    "room": "room",
    "run": "run",
    "task": "task",
    "message": "msg",
    "correlation": "corr",
    "artifact": "art",
}


def new_id(kind: IdKind) -> str:
    """Return a lexically sortable opaque ID; IDs never carry authority."""
    milliseconds = int(time.time_ns() // 1_000_000)
    return f"{_PREFIXES[kind]}_{milliseconds:013x}{secrets.token_hex(6)}"
