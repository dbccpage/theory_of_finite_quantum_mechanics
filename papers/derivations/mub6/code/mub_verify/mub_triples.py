"""Exact MUB triple construction and algebraic verification.

AuthorityEffect: None.
stated region only; mints no authority.

Constructs genuine Dita seed triples {I, F6(dx,dy), Y2 (x) Q_a} and canonical T0
in exact cyclotomic arithmetic over Q(zeta_24).
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple

from .cyclotomic import Cyc24

D = 6

ExactVec = Tuple[Cyc24, ...]


def sqrt2_cyc() -> Cyc24:
    """sqrt(2) = zeta^3 + zeta^-3."""
    return Cyc24.zeta(3).add(Cyc24.zeta(-3))


def sqrt3_cyc() -> Cyc24:
    """sqrt(3) = zeta^2 + zeta^-2."""
    return Cyc24.zeta(2).add(Cyc24.zeta(-2))


def inv_sqrt2_cyc() -> Cyc24:
    """1/sqrt(2) = sqrt(2)/2."""
    return sqrt2_cyc().mul_rat(Fraction(1, 2))


def inv_sqrt3_cyc() -> Cyc24:
    """1/sqrt(3) = sqrt(3)/3."""
    return sqrt3_cyc().mul_rat(Fraction(1, 3))


def inv_sqrt6_cyc() -> Cyc24:
    """1/sqrt(6) = sqrt(2)*sqrt(3)/6."""
    return sqrt2_cyc().mul(sqrt3_cyc()).mul_rat(Fraction(1, 6))


def inner_product(u: ExactVec, v: ExactVec) -> Cyc24:
    """Exact inner product <u, v> = sum_k conj(u_k) * v_k."""
    acc = Cyc24.zero()
    for uk, vk in zip(u, v):
        acc = acc.add(uk.conj().mul(vk))
    return acc


def standard_basis_b1() -> List[ExactVec]:
    """Standard basis B1 = {e_0, ..., e_5}."""
    cols: List[ExactVec] = []
    for i in range(D):
        c = [Cyc24.zero()] * D
        c[i] = Cyc24.one()
        cols.append(tuple(c))
    return cols


def f3_entry(j: int, k: int) -> Cyc24:
    """F3 entry (j,k) = eta^{j*k} with eta = zeta_24^8."""
    return Cyc24.zeta((8 * j * k) % 24)


def f6_family_columns(dx: int, dy: int) -> List[ExactVec]:
    """Affine Fourier (Dita) family F6(dx, dy) with phases zeta^{dx}, zeta^{dy}."""
    s = inv_sqrt6_cyc()
    dphase = [
        Cyc24.one(),
        Cyc24.zeta(dx),
        Cyc24.zeta(dy),
    ]
    cols: List[ExactVec] = []
    for col in range(D):
        v = [Cyc24.zero()] * D
        if col < 3:
            for j in range(3):
                e = f3_entry(j, col).mul(s)
                v[j] = e
                v[j + 3] = e
        else:
            m = col - 3
            for j in range(3):
                e = dphase[j].mul(f3_entry(j, m)).mul(s)
                v[j] = e
                v[j + 3] = e.neg()
        cols.append(tuple(v))
    return cols


def qubit_y_columns() -> Tuple[Tuple[Cyc24, Cyc24], Tuple[Cyc24, Cyc24]]:
    """Qubit basis Y2: columns are (1/sqrt2)[1, i]^T and (1/sqrt2)[1, -i]^T."""
    s = inv_sqrt2_cyc()
    i_cyc = Cyc24.zeta(6)
    col0 = (s, i_cyc.mul(s))
    col1 = (s, i_cyc.mul(s).neg())
    return (col0, col1)


def qutrit_q_columns(a: int) -> List[Tuple[Cyc24, Cyc24, Cyc24]]:
    """Qutrit quadratic-Gauss basis Q_a, column m: (Q_a)_{j,m} = omega3^{a j^2 + m j} / sqrt3."""
    s = inv_sqrt3_cyc()
    cols: List[Tuple[Cyc24, Cyc24, Cyc24]] = []
    for m in range(3):
        col = []
        for j in range(3):
            exp = (a * j * j + m * j) % 3
            entry = Cyc24.zeta((8 * exp) % 24).mul(s)
            col.append(entry)
        cols.append((col[0], col[1], col[2]))
    return cols


def product_y2_qa_columns(a: int) -> List[ExactVec]:
    """Kronecker product basis Y2 (x) Q_a (6 columns)."""
    y2 = qubit_y_columns()
    qa = qutrit_q_columns(a)
    cols: List[ExactVec] = []
    for qb in y2:
        for qt in qa:
            v = [Cyc24.zero()] * D
            for a_idx in range(2):
                for b_idx in range(3):
                    v[a_idx * 3 + b_idx] = qb[a_idx].mul(qt[b_idx])
            cols.append(tuple(v))
    return cols


GENUINE_Y2Q1_SEEDS = ((0, 8), (8, 0), (16, 16))
GENUINE_Y2Q2_SEEDS = ((0, 16), (8, 8), (16, 0))


def resolve_seed_qa(dx: int, dy: int) -> int:
    """Resolve external B3 index a in {1, 2} for genuine Dita seed (dx, dy)."""
    if (dx, dy) in GENUINE_Y2Q1_SEEDS:
        return 1
    elif (dx, dy) in GENUINE_Y2Q2_SEEDS:
        return 2
    else:
        raise ValueError(f"({dx}, {dy}) is not a locked genuine Dita seed")


def dita_seed_triple_columns(dx: int, dy: int) -> List[ExactVec]:
    """18 exact columns of the triple {B1, F6(dx,dy), Y2 (x) Q_a}."""
    qa = resolve_seed_qa(dx, dy)
    cols: List[ExactVec] = []
    cols.extend(standard_basis_b1())
    cols.extend(f6_family_columns(dx, dy))
    cols.extend(product_y2_qa_columns(qa))
    return cols


def check_basis_orthonormal(basis: Sequence[ExactVec]) -> bool:
    """Verify that a set of 6 vectors forms an exact orthonormal basis."""
    if len(basis) != D:
        return False
    one = Cyc24.one()
    zero = Cyc24.zero()
    for i in range(D):
        for j in range(D):
            ip = inner_product(basis[i], basis[j])
            want = one if i == j else zero
            if ip != want:
                return False
    return True


def check_bases_mutually_unbiased(b1: Sequence[ExactVec], b2: Sequence[ExactVec]) -> bool:
    """Verify that |<u, v>|^2 = 1/6 for all u in b1, v in b2."""
    sixth = Cyc24.rat(Fraction(1, 6))
    for u in b1:
        for v in b2:
            ip = inner_product(u, v)
            if ip.abs_sq() != sixth:
                return False
    return True


def verify_triple_pairwise_mu(triple_cols: Sequence[ExactVec]) -> bool:
    """Verify that the 18 columns form 3 orthonormal bases that are pairwise MU."""
    if len(triple_cols) != 18:
        return False
    b1 = triple_cols[0:6]
    b2 = triple_cols[6:12]
    b3 = triple_cols[12:18]

    if not (check_basis_orthonormal(b1) and check_basis_orthonormal(b2) and check_basis_orthonormal(b3)):
        return False

    return (
        check_bases_mutually_unbiased(b1, b2)
        and check_bases_mutually_unbiased(b1, b3)
        and check_bases_mutually_unbiased(b2, b3)
    )
