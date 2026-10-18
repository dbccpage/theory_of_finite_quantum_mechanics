"""test_topological_half_instanton_4d.py: Unit tests for 4D Half-Instantons & Chern Class Cancellation.
AuthorityEffect: None.

Tests:
1. Discrete 4-torus T^4 geometry, periodic boundaries, volume V=16, and discrete metrics.
2. Localized half-instanton centers with chirality in {+1, -1} and charges in (1/2)Z.
3. Discrete second Chern class density and integral operators in exact rational arithmetic.
4. HalfInstantonCluster4D value object properties and sector classifications.
5. Orientation flip involution tau: c_2 |-> -c_2, sign inversion, and exact zero-sum doublet identity.
6. Ensemble partition function cancellation: odd sectors vanish identically, zero-charge sector strictly positive.
7. Strict ZERO FLOATS invariant across AST, runtime types, and exception boundaries.
8. Claim hygiene: zero forbidden hype verbs in docstrings and receipt consistency with Target T5.
9. Fail-closed behavior on invalid coordinates, negative counts, and tampered weights/signs.
"""

from __future__ import annotations

import ast
from fractions import Fraction
from pathlib import Path

import pytest

from topological_half_instanton_4d import (
    DiscreteTorus4D,
    HalfInstantonCenter4D,
    HalfInstantonCluster4D,
    assert_no_floats,
    compute_discrete_topological_density,
    compute_t5_receipt,
    discrete_second_chern_integral,
    fermion_determinant_sign,
    orientation_flip,
    second_chern_number,
    verify_ensemble_cancellation,
    verify_zero_sum_doublet,
)

# ---------------------------------------------------------------------------
# Test 1: Discrete 4-Torus T^4 Carrier
# ---------------------------------------------------------------------------


def test_discrete_torus_4d_geometry() -> None:
    """Validates discrete 4-torus carrier dimensions, volume, sites, and distance."""
    # Default isotropic torus L=(2,2,2,2), volume V=16
    torus_16 = DiscreteTorus4D()
    assert torus_16.dimensions == (2, 2, 2, 2)
    assert torus_16.volume == 16
    sites = torus_16.sites()
    assert len(sites) == 16
    assert len(set(sites)) == 16

    # Verify site coordinate bounds
    for s in sites:
        assert len(s) == 4
        for mu in range(4):
            assert 0 <= s[mu] < 2
            assert type(s[mu]) is int

    # Boundary wrapping
    assert torus_16.wrap((2, 3, -1, 4)) == (0, 1, 1, 0)
    assert torus_16.wrap((0, 0, 0, 0)) == (0, 0, 0, 0)

    # Periodic squared Euclidean distance
    assert torus_16.distance_sq((0, 0, 0, 0), (0, 0, 0, 0)) == 0
    assert torus_16.distance_sq((0, 0, 0, 0), (1, 0, 0, 0)) == 1
    assert torus_16.distance_sq((0, 0, 0, 0), (1, 1, 1, 1)) == 4
    # Periodic wrap: on L=2, distance between 0 and 1 is 1; between 0 and 2 wraps to 0
    assert torus_16.distance_sq((0, 0, 0, 0), (2, 0, 0, 0)) == 0

    # Custom cubic torus L=3, volume V=81
    torus_81 = DiscreteTorus4D.cubic(3)
    assert torus_81.volume == 81
    assert len(torus_81.sites()) == 81

    # Exception checks
    with pytest.raises(ValueError):
        DiscreteTorus4D(dimensions=(2, 2, 2))  # Not 4D
    with pytest.raises(ValueError):
        DiscreteTorus4D(dimensions=(2, 2, 2, 0))  # Non-positive dimension
    with pytest.raises(TypeError):
        DiscreteTorus4D(dimensions=(2, 2, 2, 2.0))  # Float forbidden


# ---------------------------------------------------------------------------
# Test 2: Localized 4D Half-Instanton Centers
# ---------------------------------------------------------------------------


