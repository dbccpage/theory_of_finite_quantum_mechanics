"""
Unit Tests for Smith Normal Form, Simplicial Complexes & Torsion Homology
AuthorityEffect: None
"""

import sys
from pathlib import Path

_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from smith_normal_form import (
    SmithNormalForm,
    _mat_mul,
    build_klein_bottle_complex,
    build_moore_space_complex,
    build_rp2_complex,
    build_sphere_complex,
)


def test_rp2_boundary_nilpotency_and_homology():
    """Validates RP^2 complex: Stokes nilpotency d1 * d2 = 0 and H_1 = Z/2Z torsion."""
    f, d1, d2 = build_rp2_complex()
    assert f == [6, 15, 10]

    # 1. Nilpotency
    prod = _mat_mul(d1, d2)
    assert all(all(x == 0 for x in row) for row in prod), (
        "RP2 boundary operator must satisfy d1 * d2 = 0"
    )

    # 2. Homology groups
    h0 = SmithNormalForm.compute_homology(None, d1, f[0], dim=0)
    h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
    h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)

    assert h0.betti_number == 1 and h0.torsion_coefficients == [] and h0.homology_group_str == "Z"
    assert (
        h1.betti_number == 0 and h1.torsion_coefficients == [2] and h1.homology_group_str == "Z/2Z"
    )
    assert h2.betti_number == 0 and h2.torsion_coefficients == [] and h2.homology_group_str == "0"

    # 3. Euler characteristic
    chi = f[0] - f[1] + f[2]
    assert chi == 1


def test_klein_bottle_boundary_nilpotency_and_homology():
    """Validates Klein Bottle complex: Stokes nilpotency d1 * d2 = 0 and H_1 = Z (+) Z/2Z."""
    f, d1, d2 = build_klein_bottle_complex()
    assert f == [12, 36, 24]

    # 1. Nilpotency
    prod = _mat_mul(d1, d2)
    assert all(all(x == 0 for x in row) for row in prod), (
        "Klein bottle boundary must satisfy d1 * d2 = 0"
    )

    # 2. Homology groups
    h0 = SmithNormalForm.compute_homology(None, d1, f[0], dim=0)
    h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
    h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)

    assert h0.betti_number == 1 and h0.torsion_coefficients == [] and h0.homology_group_str == "Z"
    assert (
        h1.betti_number == 1
        and h1.torsion_coefficients == [2]
        and h1.homology_group_str == "Z (+) Z/2Z"
    )
    assert h2.betti_number == 0 and h2.torsion_coefficients == [] and h2.homology_group_str == "0"

    # 3. Euler characteristic
    chi = f[0] - f[1] + f[2]
    assert chi == 0


def test_sphere_boundary_nilpotency_and_homology():
    """Validates Sphere S^2 complex: Stokes nilpotency d1 * d2 = 0 and H_2 = Z."""
    f, d1, d2 = build_sphere_complex()
    assert f == [4, 6, 4]

    prod = _mat_mul(d1, d2)
    assert all(all(x == 0 for x in row) for row in prod), "Sphere boundary must satisfy d1 * d2 = 0"

    h0 = SmithNormalForm.compute_homology(None, d1, f[0], dim=0)
    h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
    h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)

    assert h0.betti_number == 1 and h0.torsion_coefficients == []
    assert h1.betti_number == 0 and h1.torsion_coefficients == []
    assert h2.betti_number == 1 and h2.torsion_coefficients == []

    chi = f[0] - f[1] + f[2]
    assert chi == 2


def test_moore_space_homology_and_torsion():
    """Validates Moore spaces M(Z/mZ, 1) having H_1 = Z/mZ for m in [2, 3, 5, 7]."""
    for m in [2, 3, 5, 7]:
        f, d1, d2 = build_moore_space_complex(m)
        h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
        h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)
        assert h1.betti_number == 0 and h1.torsion_coefficients == [m]
        assert h2.betti_number == 0 and h2.torsion_coefficients == []


def test_negative_control_tampered_d2_violates_nilpotency():
    """Negative control: Mutating an entry in d2 breaks Stokes nilpotency d1 * d2 = 0."""
    _, d1, d2 = build_rp2_complex()
    # Copy and tamper
    tampered_d2 = [row[:] for row in d2]
    tampered_d2[0][0] += 1
    prod = _mat_mul(d1, tampered_d2)
    assert not all(all(x == 0 for x in row) for row in prod), "Tampered d2 must fail nilpotency"
