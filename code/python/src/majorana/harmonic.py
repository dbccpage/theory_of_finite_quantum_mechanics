"""l1 harmonic projection and cohomology-class typing over GF(2).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from .gf2_terminalizer import GF2Matrix, Gf2CocycleClassifier

DEFAULT_BUDGET: int = 1 << 22


@dataclass
class H1Basis:
    dim_h1: int
    generators: list[list[int]]  # each of length num_edges
    d0_rank: int
    d1_rank: int
    im_d0_basis: list[list[int]]  # basis vectors for image d0


@dataclass
class L1HarmonicProjection:
    class_id: int
    class_coordinates: list[int]
    phi1_min_weight: int
    representative: list[int]
    exact_within_budget: bool
    coset_elements_evaluated: int


def _nullspace(m: GF2Matrix) -> list[list[int]]:
    """Find a basis for the nullspace ker(M) = { x : M x = 0 mod 2 }."""
    # Augmented matrix [M^T | I]
    # M has shape (rows, cols)
    # M x = 0 <=> x in ker(M)
    # Using Gaussian elimination on M
    red, pivots, rank = m.row_reduce()
    free_cols = [c for c in range(m.cols) if c not in pivots]
    basis = []
    for f in free_cols:
        v = [0] * m.cols
        v[f] = 1
        for r, p in enumerate(pivots):
            if red.data[r][f] == 1:
                v[p] = 1
        basis.append(v)
    return basis


def h1_basis(d0: GF2Matrix, d1: GF2Matrix) -> H1Basis:
    if not Gf2CocycleClassifier.verify_boundary(d0, d1):
        raise ValueError("Invalid boundary d1 * d0 != 0")
    num_edges = d0.rows
    # 1. Basis for im(d0) (column space of d0)
    # Pivot columns of d0 give a basis for col(d0)
    _, d0_pivots, d0_rank = d0.row_reduce()
    im_d0_basis = []
    for p in d0_pivots:
        im_d0_basis.append([d0.data[r][p] for r in range(num_edges)])

    # 2. Basis for ker(d1)
    ker_d1 = _nullspace(d1)
    d1_rank = d1.rank()

    # 3. Find vectors in ker(d1) linearly independent mod im(d0)
    # We build a matrix with rows from im_d0_basis, and greedily add from ker_d1
    current_space = [list(r) for r in im_d0_basis]
    generators: list[list[int]] = []

    for v in ker_d1:
        test_mat = GF2Matrix.from_data(current_space + [v])
        if test_mat.rank() > len(current_space):
            generators.append(v)
            current_space.append(v)

    dim_h1 = len(generators)
    return H1Basis(
        dim_h1=dim_h1,
        generators=generators,
        d0_rank=d0_rank,
        d1_rank=d1_rank,
        im_d0_basis=im_d0_basis,
    )


def l1_harmonic_projection(
    d0: GF2Matrix,
    d1: GF2Matrix,
    basis: H1Basis,
    residual: Sequence[int],
    budget: int = DEFAULT_BUDGET,
) -> L1HarmonicProjection:
    syndrome = d1.multiply_vector(residual)
    if any(s != 0 for s in syndrome):
        raise ValueError("Residual is not closed (d1 r != 0); has no cohomology class")

    num_edges = d0.rows
    # 1. Determine class coordinates c_1, ..., c_k
    # We need to solve: residual + sum c_i g_i in im(d0)
    # System: [im_d0_basis | generators]^T * x = residual
    coord_mat_cols = basis.im_d0_basis + basis.generators
    if not coord_mat_cols:
        class_coords = []
        class_id = 0
    else:
        # Solve A * x = residual mod 2 where cols of A are coord_mat_cols
        A_data = [[col[r] for col in coord_mat_cols] for r in range(num_edges)]
        A = GF2Matrix.from_data(A_data)
        sol = Gf2CocycleClassifier.solve_coboundary(A, residual)
        if sol is None:
            raise ValueError("Failed to resolve residual in cohomology basis")
        gen_start = len(basis.im_d0_basis)
        class_coords = sol[gen_start:]
        class_id = sum(bit * (1 << i) for i, bit in enumerate(class_coords))

    # 2. Minimize Hamming weight over r + im(d0)
    # Coset search over 2^(len(im_d0_basis))
    k = len(basis.im_d0_basis)
    total_elements = 1 << k
    evaluated = 0
    exact = True

    best_rep = list(residual)
    min_wt = sum(b % 2 for b in best_rep)

    if total_elements > budget:
        exact = False
        limit = budget
    else:
        limit = total_elements

    # Fast gray-code or binary iteration over im_d0_basis
    curr = list(residual)
    for mask in range(1, limit):
        # bit flipped:
        diff = mask ^ (mask - 1)
        flipped_bit = (diff.bit_length() - 1)
        if flipped_bit < k:
            basis_vec = basis.im_d0_basis[flipped_bit]
            for i in range(num_edges):
                curr[i] ^= basis_vec[i]
            wt = sum(curr)
            if wt < min_wt:
                min_wt = wt
                best_rep = list(curr)
        evaluated += 1

    return L1HarmonicProjection(
        class_id=class_id,
        class_coordinates=class_coords,
        phi1_min_weight=min_wt,
        representative=best_rep,
        exact_within_budget=exact,
        coset_elements_evaluated=max(evaluated, 1),
    )


def code_distance(
    d0: GF2Matrix, d1: GF2Matrix, basis: H1Basis, budget: int = DEFAULT_BUDGET
) -> Optional[int]:
    if basis.dim_h1 == 0:
        return None
    min_dist: Optional[int] = None
    num_classes = 1 << basis.dim_h1
    for class_idx in range(1, num_classes):
        # Construct representative for class_idx
        rep = [0] * d0.rows
        for i in range(basis.dim_h1):
            if (class_idx >> i) & 1:
                for r in range(d0.rows):
                    rep[r] ^= basis.generators[i][r]
        proj = l1_harmonic_projection(d0, d1, basis, rep, budget)
        if min_dist is None or proj.phi1_min_weight < min_dist:
            min_dist = proj.phi1_min_weight
            if min_dist == 1:
                break
    return min_dist
