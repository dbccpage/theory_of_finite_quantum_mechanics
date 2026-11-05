"""Injected-fault mutants for CODA-FDA decision procedures.

Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real evaluate_authorization / derive_guards oracle
on a known packet, so the suite kills the fault if it is ever injected.
Packets match test_coda_fda._valid_packet / _green_evidence.
"""

from __future__ import annotations

from typing import Any, Optional

import pytest
from coda_fda_core import (
    DescentPacket,
    GuardEvidence,
    HaltGuards,
    derive_guards,
    evaluate_authorization,
)
from sympy import Rational


def _valid_packet() -> DescentPacket:
    return DescentPacket(
        carrier_k="carrier_demo",
        evaluator_class_e=["e0", "e1"],
        verifier_v="verifier_replay_v1",
        terminalizer_tau="tau_standing",
        discipline_lambda="no_self_promote",
    )


def _incomplete_packet() -> DescentPacket:
    return DescentPacket(
        carrier_k="",
        evaluator_class_e=["e0"],
        verifier_v="v",
        terminalizer_tau="t",
        discipline_lambda="L",
    )


def _green_evidence(**overrides) -> GuardEvidence:
    base = dict(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        residual_zero_tol=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        pending_lifts=0,
        active_refusal=False,
    )
    base.update(overrides)
    if "checked_candidate_ids" not in overrides:
        checked_n = base.get("candidates_checked", 0)
        base["checked_candidate_ids"] = tuple(f"e{i}" for i in range(checked_n))
    return GuardEvidence(**base)


def mutant_inhabit_incomplete_or_missing_packet(
    proposal_id: str,
    packet: Optional[DescentPacket],
    evidence: GuardEvidence,
    logit_confidence: Any = Rational(99, 100),
) -> bool:
    """Inhabit standing from green guards even when the packet is missing or incomplete."""
    del proposal_id, packet, logit_confidence
    return derive_guards(evidence).is_auth()


def mutant_high_confidence_without_packet(
    proposal_id: str,
    packet: Optional[DescentPacket],
    evidence: GuardEvidence,
    logit_confidence: Any = 0.99,
) -> bool:
    """Treat logit_confidence 0.99 as standing even without a packet."""
    if logit_confidence >= 0.99:
        return True
    return evaluate_authorization(
        proposal_id, packet, evidence, logit_confidence
    ).inhabited


def mutant_force_zero_residual_mass(evidence: GuardEvidence) -> HaltGuards:
    """Skip a failed residual halt guard by forcing zero_residual_mass true."""
    guards = derive_guards(evidence)
    return HaltGuards(
        accepted=guards.accepted,
        deterministic=guards.deterministic,
        zero_residual_mass=True,
        skeleton_preserving=guards.skeleton_preserving,
        exhaustive=guards.exhaustive,
        no_pending_lift=guards.no_pending_lift,
        no_refusal=guards.no_refusal,
    )


def mutant_evaluate_skip_failed_halt_guard(
    proposal_id: str,
    packet: Optional[DescentPacket],
    evidence: GuardEvidence,
) -> bool:
    if packet is None or not packet.is_valid():
        return False
    del proposal_id
    return mutant_force_zero_residual_mass(evidence).is_auth()


def mutant_green_evidence_accept_float(**overrides) -> GuardEvidence:
    """Accept a float residual_mass by coercing it instead of refusing."""
    base = dict(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        residual_zero_tol=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        pending_lifts=0,
        active_refusal=False,
    )
    base.update(overrides)
    if "checked_candidate_ids" not in overrides:
        checked_n = base.get("candidates_checked", 0)
        if isinstance(checked_n, int) and not isinstance(checked_n, bool):
            base["checked_candidate_ids"] = tuple(f"e{i}" for i in range(checked_n))
    mass = base["residual_mass"]
    if isinstance(mass, float):
        base["residual_mass"] = Rational(mass).limit_denominator()
    tol = base["residual_zero_tol"]
    if isinstance(tol, float):
        base["residual_zero_tol"] = Rational(tol).limit_denominator()
    return GuardEvidence(**base)


def mutant_derive_guards_accept_float(**overrides) -> HaltGuards:
    return derive_guards(mutant_green_evidence_accept_float(**overrides))


def mutant_evaluate_accept_float(
    proposal_id: str,
    packet: Optional[DescentPacket],
    residual_mass: Any,
) -> Any:
    return evaluate_authorization(
        proposal_id,
        packet,
        mutant_green_evidence_accept_float(residual_mass=residual_mass),
    ).inhabited


def _real_float_residual_outcome(residual_mass: Any) -> Any:
    try:
        return evaluate_authorization(
            "prop_float",
            _valid_packet(),
            _green_evidence(residual_mass=residual_mass),
        ).inhabited
    except TypeError:
        return "refused_float"


def _real_float_derive_outcome(residual_mass: Any) -> Any:
    try:
        return derive_guards(_green_evidence(residual_mass=residual_mass)).is_auth()
    except TypeError:
        return "refused_float"