def test_half_instanton_center_properties() -> None:
    """Validates localized centers on T^4, topological charges, and chirality inversion."""
    c_plus = HalfInstantonCenter4D(coords=(0, 1, 0, 1), chirality=1)
    assert c_plus.chirality == 1
    assert c_plus.charge == Fraction(1, 2)
    assert type(c_plus.charge) is Fraction

    c_minus = HalfInstantonCenter4D(coords=(1, 0, 1, 0), chirality=-1)
    assert c_minus.chirality == -1
    assert c_minus.charge == Fraction(-1, 2)
    assert type(c_minus.charge) is Fraction

    # Inversion flip
    c_flipped = c_plus.flip()
    assert c_flipped.coords == c_plus.coords
    assert c_flipped.chirality == -1
    assert c_flipped.charge == Fraction(-1, 2)

    # Involutive flip
    assert c_flipped.flip() == c_plus

    # Validation errors
    with pytest.raises(ValueError):
        HalfInstantonCenter4D(coords=(0, 0, 0, 0), chirality=0)  # Invalid chirality
    with pytest.raises(ValueError):
        HalfInstantonCenter4D(coords=(0, 0, 0, 0), chirality=2)
    with pytest.raises(TypeError):
        HalfInstantonCenter4D(coords=(0, 0, 0, 0), chirality=1.0)  # Float forbidden


# ---------------------------------------------------------------------------
# Test 3: Discrete Topological Charge Density & Operators
# ---------------------------------------------------------------------------


def test_discrete_topological_density_and_operator() -> None:
    """Validates discrete charge density distribution and exact integral over T^4."""
    torus = DiscreteTorus4D()
    c1 = HalfInstantonCenter4D(coords=(0, 0, 0, 0), chirality=1)
    c2 = HalfInstantonCenter4D(coords=(1, 1, 0, 0), chirality=1)
    c3 = HalfInstantonCenter4D(coords=(0, 1, 1, 0), chirality=-1)

    # 1. Point density profile: N_+ = 2, N_- = 1 -> c_2 = 1/2
    density_pt = compute_discrete_topological_density([c1, c2, c3], torus, smeared=False)
    assert len(density_pt) == 16
    for site, q in density_pt.items():
        assert isinstance(q, Fraction)
    assert density_pt[(0, 0, 0, 0)] == Fraction(1, 2)
    assert density_pt[(1, 1, 0, 0)] == Fraction(1, 2)
    assert density_pt[(0, 1, 1, 0)] == Fraction(-1, 2)
    assert density_pt[(1, 1, 1, 1)] == Fraction(0, 1)

    # Integral check
    int_pt = discrete_second_chern_integral(density_pt)
    assert int_pt == Fraction(1, 2)
    assert isinstance(int_pt, Fraction)

    # 2. Smeared density profile: exact partition of unity over Q
    density_sm = compute_discrete_topological_density([c1, c2, c3], torus, smeared=True)
    int_sm = discrete_second_chern_integral(density_sm)
    assert int_sm == Fraction(1, 2)
    assert isinstance(int_sm, Fraction)

    # 3. Neutral configuration N_+ = N_- = 1 -> c_2 = 0
    density_neutral = compute_discrete_topological_density([c1, c3], torus, smeared=False)
    assert discrete_second_chern_integral(density_neutral) == Fraction(0, 1)

    # 4. Anti-self-dual excess N_+ = 0, N_- = 2 -> c_2 = -1
    c4 = HalfInstantonCenter4D(coords=(1, 0, 0, 1), chirality=-1)
    density_asd = compute_discrete_topological_density([c3, c4], torus, smeared=False)
    assert discrete_second_chern_integral(density_asd) == Fraction(-1, 1)


# ---------------------------------------------------------------------------
# Test 4: HalfInstantonCluster4D Value Object & Properties
# ---------------------------------------------------------------------------


