"""
Unit tests for GF(2) matrix operations, nilpotency refusal, and residual trichotomy.
AuthorityEffect: None.
"""

import numpy as np
import pytest

from majorana_evaluator import (
    GF2Matrix,
    F2CochainComplex,
    TrichotomyClass,
    classify_residual,
    verify_norm_equivalence,
)


def test_gf2_matrix_rank_and_solve():
    # 3x3 identity matrix over GF(2)
    ident = GF2Matrix.from_array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert ident.rank() == 3

    b = np.array([1, 1, 0])
    sol = ident.solve(b)
    assert sol is not None
    assert np.array_equal(sol, b)

    # Singular matrix
    sing = GF2Matrix.from_array([[1, 1], [1, 1]])
    assert sing.rank() == 1
    # Solvable system: [1, 1]^T has solution [1, 0]
    assert sing.solve(np.array([1, 1])) is not None
    # Unsolvable system: [1, 0]^T has no solution
    assert sing.solve(np.array([1, 0])) is None


def test_cochain_nilpotency_and_refusal():
    # Simple complex: triangle graph (3 vertices, 3 edges, 1 face)
    # d0: edges x vertices
    d0_data = [
        [1, 1, 0],  # e0 = v0 - v1
        [0, 1, 1],  # e1 = v1 - v2
        [1, 0, 1],  # e2 = v0 - v2
    ]
    # d1: face x edges (f0 = e0 + e1 + e2)
    d1_data = [
        [1, 1, 1]
    ]

    complex_valid = F2CochainComplex(
        n0=3, n1=3, n2=1,
        d0=GF2Matrix.from_array(d0_data),
        d1=GF2Matrix.from_array(d1_data),
    )
    assert complex_valid.is_nilpotent() is True

    # Mutated complex violating nilpotency
    d1_invalid = GF2Matrix.from_array([[1, 1, 0]])
    complex_invalid = F2CochainComplex(
        n0=3, n1=3, n2=1,
        d0=GF2Matrix.from_array(d0_data),
        d1=d1_invalid,
    )
    assert complex_invalid.is_nilpotent() is False

    # Classification must strictly refuse invalid complex
    status, meta = classify_residual(complex_invalid, np.array([1, 0, 0]))
    assert status == TrichotomyClass.REPRESENTATION_INVALID
    assert "d1 * d0 != 0" in meta["reason"]


def test_residual_trichotomy_classification():
    # Triangle complex: H1 dimension is (3 - rank(d1)) - rank(d0) = (3 - 1) - 2 = 0
    # To have a non-trivial H1, remove the face: C0 -> C1 -> 0
    d0_data = [
        [1, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
    ]
    d1_zero = GF2Matrix.from_array([[0, 0, 0]])
    triangle_no_face = F2CochainComplex(
        n0=3, n1=3, n2=1,
        d0=GF2Matrix.from_array(d0_data),
        d1=d1_zero,
    )
    assert triangle_no_face.betti_1() == 1

    # 1. Exact coboundary: column 0 of d0 = [1, 0, 1]^T
    coboundary = np.array([1, 0, 1])
    status, _ = classify_residual(triangle_no_face, coboundary)
    assert status == TrichotomyClass.EXACT

    # 2. Closed residual: cycle loop [1, 1, 1]^T (not in im(d0) because rank(d0)=2 and [1,1,1] not in span)
    # Check: [1,1,1] = e0 + e1 + e2. Sum of d0 rows is [2, 2, 2] = 0 mod 2.
    cycle = np.array([1, 1, 1])
    status, _ = classify_residual(triangle_no_face, cycle)
    assert status == TrichotomyClass.CLOSED_RESIDUAL

    # 3. Open obstruction: if we put a non-zero face
    triangle_with_face = F2CochainComplex(
        n0=3, n1=3, n2=1,
        d0=GF2Matrix.from_array(d0_data),
        d1=GF2Matrix.from_array([[1, 1, 1]]),
    )
    single_edge = np.array([1, 0, 0])
    status, meta = classify_residual(triangle_with_face, single_edge)
    assert status == TrichotomyClass.OPEN_OBSTRUCTION
    assert meta["syndrome_weight"] == 1


def test_norm_equivalence_on_binary_vectors():
    # Theorem 6.1: ||v||_p^p = wt(v) for all p >= 1 on binary vectors
    v1 = [1, 0, 1, 1, 0, 0, 1]
    assert verify_norm_equivalence(v1) is True

    v2 = [0, 0, 0]
    assert verify_norm_equivalence(v2) is True

    v3 = [1, 1, 1, 1]
    assert verify_norm_equivalence(v3) is True


def test_ising_fusion_and_braid_relations():
    """Verifies Claim MAJ-C7: Ising fusion rules, quantum dimensions, and Yang-Baxter braid relation."""
    from majorana_evaluator import IsingFusionAlgebra

    assert IsingFusionAlgebra.verify_quantum_dimensions() is True
    assert IsingFusionAlgebra.verify_yang_baxter_braid() is True


def test_parity_observable_algebra_and_sector_splitting():
    """Verifies Claim MAJ-C8: Parity observable algebra P^2 = I, [P, H] = 0, and sector splitting."""
    from majorana_evaluator import ParityAlgebraModel

    model = ParityAlgebraModel(num_modes=2)
    assert model.verify_involutory_and_hermitian() is True

    # Parity-conserving quadratic Hamiltonian (pairing between modes 1 and 2)
    # in 4-dim Fock space: |00>, |01>, |10>, |11>
    H = np.zeros((4, 4), dtype=complex)
    H[0, 3] = 0.5  # creates 2 fermions: |00> <-> |11> (even-even coupling)
    H[3, 0] = 0.5
    H[1, 2] = -0.3 # hopping: |01> <-> |10> (odd-odd coupling)
    H[2, 1] = -0.3

    assert model.verify_hamiltonian_commutation(H) is True
    H_even, H_odd = model.sector_splitting(H)
    assert H_even.shape == (2, 2)
    assert H_odd.shape == (2, 2)


def test_pfaffian_z2_topological_invariant():
    """Verifies Claim MAJ-C9: Pfaffian topological invariant nu = sgn(Pf(B)) in {+1, -1}."""
    from majorana_evaluator import pfaffian_z2_invariant

    # Topological phase: |mu| < 2t (e.g. mu = 0.5, t = 1.0)
    nu_topological = pfaffian_z2_invariant(mu=0.5, t=1.0, delta=1.0, L=4)
    assert nu_topological == -1

    # Trivial phase: |mu| > 2t (e.g. mu = 2.5, t = 1.0)
    nu_trivial = pfaffian_z2_invariant(mu=2.5, t=1.0, delta=1.0, L=4)
    assert nu_trivial == 1


def test_trichotomy_benchmark_6x6_torus():
    """Verifies Claims MAJ-C3 & MAJ-C16: O(n^3) benchmark runtime on 6x6 torus."""
    import time
    from majorana_evaluator import build_tetron_carrier

    t66 = build_tetron_carrier("torus", rows=6, cols=6)
    assert t66.complex.n0 == 36
    assert t66.complex.n1 == 72
    assert t66.h1_dim == 2

    # Residual to classify
    res = np.zeros(t66.complex.n1, dtype=int)
    res[0] = 1

    t0 = time.perf_counter()
    status, meta = classify_residual(t66.complex, res)
    elapsed = time.perf_counter() - t0

    assert status == TrichotomyClass.OPEN_OBSTRUCTION
    assert elapsed < 0.1  # Fast GF(2) reduction < 100 ms

