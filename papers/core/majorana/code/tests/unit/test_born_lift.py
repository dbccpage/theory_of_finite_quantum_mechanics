"""
Lev Landau Invariant & Unit Tests for qm_020_born_normalization_and_conditional_hilbert_lift.
Verifies L1 to L2 amplitude lift and Born rule probability normalization.
"""

import sys
import importlib.util
from pathlib import Path
import numpy as np
import pytest

from omega_engine.crates.quantum_physics.born_normalization import (
    PaperEvaluator,
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)


def test_qm020_paper_evaluator():
    """Verify PaperEvaluator returns EVALUATED_PASS with Born normalization."""
    evaluator = PaperEvaluator()
    res = evaluator.evaluate()
    assert res["paper_id"] == "qm_020_born_normalization_and_conditional_hilbert_lift"
    assert res["status"] == "EVALUATED_PASS"
    assert res["born_normalization"] is True


def test_l1_to_l2_amplitude_lift():
    """Verify L1 probability distribution converts to unit L2 Hilbert amplitude."""
    rho = np.array([3.0, 1.0])
    phases = np.array([0.0, np.pi / 2])
    psi = l1_to_l2_amplitude_lift(rho, phases)

    # sqrt(0.75)*e^{i0} and sqrt(0.25)*e^{i pi/2}
    assert pytest.approx(abs(psi[0]), 1e-6) == np.sqrt(0.75)
    assert pytest.approx(abs(psi[1]), 1e-6) == 0.5
    assert verify_born_normalization(psi)


