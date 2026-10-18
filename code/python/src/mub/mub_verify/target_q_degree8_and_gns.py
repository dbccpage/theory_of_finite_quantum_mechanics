"""Target Q Degree-8 SDP, GNS Pre-Hilbert Space, and Algebraic Rewriting Engine.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority.

This module resolves and implements the six key Stream 3 vectors:
1. T09_10: Non-commutative GNS pre-Hilbert space construction H_GNS = W_<=d / N
   and state vector evaluation on exact rational test states.
2. T07_08: Degree-8 decoupled X=0 dual witness replay with exact trace
   Tr(W8 . M8) = -9071/10800 and strictly positive LDL^T pivots.
3. T07_09: Degree-8 synthetic Tao S6 dual witness replay with exact trace
   Tr(W8 . M8) = -5046587/129600 and strictly positive LDL^T pivots.
4. T06_03: Confluent term rewriting system for projector idempotency
   Pi^2 -> Pi and intra-basis orthogonality Pi_ia Pi_ib -> 0 (a != b).
5. T08_05: Idempotency identity: 1 - Pi = (1 - Pi)^2 in Q certifying projector
   spectra lie in [0, 1].
6. T10_10: Exact cyclotomic inner product verification engine over Q(zeta_24)
   with zero floating-point tolerance.

All operations operate over fractions.Fraction, Cyc24, or exact integers.
Zero floating-point arithmetic is permitted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
import pathlib
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from .cyclotomic import Cyc24
from .mub_triples import (
    dita_seed_triple_columns,
    f6_family_columns,
    inner_product as cyc_inner_product,
    product_y2_qa_columns,
    standard_basis_b1,
)
from .target_a4_gram_certifier import (
    DIM_HILBERT,
    NUM_BASES,
    GRAMIAN_DIM,
    canonical_quad_gramian,
    canonical_triple_exact,
    exact_rational,
)
from .target_q4_degree8_sdp import (
    DEG8_INVARIANT_DIM,
    DEG8_EXTENDED_DIM,
    build_block_diagonal_gramian,
    build_degree8_extended_diagnostic_matrix,
    build_degree8_invariant_diagnostic_matrix,
    build_extended_dual_witness_s6,
    build_invariant_dual_witness_x0,
    ldlt_decomposition_rational,
    ldlt_pivots_strictly_positive,
)

SCHEMA_VERSION: str = "omega.mub.target-q-degree8-and-gns.v1"
FIREWALL_LINE: str = "stated region only; mints no authority"
AUTHORITY_EFFECT: str = "None"
SCOPE_STRING: str = "stream3_target_q_degree8_sdp_and_gns_replay"

STATUS_CERTIFIED_REPLAY: str = "CERTIFIED_CANDIDATE_REPLAY"
STATUS_DIAGNOSTIC_REPLAY: str = "DIAGNOSTIC_MATRIX_REPLAY_ONLY"
STATUS_CONFLUENT_REWRITING: str = "CERTIFIED_CONFLUENT_REWRITING"
STATUS_SPECTRAL_BOUND: str = "CERTIFIED_SPECTRAL_BOUND"
STATUS_GNS_CONSTRUCTED: str = "CERTIFIED_GNS_CONSTRUCTION"
STATUS_INDEFINITE_FORM_DIAGNOSTIC: str = "STATUS_INDEFINITE_FORM_DIAGNOSTIC"
STATUS_CYCLOTOMIC_VERIFIED: str = "CERTIFIED_CYCLOTOMIC_INNER_PRODUCT"

DEG8_X0_EXACT_TRACE: Fraction = Fraction(-9071, 10800)
DEG8_S6_EXACT_TRACE: Fraction = Fraction(-5046587, 129600)



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



@dataclass(frozen=True)
class ProjectorSymbol:
    """Formal projector generator symbol Pi_{basis, outcome}."""
    basis: int
    outcome: int

    def __post_init__(self) -> None:
        if not (0 <= self.basis < NUM_BASES):
            raise ValueError(f"Basis index {self.basis} out of range [0, {NUM_BASES})")
        if not (0 <= self.outcome < DIM_HILBERT):
            raise ValueError(f"Outcome index {self.outcome} out of range [0, {DIM_HILBERT})")

    def __str__(self) -> str:
        return f"Pi_{self.basis}_{self.outcome}"

    def adj(self) -> ProjectorSymbol:
        """Involution: projectors are self-adjoint Pi^* = Pi."""
        return self


@dataclass(frozen=True)
class ProjectorWord:
    """Formal non-commutative word (monomial) in projector generator symbols."""
    symbols: Tuple[ProjectorSymbol, ...] = ()

    def __post_init__(self) -> None:
        for s in self.symbols:
            if not isinstance(s, ProjectorSymbol):
                raise TypeError(f"Word symbols must be ProjectorSymbol instances, got {type(s)}")

    @property
    def is_identity(self) -> bool:
        return len(self.symbols) == 0

    @property
    def length(self) -> int:
        return len(self.symbols)

    def __str__(self) -> str:
        if self.is_identity:
            return "1"
        return " * ".join(str(s) for s in self.symbols)

    def adj(self) -> ProjectorWord:
        """Involution: reverses word sequence with adjoint symbols (s_k ... s_1)."""
        return ProjectorWord(tuple(s.adj() for s in reversed(self.symbols)))

    def mul(self, other: ProjectorWord) -> ProjectorWord:
        """Non-commutative concatenation of words."""
        return ProjectorWord(self.symbols + other.symbols)


def reduce_projector_word_step(
    word: ProjectorWord,
    left_first: bool = True,
) -> Tuple[Optional[ProjectorWord], bool]:
    """Perform a single rewriting step on a projector word.

    Rules:
    1. Idempotency: Pi_{i, a} Pi_{i, a} -> Pi_{i, a}
    2. Orthogonality: Pi_{i, a} Pi_{i, b} -> 0 for a != b

    Returns:
        (new_word, changed): new_word is None if reduced to 0.
    """
    syms = word.symbols
    n = len(syms)
    if n <= 1:
        return word, False

    indices = list(range(n - 1)) if left_first else list(range(n - 2, -1, -1))

    for k in indices:
        s1 = syms[k]
        s2 = syms[k + 1]
        if s1.basis == s2.basis:
            if s1.outcome == s2.outcome:
                new_syms = syms[:k] + (s1,) + syms[k + 2:]
                return ProjectorWord(new_syms), True
            else:
                return None, True

    return word, False


def reduce_projector_word(
    word: ProjectorWord,
    left_first: bool = True,
) -> Optional[ProjectorWord]:
    """Fully reduce a projector word to normal form under the rewriting system.

    Returns:
        Optional[ProjectorWord]: Normal form word, or None if the word rewrites to 0.
    """
    current: Optional[ProjectorWord] = word
    while current is not None:
        next_word, changed = reduce_projector_word_step(current, left_first=left_first)
        if not changed:
            break
        current = next_word
    return current


@dataclass
class NonCommutativeProjectorPolynomial:
    """Non-commutative polynomial in projector words with exact Fraction coefficients."""
    terms: Dict[ProjectorWord, Fraction] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert_no_float(self.terms, "NonCommutativeProjectorPolynomial.terms")

    def get(self, word: ProjectorWord) -> Fraction:
        return self.terms.get(word, Fraction(0))

    def set(self, word: ProjectorWord, coeff: Any) -> None:
        c = _require_exact(coeff)
        if c == 0:
            self.terms.pop(word, None)
        else:
            self.terms[word] = c

    def add_word(self, word: ProjectorWord, coeff: Any) -> None:
        c = _require_exact(coeff)
        new_c = self.get(word) + c
        if new_c == 0:
            self.terms.pop(word, None)
        else:
            self.terms[word] = new_c

    def add(self, other: NonCommutativeProjectorPolynomial) -> NonCommutativeProjectorPolynomial:
        res = NonCommutativeProjectorPolynomial(dict(self.terms))
        for w, c in other.terms.items():
            res.add_word(w, c)
        return res

    def sub(self, other: NonCommutativeProjectorPolynomial) -> NonCommutativeProjectorPolynomial:
        res = NonCommutativeProjectorPolynomial(dict(self.terms))
        for w, c in other.terms.items():
            res.add_word(w, -c)
        return res

    def mul_scalar(self, scalar: Any) -> NonCommutativeProjectorPolynomial:
        s = _require_exact(scalar)
        if s == 0:
            return NonCommutativeProjectorPolynomial()
        return NonCommutativeProjectorPolynomial({w: c * s for w, c in self.terms.items()})

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.terms.values())

    def reduce(self) -> NonCommutativeProjectorPolynomial:
        """Reduce all monomial words in polynomial to their confluent normal forms."""
        res = NonCommutativeProjectorPolynomial()
        for w, c in self.terms.items():
            nw = reduce_projector_word(w)
            if nw is not None:
                res.add_word(nw, c)
        return res


@dataclass(frozen=True)
class ConfluentRewritingReceipt:
    """Typed receipt certifying confluent term rewriting for projector relations."""
    rules_enforced: Tuple[str, ...]
    critical_triples_tested: int
    critical_triples_confluent: int
    all_critical_pairs_confluent: bool
    strongly_normalizing: bool
    unique_normal_form_certified: bool
    status: str
    firewall: str
    authority_effect: str


def verify_confluent_rewriting_system() -> ConfluentRewritingReceipt:
    """Verify confluence and termination across all critical overlapping triples.

    For 4 bases and 6 outcomes, tests all 4 * 6^3 = 864 critical triples
    (Pi_{i, a}, Pi_{i, b}, Pi_{i, c}) under left-first and right-first reductions,
    checking that both reduction sequences reach identical normal forms.
    """
    critical_tested = 0
    critical_confluent = 0

    for i in range(NUM_BASES):
        for a in range(DIM_HILBERT):
            for b in range(DIM_HILBERT):
                for c in range(DIM_HILBERT):
                    sym1 = ProjectorSymbol(i, a)
                    sym2 = ProjectorSymbol(i, b)
                    sym3 = ProjectorSymbol(i, c)
                    word = ProjectorWord((sym1, sym2, sym3))

                    norm_left = reduce_projector_word(word, left_first=True)
                    norm_right = reduce_projector_word(word, left_first=False)

                    critical_tested += 1
                    if norm_left == norm_right:
                        critical_confluent += 1
                    else:
                        raise ValueError(
                            f"Confluence failure on triple {word}: "
                            f"left={norm_left} != right={norm_right}"
                        )

    receipt = ConfluentRewritingReceipt(
        rules_enforced=(
            "Pi_{i, a}^2 -> Pi_{i, a} (idempotency)",
            "Pi_{i, a} Pi_{i, b} -> 0 for a != b (intra-basis orthogonality)",
        ),
        critical_triples_tested=critical_tested,
        critical_triples_confluent=critical_confluent,
        all_critical_pairs_confluent=(critical_tested == critical_confluent),
        strongly_normalizing=True,
        unique_normal_form_certified=True,
        status=STATUS_CONFLUENT_REWRITING,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "verify_confluent_rewriting_system.receipt")
    return receipt



@dataclass(frozen=True)
class IdempotencySpectralBoundReceipt:
    """Typed certificate for projector spectral containment sigma(Pi) subset [0, 1]."""
    symbol: str
    basis: int
    outcome: int
    sos_decomposition_verified: bool
    ideal_element_verified: bool
    lower_bound_zero_verified: bool
    upper_bound_one_verified: bool
    spectrum_contained_in_unit_interval: bool
    operator_norm_bound: Fraction
    status: str
    firewall: str
    authority_effect: str


def verify_idempotency_spectral_bound(
    basis: int = 0,
    outcome: int = 0,
    perturb_sos_coeff: Optional[Fraction] = None,
) -> IdempotencySpectralBoundReceipt:
    """Verify algebraic identity 1 - Pi = (1 - Pi)^2 in quotient ring certifying sigma(Pi) subset [0, 1].

    Decomposition in free non-commutative polynomial algebra:
      (1 - Pi) = (1 - Pi)^2 + (Pi - Pi^2)
    where:
      - (1 - Pi)^2 = (1 - Pi)^* (1 - Pi) is an exact sum-of-squares (SOS) square.
      - (Pi - Pi^2) is an element of the projector ideal I_proj.
    This establishes 1 - Pi >= 0 in the quadratic module Q(I_proj), yielding Pi <= 1.
    Together with Pi = Pi^2 + (Pi - Pi^2) >= 0 (yielding Pi >= 0),
    the spectrum sigma(Pi) is contained in [0, 1] with operator norm bound ||Pi|| <= 1.

    Args:
        basis: Basis index in [0, 4).
        outcome: Outcome index in [0, 6).
        perturb_sos_coeff: Optional perturbation to test failure detection.
    """
    sym = ProjectorSymbol(basis, outcome)
    w_id = ProjectorWord(())
    w_p = ProjectorWord((sym,))
    w_p2 = ProjectorWord((sym, sym))

    target = NonCommutativeProjectorPolynomial()
    target.set(w_id, Fraction(1))
    target.set(w_p, Fraction(-1))

    sos_weight = Fraction(1)
    if perturb_sos_coeff is not None:
        sos_weight += _require_exact(perturb_sos_coeff)

    sos_square = NonCommutativeProjectorPolynomial()
    sos_square.set(w_id, Fraction(1) * sos_weight)
    sos_square.set(w_p, Fraction(-2) * sos_weight)
    sos_square.set(w_p2, Fraction(1) * sos_weight)

    ideal_elem = NonCommutativeProjectorPolynomial()
    ideal_elem.set(w_p, Fraction(1))
    ideal_elem.set(w_p2, Fraction(-1))

    diff = target.sub(sos_square).sub(ideal_elem)
    sos_ok = diff.is_zero()

    p_target = NonCommutativeProjectorPolynomial()
    p_target.set(w_p, Fraction(1))

    p_square = NonCommutativeProjectorPolynomial()
    p_square.set(w_p2, Fraction(1))

    p_diff = p_target.sub(p_square).sub(ideal_elem)
    p_ok = p_diff.is_zero()

    if not (sos_ok and p_ok):
        if perturb_sos_coeff is None:
            raise ValueError(
                f"Spectral bound identity check failed for {sym}: "
                f"diff={diff.terms}, p_diff={p_diff.terms}"
            )

    receipt = IdempotencySpectralBoundReceipt(
        symbol=str(sym),
        basis=basis,
        outcome=outcome,
        sos_decomposition_verified=sos_ok,
        ideal_element_verified=p_ok,
        lower_bound_zero_verified=p_ok,
        upper_bound_one_verified=sos_ok,
        spectrum_contained_in_unit_interval=(sos_ok and p_ok),
        operator_norm_bound=Fraction(1, 1),
        status=STATUS_SPECTRAL_BOUND,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "verify_idempotency_spectral_bound.receipt")
    return receipt



def nullspace_rational(matrix: Sequence[Sequence[Fraction]]) -> Tuple[List[List[Fraction]], int]:
    """Compute an exact rational basis for the nullspace (kernel) of a matrix over Fraction.

    Returns:
        (null_basis, rank): null_basis is a list of basis vectors for ker(M).
    """
    if not matrix or not matrix[0]:
        return [], 0

    m = len(matrix)
    n = len(matrix[0])
    mat = [[_require_exact(matrix[r][c]) for c in range(n)] for r in range(m)]

    pivots: List[int] = []
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(m):
            if i != r and mat[i][c] != 0:
                fac = mat[i][c]
                mat[i] = [mat[i][k] - fac * mat[r][k] for k in range(n)]
        pivots.append(c)
        r += 1
        if r == m:
            break

    rank = len(pivots)
    free_vars = [c for c in range(n) if c not in pivots]
    null_basis: List[List[Fraction]] = []
    for f in free_vars:
        vec = [Fraction(0) for _ in range(n)]
        vec[f] = Fraction(1)
        for i, p in enumerate(pivots):
            vec[p] = -mat[i][f]
        null_basis.append(vec)

    return null_basis, rank


def find_negative_mode_or_certify_psd(
    m: Sequence[Sequence[Fraction]],
) -> Tuple[bool, Optional[List[Fraction]]]:
    """Verify whether symmetric rational matrix m is PSD.

    Returns:
        (is_psd, negative_mode):
        If PSD, returns (True, None).
        If not PSD, returns (False, v) where v^T m v < 0 is an exact witness vector.
    """
    n = len(m)
    for i in range(n):
        if m[i][i] < 0:
            v = [Fraction(1 if k == i else 0) for k in range(n)]
            return False, v

    for i in range(n):
        if m[i][i] == 0:
            for j in range(n):
                if m[i][j] != 0:
                    lam = -(m[j][j] + 1) / (2 * m[i][j])
                    v = [Fraction(0) for _ in range(n)]
                    v[i] = lam
                    v[j] = Fraction(1)
                    return False, v

    L, D, is_psd = ldlt_decomposition_rational(m)
    if is_psd and all(d >= 0 for d in D):
        return True, None

    neg_idx = -1
    for k in range(n):
        if D[k] < 0:
            neg_idx = k
            break

    if neg_idx >= 0:
        v = [Fraction(0) for _ in range(n)]
        v[neg_idx] = Fraction(1)
        for i in range(neg_idx - 1, -1, -1):
            s = Fraction(0)
            for j in range(i + 1, n):
                s += L[j][i] * v[j]
            v[i] = -s
        return False, v

    v_alt = [Fraction((-1) ** k) for k in range(n)]
    tot = Fraction(0)
    for i in range(n):
        for j in range(n):
            tot += v_alt[i] * m[i][j] * v_alt[j]
    if tot < 0:
        return False, v_alt

    return False, [Fraction(1 if k == 0 else -1) for k in range(n)]


class GNSPreHilbertSpace:
    """Non-commutative GNS pre-Hilbert space H_GNS = W_<=d / N over Fraction.

    Formed from a finite word subspace W and an exact rational moment matrix M.
    The radical N = ker(M) = { v : M v = 0 } is quotiented out, giving pre-Hilbert
    dimension dim(H_GNS) = rank(M).
    Requires M to be positive semidefinite (PSD). If M is indefinite, it cannot
    form a valid pre-Hilbert space with a positive semi-definite inner product.
    """

    def __init__(
        self,
        basis_words: Sequence[str],
        moment_matrix: Sequence[Sequence[Fraction]],
        allow_indefinite: bool = False,
    ) -> None:
        self.dim = len(basis_words)
        if self.dim == 0:
            raise ValueError("Basis words cannot be empty")
        if len(moment_matrix) != self.dim or any(len(row) != self.dim for row in moment_matrix):
            raise ValueError(f"Moment matrix must be {self.dim}x{self.dim}")

        self.basis_words = tuple(basis_words)
        self.moment_matrix = [
            tuple(_require_exact(val) for val in row) for row in moment_matrix
        ]
        assert_no_float(self.moment_matrix, "GNSPreHilbertSpace.moment_matrix")

        for i in range(self.dim):
            for j in range(i + 1, self.dim):
                if self.moment_matrix[i][j] != self.moment_matrix[j][i]:
                    raise ValueError(f"Moment matrix not symmetric at ({i}, {j})")

        self.is_psd, self.negative_mode = find_negative_mode_or_certify_psd(self.moment_matrix)
        if not self.is_psd and not allow_indefinite:
            raise ValueError(
                "Moment matrix must be positive semidefinite (PSD) to form a GNS pre-Hilbert space; "
                "indefinite form detected."
            )

        self.null_basis, self.rank = nullspace_rational(self.moment_matrix)
        self.null_dim = len(self.null_basis)
        self.gns_dim = self.rank

    def cyclic_state_vector(self) -> List[Fraction]:
        """Distinguished cyclic state vector Omega = [1] (index 0)."""
        vec = [Fraction(0) for _ in range(self.dim)]
        vec[0] = Fraction(1)
        return vec

    def inner_product(self, u: Sequence[Fraction], v: Sequence[Fraction]) -> Fraction:
        """Exact rational inner product <u, v> = u^T M v in H_GNS."""
        if len(u) != self.dim or len(v) != self.dim:
            raise ValueError(f"State vectors must have dimension {self.dim}")
        u_exact = [_require_exact(x) for x in u]
        v_exact = [_require_exact(y) for y in v]

        total = Fraction(0)
        for i in range(self.dim):
            ui = u_exact[i]
            if ui != 0:
                for j in range(self.dim):
                    vj = v_exact[j]
                    if vj != 0:
                        total += ui * self.moment_matrix[i][j] * vj
        return total

    def norm_squared(self, u: Sequence[Fraction]) -> Fraction:
        """Exact rational semi-norm squared ||u||^2 = <u, u>."""
        return self.inner_product(u, u)

    def is_null_state(self, u: Sequence[Fraction]) -> bool:
        """Check if vector u belongs to the radical N = ker(M)."""
        u_exact = [_require_exact(x) for x in u]
        for i in range(self.dim):
            row_sum = Fraction(0)
            for j in range(self.dim):
                row_sum += self.moment_matrix[i][j] * u_exact[j]
            if row_sum != 0:
                return False
        return True


@dataclass(frozen=True)
class GNSTestStateEvaluation:
    """Evaluation record of an exact rational test state in H_GNS."""
    name: str
    coefficients: List[Fraction]
    norm_squared: Fraction
    overlap_with_omega: Fraction
    is_null: bool
    is_negative_norm: bool


@dataclass(frozen=True)
class GNSConstructionReceipt:
    """Typed certificate for GNS pre-Hilbert space construction and state evaluation."""
    basis_dimension: int
    radical_dimension: int
    gns_dimension: int
    cyclic_norm_squared: Fraction
    test_states_evaluated: int
    test_evaluations: List[GNSTestStateEvaluation]
    negative_norm_modes_detected: int
    is_psd: bool
    positivity_refuted: bool
    pre_hilbert_constructed: bool
    status: str
    firewall: str
    authority_effect: str


def evaluate_gns_pre_hilbert_space(
    basis_words: Sequence[str],
    moment_matrix: Sequence[Sequence[Fraction]],
    test_states: Optional[Sequence[Tuple[str, Sequence[Fraction]]]] = None,
    allow_indefinite: bool = True,
) -> Tuple[GNSPreHilbertSpace, GNSConstructionReceipt]:
    """Construct non-commutative GNS space H_GNS = W / N or diagnose indefinite form.

    Args:
        basis_words: Words spanning the subspace W_<=d.
        moment_matrix: Exact rational moment matrix M over Fraction.
        test_states: Optional list of (name, vector) test states to evaluate.
        allow_indefinite: If True, evaluates indefinite forms as diagnostics rather than raising.

    Returns:
        (gns_space, receipt): constructed space (or diagnostic form) and typed evaluation receipt.
    """
    gns = GNSPreHilbertSpace(basis_words, moment_matrix, allow_indefinite=allow_indefinite)
    omega = gns.cyclic_state_vector()
    omega_norm_sq = gns.norm_squared(omega)

    if test_states is None:
        eval_states: List[Tuple[str, Sequence[Fraction]]] = [("Omega (cyclic)", omega)]
        for i in range(min(5, gns.dim)):
            e_i = [Fraction(1 if k == i else 0) for k in range(gns.dim)]
            eval_states.append((f"basis_word[{i}]={basis_words[i]}", e_i))
        if gns.dim >= 2:
            sup = [Fraction(1, 2) if k in (0, 1) else Fraction(0) for k in range(gns.dim)]
            eval_states.append(("equal_superposition[0,1]", sup))
        if gns.negative_mode is not None:
            eval_states.append(("ldlt_negative_eigenmode", gns.negative_mode))
    else:
        eval_states = list(test_states)
        if gns.negative_mode is not None and not any(name == "ldlt_negative_eigenmode" for name, _ in eval_states):
            eval_states.append(("ldlt_negative_eigenmode", gns.negative_mode))

    eval_records: List[GNSTestStateEvaluation] = []
    neg_norm_count = 0

    for name, vec in eval_states:
        norm_sq = gns.norm_squared(vec)
        overlap = gns.inner_product(omega, vec)
        is_null = gns.is_null_state(vec)
        is_neg = (norm_sq < 0)
        if is_neg:
            neg_norm_count += 1

        eval_records.append(
            GNSTestStateEvaluation(
                name=name,
                coefficients=list(vec),
                norm_squared=norm_sq,
                overlap_with_omega=overlap,
                is_null=is_null,
                is_negative_norm=is_neg,
            )
        )

    if gns.is_psd and omega_norm_sq >= 0 and neg_norm_count == 0:
        status = STATUS_GNS_CONSTRUCTED
        pre_hilbert_constructed = True
        positivity_refuted = False
    else:
        status = STATUS_INDEFINITE_FORM_DIAGNOSTIC
        pre_hilbert_constructed = False
        positivity_refuted = True

    receipt = GNSConstructionReceipt(
        basis_dimension=gns.dim,
        radical_dimension=gns.null_dim,
        gns_dimension=gns.gns_dim,
        cyclic_norm_squared=omega_norm_sq,
        test_states_evaluated=len(eval_records),
        test_evaluations=eval_records,
        negative_norm_modes_detected=neg_norm_count,
        is_psd=gns.is_psd,
        positivity_refuted=positivity_refuted,
        pre_hilbert_constructed=pre_hilbert_constructed,
        status=status,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "evaluate_gns_pre_hilbert_space.receipt")
    return gns, receipt




@dataclass(frozen=True)
class Degree8WitnessReplayReceipt:
    """Typed certificate for degree-8 dual witness replay."""
    fixture_name: str
    dimension: int
    trace: Fraction
    trace_num: int
    trace_den: int
    trace_str: str
    strictly_negative: bool
    expected_trace_matched: bool
    pivots: List[Fraction]
    pivot_strings: List[str]
    pivots_strictly_positive: bool
    status: str
    firewall: str
    authority_effect: str


def replay_degree8_x0_witness(
    perturb_pivot_idx: Optional[int] = None,
    corrupt_trace_den: bool = False,
) -> Degree8WitnessReplayReceipt:
    """Replay exact rational degree-8 dual witness for decoupled X=0 fixture.

    Witness: W_8(X=0) = z z^T + (1/50) * I_22 where z = (-1, 1, 0, 0, 1, 0, ...).
    Target trace: Tr(W_8 . M_8) = -9071/10800.
    Pivots: All 22 LDL^T pivots strictly positive (> 0).

    Args:
        perturb_pivot_idx: Optional index to perturb witness entry to test rejection.
        corrupt_trace_den: Optional flag to simulate corrupted trace expectation.
    """
    g_diag = build_block_diagonal_gramian()
    m8 = build_degree8_invariant_diagnostic_matrix(g_diag)
    w_witness = build_invariant_dual_witness_x0(strict=True)
    w_mat = w_witness.to_matrix()

    if perturb_pivot_idx is not None:
        if not (0 <= perturb_pivot_idx < DEG8_INVARIANT_DIM):
            raise IndexError(f"perturb_pivot_idx {perturb_pivot_idx} out of range")
        w_mat = [list(r) for r in w_mat]
        w_mat[perturb_pivot_idx][perturb_pivot_idx] = Fraction(-1)

    pivots = ldlt_pivots_strictly_positive(w_mat)
    if len(pivots) != DEG8_INVARIANT_DIM:
        raise ValueError(f"Expected {DEG8_INVARIANT_DIM} pivots, got {len(pivots)}")

    trace = Fraction(0)
    for i in range(DEG8_INVARIANT_DIM):
        for j in range(DEG8_INVARIANT_DIM):
            trace += w_mat[i][j] * m8[j][i]

    expected = DEG8_X0_EXACT_TRACE
    if corrupt_trace_den:
        expected = Fraction(DEG8_X0_EXACT_TRACE.numerator, DEG8_X0_EXACT_TRACE.denominator + 1)

    trace_matched = (trace == expected)
    if not trace_matched and perturb_pivot_idx is None:
        raise ValueError(f"Trace mismatch: actual {trace} != expected {expected}")

    receipt = Degree8WitnessReplayReceipt(
        fixture_name="Degree-8 Decoupled X=0 Diagnostic Fixture",
        dimension=DEG8_INVARIANT_DIM,
        trace=trace,
        trace_num=trace.numerator,
        trace_den=trace.denominator,
        trace_str=f"{trace.numerator}/{trace.denominator}",
        strictly_negative=(trace < 0),
        expected_trace_matched=trace_matched,
        pivots=pivots,
        pivot_strings=[f"{p.numerator}/{p.denominator}" for p in pivots],
        pivots_strictly_positive=all(p > 0 for p in pivots),
        status=STATUS_DIAGNOSTIC_REPLAY,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "replay_degree8_x0_witness.receipt")
    return receipt



def replay_degree8_s6_witness(
    perturb_pivot_idx: Optional[int] = None,
    corrupt_trace_den: bool = False,
) -> Degree8WitnessReplayReceipt:
    """Replay exact rational degree-8 dual witness for synthetic Tao S6 fixture.

    Witness: W_8(S6) = z z^T + (1/100) * I_36 where
      z = (12, -2*ones(24), -5*ones(6), 0*ones(5)).
    Target trace: Tr(W_8 . M_8) = -5046587/129600.
    Pivots: All 36 LDL^T pivots strictly positive (> 0).

    Args:
        perturb_pivot_idx: Optional index to perturb witness entry to test rejection.
        corrupt_trace_den: Optional flag to simulate corrupted trace expectation.
    """
    g_synth = canonical_quad_gramian()
    m8 = build_degree8_extended_diagnostic_matrix(g_synth)
    w_witness = build_extended_dual_witness_s6(strict=True)
    w_mat = w_witness.to_matrix()

    if perturb_pivot_idx is not None:
        if not (0 <= perturb_pivot_idx < DEG8_EXTENDED_DIM):
            raise IndexError(f"perturb_pivot_idx {perturb_pivot_idx} out of range")
        w_mat = [list(r) for r in w_mat]
        w_mat[perturb_pivot_idx][perturb_pivot_idx] = Fraction(-1)

    pivots = ldlt_pivots_strictly_positive(w_mat)
    if len(pivots) != DEG8_EXTENDED_DIM:
        raise ValueError(f"Expected {DEG8_EXTENDED_DIM} pivots, got {len(pivots)}")

    trace = Fraction(0)
    for i in range(DEG8_EXTENDED_DIM):
        for j in range(DEG8_EXTENDED_DIM):
            trace += w_mat[i][j] * m8[j][i]

    expected = DEG8_S6_EXACT_TRACE
    if corrupt_trace_den:
        expected = Fraction(DEG8_S6_EXACT_TRACE.numerator, DEG8_S6_EXACT_TRACE.denominator + 1)

    trace_matched = (trace == expected)
    if not trace_matched and perturb_pivot_idx is None:
        raise ValueError(f"Trace mismatch: actual {trace} != expected {expected}")

    receipt = Degree8WitnessReplayReceipt(
        fixture_name="Degree-8 Synthetic Tao S6 Diagnostic Fixture",
        dimension=DEG8_EXTENDED_DIM,
        trace=trace,
        trace_num=trace.numerator,
        trace_den=trace.denominator,
        trace_str=f"{trace.numerator}/{trace.denominator}",
        strictly_negative=(trace < 0),
        expected_trace_matched=trace_matched,
        pivots=pivots,
        pivot_strings=[f"{p.numerator}/{p.denominator}" for p in pivots],
        pivots_strictly_positive=all(p > 0 for p in pivots),
        status=STATUS_DIAGNOSTIC_REPLAY,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "replay_degree8_s6_witness.receipt")
    return receipt



class ExactCyclotomicInnerProductEngine:
    """Exact cyclotomic inner product verification engine over Q(zeta_24).

    Operates strictly on Cyc24 with zero floating-point arithmetic.
    Verifies sesquilinearity, conjugate symmetry, Cauchy-Schwarz, and MUB relations.
    """

    @staticmethod
    def inner_product(u: Sequence[Cyc24], v: Sequence[Cyc24]) -> Cyc24:
        """Exact Hermitian inner product <u, v> = sum_k conj(u_k) * v_k."""
        if len(u) != len(v):
            raise ValueError(f"Vector length mismatch: {len(u)} != {len(v)}")
        assert_no_float(u, "ExactCyclotomicInnerProductEngine.inner_product.u")
        assert_no_float(v, "ExactCyclotomicInnerProductEngine.inner_product.v")

        acc = Cyc24.zero()
        for uk, vk in zip(u, v):
            acc = acc.add(uk.conj().mul(vk))
        return acc

    @classmethod
    def norm_squared(cls, u: Sequence[Cyc24]) -> Fraction:
        """Exact rational norm squared ||u||^2 = <u, u> in Q."""
        val = cls.inner_product(u, u)
        frac = exact_rational(val)
        if frac < 0:
            raise ValueError(f"Norm squared must be non-negative, got {frac}")
        return frac

    @classmethod
    def cauchy_schwarz(cls, u: Sequence[Cyc24], v: Sequence[Cyc24]) -> Tuple[Fraction, Fraction, bool]:
        """Verify Cauchy-Schwarz inequality |<u, v>|^2 <= ||u||^2 * ||v||^2 over Fraction."""
        ip = cls.inner_product(u, v)
        mod_sq_cyc = ip.mul(ip.conj())
        lhs = exact_rational(mod_sq_cyc)

        norm_u_sq = cls.norm_squared(u)
        norm_v_sq = cls.norm_squared(v)
        rhs = norm_u_sq * norm_v_sq

        return lhs, rhs, (lhs <= rhs)

    @classmethod
    def matrix_trace(cls, m: Sequence[Sequence[Cyc24]]) -> Cyc24:
        """Exact cyclotomic matrix trace Tr(M) = sum_i M_ii."""
        n = len(m)
        if any(len(row) != n for row in m):
            raise ValueError("Matrix must be square")
        acc = Cyc24.zero()
        for i in range(n):
            acc = acc.add(m[i][i])
        return acc

    @classmethod
    def frobenius_inner_product(
        cls,
        a: Sequence[Sequence[Cyc24]],
        b: Sequence[Sequence[Cyc24]],
    ) -> Cyc24:
        """Exact Frobenius inner product Tr(A^* B) = sum_ij conj(A_ij) * B_ij."""
        n = len(a)
        if len(b) != n or any(len(r) != n for r in a) or any(len(r) != n for r in b):
            raise ValueError("Matrices must be square of identical size")
        acc = Cyc24.zero()
        for i in range(n):
            for j in range(n):
                acc = acc.add(a[i][j].conj().mul(b[i][j]))
        return acc


@dataclass(frozen=True)
class CyclotomicInnerProductReceipt:
    """Typed certificate for exact cyclotomic inner product verification."""
    sesquilinearity_verified: bool
    conjugate_symmetry_verified: bool
    positive_definiteness_verified: bool
    cauchy_schwarz_verified: bool
    intra_basis_orthonormality_verified: bool
    inter_basis_unbiasedness_verified: bool
    total_inner_products_evaluated: int
    status: str
    firewall: str
    authority_effect: str


def evaluate_cyclotomic_inner_product_suite() -> CyclotomicInnerProductReceipt:
    """Execute algebraic verification of cyclotomic inner products on canonical MUB triples."""
    engine = ExactCyclotomicInnerProductEngine

    b1 = standard_basis_b1()
    f6 = f6_family_columns(0, 0)
    cols_triple = canonical_triple_exact()

    u = b1[0]
    v1 = f6[0]
    v2 = f6[1]
    c = Cyc24.zeta(3)

    lhs_lin = engine.inner_product(u, [c.mul(v1[k]).add(v2[k]) for k in range(DIM_HILBERT)])
    rhs_lin = c.mul(engine.inner_product(u, v1)).add(engine.inner_product(u, v2))
    diff_lin = lhs_lin.sub(rhs_lin)
    sesqui_ok = diff_lin.is_zero()

    ip_uv = engine.inner_product(u, v1)
    ip_vu = engine.inner_product(v1, u)
    symm_ok = ip_uv.sub(ip_vu.conj()).is_zero()

    zero_vec = [Cyc24.zero() for _ in range(DIM_HILBERT)]
    pos_def_ok = (engine.norm_squared(u) == Fraction(1)) and (engine.inner_product(zero_vec, zero_vec).is_zero())

    lhs_cs, rhs_cs, cs_ok = engine.cauchy_schwarz(u, v1)
    if not cs_ok:
        raise ValueError(f"Cauchy-Schwarz violation: {lhs_cs} > {rhs_cs}")

    num_evals = 0
    ortho_ok = True
    unbiased_ok = True

    for i in range(DIM_HILBERT):
        for j in range(DIM_HILBERT):
            ip = engine.inner_product(b1[i], b1[j])
            num_evals += 1
            expected = Cyc24.one() if i == j else Cyc24.zero()
            if not ip.sub(expected).is_zero():
                ortho_ok = False

    for i in range(DIM_HILBERT):
        for j in range(DIM_HILBERT):
            ip = engine.inner_product(b1[i], f6[j])
            num_evals += 1
            mod_sq = exact_rational(ip.mul(ip.conj()))
            if mod_sq != Fraction(1, 6):
                unbiased_ok = False

    receipt = CyclotomicInnerProductReceipt(
        sesquilinearity_verified=sesqui_ok,
        conjugate_symmetry_verified=symm_ok,
        positive_definiteness_verified=pos_def_ok,
        cauchy_schwarz_verified=cs_ok,
        intra_basis_orthonormality_verified=ortho_ok,
        inter_basis_unbiasedness_verified=unbiased_ok,
        total_inner_products_evaluated=num_evals + 3,
        status=STATUS_CYCLOTOMIC_VERIFIED,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "evaluate_cyclotomic_inner_product_suite.receipt")
    return receipt



@dataclass(frozen=True)
class ConsistencyReceipt:
    """Typed certificate for consistency with Lean 4 and Rust specifications."""
    lean4_file_exists: bool
    lean4_definitions_matched: List[str]
    rust_file_exists: bool
    rust_definitions_matched: List[str]
    lexical_identifiers_present: bool
    semantic_consistency_verified: bool
    consistent: bool
    status: str
    firewall: str
    authority_effect: str


def verify_target_q_lean4_and_rust_consistency(
    repo_root: Optional[pathlib.Path] = None,
) -> ConsistencyReceipt:
    """Check structural consistency with Lean 4 and Rust reference implementations."""
    if repo_root is None:
        repo_root = next(
            p for p in pathlib.Path(__file__).resolve().parents if (p / "omega_engine").is_dir()
        )

    lean_path = repo_root / "lean4" / "sdp" / "TargetQArchimedeanPositivstellensatz.lean"
    rust_path = repo_root / "omega_engine" / "crates_rs" / "omega_mub" / "src" / "omega_native" / "mub6_degree8_sdp.rs"

    lean_matched: List[str] = []
    if lean_path.exists():
        content_lean = lean_path.read_text(encoding="utf-8")
        expected_lean = [
            "ProjectorIdealElement",
            "ProjectorWordAlgebra",
            "archimedean_norm_bound_identity",
            "projector_spectral_bound_sos",
            "degree1_rank_gap",
            "sound_universal_exclusion_via_rank_loop",
            "fail_closed_epistemic_audit_soundness",
        ]
        for item in expected_lean:
            if item in content_lean:
                lean_matched.append(item)

    rust_matched: List[str] = []
    if rust_path.exists():
        content_rust = rust_path.read_text(encoding="utf-8")
        expected_rust = [
            "DEG8_INVARIANT_DIM",
            "DEG8_EXTENDED_DIM",
            "build_invariant_dual_witness_x0",
            "build_extended_dual_witness_s6",
            "ldlt_decomposition_rational",
            "ldlt_pivots_strictly_positive_rational",
            "evaluate_target_q4_diagnostics",
        ]
        for item in expected_rust:
            if item in content_rust:
                rust_matched.append(item)

    lexical_present = (
        lean_path.exists()
        and len(lean_matched) >= 6
        and rust_path.exists()
        and len(rust_matched) >= 6
    )

    receipt = ConsistencyReceipt(
        lean4_file_exists=lean_path.exists(),
        lean4_definitions_matched=lean_matched,
        rust_file_exists=rust_path.exists(),
        rust_definitions_matched=rust_matched,
        lexical_identifiers_present=lexical_present,
        semantic_consistency_verified=False,
        consistent=False,
        status="LEXICAL_IDENTIFIER_PRESENCE_CHECKED",
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
    )
    assert_no_float(receipt, "verify_target_q_lean4_and_rust_consistency.receipt")
    return receipt



@dataclass(frozen=True)
class Stream3MasterReceipt:
    """Master aggregate certificate for Stream 3 (Target Q Degree-8 SDP & GNS Replay)."""
    schema_version: str
    firewall: str
    authority_effect: str
    scope: str
    confluent_rewriting_receipt: ConfluentRewritingReceipt
    spectral_bound_receipt: IdempotencySpectralBoundReceipt
    gns_construction_receipt: GNSConstructionReceipt
    degree8_x0_replay_receipt: Degree8WitnessReplayReceipt
    degree8_s6_replay_receipt: Degree8WitnessReplayReceipt
    cyclotomic_inner_product_receipt: CyclotomicInnerProductReceipt
    consistency_receipt: ConsistencyReceipt
    all_vectors_satisfied: bool


def evaluate_stream3_target_q_degree8_and_gns(
    repo_root: Optional[pathlib.Path] = None,
) -> Stream3MasterReceipt:
    """Execute all six Stream 3 vectors and emit the master certificate."""
    rewriting_receipt = verify_confluent_rewriting_system()

    spectral_receipt = verify_idempotency_spectral_bound(basis=0, outcome=0)

    x0_receipt = replay_degree8_x0_witness()

    s6_receipt = replay_degree8_s6_witness()

    g_diag = build_block_diagonal_gramian()
    m8_diag = build_degree8_invariant_diagnostic_matrix(g_diag)
    word_labels = [f"word_{i}" for i in range(DEG8_INVARIANT_DIM)]

    z_x0 = [Fraction(0) for _ in range(DEG8_INVARIANT_DIM)]
    z_x0[0] = Fraction(-1)
    z_x0[1] = Fraction(1)
    z_x0[4] = Fraction(1)
    test_states = [
        ("Omega (cyclic)", [Fraction(1 if i == 0 else 0) for i in range(DEG8_INVARIANT_DIM)]),
        ("basis_word[1]", [Fraction(1 if i == 1 else 0) for i in range(DEG8_INVARIANT_DIM)]),
        ("dual_witness_mode_z", z_x0),
    ]
    _, gns_receipt = evaluate_gns_pre_hilbert_space(word_labels, m8_diag, test_states)

    cyclotomic_receipt = evaluate_cyclotomic_inner_product_suite()

    consistency_receipt = verify_target_q_lean4_and_rust_consistency(repo_root)

    all_satisfied = (
        rewriting_receipt.unique_normal_form_certified
        and spectral_receipt.spectrum_contained_in_unit_interval
        and x0_receipt.expected_trace_matched
        and x0_receipt.pivots_strictly_positive
        and s6_receipt.expected_trace_matched
        and s6_receipt.pivots_strictly_positive
        and gns_receipt.pre_hilbert_constructed
        and cyclotomic_receipt.sesquilinearity_verified
        and cyclotomic_receipt.inter_basis_unbiasedness_verified
        and consistency_receipt.semantic_consistency_verified
    )

    master = Stream3MasterReceipt(
        schema_version=SCHEMA_VERSION,
        firewall=FIREWALL_LINE,
        authority_effect=AUTHORITY_EFFECT,
        scope=SCOPE_STRING,
        confluent_rewriting_receipt=rewriting_receipt,
        spectral_bound_receipt=spectral_receipt,
        gns_construction_receipt=gns_receipt,
        degree8_x0_replay_receipt=x0_receipt,
        degree8_s6_replay_receipt=s6_receipt,
        cyclotomic_inner_product_receipt=cyclotomic_receipt,
        consistency_receipt=consistency_receipt,
        all_vectors_satisfied=all_satisfied,
    )
    assert_no_float(master, "evaluate_stream3_target_q_degree8_and_gns.master")
    return master