def test_half_instanton_cluster_properties() -> None:
    """Validates cluster representation, Chern numbers, fermion signs, and sector flags."""
    # Single self-dual half-instanton
    c_single = HalfInstantonCluster4D(n_plus=1, n_minus=0, volume=16)
    assert c_single.n_plus == 1
    assert c_single.n_minus == 0
    assert c_single.volume == 16
    assert c_single.weight == Fraction(1, 1)
    assert c_single.second_chern_number == Fraction(1, 2)
    assert c_single.fermion_determinant_sign == -1
    assert c_single.total_centers == 1
    assert c_single.is_half_integer_charge is True
    assert c_single.is_integer_charge is False
    assert c_single.is_zero_charge is False

    # Standalone function interface parity
    assert second_chern_number(c_single) == Fraction(1, 2)
    assert fermion_determinant_sign(c_single) == -1

    # Zero-charge sectors
    c_zero_0 = HalfInstantonCluster4D(n_plus=0, n_minus=0)
    assert c_zero_0.second_chern_number == Fraction(0, 1)
    assert c_zero_0.fermion_determinant_sign == 1
    assert c_zero_0.is_zero_charge is True

    c_zero_2 = HalfInstantonCluster4D(n_plus=2, n_minus=2)
    assert c_zero_2.second_chern_number == Fraction(0, 1)
    assert c_zero_2.fermion_determinant_sign == 1
    assert c_zero_2.is_zero_charge is True

    # Integer charge sector (full instanton Q=1)
    c_full = HalfInstantonCluster4D(n_plus=2, n_minus=0)
    assert c_full.second_chern_number == Fraction(1, 1)
    assert c_full.fermion_determinant_sign == 1
    assert c_full.is_integer_charge is True
    assert c_full.is_zero_charge is False

    # From centers constructor
    centers = [
        HalfInstantonCenter4D(coords=(0, 0, 0, 0), chirality=1),
        HalfInstantonCenter4D(coords=(1, 0, 0, 0), chirality=1),
        HalfInstantonCenter4D(coords=(0, 1, 0, 0), chirality=-1),
    ]
    c_from_centers = HalfInstantonCluster4D.from_centers(centers, volume=16, weight=Fraction(3, 4))
    assert c_from_centers.n_plus == 2
    assert c_from_centers.n_minus == 1
    assert c_from_centers.weight == Fraction(3, 4)
    assert c_from_centers.second_chern_number == Fraction(1, 2)
    assert c_from_centers.fermion_determinant_sign == -1


# ---------------------------------------------------------------------------
# Test 5: Orientation Flip Involution & Exact Zero-Sum Doublet
# ---------------------------------------------------------------------------


def test_orientation_flip_involution_and_zero_sum() -> None:
    """Validates involution tau, charge flip, sign reversal, and (1 + (-1)) w(C) = 0 cancellation."""
    # Test across multiple half-instanton sectors
    odd_sectors = [
        (1, 0, Fraction(1, 2)),
        (0, 1, Fraction(-1, 2)),
        (2, 1, Fraction(1, 2)),
        (1, 2, Fraction(-1, 2)),
        (3, 0, Fraction(3, 2)),
        (0, 3, Fraction(-3, 2)),
        (4, 3, Fraction(1, 2)),
    ]

    for n_p, n_m, expected_c2 in odd_sectors:
        cluster = HalfInstantonCluster4D(n_plus=n_p, n_minus=n_m, weight=Fraction(5, 7))
        partner = orientation_flip(cluster)

        # 1. Centers swap
        assert partner.n_plus == n_m
        assert partner.n_minus == n_p

        # 2. Charge flips c_2 |-> -c_2
        assert second_chern_number(cluster) == expected_c2
        assert second_chern_number(partner) == -expected_c2
        assert second_chern_number(partner) == -second_chern_number(cluster)

        # 3. Fermion determinant sign inverts
        s_orig = fermion_determinant_sign(cluster)
        s_flip = fermion_determinant_sign(partner)
        assert s_flip == -s_orig
        assert s_orig in (1, -1)
        assert s_flip in (1, -1)

        # 4. Weight preserved
        assert partner.weight == cluster.weight

        # 5. Exact zero-sum doublet identity: (sigma(C) + sigma(tau(C))) * w(C) = 0
        doublet_sum = (s_orig + s_flip) * cluster.weight
        assert doublet_sum == Fraction(0, 1)

        # 6. Involutive property tau(tau(C)) == C
        double_flipped = orientation_flip(partner)
        assert double_flipped == cluster
        assert fermion_determinant_sign(double_flipped) == s_orig

        # 7. Audit helper verification
        audit = verify_zero_sum_doublet(cluster)
        assert audit["exact_zero_sum_doublet"] is True
        assert audit["duality_gap"] == "0"
        assert audit["involution_intact"] is True

    # Zero-charge sectors: orientation flip preserves sign +1 strictly
    for n in (0, 1, 2, 4):
        c_zero = HalfInstantonCluster4D(n_plus=n, n_minus=n, weight=Fraction(3, 1))
        p_zero = orientation_flip(c_zero)
        assert p_zero.n_plus == n
        assert p_zero.n_minus == n
        assert second_chern_number(p_zero) == Fraction(0, 1)
        assert fermion_determinant_sign(c_zero) == 1
        assert fermion_determinant_sign(p_zero) == 1
        audit_zero = verify_zero_sum_doublet(c_zero)
        assert audit_zero["exact_zero_sum_doublet"] is True


