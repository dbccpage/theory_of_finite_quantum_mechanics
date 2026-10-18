"""Target A4 Python Exact Rational & Cyclotomic Certifier for 24x24 Gramian Matrix.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority.

This module implements the exact Python counterpart to `mub6_quad_sdp.rs` and
`CandidateGramPositivity.lean` for Target A4 (and Target 5):
1. Formulation of the 24x24 Gramian matrix G(B) over exact cyclotomic arithmetic (Q(zeta_24))
   and exact rational arithmetic (Q).
2. Characterization of the exact block structure:
   - Diagonal blocks equal to I_6 (orthonormal bases).
   - Off-diagonal blocks satisfying |G_{ij}|^2 = 1/6 (mutually unbiased condition).
   - Exact Hermitian symmetry G_{ji} = G_{ij}^*.
3. Connection to the dual witness W = L D L^dagger (D >= 0) and exact LDL^T decomposition:
   - Constructive PSD verification for candidate dual witness matrices.
   - Trace inner product Tr(W * G) = sum_{i,j} W_{ij} G_{ji}.
   - Incompatibility obstruction certification Tr(W * G) < 0 showing G is not PSD.
4. Complete Zero Floating-Point enforcement (no float / f32 / f64 types admitted).
5. Comprehensive negative control matrix rejection routines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from .cyclotomic import Cyc24
from .mub_triples import (
    D,
    inner_product as cyc_inner_product,
    inv_sqrt2_cyc,
    inv_sqrt6_cyc,
    product_y2_qa_columns,
    qutrit_q_columns,
    sqrt2_cyc,
    sqrt3_cyc,
    standard_basis_b1,
)

# Constants & Epistemic Firewall
DIM_HILBERT: int = 6
NUM_BASES: int = 4
GRAMIAN_DIM: int = NUM_BASES * DIM_HILBERT  # 24
SCHEMA_VERSION: str = "omega.mub.quad-sdp.v2"
FIREWALL_LINE: str = "stated region only; mints no authority"
AUTHORITY_EFFECT: str = "None"
SCOPE_STRING: str = "single_synthetic_block_matrix"

TAO_PHASES: Tuple[Tuple[int, ...], ...] = (
    (0, 0, 0, 0, 0, 0),
    (0, 0, 1, 1, 2, 2),
    (0, 1, 0, 2, 2, 1),
    (0, 1, 2, 0, 1, 2),
    (0, 2, 2, 1, 0, 1),
    (0, 2, 1, 2, 1, 0),
)


# ==============================================================================
# Zero Floating-Point Type Auditor
# ==============================================================================

def assert_no_float(obj: Any, path: str = "root") -> None:
    """Recursively verify that no float types exist in any certifier data structure.
    
    Raises TypeError if float or complex built-in types are detected.
    """
    if isinstance(obj, (float, complex)):
        raise TypeError(
            f"Zero Float Violation: Found float type {type(obj).__name__} at '{path}': {obj}. "
            "All arithmetic must be exact Fraction or Cyc24."
        )
    elif isinstance(obj, (list, tuple)):
        for idx, item in enumerate(obj):
            assert_no_float(item, f"{path}[{idx}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            assert_no_float(v, f"{path}['{k}']")
    elif hasattr(obj, "__dataclass_fields__"):
        for f_name in obj.__dataclass_fields__:
            assert_no_float(getattr(obj, f_name), f"{path}.{f_name}")


# ==============================================================================
# Exact Arithmetic Helpers & Field Projections
# ==============================================================================

def exact_rational(value: Cyc24) -> Fraction:
    """Extract exact rational value from Cyc24 element, ensuring it lies in Q.
    
    Raises ValueError if any cyclotomic coefficient a_1..a_7 is non-zero.
    """
    if any(c != 0 for c in value.coeffs[1:]):
        raise ValueError(
            f"Cyclotomic value is not rational: {value} has non-zero non-rational parts"
        )
    return value.coeffs[0]


def sqrt6_cyc() -> Cyc24:
    """sqrt(6) = sqrt(2) * sqrt(3) in Q(zeta_24)."""
    return sqrt2_cyc().mul(sqrt3_cyc())


def omega3_pow(exp: int) -> Cyc24:
    """omega_3^exp = zeta_24^{8 * (exp % 3)} in Q(zeta_24)."""
    return Cyc24.zeta((8 * (exp % 3)) % 24)


# ==============================================================================
# Canonical Basis Columns & 24x24 Gramian Construction
# ==============================================================================

def qubit_x_columns() -> Tuple[Tuple[Cyc24, Cyc24], Tuple[Cyc24, Cyc24]]:
    """Qubit basis X2: columns are (1/sqrt2)[1, 1]^T and (1/sqrt2)[1, -1]^T."""
    s = inv_sqrt2_cyc()
    col0 = (s, s)
    col1 = (s, s.neg())
    return (col0, col1)


def canonical_triple_exact() -> List[Tuple[Cyc24, ...]]:
    """The 18 exact column vectors of canonical triple T0 = {Z2(x)Z3, X2(x)Q0, Y2(x)Q1} in C^6.
    
    Returns:
    - Columns 0..5: B0 (Standard basis Z2 (x) Z3)
    - Columns 6..11: B1 (X2 (x) Q0)
    - Columns 12..17: B2 (Y2 (x) Q1)
    """
    cols: List[Tuple[Cyc24, ...]] = []
    # B0: Standard basis
    cols.extend(standard_basis_b1())

    # B1: X2 (x) Q0
    x2 = qubit_x_columns()
    q0 = qutrit_q_columns(0)
    for qb in x2:
        for qt in q0:
            v = [Cyc24.zero()] * DIM_HILBERT
            for a_idx in range(2):
                for b_idx in range(3):
                    v[a_idx * 3 + b_idx] = qb[a_idx].mul(qt[b_idx])
            cols.append(tuple(v))

    # B2: Y2 (x) Q1
    cols.extend(product_y2_qa_columns(1))
    return cols


def tao_s6_block() -> List[List[Cyc24]]:
    """Construct the 6x6 Tao Hadamard matrix S6 with entries S6[j][k] = omega_3^{phases[j][k]} / sqrt(6)."""
    s = inv_sqrt6_cyc()
    mat: List[List[Cyc24]] = []
    for j in range(DIM_HILBERT):
        row: List[Cyc24] = []
        for k in range(DIM_HILBERT):
            exp = TAO_PHASES[j][k]
            z = omega3_pow(exp).mul(s)
            row.append(z)
        mat.append(row)
    return mat


def canonical_quad_gramian() -> List[List[Cyc24]]:
    """Construct the 24x24 Gramian overlap matrix G for the candidate 4-basis configuration.
    
    Structure:
    - Blocks (a, b) for a, b in {0, 1, 2}: exact inner products of canonical triple T0.
    - Block (3, 3): 6x6 identity matrix I_6.
    - Off-diagonal blocks (a, 3): S6 for a in {0, 1, 2}.
    - Off-diagonal blocks (3, a): S6^dagger for a in {0, 1, 2}.
    """
    cols = canonical_triple_exact()
    s6 = tao_s6_block()
    g = [[Cyc24.zero() for _ in range(GRAMIAN_DIM)] for _ in range(GRAMIAN_DIM)]

    # Blocks 0, 1, 2: pairwise Gramian from canonical triple T0
    for a in range(3):
        for b in range(3):
            for j in range(DIM_HILBERT):
                for k in range(DIM_HILBERT):
                    u = cols[a * DIM_HILBERT + j]
                    v = cols[b * DIM_HILBERT + k]
                    g[a * DIM_HILBERT + j][b * DIM_HILBERT + k] = cyc_inner_product(u, v)

    # Block 3: diagonal identity I_6
    one = Cyc24.one()
    for j in range(DIM_HILBERT):
        g[3 * DIM_HILBERT + j][3 * DIM_HILBERT + j] = one

    # Off-diagonal Block 3: G_{a, 3} = S6 and G_{3, a} = S6^dagger for a in {0, 1, 2}
    for a in range(3):
        for j in range(DIM_HILBERT):
            for k in range(DIM_HILBERT):
                entry = s6[j][k]
                g[a * DIM_HILBERT + j][3 * DIM_HILBERT + k] = entry
                g[3 * DIM_HILBERT + k][a * DIM_HILBERT + j] = entry.conj()

    return g


def compute_gram_matrix_cyc(vectors: Sequence[Sequence[Cyc24]]) -> List[List[Cyc24]]:
    """Construct exact cyclotomic Gram matrix G_ij = <v_i, v_j> = sum_k conj(v_i[k]) * v_j[k]."""
    n = len(vectors)
    G = [[Cyc24.zero() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            G[i][j] = cyc_inner_product(vectors[i], vectors[j])
    return G


# ==============================================================================
# Exact Block Structure Verifier
# ==============================================================================

@dataclass(frozen=True)
class GramianStructureReport:
    """Report on the exact block structure of the 24x24 Gramian matrix."""
    diagonal_blocks_identity: bool
    off_diagonal_blocks_modulus_sixth: bool
    hermitian_exact: bool
    verified_sound: bool
    dimension: int = GRAMIAN_DIM
    bases_count: int = NUM_BASES
    details: str = ""


def verify_gramian_structure(g: Sequence[Sequence[Cyc24]]) -> GramianStructureReport:
    """Verify that a 24x24 matrix has the exact structure of a 4-MUB Gramian:
    
    1. Diagonal blocks are exactly I_6.
    2. Off-diagonal blocks satisfy |G_{ij}|^2 = 1/6.
    3. The matrix is strictly Hermitian: G_{ji} = G_{ij}^*.
    """
    if len(g) != GRAMIAN_DIM or any(len(row) != GRAMIAN_DIM for row in g):
        return GramianStructureReport(
            diagonal_blocks_identity=False,
            off_diagonal_blocks_modulus_sixth=False,
            hermitian_exact=False,
            verified_sound=False,
            dimension=len(g),
            details=f"Invalid matrix dimension: expected {GRAMIAN_DIM}x{GRAMIAN_DIM}, got {len(g)}x{len(g[0]) if g else 0}"
        )

    sixth = Cyc24.rat(Fraction(1, 6))
    one = Cyc24.one()
    zero = Cyc24.zero()

    # 1. Diagonal blocks are identity
    diag_ok = True
    diag_errors: List[str] = []
    for a in range(NUM_BASES):
        for i in range(DIM_HILBERT):
            for j in range(DIM_HILBERT):
                idx_i = a * DIM_HILBERT + i
                idx_j = a * DIM_HILBERT + j
                if i == j:
                    if g[idx_i][idx_j] != one:
                        diag_ok = False
                        diag_errors.append(f"G[{idx_i},{idx_j}] != 1")
                else:
                    if g[idx_i][idx_j] != zero:
                        diag_ok = False
                        diag_errors.append(f"G[{idx_i},{idx_j}] != 0")

    # 2. Off-diagonal blocks have modulus squared = 1/6
    modulus_ok = True
    modulus_errors: List[str] = []
    for a in range(NUM_BASES):
        for b in range(NUM_BASES):
            if a == b:
                continue
            for i in range(DIM_HILBERT):
                for j in range(DIM_HILBERT):
                    idx_i = a * DIM_HILBERT + i
                    idx_j = b * DIM_HILBERT + j
                    entry = g[idx_i][idx_j]
                    mod_sq = entry.abs_sq()
                    if mod_sq != sixth:
                        modulus_ok = False
                        modulus_errors.append(f"|G[{idx_i},{idx_j}]|^2 = {mod_sq} != 1/6")

    # 3. Exactly Hermitian
    herm_ok = True
    herm_errors: List[str] = []
    for i in range(GRAMIAN_DIM):
        for j in range(GRAMIAN_DIM):
            if g[j][i] != g[i][j].conj():
                herm_ok = False
                herm_errors.append(f"G[{j},{i}] != G[{i},{j}]^*")

    sound = diag_ok and modulus_ok and herm_ok
    details_parts: List[str] = []
    if diag_errors:
        details_parts.append(f"Diagonal errors (first 3): {diag_errors[:3]}")
    if modulus_errors:
        details_parts.append(f"Modulus errors (first 3): {modulus_errors[:3]}")
    if herm_errors:
        details_parts.append(f"Hermitian errors (first 3): {herm_errors[:3]}")

    return GramianStructureReport(
        diagonal_blocks_identity=diag_ok,
        off_diagonal_blocks_modulus_sixth=modulus_ok,
        hermitian_exact=herm_ok,
        verified_sound=sound,
        dimension=GRAMIAN_DIM,
        bases_count=NUM_BASES,
        details="; ".join(details_parts) if details_parts else "All block structure requirements verified."
    )


# ==============================================================================
# Exact LDL^T Decomposition & PSD Verification
# ==============================================================================

def ldlt_pivots_rational(m: Sequence[Sequence[Cyc24]]) -> List[Fraction]:
    """Exact rational LDL^T pivots of a Hermitian matrix over Q(zeta_24).
    
    Replicates the exact semantics of `omega_native::mub6_quad_sdp::ldlt_pivots_rational`:
    - Checks matrix is square, non-empty, and Hermitian.
    - Requires all diagonal pivots to be in Q (via `exact_rational`).
    - Requires pivots to be non-negative; raises ValueError on negative pivot.
    - Verifies rank-deficiency condition on zero pivot (remaining row/col must vanish).
    - Returns list of exact rational pivots.
    """
    n = len(m)
    if n == 0 or any(len(row) != n for row in m):
        raise ValueError("expected a nonempty square matrix")

    for i in range(n):
        for j in range(n):
            if m[i][j] != m[j][i].conj():
                raise ValueError(f"matrix is not Hermitian at ({i}, {j})")

    a: List[List[Cyc24]] = [[m[i][j] for j in range(n)] for i in range(n)]
    pivots: List[Fraction] = []

    for k in range(n):
        piv_cyc = a[k][k]
        piv_rat = exact_rational(piv_cyc)
        pivots.append(piv_rat)

        if piv_rat < 0:
            raise ValueError(f"Negative pivot at step {k}: {piv_rat}")

        if piv_rat == 0:
            # Check rank-deficient direction: whole remaining row/col must vanish
            for i in range(k + 1, n):
                if not a[k][i].is_zero() or not a[i][k].is_zero():
                    raise ValueError(f"Indefinite 2x2 minor at step {k}")
            continue

        piv_inv = Cyc24.rat(Fraction(1, piv_rat))
        for i in range(k + 1, n):
            if a[i][k].is_zero():
                continue
            factor = a[i][k].mul(piv_inv)
            for j in range(k, n):
                delta = factor.mul(a[k][j])
                a[i][j] = a[i][j].sub(delta)

    return pivots


def ldlt_decomposition_cyc(
    A: Sequence[Sequence[Cyc24]],
) -> Tuple[List[List[Cyc24]], List[Fraction], bool]:
    """Exact rational LDL^dagger decomposition of a Hermitian matrix over Q(zeta_24).
    
    Returns (L, D, is_psd) where:
    - L is unit lower triangular matrix over Q(zeta_24).
    - D is list of rational pivots in Q.
    - is_psd is True iff all d_k >= 0.
    
    Satisfies A = L * D * L^dagger exactly.
    """
    n = len(A)
    L = [[Cyc24.one() if i == j else Cyc24.zero() for j in range(n)] for i in range(n)]
    D_list = [Fraction(0) for _ in range(n)]
    A_copy = [[A[i][j] for j in range(n)] for i in range(n)]

    for j in range(n):
        sum_prev = Cyc24.zero()
        for k in range(j):
            sum_prev = sum_prev.add(L[j][k].mul(L[j][k].conj()).mul_rat(D_list[k]))
        piv_cyc = A_copy[j][j].sub(sum_prev)
        try:
            piv_rat = exact_rational(piv_cyc)
        except ValueError:
            return L, D_list, False
        D_list[j] = piv_rat

        if piv_rat < 0:
            return L, D_list, False
        elif piv_rat == 0:
            for i in range(j + 1, n):
                s = Cyc24.zero()
                for k in range(j):
                    s = s.add(L[i][k].mul(L[j][k].conj()).mul_rat(D_list[k]))
                if not A_copy[i][j].sub(s).is_zero():
                    return L, D_list, False
        else:
            inv_piv = Fraction(1, piv_rat)
            for i in range(j + 1, n):
                s = Cyc24.zero()
                for k in range(j):
                    s = s.add(L[i][k].mul(L[j][k].conj()).mul_rat(D_list[k]))
                L[i][j] = A_copy[i][j].sub(s).mul_rat(inv_piv)

    is_psd = all(d >= 0 for d in D_list)
    return L, D_list, is_psd


def is_psd_cyc(G: Sequence[Sequence[Cyc24]]) -> bool:
    """Return True iff Hermitian matrix G over Q(zeta_24) is positive semidefinite."""
    n = len(G)
    for i in range(n):
        for j in range(n):
            if G[i][j] != G[j][i].conj():
                return False
    _, _, psd = ldlt_decomposition_cyc(G)
    return psd


# ==============================================================================
# Dual Witness Matrix W = L D L^dagger & Trace Inner Product
# ==============================================================================

class DualWitnessCyc:
    """Factored dual witness matrix W = L * D * L^dagger over Q(zeta_24) with D in Q."""

    def __init__(self, L: Sequence[Sequence[Cyc24]], D_diag: Sequence[Fraction | int]):
        self.n = len(L)
        self.m = len(D_diag)
        if any(len(row) != self.m for row in L):
            raise ValueError(f"L matrix dimensions must be {self.n} x {self.m}")
        self.L = [[Cyc24(entry.coeffs) for entry in row] for row in L]
        self.D_diag = [Fraction(x) for x in D_diag]
        assert_no_float(self.D_diag, "DualWitnessCyc.D_diag")

    def is_valid(self) -> bool:
        """A dual witness W >= 0 is valid iff all diagonal pivots D_k >= 0."""
        return all(d >= 0 for d in self.D_diag)

    def to_full_matrix(self) -> List[List[Cyc24]]:
        """Construct full matrix W_ij = sum_k L_ik * D_k * conj(L_jk)."""
        W = [[Cyc24.zero() for _ in range(self.n)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                acc = Cyc24.zero()
                for k in range(self.m):
                    term = self.L[i][k].mul(self.L[j][k].conj()).mul_rat(self.D_diag[k])
                    acc = acc.add(term)
                W[i][j] = acc
        return W

    def trace_inner(self, G: Sequence[Sequence[Cyc24]]) -> Cyc24:
        """Compute Tr(W * G) = sum_k D_k * (L[:, k]^dagger * G * L[:, k]).
        
        Factored computation directly matching Lean 4 CandidateGramPositivity:
        Tr(W · G) = ∑_k D_k ‖∑_i L_{ik} v_i‖² ≥ 0 for any valid Gramian.
        """
        if len(G) != self.n or any(len(row) != self.n for row in G):
            raise ValueError(f"Matrix dimension does not match witness dimension {self.n}")
        acc = Cyc24.zero()
        for k in range(self.m):
            col_k = [self.L[i][k] for i in range(self.n)]
            # Quadratic form: col_k^dagger * G * col_k
            q = Cyc24.zero()
            for i in range(self.n):
                for j in range(self.n):
                    q = q.add(col_k[i].conj().mul(G[i][j]).mul(col_k[j]))
            acc = acc.add(q.mul_rat(self.D_diag[k]))
        return acc


def trace_inner_product(w: Sequence[Sequence[Cyc24]], g: Sequence[Sequence[Cyc24]]) -> Cyc24:
    """Compute Tr(W * G) = sum_{i,j} W_{ij} * G_{ji} for full matrices."""
    n = len(w)
    if len(g) != n or any(len(row) != n for row in g) or any(len(row) != n for row in w):
        raise ValueError("Matrix dimension mismatch in trace_inner_product")
    acc = Cyc24.zero()
    for i in range(n):
        for j in range(n):
            acc = acc.add(w[i][j].mul(g[j][i]))
    return acc


def dual_witness_vector() -> List[Cyc24]:
    """Construct the canonical 24-dimensional dual witness vector v from mub6_quad_sdp.rs.
    
    Structure:
    - Block 0 (indices 0..5): all 0
    - Block 1 (indices 6..11): [-3, 1, -2, -2, 2, 1]
    - Block 2 (indices 12..17): [-3, 1, 1, -1, 3, 3]
    - Block 3 (indices 18..23): sqrt(6) * [-1, 1, 1, 1, 1, 1]
    
    Exact squared norm ||v||^2 = 0 + 23 + 30 + 36 = 89.
    """
    v = [Cyc24.zero() for _ in range(GRAMIAN_DIM)]

    # Block 1
    v1_int = (-3, 1, -2, -2, 2, 1)
    for i, val in enumerate(v1_int):
        v[DIM_HILBERT + i] = Cyc24.rat(val)

    # Block 2
    v2_int = (-3, 1, 1, -1, 3, 3)
    for i, val in enumerate(v2_int):
        v[2 * DIM_HILBERT + i] = Cyc24.rat(val)

    # Block 3: sqrt(6) * u3
    s6 = sqrt6_cyc()
    v3_int = (-1, 1, 1, 1, 1, 1)
    for i, val in enumerate(v3_int):
        v[3 * DIM_HILBERT + i] = s6.mul_rat(val)

    return v


def dual_certificate_matrix(strict: bool = False) -> List[List[Cyc24]]:
    """Construct the canonical dual witness matrix W = v * v^dagger (+ eps * I if strict).
    
    - If strict=False: Rank-1 PSD witness W = v * v^dagger with Tr(W * G) = -7.
    - If strict=True: Strictly positive definite witness W = v * v^dagger + (1/24) * I_24
      with Tr(W * G) = -7 + (1/24)*24 = -6.
    """
    v = dual_witness_vector()
    w = [[v[i].mul(v[j].conj()) for j in range(GRAMIAN_DIM)] for i in range(GRAMIAN_DIM)]

    if strict:
        eps = Cyc24.rat(Fraction(1, 24))
        for i in range(GRAMIAN_DIM):
            w[i][i] = w[i][i].add(eps)

    return w


# ==============================================================================
# Full MubQuadSdpCertificate & Solver
# ==============================================================================

@dataclass(frozen=True)
class MubQuadSdpCertificate:
    """Full exact verification certificate for the 24x24 Gramian matrix.
    
    Matches schema 'omega.mub.quad-sdp.v2' from omega_native::mub6_quad_sdp.
    """
    schema_version: str
    dimension: int
    bases_count: int
    gramian_dim: int
    gramian_structure: GramianStructureReport
    rank1_inner_product: str
    rank1_inner_product_num: str
    rank1_inner_product_den: str
    rank1_strictly_negative: bool
    strict_inner_product: str
    strict_inner_product_num: str
    strict_inner_product_den: str
    strict_strictly_negative: bool
    strict_regularizer: str
    rank1_pivots: List[str]
    rank1_pivots_nonnegative: bool
    strict_pivots: List[str]
    strict_pivots_strictly_positive: bool
    dual_certificate_psd_certified: bool
    fixed_matrix_witness_checked: bool
    constructed_matrix_not_psd: bool
    complete: bool
    scope: str
    mub_nonexistence_established: bool
    firewall: str
    authority_effect: str
    sha256_digest: Optional[str] = None


def solve_quad_sdp_certificate() -> MubQuadSdpCertificate:
    """Generate the full exact rational/cyclotomic certificate solving the quad SDP problem.
    
    Verifies:
    1. Exact 24x24 Gramian structure (diagonal identity, off-diagonal modulus 1/6, Hermitian).
    2. Rank-1 dual witness PSD certification and Tr(W_rank1 * G) = -7 < 0.
    3. Strict dual witness positive-definiteness certification and Tr(W_strict * G) = -6 < 0.
    4. Logical contradiction: W >= 0 and Tr(W * G) < 0 implies G is NOT positive semidefinite.
    """
    g = canonical_quad_gramian()
    struct_report = verify_gramian_structure(g)

    w_rank1 = dual_certificate_matrix(strict=False)
    w_strict = dual_certificate_matrix(strict=True)

    inner_rank1 = trace_inner_product(w_rank1, g)
    inner_strict = trace_inner_product(w_strict, g)

    rat_rank1 = exact_rational(inner_rank1)
    rat_strict = exact_rational(inner_strict)

    rank1_neg = rat_rank1 < Fraction(0)
    strict_neg = rat_strict < Fraction(0)

    # Verify LDL^T pivots
    rank1_pivots = ldlt_pivots_rational(w_rank1)
    rank1_all_nonneg = all(p >= Fraction(0) for p in rank1_pivots)

    strict_pivots = ldlt_pivots_rational(w_strict)
    strict_all_pos = all(p > Fraction(0) for p in strict_pivots)

    psd_ok = rank1_all_nonneg and strict_all_pos
    contradiction = psd_ok and rank1_neg and strict_neg and struct_report.verified_sound

    cert = MubQuadSdpCertificate(
        schema_version=SCHEMA_VERSION,
        dimension=DIM_HILBERT,
        bases_count=NUM_BASES,
        gramian_dim=GRAMIAN_DIM,
        gramian_structure=struct_report,
        rank1_inner_product=str(rat_rank1),
        rank1_inner_product_num=str(rat_rank1.numerator),
        rank1_inner_product_den=str(rat_rank1.denominator),
        rank1_strictly_negative=rank1_neg,
        strict_inner_product=str(rat_strict),
        strict_inner_product_num=str(rat_strict.numerator),
        strict_inner_product_den=str(rat_strict.denominator),
        strict_strictly_negative=strict_neg,
        strict_regularizer="1/24",
        rank1_pivots=[str(p) for p in rank1_pivots],
        rank1_pivots_nonnegative=rank1_all_nonneg,
        strict_pivots=[str(p) for p in strict_pivots],
        strict_pivots_strictly_positive=strict_all_pos,
        dual_certificate_psd_certified=psd_ok,
        fixed_matrix_witness_checked=contradiction,
        constructed_matrix_not_psd=contradiction,
        complete=contradiction,
        scope=SCOPE_STRING,
        mub_nonexistence_established=False,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
        sha256_digest=None,
    )
    assert_no_float(cert, "MubQuadSdpCertificate")
    return cert


def verify_dual_obstruction_cyc(
    witness: DualWitnessCyc,
    candidate_evals: Sequence[List[List[Cyc24]]],
) -> Tuple[bool, str]:
    """Verify regional dual obstruction Tr(W * G) < 0 on a set of candidate Gram matrices.
    
    Strictly requires witness.is_valid() (D >= 0).
    """
    if not witness.is_valid():
        return False, "Dual witness validation failed: D has negative eigenvalues"

    if not candidate_evals:
        return False, "Empty candidate evaluations"

    traces: List[Fraction] = []
    for G in candidate_evals:
        tr = witness.trace_inner(G)
        tr_rat = exact_rational(tr)
        traces.append(tr_rat)

    max_trace = max(traces)
    if max_trace < Fraction(0):
        return True, f"Obstruction certified: max Tr(W * G) = {max_trace} < 0"
    else:
        return False, f"Obstruction not certified: max Tr(W * G) = {max_trace} >= 0"
