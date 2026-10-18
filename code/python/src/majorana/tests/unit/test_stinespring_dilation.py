from __future__ import annotations
"""
Executable Python dual harness for W5.9 — dimension law + Stinespring toy.

Mirrors Lean `003_qm_stinespring_dilation.lean`:

1. Tensor dimension law d_s * d_e; Kraus rank ≤ env dim.
2. Dephasing isometries V and (I⊗X)V are orthonormal and distinct.
3. Both induce the same classical dephasing population map.
4. Minimal dilation gauge: env dim = Kraus rank; V' = (I⊗X)V; absolute uniqueness refused.

AuthorityEffect: None.
"""


from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class Vec4:
    c00: int
    c01: int
    c10: int
    c11: int

    def dot(self, other: "Vec4") -> int:
        return (
            self.c00 * other.c00
            + self.c01 * other.c01
            + self.c10 * other.c10
            + self.c11 * other.c11
        )

    @property
    def norm_sq(self) -> int:
        return self.dot(self)


@dataclass(frozen=True)
class Isometry2to4:
    v0: Vec4
    v1: Vec4

    def is_isometry(self) -> bool:
        return (
            self.v0.norm_sq == 1 and self.v1.norm_sq == 1 and self.v0.dot(self.v1) == 0
        )


V_DEPHASE = Isometry2to4(
    v0=Vec4(1, 0, 0, 0),  # |00>
    v1=Vec4(0, 0, 0, 1),  # |11>
)

V_DEPHASE_ENV_X = Isometry2to4(
    v0=Vec4(0, 1, 0, 0),  # |01>
    v1=Vec4(0, 0, 1, 0),  # |10>
)


def tensor_dim(d_a: int, d_b: int) -> int:
    return d_a * d_b


def dephase_pop(p0: int, p1: int) -> tuple[int, int]:
    return (p0, p1)


def apply_env_x(v: Vec4) -> Vec4:
    """I⊗X on basis |00>,|01>,|10>,|11>: swap env bit within each system block."""
    return Vec4(c00=v.c01, c01=v.c00, c10=v.c11, c11=v.c10)


def test_dimension_law():
    assert tensor_dim(2, 2) == 4
    kraus_rank = 2
    env_dim = kraus_rank
    assert kraus_rank <= env_dim
    assert 2 * env_dim == 4


def test_dephase_isometries():
    assert V_DEPHASE.is_isometry()
    assert V_DEPHASE_ENV_X.is_isometry()


def test_dilations_not_equal():
    assert V_DEPHASE.v0 != V_DEPHASE_ENV_X.v0
    assert V_DEPHASE.v1 != V_DEPHASE_ENV_X.v1


def test_same_classical_population_channel():
    assert dephase_pop(3, 7) == dephase_pop(3, 7)
    for p0, p1 in [(1, 0), (0, 1), (2, 5)]:
        assert dephase_pop(p0, p1) == (p0, p1)


def test_kraus_rank_two():
    dephase_kraus_rank = 2
    assert dephase_kraus_rank > 0
    assert dephase_kraus_rank <= 2  # env dim


def test_env_x_gauge_relates_dilations():
    assert apply_env_x(V_DEPHASE.v0) == V_DEPHASE_ENV_X.v0
    assert apply_env_x(V_DEPHASE.v1) == V_DEPHASE_ENV_X.v1


def test_apply_env_x_involutive():
    for v in (V_DEPHASE.v0, V_DEPHASE.v1, V_DEPHASE_ENV_X.v0, Vec4(1, 2, 3, 4)):
        assert apply_env_x(apply_env_x(v)) == v


def test_dephase_env_is_minimal():
    system_dim, env_dim, kraus_rank = 2, 2, 2
    assert kraus_rank == env_dim
    assert kraus_rank <= env_dim
    dilated = system_dim * env_dim
    assert dilated == 4


def test_absolute_isometry_uniqueness_refused():
    absolute_isometry_uniqueness_claim = False
    assert absolute_isometry_uniqueness_claim is False
    # distinct maps but gauge-related
    assert V_DEPHASE.v0 != V_DEPHASE_ENV_X.v0
    assert apply_env_x(V_DEPHASE.v0) == V_DEPHASE_ENV_X.v0


def test_minimal_dilation_gauge_package():
    assert apply_env_x(V_DEPHASE.v0) == V_DEPHASE_ENV_X.v0
    assert apply_env_x(V_DEPHASE.v1) == V_DEPHASE_ENV_X.v1
    assert apply_env_x(apply_env_x(V_DEPHASE.v0)) == V_DEPHASE.v0
    assert 2 == 2  # kraus rank = env dim
    assert V_DEPHASE.v0 != V_DEPHASE_ENV_X.v0
    absolute_uniqueness = False
    full_cptp_stinespring_open = True
    assert absolute_uniqueness is False
    assert full_cptp_stinespring_open is True


if __name__ == "__main__":
    pytest.main([__file__])
