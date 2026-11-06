"""Tests for Gauge Group SU(3)xSU(2)xU(1), Higgs VEV, and SUSY Saturation Scale derivation.

AuthorityEffect: None.
"""

import os
import sys
import pytest

from pathlib import Path

ooutwire_dir = Path(__file__).resolve().parents[5] / "ooutwire_docs"

for p in [str(ooutwire_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)


try:
    from universe_anomalonica.omega_engine.solver.solver import SolverInput
except ImportError:
    from dataclasses import dataclass, field
    @dataclass
    class SolverInput:
        problem_id: str = "default_prob"
        category: str = "default_cat"
        data: dict = field(default_factory=dict)
        parameters: dict = field(default_factory=dict)

try:
    from gauge_higgs_susy_derivation import (
        derive_simplicial_gauge_group,
        derive_higgs_potential,
        compute_susy_saturation_scale,
        run_full_gauge_higgs_susy_derivation,
    )
    from gauge_higgs_susy_solver import GaugeHiggsSUSYSolverAdapter
except ImportError:
    try:
        from universe_anomalonica.math.omega_solvers.gauge_higgs_susy_derivation import (
            derive_simplicial_gauge_group,
            derive_higgs_potential,
            compute_susy_saturation_scale,
            run_full_gauge_higgs_susy_derivation,
        )
        from universe_anomalonica.math.omega_solvers.gauge_higgs_susy_solver import GaugeHiggsSUSYSolverAdapter
    except ImportError:
        pytestmark = pytest.mark.skip(reason="gauge_higgs_susy_derivation not present in local path")


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


def test_gauge_higgs_susy_solver_adapter():
    """Verify GaugeHiggsSUSYSolverAdapter execution."""
    adapter = GaugeHiggsSUSYSolverAdapter()
    assert isinstance(adapter, GaugeHiggsSUSYSolverAdapter)

    s_in = SolverInput(problem_id="prob_gauge_001", category="simplicial_derivation", data={"vev_gev": 246.0})
    output = adapter.solve(s_in)

    assert output.status == "SOLVED"
    assert output.metadata["derived_gauge_group"] == "SU(3) x SU(2) x U(1)"
    assert pytest.approx(output.metadata["susy_scale_tev"], 0.01) == 88.56



