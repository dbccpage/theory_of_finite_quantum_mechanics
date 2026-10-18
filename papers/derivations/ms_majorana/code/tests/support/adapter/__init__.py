"""Adapter crate: transport boundaries, loss ledgers, and adapter soundness."""

from __future__ import annotations

from ..type.prime.adapter import (
    AdapterCheck,
    AdapterStatus,
    LossEntry,
    LossLedger,
)
from .prime_001_soundness import check_adapter

__all__ = (
    "AdapterCheck",
    "AdapterStatus",
    "LossEntry",
    "LossLedger",
    "check_adapter",
)
