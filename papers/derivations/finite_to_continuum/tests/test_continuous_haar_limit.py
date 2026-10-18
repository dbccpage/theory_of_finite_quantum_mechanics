# -*- coding: utf-8 -*-
"""
Tests for Inductive Direct Limit of Finite Character Sums to Continuous Haar Measure.

AuthorityEffect: None.

Verifies:
  1. Character pair direct limit sequences stabilize to exact Kronecker delta.
  2. Trigonometric polynomials recover exact Haar integral c_0 on finite dyadic grids.
  3. Lipschitz continuous functions admit certified Cauchy rational interval contractions.
  4. Zero-Float Law is strictly enforced across all types and receipts.
  5. SHA-256 evidence digest integrity is verified.
"""

from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest

from omega_engine_projects.finite_to_continuum.code.continuous_haar_limit import (
    HaarLimitCharacterPair,
    LipschitzContinuumEnclosure,
    TrigPolynomial,
    generate_continuous_haar_limit_receipt,
)

# ==============================================================================
# 1. Character Pair Direct Limit Stabilization
# ==============================================================================

def test_haar_limit_character_pair_trivial():
    """Trivial character pair (k == j) stabilizes at level 0 to exact 1."""
    pair = HaarLimitCharacterPair(3, 3)
    assert pair.k == 3
    assert pair.j == 3
    assert pair.delta_freq == 0
    assert pair.stabilization_level == 0
    assert pair.exact_haar_integral == Fraction(1)

    seq = pair.evaluate_limit_sequence(max_level=4)
    assert seq == [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(1)]
    assert pair.is_stabilized_at(0)
    assert pair.is_stabilized_at(4)


