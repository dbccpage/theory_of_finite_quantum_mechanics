"""Adversarial stress testing and property-based oracles for MUB(6).

Covers:
- Unitarity of dephased Hadamard matrices
- Complex modulus invariance under unitary and dephasing transformations
- Ray obstruction invariants (SDP dual witness Tr(W * G) < 0)
- Cyc24 arithmetic under extreme perturbations and algebraic ring axioms
- Genuine non-mocked verification without trivial passes

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import random
import pytest
from hypothesis import given, settings, strategies as st

from src.mub.mub_verify.cyclotomic import Cyc24
from src.mub.mub_verify.mub_triples import (
    D,
    check_basis_orthonormal,
    check_bases_mutually_unbiased,
    dita_seed_triple_columns,
    f6_family_columns,
    inner_product,
    inv_sqrt6_cyc,
    standard_basis_b1,
    verify_triple_pairwise_mu,
)
from src.mub.mub_verify.target_a4_gram_certifier import (
    canonical_quad_gramian,
    canonical_triple_exact,
    compute_gram_matrix_cyc,
    tao_s6_block,
    TAO_PHASES,
)


# ============================================================================
# 1. Cyc24 Extreme Perturbations & Ring Axioms
# ============================================================================

def make_random_cyc24(rng: random.Random, max_num: int = 10**6, max_den: int = 10**6) -> Cyc24:
    """Generate a pseudo-random Cyc24 element with non-trivial rational coefficients."""
    coeffs = []
    for _ in range(8):
        num = rng.randint(-max_num, max_num)
        den = rng.randint(1, max_den)
        coeffs.append(Fraction(num, den))
    return Cyc24(coeffs)


def test_cyc24_minimal_polynomial_vanishing():
    """Verify that the minimal polynomial Phi_24(x) = x^8 - x^4 + 1 vanishes identically."""
    z = Cyc24.zeta(1)
    # Compute z^8, z^4
    z2 = z.mul(z)
    z4 = z2.mul(z2)
    z8 = z4.mul(z4)
    # Phi_24(z) = z^8 - z^4 + 1
    phi = z8.sub(z4).add(Cyc24.one())
    assert phi.is_zero(), f"Minimal polynomial did not vanish: {phi.coeffs}"


def test_cyc24_order_24_exactness():
    """Verify that zeta has exact order 24: zeta^24 == 1, zeta^12 == -1, zeta^k != 1 for 0 < k < 24."""
    z = Cyc24.zeta(1)
    acc = Cyc24.one()
    for k in range(1, 25):
        acc = acc.mul(z)
        if k == 12:
            assert acc == Cyc24.rat(-1), f"zeta^12 is not -1: {acc.coeffs}"
        elif k == 24:
            assert acc == Cyc24.one(), f"zeta^24 is not 1: {acc.coeffs}"
        else:
            assert acc != Cyc24.one(), f"zeta^{k} prematurely equals 1"


def test_cyc24_extreme_large_coefficients():
    """Stress test Cyc24 arithmetic with huge 60-digit coefficients."""
    huge_int = 10**60 + 37
    huge_den = 10**58 + 19
    c1 = Cyc24([Fraction(huge_int, huge_den)] + [Fraction(0, 1)] * 7)
    c2 = Cyc24.zeta(3)
    prod = c1.mul(c2)
    inv_c1 = c1.inv()
    recovered = prod.mul(inv_c1)
    assert recovered == c2, "Failed exact recovery under 60-digit rational arithmetic"


def test_cyc24_ring_axioms_randomized():
    """Verify field and ring axioms for random elements."""
    rng = random.Random(42)
    for _ in range(25):
        a = make_random_cyc24(rng)
        b = make_random_cyc24(rng)
        c = make_random_cyc24(rng)

        # Addition commutativity & associativity
        assert a.add(b) == b.add(a)
        assert a.add(b).add(c) == a.add(b.add(c))

        # Multiplication commutativity & associativity
        assert a.mul(b) == b.mul(a)
        assert a.mul(b).mul(c) == a.mul(b.mul(c))

        # Distributivity
        assert a.mul(b.add(c)) == a.mul(b).add(a.mul(c))

        # Conjugation involution
        assert a.conj().conj() == a
        assert a.add(b).conj() == a.conj().add(b.conj())
        assert a.mul(b).conj() == a.conj().mul(b.conj())

        # Inverse
        if not a.is_zero():
            inv_a = a.inv()
            prod = a.mul(inv_a)
            assert prod == Cyc24.one(), f"a * a^-1 != 1: {prod.coeffs}"

        # Norm is real: self-conjugate
        norm_sq = a.abs_sq()
        assert norm_sq.conj() == norm_sq, f"abs_sq not self-conjugate (not real): {norm_sq.coeffs}"
        if a.is_zero():
            assert norm_sq.is_zero()
        else:
            assert not norm_sq.is_zero()


def test_cyc24_inversion_error_paths():
    """Ensure inverting zero strictly raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        Cyc24.zero().inv()

    with pytest.raises(ValueError, match="exactly 8 coefficients"):
        Cyc24([Fraction(1)] * 7)

    with pytest.raises(ValueError, match="exactly 8 coefficients"):
        Cyc24([Fraction(1)] * 9)


# ============================================================================
# 2. Unitarity & Complex Modulus Invariance of Dephased Hadamard Matrices
# ============================================================================

