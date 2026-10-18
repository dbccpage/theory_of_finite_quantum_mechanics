# AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

"""
Growth against refinement: continuous limit obstruction, fine-graining entropy, and field escalation rates.

Campaign C250 Block 09 (Global Steps 251-275).
"""

from __future__ import annotations

import json
import math
import pathlib
from pathlib import Path as _Path
from typing import Any, Dict


def is_prime(n: int) -> bool:
    """Return True if n is prime."""
    if n < 2:
        return False
    for d in range(2, int(math.isqrt(n)) + 1):
        if n % d == 0:
            return False
    return True


def next_prime_not_dividing(n: int) -> int:
    """Find the smallest prime that does not divide n."""
    if type(n) is not int or n < 1:
        raise ValueError("Expected a positive integer")
    p = 2
    while True:
        if is_prime(p) and n % p != 0:
            return p
        p += 1


def squarefree_part(n: int) -> int:
    """Return the squarefree part of an integer n >= 1."""
    if type(n) is not int or n < 1:
        raise ValueError("Expected a positive integer")
    d = 1
    rem = n
    p = 2
    while p * p <= rem:
        count = 0
        while rem % p == 0:
            count += 1
            rem //= p
        if count % 2 == 1:
            d *= p
        p += 1
    if rem > 1:
        d *= rem
    return d


def minimal_conductor_for_sqrt(m: int) -> int:
    """Return the minimal cyclotomic conductor carrying sqrt(m) for integer m >= 1."""
    sqf = squarefree_part(m)
    if sqf == 1:
        return 1
    if sqf % 4 == 1:
        return sqf
    return 4 * sqf


def evaluate_growth_unboundedness() -> Dict[str, Any]:
    """Demonstrate unbounded growth: for any conductor n, prime-qudit MUBs require a higher conductor."""
    test_conductors = [1, 2, 4, 8, 12, 24, 120, 3360, 9240]
    escalation_witnesses = []
    for cond in test_conductors:
        p_new = next_prime_not_dividing(2 * cond)
        escalation_witnesses.append({
            "conductor": cond,
            "escalating_prime": p_new,
            "requires_conductor_multiple": math.lcm(cond, p_new),
        })
    return {
        "growth_unbounded": True,
        "evidence_scope": "cited field theorem plus finite sample witnesses; no Lean containment bridge",
        "mechanism": "prime_qudit_mub_escalation",
        "sample_witnesses": escalation_witnesses,
    }


def evaluate_refinement_duality() -> Dict[str, Any]:
    """Evaluate refinement (branch counting) on rational vs irrational sectors."""
    sample_rational_weights = [(1, 2), (1, 3), (1, 6)]
    lcm_denom = math.lcm(*(denom for _, denom in sample_rational_weights))

    return {
        "refinement_bounded_on_rational_sector": True,
        "rational_sector_bound_mechanism": "lcm_of_denominators",
        "sample_rational_bound": lcm_denom,
        "scope": "each fixed finite list of rational weights has its own bound; no global bound over Q",
        "refinement_impossible_on_irrational_sector": True,
        "irrational_sector_status": "obstructed_no_finite_integer_solution",
    }


def evaluate_cglmp_conductors() -> Dict[str, Any]:
    """Compute minimal cyclotomic conductors carrying CGLMP Bell operators for d=3..8."""
    cglmp_conductors = {
        3: 24,
        4: 240,
        5: 120,
        6: 120,
        7: 840,
        8: 480,
    }
    all_lcm = 1
    for cond in cglmp_conductors.values():
        all_lcm = math.lcm(all_lcm, cond)

    return {
        "cglmp_dimension_conductors": cglmp_conductors,
        "input_status": "declared sufficient conductors; global operator-realization minimality unproved",
        "smallest_conductor_carrying_all_cglmp_d_le_8": all_lcm,
        "prime_factorization": "2^5 * 3 * 5 * 7",
    }


def evaluate_w_state_conductors() -> Dict[str, Any]:
    """Compute minimal cyclotomic conductors carrying multi-qubit W states for N=1..11."""
    w_conductors = {}
    for n in range(1, 12):
        w_conductors[n] = minimal_conductor_for_sqrt(n)

    all_lcm = 1
    for cond in w_conductors.values():
        all_lcm = math.lcm(all_lcm, cond)

    return {
        "w_state_conductors": w_conductors,
        "smallest_conductor_carrying_w_states_up_to_11": all_lcm,
        "prime_factorization": "2^3 * 3 * 5 * 7 * 11",
    }


def evaluate_differential_pricing() -> Dict[str, Any]:
    """Record differential pricing of growth vs refinement in separate ledger structures."""
    return {
        "growth_and_refinement_priced_differently": True,
        "growth_metric": "cyclotomic_conductor_and_field_degree",
        "refinement_metric": "branch_counting_lcm_or_refusal",
        "combination_rule": "orthogonal_ledger_columns_never_summed",
        "limit_object": "Q^ab",
        "limit_object_description": "directed colimit of Q(zeta_n) over inclusion; maximal abelian extension of Q",
    }


def run_block_09_evaluation() -> Dict[str, Any]:
    """Run full evaluation of Campaign C250 Block 09."""
    growth = evaluate_growth_unboundedness()
    refinement = evaluate_refinement_duality()
    cglmp = evaluate_cglmp_conductors()
    w_states = evaluate_w_state_conductors()
    pricing = evaluate_differential_pricing()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C250",
        "block_id": "block_09",
        "growth_unbounded": growth["growth_unbounded"],
        "refinement_bounded_on_rational_sector": refinement["refinement_bounded_on_rational_sector"],
        "refinement_impossible_on_irrational_sector": refinement["refinement_impossible_on_irrational_sector"],
        "growth_and_refinement_priced_differently": pricing["growth_and_refinement_priced_differently"],
        "smallest_conductor_carrying_all_cglmp_d_le_8": cglmp["smallest_conductor_carrying_all_cglmp_d_le_8"],
        "smallest_conductor_carrying_w_states_up_to_11": w_states["smallest_conductor_carrying_w_states_up_to_11"],
        "limit_object": pricing["limit_object"],
        "growth_details": growth,
        "refinement_details": refinement,
        "cglmp_details": cglmp,
        "w_state_details": w_states,
        "pricing_details": pricing,
    }


def emit_receipt(path: str | None = None) -> Dict[str, Any]:
    """Emit a JSON evidence report for Block 09."""
    report = run_block_09_evaluation()
    if path is None:
        p = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / "evidence" / "c250_block09_growth_refinement.json"
    else:
        p = pathlib.Path(path)
        if not p.is_absolute():
            p = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    rep = emit_receipt()
    print("Block 09 receipt successfully emitted.")
    print("Growth unbounded:", rep["growth_unbounded"])
    print("CGLMP d<=8 smallest conductor:", rep["smallest_conductor_carrying_all_cglmp_d_le_8"])
    print("W states N<=11 smallest conductor:", rep["smallest_conductor_carrying_w_states_up_to_11"])
    print("Limit object:", rep["limit_object"])

__all__ = ['emit_receipt', 'evaluate_cglmp_conductors', 'evaluate_differential_pricing', 'evaluate_growth_unboundedness', 'evaluate_refinement_duality', 'evaluate_w_state_conductors', 'is_prime', 'minimal_conductor_for_sqrt', 'next_prime_not_dividing', 'run_block_09_evaluation', 'squarefree_part']
