from __future__ import annotations
"""Unit test suite for Single-Edge Indicator Sharp L1/L2 Distortion Bound.

Direct Python verification of Lean 4 theorems in `single_edge_indicator.lean`:
- `UniverseAnomalonica.SingleEdgeIndicator.l1_l2_relation`
"""


import numpy as np
import pytest

from omega_engine.crates.solver.solv_single_edge_indicator import (
    SingleEdgeIndicatorCert,
    compute_n_cycle_single_edge_distortion,
)


def test_single_edge_indicator_sharp_bound():
    """Verify sharp closed-form distortion ratio sqrt(n) across n >= 3."""
    for n in [3, 4, 5, 10, 100]:
        cert = compute_n_cycle_single_edge_distortion(n)
        assert cert.is_sharp is True
        assert cert.l1_quotient_norm == 1.0
        assert cert.l2_projection_norm == pytest.approx(1.0 / np.sqrt(n))
        assert cert.sharp_ratio == pytest.approx(np.sqrt(n))
        assert cert.authority_effect == "None"


def test_single_edge_asymptotic_limit():
    """Verify asymptotic growth as n -> inf."""
    cert_1000 = compute_n_cycle_single_edge_distortion(1000)
    assert cert_1000.sharp_ratio == pytest.approx(np.sqrt(1000))



