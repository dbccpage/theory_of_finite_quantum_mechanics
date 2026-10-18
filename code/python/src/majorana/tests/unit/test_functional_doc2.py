"""Narrow tests for the omega_functional doc2 defect fixes.

Covers the highest-priority Xi fix (one-zero/one-nonzero comparison must be
None, not a success-looking 0.0) plus a sample of the validation guards added
across the package.
"""

import numpy as np
import pytest

from omega_engine.crates.functional.density_lift import compute_xi
from omega_engine.crates.functional.gamma2 import cycle_coboundary, gamma2
from omega_engine.crates.functional.norms import lp_norm, lp_subadditivity
from omega_engine.crates.functional.phi1 import phi1
from omega_engine.crates.functional.aggregation import AggregationMonotonicity


# ---- HIGHEST PRIORITY: compute_xi zero/nonzero asymmetry ----


def test_compute_xi_one_zero_one_nonzero_is_none():
    """Exactly one side zero => comparison undefined => None (not 0.0)."""
    zero_vec = np.zeros(3)
    nonzero_vec = np.array([1.0, 2.0, 3.0])
    assert compute_xi(zero_vec, nonzero_vec) is None
    assert compute_xi(nonzero_vec, zero_vec) is None


def test_compute_xi_identical_is_zero():
    v = np.array([1.0, -2.0, 0.5])
    assert compute_xi(v, v) == 0.0


def test_compute_xi_both_zero_is_zero():
    z = np.zeros(4)
    assert compute_xi(z, z) == 0.0


# ---- gamma2 validation guards (defect 3) ----


def test_cycle_coboundary_rejects_bad_orientation():
    with pytest.raises(ValueError):
        cycle_coboundary(3, [[(0, 2)]])  # orientation 2 not in {+1,-1}


def test_cycle_coboundary_rejects_out_of_range_edge():
    with pytest.raises(ValueError):
        cycle_coboundary(2, [[(5, 1)]])  # edge index 5 >= num_edges


def test_gamma2_rejects_negative_tolerance():
    d1 = cycle_coboundary(3, [[(0, 1), (1, 1), (2, -1)]])
    with pytest.raises(ValueError):
        gamma2(d1, np.array([1.0, 0.0, 0.0]), tolerance=-1.0)


# ---- norms validation guards (defect 12) ----


def test_lp_norm_rejects_nonpositive_p():
    with pytest.raises(ValueError):
        lp_norm(np.array([1.0, 2.0]), 0.0)


def test_lp_norm_empty_is_zero():
    assert lp_norm(np.array([]), 2.0) == 0.0


def test_lp_subadditivity_rejects_p_lt_1_without_quasi_flag():
    with pytest.raises(ValueError):
        lp_subadditivity(np.array([1.0]), np.array([1.0]), 0.5)


# ---- phi1 validation guards (defect 11) ----


def test_phi1_rejects_edge_endpoint_out_of_range():
    with pytest.raises(ValueError):
        phi1(2, [(0, 5)], [1.0])  # endpoint 5 outside [0, 2)


def test_phi1_rejects_length_mismatch():
    with pytest.raises(ValueError):
        phi1(3, [(0, 1), (1, 2)], [1.0])  # omega1 len != edge count


# ---- aggregation validation guard (defect 7) ----


def test_coarse_grain_rejects_non_divisible_block_size():
    with pytest.raises(ValueError):
        AggregationMonotonicity.coarse_grain_1d(
            [1.0, 2.0, 3.0], [(0, 1), (1, 2)], block_size=2
        )


