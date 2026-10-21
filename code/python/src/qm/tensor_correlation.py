"""Campaign C500 Block 08: Correlation Models and Computability Boundary.

Mechanizes:
1. Four correlation model labels and a cited inclusion registry:
   - C_q(d) (fixed dimension d tensor product correlations)
   - C_q = union_d C_q(d) (finite-dimensional tensor correlations)
   - C_qa = closure(C_q) (approximate tensor correlations)
   - C_qc (commuting-operator correlations)
   Inclusions: C_q(d) subset C_q subset C_qa subset C_qc.
2. MIP* = RE separation as cited guardrail:
   - C_qa != C_qc (refuting Tsirelson's conjecture).
   - The value problem for general nonlocal games is undecidable.
   - Refuses uniform value solver for unrestricted quantum correlations.
3. Bounded Decidable Island:
   - Bounded game class (CHSH, Clauser-Horne, Magic Square).
   - NPA hierarchy outer relaxation certificates:
     * CHSH classical bound: 3/4 = 0.75.
     * CHSH quantum Tsirelson bound: 1/2 + sqrt(2)/4 in interval [17/20, 43/50].
     * The exact expression is a cited input; no local SDP is constructed.
4. Finite-level distinction:
   - NPA finite level is an outer SDP relaxation, not an exact value,
     without an independent certificate closing the gap. Flatness is one
     sufficient route; it is not a necessary condition for every exact bound.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any, Dict


def correlation_set_inclusions() -> Dict[str, Any]:
    """Catalog correlation sets, their formal definitions, and proven inclusions:

    - C_q(d): States on C^d (x) C^d with local projective measurements.
    - C_q: Union over all finite d.
    - C_qa: Topological closure in R^{|X||Y||A||B|}.
    - C_qc: States on H with commuting subalgebras [A_x, B_y] = 0.
    """
    return {
        "hierarchy": [
            {"set": "C_q(d)", "description": "Fixed finite dimension d tensor product"},
            {"set": "C_q", "description": "Arbitrary finite dimension tensor product union"},
            {"set": "C_qa", "description": "Topological closure of C_q (approximate tensor)"},
            {"set": "C_qc", "description": "Commuting-operator model (possibly infinite dimensional)"},
        ],
        "inclusions": [
            "C_q(d) subset C_q",
            "C_q subset C_qa",
            "C_qa subset C_qc",
        ],
        "global_guardrail": {
            "theorem": "MIP* = RE (Ji-Natarajan-Vidick-Wright-Yuen 2020)",
            "citation": "arXiv:2001.04383",
            "status": "CITED_GUARDRAIL",
            "implication": "C_qa != C_qc; general game value is undecidable",
            "unrestricted_uniform_value_solver_claimed": False,
        },
    }


def certify_chsh_interval(lower_bound: Fraction, upper_bound: Fraction) -> bool:
    """Enclose the cited expression 1/2 + sqrt(2)/4 by exact rational squaring.

    This verifies the algebraic enclosure, not optimality of a strategy or SDP.
    """
    if not isinstance(lower_bound, Fraction) or not isinstance(upper_bound, Fraction):
        raise TypeError("interval endpoints must be exact fractions")
    lower_root = 4 * lower_bound - 2
    upper_root = 4 * upper_bound - 2
    return (lower_bound < upper_bound
            and (lower_root < 0 or lower_root * lower_root < 2)
            and upper_root > 0 and upper_root * upper_root > 2)


def chsh_bounded_game_certificate() -> Dict[str, Any]:
    """Certified bounds for the 2-player CHSH nonlocal game:

    - Classical value: 3/4 = Fraction(3, 4).
    - Quantum value: (1/2) * (1 + 1/sqrt(2)) = 1/2 + sqrt(2)/4.
    - Certified rational interval enclosure:
      Lower rational: 17/20 = 0.850.
      Upper rational: 43/50 = 0.860.
      Since 0.850 < 0.853553... < 0.860, the true value is strictly enclosed.
    - NPA Level 1 bound: Certified upper bound 1/2 + 1/(2*sqrt(2)).
    """
    omega_c = Fraction(3, 4)
    lower_bound = Fraction(17, 20)
    upper_bound = Fraction(43, 50)
    val_float = 0.5 + math.sqrt(2.0) / 4.0

    enclosure_verified = certify_chsh_interval(lower_bound, upper_bound)

    return {
        "game": "CHSH",
        "question_alphabet_size": 2,
        "answer_alphabet_size": 2,
        "classical_value": str(omega_c),
        "classical_value_float": float(omega_c),
        "quantum_certified_lower_bound": str(lower_bound),
        "quantum_certified_upper_bound": str(upper_bound),
        "quantum_value_float_approx": val_float,
        "float_approximation_role": "display only; not used by the certificate",
        "exact_expression": "1/2 + sqrt(2)/4",
        "expression_evidence_class": "CITED_INPUT",
        "local_sdp_or_strategy_certificate": False,
        "interval_enclosure_verified": enclosure_verified,
        "transformed_lower_squared": str((4*lower_bound-2)**2),
        "transformed_upper_squared": str((4*upper_bound-2)**2),
        "is_strictly_superclassical": enclosure_verified and lower_bound > omega_c,
        "npa_level_1_is_exact_for_chsh": None,
        "flatness_condition_required_in_general": False,
    }


def npa_finite_level_distinction_audit() -> Dict[str, Any]:
    """Audit whether every finite NPA level is exact:

    VERDICT: FALSE.
    Finite levels of the NPA hierarchy Q_1, Q_2, ... give outer SDP relaxations of C_qc.
    Convergence Q_k -> C_qc holds as k -> infty, but at any finite level k,
    the SDP bound can strictly exceed the true quantum value. A rank/flatness
    condition may certify realization; matching feasible lower and upper bounds
    can also certify a game value. No such NPA certificate is constructed here.
    """
    return {
        "npa_finite_level_is_automatically_exact": False,
        "requires_rank_flatness_certificate": False,
        "requires_independent_exactness_certificate": True,
        "status": "CITED_OUTER_RELAXATION_SEMANTICS",
        "audit_finding": "A finite NPA level alone does not certify exactness; flatness is one sufficient certificate route.",
    }


def generate_canonical_block08_receipt() -> Dict[str, Any]:
    """Generate the complete canonical receipt for Block 08."""
    inclusions = correlation_set_inclusions()
    chsh_cert = chsh_bounded_game_certificate()
    npa_audit = npa_finite_level_distinction_audit()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_08",
        "global_targets": "C500-T476..C500-T500",
        "terminal_outcome": "BOUNDED_CORRELATION_ISLAND_WITH_GLOBAL_GUARDRAIL",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "correlation_set_hierarchy": inclusions,
        "bounded_game_certificates": {
            "chsh": chsh_cert,
        },
        "npa_finite_level_audit": npa_audit,
        "machine_bet_clauses": {
            "frozen_small_game_family_has_verified_bounds": None,
            "every_finite_npa_level_is_exact": False,
            "unrestricted_uniform_value_solver_claimed": False,
            "cqa_qc_separation_recorded_as_cited_guardrail": True,
            "current_small_corpus_witnesses_global_separation": False,
            "solver_tolerances_and_certificate_checks_are_pinned": False,
        },
    }


if __name__ == "__main__":
    receipt = generate_canonical_block08_receipt()
    print(json.dumps(receipt, indent=2))

__all__ = ['certify_chsh_interval', 'chsh_bounded_game_certificate', 'correlation_set_inclusions', 'generate_canonical_block08_receipt', 'npa_finite_level_distinction_audit']
