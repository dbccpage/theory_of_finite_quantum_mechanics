"""Target Q3: experimental rational coefficient-matrix diagnostics.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority.

The proposed lifts are not validated projector moment matrices. They fail a
repeated-standard-basis positivity control, and their real cyclotomic terms need
not be rational. Diagnostic builders explicitly project onto the constant
power-basis coefficient. This is not an ordered-field embedding or a
positivity-preserving map. Negative traces concern only the constructed rational
matrices; they do not certify a candidate or a Lasserre relaxation.
The former certification entry points fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .cyclotomic import Cyc24
from .mub_triples import (
    inner_product as cyc_inner_product,
)
from .target_a4_gram_certifier import (
    DIM_HILBERT,
    NUM_BASES,
    GRAMIAN_DIM,
    canonical_quad_gramian,
    canonical_triple_exact,
    exact_rational,
)

SCHEMA_VERSION: str = "omega.mub.degree6-diagnostics.v2"
FIREWALL_LINE: str = "stated region only; mints no authority"
AUTHORITY_EFFECT: str = "None"
SCOPE_STRING: str = "experimental_coefficient_projection_only_no_moment_soundness"

DEG6_INVARIANT_DIM: int = 21
DEG6_EXTENDED_DIM: int = 35


def _require_exact(value: Any) -> Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError(f"Expected exact integer or Fraction, got {type(value).__name__}: {value}")
    return Fraction(value)



def assert_no_float(obj: Any, path: str = "root") -> None:
    """Recursively verify that no float or complex types exist in any data structure."""
    if isinstance(obj, (float, complex)):
        raise TypeError(
            f"Zero Float Violation: Found {type(obj).__name__} at '{path}': {obj}. "
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



def ldlt_decomposition_rational(
    m: Sequence[Sequence[Fraction]],
) -> Tuple[List[List[Fraction]], List[Fraction], bool]:
    """Exact rational LDL^T decomposition of a real symmetric matrix over Fraction.

    If is_psd is True, M = L * diag(D) * L^T. On rejection L and D
    may be partial and are not a decomposition certificate.
    """
    n = len(m)
    if n == 0 or any(len(row) != n for row in m):
        raise ValueError("Matrix must be non-empty and square")

    m = [[_require_exact(value) for value in row] for row in m]

    for i in range(n):
        for j in range(i + 1, n):
            if m[i][j] != m[j][i]:
                raise ValueError(f"Matrix is not symmetric at ({i}, {j}): {m[i][j]} != {m[j][i]}")

    L = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    D = [Fraction(0) for _ in range(n)]
    a = [[m[i][j] for j in range(n)] for i in range(n)]

    for j in range(n):
        sum_prev = Fraction(0)
        for k in range(j):
            sum_prev += L[j][k] * L[j][k] * D[k]
        piv = a[j][j] - sum_prev
        D[j] = piv

        if piv < 0:
            return L, D, False
        elif piv == 0:
            for i in range(j + 1, n):
                s = Fraction(0)
                for k in range(j):
                    s += L[i][k] * L[j][k] * D[k]
                if a[i][j] - s != 0:
                    return L, D, False
        else:
            inv_piv = Fraction(1, piv)
            for i in range(j + 1, n):
                s = Fraction(0)
                for k in range(j):
                    s += L[i][k] * L[j][k] * D[k]
                L[i][j] = (a[i][j] - s) * inv_piv

    is_psd = all(d >= 0 for d in D)
    return L, D, is_psd


def ldlt_pivots_strictly_positive(
    m: Sequence[Sequence[Fraction]],
) -> List[Fraction]:
    """Compute exact rational LDL^T pivots and verify that every pivot is strictly positive (> 0)."""
    _, pivots, is_psd = ldlt_decomposition_rational(m)
    if not is_psd or any(p <= 0 for p in pivots):
        for step, p in enumerate(pivots):
            if p <= 0:
                raise ValueError(f"Pivot at step {step} is not strictly positive: {p}")
    return pivots



def get_basis_pairs() -> List[Tuple[int, int]]:
    """Return the 6 lexicographically ordered basis pairs (a, b) with 0 <= a < b < 4."""
    pairs: List[Tuple[int, int]] = []
    for a in range(NUM_BASES):
        for b in range(a + 1, NUM_BASES):
            pairs.append((a, b))
    return pairs


def get_basis_triples() -> List[Tuple[int, int, int]]:
    """Return the 4 lexicographically ordered basis triples (a, b, c) with 0 <= a < b < c < 4."""
    triples: List[Tuple[int, int, int]] = []
    for a in range(NUM_BASES):
        for b in range(a + 1, NUM_BASES):
            for c in range(b + 1, NUM_BASES):
                triples.append((a, b, c))
    return triples



def cyc_real_rational(z: Cyc24) -> Fraction:
    """Return Re(z) only when it lies in Q; reject non-rational components."""
    _validate_cyclotomic(z)
    return exact_rational(z.add(z.conj()).mul_rat(Fraction(1, 2)))


def _validate_cyclotomic(z: Cyc24) -> None:
    if not isinstance(z, Cyc24) or len(z.coeffs) != 8:
        raise TypeError("Expected an exact Cyc24 value")
    for coefficient in z.coeffs:
        _require_exact(coefficient)


def cyc_real_constant_coefficient(z: Cyc24) -> Fraction:
    """Project Re(z) to its constant coefficient; this discards other terms."""
    _validate_cyclotomic(z)
    re = z.add(z.conj()).mul_rat(Fraction(1, 2))
    return re.coeffs[0]


def _validate_gramian_matrix(g: Sequence[Sequence[Cyc24]], dim: int) -> None:
    if len(g) != dim or any(len(row) != dim for row in g):
        raise ValueError(f"Gramian dimension must be {dim}x{dim}")
    for row in g:
        for entry in row:
            _validate_cyclotomic(entry)
    if any(g[i][j] != g[j][i].conj() for i in range(dim) for j in range(dim)):
        raise ValueError("Input matrix must be Hermitian")


def _populate_linear_projector_sums(m6: List[List[Fraction]], g: Sequence[Sequence[Cyc24]]) -> None:
    m6[0][0] = Fraction(1)
    for a in range(NUM_BASES):
        idx_a = 1 + a
        m6[0][idx_a] = Fraction(1)
        m6[idx_a][0] = Fraction(1)
        m6[idx_a][idx_a] = Fraction(1)

    for a in range(NUM_BASES):
        for b in range(a + 1, NUM_BASES):
            idx_a = 1 + a
            idx_b = 1 + b
            sum_mod_sq = Fraction(0)
            for i in range(DIM_HILBERT):
                for j in range(DIM_HILBERT):
                    entry = g[a * DIM_HILBERT + i][b * DIM_HILBERT + j]
                    sum_mod_sq += exact_rational(entry.abs_sq())
            val = Fraction(1, 6) * sum_mod_sq
            m6[idx_a][idx_b] = val
            m6[idx_b][idx_a] = val


def _populate_pairs_and_cross_terms(
    m6: List[List[Fraction]],
    g: Sequence[Sequence[Cyc24]],
    pairs: Sequence[Tuple[int, int]],
) -> None:
    for p_idx, (a, b) in enumerate(pairs):
        idx_p = 5 + p_idx
        idx_q = 11 + p_idx

        diag_mod_sq = Fraction(0)
        off_mod_sq = Fraction(0)
        for i in range(DIM_HILBERT):
            entry_diag = g[a * DIM_HILBERT + i][b * DIM_HILBERT + i]
            diag_mod_sq += exact_rational(entry_diag.abs_sq())
            for j in range(DIM_HILBERT):
                if i != j:
                    entry_off = g[a * DIM_HILBERT + i][b * DIM_HILBERT + j]
                    off_mod_sq += exact_rational(entry_off.abs_sq())

        exp_p = Fraction(1, 6) * diag_mod_sq
        exp_q = Fraction(1, 6) * off_mod_sq

        m6[0][idx_p] = exp_p
        m6[idx_p][0] = exp_p
        m6[0][idx_q] = exp_q
        m6[idx_q][0] = exp_q

        m6[1 + a][idx_p] = exp_p
        m6[idx_p][1 + a] = exp_p
        m6[1 + b][idx_p] = exp_p
        m6[idx_p][1 + b] = exp_p

        m6[1 + a][idx_q] = exp_q
        m6[idx_q][1 + a] = exp_q
        m6[1 + b][idx_q] = exp_q
        m6[idx_q][1 + b] = exp_q

        for c in range(NUM_BASES):
            if c != a and c != b:
                m6[1 + c][idx_p] = exp_p
                m6[idx_p][1 + c] = exp_p
                m6[1 + c][idx_q] = exp_q
                m6[idx_q][1 + c] = exp_q

        m6[idx_p][idx_p] = exp_p
        m6[idx_q][idx_q] = exp_q

    for p1, (a, b) in enumerate(pairs):
        for p2, (c, d) in enumerate(pairs):
            if p1 < p2:
                idx1 = 5 + p1
                idx2 = 5 + p2
                val = Fraction(0)
                for i in range(DIM_HILBERT):
                    e_ab = g[a * DIM_HILBERT + i][b * DIM_HILBERT + i]
                    e_cd = g[c * DIM_HILBERT + i][d * DIM_HILBERT + i]
                    prod = e_ab.mul(e_cd.conj())
                    val += cyc_real_constant_coefficient(prod)
                cross_val = Fraction(1, 6) * val
                m6[idx1][idx2] = cross_val
                m6[idx2][idx1] = cross_val


def _populate_triples_and_cross_terms(
    m6: List[List[Fraction]],
    g: Sequence[Sequence[Cyc24]],
    pairs: Sequence[Tuple[int, int]],
    triples: Sequence[Tuple[int, int, int]],
) -> None:
    for t_idx, (a, b, c) in enumerate(triples):
        idx_t = 17 + t_idx

        bargmann_sum = Fraction(0)
        diag_cubed_sum = Fraction(0)
        for i in range(DIM_HILBERT):
            e_ab = g[a * DIM_HILBERT + i][b * DIM_HILBERT + i]
            e_bc = g[b * DIM_HILBERT + i][c * DIM_HILBERT + i]
            e_ca = g[c * DIM_HILBERT + i][a * DIM_HILBERT + i]
            cycle = e_ab.mul(e_bc).mul(e_ca)
            bargmann_sum += cyc_real_constant_coefficient(cycle)

            mod_sq = exact_rational(e_ab.abs_sq()) * exact_rational(e_bc.abs_sq()) * exact_rational(e_ca.abs_sq())
            diag_cubed_sum += mod_sq

        exp_t = Fraction(1, 6) * bargmann_sum
        exp_t_diag = Fraction(1, 6) * diag_cubed_sum

        m6[0][idx_t] = exp_t
        m6[idx_t][0] = exp_t

        for d in range(NUM_BASES):
            m6[1 + d][idx_t] = exp_t
            m6[idx_t][1 + d] = exp_t

        for p_idx, (p_a, p_b) in enumerate(pairs):
            idx_p = 5 + p_idx
            idx_q = 11 + p_idx
            if (p_a in (a, b, c)) and (p_b in (a, b, c)):
                m6[idx_p][idx_t] = exp_t
                m6[idx_t][idx_p] = exp_t
            else:
                m6[idx_p][idx_t] = Fraction(0)
                m6[idx_t][idx_p] = Fraction(0)

            m6[idx_q][idx_t] = exp_t - m6[idx_p][idx_t]
            m6[idx_t][idx_q] = m6[idx_q][idx_t]

        m6[idx_t][idx_t] = exp_t_diag if exp_t_diag > 0 else exp_t

    for t1, (a1, b1, c1) in enumerate(triples):
        for t2, (a2, b2, c2) in enumerate(triples):
            if t1 < t2:
                idx1 = 17 + t1
                idx2 = 17 + t2
                cross_val = Fraction(0)
                for i in range(DIM_HILBERT):
                    c1_val = (g[a1 * DIM_HILBERT + i][b1 * DIM_HILBERT + i]
                              .mul(g[b1 * DIM_HILBERT + i][c1 * DIM_HILBERT + i])
                              .mul(g[c1 * DIM_HILBERT + i][a1 * DIM_HILBERT + i]))
                    c2_val = (g[a2 * DIM_HILBERT + i][b2 * DIM_HILBERT + i]
                              .mul(g[b2 * DIM_HILBERT + i][c2 * DIM_HILBERT + i])
                              .mul(g[c2 * DIM_HILBERT + i][a2 * DIM_HILBERT + i]))
                    prod = c1_val.mul(c2_val.conj())
                    cross_val += cyc_real_constant_coefficient(prod)
                val = Fraction(1, 6) * cross_val
                m6[idx1][idx2] = val
                m6[idx2][idx1] = val


def build_degree6_invariant_diagnostic_matrix(
    g: Sequence[Sequence[Cyc24]],
) -> List[List[Fraction]]:
    """Construct the experimental 21x21 rational coefficient matrix."""
    _validate_gramian_matrix(g, GRAMIAN_DIM)
    pairs = get_basis_pairs()
    triples = get_basis_triples()
    n = DEG6_INVARIANT_DIM
    m6 = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    _populate_linear_projector_sums(m6, g)
    _populate_pairs_and_cross_terms(m6, g, pairs)
    _populate_triples_and_cross_terms(m6, g, pairs, triples)

    assert_no_float(m6, "build_degree6_invariant_diagnostic_matrix.m6")
    return m6


def _populate_extended_single_projectors(m6: List[List[Fraction]], g: Sequence[Sequence[Cyc24]]) -> None:
    m6[0][0] = Fraction(1)
    for a in range(NUM_BASES):
        for i in range(DIM_HILBERT):
            idx = 1 + a * DIM_HILBERT + i
            m6[0][idx] = Fraction(1, 6)
            m6[idx][0] = Fraction(1, 6)
            m6[idx][idx] = Fraction(1, 6)

    for a in range(NUM_BASES):
        for i in range(DIM_HILBERT):
            idx_a = 1 + a * DIM_HILBERT + i
            for b in range(NUM_BASES):
                for j in range(DIM_HILBERT):
                    idx_b = 1 + b * DIM_HILBERT + j
                    if a == b and i != j:
                        m6[idx_a][idx_b] = Fraction(0)
                    elif a != b:
                        entry = g[a * DIM_HILBERT + i][b * DIM_HILBERT + j]
                        val = Fraction(1, 6) * exact_rational(entry.abs_sq())
                        m6[idx_a][idx_b] = val


def _populate_extended_pairs(m6: List[List[Fraction]], g: Sequence[Sequence[Cyc24]], pairs: Sequence[Tuple[int, int]]) -> None:
    for p_idx, (a, b) in enumerate(pairs):
        col_p = 25 + p_idx
        diag_mod_sq = Fraction(0)
        for i in range(DIM_HILBERT):
            entry = g[a * DIM_HILBERT + i][b * DIM_HILBERT + i]
            mod_sq = exact_rational(entry.abs_sq())
            diag_mod_sq += mod_sq
            m6[a * DIM_HILBERT + i + 1][col_p] = Fraction(1, 6) * mod_sq
            m6[col_p][a * DIM_HILBERT + i + 1] = Fraction(1, 6) * mod_sq
            m6[b * DIM_HILBERT + i + 1][col_p] = Fraction(1, 6) * mod_sq
            m6[col_p][b * DIM_HILBERT + i + 1] = Fraction(1, 6) * mod_sq

        exp_p = Fraction(1, 6) * diag_mod_sq
        m6[0][col_p] = exp_p
        m6[col_p][0] = exp_p
        m6[col_p][col_p] = exp_p


def _populate_extended_triples(m6: List[List[Fraction]], g: Sequence[Sequence[Cyc24]], triples: Sequence[Tuple[int, int, int]]) -> None:
    for t_idx, (a, b, c) in enumerate(triples):
        col_t = 31 + t_idx
        bargmann_sum = Fraction(0)
        for i in range(DIM_HILBERT):
            e_ab = g[a * DIM_HILBERT + i][b * DIM_HILBERT + i]
            e_bc = g[b * DIM_HILBERT + i][c * DIM_HILBERT + i]
            e_ca = g[c * DIM_HILBERT + i][a * DIM_HILBERT + i]
            cycle = e_ab.mul(e_bc).mul(e_ca)
            c_val = cyc_real_constant_coefficient(cycle)
            bargmann_sum += c_val
            m6[a * DIM_HILBERT + i + 1][col_t] = Fraction(1, 6) * c_val
            m6[col_t][a * DIM_HILBERT + i + 1] = Fraction(1, 6) * c_val
            m6[b * DIM_HILBERT + i + 1][col_t] = Fraction(1, 6) * c_val
            m6[col_t][b * DIM_HILBERT + i + 1] = Fraction(1, 6) * c_val
            m6[c * DIM_HILBERT + i + 1][col_t] = Fraction(1, 6) * c_val
            m6[col_t][c * DIM_HILBERT + i + 1] = Fraction(1, 6) * c_val

        exp_t = Fraction(1, 6) * bargmann_sum
        m6[0][col_t] = exp_t
        m6[col_t][0] = exp_t
        m6[col_t][col_t] = exp_t if exp_t > 0 else Fraction(0)


def build_degree6_extended_diagnostic_matrix(
    g: Sequence[Sequence[Cyc24]],
) -> List[List[Fraction]]:
    """Construct the experimental 35x35 rational coefficient matrix."""
    _validate_gramian_matrix(g, GRAMIAN_DIM)
    pairs = get_basis_pairs()
    triples = get_basis_triples()
    n = DEG6_EXTENDED_DIM
    m6 = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    _populate_extended_single_projectors(m6, g)
    _populate_extended_pairs(m6, g, pairs)
    _populate_extended_triples(m6, g, triples)

    assert_no_float(m6, "build_degree6_extended_diagnostic_matrix.m6")
    return m6



@dataclass(frozen=True)
class DualWitnessRational:
    """Exact rational positive semidefinite dual certificate W = sum_i w_i z_i z_i^T."""
    dim: int
    num_modes: int
    vectors: List[List[Fraction]]
    weights: List[Fraction]

    def __post_init__(self) -> None:
        assert_no_float(self, "DualWitnessRational")
        self._validate()

    def _validate(self) -> None:
        if type(self.dim) is not int or type(self.num_modes) is not int:
            raise TypeError("Dimensions must be integers")
        if self.dim <= 0 or self.num_modes <= 0:
            raise ValueError("Dimensions must be positive")
        if len(self.vectors) != self.num_modes or len(self.weights) != self.num_modes:
            raise ValueError("Inconsistent number of modes")
        for vector in self.vectors:
            if len(vector) != self.dim:
                raise ValueError("Witness vector dimension mismatch")
            for value in vector:
                _require_exact(value)
        for idx, w in enumerate(self.weights):
            _require_exact(w)
            if w <= 0:
                raise ValueError(f"Weight {idx} must be strictly positive: {w}")

    def to_matrix(self) -> List[List[Fraction]]:
        """Materialize exact rational symmetric matrix W."""
        self._validate()
        w_mat = [[Fraction(0) for _ in range(self.dim)] for _ in range(self.dim)]
        for k in range(self.num_modes):
            w_k = self.weights[k]
            z_k = self.vectors[k]
            for i in range(self.dim):
                zi = z_k[i]
                if zi != 0:
                    for j in range(self.dim):
                        zj = z_k[j]
                        if zj != 0:
                            w_mat[i][j] += w_k * zi * zj
        return w_mat

    def to_full_matrix(self) -> List[List[Fraction]]:
        """Alias for to_matrix for compatibility."""
        return self.to_matrix()

    def trace_inner(self, m: Sequence[Sequence[Fraction]]) -> Fraction:
        """Exact rational trace inner product Tr(W * M) = sum_k w_k (z_k^T M z_k)."""
        self._validate()
        if len(m) != self.dim or any(len(row) != self.dim for row in m):
            raise ValueError("Matrix dimension mismatch")
        m = [[_require_exact(value) for value in row] for row in m]
        if any(m[i][j] != m[j][i] for i in range(self.dim) for j in range(self.dim)):
            raise ValueError("Matrix must be symmetric")
        total = Fraction(0)
        for k in range(self.num_modes):
            w_k = self.weights[k]
            z_k = self.vectors[k]
            quad = Fraction(0)
            for i in range(self.dim):
                zi = z_k[i]
                if zi != 0:
                    for j in range(self.dim):
                        zj = z_k[j]
                        if zj != 0:
                            quad += zi * zj * m[i][j]
            total += w_k * quad
        return total


def build_invariant_dual_witness_x0(strict: bool = True) -> DualWitnessRational:
    """Construct a PSD weight matrix for the experimental X=0 coefficient matrix.

    Evaluated on the experimental 21x21 coefficient matrix for G_{diag}.
    Vector z:
    - z[0] = -1
    - z[1] = 1 (A_0)
    - z[4] = 1 (A_3)
    - z[17..20] = 0 (triples)

    z^T M_6(X=0) z = -1.
    For strict=True, regularize with eps * I_21 where eps = 1/50:
    Tr(W_strict * M_6) = -9071/10800 for this coefficient fixture.
    """
    z = [Fraction(0) for _ in range(DEG6_INVARIANT_DIM)]
    z[0] = Fraction(-1)
    z[1] = Fraction(1)
    z[4] = Fraction(1)

    vectors = [z]
    weights = [Fraction(1)]

    if strict:
        eps = Fraction(1, 50)
        for i in range(DEG6_INVARIANT_DIM):
            e = [Fraction(0) for _ in range(DEG6_INVARIANT_DIM)]
            e[i] = Fraction(1)
            vectors.append(e)
            weights.append(eps)

    return DualWitnessRational(
        dim=DEG6_INVARIANT_DIM,
        num_modes=len(vectors),
        vectors=vectors,
        weights=weights,
    )


def build_extended_dual_witness_s6(strict: bool = True) -> DualWitnessRational:
    """Construct a PSD weight matrix for the experimental S6 coefficient matrix.

    Evaluated on the experimental 35x35 coefficient matrix for G_{synth}.
    Vector z:
    - z[0] = 12
    - z[1..24] = -2 (single projectors Pi_{a, i})
    - z[25..30] = -5 (diagonal pair projectors P_{ab})
    - z[31..34] = 0 (triples T_{abc})

    z^T M_6 z = -39.
    For strict=True, regularize with (1/100) * I_35:
    Tr(W_strict * M_6) = -140183/3600 for this coefficient fixture.
    """
    z = [Fraction(0) for _ in range(DEG6_EXTENDED_DIM)]
    z[0] = Fraction(12)
    for i in range(1, 25):
        z[i] = Fraction(-2)
    for p in range(25, 31):
        z[p] = Fraction(-5)

    vectors = [z]
    weights = [Fraction(1)]

    if strict:
        eps = Fraction(1, 100)
        for i in range(DEG6_EXTENDED_DIM):
            e = [Fraction(0) for _ in range(DEG6_EXTENDED_DIM)]
            e[i] = Fraction(1)
            vectors.append(e)
            weights.append(eps)

    return DualWitnessRational(
        dim=DEG6_EXTENDED_DIM,
        num_modes=len(vectors),
        vectors=vectors,
        weights=weights,
    )



@dataclass(frozen=True)
class DualWitnessReceipt:
    """Exact trace and positive-pivot diagnostics for a specified rational matrix."""
    target_description: str
    witness_dimension: int
    inner_product: str
    inner_product_num: str
    inner_product_den: str
    strictly_negative: bool
    pivots_strictly_positive: bool
    pivots: List[str]


@dataclass(frozen=True)
class Degree6MomentReport:
    """Report on the experimental coefficient matrices; no candidate refutations."""
    invariant_dimension: int
    extended_dimension: int
    candidate_x0_refuted: bool
    candidate_s6_refuted: bool
    details: str


@dataclass(frozen=True)
class Degree6DiagnosticReport:
    """Diagnostic receipt; complete and moment_semantics_verified remain false."""
    schema_version: str
    firewall: str
    authority_effect: str
    scope: str
    dimension: int
    bases_count: int
    invariant_dim: int
    extended_dim: int
    moment_report: Degree6MomentReport
    receipt_x0: DualWitnessReceipt
    receipt_s6: DualWitnessReceipt
    complete: bool
    diagnostics_complete: bool
    moment_semantics_verified: bool


def build_block_diagonal_gramian() -> List[List[Cyc24]]:
    """Construct the block-diagonal Gramian G_diag = diag(G_triple, I_6) with X = 0."""
    cols = canonical_triple_exact()
    g = [[Cyc24.zero() for _ in range(GRAMIAN_DIM)] for _ in range(GRAMIAN_DIM)]

    for a in range(3):
        for b in range(3):
            for i in range(DIM_HILBERT):
                for j in range(DIM_HILBERT):
                    u = cols[a * DIM_HILBERT + i]
                    v = cols[b * DIM_HILBERT + j]
                    g[a * DIM_HILBERT + i][b * DIM_HILBERT + j] = cyc_inner_product(u, v)

    one = Cyc24.one()
    for j in range(DIM_HILBERT):
        g[3 * DIM_HILBERT + j][3 * DIM_HILBERT + j] = one

    return g


def evaluate_target_q3_diagnostics() -> Degree6DiagnosticReport:
    """Evaluate two experimental coefficient matrices without candidate certification."""
    g_diag = build_block_diagonal_gramian()
    m6_diag = build_degree6_invariant_diagnostic_matrix(g_diag)
    w_x0 = build_invariant_dual_witness_x0(strict=True)
    inner_x0 = w_x0.trace_inner(m6_diag)
    if inner_x0 >= 0:
        raise ValueError(f"Dual witness X=0 matrix diagnostic failed: Tr(W * M) = {inner_x0} >= 0")

    w_mat_x0 = w_x0.to_matrix()
    pivots_x0 = ldlt_pivots_strictly_positive(w_mat_x0)

    receipt_x0 = DualWitnessReceipt(
        target_description="Experimental coefficient matrix for the block-diagonal X=0 fixture",
        witness_dimension=DEG6_INVARIANT_DIM,
        inner_product=str(inner_x0),
        inner_product_num=str(inner_x0.numerator),
        inner_product_den=str(inner_x0.denominator),
        strictly_negative=True,
        pivots_strictly_positive=True,
        pivots=[str(p) for p in pivots_x0],
    )

    g_synth = canonical_quad_gramian()
    m6_synth = build_degree6_extended_diagnostic_matrix(g_synth)
    w_s6 = build_extended_dual_witness_s6(strict=True)
    inner_s6 = w_s6.trace_inner(m6_synth)
    if inner_s6 >= 0:
        raise ValueError(f"Dual witness S6 matrix diagnostic failed: Tr(W * M) = {inner_s6} >= 0")

    w_mat_s6 = w_s6.to_matrix()
    pivots_s6 = ldlt_pivots_strictly_positive(w_mat_s6)

    receipt_s6 = DualWitnessReceipt(
        target_description="Experimental coefficient matrix for the synthetic S6 fixture",
        witness_dimension=DEG6_EXTENDED_DIM,
        inner_product=str(inner_s6),
        inner_product_num=str(inner_s6.numerator),
        inner_product_den=str(inner_s6.denominator),
        strictly_negative=True,
        pivots_strictly_positive=True,
        pivots=[str(p) for p in pivots_s6],
    )

    moment_report = Degree6MomentReport(
        invariant_dimension=DEG6_INVARIANT_DIM,
        extended_dimension=DEG6_EXTENDED_DIM,
        candidate_x0_refuted=False,
        candidate_s6_refuted=False,
        details="Exact matrix diagnostics only. Projector moment identities, positivity preservation, and a Lasserre relaxation are not established.",
    )

    cert = Degree6DiagnosticReport(
        schema_version=SCHEMA_VERSION,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
        scope=SCOPE_STRING,
        dimension=DIM_HILBERT,
        bases_count=NUM_BASES,
        invariant_dim=DEG6_INVARIANT_DIM,
        extended_dim=DEG6_EXTENDED_DIM,
        moment_report=moment_report,
        receipt_x0=receipt_x0,
        receipt_s6=receipt_s6,
        complete=False,
        diagnostics_complete=True,
        moment_semantics_verified=False,
    )
    assert_no_float(cert, "evaluate_target_q3_diagnostics.cert")
    return cert


def solve_target_q3_degree6_certificate() -> None:
    """Certification is unavailable; use evaluate_target_q3_diagnostics for exploration."""
    raise ValueError("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required")


def build_degree6_invariant_moment_matrix(g: Sequence[Sequence[Cyc24]]) -> None:
    """No sound projector-moment construction is supplied."""
    raise ValueError("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required")


def build_degree6_extended_moment_matrix(g: Sequence[Sequence[Cyc24]]) -> None:
    """No sound projector-moment construction is supplied."""
    raise ValueError("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required")
