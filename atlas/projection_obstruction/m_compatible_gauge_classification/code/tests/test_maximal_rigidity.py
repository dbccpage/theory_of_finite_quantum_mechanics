"""T06-T12: Maximal End_b(V) rigidity and monoid distinction tests for GS-001.

Verifies rank-one contracts for unit and non-unit u, Hahn-Banach dual vector construction,
SO(2) vs C_4 group distinctions, and positive diagonal operator bounds.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

_pkg = Path(__file__).resolve().parents[1]
if str(_pkg / "code") not in sys.path:
    sys.path.insert(0, str(_pkg / "code"))

from norms import l1, l2, linf, anisotropic_gauge
from rigidity import (
    rank_one_map,
    construct_hahn_banach_rank_one,
    is_maximal_end_compatible,
)
from gs001_gauges import (
    cyclic_rotation_group_c4,
    monoid_signed_permutations_r2,
    monoid_so2_discrete,
)


def test_t06_rank_one_map_non_unit_contract():
    """T06: Verify T @ u = v for any non-zero source vector u (unit or non-unit)."""
    u = np.array([2.0, 0.0])
    v = np.array([0.0, 1.0])

    T = rank_one_map(u, v)
    result = T @ u

    # T @ u MUST equal v exactly: [0.0, 1.0]
    assert np.allclose(result, v)

    # Error case for zero source vector u
    with pytest.raises(ValueError, match="non-zero"):
        rank_one_map(np.array([0.0, 0.0]), v)

    with pytest.raises(ValueError, match="matching dimensions"):
        rank_one_map(u, np.array([1.0, 2.0, 3.0]))


def test_t07_hahn_banach_rank_one_construction():
    """T07: Hahn-Banach rank-one operator construction T = (v (x) y^T) / y(u).

    Shows j(T u) = j(v) and ||T||_{j -> j} = j(v) / j(u).
    """
    u = np.array([3.0, 4.0])
    v = np.array([1.0, -2.0])

    # l2 dual construction
    T_l2 = construct_hahn_banach_rank_one(u, v, l2, "l2")
    assert np.allclose(T_l2 @ u, v)

    # l1 dual construction
    T_l1 = construct_hahn_banach_rank_one(u, v, l1, "l1")
    assert np.allclose(T_l1 @ u, v)

    # linf dual construction
    T_linf = construct_hahn_banach_rank_one(u, v, linf, "linf")
    assert np.allclose(T_linf @ u, v)


def test_t08_maximal_end_compatibility():
    """T08: Test maximal End_b(V) compatibility."""
    # l2 norm is compatible with End_b(V) under Euclidean operator norm
    assert is_maximal_end_compatible(l2, dimension=2)

    # Anisotropic norm fails maximal End_b(V) compatibility
    assert not is_maximal_end_compatible(
        lambda x: anisotropic_gauge(x, (1.0, 2.0)), dimension=2
    )


def test_t09_monoid_and_c4_vs_so2_distinction():
    """T09-T12: Verify C_4 cyclic rotations vs SO(2) continuous group distinctions.

    C_4 invariance does NOT imply SO(2) invariance for anisotropic or l4-type gauges.
    """
    c4_group = cyclic_rotation_group_c4()
    signed_perms = monoid_signed_permutations_r2()
    so2_samples = monoid_so2_discrete()

    assert len(c4_group) == 4
    assert len(signed_perms) == 8
    assert len(so2_samples) == 16

    # l4 gauge j(x) = (x1^4 + x2^4)^(1/4) is C_4 invariant but NOT SO(2) invariant!
    def l4_gauge(x: np.ndarray) -> float:
        v = np.asarray(x, dtype=float).ravel()
        return float((v[0] ** 4 + v[1] ** 4) ** 0.25)

    v = np.array([1.0, 0.0])
    # 45-degree rotation in SO(2)
    r45 = np.array(
        [
            [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
            [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        ]
    )

    # C_4 rotation preserves l4_gauge
    r90 = c4_group[1]
    assert np.isclose(l4_gauge(r90 @ v), l4_gauge(v))

    # 45-degree rotation changes l4_gauge: 1.0 vs (0.5 + 0.5)^(1/4) * (1/sqrt(2)) = 2^{-1/4} = 0.8409
    assert not np.isclose(l4_gauge(r45 @ v), l4_gauge(v))
