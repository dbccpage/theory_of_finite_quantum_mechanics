"""Campaign C500 Block 07: Finite Operational Reconstruction and Rivals.

Mechanizes:
1. Operational theory signatures:
   - System dimension, state space dimension D(A), effect space, channels.
2. Local tomography test across finite rivals:
   - Local tomography requires D(AB) = D(A) * D(B).
   - Classical: D(d) = d. D(d_A * d_B) = d_A * d_B = D(d_A) * D(d_B). (PASSES)
   - Complex quantum: D(d) = d^2. D(d_A * d_B) = (d_A * d_B)^2 = d_A^2 * d_B^2 = D(d_A) * D(d_B). (PASSES)
   - Real quantum: D(d) = d(d+1)/2. For d=2, D(2) = 3. D(4) = 10 != 3 * 3 = 9. (FAILS by deficit 1)
   - Quaternionic: D(d) = d(2d-1). For d=2, D(2) = 6. D(4) = 28 != 6 * 6 = 36. (FAILS by deficit 8)
3. Declared purification truth-table inputs (no state/purification evaluator):
   - Every mixed state can be purified to an essentially unique pure state on a bipartite extension.
   - Complex quantum: PASSES.
   - Classical theory: FAILS (simplex states admit no entangled purification).
4. Conditional selection in that declared Boolean table; operational-model
   reconstruction and axiom independence remain unverified.
5. Naimark dilation vs Born rule:
   - Naimark dilation embeds POVMs into projective measurements on an enlarged space,
     but the operator embedding alone does not derive Born probabilities.
     Probability evaluation via the trace pairing is a separate input.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
from typing import Any, Dict


def classical_state_dimension(d: int) -> int:
    """Real linear dimension of the state space of a d-outcome classical simplex."""
    return d


def complex_quantum_state_dimension(d: int) -> int:
    """Real linear dimension of the Hermitian operator space Herm_d(C): d^2."""
    return d * d


def real_quantum_state_dimension(d: int) -> int:
    """Real linear dimension of symmetric matrices Sym_d(R): d(d + 1) / 2."""
    return (d * (d + 1)) // 2


def quaternionic_quantum_state_dimension(d: int) -> int:
    """Real linear dimension of quaternionic Hermitian matrices Herm_d(H): d(2d - 1)."""
    return d * (2 * d - 1)


def evaluate_local_tomography(d_a: int, d_b: int) -> Dict[str, Any]:
    """Test local tomography D(AB) == D(A) * D(B) for classical, complex, real, quaternionic."""
    d_ab = d_a * d_b

    # Classical
    c_a = classical_state_dimension(d_a)
    c_b = classical_state_dimension(d_b)
    c_ab = classical_state_dimension(d_ab)
    classical_pass = (c_ab == c_a * c_b)

    # Complex
    z_a = complex_quantum_state_dimension(d_a)
    z_b = complex_quantum_state_dimension(d_b)
    z_ab = complex_quantum_state_dimension(d_ab)
    complex_pass = (z_ab == z_a * z_b)

    # Real
    r_a = real_quantum_state_dimension(d_a)
    r_b = real_quantum_state_dimension(d_b)
    r_ab = real_quantum_state_dimension(d_ab)
    real_pass = (r_ab == r_a * r_b)
    real_deficit = (r_a * r_b) - r_ab

    # Quaternionic
    h_a = quaternionic_quantum_state_dimension(d_a)
    h_b = quaternionic_quantum_state_dimension(d_b)
    h_ab = quaternionic_quantum_state_dimension(d_ab)
    quaternionic_pass = (h_ab == h_a * h_b)
    quaternionic_deficit = (h_a * h_b) - h_ab

    return {
        "subsystem_dimensions": {"d_A": d_a, "d_B": d_b, "d_AB": d_ab},
        "classical": {
            "D_A": c_a, "D_B": c_b, "D_AB": c_ab,
            "product": c_a * c_b, "local_tomography_holds": classical_pass
        },
        "complex_quantum": {
            "D_A": z_a, "D_B": z_b, "D_AB": z_ab,
            "product": z_a * z_b, "local_tomography_holds": complex_pass
        },
        "real_quantum": {
            "D_A": r_a, "D_B": r_b, "D_AB": r_ab,
            "product": r_a * r_b, "deficit": real_deficit,
            "local_tomography_holds": real_pass
        },
        "quaternionic_quantum": {
            "D_A": h_a, "D_B": h_b, "D_AB": h_ab,
            "product": h_a * h_b, "deficit": quaternionic_deficit,
            "local_tomography_holds": quaternionic_pass
        },
    }


def rival_axiom_matrix() -> Dict[str, Any]:
    """Evaluate a declared Boolean table, not an operational-model census.

    Axioms evaluated:
    1. Causality (unique deterministic effect, no signaling from future)
    2. Local Tomography (composite state determined by local measurements)
    3. Purification (every state purifies essentially uniquely)
    4. Continuous Reversibility (pure states connected by continuous reversible group)
    5. Superposition (existence of non-trivial coherent superpositions)
    """
    rivals = [
        {
            "theory_name": "Finite Classical Probability",
            "causality": True,
            "local_tomography": True,
            "purification": False,
            "continuous_reversibility": False,
            "superposition": False,
            "survives_some_axioms": True,
            "survives_all_axioms": False,
        },
        {
            "theory_name": "Finite Real Quantum Mechanics (Rebits)",
            "causality": True,
            "local_tomography": False,
            "purification": True,
            "continuous_reversibility": True,
            "superposition": True,
            "survives_some_axioms": True,
            "survives_all_axioms": False,
        },
        {
            "theory_name": "Finite Quaternionic Quantum Mechanics",
            "causality": True,
            "local_tomography": False,
            "purification": True,
            "continuous_reversibility": True,
            "superposition": True,
            "survives_some_axioms": True,
            "survives_all_axioms": False,
        },
        {
            "theory_name": "Finite Complex Quantum Mechanics",
            "causality": True,
            "local_tomography": True,
            "purification": True,
            "continuous_reversibility": True,
            "superposition": True,
            "survives_some_axioms": True,
            "survives_all_axioms": True,
        },
    ]
    axiom_names = ("causality", "local_tomography", "purification",
                   "continuous_reversibility", "superposition")
    for rival in rivals:
        rival["survives_some_axioms"] = any(rival[name] for name in axiom_names)
        rival["survives_all_axioms"] = all(rival[name] for name in axiom_names)
    selected = [rival["theory_name"] for rival in rivals
                if all(rival[name] for name in ("causality", "local_tomography", "purification"))]
    return {
        "candidate_rivals": rivals,
        "table_evidence_class": "DECLARED_ASSUMPTION",
        "uniquely_selects_complex_qm": selected == ["Finite Complex Quantum Mechanics"],
        "selected_table_rows": selected,
        "operational_model_uniqueness_proved": False,
        "selection_axioms": ["Causality", "Local Tomography", "Purification"],
    }


def naimark_dilation_audit() -> Dict[str, Any]:
    r"""Audit whether Naimark dilation alone derives Born rule uniqueness:

    VERDICT: FALSE.
    Naimark dilation shows that any POVM {E_i} on H can be realized as a projection
    measurement {P_i} on an enlarged space H (x) K with E_i = V^\dagger P_i V.
    However, the evaluation of probabilities p(i) = tr(rho E_i) uses the linear trace pairing
    as an initial input assumption; it does not derive the Born probability measure from
    state geometry without Gleason's theorem or Busch's effect-frame theorem.
    """
    return {
        "dilation_theorem": "Naimark Dilation: POVM -> Projective Measurement on Ancilla",
        "assumes_trace_pairing": False,
        "probability_evaluation_assumes_trace_pairing": True,
        "derives_born_rule_uniqueness": False,
        "status": "NON_DERIVATION",
        "audit_finding": "Naimark dilation is an operator identity; using trace pairing to evaluate probabilities is a separate input.",
    }


def generate_canonical_block07_receipt() -> Dict[str, Any]:
    """Generate the complete canonical receipt for Block 07."""
    tomo_2x2 = evaluate_local_tomography(2, 2)
    tomo_2x3 = evaluate_local_tomography(2, 3)
    tomo_3x3 = evaluate_local_tomography(3, 3)

    axioms = rival_axiom_matrix()
    naimark = naimark_dilation_audit()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_07",
        "global_targets": "C500-T451..C500-T475",
        "terminal_outcome": "OPERATIONAL_AXIOMS_PRICED",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "local_tomography_evaluations": {
            "qubit_qubit_2x2": tomo_2x2,
            "qubit_qutrit_2x3": tomo_2x3,
            "qutrit_qutrit_3x3": tomo_3x3,
        },
        "rival_axiom_comparison": axioms,
        "naimark_dilation_audit": naimark,
        "machine_bet_clauses": {
            "operational_axioms_derived_from_carrier_alone": False,
            "classical_rival_survives_some_but_not_all_axioms": True,
            "real_hilbert_rival_differs_on_composition_or_local_tomography": True,
            "naimark_dilation_alone_derives_born_uniqueness": False,
            "complex_model_selection_scope_is_explicit": False,
            "independent_axiom_subsets_are_frozen_before_search": False,
        },
    }


if __name__ == "__main__":
    receipt = generate_canonical_block07_receipt()
    print(json.dumps(receipt, indent=2))

__all__ = ['classical_state_dimension', 'complex_quantum_state_dimension', 'evaluate_local_tomography', 'generate_canonical_block07_receipt', 'naimark_dilation_audit', 'quaternionic_quantum_state_dimension', 'real_quantum_state_dimension', 'rival_axiom_matrix']
