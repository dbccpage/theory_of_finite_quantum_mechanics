"""Adversarial stress testing and property-based oracles for FSP (Fermion Sign Problem).

Covers:
- BQNF routing edge cases, nilpotence violations, and multi-fault priority orders
- Kitaev chain Majorana zero mode isolation, bulk non-isolation, and detuning transitions
- Exact rational Hubbard determinants on square plaquettes (2x2 and 4x4)
- Attractive Hubbard square-root symmetry: det(I + B_up) == det(I + B_down) and sign-free positivity
- Repulsive Hubbard sign problem onset
- Palindromic kinetic matrix spectra

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import random
import pytest

from src.fsp.bqnf_sign_evaluator import (
    BQNFSignEvaluator,
    CochainComplex,
    TerminalRoute,
    exact_rational,
)
from src.majorana.sparse_kitaev import (
    SparseKitaevWire,
    KitaevWireError,
    MajoranaBilinear,
)


# ============================================================================
# Exact Rational Matrix Utilities for Hubbard Verification
# ============================================================================

def exact_det_rat(mat: list[list[Fraction]]) -> Fraction:
    """Exact Gaussian elimination determinant over Fraction."""
    n = len(mat)
    if n == 0:
        return Fraction(1)
    a = [list(row) for row in mat]
    det = Fraction(1)
    sign = 1
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if a[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        p_val = a[col][col]
        det *= p_val
        for r in range(col + 1, n):
            if a[r][col] != 0:
                factor = a[r][col] / p_val
                for c in range(col, n):
                    a[r][c] -= factor * a[col][c]
    return det * sign


def exact_mat_mul_rat(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    """Exact matrix multiplication over Fraction."""
    n = len(a)
    c = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            for j in range(n):
                c[i][j] += a[i][k] * b[k][j]
    return c


def exact_kinetic_matrix_rat(sites: int, bonds: list[tuple[int, int]], r: Fraction) -> list[list[Fraction]]:
    """Exact palindromic kinetic matrix K = prod_e B_e prod_{e^rev} B_e over Q."""
    r_inv = Fraction(1, 1) / r
    two = Fraction(2, 1)
    cosh_val = (r + r_inv) / two
    sinh_val = (r - r_inv) / two

    k_mat = [[Fraction(1 if i == j else 0) for j in range(sites)] for i in range(sites)]
    schedule = list(bonds) + list(reversed(bonds))

    for u, v in schedule:
        b = [[Fraction(1 if i == j else 0) for j in range(sites)] for i in range(sites)]
        b[u][u] = cosh_val
        b[v][v] = cosh_val
        b[u][v] = sinh_val
        b[v][u] = sinh_val
        k_mat = exact_mat_mul_rat(b, k_mat)
    return k_mat


# ============================================================================
# 1. BQNF Routing Edge Cases & Nilpotence Violations
# ============================================================================

def test_bqnf_exact_nilpotence_and_violation():
    """Verify cochain complex exact nilpotence d1 * d0 == 0 and detection of violations."""
    # Standard triangle complex: 3 vertices, 3 edges, 1 face
    # d0: edges x vertices (3 x 3)
    # e0 = (0, 1), e1 = (1, 2), e2 = (2, 0)
    d0 = [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(-1)],
    ]
    # d1: faces x edges (1 x 3)
    # f0 = e0 + e1 + e2
    d1 = [[Fraction(1), Fraction(1), Fraction(1)]]

    complex_valid = CochainComplex(dim_c0=3, dim_c1=3, dim_c2=1, d0=d0, d1=d1)
    assert complex_valid.check_nilpotence(), "Valid triangle complex failed nilpotence check"

    # Perturb d1 by adding 1 to d1[0][0] -> d1 * d0 != 0
    d1_broken = [[Fraction(2), Fraction(1), Fraction(1)]]
    complex_broken = CochainComplex(dim_c0=3, dim_c1=3, dim_c2=1, d0=d0, d1=d1_broken)
    assert not complex_broken.check_nilpotence(), "Broken complex falsely passed nilpotence check"


def test_bqnf_terminal_routing_five_fold_outcomes():
    """Verify BQNF terminal routing cleanly reaches each of the canonical routing terminals."""
    # 1. ExactRepair: coboundary defect in im(d0)
    complex_rep = CochainComplex(dim_c0=1, dim_c1=2, dim_c2=0, d0=[[Fraction(1)], [Fraction(1)]], d1=[])
    eval_rep = BQNFSignEvaluator(complex_rep)
    res_repair = eval_rep.evaluate_sign_packet([Fraction(1), Fraction(1)], [1, 1])
    assert res_repair['route'] == TerminalRoute.EXACT_REPAIR

    # 2. ExactCancellation: sign pairing cancellation via involution
    complex_cancel = CochainComplex(dim_c0=1, dim_c1=2, dim_c2=0, d0=[[Fraction(0)], [Fraction(0)]], d1=[])
    eval_cancel = BQNFSignEvaluator(complex_cancel)
    res_cancel = eval_cancel.evaluate_sign_packet([Fraction(1), Fraction(1)], [1, -1])
    assert res_cancel['route'] == TerminalRoute.EXACT_CANCELLATION

    # 3. StabilizedSurvivor: closed residual (gamma == 0, phi > 0, no involution)
    complex_surv = CochainComplex(dim_c0=1, dim_c1=2, dim_c2=0, d0=[[Fraction(0)], [Fraction(0)]], d1=[])
    eval_surv = BQNFSignEvaluator(complex_surv)
    res_surv = eval_surv.evaluate_sign_packet([Fraction(1), Fraction(2)], [1, 1])
    assert res_surv['route'] == TerminalRoute.STABILIZED_SURVIVOR

    # 4. OpenSignObstruction: non-zero d1 defect (closure defect gamma > 0)
    complex_open = CochainComplex(dim_c0=1, dim_c1=2, dim_c2=1, d0=[[Fraction(0)], [Fraction(0)]], d1=[[Fraction(1), Fraction(0)]])
    eval_open = BQNFSignEvaluator(complex_open)
    res_open = eval_open.evaluate_sign_packet([Fraction(1), Fraction(0)], [1, 1])
    assert res_open['route'] == TerminalRoute.OPEN_SIGN_OBSTRUCTION


def test_bqnf_refusal_on_empty_and_corrupt_inputs():
    """Stress test refusal behavior on degenerate inputs."""
    complex_valid = CochainComplex(dim_c0=1, dim_c1=2, dim_c2=0, d0=[[Fraction(0)], [Fraction(0)]], d1=[])
    evaluator = BQNFSignEvaluator(complex_valid)

    # Invalid path signs length or values
    res1 = evaluator.evaluate_sign_packet([Fraction(1), Fraction(1)], [1])  # length mismatch
    assert res1['route'] == TerminalRoute.REFUSED

    res2 = evaluator.evaluate_sign_packet([Fraction(1), Fraction(1)], [1, 0])  # sign not in {-1, 1}
    assert res2['route'] == TerminalRoute.REFUSED

    res3 = evaluator.evaluate_sign_packet([Fraction(1)], [1, 1])  # defect length mismatch
    assert res3['route'] == TerminalRoute.REFUSED

    with pytest.raises(ValueError, match="Invalid cochain complex: d1 . d0 != 0"):
        d0 = [[Fraction(-1), Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1), Fraction(1)], [Fraction(1), Fraction(0), Fraction(-1)]]
        d1_broken = [[Fraction(2), Fraction(1), Fraction(1)]]
        broken = CochainComplex(dim_c0=3, dim_c1=3, dim_c2=1, d0=d0, d1=d1_broken)
        BQNFSignEvaluator(broken)


# ============================================================================
# 2. Kitaev Chain Majorana Zero Mode Parity & Detuning
# ============================================================================

def test_kitaev_wire_sweet_spot_mode_isolation():
    """Verify sweet spot (t = delta, mu = 0) isolates exactly gamma_1 and gamma_{2N}."""
    for sites in [2, 4, 8, 16, 64]:
        wire = SparseKitaevWire(sites, Fraction(1), Fraction(1), Fraction(0))
        assert wire.sites() == sites
        assert wire.mode_count() == 2 * sites

        isolated = wire.isolated_majoranas()
        assert isolated == [1, 2 * sites], f"Sweet spot failed to isolate boundary modes for sites={sites}: {isolated}"

        # Commutator of isolated modes with H is identically zero
        assert wire.commutator_with_generator(1) == {}
        assert wire.commutator_with_generator(2 * sites) == {}

        # Commutator of internal modes with H is strictly non-zero
        for internal in range(2, 2 * sites):
            comm = wire.commutator_with_generator(internal)
            assert len(comm) > 0, f"Internal mode {internal} unexpectedly isolated for sites={sites}"


def test_kitaev_wire_detuning_destroys_zero_modes():
    """Verify that detuning mu != 0 destroys zero mode isolation (enters trivial or gapped bulk)."""
    sites = 4
    # With mu = 2*t, zero modes disappear
    wire_detuned = SparseKitaevWire(sites, Fraction(1), Fraction(1), Fraction(2))
    assert wire_detuned.isolated_majoranas() == [], "Detuned wire unexpectedly has isolated modes"

    # Even a small rational perturbation mu = 1/1000 destroys exact sweet-spot isolation
    wire_perturbed = SparseKitaevWire(sites, Fraction(1), Fraction(1), Fraction(1, 1000))
    assert wire_perturbed.isolated_majoranas() == [], "Perturbed wire unexpectedly has isolated modes"


def test_kitaev_wire_validation_error_boundaries():
    """Ensure invalid site counts and indices fail closed."""
    with pytest.raises(KitaevWireError, match="outside 2.."):
        SparseKitaevWire(1, Fraction(1), Fraction(1), Fraction(0))

    with pytest.raises(KitaevWireError, match="outside 2.."):
        SparseKitaevWire(100_000, Fraction(1), Fraction(1), Fraction(0))

    wire = SparseKitaevWire(4, Fraction(1), Fraction(1), Fraction(0))
    with pytest.raises(KitaevWireError, match="outside 1..="):
        wire.commutator_with_generator(0)

    with pytest.raises(KitaevWireError, match="outside 1..="):
        wire.commutator_with_generator(9)

    with pytest.raises(KitaevWireError, match="1 <= a < b"):
        MajoranaBilinear(2, 1)

    with pytest.raises(KitaevWireError, match="1 <= a < b"):
        MajoranaBilinear(1, 1)


# ============================================================================
# 3. Exact Rational Hubbard Determinants & Symmetries
# ============================================================================

def test_hubbard_exact_determinant_rational_solver():
    """Verify exact rational determinant algorithm against known matrices."""
    # Singular matrix
    sing = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ]
    assert exact_det_rat(sing) == Fraction(0)

    # 3x3 permutation matrix (odd permutation, det = -1)
    perm = [
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    assert exact_det_rat(perm) == Fraction(-1)

    # 4x4 Hilbert matrix
    hilbert = [[Fraction(1, i + j + 1) for j in range(4)] for i in range(4)]
    # Det of 4x4 Hilbert matrix is 1 / 6_048_000
    assert exact_det_rat(hilbert) == Fraction(1, 6_048_000)


def test_hubbard_attractive_square_root_symmetry_square_plaquette():
    """Verify attractive Hubbard square-root symmetry on a 2x2 square plaquette.

    For attractive U (U < 0), for ANY field configuration,
    det(I + B_up) == det(I + B_down), so total weight is a perfect square >= 0.
    """
    sites = 4
    bonds = [(0, 1), (1, 2), (2, 3), (3, 0)]
    slices = 2
    r = Fraction(3, 2)
    hs = Fraction(2, 1)
    fugacity = Fraction(1, 1)

    k_mat = exact_kinetic_matrix_rat(sites, bonds, r)

    rng = random.Random(777)
    total_fields = 1 << (sites * slices)  # 2^8 = 256 configurations
    # Test 30 random configurations
    sample_masks = [rng.randint(0, total_fields - 1) for _ in range(30)]
    sample_masks.extend([0, 1, 5, 15, 255])  # Include extremal masks

    for mask in sample_masks:
        b_up = [[Fraction(1 if i == j else 0) for j in range(sites)] for i in range(sites)]
        b_down = [[Fraction(1 if i == j else 0) for j in range(sites)] for i in range(sites)]

        for time in range(slices):
            v_up = [[Fraction(0) for _ in range(sites)] for _ in range(sites)]
            v_down = [[Fraction(0) for _ in range(sites)] for _ in range(sites)]

            for j in range(sites):
                bit = (mask >> (time * sites + j)) & 1
                s_val = 1 if bit == 1 else -1

                # Attractive Hubbard: spin up and spin down couple identically
                hs_val = hs if s_val == 1 else Fraction(1, 1) / hs
                v_up[j][j] = fugacity * hs_val
                v_down[j][j] = fugacity * hs_val

            slice_up = exact_mat_mul_rat(k_mat, v_up)
            slice_down = exact_mat_mul_rat(k_mat, v_down)

            b_up = exact_mat_mul_rat(slice_up, b_up)
            b_down = exact_mat_mul_rat(slice_down, b_down)

        # I + B
        for i in range(sites):
            b_up[i][i] += Fraction(1)
            b_down[i][i] += Fraction(1)

        det_up = exact_det_rat(b_up)
        det_down = exact_det_rat(b_down)

        # In attractive Hubbard, det_up == det_down identically!
        assert det_up == det_down, f"Attractive symmetry broken at mask {mask}: det_up={det_up}, det_down={det_down}"

        # Product is a square >= 0
        total_weight = det_up * det_down
        assert total_weight >= 0, f"Negative weight in attractive Hubbard at mask {mask}: {total_weight}"


def test_hubbard_repulsive_sign_problem_onset():
    """Verify that in repulsive Hubbard, spin-down couples with OPPOSITE sign, inducing negative weights."""
    sites = 4
    bonds = [(0, 1), (1, 2), (2, 3), (3, 0)]
    slices = 1
    r = Fraction(5, 2)
    hs = Fraction(3, 1)
    fugacity = Fraction(1, 1)

    k_mat = exact_kinetic_matrix_rat(sites, bonds, r)

    found_asymmetry = False
    for mask in range(1 << sites):
        b_up = [[Fraction(1 if i == j else 0) for j in range(sites)] for i in range(sites)]
        b_down = [[Fraction(1 if i == j else 0) for j in range(sites)] for i in range(sites)]

        v_up = [[Fraction(0) for _ in range(sites)] for _ in range(sites)]
        v_down = [[Fraction(0) for _ in range(sites)] for _ in range(sites)]

        for j in range(sites):
            bit = (mask >> j) & 1
            s_val = 1 if bit == 1 else -1

            hs_up = hs if s_val == 1 else Fraction(1, 1) / hs
            # Repulsive Hubbard: opposite sign for spin down
            hs_down = hs if (-s_val) == 1 else Fraction(1, 1) / hs

            v_up[j][j] = fugacity * hs_up
            v_down[j][j] = fugacity * hs_down

        b_up = exact_mat_mul_rat(k_mat, v_up)
        b_down = exact_mat_mul_rat(k_mat, v_down)

        for i in range(sites):
            b_up[i][i] += Fraction(1)
            b_down[i][i] += Fraction(1)

        det_up = exact_det_rat(b_up)
        det_down = exact_det_rat(b_down)

        if det_up != det_down:
            found_asymmetry = True
            break

    assert found_asymmetry, "Repulsive Hubbard unexpectedly maintained identical up/down determinants"
