"""Lev Landau Invariant & Comprehensive Unit Tests for GS-001 (gs001_gauges facade).

AuthorityEffect: None.
"""

import sys
from pathlib import Path
import numpy as np

_pkg = Path(__file__).resolve().parents[1]
if str(_pkg / "code") not in sys.path:
    sys.path.insert(0, str(_pkg / "code"))

from gs001_gauges import (
    l1,
    l2,
    linf,
    anisotropic_gauge,
    probe_counterexample_search,
    is_faithful,
    is_absolutely_homogeneous,
    is_subadditive,
    is_m_compatible,
    monoid_trivial,
    monoid_signed_permutations_r2,
    cyclic_rotation_group_c4,
    monoid_so2_discrete,
)


def test_standard_norms_and_predicates():
    """Verify standard norms, faithfulness, homogeneity, subadditivity, and compatibility."""
    v = np.array([3.0, -4.0])
    assert l1(v) == 7.0
    assert l2(v) == 5.0
    assert linf(v) == 4.0
    assert anisotropic_gauge(v, (1.0, 2.0)) == 11.0

    # Faithfulness
    samples = [v, np.array([1.0, 0.0])]
    assert is_faithful(l1, samples)
    assert not is_faithful(lambda x: 0.0, samples)

    # Absolute homogeneity
    assert is_absolutely_homogeneous(l1, v, [-2.0, -1.0, 0.5, 3.0])
    assert not is_absolutely_homogeneous(lambda x: float(np.sum(x**2)), v, [2.0])

    # Subadditivity
    pairs = [(np.array([1.0, 2.0]), np.array([3.0, 4.0]))]
    assert is_subadditive(l1, pairs)

    # Compatibility
    ops = [np.eye(2), np.array([[1.0, 0.0], [0.0, 0.5]])]
    assert is_m_compatible(l2, ops, ambient_norm=l2)


def test_monoids_and_counterexample_results():
    """Verify monoid helpers and counterexample probe execution."""
    triv = monoid_trivial(2)
    assert len(triv) == 1 and np.allclose(triv[0], np.eye(2))

    sp = monoid_signed_permutations_r2()
    assert len(sp) == 8

    c4 = cyclic_rotation_group_c4()
    assert len(c4) == 4

    so2 = monoid_so2_discrete(8)
    assert len(so2) == 8

    # Counterexample result
    res = probe_counterexample_search(lambda x: l1(x) > 0, [np.array([1.0, 2.0])])
    assert not res.found_counterexample
    assert "Counterexample" in res.description
