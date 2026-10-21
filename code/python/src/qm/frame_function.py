"""QM-210 finite map: Born pairing and finite frame functions.

AuthorityEffect: None.

What the L1 shadow provides: count proportions on one diagonal. The import named
QM-210 is P(i) = |<i|psi>|^2 = Tr(rho E) together with the uniqueness theorems
(Gleason, Busch) that rest on every frame and on continuity. This control works
on a declared finite frame set in Q^4, the eighteen rays of Cabello, Estebaranz and
Garcia-Alcaine arranged in nine orthogonal bases, and computes exactly over Q:
the frame identity for quantum frame functions, the dimension of the space of all
frame functions on the finite set against the dimension of the quantum ones (the
nullity is the exact distance from a finite linear Gleason statement), the parity
obstruction that forbids any two-valued frame function (a Kochen-Specker set) with
the prefix of bases on which a two-valued function still exists as the negative
control, and a positivity-gap witness: a trace-one real symmetric matrix that is
not positive semidefinite yet is nonnegative on every declared ray. The Peres
24-ray set is run beside the Cabello set. Nothing here produces uniqueness.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from typing import Any, Sequence

from .context_parity import f2_eliminate

Vector = tuple[int, ...]

CABELLO_BASES: tuple[tuple[Vector, ...], ...] = (
    ((0, 0, 0, 1), (0, 0, 1, 0), (1, 1, 0, 0), (1, -1, 0, 0)),
    ((0, 0, 0, 1), (0, 1, 0, 0), (1, 0, 1, 0), (1, 0, -1, 0)),
    ((1, -1, 1, -1), (1, -1, -1, 1), (1, 1, 0, 0), (0, 0, 1, 1)),
    ((1, -1, 1, -1), (1, 1, 1, 1), (1, 0, -1, 0), (0, 1, 0, -1)),
    ((0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 1), (1, 0, 0, -1)),
    ((1, -1, -1, 1), (1, 1, 1, 1), (1, 0, 0, -1), (0, 1, -1, 0)),
    ((1, 1, -1, 1), (1, 1, 1, -1), (1, -1, 0, 0), (0, 0, 1, 1)),
    ((1, 1, -1, 1), (-1, 1, 1, 1), (1, 0, 1, 0), (0, 1, 0, -1)),
    ((1, 1, 1, -1), (-1, 1, 1, 1), (1, 0, 0, 1), (0, 1, -1, 0)),
)


class FrameControlRefusal(ValueError):
    """Typed refusal for malformed frame-function inputs."""


def peres_bases() -> tuple[tuple[Vector, ...], ...]:
    """The 24 Peres rays in Q^4 (entries in {0, 1, -1}, one, two or four nonzero entries,
    first nonzero entry positive) and the 24 orthogonal bases they form."""
    rays: list[Vector] = []
    for v in product((-1, 0, 1), repeat=4):
        nonzero = [x for x in v if x]
        if len(nonzero) in (1, 2, 4) and nonzero[0] == 1:
            rays.append(v)
    return tuple(
        b for b in combinations(rays, 4) if all(dot(u, w) == 0 for u, w in combinations(b, 2))
    )


def dot(u: Sequence[int], v: Sequence[int]) -> int:
    return sum(a * b for a, b in zip(u, v))


def proportional(u: Vector, v: Vector) -> bool:
    return all(u[i] * v[j] == u[j] * v[i] for i in range(len(u)) for j in range(len(u)))


def rays_of(bases: Sequence[Sequence[Vector]]) -> list[Vector]:
    rays: list[Vector] = []
    for basis in bases:
        for v in basis:
            if not any(proportional(v, r) for r in rays):
                rays.append(v)
    return rays


def ray_index(rays: Sequence[Vector], v: Vector) -> int:
    for i, r in enumerate(rays):
        if proportional(v, r):
            return i
    raise FrameControlRefusal("vector is not one of the declared rays")


def frame_set_checks(bases: Sequence[Sequence[Vector]]) -> dict[str, Any]:
    """Orthogonality of every basis, distinctness of the rays, and the incidence counts."""
    dim = len(bases[0][0])
    orthogonal = all(
        len(b) == dim and all(dot(u, v) == 0 for u, v in combinations(b, 2)) for b in bases
    )
    nonzero = all(dot(v, v) > 0 for b in bases for v in b)
    rays = rays_of(bases)
    counts = [0] * len(rays)
    for b in bases:
        for v in b:
            counts[ray_index(rays, v)] += 1
    return {
        "dimension": dim,
        "basis_count": len(bases),
        "ray_count": len(rays),
        "all_bases_orthogonal": orthogonal and nonzero,
        "ray_multiplicities": counts,
        "every_ray_in_exactly_two_bases": all(c == 2 for c in counts),
    }


def q_rank(rows: Sequence[Sequence[Fraction]]) -> int:
    m = [list(r) for r in rows]
    rank = 0
    ncols = len(m[0]) if m else 0
    for col in range(ncols):
        pivot = next((r for r in range(rank, len(m)) if m[r][col] != 0), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inv = 1 / m[rank][col]
        m[rank] = [x * inv for x in m[rank]]
        for r in range(len(m)):
            if r != rank and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[rank])]
        rank += 1
    return rank


def symmetric_basis(dim: int, traceless: bool) -> list[list[list[Fraction]]]:
    """A Q-basis of the real symmetric dim x dim matrices, or of the traceless ones."""
    mats: list[list[list[Fraction]]] = []
    diag_range = range(dim - 1) if traceless else range(dim)
    for i in diag_range:
        m = [[Fraction(0)] * dim for _ in range(dim)]
        m[i][i] = Fraction(1)
        if traceless:
            m[dim - 1][dim - 1] = Fraction(-1)
        mats.append(m)
    for i in range(dim):
        for j in range(i + 1, dim):
            m = [[Fraction(0)] * dim for _ in range(dim)]
            m[i][j] = m[j][i] = Fraction(1)
            mats.append(m)
    return mats


def quantum_frame_function(
    rho: Sequence[Sequence[Fraction]], rays: Sequence[Vector]
) -> list[Fraction]:
    """f_rho(v) = v^T rho v / v^T v on each ray: the Born pairing on the finite set."""
    out = []
    for v in rays:
        num = sum(Fraction(v[i]) * rho[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))
        out.append(num / dot(v, v))
    return out


def frame_identity_holds(
    rho: Sequence[Sequence[Fraction]], bases: Sequence[Sequence[Vector]]
) -> bool:
    """sum over an orthogonal basis of v^T rho v / v^T v equals Tr rho (checked exactly)."""
    trace = sum(rho[i][i] for i in range(len(rho)))
    rays = rays_of(bases)
    f = quantum_frame_function(rho, rays)
    return all(sum(f[ray_index(rays, v)] for v in b) == trace for b in bases)


def gleason_nullity(bases: Sequence[Sequence[Vector]]) -> dict[str, Any]:
    """Dimension of all frame functions on the finite set against the quantum ones.

    Frame functions: f with sum_{v in B} f(v) = 1 on every basis B (an affine space of
    dimension |rays| - rank). Quantum ones: f_rho for trace-one real symmetric rho (an
    affine space of dimension rank of the traceless directions). The nullity is their
    difference; a finite Gleason statement on this set would need it to be zero.
    """
    rays = rays_of(bases)
    dim = len(rays[0])
    constraint_rows = [
        [Fraction(1) if any(proportional(v, r) for v in b) else Fraction(0) for r in rays]
        for b in bases
    ]
    rank = q_rank(constraint_rows)
    all_dim = len(rays) - rank
    quantum_dim = q_rank([quantum_frame_function(m, rays) for m in symmetric_basis(dim, True)])
    quantum_linear_span = q_rank(
        [quantum_frame_function(m, rays) for m in symmetric_basis(dim, False)]
    )
    return {
        "ray_count": len(rays),
        "constraint_rank_q": rank,
        "frame_function_affine_dimension": all_dim,
        "quantum_affine_dimension": quantum_dim,
        "quantum_linear_span_dimension": quantum_linear_span,
        "nullity": all_dim - quantum_dim,
        "finite_gleason_holds": all_dim - quantum_dim == 0,
    }


def two_valued_frame_function(bases: Sequence[Sequence[Vector]]) -> list[int] | None:
    """A {0,1} assignment with exactly one 1 in every basis, by backtracking; None if none."""
    rays = rays_of(bases)
    index = [[ray_index(rays, v) for v in b] for b in bases]
    value: list[int | None] = [None] * len(rays)

    def place(k: int) -> bool:
        if k == len(index):
            return True
        for chosen in index[k]:
            assignment = {i: (1 if i == chosen else 0) for i in index[k]}
            if any(value[i] is not None and value[i] != a for i, a in assignment.items()):
                continue
            touched = [i for i in assignment if value[i] is None]
            for i in touched:
                value[i] = assignment[i]
            if place(k + 1):
                return True
            for i in touched:
                value[i] = None
        return False

    if not place(0):
        return None
    return [0 if v is None else v for v in value]


def parity_obstruction(bases: Sequence[Sequence[Vector]]) -> dict[str, Any]:
    """A {0,1} frame function needs M v = 1 over F_2; with every ray in two bases, M has
    even column sums, so the system is inconsistent when the number of bases is odd."""
    rays = rays_of(bases)
    rows = [[1 if any(proportional(v, r) for v in b) else 0 for r in rays] for b in bases]
    system = f2_eliminate(rows, [1] * len(bases))
    return {
        "basis_count": len(bases),
        "f2_rank": system["rank"],
        "f2_system_consistent": system["consistent"],
        "two_valued_function_by_search": two_valued_frame_function(bases) is not None,
    }


def _determinant(a: list[list[Fraction]]) -> Fraction:
    a = [row[:] for row in a]
    det = Fraction(1)
    for c in range(len(a)):
        pivot = next((r for r in range(c, len(a)) if a[r][c] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            det = -det
        det *= a[c][c]
        for r in range(c + 1, len(a)):
            factor = a[r][c] / a[c][c]
            a[r] = [x - factor * y for x, y in zip(a[r], a[c])]
    return det


def principal_minors_nonnegative(m: Sequence[Sequence[Fraction]]) -> bool:
    """Exact Sylvester test: a real symmetric matrix is positive semidefinite exactly when
    every principal minor is nonnegative."""
    n = len(m)
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            if _determinant([[m[i][j] for j in idx] for i in idx]) < 0:
                return False
    return True


def quadratic_form(m: Sequence[Sequence[Fraction]], v: Sequence[int]) -> Fraction:
    return sum(Fraction(v[i]) * m[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


def positivity_gap_witness(bases: Sequence[Sequence[Vector]]) -> dict[str, Any]:
    """A trace-one real symmetric matrix that is nonnegative on every declared ray and sums
    to one on every basis, yet is not positive semidefinite: the finite frame set does not
    see positivity. The witness (nonnegative on the Cabello rays and on the Peres rays) and
    its negative direction are fixed rationals; the leading 2 x 2 minor is -1/16."""
    half, quarter, zero = Fraction(1, 2), Fraction(1, 4), Fraction(0)
    rho = [
        [zero, -quarter, zero, zero],
        [-quarter, half, zero, quarter],
        [zero, zero, half, zero],
        [zero, quarter, zero, zero],
    ]
    negative_direction = (2, 1, 0, 0)
    values = quantum_frame_function(rho, rays_of(bases))
    nonnegative = all(x >= 0 for x in values)
    psd = principal_minors_nonnegative(rho)
    negative_value = quadratic_form(rho, negative_direction)
    return {
        "witness": [[str(x) for x in row] for row in rho],
        "trace_one": sum(rho[i][i] for i in range(4)) == 1,
        "frame_identity_holds": frame_identity_holds(rho, bases),
        "nonnegative_on_every_ray": nonnegative,
        "positive_semidefinite": psd,
        "negative_direction": list(negative_direction),
        "value_on_negative_direction": str(negative_value),
        "witness_is_a_gap": nonnegative and not psd and negative_value < 0,
    }


def colorability_profile(bases: Sequence[Sequence[Vector]]) -> dict[str, Any]:
    """For each prefix of the basis list, does a two-valued frame function exist?"""
    profile = []
    for k in range(1, len(bases) + 1):
        found = two_valued_frame_function(bases[:k])
        profile.append({"bases": k, "two_valued_exists": found is not None})
    first_uncolorable = next((p["bases"] for p in profile if not p["two_valued_exists"]), None)
    return {"profile": profile, "first_uncolorable_prefix": first_uncolorable}


def residual_import_ledger() -> list[dict[str, str]]:
    return [
        {
            "layer": "finite invariant",
            "status": "COMPUTED",
            "statement": "On the Cabello frame set in Q^4: the Born pairing satisfies the "
            "frame identity exactly; the affine space of all frame functions on the finite "
            "set coincides with the space of real symmetric trace-one quadratic forms "
            "(nullity zero on the prefixes of 3, 6 and 9 bases and on the Peres 24-ray "
            "set); no two-valued frame function exists (F_2 parity: nine bases, every ray "
            "in two), while every proper prefix of the basis list admits one.",
        },
        {
            "layer": "completion",
            "status": "IMPORTED",
            "statement": "Gleason uniqueness needs every frame in dimension >= 3 and the "
            "continuity it supplies; Busch's effect version needs every effect. Neither is a "
            "finite statement.",
        },
        {
            "layer": "residual import",
            "status": "IMPORTED",
            "statement": "Positivity, and the selection of real symmetric quadratic forms "
            "as the carrier of the pairing. The finite set fixes the linear span of the "
            "frame functions (nullity zero) but not the cone: a non-positive trace-one form "
            "is nonnegative on every declared ray. Noncontextuality as a selection rule "
            "yields an obstruction (no classical value assignment), not the quantum state "
            "space; complex Hermitian forms are not examined.",
        },
    ]


def evaluate_frame_function_control() -> dict[str, Any]:
    """Run the QM-210 control exactly over Q and return JSON-serializable results."""
    quarter = Fraction(1, 4)
    maximally_mixed = [[quarter if i == j else Fraction(0) for j in range(4)] for i in range(4)]
    pure = [[Fraction(1) if i == j == 0 else Fraction(0) for j in range(4)] for i in range(4)]
    generic = [
        [Fraction(1, 2), Fraction(1, 3), Fraction(0), Fraction(-1, 5)],
        [Fraction(1, 3), Fraction(1, 4), Fraction(1, 7), Fraction(0)],
        [Fraction(0), Fraction(1, 7), Fraction(1, 8), Fraction(2, 9)],
        [Fraction(-1, 5), Fraction(0), Fraction(2, 9), Fraction(1, 8)],
    ]
    peres = peres_bases()
    return {
        "frame_set": frame_set_checks(CABELLO_BASES),
        "frame_identity": {
            "maximally_mixed": frame_identity_holds(maximally_mixed, CABELLO_BASES),
            "pure_state": frame_identity_holds(pure, CABELLO_BASES),
            "generic_trace_one": frame_identity_holds(generic, CABELLO_BASES),
        },
        "gleason_nullity_by_prefix": {k: gleason_nullity(CABELLO_BASES[:k]) for k in (3, 6, 9)},
        "parity_obstruction": parity_obstruction(CABELLO_BASES),
        "colorability": colorability_profile(CABELLO_BASES),
        "positivity_gap": positivity_gap_witness(CABELLO_BASES),
        "peres_24": {
            "frame_set": frame_set_checks(peres),
            "gleason_nullity": gleason_nullity(peres),
            "parity_obstruction": parity_obstruction(peres),
            "positivity_gap": positivity_gap_witness(peres),
        },
        "residual_import_ledger": residual_import_ledger(),
    }
