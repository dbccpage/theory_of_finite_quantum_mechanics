"""Terminal decision routing and problem-bound verification for CODA-FOC.

Bounded Context: CODA.FOC (Finite Obstruction Calculus)
AuthorityEffect: None.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

from typing import Any

from sympy import simplify

from .diagnosis import diagnose
from .exact_arithmetic import (
    _digest_exact,
    _exact_vector,
    exact_equal,
)
from .packets import (
    Diagnostic,
    FiniteObstructionPacket,
    ObstructionResult,
    TerminalRoute,
)
from .repair import (
    FiniteRepairRegistry,
    StabilizationEvidence,
)


def terminal_route(
    result: ObstructionResult,
    evidence: StabilizationEvidence | None,
    *,
    registry: FiniteRepairRegistry | None = None,
    packet: FiniteObstructionPacket | None = None,
    defect: Any | None = None,
) -> TerminalRoute:
    """Classify terminal decision on an obstruction result.

    Exact branch requires problem-bound verification:
    - Problem binding is strictly required: either `registry` or (`packet` and `defect`)
      must be provided; without problem data, routing fails closed to OPEN_OBSTRUCTION.
    - Diagnostic must be EXACT_REPAIR
    - phi1.value == 0, phi1.duality_gap == 0, and phi1.residual == 0
    - gamma2.value == 0, gamma2.duality_gap == 0, and gamma2.residual == 0
    - zero authority effect
    - phi1 certificate must verify against declared problem data, establishing the repair equation
      (x + d0 * repair == 0 with residual == 0)
    - gamma2 certificate must verify against declared problem data
    - Fresh recomputed diagnosis must match result and confirm EXACT_REPAIR.

    Survivor branch requires replaying declared finite stabilization evidence.
    Problem-bound consistency checks execute before either terminal branch.
    Any forged diagnostic, inconsistent residual, conflicting problem data, or uncertified claim routes to OPEN_OBSTRUCTION.
    """
    bound_packet: FiniteObstructionPacket | None = None
    bound_defect: Any | None = None

    if registry is not None:
        if not isinstance(registry, FiniteRepairRegistry):
            return TerminalRoute.OPEN_OBSTRUCTION
        bound_packet = registry.packet
        bound_defect = registry.defect
        if packet is not None and packet != bound_packet:
            return TerminalRoute.OPEN_OBSTRUCTION
        if defect is not None:
            try:
                defect_vec = _exact_vector(defect)
                bound_vec = _exact_vector(bound_defect)
                if not exact_equal(defect_vec, bound_vec):
                    return TerminalRoute.OPEN_OBSTRUCTION
                bound_defect = bound_vec
            except Exception:
                return TerminalRoute.OPEN_OBSTRUCTION
    elif packet is not None and defect is not None:
        if not isinstance(packet, FiniteObstructionPacket):
            return TerminalRoute.OPEN_OBSTRUCTION
        bound_packet = packet
        bound_defect = defect
    else:
        # Without packet and defect, or a registry, problem-bound verification is impossible.
        return TerminalRoute.OPEN_OBSTRUCTION

    if result.diagnostic is Diagnostic.EXACT_REPAIR:
        # Validate classification consistency: exact repair implies zero obstruction
        if (
            result.authority_effect != "None"
            or result.phi1.authority_effect != "None"
            or result.gamma2.authority_effect != "None"
            or result.phi1.value != 0
            or result.phi1.duality_gap != 0
            or any(simplify(v) != 0 for v in result.phi1.residual)
            or result.gamma2.value != 0
            or result.gamma2.duality_gap != 0
            or any(simplify(v) != 0 for v in result.gamma2.residual)
        ):
            return TerminalRoute.OPEN_OBSTRUCTION

        try:
            x = _exact_vector(bound_defect)
            if x.rows != bound_packet.d0.rows:
                return TerminalRoute.OPEN_OBSTRUCTION

            # Verify digests match problem data
            expected_input_digest = _digest_exact(
                "obstruction-packet",
                bound_packet.d0,
                bound_packet.d1,
                bound_packet.a2,
                bound_packet.w1,
                bound_packet.w2,
                x,
            )
            expected_observer_digest = _digest_exact(
                "observer", bound_packet.w1, bound_packet.w2
            )
            if (
                result.input_digest != expected_input_digest
                or result.observer_digest != expected_observer_digest
            ):
                return TerminalRoute.OPEN_OBSTRUCTION

            # Verify phi1 certificate against problem data (verifies repair equation d0*x_rep = v)
            if not result.phi1.verify(bound_packet.d0, x, bound_packet.w1):
                return TerminalRoute.OPEN_OBSTRUCTION

            # Verify gamma2 certificate against problem data
            d1_x = bound_packet.d1 * x
            if not result.gamma2.verify(bound_packet.a2, d1_x, bound_packet.w2):
                return TerminalRoute.OPEN_OBSTRUCTION

            # Recompute diagnosis independently and check exact match using realized vector x
            recomputed = diagnose(bound_packet, x)
            if recomputed != result or recomputed.diagnostic is not Diagnostic.EXACT_REPAIR:
                return TerminalRoute.OPEN_OBSTRUCTION
        except Exception:
            return TerminalRoute.OPEN_OBSTRUCTION

        return TerminalRoute.EXACT_REPAIR

    if (
        result.diagnostic is Diagnostic.COHERENT_RESIDUAL
        and evidence is not None
        and evidence.valid_for(result, registry)
    ):
        return TerminalRoute.STABILIZED_SURVIVOR

    return TerminalRoute.OPEN_OBSTRUCTION


__all__ = [
    "terminal_route",
]
