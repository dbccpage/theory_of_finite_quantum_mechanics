"""
test_su2_lattice_gauge.py — Integration Tests for SU(2) Lattice Gauge Theory under GIN Indexing.

AuthorityEffect: None.

Tests:
1. SU(2) Kogut-Susskind plaquette magnetic action gap Delta S = E_B(Q=1) - E_B(Q=0) = 4 / g^2.
2. Topological flux sectors Q in {0, 1} at theta = pi exhibit strictly DISJOINT weight spectra.
3. Disjoint weight spectra prevent weight-preserving involution pairing -> TerminalRoute.SplitBrainRefusal.
4. GIN mode posting lists accurately resolve color-fermion mode occupations.
5. Zero-theta unfrustrated control restores sign-free propagation.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from su2_lattice_gauge import (
    SU2LatticePlaquetteModel,
    SU2GinBridge,
    SU2SpectrumAuditReceipt,
)


def test_su2_gauge_action_gap():
    """Validates that non-trivial topological flux Q=1 incurs a finite action penalty Delta S = 4 / g^2."""
    g = 1.0
    model = SU2LatticePlaquetteModel(g_coupling=g, theta_angle=math.pi)

    e_q0 = model.evaluate_magnetic_flux_energy(0)
    e_q1 = model.evaluate_magnetic_flux_energy(1)

    assert e_q0 == pytest.approx(-2.0)
    assert e_q1 == pytest.approx(2.0)
    delta_s = e_q1 - e_q0
    assert delta_s == pytest.approx(4.0)


def test_su2_topological_flux_disjoint_weight_spectra():
    """
    Validates that at topological angle theta = pi, the positive (Q=0) and negative (Q=1)
    weight spectra under GIN mode indexing are strictly DISJOINT due to the non-zero action gap.
    """
    model = SU2LatticePlaquetteModel(g_coupling=1.0, theta_angle=math.pi)
    bridge = SU2GinBridge(in_memory=True)

    try:
        receipt = bridge.index_su2_model_paths(model, beta=1.0, model_name="SU2_Theta_Pi")

        assert receipt.positive_weight_count > 0
        assert receipt.negative_weight_count > 0

        assert len(receipt.spectral_overlap) == 0
        assert receipt.is_disjoint is True

        assert receipt.action_gap_delta_s == pytest.approx(4.0)
        assert receipt.uncancelled_defect_mass > 0.0

        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        bridge.close()


def test_su2_zero_theta_sign_free_control():
    """Validates that at theta = 0, the topological sign obstruction vanishes entirely."""
    model = SU2LatticePlaquetteModel(g_coupling=1.0, theta_angle=0.0)
    bridge = SU2GinBridge(in_memory=True)

    try:
        receipt = bridge.index_su2_model_paths(model, beta=1.0, model_name="SU2_Theta_Zero")

        assert receipt.negative_weight_count == 0
        assert receipt.positive_weight_count > 0
        assert receipt.uncancelled_defect_mass == 0.0
        assert receipt.terminal_route == "Repair"
    finally:
        bridge.close()


def test_su2_gin_posting_list_mode_resolution():
    """Validates that GIN inverted posting lists correctly track all 8 color-vertex modes."""
    model = SU2LatticePlaquetteModel(g_coupling=1.0, theta_angle=math.pi)
    bridge = SU2GinBridge(in_memory=True)

    try:
        bridge.index_su2_model_paths(model, beta=1.0, model_name="SU2_Posting_Audit")

        assert len(bridge.posting_index) > 0
        for m in range(1, 9):
            assert len(bridge.posting_index[m]) > 0
    finally:
        bridge.close()