def test_haar_limit_character_pair_orthogonal():
    """Non-trivial character pair (k != j) stabilizes to exact 0 once 2^n > |k - j|."""
    # Delta = 3 - 0 = 3; 3.bit_length() = 2; 2^2 = 4 > 3
    pair = HaarLimitCharacterPair(3, 0)
    assert pair.delta_freq == 3
    assert pair.stabilization_level == 2
    assert pair.exact_haar_integral == Fraction(0)

    seq = pair.evaluate_limit_sequence(max_level=4)
    # level 0: ord=1, 3 % 1 == 0 -> S_0 = 1
    # level 1: ord=2, 3 % 2 == 1 -> S_1 = 0
    # level 2: ord=4, 3 % 4 == 3 -> S_2 = 0
    # level 3: ord=8, 3 % 8 == 3 -> S_3 = 0
    # level 4: ord=16, 3 % 16 == 3 -> S_4 = 0
    assert seq == [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    assert not pair.is_stabilized_at(0)
    assert pair.is_stabilized_at(1)
    assert pair.is_stabilized_at(2)
    assert pair.is_stabilized_at(4)


def test_haar_limit_character_pair_negative():
    """Negative delta frequency: k = -2, j = 2 -> delta = -4."""
    pair = HaarLimitCharacterPair(-2, 2)
    assert pair.delta_freq == -4
    # |-4|.bit_length() = 3; 2^3 = 8 > 4
    assert pair.stabilization_level == 3
    assert pair.exact_haar_integral == Fraction(0)

    seq = pair.evaluate_limit_sequence(max_level=4)
    # level 0: ord=1, -4 % 1 == 0 -> 1
    # level 1: ord=2, -4 % 2 == 0 -> 1
    # level 2: ord=4, -4 % 4 == 0 -> 1
    # level 3: ord=8, -4 % 8 == 4 -> 0
    # level 4: ord=16, -4 % 16 == 12 -> 0
    assert seq == [Fraction(1), Fraction(1), Fraction(1), Fraction(0), Fraction(0)]
    assert not pair.is_stabilized_at(2)
    assert pair.is_stabilized_at(3)
    assert pair.is_stabilized_at(4)


# ==============================================================================
# 2. Trigonometric Polynomials
# ==============================================================================

def test_trig_polynomial_constant():
    """Constant polynomial P(x) = c_0 has stabilization level 0."""
    poly = TrigPolynomial({0: Fraction(7, 3)})
    assert poly.max_frequency == 0
    assert poly.stabilization_level == 0
    assert poly.exact_haar_integral == Fraction(7, 3)

    res = poly.verify_haar_recovery(max_level=3)
    assert res["recovers_exact_haar"] is True
    assert res["sequence"] == ["7/3", "7/3", "7/3", "7/3"]


def test_trig_polynomial_multi_frequency():
    """Polynomial P(x) = 4 + 3 e^{2 pi i x} - 2 e^{2 pi i * 3 x} stabilizes at level 2."""
    poly = TrigPolynomial({
        0: 4,
        1: Fraction(3),
        3: Fraction(-2),
    })
    assert poly.max_frequency == 3
    assert poly.stabilization_level == 2  # 3.bit_length() = 2, 2^2 = 4 > 3
    assert poly.exact_haar_integral == Fraction(4)

    # R_0: 4 + 3 - 2 = 5
    # R_1 (ord=2): 4 + (-2) = 2 (freq 1 cancels since 1 % 2 != 0; freq 3 cancels since 3 % 2 != 0?
    # Wait: 3 % 2 == 1, not 0! So only freq 0 has 0 % 2 == 0. Thus R_1 = 4.
    # Level 2 (ord=4): only freq 0 has 0 % 4 == 0. Thus R_2 = 4.
    res = poly.verify_haar_recovery(max_level=4)
    assert res["recovers_exact_haar"] is True
    assert poly.discrete_riemann_sum(2) == Fraction(4)
    assert poly.discrete_riemann_sum(3) == Fraction(4)
    assert poly.discrete_riemann_sum(4) == Fraction(4)


# ==============================================================================
# 3. Lipschitz Continuous Cauchy Contraction
# ==============================================================================

def test_lipschitz_continuum_enclosure():
    """Lipschitz observable produces certified nested Cauchy contraction in CODA-Q."""
    # L = 2, riemann sums converging to 1/3
    sums = [
        Fraction(1, 3) + Fraction(1, 1 << n)
        for n in range(5)
    ]
    enc = LipschitzContinuumEnclosure(lipschitz_constant=2, riemann_sums=sums)
    assert enc.levels == 5
    assert enc.lipschitz_constant == Fraction(2)

    continuum_enc = enc.to_continuum_enclosure("test_lipschitz")
    assert continuum_enc.steps == 5
    assert continuum_enc.is_cauchy_contractive() is True
    # Width at level n should be <= 2L / 2^n = 4 / 2^n
    for n, iv in enumerate(continuum_enc.intervals):
        assert iv.width <= Fraction(4, 1 << n)


# ==============================================================================
# 4. Zero-Float Law Strict Rejection
# ==============================================================================

def test_zero_float_law_rejections():
    """Floats are strictly rejected across all module APIs."""
    with pytest.raises(TypeError, match="float"):
        HaarLimitCharacterPair(1.0, 0)

    with pytest.raises(TypeError, match="float"):
        HaarLimitCharacterPair(0, 2.5)

    with pytest.raises(TypeError, match="float"):
        TrigPolynomial({0: 1.5})

    with pytest.raises(TypeError, match="float"):
        LipschitzContinuumEnclosure(lipschitz_constant=1.0, riemann_sums=[Fraction(1)])

    with pytest.raises(TypeError, match="float"):
        LipschitzContinuumEnclosure(lipschitz_constant=1, riemann_sums=[0.5])


# ==============================================================================
# 5. Stamped Receipt Verification & SHA-256 Digest Integrity
# ==============================================================================

def test_continuous_haar_limit_receipt_generation_and_integrity():
    """Verify generated receipt matches schema, Zero-Float Law, and SHA-256 digest."""
    receipt = generate_continuous_haar_limit_receipt()
    assert receipt["schema"] == "omega.coda.continuous_haar_limit.v1"
    assert receipt["authority_effect"] == "None"
    assert receipt["zero_float_law_verified"] is True
    assert "evidence_sha256" in receipt

    # Verify SHA-256 digest reproducibility
    payload = dict(receipt)
    digest = payload.pop("evidence_sha256")
    raw_json = json.dumps(payload, sort_keys=True, indent=2)
    expected_digest = sha256(raw_json.encode("utf-8")).hexdigest()
    assert digest == expected_digest

    # Verify matching file on disk
    receipt_file = Path("omega_engine_projects/finite_to_continuum/results/continuous_haar_limit_receipt.json")
    assert receipt_file.is_file()
    disk_data = json.loads(receipt_file.read_text(encoding="utf-8"))
    assert disk_data["evidence_sha256"] == digest
@pytest.mark.parametrize("max_level", [True, False, 1.0, -1])
def test_polynomial_recovery_requires_a_nonnegative_exact_level(max_level):
    with pytest.raises((TypeError, ValueError)):
        TrigPolynomial({4: Fraction(1)}).verify_haar_recovery(max_level)


def test_polynomial_recovery_does_not_accept_an_empty_stabilized_tail():
    report = TrigPolynomial({4: Fraction(1)}).verify_haar_recovery(1)
    assert report["recovers_exact_haar"] is False
    assert report["stabilized_levels_tested"] == 0
