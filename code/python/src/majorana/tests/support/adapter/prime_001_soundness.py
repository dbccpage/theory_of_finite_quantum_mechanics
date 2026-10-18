"""Prime 001: dual adapter soundness + loss accounting operation. AuthorityEffect: None."""

from __future__ import annotations

from typing import List, Optional, Tuple

from ..type.prime.adapter import (
    AdapterCheck,
    AdapterStatus,
    LossEntry,
    LossLedger,
)


def check_adapter(
    *,
    placement: str,
    source_typed: bool,
    locus_grounded: bool,
    adapter_adequate: bool,
    preserves_authority_fence: bool,
    losses: Optional[List[Tuple[str, str]]] = None,
) -> AdapterCheck:
    """Soundness check for intake or transport adapter (no math)."""
    entries = tuple(LossEntry(field_name=name, reason=reason) for name, reason in losses or [])
    ledger = LossLedger(entries=entries)

    if not source_typed:
        return AdapterCheck(
            placement=placement,
            status=AdapterStatus.REFUSED_UNTYPED,
            loss_ledger=ledger.entries,
            reason="REFUSED_UNTYPED",
            enters_dda_trace=False,
        )
    if not locus_grounded:
        return AdapterCheck(
            placement=placement,
            status=AdapterStatus.REFUSED_UNGROUNDED_LOCUS,
            loss_ledger=ledger.entries,
            reason="REFUSED_UNGROUNDED_LOCUS",
            enters_dda_trace=False,
        )
    if not adapter_adequate or not preserves_authority_fence:
        return AdapterCheck(
            placement=placement,
            status=AdapterStatus.ADAPTER_INADEQUATE,
            loss_ledger=ledger.entries,
            reason="ADAPTER_INADEQUATE",
            enters_dda_trace=False,
        )
    # Losses allowed if recorded
    return AdapterCheck(
        placement=placement,
        status=AdapterStatus.ADMITTED,
        loss_ledger=ledger.entries,
        reason="ADMITTED",
        enters_dda_trace=False,
    )
