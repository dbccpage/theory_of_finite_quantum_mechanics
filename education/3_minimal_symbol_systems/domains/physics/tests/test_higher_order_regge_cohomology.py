"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import sys
from pathlib import Path

import numpy as np

# Add physics code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from higher_order_regge_cohomology import (
    HigherOrderSimplicialComplex,
)


def test_4sphere_seed_boundary_nilpotency_all_orders():
    """
    Verifies that the standard 4-sphere S^4 triangulation (boundary of a 5-simplex)
    satisfies exact integer boundary nilpotency B_{k-1} * B_k = 0 for all k in {2, 3, 4},
    coboundary nilpotency delta_{k} o delta_{k-1} = 0, and exact Betti numbers beta = (1, 0, 0, 0, 1).
    """
    manifold = HigherOrderSimplicialComplex()
    receipt = manifold.evaluate_higher_order_cohomology(surgery_label="Seed_S4")

    # Topological counts for boundary of 5-simplex
    assert receipt.num_vertices == 6
    assert receipt.num_edges == 15
    assert receipt.num_triangles == 20
    assert receipt.num_tetrahedra == 15
    assert receipt.num_four_simplices == 6
    assert receipt.euler_characteristic == 2

    # Higher-order boundary nilpotency (k >= 3)
    assert receipt.is_b1_b2_nilpotent, "B_1 * B_2 != 0"
    assert receipt.is_b2_b3_nilpotent, "B_2 * B_3 != 0 (k=3 boundary nilpotency failed)"
    assert receipt.is_b3_b4_nilpotent, "B_3 * B_4 != 0 (k=4 boundary nilpotency failed)"

    # Coboundary nilpotency
    assert receipt.is_delta1_delta0_nilpotent
    assert receipt.is_delta2_delta1_nilpotent
    assert receipt.is_delta3_delta2_nilpotent
    assert receipt.is_all_nilpotent

    # Cohomology Betti numbers for S^4
    beta_0, beta_1, beta_2, beta_3, beta_4 = receipt.betti_numbers
    assert beta_0 == 1, f"Expected beta_0 = 1, got {beta_0}"
    assert beta_1 == 0, f"Expected beta_1 = 0, got {beta_1}"
    assert beta_2 == 0, f"Expected beta_2 = 0, got {beta_2}"
    assert beta_3 == 0, f"Expected beta_3 = 0, got {beta_3}"
    assert beta_4 == 1, f"Expected beta_4 = 1, got {beta_4}"

    # Euler-Poincaré formula: chi = sum (-1)^k beta_k = 1 - 0 + 0 - 0 + 1 = 2
    assert (beta_0 - beta_1 + beta_2 - beta_3 + beta_4) == receipt.euler_characteristic


def test_pachner_1_to_5_surgery_cohomology_invariance():
    """
    Verifies that a 1->5 Pachner bistellar move (stellar subdivision of a 4-simplex)
    preserves exact boundary nilpotency B_2 * B_3 = 0, B_3 * B_4 = 0,
    Euler characteristic chi = 2, and Betti numbers.
    """
    manifold = HigherOrderSimplicialComplex()
    assert manifold.apply_1_to_5_move()

    receipt = manifold.evaluate_higher_order_cohomology(surgery_label="Pachner_1_to_5")

    # 1->5 move: N0 increases by 1 (6 -> 7), N4 increases by 4 (6 -> 10)
    assert receipt.num_vertices == 7
    assert receipt.num_four_simplices == 10
    assert receipt.euler_characteristic == 2

    # Boundary nilpotency for k >= 3 must remain exact
    assert receipt.is_b2_b3_nilpotent, "1->5 move broke B_2 * B_3 = 0"
    assert receipt.is_b3_b4_nilpotent, "1->5 move broke B_3 * B_4 = 0"
    assert receipt.is_all_nilpotent

    # Topological invariance of cohomology
    assert receipt.betti_numbers == (1, 0, 0, 0, 1)


