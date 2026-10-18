"""Tests for Gauge Group SU(3)xSU(2)xU(1), Higgs VEV, and SUSY Saturation Scale derivation.

AuthorityEffect: None.
"""

import os
import sys
import pytest

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from omega_engine.crates.solver.solv_gauge_higgs_susy_derivation import (
    derive_simplicial_gauge_group,
    derive_higgs_potential,
    compute_susy_saturation_scale,
    run_full_gauge_higgs_susy_derivation,
)


def test_simplicial_gauge_group_uniqueness():
    """Verify SU(3)xSU(2)xU(1) gauge group derivation from 3-2-1 simplicial chain hierarchy."""
    hierarchy = derive_simplicial_gauge_group()
    assert len(hierarchy) == 3

    dim_map = {b.dimension: b.associated_group for b in hierarchy}
    assert dim_map[2] == "SU(3)"
    assert dim_map[1] == "SU(2)"
    assert dim_map[0] == "U(1)"

    total_generators = sum(b.generators_count for b in hierarchy)
    assert total_generators == 8 + 3 + 1 == 12


def test_higgs_potential_and_vev():
    """Verify Higgs potential generation and electroweak VEV calculation."""
    higgs = derive_higgs_potential(mu2=15129.0, lam=0.25)
    assert higgs.vev_gev == 246.0
    assert higgs.is_spontaneously_broken is True
    assert pytest.approx(higgs.higgs_mass_gev, 0.1) == 173.95


def test_susy_saturation_scale():
    """Verify SUSY topological saturation scale in TeV."""
    scale = compute_susy_saturation_scale(vev_gev=246.0)
    assert pytest.approx(scale, 0.01) == 88.56

    scale_237 = compute_susy_saturation_scale(vev_gev=237.8)
    assert pytest.approx(scale_237, 0.01) == 85.608



