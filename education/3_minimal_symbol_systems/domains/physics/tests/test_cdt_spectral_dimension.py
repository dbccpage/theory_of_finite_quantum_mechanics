"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import math
import subprocess
import sys
from pathlib import Path

import yaml

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from cdt_spectral_dimension import (
    CdtDualGraph,
    DiscreteHeatDiffusionEngine,
)






def test_stochastic_transition_matrix():
    """Validates that discrete diffusion transition matrix M_ij is row-stochastic."""
    num_nodes, adj = CdtDualGraph.construct_flat_4d_grid(L=3)
    M = DiscreteHeatDiffusionEngine.build_transition_matrix(num_nodes, adj)
    assert len(M) == num_nodes
    for i, row in enumerate(M):
        row_sum = sum(row)
        assert math.isclose(row_sum, 1.0, rel_tol=1e-9), f"Row {i} sum was {row_sum}"


def test_return_probability_monotonicity():
    """Validates that return probability P(0) = 1.0 and decays monotonically on flat grid."""
    num_nodes, adj = CdtDualGraph.construct_flat_4d_grid(L=3)
    P = DiscreteHeatDiffusionEngine.compute_return_probability_random_walk(
        num_nodes, adj, tau_max=15
    )
    assert P[0] == 1.0
    for tau in range(1, len(P)):
        assert P[tau] >= 0.0, f"Negative return prob at tau={tau}"
        assert P[tau] <= P[tau - 1] + 1e-9, f"Non-monotonic return prob: P({tau}) > P({tau - 1})"




def test_cdt_sandwich_diffusion_dimensional_reduction():
    """Evaluates diffusion on simulated 4D CDT sandwich complex and verifies dimensional reduction."""
    engine = DiscreteHeatDiffusionEngine(in_memory=True)
    # 8 time layers, spatial size 5
    receipt = engine.evaluate_cdt_sandwich_diffusion(num_layers=8, spatial_size=5, tau_max=25)

    assert receipt.has_slope_crossover is True
    assert receipt.d_short < receipt.d_macro
    assert receipt.d_short < 3.0
    assert receipt.d_macro >= 3.2

    # Check that steps are recorded
    assert len(receipt.steps) == 25
    engine.close()


def test_finite_size_saturation_guard():
    """Validates that on any finite complex, finite-volume saturation causes d_s -> 0 as tau -> infty."""
    engine = DiscreteHeatDiffusionEngine(in_memory=True)
    # Small sandwich, large diffusion time
    receipt = engine.evaluate_cdt_sandwich_diffusion(num_layers=4, spatial_size=3, tau_max=35)
    # Late steps should exhibit low spectral dimension / saturation
    late_steps = receipt.steps[-5:]
    avg_late_ds = sum(s.spectral_dimension for s in late_steps) / len(late_steps)
    assert avg_late_ds < 1.5, f"Expected finite-size saturation, got late d_s={avg_late_ds}"
    engine.close()
