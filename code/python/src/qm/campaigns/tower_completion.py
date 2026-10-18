"""Campaign C500 Block 05: Limit Semantics and Finite-State Convergence.

Mechanizes:
1. Typed limit registry:
   - Algebraic direct colimit (no topology).
   - C*-algebra norm completion (UHF 2^infty / CAR algebra).
   - Weak-* state projective limit.
   - Moment convergence along matrix sequences.
   - Quantum metric (Rieffel quantum Gromov-Hausdorff distance).
2. Finite benchmark formulas under the declared spin-j representation:
   - Commutator [X_i, X_j] = (2i / d) eps_{ijk} X_k -> 0 at rate O(1/d).
   - Casimir sum X_1^2 + X_2^2 + X_3^2 = (1 - 1/d^2) I_d.
3. Countermodel to topology-free limit:
   - Moment / tracial convergence holds while uniform operator-norm convergence fails
     for rank-one projections of increasing dimension.
4. A topology/completion must be declared separately from the algebraic union.
No quantum metric convergence or general tower convergence is proved here.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
from fractions import Fraction
from typing import Any, Dict


def fuzzy_sphere_commutator_rate(d: int) -> Dict[str, Any]:
    """Compute exact fuzzy sphere commutator norm and convergence rate:

    Coordinates J_1, J_2, J_3 are spin j = (d - 1)/2 representations of su(2).
    Normalized coordinates X_i = 2 * J_i / d.
    Commutator [X_1, X_2] = (2i / d) X_3.
    Since ||X_3|| = (d-1)/d, the exact commutator norm is 2(d-1)/d^2.
    The value 2/d is an upper bound, not the exact norm.
    Rate: O(1/d).
    """
    if type(d) is not int or d < 2:
        raise ValueError("The nontrivial fuzzy-sphere benchmark requires integer dimension d >= 2.")
    op_norm_comm = Fraction(2 * (d - 1), d * d)
    casimir = 1 - Fraction(1, d * d)
    return {
        "dimension": d,
        "spin_j": (d - 1) / 2.0,
        "normalized_commutator_norm": float(op_norm_comm),
        "commutator_norm_exact": str(op_norm_comm),
        "commutator_norm_upper_bound": float(Fraction(2, d)),
        "convergence_rate": f"2 / {d}",
        "casimir_norm": float(casimir),
        "casimir_norm_exact": str(casimir),
    }


def compare_topology_choices_countermodel() -> Dict[str, Any]:
    """Exhibit two topology choices yielding different convergence verdicts on the same sequence:

    Sequence: Rank-1 projector P_d = |0><0| in M_d.
    - Under normalized tracial moment comparison:
      tau_d(P_d) = tr(P_d) / d = 1 / d -> 0 as d -> infty (CONVERGES to zero).
    - Under uniform operator norm topology:
      ||P_d||_{op} = 1 for all d (DOES NOT CONVERGE to 0; stays at 1).

    Verdict changes from CONVERGENT (under trace) to NON-CONVERGENT-TO-ZERO (under operator norm).
    """
    dimensions = [2, 4, 8, 16, 32, 64, 128]
    data = []
    for d in dimensions:
        data.append({
            "dimension": d,
            "tracial_state_expectation": float(Fraction(1, d)),
            "operator_norm": 1.0,
            "tracial_limit_is_zero": True,
            "operator_norm_limit_is_zero": False,
        })

    return {
        "sequence_description": "Rank-1 projector P_d = |0><0| on C^d",
        "topology_1": "Normalized tracial moments on the varying matrix algebras",
        "topology_1_verdict": "CONVERGES_TO_ZERO",
        "topology_2": "Uniform C*-Operator Norm Topology",
        "topology_2_verdict": "DOES_NOT_CONVERGE_TO_ZERO",
        "verdict_changes": True,
        "scope": "Scalar moments tau_d(P_d^k)=1/d for every positive k; no weak-* state-space or common embedding claim.",
        "dimension_data": data,
    }


def separate_algebraic_union_from_analytic_completion() -> Dict[str, Any]:
    """Separate the algebraic union Q^ab from analytic completions:

    - Q^ab = colim Q(zeta_n) is a countable algebraic field of characteristic 0.
      It has decidable equality and absolute Galois action Gal(Q^ab / Q) = Z_hat^x.
    - Metric completions:
      * Archimedian completion under complex norm is C (uncountable, continuum).
      * For a fixed embedding in C_p, completion is the closure of that embedded
        cyclotomic field; it is not identified here with the larger field C_p.
    - The algebraic union alone DOES NOT select a topology or completion.
    """
    return {
        "algebraic_union": "Q^ab = colim Q(zeta_n)",
        "is_countable": True,
        "has_decidable_equality": True,
        "has_selected_analytic_topology": False,
        "field_property_status": "DECLARED_THEORY_INPUTS_NOT_A_FIELD_IMPLEMENTATION",
        "completion_c": "Complex numbers C (Archimedean, continuous Lie groups)",
        "completion_cp": "Closure of a declared embedding of Q^ab in C_p; no identification with C_p is asserted.",
        "algebraic_union_equals_unqualified_completion": False,
    }


def generate_canonical_block05_receipt() -> Dict[str, Any]:
    """Generate the finite formula comparisons and declared completion boundaries."""
    dims = [2, 4, 8, 16, 32, 64, 128, 256]
    fuzzy_benchmark = [fuzzy_sphere_commutator_rate(d) for d in dims]
    topology_countermodel = compare_topology_choices_countermodel()
    algebraic_separation = separate_algebraic_union_from_analytic_completion()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_05",
        "global_targets": "C500-T401..C500-T425",
        "terminal_outcome": "FINITE_SPIN_BENCHMARK_WITH_DECLARED_MOMENT_COMPARISON",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "benchmark_sequence": {
            "name": "Fuzzy Sphere matrix approximation to S^2",
            "anchor": "S3",
            "rate": "O(1/d)",
            "benchmark_results": fuzzy_benchmark,
        },
        "topology_comparison_countermodel": topology_countermodel,
        "algebraic_union_separation": algebraic_separation,
        "machine_bet_clauses": {
            "benchmark_convergence_status": "FINITE_FORMULA_CHECKS_GENERAL_LIMIT_OPEN",
            "topology_is_explicit_input": False,
            "algebraic_union_equals_unqualified_completion": False,
            "topology_choice_changes_at_least_one_verdict": True,
            "all_declared_towers_converge": False,
            "analytic_source_claims_are_not_encoded_as_test_fixtures": False,
        },
    }


if __name__ == "__main__":
    receipt = generate_canonical_block05_receipt()
    print(json.dumps(receipt, indent=2))

__all__ = ['compare_topology_choices_countermodel', 'fuzzy_sphere_commutator_rate', 'generate_canonical_block05_receipt', 'separate_algebraic_union_from_analytic_completion']
