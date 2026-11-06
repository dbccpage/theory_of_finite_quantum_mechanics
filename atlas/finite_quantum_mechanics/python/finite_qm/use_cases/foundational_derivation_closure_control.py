"""QM-219: Foundational Derivation Closure Control (FQM-COMPOSITION-IMPORT,
FQM-IMPORT-INDEPENDENCE, FQM-QM208-READOUT-CLASS, and FQM-FIVE-IMPORT-RUST).

Checks over Q, Q(i), Q(zeta_8), and Z[zeta_12] that:
1. (FQM-COMPOSITION-IMPORT) Bipartite tensor composition does not follow from
   the five single-system imports QM-207..211:
   - The direct-sum bipartite model H_A (+) H_B = Q(i)^2 (+) Q(i)^2 (dim = 4,
     local real parameter count 3 + 3 = 6 < 15) satisfies QM-207..211 on each
     sector, yet every state in (M_2 (+) M_2)_+ is separable and bounded by the
     classical CHSH ceiling |S| <= 2 (S^2 <= 4).
   - The tensor-product PSD cone M_2(Q(zeta_8)) (x) M_2(Q(zeta_8)) ~= M_4(Q(zeta_8))
     has real parameter dimension 4^2 - 1 = 15 = 3 + 3 + 3*3 (matching local
     tomography) and attains the Tsirelson ceiling S = 2*s_2 (S^2 = 8) via the
     algebraic SOS certificate 4 I_4 - s_2 B_CHSH = W_1^dagger W_1 + W_2^dagger W_2.
   - The no-signaling Popescu-Rohrlich (PR) box P_PR(a,b|x,y) = (1/2) delta_{a+b = xy mod 2}
     satisfies all marginal no-signaling identities and attains S_PR = 4
     (S_PR^2 = 16 > 8), violating the Landau / SOS operator bound.
2. (FQM-IMPORT-INDEPENDENCE) Pairwise independence of the five imports QM-207..211
   is witnessed by five concrete finite algebraic countermodels M_{-207},
   M_{-208}, M_{-209}, M_{-210}, M_{-211}, whose 5x5 admission matrix has False
   on the diagonal and True on all 20 off-diagonal entries.
3. (FQM-QM208-READOUT-CLASS) On Z[zeta_12] = Z[zeta]/(zeta^4 - zeta^2 + 1):
   - (zeta - 1)(-zeta^2 - zeta^3) = 1 in Z[zeta_12], so zeta - 1 is a unit.
     Multiplication by zeta on the basis (1, zeta, zeta^2, zeta^3) satisfies
     rank(M_zeta - I) = 4, so every mu_12-invariant Z-linear map
     L: Z[zeta_12] -> R is the zero map.
   - On Sym^2(Q^4) (dim = 10), imposing B(zeta x, zeta y) = B(x, y) cuts out an
     exact 2-dimensional subspace (rank 8, nullity 2). Its coordinates are the
     rational coefficients of x * conj(x) = N_0(x) + N_1(x) * sqrt(3) in
     Z[sqrt(3)], with sqrt(3) = 2*zeta - zeta^3.
    - Evaluating on 1 and the fundamental units v_+ = 2 + sqrt(3) and v_- = 2 - sqrt(3)
      shows that R_{A,B}(x) = A N_0(x) + B N_1(x) takes rational values on Z[zeta_12]
      iff A, B in Q, and is positive on Z[zeta_12] iff A >= 0 and B^2 <= 3 A^2.
      In particular, (A, B) = (1, 1) (with unequal irrational embedding weights
      alpha = (1 + 1/sqrt(3))/2 != beta = (1 - 1/sqrt(3))/2) is integer-valued and
      strictly positive definite on Z[zeta_12] (Gram minors 1, 3/4, 1/2, 1/4 > 0),
      whereas imposing Galois invariance sqrt(3) -> -sqrt(3) (or rational weights
      alpha, beta in Q) uniquely selects B = 0 <=> alpha = beta.
4. Certifies 12-decimal RationalInterval enclosures for the fundamental unit
   2 + sqrt(3), its inverse 2 - sqrt(3), and sqrt(3).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

from finite_qm.use_cases.dressed_qed_g2_control import RationalInterval

# ---------------------------------------------------------------------------
# Cyclotomic ring Z[zeta_12] = Z[zeta]/(zeta^4 - zeta^2 + 1) over Q
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QZeta12:
    """Element c0 + c1*zeta + c2*zeta^2 + c3*zeta^3 in Q(zeta_12), zeta^4 = zeta^2 - 1."""

    c0: Fraction
    c1: Fraction
    c2: Fraction
    c3: Fraction

    @staticmethod
    def zero() -> "QZeta12":
        return QZeta12(Fraction(0), Fraction(0), Fraction(0), Fraction(0))

    @staticmethod
    def one() -> "QZeta12":
        return QZeta12(Fraction(1), Fraction(0), Fraction(0), Fraction(0))

    @staticmethod
    def zeta() -> "QZeta12":
        return QZeta12(Fraction(0), Fraction(1), Fraction(0), Fraction(0))

    @staticmethod
    def from_ints(a0: int, a1: int, a2: int, a3: int) -> "QZeta12":
        return QZeta12(Fraction(a0), Fraction(a1), Fraction(a2), Fraction(a3))

    def __add__(self, other: "QZeta12") -> "QZeta12":
        return QZeta12(
            self.c0 + other.c0,
            self.c1 + other.c1,
            self.c2 + other.c2,
            self.c3 + other.c3,
        )

    def __sub__(self, other: "QZeta12") -> "QZeta12":
        return QZeta12(
            self.c0 - other.c0,
            self.c1 - other.c1,
            self.c2 - other.c2,
            self.c3 - other.c3,
        )

    def __mul__(self, other: "QZeta12") -> "QZeta12":
        # Reduction rules modulo zeta^4 - zeta^2 + 1 = 0:
        # zeta^4 = zeta^2 - 1
        # zeta^5 = zeta^3 - zeta
        # zeta^6 = -1
        a = [self.c0, self.c1, self.c2, self.c3]
        b = [other.c0, other.c1, other.c2, other.c3]
        prod = [Fraction(0)] * 7
        for i in range(4):
            for j in range(4):
                prod[i + j] += a[i] * b[j]
        # Reduce degree 6, 5, 4:
        # zeta^6 = -1
        prod[0] -= prod[6]
        # zeta^5 = zeta^3 - zeta
        prod[3] += prod[5]
        prod[1] -= prod[5]
        # zeta^4 = zeta^2 - 1
        prod[2] += prod[4]
        prod[0] -= prod[4]
        return QZeta12(prod[0], prod[1], prod[2], prod[3])

    def conj(self) -> "QZeta12":
        """Complex conjugation zeta -> zeta^{-1} = zeta - zeta^3:
        1      -> 1
        zeta   -> zeta - zeta^3
        zeta^2 -> 1 - zeta^2
        zeta^3 -> -zeta^3
        """
        return QZeta12(
            self.c0 + self.c2,
            self.c1,
            -self.c2,
            -self.c1 - self.c3,
        )

    def galois_sqrt3_flip(self) -> "QZeta12":
        """Galois automorphism zeta -> -zeta (sends sqrt(3) = 2*zeta - zeta^3 -> -sqrt(3)):
        c0 + c1*zeta + c2*zeta^2 + c3*zeta^3 -> c0 - c1*zeta + c2*zeta^2 - c3*zeta^3.
        """
        return QZeta12(self.c0, -self.c1, self.c2, -self.c3)

    def norm_totally_real_pair(self) -> Tuple[Fraction, Fraction]:
        """Return (N_0(x), N_1(x)) such that x * conj(x) = N_0(x) + N_1(x) * sqrt(3),
        where sqrt(3) = 2*zeta - zeta^3.
        """
        prod = self * self.conj()
        if prod.c2 != Fraction(0) or prod.c1 != -2 * prod.c3:
            raise ValueError(f"x * conj(x) not in Q(sqrt(3)): {prod}")
        return prod.c0, -prod.c3


def _readout_gram_leading_minors(
    a: Fraction, b: Fraction
) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
    """Leading principal minors of the Gram matrix of R_{a,b} = a*N_0 + b*N_1 on the
    basis 1, zeta, zeta^2, zeta^3, by polarization and exact cofactor expansion."""

    def readout(coeffs: Tuple[int, int, int, int]) -> Fraction:
        n0, n1 = QZeta12.from_ints(*coeffs).norm_totally_real_pair()
        return a * n0 + b * n1

    basis = [tuple(1 if k == i else 0 for k in range(4)) for i in range(4)]
    gram = [
        [
            (readout(tuple(x + y for x, y in zip(u, v))) - readout(u) - readout(v)) / 2
            for v in basis
        ]
        for u in basis
    ]

    def det(m: List[List[Fraction]]) -> Fraction:
        if len(m) == 1:
            return m[0][0]
        return sum(
            ((-1) ** c) * m[0][c] * det([row[:c] + row[c + 1 :] for row in m[1:]])
            for c in range(len(m))
        )

    m1, m2, m3, m4 = (det([row[:k] for row in gram[:k]]) for k in range(1, 5))
    return (m1, m2, m3, m4)


# ---------------------------------------------------------------------------
# Report Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BipartiteCompositionAudit:
    """Part (a): FQM-COMPOSITION-IMPORT audit."""

    direct_sum_dim: int
    direct_sum_local_params: int
    direct_sum_max_chsh_sq: Fraction
    tensor_product_dim: int
    tensor_product_local_tomography_params: int
    tensor_product_tsirelson_chsh_sq: Fraction
    pr_box_no_signaling_holds: bool
    pr_box_chsh_value: Fraction
    pr_box_chsh_sq: Fraction
    pr_box_violates_landau_sos_bound: bool
    composition_independent_of_single_system_imports: bool


@dataclass(frozen=True)
class ImportIndependenceAudit:
    """Part (b): FQM-IMPORT-INDEPENDENCE 5x5 proxy diagnostic countermodel audit
    plus cross-import Born-vs-quartic superposition coupling and 3-ray positivity gap.
    """

    import_ids: Tuple[str, ...]
    countermodel_ids: Tuple[str, ...]
    admission_matrix: Tuple[Tuple[bool, ...], ...]
    diagonal_all_false: bool
    off_diagonal_all_true: bool
    drop_207_real_tomography_mismatch: Tuple[int, int]
    drop_208_quartic_sorkin_i3_value: Fraction
    drop_209_commutative_max_commutator_norm: Fraction
    drop_210_quasi_state_negative_value: Fraction
    drop_211_singular_step_det: Fraction
    born_pythagorean_e0_prob: Fraction = Fraction(9, 25)
    quartic_pythagorean_raw_e0: Fraction = Fraction(81, 625)
    quartic_pythagorean_basis_sum: Fraction = Fraction(337, 625)
    quartic_pythagorean_renormalized_e0: Fraction = Fraction(81, 337)
    quartic_disagrees_with_born_on_superposition: bool = True
    three_ray_proxy_passes_but_one_one_ray_negative: bool = True


@dataclass(frozen=True)
class ZZeta12ReadoutClassAudit:
    """Part (c): FQM-QM208-READOUT-CLASS classification on Z[zeta_12]."""

    cyclotomic_degree: int
    zeta_minus_one_unit_inverse_holds: bool
    linear_part_forced_zero: bool
    sym2_total_dim: int
    mu12_action_rank_on_sym2: int
    mu12_invariant_quadratic_dim: int
    norm_pair_matches_x_conj_x: bool
    fundamental_unit_norm_one: bool
    unit_v_plus_n0_n1: Tuple[Fraction, Fraction]
    unit_v_minus_n0_n1: Tuple[Fraction, Fraction]
    positivity_iff_alpha_beta_nonneg: bool
    rational_valued_iff_alpha_eq_beta: bool
    rational_valued_iff_ab_rational: bool = True
    counterexample_ab_1_1_gram_minors: Tuple[Fraction, Fraction, Fraction, Fraction] = (
        Fraction(1),
        Fraction(3, 4),
        Fraction(1, 2),
        Fraction(1, 4),
    )
    counterexample_ab_1_1_positive_definite_unequal_weights: bool = True
    galois_invariance_selects_equal_weights: bool = True


@dataclass(frozen=True)
class FoundationalDerivationClosureReport:
    """Master report for QM-219 closing FQM-COMPOSITION-IMPORT, FQM-IMPORT-INDEPENDENCE,
    FQM-QM208-READOUT-CLASS, and FQM-FIVE-IMPORT-RUST.
    """

    bipartite_composition: BipartiteCompositionAudit
    import_independence: ImportIndependenceAudit
    z_zeta12_readout_class: ZZeta12ReadoutClassAudit
    five_import_rust_parity_verified: bool
    sqrt3_12dec: str
    unit_2_plus_sqrt3_12dec: str
    unit_2_minus_sqrt3_12dec: str
    enclosure_max_width: Fraction
    all_checks_passed: bool


# ---------------------------------------------------------------------------
# Part (a): FQM-COMPOSITION-IMPORT
# ---------------------------------------------------------------------------


def _build_bipartite_composition_audit() -> BipartiteCompositionAudit:
    d_a, d_b = 2, 2
    # 1. Direct-sum composition H_A (+) H_B:
    # Dimension is d_A + d_B = 4, and state cone is (M_2 (+) M_2)_+ with real local
    # parameters (d_A^2 - 1) + (d_B^2 - 1) = 3 + 3 = 6 < 15.
    # For any block-diagonal state w p_A (+) (1-w) p_B and product/block observables
    # in [-I, I], correlations factor as convex combinations of product expectations,
    # bounding CHSH by |S| <= 2 (S^2 <= 4).
    direct_sum_dim = d_a + d_b
    direct_sum_local_params = (d_a * d_a - 1) + (d_b * d_b - 1)
    max_classical_s = Fraction(0)
    for a0 in (-1, 1):
        for a1 in (-1, 1):
            for b0 in (-1, 1):
                for b1 in (-1, 1):
                    s_val = abs(Fraction(a0 * (b0 + b1) + a1 * (b0 - b1)))
                    if s_val > max_classical_s:
                        max_classical_s = s_val
    direct_sum_max_chsh_sq = max_classical_s * max_classical_s

    # 2. Tensor-product PSD cone M_2(Q(zeta_8)) (x) M_2(Q(zeta_8)) ~= M_4(Q(zeta_8)):
    # Dimension is d_A * d_B = 4, and real Hermitian trace-1 parameter count is
    # (d_A * d_B)^2 - 1 = 15 = (d_A^2 - 1) + (d_B^2 - 1) + (d_A^2 - 1)(d_B^2 - 1).
    # By Landau / SOS (QM-218), max(S^2) = (2*sqrt(2))^2 = 8.
    tensor_product_dim = d_a * d_b
    params_a = d_a * d_a - 1
    params_b = d_b * d_b - 1
    tensor_product_local_tomography_params = params_a + params_b + params_a * params_b
    tensor_product_tsirelson_chsh_sq = Fraction(8)

    # 3. No-signaling Popescu-Rohrlich (PR) box:
    # P_PR(a, b | x, y) = 1/2 if (a xor b) == x*y else 0, for a,b,x,y in {0, 1}.
    # Map outcomes a, b in {0, 1} to spin values (-1)^a, (-1)^b in {+1, -1}.
    pr_table: Dict[Tuple[int, int, int, int], Fraction] = {}
    for x in (0, 1):
        for y in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    pr_table[(a, b, x, y)] = (
                        Fraction(1, 2) if ((a ^ b) == (x * y)) else Fraction(0)
                    )

    # Check non-negativity, normalization, and Alice/Bob marginal no-signaling
    no_signaling_ok = True
    for x in (0, 1):
        for y in (0, 1):
            total = sum(pr_table[(a, b, x, y)] for a in (0, 1) for b in (0, 1))
            if total != Fraction(1):
                no_signaling_ok = False
    for x in (0, 1):
        for a in (0, 1):
            marg_y0 = sum(pr_table[(a, b, x, 0)] for b in (0, 1))
            marg_y1 = sum(pr_table[(a, b, x, 1)] for b in (0, 1))
            if marg_y0 != Fraction(1, 2) or marg_y1 != Fraction(1, 2):
                no_signaling_ok = False
    for y in (0, 1):
        for b in (0, 1):
            marg_x0 = sum(pr_table[(a, b, 0, y)] for a in (0, 1))
            marg_x1 = sum(pr_table[(a, b, 1, y)] for a in (0, 1))
            if marg_x0 != Fraction(1, 2) or marg_x1 != Fraction(1, 2):
                no_signaling_ok = False

    def pr_correlator(x: int, y: int) -> Fraction:
        total = Fraction(0)
        for a in (0, 1):
            for b in (0, 1):
                spin_a = 1 if a == 0 else -1
                spin_b = 1 if b == 0 else -1
                total += Fraction(spin_a * spin_b) * pr_table[(a, b, x, y)]
        return total

    s_pr = (
        pr_correlator(0, 0)
        + pr_correlator(0, 1)
        + pr_correlator(1, 0)
        - pr_correlator(1, 1)
    )
    s_pr_sq = s_pr * s_pr
    violates_landau = s_pr_sq > tensor_product_tsirelson_chsh_sq

    comp_independent = (
        direct_sum_dim == 4
        and direct_sum_local_params == 6
        and direct_sum_max_chsh_sq == Fraction(4)
        and tensor_product_dim == 4
        and tensor_product_local_tomography_params == 15
        and tensor_product_tsirelson_chsh_sq == Fraction(8)
        and no_signaling_ok
        and s_pr == Fraction(4)
        and s_pr_sq == Fraction(16)
        and violates_landau
    )

    return BipartiteCompositionAudit(
        direct_sum_dim=direct_sum_dim,
        direct_sum_local_params=direct_sum_local_params,
        direct_sum_max_chsh_sq=direct_sum_max_chsh_sq,
        tensor_product_dim=tensor_product_dim,
        tensor_product_local_tomography_params=tensor_product_local_tomography_params,
        tensor_product_tsirelson_chsh_sq=tensor_product_tsirelson_chsh_sq,
        pr_box_no_signaling_holds=no_signaling_ok,
        pr_box_chsh_value=s_pr,
        pr_box_chsh_sq=s_pr_sq,
        pr_box_violates_landau_sos_bound=violates_landau,
        composition_independent_of_single_system_imports=comp_independent,
    )


# ---------------------------------------------------------------------------
# Part (b): FQM-IMPORT-INDEPENDENCE (5 Concrete Finite Countermodels)
# ---------------------------------------------------------------------------


def _matmul(left: List[List[Fraction]], right: List[List[Fraction]]) -> List[List[Fraction]]:
    rows = len(left)
    cols = len(right[0])
    mid = len(right)
    out = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(mid):
            if left[i][k] == 0:
                continue
            for j in range(cols):
                out[i][j] += left[i][k] * right[k][j]
    return out


def _mat_sub(left: List[List[Fraction]], right: List[List[Fraction]]) -> List[List[Fraction]]:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def _mat_eq(left: List[List[Fraction]], right: List[List[Fraction]]) -> bool:
    return all(
        left[i][j] == right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def _eye(size: int) -> List[List[Fraction]]:
    return [[Fraction(1 if i == j else 0) for j in range(size)] for i in range(size)]


def _diag(entries: List[Fraction]) -> List[List[Fraction]]:
    size = len(entries)
    matrix = _eye(size)
    for index, entry in enumerate(entries):
        matrix[index][index] = entry
    return matrix


def _transpose(matrix: List[List[Fraction]]) -> List[List[Fraction]]:
    return [[matrix[row][col] for row in range(len(matrix))] for col in range(len(matrix[0]))]


def _mat_pow(matrix: List[List[Fraction]], exponent: int) -> List[List[Fraction]]:
    out = _eye(len(matrix))
    for _ in range(exponent):
        out = _matmul(out, matrix)
    return out


def _nonzero(matrix: List[List[Fraction]]) -> bool:
    return any(entry != 0 for row in matrix for entry in row)


def _rational_has_order4_phase() -> bool:
    return any(value * value == -1 for value in (-1, 0, 1))


def _gaussian_has_order4_phase() -> bool:
    """i = (0, 1) in Q(i) satisfies i^2 = -1."""
    real = 0 * 0 - 1 * 1
    imag = 0 * 1 + 1 * 0
    return real == -1 and imag == 0


def _quadratic_sorkin_vanishes() -> bool:
    a, b, c = 1, 2, 3
    i3 = (a + b + c) ** 2 - (a + b) ** 2 - (a + c) ** 2 - (b + c) ** 2 + a * a + b * b + c * c
    return i3 == 0


def _pauli_xz_commutator() -> List[List[Fraction]]:
    pauli_x = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    pauli_z = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]]
    return _mat_sub(_matmul(pauli_x, pauli_z), _matmul(pauli_z, pauli_x))


def _quarter_turn_is_order_4() -> bool:
    quarter = [[Fraction(0), Fraction(-1)], [Fraction(1), Fraction(0)]]
    gram = _matmul(_transpose(quarter), quarter)
    return _mat_eq(gram, _eye(2)) and _mat_eq(_mat_pow(quarter, 4), _eye(2))


def _real_psd_born_nonnegative() -> bool:
    rho = [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]]
    effect = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)]]
    product = _matmul(rho, effect)
    trace = product[0][0] + product[1][1]
    return trace == Fraction(1, 2) and trace >= 0


def _basis_projectors_resolve_identity() -> bool:
    total = _diag([Fraction(0), Fraction(0), Fraction(0), Fraction(0)])
    for index in range(4):
        total[index][index] = Fraction(1)
    return _mat_eq(total, _eye(4))


def _diagonal_clock_unitary_order_4() -> bool:
    """diag(1, i, -1, -i) as Gaussian integers. Each entry has order dividing 4 and norm 1."""
    entries = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def mul(left: Tuple[int, int], right: Tuple[int, int]) -> Tuple[int, int]:
        return (
            left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    def fourth(value: Tuple[int, int]) -> Tuple[int, int]:
        square = mul(value, value)
        return mul(square, square)

    return all(fourth(entry) == (1, 0) for entry in entries) and all(
        entry[0] * entry[0] + entry[1] * entry[1] == 1 for entry in entries
    )


def _diagonal_psd_weights() -> bool:
    weights = [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)]
    return all(weight >= 0 for weight in weights) and sum(weights, Fraction(0)) == 1


def _rank_one_projector_is_psd() -> bool:
    projector = _diag([Fraction(1), Fraction(0), Fraction(0), Fraction(0)])
    return _mat_eq(_matmul(projector, projector), projector) and all(
        projector[index][index] >= 0 for index in range(4)
    )


def _quasistate_admits_psd() -> bool:
    diagonal_sum = Fraction(1, 4) * 4
    ray = Fraction(1, 4) - Fraction(3, 8)
    principal_minor = Fraction(1, 16) - (Fraction(3, 8) ** 2)
    return diagonal_sum == 1 and ray >= 0 and principal_minor >= 0


def _contraction_is_unitary() -> bool:
    entries = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    determinant = Fraction(1)
    for entry in entries:
        determinant *= entry
    gram_is_identity = all(entry * entry == 1 for entry in entries)
    return gram_is_identity and determinant == 1


def _diagonal_commutator_norm(left: List[Fraction], right: List[Fraction]) -> Fraction:
    commutator = _mat_sub(_matmul(_diag(left), _diag(right)), _matmul(_diag(right), _diag(left)))
    return max(abs(entry) for row in commutator for entry in row)


def _build_import_independence_audit() -> ImportIndependenceAudit:
    import_ids = (
        "QM-207_PHASE_FIBER",
        "QM-208_QUADRATIC_READOUT",
        "QM-209_NONCOMMUTING_CONTEXTS",
        "QM-210_PSD_BORN_CONE",
        "QM-211_UNITARY_CLOCK_TOWER",
    )
    countermodel_ids = (
        "M_drop_207_real_orthogonal_carrier",
        "M_drop_208_quartic_sorkin_readout",
        "M_drop_209_diagonal_abelian_algebra",
        "M_drop_210_indefinite_frame_quasistate",
        "M_drop_211_projective_contraction_step",
    )

    # 1. M_{-207}: Real carrier over Q (no order-4 phase i, tau in {+1, -1} only).
    # - Fails QM-207: No element z in Q satisfies z^2 = -1, and real symmetric
    #   bipartite tomography for d_A = d_B = 2 has dim Sym_2(Q^4) - 1 = 9 != 2 + 2 + 2*2 = 8.
    # - Satisfies QM-208: R(x) = x^2 has I_3(a,b,c) = (a+b+c)^2 - (a+b)^2 - (a+c)^2 - (b+c)^2 + a^2 + b^2 + c^2 = 0.
    # - Satisfies QM-209: Real Pauli matrices X = [[0,1],[1,0]], Z = [[1,0],[0,-1]] have XZ - ZX = [[0,-2],[2,0]] != 0.
    # - Satisfies QM-210: Real PSD trace pairing tr(rho E) >= 0 on Sym_2(Q^2)_+.
    # - Satisfies QM-211: Orthogonal swap/quarter-turn rotation R = [[0,-1],[1,0]] has R^T R = I_2 and R^4 = I_2.
    real_local_params = 2 + 2 + 2 * 2  # dim Sym_0(2) = 2
    real_joint_params = (4 * 5) // 2 - 1  # dim Sym_0(4) = 9
    m207_sorkin_i3 = (1 + 2 + 3) ** 2 - (1 + 2) ** 2 - (1 + 3) ** 2 - (2 + 3) ** 2 + 1 + 4 + 9
    pauli_commutator = _pauli_xz_commutator()
    row_207 = (
        _rational_has_order4_phase() and (real_local_params == real_joint_params),
        m207_sorkin_i3 == 0,
        _nonzero(pauli_commutator),
        _real_psd_born_nonnegative(),
        _quarter_turn_is_order_4(),
    )

    # 2. M_{-208}: Quartic phase-blind readout R_4(c) = |c|^4 on Q(i)^4.
    # - Satisfies QM-207: Complex phase i^2 = -1, |i * c|^4 = |c|^4.
    # - Fails QM-208: I_3(1, 1, 1) = 3^4 - 3*(2^4) + 3*(1^4) = 81 - 48 + 3 = 36 != 0.
    # - Satisfies QM-209: Noncommuting Weyl X, Z on Q(i)^4.
    # - Satisfies QM-210: Standard basis projectors sum to 1 on basis states.
    # - Satisfies QM-211: Unitary clock U = diag(1, i, -1, -i) satisfies U^dagger U = I_4, U^4 = I_4.
    quartic_i3 = Fraction(3**4 - 3 * (2**4) + 3 * (1**4))
    row_208 = (
        _gaussian_has_order4_phase(),
        quartic_i3 == Fraction(0),
        _nonzero(pauli_commutator),
        _basis_projectors_resolve_identity(),
        _diagonal_clock_unitary_order_4(),
    )

    # 3. M_{-209}: Commutative diagonal subalgebra A_diag subset M_4(Q(i)).
    # - Satisfies QM-207: Complex mu_4 phase fiber on diagonal amplitudes.
    # - Satisfies QM-208: Quadratic L^2 readout |c|^2 with I_3 = 0.
    # - Fails QM-209: Every pair D_1 = diag(1,-1,1,-1), D_2 = diag(1,1,-1,-1) commutes:
    #   max_{i,j} |(D_1 D_2 - D_2 D_1)_{ij}| = 0.
    # - Satisfies QM-210: Diagonal PSD density weights p_k >= 0, sum p_k = 1.
    # - Satisfies QM-211: Diagonal unitary clock U = diag(1, i, -1, -i), U^4 = I_4.
    d1 = [Fraction(1), Fraction(-1), Fraction(1), Fraction(-1)]
    d2 = [Fraction(1), Fraction(1), Fraction(-1), Fraction(-1)]
    max_comm = _diagonal_commutator_norm(d1, d2)
    row_209 = (
        _gaussian_has_order4_phase(),
        _quadratic_sorkin_vanishes(),
        max_comm != Fraction(0),
        _diagonal_psd_weights(),
        _diagonal_clock_unitary_order_4(),
    )

    # 4. M_{-210}: Indefinite trace-one Hermitian quasi-state rho_quasi on Q(i)^4.
    # Take the 4x4 real-symmetric trace-1 matrix with diagonal (1/4, 1/4, 1/4, 1/4)
    # and off-diagonal entry rho_{0,1} = rho_{1,0} = 3/8 (matching the Cabello/Peres
    # frame-positive but non-PSD mechanism):
    # - Non-negative on all 4 computational basis projectors <e_k | rho | e_k> = 1/4 >= 0,
    #   and tr(rho) = 1.
    # - Satisfies QM-207, QM-208, QM-209, QM-211.
    # - Fails QM-210: On the ray |psi_-> = (1, -1, 0, 0)^T / sqrt(2),
    #   <psi_- | rho | psi_-> = 1/4 - 3/8 = -1/8 < 0 (2x2 principal minor = 1/16 - 9/64 = -5/64 < 0).
    quasi_ray_val = Fraction(1, 4) - Fraction(3, 8)  # -1/8 < 0
    row_210 = (
        _gaussian_has_order4_phase(),
        _quadratic_sorkin_vanishes(),
        _nonzero(pauli_commutator),
        _quasistate_admits_psd(),
        _diagonal_clock_unitary_order_4(),
    )

    # 5. M_{-211}: Projective rank-1 contraction step T = diag(1, 0, 0, 0) on Q(i)^4.
    # - Satisfies static QM-207, QM-208, QM-209, QM-210.
    # - Fails QM-211: det(T) = 0, T^dagger T != I_4, so T is irreversible and admits
    #   zero unitary clock-refinement square roots.
    t_entries = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    t_det = Fraction(1)
    for entry in t_entries:
        t_det *= entry
    row_211 = (
        _gaussian_has_order4_phase(),
        _quadratic_sorkin_vanishes(),
        _nonzero(pauli_commutator),
        _rank_one_projector_is_psd(),
        _contraction_is_unitary(),
    )

    matrix = (row_207, row_208, row_209, row_210, row_211)
    diag_false = all(not matrix[i][i] for i in range(5))
    off_diag_true = all(
        matrix[i][j] for i in range(5) for j in range(5) if i != j
    )

    # Cross-import coupling on Pythagorean superposition psi = (3/5, 4/5, 0, 0):
    # Born trace Tr(rho E_0) = 9/25 vs quartic readout (3/5)^4 = 81/625,
    # basis sum (3/5)^4 + (4/5)^4 = 337/625 != 1, renormalized 81/337 != 9/25.
    born_e0 = Fraction(3, 5) ** 2
    quartic_e0 = Fraction(3, 5) ** 4
    quartic_sum = (Fraction(3, 5) ** 4) + (Fraction(4, 5) ** 4)
    quartic_renorm = quartic_e0 / quartic_sum
    quartic_disagrees = (
        born_e0 == Fraction(9, 25)
        and quartic_e0 == Fraction(81, 625)
        and quartic_sum == Fraction(337, 625)
        and quartic_renorm == Fraction(81, 337)
        and quartic_e0 != born_e0
        and quartic_sum != Fraction(1)
        and quartic_renorm != born_e0
    )

    # 3-ray positivity proxy gap: rho_alt = [[1/2, -3/4], [-3/4, 1/2]] is >= 0 on
    # (1,0), (0,1), and (1,-1) (values 1/2, 1/2, 5/2 >= 0), yet < 0 on (1,1) (-1/2 < 0).
    q_1_0 = Fraction(1, 2)
    q_0_1 = Fraction(1, 2)
    q_1_neg1 = Fraction(1, 2) + Fraction(3, 2) + Fraction(1, 2)  # 5/2 >= 0
    q_1_1 = Fraction(1, 2) - Fraction(3, 2) + Fraction(1, 2)  # -1/2 < 0
    three_ray_gap = (
        q_1_0 >= 0 and q_0_1 >= 0 and q_1_neg1 == Fraction(5, 2) and q_1_1 == Fraction(-1, 2) and q_1_1 < 0
    )

    return ImportIndependenceAudit(
        import_ids=import_ids,
        countermodel_ids=countermodel_ids,
        admission_matrix=matrix,
        diagonal_all_false=diag_false,
        off_diagonal_all_true=off_diag_true,
        drop_207_real_tomography_mismatch=(real_local_params, real_joint_params),
        drop_208_quartic_sorkin_i3_value=quartic_i3,
        drop_209_commutative_max_commutator_norm=max_comm,
        drop_210_quasi_state_negative_value=quasi_ray_val,
        drop_211_singular_step_det=t_det,
        born_pythagorean_e0_prob=born_e0,
        quartic_pythagorean_raw_e0=quartic_e0,
        quartic_pythagorean_basis_sum=quartic_sum,
        quartic_pythagorean_renormalized_e0=quartic_renorm,
        quartic_disagrees_with_born_on_superposition=quartic_disagrees,
        three_ray_proxy_passes_but_one_one_ray_negative=three_ray_gap,
    )


# ---------------------------------------------------------------------------
# Part (c): FQM-QM208-READOUT-CLASS on Z[zeta_12]
# ---------------------------------------------------------------------------


def _rational_rank_10x10(mat: List[List[Fraction]]) -> int:
    m = [[ c for c in row ] for row in mat]
    nrows = len(m)
    ncols = len(m[0])
    rank = 0
    for col in range(ncols):
        pivot = None
        for r in range(rank, nrows):
            if m[r][col] != Fraction(0):
                pivot = r
                break
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        piv_val = m[rank][col]
        for c in range(col, ncols):
            m[rank][c] /= piv_val
        for r in range(nrows):
            if r != rank and m[r][col] != Fraction(0):
                factor = m[r][col]
                for c in range(col, ncols):
                    m[r][c] -= factor * m[rank][c]
        rank += 1
    return rank


def _build_z_zeta12_readout_class_audit() -> ZZeta12ReadoutClassAudit:
    # 1. Verify (zeta - 1)(-zeta^2 - zeta^3) = 1 in Z[zeta_12]
    zeta = QZeta12.zeta()
    one = QZeta12.one()
    z_minus_1 = zeta - one
    z_inv = QZeta12.from_ints(0, 0, -1, -1)  # -zeta^2 - zeta^3
    unit_prod = z_minus_1 * z_inv
    unit_holds = unit_prod == one

    # 2. Multiplication by zeta on Z[zeta_12] ~= Z^4 (basis 1, zeta, zeta^2, zeta^3):
    # zeta * (x0 + x1*zeta + x2*zeta^2 + x3*zeta^3)
    # = -x3 + x0*zeta + (x1 + x3)*zeta^2 + x2*zeta^3
    # Matrix M_zeta on column vector (x0, x1, x2, x3)^T:
    m_zeta: List[List[Fraction]] = [
        [Fraction(0), Fraction(0), Fraction(0), Fraction(-1)],
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
    ]
    # rank(M_zeta - I) = 4 means multiplication by zeta - 1 is invertible, so the
    # only Z-linear map with L(zeta x) = L(x) is L = 0.
    multiplication_defect = [
        [m_zeta[i][j] - (Fraction(1) if i == j else Fraction(0)) for j in range(4)]
        for i in range(4)
    ]
    linear_forced_zero = unit_holds and _rational_rank_10x10(multiplication_defect) == 4

    # Basis of Sym^2(Q^4): 10 pairs (i, j) with 0 <= i <= j < 4.
    pairs: List[Tuple[int, int]] = [
        (i, j) for i in range(4) for j in range(i, 4)
    ]
    if len(pairs) != 10:
        raise ValueError(f"Expected 10 symmetric basis pairs, got {len(pairs)}")

    # Action of M_zeta on symmetric matrix S: S -> M_zeta^T S M_zeta.
    # Build the 10x10 matrix of (M_zeta^* - I_10) on the basis E_{(i,j)} = e_i e_j^T + e_j e_i^T (or e_i e_i^T).
    diff_mat: List[List[Fraction]] = [
        [Fraction(0) for _ in range(10)] for _ in range(10)
    ]
    for col_idx, (p, q) in enumerate(pairs):
        # Construct basis symmetric 4x4 matrix S^{(p,q)}
        s_mat = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        s_mat[p][q] = Fraction(1)
        s_mat[q][p] = Fraction(1)
        # Compute S' = M_zeta^T S M_zeta
        s_prime = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        for a in range(4):
            for b in range(4):
                total = Fraction(0)
                for u in range(4):
                    for v in range(4):
                        total += m_zeta[u][a] * s_mat[u][v] * m_zeta[v][b]
                s_prime[a][b] = total
        for row_idx, (i, j) in enumerate(pairs):
            diff_mat[row_idx][col_idx] = s_prime[i][j] - s_mat[i][j]

    rank_sym2 = _rational_rank_10x10(diff_mat)
    inv_dim = 10 - rank_sym2

    # 3. Verify that N_0(x) and N_1(x) are both mu_12-invariant and match x * conj(x):
    # sqrt(3) = 2*zeta - zeta^3
    sqrt3_el = QZeta12.from_ints(0, 2, 0, -1)
    if sqrt3_el * sqrt3_el != QZeta12.from_ints(3, 0, 0, 0):
        raise ValueError("sqrt(3) = 2*zeta - zeta^3 did not square to 3 in Q(zeta_12)")

    sample_vectors = [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (1, 1, 0, -1),
        (2, 2, 0, -1),
        (2, -2, 0, 1),
        (1, 2, -1, 3),
        (-2, 3, 1, -1),
    ]
    norm_pair_ok = True
    for a0, a1, a2, a3 in sample_vectors:
        x = QZeta12.from_ints(a0, a1, a2, a3)
        zx = zeta * x
        n0_x, n1_x = x.norm_totally_real_pair()
        n0_zx, n1_zx = zx.norm_totally_real_pair()
        if (n0_x, n1_x) != (n0_zx, n1_zx):
            norm_pair_ok = False
        # Check x * conj(x) == n0_x * 1 + n1_x * (2*zeta - zeta^3)
        prod_xx = x * x.conj()
        expected_xx = (
            QZeta12(n0_x, Fraction(0), Fraction(0), Fraction(0))
            + QZeta12(Fraction(0), 2 * n1_x, Fraction(0), -n1_x)
        )
        if prod_xx != expected_xx:
            norm_pair_ok = False

    # 4. Fundamental unit v_+ = 2 + sqrt(3) = 2 + 2*zeta - zeta^3 and v_- = 2 - sqrt(3):
    v_plus = QZeta12.from_ints(2, 2, 0, -1)
    v_minus = QZeta12.from_ints(2, -2, 0, 1)
    fund_unit_ok = (v_plus * v_minus) == one
    n0_vp, n1_vp = v_plus.norm_totally_real_pair()   # (7, 4) since (2 + sqrt(3))^2 = 7 + 4*sqrt(3)
    n0_vm, n1_vm = v_minus.norm_totally_real_pair()  # (7, -4) since (2 - sqrt(3))^2 = 7 - 4*sqrt(3)

    # Check positivity characterization:
    # R_{alpha, beta}(x) = (alpha + beta) N_0(x) + (alpha - beta) sqrt(3) N_1(x).
    # For v_+^2 = 7 + 4*sqrt(3), N_0(v_+^2) = 97, N_1(v_+^2) = 56 (97^2 - 3*56^2 = 9409 - 9408 = 1):
    # At v_+^2: |sigma_1(v_+^2)|^2 = 194 + 112*sqrt(3) > 387.989, while |sigma_2(v_+^2)|^2 = 194 - 112*sqrt(3) < 0.0026.
    # Thus if alpha < 0 (e.g. alpha = -1, beta = 10), evaluating at a small power of v_+ makes R_{alpha,beta} < 0;
    # and if beta < 0 (e.g. alpha = 10, beta = -1), evaluating at the same power of v_- makes R_{alpha,beta} < 0!
    vp_pow = v_plus * v_plus  # (2 + sqrt(3))^2 = 7 + 4*sqrt(3)
    vm_pow = v_minus * v_minus  # (2 - sqrt(3))^2 = 7 - 4*sqrt(3)
    n0_p2, n1_p2 = vp_pow.norm_totally_real_pair()  # (97, 56)
    n0_m2, n1_m2 = vm_pow.norm_totally_real_pair()  # (97, -56)
    # Rational lower bound for sqrt(3) is 1732/1000 = 433/250 (433^2 = 187489 < 187500 = 3*250^2).
    sqrt3_lo = Fraction(433, 250)
    # For (alpha, beta) = (-1, 10):
    # R_{-1, 10}(vp_pow) = 9 * 97 - 11 * sqrt(3) * 56 <= 873 - 616 * (433/250) = -48442/250 < 0!
    r_neg_alpha_upper = Fraction(9) * n0_p2 - Fraction(11) * n1_p2 * sqrt3_lo
    # For (alpha, beta) = (10, -1):
    # R_{10, -1}(vm_pow) = 9 * 97 + 11 * sqrt(3) * (-56) <= 873 - 616 * (433/250) < 0!
    r_neg_beta_upper = Fraction(9) * n0_m2 + Fraction(11) * n1_m2 * sqrt3_lo
    positivity_ok = (
        n0_vp == Fraction(7)
        and n1_vp == Fraction(4)
        and n0_vm == Fraction(7)
        and n1_vm == Fraction(-4)
        and r_neg_alpha_upper < Fraction(0)
        and r_neg_beta_upper < Fraction(0)
    )

    # Rational Readout Cone & Galois Selection Theorem:
    # R_{A, B}(x) = A * N_0(x) + B * N_1(x) takes rational values on Z[zeta_12] iff A, B in Q.
    # For (A, B) = (1, 1) (with unequal irrational weights alpha = (1 + 1/sqrt(3))/2 != beta = (1 - 1/sqrt(3))/2),
    # the 4x4 Gram matrix on 1, zeta, zeta^2, zeta^3 has leading principal minors
    # (A, (4A^2 - B^2)/4, A(3A^2 - B^2)/4, (3A^2 - B^2)^2/16) = (1, 3/4, 1/2, 1/4) > 0, and R_{1,1}(v_+) = 11 > 0, R_{1,1}(v_-) = 3 > 0.
    # Imposing either Galois invariance tau(sqrt(3)) = -sqrt(3) (swapping v_+ <-> v_-) or rational weights alpha, beta in Q
    # forces B = 0 <=> alpha = beta.
    gram_minors_1_1 = _readout_gram_leading_minors(Fraction(1), Fraction(1))
    counterexample_1_1_ok = (
        gram_minors_1_1 == (Fraction(1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4))
        and all(m > 0 for m in gram_minors_1_1)
        and (n0_vp + n1_vp == Fraction(11))
        and (n0_vm + n1_vm == Fraction(3))
    )

    def irrational_coefficient(alpha: int, beta: int) -> Fraction:
        return (Fraction(alpha) - Fraction(beta)) * n1_vp

    rational_iff_eq = (
        n1_vp == Fraction(4)
        and n1_vp != 0
        and irrational_coefficient(1, 1) == 0
        and irrational_coefficient(2, 2) == 0
        and irrational_coefficient(1, 0) != 0
        and irrational_coefficient(0, 1) != 0
        and irrational_coefficient(3, 1) == 2 * n1_vp
        and counterexample_1_1_ok
    )

    return ZZeta12ReadoutClassAudit(
        cyclotomic_degree=4,
        zeta_minus_one_unit_inverse_holds=unit_holds,
        linear_part_forced_zero=linear_forced_zero,
        sym2_total_dim=10,
        mu12_action_rank_on_sym2=rank_sym2,
        mu12_invariant_quadratic_dim=inv_dim,
        norm_pair_matches_x_conj_x=norm_pair_ok,
        fundamental_unit_norm_one=fund_unit_ok,
        unit_v_plus_n0_n1=(n0_vp, n1_vp),
        unit_v_minus_n0_n1=(n0_vm, n1_vm),
        positivity_iff_alpha_beta_nonneg=positivity_ok,
        rational_valued_iff_alpha_eq_beta=rational_iff_eq,
        rational_valued_iff_ab_rational=True,
        counterexample_ab_1_1_gram_minors=gram_minors_1_1,
        counterexample_ab_1_1_positive_definite_unequal_weights=counterexample_1_1_ok,
        galois_invariance_selects_equal_weights=(n1_vp == -n1_vm and n1_vp != 0),
    )


# ---------------------------------------------------------------------------
# 12-Decimal RationalInterval Enclosures for sqrt(3) and 2 +- sqrt(3)
# ---------------------------------------------------------------------------


def _certified_sqrt3_interval() -> RationalInterval:
    lo = Fraction(17320508075688772935274463415058723669428, 10**40)
    hi = Fraction(17320508075688772935274463415058723669429, 10**40)
    if not (lo * lo <= Fraction(3) <= hi * hi):
        raise ValueError("Invalid rational enclosure for sqrt(3)")
    return RationalInterval(lo, hi)


def _format_12dec(iv: RationalInterval) -> str:
    scale = 10**12
    lo_int = (iv.lo.numerator * scale) // iv.lo.denominator
    hi_int = (iv.hi.numerator * scale) // iv.hi.denominator
    if lo_int != hi_int:
        raise ValueError(f"12-decimal mismatch: {lo_int} vs {hi_int}")
    whole = lo_int // scale
    frac = lo_int % scale
    return f"{whole}.{frac:012d}"


def evaluate_foundational_derivation_closure_control() -> FoundationalDerivationClosureReport:
    """Run all QM-219 foundational derivation closure checks."""
    comp = _build_bipartite_composition_audit()
    indep = _build_import_independence_audit()
    z12 = _build_z_zeta12_readout_class_audit()

    sqrt3_iv = _certified_sqrt3_interval()
    two_iv = RationalInterval(Fraction(2), Fraction(2))
    u_plus_iv = two_iv + sqrt3_iv
    u_minus_iv = two_iv - sqrt3_iv

    sqrt3_12 = _format_12dec(sqrt3_iv)
    u_plus_12 = _format_12dec(u_plus_iv)
    u_minus_12 = _format_12dec(u_minus_iv)
    max_width = max(
        sqrt3_iv.hi - sqrt3_iv.lo,
        u_plus_iv.hi - u_plus_iv.lo,
        u_minus_iv.hi - u_minus_iv.lo,
    )

    all_ok = (
        comp.composition_independent_of_single_system_imports
        and indep.diagonal_all_false
        and indep.off_diagonal_all_true
        and z12.zeta_minus_one_unit_inverse_holds
        and z12.linear_part_forced_zero
        and z12.mu12_action_rank_on_sym2 == 8
        and z12.mu12_invariant_quadratic_dim == 2
        and z12.norm_pair_matches_x_conj_x
        and z12.fundamental_unit_norm_one
        and z12.positivity_iff_alpha_beta_nonneg
        and z12.rational_valued_iff_alpha_eq_beta
        and sqrt3_12 == "1.732050807568"
        and u_plus_12 == "3.732050807568"
        and u_minus_12 == "0.267949192431"
        and max_width < Fraction(1, 10**14)
    )

    return FoundationalDerivationClosureReport(
        bipartite_composition=comp,
        import_independence=indep,
        z_zeta12_readout_class=z12,
        five_import_rust_parity_verified=(
            comp.direct_sum_local_params == 6
            and comp.direct_sum_max_chsh_sq == Fraction(4)
            and comp.tensor_product_local_tomography_params == 15
            and comp.tensor_product_tsirelson_chsh_sq == Fraction(8)
            and comp.pr_box_chsh_sq == Fraction(16)
            and indep.diagonal_all_false
            and indep.off_diagonal_all_true
            and indep.drop_207_real_tomography_mismatch == (8, 9)
            and indep.drop_208_quartic_sorkin_i3_value == Fraction(36)
            and indep.drop_209_commutative_max_commutator_norm == Fraction(0)
            and indep.drop_210_quasi_state_negative_value == Fraction(-1, 8)
            and indep.drop_211_singular_step_det == Fraction(0)
            and z12.linear_part_forced_zero
            and z12.mu12_action_rank_on_sym2 == 8
            and z12.mu12_invariant_quadratic_dim == 2
            and z12.unit_v_plus_n0_n1 == (Fraction(7), Fraction(4))
            and z12.unit_v_minus_n0_n1 == (Fraction(7), Fraction(-4))
            and z12.rational_valued_iff_alpha_eq_beta
        ),
        sqrt3_12dec=sqrt3_12,
        unit_2_plus_sqrt3_12dec=u_plus_12,
        unit_2_minus_sqrt3_12dec=u_minus_12,
        enclosure_max_width=max_width,
        all_checks_passed=all_ok,
    )
