
"""
Cyclotomic cancellation certificates and discrete phase sum classification.

Campaign C250 Block 08 (Global Steps 226-250).
"""

from __future__ import annotations

import json
import math
import pathlib
from pathlib import Path as _Path
from typing import Any, Dict

from .cyclotomic_tower import CyclotomicElement


def is_two_power(n: int) -> bool:
    """Return True if n is a power of 2 (n = 2^k for k >= 0)."""
    return n > 0 and (n & (n - 1)) == 0


def smallest_odd_prime_factor(n: int) -> int | None:
    """Return the smallest odd prime factor of n, or None if n is a power of 2."""
    if type(n) is not int or n < 1:
        raise ValueError("Expected a positive integer")
    while n % 2 == 0:
        n //= 2
    if n <= 1:
        return None
    for d in range(3, int(math.isqrt(n)) + 1, 2):
        if n % d == 0:
            return d
    return n


def classify_conductor_cancellations(conductor: int) -> Dict[str, Any]:
    """Classify vanishing sum behavior for cyclotomic field Q(zeta_n) by Lam-Leung theorem."""
    p_odd = smallest_odd_prime_factor(conductor)
    if p_odd is None:
        return {
            "conductor": conductor,
            "all_minimal_sums_pairable": True,
            "classification_basis": "Lam-Leung; nonnegative integer multiplicities of nth roots",
            "unpairable_minimal_length": None,
            "cancellation_family": "pairable",
            "mechanism": "identity" if conductor <= 1 else "pairwise_reflection_involution",
        }
    return {
        "conductor": conductor,
        "all_minimal_sums_pairable": False,
        "classification_basis": "Lam-Leung; nonnegative integer multiplicities of nth roots",
        "unpairable_minimal_length": p_odd,
        "cancellation_family": "prime",
        "mechanism": f"irreducible_cyclic_vortex_order_{p_odd}",
    }


TARGET_CONDUCTOR_MAP: Dict[int, int] = {
    1: 1,
    2: 12,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 2,
    8: 1,
    9: 1,
    10: 4,
    11: 4,
    12: 1,
    13: 5,
    14: 1,
    15: 8,
    16: 2,
    17: 8,
    18: 2,
    19: 1,
    20: 1,
    21: 4,
    22: 3,
}


def audit_two_power_cancellations() -> Dict[str, Any]:
    """Report the cited two-power classification for the declared sample conductors."""
    two_power_conductors = [2, 4, 8, 16, 32, 64, 128]
    all_pairable = all(
        classify_conductor_cancellations(c)["all_minimal_sums_pairable"]
        for c in two_power_conductors
    )
    return {
        "conductors_evaluated": two_power_conductors,
        "all_two_power_sums_pairable": all_pairable,
        "minimal_vanishing_length": 2,
    }


def audit_target_cancellations() -> Dict[str, Any]:
    """Audit cyclotomic phase cancellation types across all 22 foundational targets."""
    target_census = []
    unpairable_ids = []

    for tid in range(1, 23):
        cond = TARGET_CONDUCTOR_MAP[tid]
        info = classify_conductor_cancellations(cond)
        is_unpairable = not info["all_minimal_sums_pairable"]
        if is_unpairable:
            unpairable_ids.append(tid)

        target_census.append({
            "target_id": tid,
            "conductor": cond,
            "is_unpairable": is_unpairable,
            "unpairable_minimal_length": info["unpairable_minimal_length"],
            "cancellation_family": info["cancellation_family"],
        })

    unpairable_count = len(unpairable_ids)
    first_unpairable_len = min(
        t["unpairable_minimal_length"] for t in target_census if t["is_unpairable"]
    )

    return {
        "targets_censused_count": 22,
        "targets_with_unpairable_cancellation_count": unpairable_count,
        "targets_with_unpairable_cancellation_ids": unpairable_ids,
        "first_unpairable_length": first_unpairable_len,
        "target_census": target_census,
    }


def sorkin_i3(amplitudes: tuple[CyclotomicElement, CyclotomicElement, CyclotomicElement]) -> CyclotomicElement:
    """Exact third-order inclusion-exclusion under the declared quadratic rule."""
    if len(amplitudes) != 3:
        raise ValueError("I3 requires exactly three amplitudes")
    a, b, c = amplitudes
    return ((a+b+c).born_weight() - (a+b).born_weight()
            - (a+c).born_weight() - (b+c).born_weight()
            + a.born_weight() + b.born_weight() + c.born_weight())


