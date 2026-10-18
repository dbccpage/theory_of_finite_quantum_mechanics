"""Prime 000: declaration admission stage (OE001-02). AuthorityEffect: None."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..type.prime.declaration import (
    DECLARATION_STEPS,
    AdmissionDecision,
    AdmissionKind,
    DeclarationPacket,
)


def admit_declaration(packet: DeclarationPacket) -> AdmissionDecision:
    """Validate 7-step order with hard early refusal (no math)."""
    steps: List[Dict[str, Any]] = []
    filled: List[str] = []

    def ok(name: str, note: str) -> None:
        filled.append(name)
        steps.append({"step": name, "status": "OK", "note": note})

    def refuse(kind: AdmissionKind, name: str, reason: str) -> AdmissionDecision:
        steps.append({"step": name, "status": "REFUSED", "reason": reason})
        return AdmissionDecision(
            kind=kind,
            filled_steps=tuple(filled),
            reason=reason,
            steps=tuple(steps),
        )

    if not packet.locus_hash:
        return refuse(
            AdmissionKind.REFUSE_MISSING_LOCUS,
            "locus_grounding",
            "MISSING_locus_hash",
        )
    ok("locus_grounding", f"locus={packet.locus_hash}")

    if not packet.carrier:
        return refuse(
            AdmissionKind.REFUSE_MISSING_CARRIER, "carrier", "MISSING_carrier"
        )
    ok("carrier", f"carrier={packet.carrier}")

    if not packet.observer:
        return refuse(
            AdmissionKind.REFUSE_MISSING_OBSERVER, "observer", "MISSING_observer"
        )
    ok("observer", f"observer={packet.observer}")

    if not packet.primitive_difference:
        return refuse(
            AdmissionKind.REFUSE_MISSING_PRIMITIVE_DIFFERENCE,
            "primitive_difference",
            "MISSING_primitive_difference",
        )
    ok("primitive_difference", f"δ={packet.primitive_difference}")

    if not packet.zero_rel:
        return refuse(
            AdmissionKind.REFUSE_MISSING_ZERO_REL, "zero_rel", "MISSING_zero_rel"
        )
    ok("zero_rel", f"ZeroRel={packet.zero_rel}")

    if not packet.witness and not packet.refusal_route:
        return refuse(
            AdmissionKind.REFUSE_MISSING_WITNESS,
            "witness_or_refusal",
            "MISSING_witness_or_refusal_route",
        )
    ok(
        "witness_or_refusal",
        f"witness={packet.witness!r} refusal_route={packet.refusal_route!r}",
    )

    if packet.request_split:
        steps.append({"step": "optional_policy", "status": "SPLIT"})
        return AdmissionDecision(
            kind=AdmissionKind.SPLIT_PACKET,
            filled_steps=tuple(filled + ["optional_policy"]),
            reason="SPLIT_PACKET",
            steps=tuple(steps),
        )
    if packet.request_lift:
        steps.append({"step": "optional_policy", "status": "LIFT"})
        return AdmissionDecision(
            kind=AdmissionKind.REQUEST_LIFT,
            filled_steps=tuple(filled + ["optional_policy"]),
            reason="REQUEST_LIFT",
            steps=tuple(steps),
        )

    ok("optional_policy", "default_pass")
    return AdmissionDecision(
        kind=AdmissionKind.ACCEPT_DECLARATION,
        filled_steps=tuple(filled),
        reason="ALL_STEPS_OK",
        steps=tuple(steps),
    )
