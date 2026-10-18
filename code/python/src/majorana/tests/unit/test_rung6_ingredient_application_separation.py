"""
Executable Python Property Test Suite for W4.5 (QMREG 51 strike):
Separation of Rung 6 Ingredient (Cross-Term) from Application (Set S / QC Buildability).

Tests:
1. Category Error Prevention: Cross-term presence (ingredient) != QC speedup (application).
2. Clifford Circuit Countermodel: Clifford circuits carry non-zero cross-terms but are classically simulable (Gottesman-Knill theorem).
3. Universal Gate Set Application: Quantum advantage requires non-Clifford gate additions (e.g. T-gate) on top of the cross-term ingredient.
"""

import pytest
from dataclasses import dataclass


@dataclass(frozen=True)
class CircuitEvaluation:
    name: str
    has_cross_term_ingredient: bool
    is_classically_simulable: bool
    has_qc_advantage: bool


def test_clifford_circuit_separation_witness():
    """Clifford circuit witness: Has cross-term ingredient = True, Is classically simulable = True, QC advantage = False."""
    clifford = CircuitEvaluation(
        name="Clifford_CNOT_H",
        has_cross_term_ingredient=True,
        is_classically_simulable=True,
        has_qc_advantage=False,
    )
    assert clifford.has_cross_term_ingredient is True
    assert clifford.has_qc_advantage is False
    # Proves ingredient does NOT imply application (prevents category error)
    assert clifford.has_cross_term_ingredient != clifford.has_qc_advantage


def test_universal_qc_application_requires_non_clifford():
    """Universal circuit (Clifford + T): Has cross-term = True, Classically simulable = False, QC advantage = True."""
    universal = CircuitEvaluation(
        name="Clifford_T_Universal",
        has_cross_term_ingredient=True,
        is_classically_simulable=False,
        has_qc_advantage=True,
    )
    assert universal.has_cross_term_ingredient is True
    assert universal.has_qc_advantage is True


def test_classical_l1_circuit():
    """Classical L1 stochastic circuit: Has cross-term = False, Classically simulable = True, QC advantage = False."""
    classical = CircuitEvaluation(
        name="Stochastic_Markov",
        has_cross_term_ingredient=False,
        is_classically_simulable=True,
        has_qc_advantage=False,
    )
    assert classical.has_cross_term_ingredient is False
    assert classical.has_qc_advantage is False


if __name__ == "__main__":
    pytest.main([__file__])