# ---------------------------------------------------------------------------
# Test 6: Ensemble Partition Function Cancellation
# ---------------------------------------------------------------------------


def test_ensemble_partition_function_cancellation() -> None:
    """Validates that odd half-instanton sectors cancel identically in partition sums."""
    # Ensemble with zero-charge configurations and paired half-instanton configurations
    c_zero_1 = HalfInstantonCluster4D(n_plus=0, n_minus=0, weight=Fraction(2, 1))
    c_zero_2 = HalfInstantonCluster4D(n_plus=1, n_minus=1, weight=Fraction(5, 1))
    c_zero_3 = HalfInstantonCluster4D(n_plus=2, n_minus=2, weight=Fraction(7, 3))

    # Half-instanton pairs with identical weights
    c_half_1 = HalfInstantonCluster4D(n_plus=1, n_minus=0, weight=Fraction(3, 2))
    c_half_1_tau = orientation_flip(c_half_1)

    c_half_2 = HalfInstantonCluster4D(n_plus=2, n_minus=1, weight=Fraction(4, 5))
    c_half_2_tau = orientation_flip(c_half_2)

    c_half_3 = HalfInstantonCluster4D(n_plus=3, n_minus=0, weight=Fraction(11, 4))
    c_half_3_tau = orientation_flip(c_half_3)

    ensemble = [
        c_zero_1,
        c_zero_2,
        c_zero_3,
        c_half_1,
        c_half_1_tau,
        c_half_2,
        c_half_2_tau,
        c_half_3,
        c_half_3_tau,
    ]

    report = verify_ensemble_cancellation(ensemble)
    assert report["total_clusters"] == 9
    assert report["zero_charge_count"] == 3
    assert report["odd_half_instanton_count"] == 6
    assert report["odd_sector_exact_cancellation"] is True
    assert report["zero_sector_strictly_positive"] is True
    assert report["duality_gap"] == "0"

    expected_z_zero = Fraction(2, 1) + Fraction(5, 1) + Fraction(7, 3)  # 7 + 7/3 = 28/3
    assert report["z_zero_charge_partition"] == str(expected_z_zero)
    assert report["z_odd_sector_partition"] == "0"
    assert report["z_total_partition"] == str(expected_z_zero)


# ---------------------------------------------------------------------------
# Test 7: Zero Float Enforcement & AST Static Audit
# ---------------------------------------------------------------------------


