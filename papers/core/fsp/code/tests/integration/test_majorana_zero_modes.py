"""
test_majorana_zero_modes.py — Integration Tests for Kitaev Chain Majorana Zero Modes
Status: Integration Test Suite
AuthorityEffect: None

Tests:
1. Sweet-spot Kitaev chain (L=4, 8 modes) bulk pairing and boundary mode isolation.
2. ViewMajoranaZeroModeAudit verification in SQL GIN engine.
3. Assert Topological Protection status MZM_TOPOLOGICALLY_PROTECTED.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermion_gin_index import MockFermionGinIndex
from hamiltonian_gin_bridge import HamiltonianGinBridge


def test_kitaev_chain_majorana_zero_mode_isolation():
    """Validates that ViewMajoranaZeroModeAudit certifies boundary isolation of gamma_1 and gamma_2L."""
    gin = MockFermionGinIndex(in_memory=True)
    try:
        gin.build_kitaev_chain_majorana_model(L=4)

        mzm_rec = gin.verify_majorana_zero_modes(expected_edges=(1, 8))
        assert mzm_rec.is_boundary_isolated is True
        assert set(mzm_rec.unpaired_zero_modes) == {1, 8}
        assert mzm_rec.mzm_status == "MZM_TOPOLOGICALLY_PROTECTED"
        assert len(mzm_rec.bulk_bonded_modes) == 6  # Modes 2, 3, 4, 5, 6, 7 are bulk bonded
    finally:
        gin.close()


def test_kitaev_chain_majorana_bridge_scaling():
    """Tests boundary isolation across multiple chain lengths L=3 and L=5."""
    for L in (3, 5):
        bridge = HamiltonianGinBridge(in_memory=True)
        try:
            mzm = bridge.index_kitaev_chain_majorana(L=L, model_name=f"KitaevL{L}")
            assert mzm.is_boundary_isolated is True
            assert set(mzm.unpaired_zero_modes) == {1, 2 * L}
            assert len(mzm.bulk_bonded_modes) == 2 * L - 2
            assert mzm.mzm_status == "MZM_TOPOLOGICALLY_PROTECTED"
        finally:
            bridge.close()