def evaluate_sorkin_i3_cancellation() -> Dict[str, Any]:
    """Evaluate I3 separately from a particular vanishing three-root sum."""
    z3 = CyclotomicElement.zeta(3)
    one = CyclotomicElement.rational(1, 3)
    special = (one, z3, z3*z3)
    ordinary = (one, one, one)
    checks = [sorkin_i3(v).is_zero() for v in (special, ordinary)]
    return {
        "target_id": 3, "interference_term": "I_3",
        "vanishing_identity": "quadratic inclusion-exclusion for three amplitudes",
        "sum_length": 7, "cancellation_type": "quadratic_inclusion_exclusion",
        "is_pairable": None, "conductor": 1,
        "parity_obstruction": "not applicable to intensity inclusion-exclusion",
        "i3_evaluated_deviation": 0.0 if all(checks) else None,
        "i3_identically_zero": all(checks),
        "evidence_scope": "two exact examples; arbitrary rational complex amplitudes proved in H065",
        "prime_sum_example": {
            "identity": "1 + zeta_3 + zeta_3^2 = 0",
            "verified": (one+z3+z3*z3).is_zero(), "length": 3, "conductor": 3,
        },
        "nonzero_total_amplitude_example": not (one+one+one).is_zero(),
    }


def record_estate_certificate_correspondence() -> Dict[str, Any]:
    """Record structural correspondence between cyclotomic cancellations and SignRepair certificate."""
    return {
        "estate_theorem": "SignRepair.certificate_iff_dominated",
        "pairing_correspondence": (
            "A pairing certificate corresponds to per-magnitude domination with magnitudes in {1}, "
            "where phase interference is resolved by pairwise involution."
        ),
        "two_power_domination": (
            "For conductor n = 2^k, roots of unity decompose into orthogonal antipodal pairs {zeta, -zeta}, "
            "so every vanishing sum is dominated by a pairing certificate."
        ),
        "prime_power_obstruction": (
            "For conductor divisible by an odd prime p, the minimal vanishing sum is the regular p-gon "
            "sum_{j=0}^{p-1} zeta_p^j = 0, which has odd length p and admits no pairing certificate."
        ),
        "estate_certificate_link_recorded": True,
        "correspondence_proved": False,
        "evidence_scope": "analogy recorded; no typed transport to the estate certificate is supplied",
    }


def run_block_08_cancellation_audit() -> Dict[str, Any]:
    """Execute complete Block 08 audit and return structured report."""
    two_pow = audit_two_power_cancellations()
    census = audit_target_cancellations()
    sorkin = evaluate_sorkin_i3_cancellation()
    estate = record_estate_certificate_correspondence()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "block_id": "block_08",
        "global_step": 250,
        "two_power_conductor_cancellations_all_pairable": two_pow["all_two_power_sums_pairable"],
        "targets_with_unpairable_cancellation_count": census["targets_with_unpairable_cancellation_count"],
        "targets_with_unpairable_cancellation_ids": census["targets_with_unpairable_cancellation_ids"],
        "first_unpairable_length": census["first_unpairable_length"],
        "sorkin_i3_cancellation_type_target3": sorkin["cancellation_type"],
        "estate_certificate_link_recorded": estate["estate_certificate_link_recorded"],
        "census_details": census,
        "sorkin_evaluation": sorkin,
        "estate_link": estate,
    }


def emit_receipt(path: str | None = None) -> Dict[str, Any]:
    """Emit a JSON evidence report for Block 08."""
    report = run_block_08_cancellation_audit()
    if path is None:
        p = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / "evidence" / "c250_block08_cancellations.json"
    else:
        p = pathlib.Path(path)
        if not p.is_absolute():
            p = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    rep = emit_receipt()
    print("Block 08 cancellation receipt successfully emitted.")
    print("Targets with unpairable cancellation count:", rep["targets_with_unpairable_cancellation_count"])
    print("Unpairable target IDs:", rep["targets_with_unpairable_cancellation_ids"])
    print("First unpairable length:", rep["first_unpairable_length"])
    print("Sorkin I3 cancellation type:", rep["sorkin_i3_cancellation_type_target3"])

__all__ = ['TARGET_CONDUCTOR_MAP', 'audit_target_cancellations', 'audit_two_power_cancellations', 'classify_conductor_cancellations', 'emit_receipt', 'evaluate_sorkin_i3_cancellation', 'is_two_power', 'record_estate_certificate_correspondence', 'run_block_08_cancellation_audit', 'smallest_odd_prime_factor', 'sorkin_i3']
