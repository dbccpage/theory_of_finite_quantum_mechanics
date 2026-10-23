# -*- coding: utf-8 -*-
"""
Process-private sealing for objects only the CODA stack may produce.

Authority tokens and computed evidence carry an HMAC-SHA256 seal under a key drawn
from ``secrets`` when this module is imported. Data handed in by a proposer cannot
carry a valid seal, so it cannot pass for a minted token or for evidence the stack
computed. The key lives in process memory: the boundary this defends is data from
proposers, not code running inside the same interpreter.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from typing import Any

_PROCESS_KEY = secrets.token_bytes(32)


def canonical_bytes(obj: Any) -> bytes:
    """Deterministic JSON bytes (sorted keys, compact, ASCII) for hashing and MACs."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def seal(purpose: str, obj: Any) -> str:
    return hmac.new(_PROCESS_KEY, purpose.encode("ascii") + b"\x00" + canonical_bytes(obj), hashlib.sha256).hexdigest()


def seal_ok(purpose: str, obj: Any, mac: Any) -> bool:
    if not isinstance(mac, str) or not mac.isascii():
        return False
    try:
        expected = seal(purpose, obj)
    except (TypeError, ValueError):
        return False
    return hmac.compare_digest(expected, mac)