def test_pachner_2_to_4_surgery_cohomology_invariance():
    """
    Verifies that a 2->4 Pachner bistellar move (transverse edge insertion)
    preserves exact boundary nilpotency B_2 * B_3 = 0, B_3 * B_4 = 0,
    Euler characteristic chi = 2, and Betti numbers.
    """
    manifold = HigherOrderSimplicialComplex()
    # Apply 1->5 first to create interior tetrahedra, then apply 2->4
    assert manifold.apply_1_to_5_move()
    success_2_4 = manifold.apply_2_to_4_move()
    assert success_2_4, "2->4 move failed on subdivided complex"

    receipt = manifold.evaluate_higher_order_cohomology(surgery_label="Pachner_2_to_4")
    assert receipt.euler_characteristic == 2
    assert receipt.is_b2_b3_nilpotent, "2->4 move broke B_2 * B_3 = 0"
    assert receipt.is_b3_b4_nilpotent, "2->4 move broke B_3 * B_4 = 0"
    assert receipt.is_all_nilpotent
    assert receipt.betti_numbers == (1, 0, 0, 0, 1)


def test_hodge_laplacians_positive_semidefinite_and_harmonic_dimension():
    """
    Verifies that combinatorial Hodge Laplacians Delta_k = B_k^T B_k + B_{k+1} B_{k+1}^T
    are symmetric positive semi-definite, and dim(ker Delta_k) equals the Betti number beta_k.
    """
    manifold = HigherOrderSimplicialComplex()
    d0, d1, d2, d3, d4 = manifold.compute_hodge_laplacians()
    betti = manifold.compute_betti_numbers()

    for k, delta_k in enumerate([d0, d1, d2, d3, d4]):
        # Symmetry: Delta_k = Delta_k^T
        assert np.allclose(delta_k, delta_k.T), f"Hodge Laplacian Delta_{k} is not symmetric"

        # Positive semi-definiteness: all eigenvalues >= -1e-10
        eigvals = np.linalg.eigvalsh(delta_k)
        assert np.all(eigvals >= -1e-10), f"Hodge Laplacian Delta_{k} has negative eigenvalues"

        # Harmonic cochain count = number of zero eigenvalues
        num_harmonic = np.sum(np.isclose(eigvals, 0.0, atol=1e-8))
        assert num_harmonic == betti[k], (
            f"Harmonic dimension mismatch at k={k}: dim(ker Delta_{k})={num_harmonic} != beta_{k}={betti[k]}"
        )


def test_adversarial_corrupted_boundary_orientation_detection():
    """
    INVARIANT: Any corrupted orientation sign in B_3 or B_4 must immediately violate
    nilpotency B_2 * B_3 = 0 or B_3 * B_4 = 0, proving the test suite is non-trivial and falsifiable.
    """
    manifold = HigherOrderSimplicialComplex()
    b1, b2, b3, b4 = manifold.build_boundary_matrices()

    # Intentionally corrupt B_3 by flipping a non-zero entry's sign
    b3_corrupted = b3.copy()
    nz_indices = np.nonzero(b3_corrupted)
    b3_corrupted[nz_indices[0][0], nz_indices[1][0]] *= -1

    # Product B_2 * B_3_corrupted must NOT vanish
    p23_corrupted = b2 @ b3_corrupted
    assert not np.all(p23_corrupted == 0), "Corrupted B_3 was falsely accepted as nilpotent!"

    # Intentionally corrupt B_4 by flipping a non-zero entry's sign
    b4_corrupted = b4.copy()
    nz4_indices = np.nonzero(b4_corrupted)
    b4_corrupted[nz4_indices[0][0], nz4_indices[1][0]] *= -1

    # Product B_3 * B_4_corrupted must NOT vanish
    p34_corrupted = b3 @ b4_corrupted
    assert not np.all(p34_corrupted == 0), "Corrupted B_4 was falsely accepted as nilpotent!"
