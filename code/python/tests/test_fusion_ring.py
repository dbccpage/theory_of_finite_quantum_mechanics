"""Tests for the FusionRing and FusionTable Python dual-implementation."""

import pytest
import math
from src.fusion_categories.fusion_ring import (
    AbelianGroup,
    FusionTable,
    FusionRing,
    RingDefectType,
)


def test_abelian_group_properties():
    grp = AbelianGroup([2, 3])
    assert grp.order == 6
    assert grp.moduli == [2, 3]

    # Digits and labels
    for lbl in range(6):
        digits = grp.digits(lbl)
        assert grp.label(digits) == lbl

    # Addition and negation
    assert grp.add(0, 5) == 5
    assert grp.add(1, 1) == grp.label([0, 0])
    for a in range(6):
        neg = grp.negate(a)
        assert grp.add(a, neg) == 0

    with pytest.raises(ValueError):
        AbelianGroup([1])
    with pytest.raises(ValueError):
        grp.digits(6)


def test_ising_fusion_ring():
    ising = FusionRing.ising()
    assert ising.rank == 3
    assert ising.names == ["1", "sigma", "psi"]

    # Duals (all self-dual in Ising)
    assert ising.dual(0) == 0
    assert ising.dual(1) == 1
    assert ising.dual(2) == 2

    # Multiplication rules
    # sigma x sigma = 1 + psi
    assert ising.n(1, 1, 0) == 1
    assert ising.n(1, 1, 1) == 0
    assert ising.n(1, 1, 2) == 1

    # sigma x psi = sigma
    assert ising.n(1, 2, 1) == 1

    # psi x psi = 1
    assert ising.n(2, 2, 0) == 1

    # Bratteli path count
    # 1 -> sigma -> 1 : 1 path
    assert ising.fusion_path_count(0, [1], 1) == 1
    # 1 -> sigma -> sigma -> 1 : 1 path (via 1)
    assert ising.fusion_path_count(0, [1, 1], 0) == 1
    assert ising.fusion_path_count(0, [1, 1], 2) == 1

    # Frobenius-Perron dimensions
    d_0 = ising.frobenius_perron_dimension(0)
    d_sigma = ising.frobenius_perron_dimension(1)
    d_psi = ising.frobenius_perron_dimension(2)
    assert pytest.approx(d_0, rel=1e-4) == 1.0
    assert pytest.approx(d_sigma, rel=1e-4) == math.sqrt(2)
    assert pytest.approx(d_psi, rel=1e-4) == 1.0

    # Global dimension squared D^2 = 1^2 + (sqrt(2))^2 + 1^2 = 4
    assert pytest.approx(ising.global_dimension_squared(), rel=1e-4) == 4.0


def test_fibonacci_fusion_ring():
    fib = FusionRing.fibonacci()
    assert fib.rank == 2
    assert fib.names == ["1", "tau"]

    # tau x tau = 1 + tau
    assert fib.n(1, 1, 0) == 1
    assert fib.n(1, 1, 1) == 1

    phi = (1 + math.sqrt(5)) / 2
    d_tau = fib.frobenius_perron_dimension(1)
    assert pytest.approx(d_tau, rel=1e-4) == phi

    # D^2 = 1 + phi^2 = (5 + sqrt(5)) / 2
    expected_d2 = 1 + phi ** 2
    assert pytest.approx(fib.global_dimension_squared(), rel=1e-4) == expected_d2


def test_toric_code_ring():
    toric = FusionRing.toric_code()
    assert toric.rank == 4
    for a in range(4):
        assert pytest.approx(toric.frobenius_perron_dimension(a), rel=1e-4) == 1.0
    assert pytest.approx(toric.global_dimension_squared(), rel=1e-4) == 4.0


def test_rep_s3_ring():
    s3 = FusionRing.rep_s3()
    assert s3.rank == 3
    assert pytest.approx(s3.frobenius_perron_dimension(0), rel=1e-4) == 1.0
    assert pytest.approx(s3.frobenius_perron_dimension(1), rel=1e-4) == 1.0
    assert pytest.approx(s3.frobenius_perron_dimension(2), rel=1e-4) == 2.0
    # D^2 = 1^2 + 1^2 + 2^2 = 6
    assert pytest.approx(s3.global_dimension_squared(), rel=1e-4) == 6.0


def test_defect_detection():
    # Mutate unit law
    mutated = [
        [[0, 0], [0, 1]],
        [[0, 1], [1, 1]],
    ]
    t = FusionTable.from_3d(mutated)
    defect = t.first_defect()
    assert defect is not None
    assert defect.defect_type == RingDefectType.UNIT
