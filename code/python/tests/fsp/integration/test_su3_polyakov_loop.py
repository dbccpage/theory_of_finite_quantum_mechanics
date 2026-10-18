"""
test_su3_polyakov_loop.py — Integration Tests for SU(3) Polyakov Loop Holonomies and Z_3 Center Symmetry.

AuthorityEffect: None.

Tests:
1. Polyakov order parameter <|P|> exhibits sharp transition between confined (beta < beta_c) and deconfined (beta > beta_c).
2. Confined phase (beta < beta_c): Delta S = 0, but Z_3 triality excess (1 real vs 2 complex sectors) leaves unpartnered paths -> SplitBrainRefusal.
3. Deconfined phase (beta > beta_c): Polyakov condensation <|P|> > 0 induces macroscopic action gap Delta S > 0,
   driving weight spectra into strictly DISJOINT supports (supp(W_+) cap supp(W_-) = emptyset).
4. Deconfining phase transition DOES NOT restore spectral overlap; it destroys degenerate overlap and amplifies spectral separation.
5. GIN mode posting lists accurately resolve all 6 color-spatial modes.
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

from src.fsp.su3_polyakov_loop import (
    SU3PolyakovLoopModel,
    SU3PolyakovGinBridge,
    SU3PolyakovAuditReceipt,
)


def test_polyakov_order_parameter_phase_transition():
    """Validates that Polyakov loop magnitude <|P|> vanishes in confined phase and is positive in deconfined phase."""
    beta_c = 5.69
    m_conf = SU3PolyakovLoopModel(beta=5.0, critical_beta=beta_c)
    m_deconf = SU3PolyakovLoopModel(beta=8.0, critical_beta=beta_c)

    assert m_conf.is_deconfined is False
    assert m_conf.evaluate_polyakov_order_parameter() == 0.0

    assert m_deconf.is_deconfined is True
    p_deconf = m_deconf.evaluate_polyakov_order_parameter()
    assert p_deconf > 0.0
    expected_p = math.sqrt(1.0 - (beta_c / 8.0) ** 2)
    assert p_deconf == pytest.approx(expected_p, rel=1e-5)


def test_confined_phase_triality_sign_excess():
    """
    Validates that in the confined phase (beta < beta_c), the center-rotated action gap vanishes (Delta S = 0),
    but Z_3 triality multiplicity (1 real positive vs 2 complex negative sectors) yields unpartnered negative paths.
    """
    bridge = SU3PolyakovGinBridge(in_memory=True)
    try:
        model = SU3PolyakovLoopModel(beta=4.0, fermion_hopping_h=0.1)
        receipt = bridge.index_polyakov_paths(model, model_name="SU3_Polyakov_Confined")

        assert receipt.temperature_regime == "Confined"
        assert receipt.polyakov_order_param == 0.0
        assert receipt.action_gap_delta_s == 0.0

        # Identical weights because |P| = 0
        assert receipt.is_disjoint is False
        assert len(receipt.spectral_overlap) > 0

        # Triality multiplicity: 8 positive paths vs 16 negative paths
        assert receipt.positive_weight_count == 8
        assert receipt.negative_weight_count == 16

        # 8 negative paths remain unpartnered -> SplitBrainRefusal
        assert receipt.uncancelled_defect_mass > 0.0
        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        bridge.close()


def test_deconfined_phase_disjoint_weight_spectra():
    """
    Validates that in the deconfined phase (beta > beta_c), Polyakov loop condensation (<|P|> > 0)
    induces a non-zero action gap Delta S > 0, forcing positive and negative weight spectra to be STRICTLY DISJOINT.
    Demonstrates that the deconfining phase transition DOES NOT restore spectral overlap.
    """
    bridge = SU3PolyakovGinBridge(in_memory=True)
    try:
        model = SU3PolyakovLoopModel(beta=8.0, fermion_hopping_h=0.1)
        receipt = bridge.index_polyakov_paths(model, model_name="SU3_Polyakov_Deconfined")

        assert receipt.temperature_regime == "Deconfined"
        assert receipt.polyakov_order_param > 0.70
        assert receipt.action_gap_delta_s > 1.20

        # Core Discovery: Spectral overlap is EMPTY
        assert len(receipt.spectral_overlap) == 0
        assert receipt.is_disjoint is True

        # Positive weights are strictly separated from negative weights
        assert min(receipt.positive_weight_support) > max(receipt.negative_weight_support)

        # Disjoint spectra obstruct weight-preserving involution pairing -> SplitBrainRefusal
        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        bridge.close()


def test_gin_mode_posting_list_resolution():
    """Validates that GIN inverted posting lists track all 6 color-spatial modes."""
    bridge = SU3PolyakovGinBridge(in_memory=True)
    try:
        model = SU3PolyakovLoopModel(beta=8.0)
        bridge.index_polyakov_paths(model, model_name="SU3_Polyakov_Modes")

        # Modes 1..6 must have non-empty posting lists
        assert len(bridge.posting_index) == 6
        for m in range(1, 7):
            assert len(bridge.posting_index[m]) > 0
    finally:
        bridge.close()
