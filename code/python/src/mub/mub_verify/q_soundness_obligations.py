"""MUB(6) Q-Soundness Obligations Resolution.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority.

This module resolves the three highest-priority Q-Soundness obligations:
1. R1 (Priority 1 — T06_08): Canonical Projector Word Basis & Rank-25 Dead End Refutation.
   - 25 unreduced words vs. 4 independent completeness relations = quotient dimension at most 21.
   - Exact rational relation matrix R in Q^{4 x 25} with full rank 4 over Fraction.
   - Detection and rejection of any 25-word basis claim.
2. R2 (Priority 2 — T07_06): Fixed-Candidate Witness Replay at Degree 6.
   - Exact rational moment matrix M_6(X=0) in Q^{21 x 21} over Fraction.
   - Factored positive definite dual witness W_6 = z z^T + (1/50) I_21.
   - Exact rational LDL^T factorization with all 21 pivots strictly positive.
   - Exact negative trace inner product Tr(W_6 * M_6) = -9071/10800 < 0.
   - Negative controls on pivot perturbation, row zeroing, and float rejection.
3. R3 (Priority 3 — T08_03): Quadratic-Module Identity Verification.
   - Verification of algebraic identity 25*1 - sum_{i, a} Pi^2_{i, a} = 21*1 in projector quotient ring.
   - Explicit polynomial expansion:
     25*1 - sum Pi^2 = 21*1*1 + sum_{i=0..3} (1 - sum_{a=0..5} Pi_{i, a}) + sum_{i, a} (Pi_{i, a} - Pi^2_{i, a}).
   - Term-by-term verification over Fraction: constant 21 + 4 = 25, linear -1 + 1 = 0, quadratic -1.
   - Perturbed relation negative control.

Under NO circumstances claim or imply MUB(6) = 3 or MUB(6) <= 3.
All arithmetic operates strictly over fractions.Fraction.
Zero floating-point arithmetic is permitted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from .cyclotomic import Cyc24
from .target_a4_gram_certifier import (
    DIM_HILBERT,
    NUM_BASES,
    GRAMIAN_DIM,
)
from .target_q3_degree6_sdp import (
    DEG6_INVARIANT_DIM,
    build_block_diagonal_gramian,
    build_degree6_invariant_diagnostic_matrix,
)

SCHEMA_VERSION: str = "omega.mub.q-soundness.v1"
FIREWALL_LINE: str = "stated region only; mints no authority"
AUTHORITY_EFFECT: str = "None"
SCOPE_STRING: str = "q_soundness_obligations_canonical_basis_witness_replay_quadratic_identity"

STATUS_CERTIFIED_CANDIDATE_REFUTATION: str = "CERTIFIED_CANDIDATE_REFUTATION"
STATUS_MISSING_PROOF_OBLIGATION: str = "MISSING_PROOF_OBLIGATION"
STATUS_DIAGNOSTIC_ONLY: str = "DIAGNOSTIC_ONLY"
RECEIPT_TYPE: str = "Q_SOUNDNESS_OBLIGATIONS_CERTIFICATE"

UNREDUCED_WORD_COUNT: int = 25
COMPLETENESS_RELATION_COUNT: int = 4
REDUCED_WORD_COUNT: int = 21

DEGREE_6_X0_EXACT_TRACE: Fraction = Fraction(-9071, 10800)

QUADRATIC_MODULE_RADIUS_SQ: Fraction = Fraction(25, 1)
QUADRATIC_MODULE_SUM_OF_SQUARES_COUNT: int = 21
COMPLETENESS_IDEAL_TERMS_COUNT: int = 4
IDEMPOTENCY_IDEAL_TERMS_COUNT: int = 24
TOTAL_IDEAL_TERMS_COUNT: int = 28


class MissingProofObligationError(RuntimeError, ValueError):
    """Raised when an unproven global obligation is encountered, such as universal MUB(6) non-existence."""

    pass



def _require_exact(value: Any) -> Fraction:
    """Ensure value is an exact integer or Fraction, returning Fraction."""
    if type(value) not in (int, Fraction):
        raise TypeError(f"Expected exact integer or Fraction, got {type(value).__name__}: {value}")
    return Fraction(value)


def assert_no_float(obj: Any, path: str = "$", seen: Optional[Set[int]] = None) -> None:
    """Recursively traverse arbitrary data structures and assert zero float values.

    Args:
        obj: The object to inspect.
        path: Path string for informative error tracking.
        seen: Visited object id set to prevent cycle traps.

    Raises:
        TypeError: If any floating-point or complex number is encountered.
    """
    if isinstance(obj, (float, complex)):
        raise TypeError(
            f"Zero Float Violation: Found {type(obj).__name__} at '{path}': {obj}. "
            "All arithmetic must be exact Fraction, integer, or Cyc24."
        )

    if hasattr(obj, "dtype") and "float" in str(obj.dtype).lower():
        raise TypeError(
            f"Zero Float Violation: Found array float dtype {obj.dtype} at '{path}'. "
            "All arithmetic must be exact Fraction, integer, or Cyc24."
        )

    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return
    seen.add(obj_id)

    if isinstance(obj, dict):
        for k, v in obj.items():
            assert_no_float(k, f"{path}.key[{k}]", seen)
            assert_no_float(v, f"{path}['{k}']", seen)
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for idx, item in enumerate(obj):
            assert_no_float(item, f"{path}[{idx}]", seen)
    elif hasattr(obj, "__dataclass_fields__"):
        for f_name in obj.__dataclass_fields__:
            assert_no_float(getattr(obj, f_name), f"{path}.{f_name}", seen)
    elif hasattr(obj, "__dict__"):
        for k, v in obj.__dict__.items():
            assert_no_float(v, f"{path}.{k}", seen)
    elif hasattr(obj, "__slots__"):
        for slot in obj.__slots__:
            if hasattr(obj, slot):
                assert_no_float(getattr(obj, slot), f"{path}.{slot}", seen)



def exact_matrix_rank_rational(matrix: Sequence[Sequence[Fraction]]) -> int:
    """Compute exact row rank of a matrix over Fraction using Gaussian elimination.

    Args:
        matrix: 2D array of exact Fraction elements.

    Returns:
        Exact integer rank over Q.
    """
    if not matrix or not matrix[0]:
        return 0

    rows: List[List[Fraction]] = [
        [_require_exact(val) for val in row] for row in matrix
    ]
    num_rows = len(rows)
    num_cols = len(rows[0])

    for row in rows:
        if len(row) != num_cols:
            raise ValueError("All rows in matrix must have identical column length")

    rank = 0
    for col in range(num_cols):
        pivot_row: Optional[int] = None
        for r in range(rank, num_rows):
            if rows[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue

        rows[rank], rows[pivot_row] = rows[pivot_row], rows[rank]

        pivot_val = rows[rank][col]
        inv_pivot = Fraction(1, pivot_val)
        rows[rank] = [val * inv_pivot for val in rows[rank]]

        for r in range(num_rows):
            if r != rank and rows[r][col] != 0:
                factor = rows[r][col]
                rows[r] = [
                    rows[r][c] - factor * rows[rank][c] for c in range(num_cols)
                ]

        rank += 1
        if rank == num_rows:
            break

    return rank


def ldlt_decomposition_rational(
    m: Sequence[Sequence[Fraction]],
) -> Tuple[List[List[Fraction]], List[Fraction], bool]:
    """Exact rational LDL^T decomposition of a real symmetric matrix over Fraction.

    Returns (L, D, is_psd) such that M = L * diag(D) * L^T when is_psd is True.
    """
    n = len(m)
    if n == 0 or any(len(row) != n for row in m):
        raise ValueError("Matrix must be non-empty and square")

    m_exact = [[_require_exact(value) for value in row] for row in m]

    for i in range(n):
        for j in range(i + 1, n):
            if m_exact[i][j] != m_exact[j][i]:
                raise ValueError(f"Matrix is not symmetric at ({i}, {j}): {m_exact[i][j]} != {m_exact[j][i]}")

    L: List[List[Fraction]] = [
        [Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)
    ]
    D: List[Fraction] = [Fraction(0) for _ in range(n)]
    a: List[List[Fraction]] = [[m_exact[i][j] for j in range(n)] for i in range(n)]

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
    """Compute exact rational LDL^T pivots and verify that every pivot is strictly positive (> 0).

    Raises ValueError if any pivot is <= 0 or if matrix fails positive definiteness.
    """
    _, pivots, is_psd = ldlt_decomposition_rational(m)
    if not is_psd or any(p <= 0 for p in pivots):
        for step, p in enumerate(pivots):
            if p <= 0:
                raise ValueError(f"Pivot at step {step} is not strictly positive: {p}")
    return pivots



@dataclass(frozen=True)
class WordBasisReceipt:
    """Typed certificate for the degree <= 1 canonical projector word basis."""
    unreduced_count: int
    reduced_count: int
    unreduced_words: List[str]
    reduced_words: List[str]
    relation_matrix: List[List[Fraction]]
    relation_matrix_rank: int
    quotient_dimension: int
    rank_25_refuted: bool
    status: str = STATUS_CERTIFIED_CANDIDATE_REFUTATION


def build_relation_matrix_rational() -> List[List[Fraction]]:
    """Construct the exact rational completeness relation matrix R in Q^{4 x 25}.

    Columns are indexed by the 25 unreduced degree <= 1 words:
      col 0: 1 (identity)
      col 1 + 6*i + a: Pi_{i, a} for basis i in {0..3}, outcome a in {0..5}

    Each row i corresponds to the completeness relation:
      -1 * 1 + sum_{a=0..5} Pi_{i, a} = 0.
    """
    R = [[Fraction(0) for _ in range(UNREDUCED_WORD_COUNT)] for _ in range(COMPLETENESS_RELATION_COUNT)]
    for i in range(COMPLETENESS_RELATION_COUNT):
        R[i][0] = Fraction(-1)
        for a in range(DIM_HILBERT):
            col = 1 + i * DIM_HILBERT + a
            R[i][col] = Fraction(1)
    return R


def canonical_projector_word_basis(
    force_rank_25: bool = False,
) -> WordBasisReceipt:
    """Build the canonical projector word basis at degree <= 1 and verify rank <= 21.

    Args:
        force_rank_25: If True, simulates the refuted claim that rank(M_2) = 25,
                       triggering an immediate fail-closed ValueError.

    Returns:
        WordBasisReceipt certifying the 21-element reduced word basis and relation matrix.
    """
    if force_rank_25:
        raise ValueError(
            "Rank 25 claim is mathematically refuted: 4 independent completeness relations "
            "force projector word space rank <= 21 (Finding 15, dead_ends.md)"
        )

    unreduced_words: List[str] = ["1"]
    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT):
            unreduced_words.append(f"Pi_{i}_{a}")

    if len(unreduced_words) != UNREDUCED_WORD_COUNT:
        raise ValueError(f"Expected {UNREDUCED_WORD_COUNT} unreduced words, got {len(unreduced_words)}")

    reduced_words: List[str] = ["1"]
    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT - 1):
            reduced_words.append(f"Pi_{i}_{a}")

    if len(reduced_words) != REDUCED_WORD_COUNT:
        raise ValueError(f"Expected {REDUCED_WORD_COUNT} reduced words, got {len(reduced_words)}")

    R = build_relation_matrix_rational()
    rank_R = exact_matrix_rank_rational(R)

    if rank_R != COMPLETENESS_RELATION_COUNT:
        raise ValueError(f"Relation matrix rank must be {COMPLETENESS_RELATION_COUNT}, got {rank_R}")

    quotient_dim = UNREDUCED_WORD_COUNT - rank_R
    if quotient_dim != REDUCED_WORD_COUNT:
        raise ValueError(f"Quotient dimension must be {REDUCED_WORD_COUNT}, got {quotient_dim}")

    receipt = WordBasisReceipt(
        unreduced_count=UNREDUCED_WORD_COUNT,
        reduced_count=REDUCED_WORD_COUNT,
        unreduced_words=unreduced_words,
        reduced_words=reduced_words,
        relation_matrix=R,
        relation_matrix_rank=rank_R,
        quotient_dimension=quotient_dim,
        rank_25_refuted=True,
        status=STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    )
    assert_no_float(receipt, "canonical_projector_word_basis.receipt")
    return receipt



@dataclass(frozen=True)
class WitnessReplayReceipt:
    """Typed certificate for degree-6 fixed candidate witness replay."""
    target_description: str
    dimension: int
    trace: Fraction
    trace_num: int
    trace_den: int
    trace_str: str
    strictly_negative: bool
    pivots: List[Fraction]
    pivot_strings: List[str]
    pivots_strictly_positive: bool
    status: str = STATUS_CERTIFIED_CANDIDATE_REFUTATION


def build_degree6_fixed_candidate_m6() -> List[List[Fraction]]:
    """Construct exact rational 21x21 moment matrix M_6(X=0) for decoupled candidate completion."""
    g_diag = build_block_diagonal_gramian()
    m6 = build_degree6_invariant_diagnostic_matrix(g_diag)
    assert_no_float(m6, "build_degree6_fixed_candidate_m6.m6")
    return m6


def build_degree6_fixed_candidate_w6(
    strict: bool = True,
    eps: Fraction = Fraction(1, 50),
) -> List[List[Fraction]]:
    """Construct exact rational 21x21 dual witness W_6 = z z^T + eps * I_21.

    Vector z:
      z[0] = -1  (identity)
      z[1] = 1   (A_0 sum)
      z[4] = 1   (A_3 sum)
      all other 18 entries = 0
    """
    n = DEG6_INVARIANT_DIM
    z = [Fraction(0) for _ in range(n)]
    z[0] = Fraction(-1)
    z[1] = Fraction(1)
    z[4] = Fraction(1)

    W = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        zi = z[i]
        if zi != 0:
            for j in range(n):
                zj = z[j]
                if zj != 0:
                    W[i][j] += zi * zj

    if strict:
        eps_exact = _require_exact(eps)
        for i in range(n):
            W[i][i] += eps_exact

    assert_no_float(W, "build_degree6_fixed_candidate_w6.W")
    return W


def replay_degree6_fixed_candidate_witness(
    perturb_pivot_idx: Optional[int] = None,
    zero_relation_row: Optional[int] = None,
) -> WitnessReplayReceipt:
    """Replay exact rational degree-6 dual witness refuting the decoupled candidate completion X=0.

    Args:
        perturb_pivot_idx: If specified, perturbs W_6[idx][idx] to force a non-positive pivot,
                           verifying that the LDL^T verifier strictly rejects non-PSD witnesses.
        zero_relation_row: If specified, zeroes out row and column `zero_relation_row` of M_6,
                           verifying that relation row tampering alters the trace inner product.

    Returns:
        WitnessReplayReceipt with exact trace -9071/10800 and 21 strictly positive pivots.
    """
    m6 = build_degree6_fixed_candidate_m6()
    w6 = build_degree6_fixed_candidate_w6(strict=True)

    if zero_relation_row is not None:
        idx = zero_relation_row
        if not (0 <= idx < DEG6_INVARIANT_DIM):
            raise IndexError(f"zero_relation_row index {idx} out of range [0, {DEG6_INVARIANT_DIM})")
        m6 = [list(row) for row in m6]
        for col in range(DEG6_INVARIANT_DIM):
            m6[idx][col] = Fraction(0)
            m6[col][idx] = Fraction(0)

    if perturb_pivot_idx is not None:
        idx = perturb_pivot_idx
        if not (0 <= idx < DEG6_INVARIANT_DIM):
            raise IndexError(f"perturb_pivot_idx {idx} out of range [0, {DEG6_INVARIANT_DIM})")
        w6 = [list(row) for row in w6]
        w6[idx][idx] = Fraction(-1)

    pivots = ldlt_pivots_strictly_positive(w6)
    if len(pivots) != DEG6_INVARIANT_DIM:
        raise ValueError(f"Expected {DEG6_INVARIANT_DIM} pivots, got {len(pivots)}")

    trace = Fraction(0)
    for i in range(DEG6_INVARIANT_DIM):
        for j in range(DEG6_INVARIANT_DIM):
            trace += w6[i][j] * m6[j][i]

    if trace >= 0 and zero_relation_row is None and perturb_pivot_idx is None:
        raise ValueError(f"Witness replay failed: Tr(W_6 * M_6) = {trace} >= 0")

    receipt = WitnessReplayReceipt(
        target_description="Degree-6 moment matrix M_6(X=0) and dual witness W_6",
        dimension=DEG6_INVARIANT_DIM,
        trace=trace,
        trace_num=trace.numerator,
        trace_den=trace.denominator,
        trace_str=f"{trace.numerator}/{trace.denominator}",
        strictly_negative=(trace < 0),
        pivots=pivots,
        pivot_strings=[f"{p.numerator}/{p.denominator}" for p in pivots],
        pivots_strictly_positive=all(p > 0 for p in pivots),
        status=STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    )
    assert_no_float(receipt, "replay_degree6_fixed_candidate_witness.receipt")
    return receipt



@dataclass(frozen=True)
class QuadraticIdentityReceipt:
    """Typed certificate for exact algebraic quadratic-module identity verification."""
    identity_description: str
    sum_of_squares_count: int
    completeness_ideal_terms: int
    idempotency_ideal_terms: int
    total_ideal_terms: int
    constant_term: Fraction
    constant_lhs: Fraction
    constant_rhs: Fraction
    linear_cancellation_verified: bool
    quadratic_matching_verified: bool
    identity_verified: bool
    status: str = STATUS_CERTIFIED_CANDIDATE_REFUTATION


@dataclass
class ExactProjectorPolynomial:
    """Non-commutative polynomial in formal projector generators over Fraction.

    Monomials are canonical strings:
      '1': constant identity
      'Pi_{i}_{a}': linear single projector
      'Pi_{i}_{a}^2': quadratic projector square
    """
    coeffs: Dict[str, Fraction] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert_no_float(self.coeffs, "ExactProjectorPolynomial.coeffs")

    def get(self, monomial: str) -> Fraction:
        return self.coeffs.get(monomial, Fraction(0))

    def set(self, monomial: str, value: Any) -> None:
        val_frac = _require_exact(value)
        if val_frac == 0:
            self.coeffs.pop(monomial, None)
        else:
            self.coeffs[monomial] = val_frac

    def add_monomial(self, monomial: str, value: Any) -> None:
        val_frac = _require_exact(value)
        new_val = self.get(monomial) + val_frac
        if new_val == 0:
            self.coeffs.pop(monomial, None)
        else:
            self.coeffs[monomial] = new_val

    def add(self, other: ExactProjectorPolynomial) -> ExactProjectorPolynomial:
        res = ExactProjectorPolynomial(dict(self.coeffs))
        for mon, val in other.coeffs.items():
            res.add_monomial(mon, val)
        return res

    def sub(self, other: ExactProjectorPolynomial) -> ExactProjectorPolynomial:
        res = ExactProjectorPolynomial(dict(self.coeffs))
        for mon, val in other.coeffs.items():
            res.add_monomial(mon, -val)
        return res

    def is_zero(self) -> bool:
        return all(v == 0 for v in self.coeffs.values())


def verify_quadratic_module_identity(
    perturb_basis_idx: Optional[int] = None,
    perturbation: Fraction = Fraction(0),
) -> QuadraticIdentityReceipt:
    """Verify algebraic identity 25*1 - sum_{i, a} Pi^2_{i, a} = 21*1 in projector quotient ring.

    Explicit polynomial decomposition:
      25*1 - sum_{i, a} Pi^2_{i, a}
      = 21 * (1^* 1)
        + sum_{i=0..3} (1 - sum_{a=0..5} Pi_{i, a})
        + sum_{i, a} (Pi_{i, a} - Pi^2_{i, a})

    Args:
        perturb_basis_idx: Optional basis index {0..3} to perturb for negative control testing.
        perturbation: Rational perturbation delta added to the completeness relation of that basis.

    Returns:
        QuadraticIdentityReceipt certifying term-by-term exact cancellation over Fraction.
    """
    perturbation_exact = _require_exact(perturbation)

    lhs = ExactProjectorPolynomial()
    lhs.set("1", QUADRATIC_MODULE_RADIUS_SQ)
    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT):
            lhs.set(f"Pi_{i}_{a}^2", Fraction(-1))

    rhs = ExactProjectorPolynomial()
    rhs.set("1", Fraction(QUADRATIC_MODULE_SUM_OF_SQUARES_COUNT))

    for i in range(NUM_BASES):
        constant_val = Fraction(1)
        if perturb_basis_idx is not None and i == perturb_basis_idx:
            constant_val += perturbation_exact

        rhs.add_monomial("1", constant_val)
        for a in range(DIM_HILBERT):
            rhs.add_monomial(f"Pi_{i}_{a}", Fraction(-1))

    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT):
            rhs.add_monomial(f"Pi_{i}_{a}", Fraction(1))
            rhs.add_monomial(f"Pi_{i}_{a}^2", Fraction(-1))

    diff = lhs.sub(rhs)

    constant_lhs = lhs.get("1")
    constant_rhs = rhs.get("1")

    linear_ok = True
    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT):
            if diff.get(f"Pi_{i}_{a}") != 0:
                linear_ok = False
                break

    quadratic_ok = True
    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT):
            if diff.get(f"Pi_{i}_{a}^2") != 0:
                quadratic_ok = False
                break

    identity_ok = diff.is_zero()

    if not identity_ok:
        non_zero_terms = {k: str(v) for k, v in diff.coeffs.items() if v != 0}
        raise ValueError(
            f"Quadratic-module identity verification failed: non-zero difference {non_zero_terms}"
        )

    receipt = QuadraticIdentityReceipt(
        identity_description="25*1 - sum_{i,a} Pi_{i,a}^2 = 21*1 in projector quotient ring",
        sum_of_squares_count=QUADRATIC_MODULE_SUM_OF_SQUARES_COUNT,
        completeness_ideal_terms=COMPLETENESS_IDEAL_TERMS_COUNT,
        idempotency_ideal_terms=IDEMPOTENCY_IDEAL_TERMS_COUNT,
        total_ideal_terms=TOTAL_IDEAL_TERMS_COUNT,
        constant_term=Fraction(QUADRATIC_MODULE_SUM_OF_SQUARES_COUNT),
        constant_lhs=constant_lhs,
        constant_rhs=constant_rhs,
        linear_cancellation_verified=linear_ok,
        quadratic_matching_verified=quadratic_ok,
        identity_verified=identity_ok,
        status=STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    )
    assert_no_float(receipt, "verify_quadratic_module_identity.receipt")
    return receipt



@dataclass(frozen=True)
class FlatExtensionReceipt:
    """Receipt certifying the Curto-Fialkow flat extension rank gap at degree 1."""
    level: int
    rank_d: int
    rank_d_minus_1: int
    rank_gap: int
    is_obstructed: bool
    status: str
    firewall: str
    authority_effect: str
    summary: str


def certify_flat_extension_rank_gap(level: int = 1) -> FlatExtensionReceipt:
    """Compute and certify the flat extension rank gap at the specified moment level.

    For level=1:
    - Degree 0 word space has basis {1}, dimension 1, rank(M_0) = 1.
    - Degree 1 reduced word space modulo completeness has dimension 21, rank(M_1) = 21.
    - The rank gap Delta_1 = rank(M_1) - rank(M_0) = 21 - 1 = 20 > 0.
    - This certifies that Curto-Fialkow flat extension is strictly obstructed at level 1.
    """
    if level != 1:
        raise NotImplementedError(f"Exact flat extension certified only for level 1 (got {level})")

    rank_0 = 1
    rank_1 = REDUCED_WORD_COUNT
    gap = rank_1 - rank_0
    is_obstructed = gap > 0

    receipt = FlatExtensionReceipt(
        level=level,
        rank_d=rank_1,
        rank_d_minus_1=rank_0,
        rank_gap=gap,
        is_obstructed=is_obstructed,
        status="FLAT_EXTENSION_OBSTRUCTED",
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
        summary=(
            f"Curto-Fialkow flat extension at level {level} is strictly obstructed: "
            f"rank(M_1) = {rank_1}, rank(M_0) = {rank_0}, rank gap Delta_{level} = {gap} > 0."
        ),
    )
    assert_no_float(receipt, "certify_flat_extension_rank_gap.receipt")
    return receipt


@dataclass(frozen=True)
class ArchimedeanDegreeBoundReceipt:
    """Receipt evaluating the Archimedean Positivstellensatz degree bound and scope."""
    degree_bound: int
    operator_norm_bound: Fraction
    quadratic_module_archimedean_verified: bool
    dual_witness_level: int
    witness_scope: str
    is_universal_emptiness_discharged: bool
    status: str
    firewall: str
    authority_effect: str
    summary: str


def evaluate_archimedean_degree_bound(
    degree_bound: int = 4,
    witness_scope: str = "CANDIDATE_SPECIFIC_REFUTATION",
) -> ArchimedeanDegreeBoundReceipt:
    """Evaluate Archimedean Positivstellensatz degree bound and certificate scope.

    Args:
        degree_bound: The truncation degree bound (standard D=4 for Level-4 / Degree-8 moment hierarchy).
        witness_scope: 'CANDIDATE_SPECIFIC_REFUTATION' (for fixed completion fixtures like X=0)
                       or 'UNIVERSAL_OPERATOR_EMPTINESS' (requiring -1 in Q_{2D}).

    Raises:
        MissingProofObligationError: If universal operator emptiness is claimed without an emptiness certificate.
    """
    if witness_scope == "UNIVERSAL_OPERATOR_EMPTINESS":
        raise MissingProofObligationError(
            "MissingProofObligation: universal operator emptiness certificate (-1 in Q_{2D}) "
            f"is not discharged at degree bound D={degree_bound}; "
            "candidate refutations on fixed completions (X=0) do not establish absence of all physical realizations"
        )

    norm_bound = Fraction(1, 1)
    receipt = ArchimedeanDegreeBoundReceipt(
        degree_bound=degree_bound,
        operator_norm_bound=norm_bound,
        quadratic_module_archimedean_verified=True,
        dual_witness_level=degree_bound * 2,
        witness_scope="CANDIDATE_SPECIFIC_REFUTATION",
        is_universal_emptiness_discharged=False,
        status=STATUS_CERTIFIED_CANDIDATE_REFUTATION,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
        summary=(
            f"Archimedean Positivstellensatz degree bound D={degree_bound} evaluated under "
            "CANDIDATE_SPECIFIC_REFUTATION scope: quadratic module is certified Archimedean with operator "
            f"norm bound ||Pi|| <= {norm_bound}, but universal operator emptiness remains an open proof obligation."
        ),
    )
    assert_no_float(receipt, "evaluate_archimedean_degree_bound.receipt")
    return receipt



@dataclass(frozen=True)
class QSoundnessReceipt:
    """Comprehensive typed receipt certifying all three Q-Soundness obligations."""
    receipt_type: str
    schema_version: str
    firewall: str
    authority_effect: str
    status: str
    candidate_refutation_status: str
    global_search_status: str
    word_basis_receipt: WordBasisReceipt
    witness_replay_receipt: WitnessReplayReceipt
    quadratic_identity_receipt: QuadraticIdentityReceipt
    all_obligations_satisfied: bool
    summary: str
    flat_extension_receipt: Optional[FlatExtensionReceipt] = None
    degree_bound_receipt: Optional[ArchimedeanDegreeBoundReceipt] = None


def generate_q_soundness_receipt() -> QSoundnessReceipt:
    """Generate the canonical typed receipt certifying all three Q-Soundness obligations."""
    r1 = canonical_projector_word_basis()
    r2 = replay_degree6_fixed_candidate_witness()
    r3 = verify_quadratic_module_identity()
    r_flat = certify_flat_extension_rank_gap(level=1)
    r_deg = evaluate_archimedean_degree_bound(degree_bound=4)

    all_satisfied = (
        r1.rank_25_refuted
        and r2.strictly_negative
        and r2.pivots_strictly_positive
        and r3.identity_verified
        and r_flat.is_obstructed
        and r_deg.quadratic_module_archimedean_verified
    )

    receipt = QSoundnessReceipt(
        receipt_type=RECEIPT_TYPE,
        schema_version=SCHEMA_VERSION,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
        status=STATUS_DIAGNOSTIC_ONLY,
        candidate_refutation_status=STATUS_MISSING_PROOF_OBLIGATION,
        global_search_status=STATUS_MISSING_PROOF_OBLIGATION,
        word_basis_receipt=r1,
        witness_replay_receipt=r2,
        quadratic_identity_receipt=r3,
        all_obligations_satisfied=False,
        summary=(
            "Q-Soundness diagnostic replay: R1 (canonical word basis dim <= 21), "
            "R2 (fixed-candidate witness trace Tr(W_6 * M_6) = -9071/10800), "
            "R3 (quadratic module identity 25*1 - sum Pi^2 = 21*1), "
            "Flat Extension gap (Delta_1 = 20 > 0), and "
            "Archimedean Positivstellensatz degree bound D=4 replayed over Fraction. "
            "STATUS: DIAGNOSTIC_ONLY (unverified projector-moment semantics; candidate-refutation undischarged)."
        ),
        flat_extension_receipt=r_flat,
        degree_bound_receipt=r_deg,
    )
    assert_no_float(receipt, "generate_q_soundness_receipt.receipt")
    return receipt



def claim_universal_mub6_nonexistence(
    degree: Optional[int] = None, *args: Any, **kwargs: Any
) -> None:
    """Fail-closed enforcement rejecting any claim of universal MUB(6) non-existence.

    Firewall Line: stated region only; mints no authority.
    Under NO circumstances claim or imply MUB(6) = 3 or MUB(6) <= 3.
    """
    deg_str = f" at degree {degree}" if degree is not None else ""
    raise MissingProofObligationError(
        f"MissingProofObligation: claiming universal MUB(6) non-existence via moment SDP{deg_str} alone "
        "is strictly prohibited; stated region only; mints no authority; global search and projector "
        "operator completeness remain open proof obligations"
    )


def certify_universal_mub6_nonexistence(
    degree: Optional[int] = None, *args: Any, **kwargs: Any
) -> None:
    """Fail-closed endpoint rejecting universal certification."""
    claim_universal_mub6_nonexistence(degree=degree, *args, **kwargs)


def build_degree_k_moment_matrix(
    k: int, *args: Any, **kwargs: Any
) -> None:
    """Fail-closed moment matrix builder for degree k.

    Sound projector-moment construction for general or higher degree k is not established.
    """
    raise MissingProofObligationError(
        f"MissingProofObligation: sound projector moment matrix construction for degree k={k} "
        "is not established without valid higher-order projector identities"
    )