def test_zero_floats_enforcement_and_ast_audit() -> None:
    """Audits the AST and runtime behavior of topological_half_instanton_4d to confirm zero floats."""
    src_path = Path(__file__).resolve().parent.parent / "topological_half_instanton_4d.py"
    assert src_path.exists(), f"Source file missing: {src_path}"

    tree = ast.parse(src_path.read_text(encoding="utf-8"))

    # Assert no float constants in AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            assert type(node.value) is not float, f"Float literal found in source code: {node.value}"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id != "float", "Call to float() built-in found in source code"

    # Runtime assert_no_floats validator
    assert_no_floats(1, Fraction(1, 2), "string", (2, 3), {"a": Fraction(0, 1)})
    with pytest.raises(TypeError):
        assert_no_floats(0.5)
    with pytest.raises(TypeError):
        assert_no_floats([1, 2, 3.14])
    with pytest.raises(TypeError):
        assert_no_floats({"k": 1.25})

    # Runtime constructor rejections
    with pytest.raises(TypeError):
        HalfInstantonCluster4D(n_plus=1.0, n_minus=0)  # Float n_plus
    with pytest.raises(TypeError):
        HalfInstantonCluster4D(n_plus=1, n_minus=0.0)  # Float n_minus
    with pytest.raises(TypeError):
        HalfInstantonCluster4D(n_plus=1, n_minus=0, weight=0.5)  # Float weight


# ---------------------------------------------------------------------------
# Test 8: Claim Hygiene & Target T5 Receipt Parity
# ---------------------------------------------------------------------------


def test_claim_hygiene_and_receipt_parity() -> None:
    """Verifies absence of forbidden hype verbs and confirms receipt structure."""
    src_path = Path(__file__).resolve().parent.parent / "topological_half_instanton_4d.py"
    content = src_path.read_text(encoding="utf-8")

    forbidden_words = [
        "proves",
        "guarantees",
        "mathematically verifies",
        "fundamentally",
        "true intelligence",
        "impossible",
        "universal",
        "flawless",
        "perfectly",
        "clearly",
        "obviously",
        "merely",
        "weaponized",
    ]

    for word in forbidden_words:
        assert word not in content.lower(), f"Forbidden hype word '{word}' found in source file"

    # Receipt parity check
    receipt = compute_t5_receipt()
    assert receipt["dimension"] == 4
    assert receipt["spacetime_carrier"] == "4_TORUS_T4"
    assert receipt["volume"] == 16
    assert receipt["half_instanton_topological_charge"] == "1/2"
    assert receipt["cluster_fermion_sign"] == -1
    assert receipt["orientation_inversion_charge"] == "-1/2"
    assert receipt["inversion_fermion_sign"] == 1
    assert receipt["exact_zero_sum_doublet"] is True
    assert receipt["partition_sign_obstruction_resolved"] is True
    assert receipt["duality_gap"] == "0"


# ---------------------------------------------------------------------------
# Test 9: Fail-Closed Boundary Testing
# ---------------------------------------------------------------------------


def test_fail_closed_boundaries() -> None:
    """Asserts fail-closed typed refusals on negative counts, zero volume, and tampered values."""
    with pytest.raises(ValueError):
        HalfInstantonCluster4D(n_plus=-1, n_minus=0)
    with pytest.raises(ValueError):
        HalfInstantonCluster4D(n_plus=0, n_minus=-2)
    with pytest.raises(ValueError):
        HalfInstantonCluster4D(n_plus=0, n_minus=0, volume=0)
    with pytest.raises(ValueError):
        HalfInstantonCluster4D(n_plus=0, n_minus=0, weight=Fraction(0, 1))  # Non-positive weight

    # Tampered weight asymmetry breaks zero-sum doublet
    c = HalfInstantonCluster4D(n_plus=1, n_minus=0, weight=Fraction(1, 1))
    partner_tampered = HalfInstantonCluster4D(
        n_plus=0,
        n_minus=1,
        weight=Fraction(2, 1),  # Tampered weight!
        sign_factor=-1,
    )
    s_c = fermion_determinant_sign(c)
    s_p = fermion_determinant_sign(partner_tampered)
    broken_sum = c.weight * Fraction(s_c, 1) + partner_tampered.weight * Fraction(s_p, 1)
    assert broken_sum != Fraction(0, 1), "Tampered weight should fail zero-sum cancellation"
    assert broken_sum == Fraction(1, 1)  # -1 * 1 + 1 * 2 = 1 != 0