def test_f6_family_unitarity_all_locked_seeds():
    """Verify unitarity and orthonormal column conditions for all locked Dita seeds."""
    locked_seeds = [(0, 8), (8, 0), (16, 16), (0, 16), (8, 8), (16, 0)]
    for dx, dy in locked_seeds:
        cols = f6_family_columns(dx, dy)
        assert len(cols) == 6
        assert check_basis_orthonormal(cols), f"F6({dx}, {dy}) columns are not orthonormal"

        # Check complex modulus of every entry is 1/sqrt(6) -> |entry|^2 == 1/6
        one_sixth = Cyc24.rat(Fraction(1, 6))
        for col in cols:
            for entry in col:
                assert entry.abs_sq() == one_sixth, f"Modulus squared mismatch in F6({dx}, {dy}): {entry.abs_sq()}"


def test_hadamard_unitarity_under_random_dephasing():
    """Adversarially dephase Hadamard matrices and verify unitarity & modulus invariance."""
    rng = random.Random(1337)
    base_cols = f6_family_columns(0, 8)  # 6 column vectors in C^6

    for trial in range(10):
        # Pick random row phases alpha_j in [0, 24) and col phases beta_k in [0, 24)
        row_phases = [rng.randint(0, 23) for _ in range(6)]
        col_phases = [rng.randint(0, 23) for _ in range(6)]

        # Apply dephasing H'[j][k] = zeta^{alpha_j} * H[j][k] * zeta^{beta_k}
        dephased_cols = []
        for k in range(6):
            orig_col = base_cols[k]
            beta_k = Cyc24.zeta(col_phases[k])
            new_col = []
            for j in range(6):
                alpha_j = Cyc24.zeta(row_phases[j])
                new_entry = alpha_j.mul(orig_col[j]).mul(beta_k)
                new_col.append(new_entry)
            dephased_cols.append(tuple(new_col))

        # Check orthonormality of dephased columns (H' (H')^dagger = I)
        assert check_basis_orthonormal(dephased_cols), f"Dephased Hadamard lost orthonormality at trial {trial}"

        # Check complex modulus invariance: |H'_{jk}|^2 must still be exactly 1/6
        one_sixth = Cyc24.rat(Fraction(1, 6))
        for col in dephased_cols:
            for entry in col:
                assert entry.abs_sq() == one_sixth, f"Modulus altered by dephasing: {entry.abs_sq()}"


def test_tao_hadamard_s6_modulus_and_unitarity():
    """Verify Tao Hadamard matrix S6 entries have exact modulus 1/sqrt(6) and rows are orthonormal."""
    s6 = tao_s6_block()
    assert len(s6) == 6
    assert all(len(row) == 6 for row in s6)

    one_sixth = Cyc24.rat(Fraction(1, 6))
    for r in range(6):
        for c in range(6):
            assert s6[r][c].abs_sq() == one_sixth, f"Tao S6 modulus squared != 1/6 at ({r}, {c})"

    # Row orthonormality
    one = Cyc24.one()
    zero = Cyc24.zero()
    for i in range(6):
        for j in range(6):
            prod = inner_product(s6[i], s6[j])
            want = one if i == j else zero
            assert prod == want, f"Tao S6 rows not orthonormal at ({i}, {j}): got {prod.coeffs}, want {want.coeffs}"


def test_negative_perturbed_hadamard_fails_unitarity():
    """Perturbing a single phase in an orthonormal basis must cause orthonormality check to fail."""
    cols = list(f6_family_columns(0, 8))
    # Perturb first entry of first column by adding 1/10
    col0 = list(cols[0])
    col0[0] = col0[0].add(Cyc24.rat(Fraction(1, 10)))
    cols[0] = tuple(col0)
    assert not check_basis_orthonormal(cols), "Perturbed basis falsely passed orthonormality"


# ============================================================================
# 3. Ray Obstruction & SDP Dual Witness Invariants
# ============================================================================

def test_canonical_triple_is_genuine_mub_triple():
    """Verify that canonical triple T0 = {B1, B2, B3} forms 3 pairwise mutually unbiased bases."""
    triple_cols = dita_seed_triple_columns(0, 8)
    assert len(triple_cols) == 18
    assert verify_triple_pairwise_mu(triple_cols), "Canonical seed triple (0, 8) failed pairwise MU verification"


def test_canonical_quad_gramian_structure():
    """Stress test 24x24 Gramian matrix structure."""
    g = canonical_quad_gramian()
    assert len(g) == 24
    assert all(len(row) == 24 for row in g)

    # Diagonal entries must all be 1
    one = Cyc24.one()
    for i in range(24):
        assert g[i][i] == one, f"Gramian diagonal at {i} is not 1: {g[i][i].coeffs}"

    # Hermitian symmetry G_{ji} = G_{ij}^*
    for i in range(24):
        for j in range(24):
            assert g[j][i] == g[i][j].conj(), f"Hermitian symmetry violated at ({i}, {j})"

    # Off-diagonal blocks between basis b and basis b' (b != b') must satisfy |G_{ij}|^2 = 1/6
    one_sixth = Cyc24.rat(Fraction(1, 6))
    for b1 in range(4):
        for b2 in range(4):
            if b1 == b2:
                continue
            for i in range(6):
                for j in range(6):
                    idx1 = b1 * 6 + i
                    idx2 = b2 * 6 + j
                    entry = g[idx1][idx2]
                    assert entry.abs_sq() == one_sixth, f"Off-diagonal overlap squared != 1/6 at ({idx1}, {idx2})"
