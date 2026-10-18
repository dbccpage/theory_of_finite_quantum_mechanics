"""Owner emission path for the sealed ``GtlaReceipt`` (Inspector OD-7/M7/M9).

Before this module the only ``GtlaReceipt`` producers were tests and the
hand-assembling script ``generate_rabbit_trace.py`` under the paper tree.
This module is the OWNER: it derives the four registry axes for each DDA
step receipt (via the declared ADAPT-01-partial letter tables below plus
the :mod:`axis_adapter` alias table for token validation/canonicalization),
assembles the layer path, the residual/debt/obligation ledgers, constructs
the receipt, and binds a :class:`omega_replay.DescentWitness`.

Deterministic by construction: no timestamps, no randomness; residuals in
diagnostic-bundle order; debt and obligations sorted.

AuthorityEffect: None throughout — a receipt binds bytes, never authority.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple

from omega_engine.crates.replay import DescentWitness, GtlaReceipt


from .axis_adapter import resolve_alias
from .dda import DdaTraceEngine
from omega_engine.crates.type.runtime_axes import (
    DdaLetter,
    DdaStepReceipt,
    DiagnosticClass,
    ExtensionStatus,
    RoutingTerminal,
)


class ReceiptEmissionRefusal(ValueError):
    """Typed refusal raised by the receipt emission owner.

    Attributes:
        token: machine-readable refusal token (stable; tests bind to it).
    """

    def __init__(self, token: str, detail: str = "") -> None:
        self.token = token
        super().__init__(f"{token}: {detail}" if detail else token)


# --- Declared four-axis adapter (ADAPT-01 partial; AuthorityEffect None) ---
# DdaStepReceipt carries the DiagnosticClass axis (diagnostic_after) and the
# authority axis (authority_effect) natively; routing_terminal and
# extension_status are derived per step from (letter, refusal_reason) via
# these explicit tables — a declared mapping onto types.py tokens, never a
# silent rename.

LETTER_ROUTING_DEFAULT: Dict[DdaLetter, RoutingTerminal] = {
    DdaLetter.C: RoutingTerminal.ShapeChecked,  # context exposure: shape-level
    DdaLetter.E: RoutingTerminal.Repair,  # exact repair step
    DdaLetter.R: RoutingTerminal.Refusal,  # residual projection records typed refusal routes
    DdaLetter.I: RoutingTerminal.CheckPassed,  # receipt integration
    DdaLetter.LAMBDA: RoutingTerminal.RequiresLift,  # structural lift
    DdaLetter.D: RoutingTerminal.CheckPassed,  # licensed descent
    DdaLetter.M: RoutingTerminal.Refusal,  # typed refusal
    DdaLetter.T: RoutingTerminal.CheckPassed,  # terminalization (with debt)
}

LETTER_EXTENSION: Dict[DdaLetter, ExtensionStatus] = {
    DdaLetter.LAMBDA: ExtensionStatus.LicensedLift,
    DdaLetter.D: ExtensionStatus.LicensedLift,  # descent inside the licensed lift
    DdaLetter.M: ExtensionStatus.ExtensionRefused,
}


def derive_step_axes(receipt: DdaStepReceipt) -> Dict[str, str]:
    """Derive the four registry axes for one ``DdaStepReceipt``.

    Law (declared adapter, not a silent rename):
      * ``diagnostic_class`` = ``receipt.diagnostic_after``, validated and
        canonicalized through the ADAPT-01 alias table on the
        DiagnosticClass axis (an alias spelling resolves to its registry
        token; an unknown or wrong-axis token refuses — the old
        ``"UNAVAILABLE: ..."`` string fallback is gone, fail-closed);
      * ``routing_terminal`` = ``Refusal`` when ``refusal_reason`` is set
        on a non-R step, else :data:`LETTER_ROUTING_DEFAULT` by letter;
      * ``extension_status`` = :data:`LETTER_EXTENSION` by letter, default
        ``NoExtensionNeeded``;
      * ``authority_status`` = the step's ``authority_effect``, which MUST
        be ``'None'``.

    Typed refusals: :class:`ReceiptEmissionRefusal` with token
    ``AUTHORITY_WIDENING_REFUSED`` (step authority not ``'None'``);
    :class:`axis_adapter.AliasAdapterRefusal` propagates for unregistered
    diagnostic tokens. AuthorityEffect: None.
    """
    diagnostic = resolve_alias(receipt.diagnostic_after, DiagnosticClass)
    if receipt.refusal_reason is not None and receipt.letter is not DdaLetter.R:
        routing = RoutingTerminal.Refusal
    else:
        routing = LETTER_ROUTING_DEFAULT[receipt.letter]
    extension = LETTER_EXTENSION.get(receipt.letter, ExtensionStatus.NoExtensionNeeded)
    if receipt.authority_effect != "None":
        raise ReceiptEmissionRefusal(
            "AUTHORITY_WIDENING_REFUSED",
            f"step {receipt.step_id} carries authority_effect "
            f"'{receipt.authority_effect}'; DDA Law 1 requires 'None'",
        )
    return {
        "diagnostic_class": diagnostic.value,
        "routing_terminal": routing.value,
        "extension_status": extension.value,
        "authority_status": "None",
    }


def adapter_declaration() -> dict:
    """The declared ADAPT-01-partial adapter block (embedded in traces)."""
    return {
        "id": "ADAPT-01-partial-rabbit-v1",
        "note": (
            "Declared adapter, not a silent rename: diagnostic_class = "
            "DdaStepReceipt.diagnostic_after; authority_status = "
            "DdaStepReceipt.authority_effect; routing_terminal/extension_status "
            "derived from (letter, refusal_reason) by this table."
        ),
        "routing_terminal_by_letter": {
            letter.value: terminal.value
            for letter, terminal in LETTER_ROUTING_DEFAULT.items()
        },
        "routing_terminal_override": "Refusal when refusal_reason is set (non-R steps)",
        "extension_status_by_letter": {
            letter.value: status.value for letter, status in LETTER_EXTENSION.items()
        },
        "extension_status_default": ExtensionStatus.NoExtensionNeeded.value,
        "authority_effect": "None",
    }


@dataclass(frozen=True)
class GtlaReceiptEmission:
    """Result of one owner emission: the sealed receipt + bound witness."""

    receipt: GtlaReceipt
    witness: DescentWitness
    authority_effect: str = "None"


def emit_gtla_receipt(
    *,
    claim_id: str,
    claim_sha256: str,
    scope: str,
    engine: DdaTraceEngine,
    diagnostic_bundle: Sequence[Any],
    loss_ledger: Optional[Any] = None,
    unresolved_obligations: Optional[Iterable[str]] = None,
) -> GtlaReceiptEmission:
    """Construct and witness-bind the sealed ``GtlaReceipt`` for one run.

    Inputs: the run's diagnostic bundle (validated
    ``DiagnosticResidualPacket`` rows), the terminalized DDA engine (tape +
    step receipts), and the loss ledger carrying the debt.

    Law:
      * ``residuals`` = the bundle's content-addressed fingerprints, in
        bundle order;
      * ``debt`` = the loss ledger's unresolved ``loss_id``s, sorted;
      * ``unresolved_obligations`` = the bundle's typed ``refusal_route``
        strings, deduplicated (via ``set()`` — a route repeated across
        several packets contributes one row, not one per packet) and then
        sorted for a deterministic order (or the explicit override, frozen
        as given, which is neither deduplicated nor sorted);
      * ``layer_path`` = one step dict per DDA receipt
        (``step_id`` + ``letter`` + the four axes via
        :func:`derive_step_axes`);
      * the engine must be terminalized (DDA Law 2 — a receipt binds a
        finished trace) and must satisfy Law 1 (all steps
        AuthorityEffect None);
      * the witness is bound to the receipt's own recomputed replay hash.

    Typed refusals (:class:`ReceiptEmissionRefusal`):
      * ``UNTERMINALIZED_TRACE_REFUSED`` — engine has no terminal T step;
      * ``AUTHORITY_WIDENING_REFUSED`` — any step widens authority
        (also enforced per-step in :func:`derive_step_axes`);
    plus the receipt's own ``ValueError`` refusals (token sets, hash
    shapes) and the adapter's ``AliasAdapterRefusal``.

    AuthorityEffect: None — the emission binds bytes for replay; it does
    not prove the claim and mints no authority.
    """
    if not engine.is_terminalized:
        raise ReceiptEmissionRefusal(
            "UNTERMINALIZED_TRACE_REFUSED",
            f"trace '{engine.trace_id}' has no terminal T step; a GtlaReceipt "
            f"binds a finished trace only",
        )
    if not engine.check_law1_all_none():
        raise ReceiptEmissionRefusal(
            "AUTHORITY_WIDENING_REFUSED",
            f"trace '{engine.trace_id}' carries a step with authority_effect "
            f"!= 'None' (DDA Law 1)",
        )

    residuals = tuple(pkt.residual_fingerprint for pkt in diagnostic_bundle)
    if unresolved_obligations is None:
        routes = set()
        for pkt in diagnostic_bundle:
            route = pkt.witness_or_refusal.get("refusal_route")
            if isinstance(route, str):
                routes.add(route)
        obligations: Tuple[str, ...] = tuple(sorted(routes))
    else:
        obligations = tuple(unresolved_obligations)

    if loss_ledger is None:
        debt: Tuple[str, ...] = ()
    else:
        debt = tuple(
            sorted(
                entry.loss_id
                for entry in loss_ledger.entries.values()
                if entry.discharge_status == "unresolved"
            )
        )

    layer_path = tuple(
        {
            "step_id": receipt.step_id,
            "letter": receipt.letter.value,
            **derive_step_axes(receipt),
        }
        for receipt in engine.receipts
    )

    gtla_receipt = GtlaReceipt(
        claim_id=claim_id,
        claim_sha256=claim_sha256,
        scope=scope,
        layer_path=layer_path,
        dda_tape=engine.get_tape_string(),
        residuals=residuals,
        debt=debt,
        unresolved_obligations=obligations,
    )
    witness = DescentWitness.from_verified_replay(
        gtla_receipt, gtla_receipt.replay_hash
    )
    return GtlaReceiptEmission(receipt=gtla_receipt, witness=witness)


__all__ = [
    "LETTER_ROUTING_DEFAULT",
    "LETTER_EXTENSION",
    "ReceiptEmissionRefusal",
    "GtlaReceiptEmission",
    "derive_step_axes",
    "adapter_declaration",
    "emit_gtla_receipt",
]




