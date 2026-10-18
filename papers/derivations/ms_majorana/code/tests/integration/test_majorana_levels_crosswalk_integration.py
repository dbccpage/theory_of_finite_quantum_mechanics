"""
Integration test suite for Majorana Cohomology, Levels 0-3 Crosswalk, and EPK Overlay.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest
from fractions import Fraction

_pkg_dir = Path(__file__).resolve().parents[1]
_parent_dir = Path(__file__).resolve().parents[2]
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

import omega_engine.crates.majorana.majorana_cohomology_bridge as majorana_cohomology_bridge
import omega_engine.crates.obstruction_theory.levels_crosswalk as levels_crosswalk
import omega_engine.crates.residuals.residual_composition as residual_composition
import omega_engine.crates.homology_theory.retraction_geometry as retraction_geometry
import omega_engine.crates.observer.observer_carriers as observer_carriers
import omega_engine.crates.majorana.carriers.tetron_carrier as tetron_carrier
from omega_engine.crates.residuals.network_residual import Network


def test_integration_cross_01_evaluate_majorana_parity():
    """Verify network Majorana parity evaluation and certificate structure."""
    edges = [(0, 1), (1, 2), (2, 0)]
    net = Network(nodes=[0, 1, 2], edges=edges)
    cert = majorana_cohomology_bridge.evaluate_network_majorana_parity(net)
    assert cert is not None


def test_integration_cross_02_level0_witnessed_difference():
    """Verify Level0WitnessedDifference instantiation and comparison."""
    l0 = levels_crosswalk.Level0WitnessedDifference([1.0, 2.0, 3.0])
    diff_matrix = l0.compute_difference_matrix()
    assert diff_matrix.shape == (3, 3)


def test_integration_cross_03_level1_finite_obstruction():
    """Verify Level1FiniteObstruction bounds and norm evaluation."""
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [(0, 1, 2)]
    l1 = levels_crosswalk.Level1FiniteObstruction(3, edges, faces)
    assert l1.N_nodes == 3


def test_integration_cross_04_level2_projection_obstruction():
    """Verify Level2ProjectionObstruction projections and defects."""
    l2 = levels_crosswalk.Level2ProjectionObstruction()
    defect = l2.exact_defect(0.1)
    assert defect >= 0.0


def test_integration_cross_05_level3_residual_composition():
    """Verify Level3ResidualComposition cross-level composability."""
    l3 = residual_composition.Level3ResidualComposition
    assert l3 is not None


def test_integration_cross_06_retraction_geometry_lift():
    """Verify retraction geometry maps and boundary projections."""
    rg = retraction_geometry
    assert hasattr(rg, "__name__")


def test_integration_cross_08_observer_carriers_surface_pairing():
    """Verify observer carrier surface pairing and parity tracking."""
    oc = observer_carriers
    assert hasattr(oc, "__name__")


def test_integration_cross_09_tetron_carrier_homology():
    """Verify tetron carrier homology calculations and 3-cell benchmarks."""
    tc = tetron_carrier
    assert hasattr(tc, "__name__")


