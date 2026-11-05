"""DDC letter I: append-only, hash-chained execution tape.

Every letter of the alphabet, I included, enters the chain:

    h_0     = SHA256(genesis_root)
    h_{t+1} = SHA256("t:h_t:letter:canonical_json(payload)")

The index, the previous head (64 hex digits) and the letter (from the closed
alphabet) cannot contain the separator, so the preimage parses uniquely.
Payloads are canonical JSON (sorted keys, no spaces); exact rationals are
written as canonical strings ("3/4", "-5"), and floats are refused.

Tamper evidence assumes SHA-256 collision resistance; that is an assumption,
not a theorem of this package. Leaf module: standard library only, loadable by
path. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List

ALPHABET = ("E", "R", "C", "I", "Λ", "D", "M", "T")
LETTER_ALIASES = {"Lambda": "Λ"}


def canonical_letter(letter: str) -> str:
    letter = LETTER_ALIASES.get(letter, letter)
    if letter not in ALPHABET:
        raise ValueError(f"UNKNOWN_LETTER: {letter!r}")
    return letter


def canonical_value(value: Any) -> Any:
    """JSON-ready copy with Fractions as canonical strings; refuses floats."""
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, float):
        raise ValueError(f"FLOAT_FORBIDDEN: {value!r}")
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        if any(not isinstance(k, str) for k in value):
            raise ValueError("NON_STRING_KEY: payload object keys must be strings")
        return {k: canonical_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [canonical_value(v) for v in value]
    raise ValueError(f"NOT_CANONICAL: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class TapeEntry:
    index: int
    prev_hash: str
    letter: str
    payload: Dict[str, Any]
    current_hash: str


@dataclass(frozen=True)
class TapeCheckpoint:
    """Head and length to retain independently of the mutable tape storage."""

    genesis_hash: str
    head_hash: str
    length: int


def entry_hash(index: int, prev_hash: str, letter: str, payload: Dict[str, Any]) -> str:
    raw = f"{index}:{prev_hash}:{letter}:{canonical_json(payload)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class ExecutionTape:
    """Append-only hash-chained execution tape for DDC letters."""

    def __init__(self, genesis_root: str = "GENESIS_TAPE_ROOT"):
        self.genesis_root = genesis_root
        self._entries: List[TapeEntry] = []

    @property
    def genesis_hash(self) -> str:
        return hashlib.sha256(self.genesis_root.encode("utf-8")).hexdigest()

    @property
    def latest_hash(self) -> str:
        return self._entries[-1].current_hash if self._entries else self.genesis_hash

    def append(self, letter: str, payload: Dict[str, Any]) -> TapeEntry:
        """Append one letter and its payload; the only way the tape grows."""
        letter = canonical_letter(letter)
        frozen = canonical_value(payload)
        index = len(self._entries)
        prev = self.latest_hash
        entry = TapeEntry(
            index=index,
            prev_hash=prev,
            letter=letter,
            payload=frozen,
            current_hash=entry_hash(index, prev, letter, frozen),
        )
        self._entries.append(entry)
        return deepcopy(entry)

    def first_broken_index(self) -> int:
        """Index of the first entry that does not chain, or -1 when all do."""
        expected_prev = self.genesis_hash
        for i, entry in enumerate(self._entries):
            if entry.index != i or entry.prev_hash != expected_prev:
                return i
            if entry.letter not in ALPHABET:
                return i
            if entry_hash(entry.index, entry.prev_hash, entry.letter, entry.payload) != entry.current_hash:
                return i
            expected_prev = entry.current_hash
        return -1

    def checkpoint(self) -> TapeCheckpoint:
        return TapeCheckpoint(self.genesis_hash, self.latest_hash, len(self._entries))

    def verify_integrity(self, checkpoint: TapeCheckpoint | None = None) -> bool:
        """Check chain consistency and, if supplied, an independently retained checkpoint.

        Without a trusted checkpoint a rehashed replacement or truncated chain
        is indistinguishable from a different valid history.
        """
        try:
            intact = self.first_broken_index() == -1
        except (TypeError, ValueError):
            return False
        return intact and (checkpoint is None or checkpoint == self.checkpoint())

    def get_entries(self) -> List[TapeEntry]:
        return deepcopy(self._entries)