def test_mutant_incomplete_or_missing_packet_killed() -> None:
    # Invariant: missing or incomplete packet refuses standing even when guards are green.
    evidence = _green_evidence()
    for packet in (None, _incomplete_packet()):
        real = evaluate_authorization("prop_packet", packet, evidence)
        mutant = mutant_inhabit_incomplete_or_missing_packet(
            "prop_packet", packet, evidence
        )
        assert real.inhabited is False
        assert mutant is True
        assert mutant != real.inhabited

    real_ok = evaluate_authorization("prop_ok", _valid_packet(), evidence)
    mutant_ok = mutant_inhabit_incomplete_or_missing_packet(
        "prop_ok", _valid_packet(), evidence
    )
    assert real_ok.inhabited is True
    assert mutant_ok is True

    blocked = _green_evidence(pipeline_accepted=False)
    real_blocked = evaluate_authorization("prop_blocked", None, blocked)
    mutant_blocked = mutant_inhabit_incomplete_or_missing_packet(
        "prop_blocked", None, blocked
    )
    assert real_blocked.inhabited is False
    assert mutant_blocked is False


def test_mutant_high_confidence_without_packet_killed() -> None:
    # Invariant: logit_confidence 0.99 does not inhabit standing without a packet.
    evidence = _green_evidence()
    real = evaluate_authorization(
        "prop_fluent",
        None,
        evidence,
        logit_confidence=0.99,
    )
    mutant = mutant_high_confidence_without_packet(
        "prop_fluent",
        None,
        evidence,
        logit_confidence=0.99,
    )
    assert real.inhabited is False
    assert mutant is True
    assert mutant != real.inhabited

    real_ok = evaluate_authorization(
        "prop_ok",
        _valid_packet(),
        evidence,
        logit_confidence=0.99,
    )
    mutant_ok = mutant_high_confidence_without_packet(
        "prop_ok",
        _valid_packet(),
        evidence,
        logit_confidence=0.99,
    )
    assert real_ok.inhabited is True
    assert mutant_ok is True

    real_low = evaluate_authorization(
        "prop_low",
        None,
        evidence,
        logit_confidence=0.1,
    )
    mutant_low = mutant_high_confidence_without_packet(
        "prop_low",
        None,
        evidence,
        logit_confidence=0.1,
    )
    assert real_low.inhabited is False
    assert mutant_low is False


def test_mutant_skip_failed_halt_guard_killed() -> None:
    # Invariant: nonzero residual_mass fails zero_residual_mass; forcing it green is a fault.
    evidence = _green_evidence(residual_mass=Rational(1, 1))
    real_guards = derive_guards(evidence)
    mutant_guards = mutant_force_zero_residual_mass(evidence)
    real_auth = evaluate_authorization("prop_mass", _valid_packet(), evidence)
    mutant_auth = mutant_evaluate_skip_failed_halt_guard(
        "prop_mass", _valid_packet(), evidence
    )
    assert real_guards.zero_residual_mass is False
    assert mutant_guards.zero_residual_mass is True
    assert mutant_guards != real_guards
    assert real_guards.is_auth() is False
    assert mutant_guards.is_auth() is True
    assert mutant_guards.is_auth() != real_guards.is_auth()
    assert real_auth.inhabited is False
    assert mutant_auth is True
    assert mutant_auth != real_auth.inhabited

    green = _green_evidence()
    real_green = evaluate_authorization("prop_green", _valid_packet(), green)
    mutant_green = mutant_evaluate_skip_failed_halt_guard(
        "prop_green", _valid_packet(), green
    )
    assert real_green.inhabited is True
    assert mutant_green is True

    other_fail = _green_evidence(pipeline_accepted=False)
    real_other = evaluate_authorization("prop_other", _valid_packet(), other_fail)
    mutant_other = mutant_evaluate_skip_failed_halt_guard(
        "prop_other", _valid_packet(), other_fail
    )
    assert real_other.inhabited is False
    assert mutant_other is False


def test_mutant_accept_float_residual_killed() -> None:
    # Invariant: float residual_mass is refused; a mutant that accepts it disagrees.
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _green_evidence(residual_mass=0.0)

    real_eval = _real_float_residual_outcome(0.0)
    mutant_eval = mutant_evaluate_accept_float("prop_float", _valid_packet(), 0.0)
    real_derive = _real_float_derive_outcome(0.0)
    mutant_derive = mutant_derive_guards_accept_float(residual_mass=0.0).is_auth()
    assert real_eval == "refused_float"
    assert mutant_eval is True
    assert mutant_eval != real_eval
    assert real_derive == "refused_float"
    assert mutant_derive is True
    assert mutant_derive != real_derive

    real_nonzero = _real_float_residual_outcome(0.99)
    mutant_nonzero = mutant_evaluate_accept_float("prop_float", _valid_packet(), 0.99)
    assert real_nonzero == "refused_float"
    assert mutant_nonzero is False
    assert mutant_nonzero != real_nonzero

    real_int_zero = evaluate_authorization(
        "prop_int_zero", _valid_packet(), _green_evidence(residual_mass=0)
    )
    mutant_int_zero = mutant_evaluate_accept_float(
        "prop_int_zero", _valid_packet(), 0
    )
    assert real_int_zero.inhabited is True
    assert mutant_int_zero is True
