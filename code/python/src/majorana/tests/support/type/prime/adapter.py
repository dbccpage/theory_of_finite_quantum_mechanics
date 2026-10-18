"""Adapter types for Prime 001 soundness + loss accounting (OE002-*)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


class AdapterStatus(str, Enum):
    ADMITTED = "ADMITTED"
    REFUSED_UNTYPED = "REFUSED_UNTYPED"
    REFUSED_UNGROUNDED_LOCUS = "REFUSED_UNGROUNDED_LOCUS"
    ADAPTER_INADEQUATE = "ADAPTER_INADEQUATE"
    LOSS_LEDGER_REQUIRED = "LOSS_LEDGER_REQUIRED"


@dataclass(frozen=True)
class LossEntry:
    field_name: str
    reason: str


@dataclass(frozen=True)
class LossLedger:
    """Explicit L_adapter: what translation lost (OE002-02)."""

    entries: Tuple[LossEntry, ...] = field(default_factory=tuple)

    def add(self, field_name: str, reason: str) -> LossLedger:
        return LossLedger(entries=self.entries + (LossEntry(field_name=field_name, reason=reason),))

    def is_empty(self) -> bool:
        return len(self.entries) == 0


@dataclass(frozen=True)
class AdapterCheck:
    placement: str
    status: AdapterStatus
    loss_ledger: Tuple[LossEntry, ...]
    reason: str
    authority_effect: str = "None"
    enters_dda_trace: bool = False
