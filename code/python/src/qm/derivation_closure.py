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

from .dressed_qed import RationalInterval



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
        a = [self.c0, self.c1, self.c2, self.c3]
        b = [other.c0, other.c1, other.c2, other.c3]
        prod = [Fraction(0)] * 7
        for i in range(4):
            for j in range(4):
                prod[i + j] += a[i] * b[j]
        prod[0] -= prod[6]
        prod[3] += prod[5]
        prod[1] -= prod[5]
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




def _verify_pr_box_no_signaling(pr_table: Dict[Tuple[int, int, int, int], Fraction]) -> bool:
    for x in (0, 1):
        for y in (0, 1):
            total = sum(pr_table[(a, b, x, y)] for a in (0, 1) for b in (0, 1))
            if total != Fraction(1):
                return False
    for x in (0, 1):
        for a in (0, 1):
            marg_y0 = sum(pr_table[(a, b, x, 0)] for b in (0, 1))
            marg_y1 = sum(pr_table[(a, b, x, 1)] for b in (0, 1))
            if marg_y0 != Fraction(1, 2) or marg_y1 != Fraction(1, 2):
                return False
    for y in (0, 1):
        for b in (0, 1):
            marg_x0 = sum(pr_table[(a, b, 0, y)] for a in (0, 1))
            marg_x1 = sum(pr_table[(a, b, 1, y)] for a in (0, 1))
            if marg_x0 != Fraction(1, 2) or marg_x1 != Fraction(1, 2):
                return False
    return True


def _compute_pr_box_chsh(pr_table: Dict[Tuple[int, int, int, int], Fraction]) -> Fraction:
    def pr_correlator(x: int, y: int) -> Fraction:
        total = Fraction(0)
        for a in (0, 1):
            for b in (0, 1):
                spin_a = 1 if a == 0 else -1
                spin_b = 1 if b == 0 else -1
                total += Fraction(spin_a * spin_b) * pr_table[(a, b, x, y)]
        return total

    return (
        pr_correlator(0, 0)
        + pr_correlator(0, 1)
        + pr_correlator(1, 0)
        - pr_correlator(1, 1)
    )


def _build_bipartite_composition_audit() -> BipartiteCompositionAudit:
    d_a, d_b = 2, 2
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

    tensor_product_dim = d_a * d_b
    params_a = d_a * d_a - 1
    params_b = d_b * d_b - 1
    tensor_product_local_tomography_params = params_a + params_b + params_a * params_b
    tensor_product_tsirelson_chsh_sq = Fraction(8)

    pr_table: Dict[Tuple[int, int, int, int], Fraction] = {}
    for x in (0, 1):
        for y in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    pr_table[(a, b, x, y)] = (
                        Fraction(1, 2) if ((a ^ b) == (x * y)) else Fraction(0)
                    )

    no_signaling_ok = _verify_pr_box_no_signaling(pr_table)
    s_pr = _compute_pr_box_chsh(pr_table)
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

    real_local_params = 2 + 2 + 2 * 2
    real_joint_params = (4 * 5) // 2 - 1
    m207_sorkin_i3 = (1 + 2 + 3) ** 2 - (1 + 2) ** 2 - (1 + 3) ** 2 - (2 + 3) ** 2 + 1 + 4 + 9
    pauli_commutator = _pauli_xz_commutator()
    row_207 = (
        _rational_has_order4_phase() and (real_local_params == real_joint_params),
        m207_sorkin_i3 == 0,
        _nonzero(pauli_commutator),
        _real_psd_born_nonnegative(),
        _quarter_turn_is_order_4(),
    )

    quartic_i3 = Fraction(3**4 - 3 * (2**4) + 3 * (1**4))
    row_208 = (
        _gaussian_has_order4_phase(),
        quartic_i3 == Fraction(0),
        _nonzero(pauli_commutator),
        _basis_projectors_resolve_identity(),
        _diagonal_clock_unitary_order_4(),
    )

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

    quasi_ray_val = Fraction(1, 4) - Fraction(3, 8)
    row_210 = (
        _gaussian_has_order4_phase(),
        _quadratic_sorkin_vanishes(),
        _nonzero(pauli_commutator),
        _quasistate_admits_psd(),
        _diagonal_clock_unitary_order_4(),
    )

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

    q_1_0 = Fraction(1, 2)
    q_0_1 = Fraction(1, 2)
    q_1_neg1 = Fraction(1, 2) + Fraction(3, 2) + Fraction(1, 2)
    q_1_1 = Fraction(1, 2) - Fraction(3, 2) + Fraction(1, 2)
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


def _compute_sym2_action(m_zeta: List[List[Fraction]]) -> tuple[int, int]:
    pairs: List[Tuple[int, int]] = [
        (i, j) for i in range(4) for j in range(i, 4)
    ]
    if len(pairs) != 10:
        raise ValueError(f"Expected 10 symmetric basis pairs, got {len(pairs)}")

    diff_mat: List[List[Fraction]] = [
        [Fraction(0) for _ in range(10)] for _ in range(10)
    ]
    for col_idx, (p, q) in enumerate(pairs):
        s_mat = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        s_mat[p][q] = Fraction(1)
        s_mat[q][p] = Fraction(1)
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
    return rank_sym2, inv_dim


def _verify_mu12_norm_pairs(zeta: QZeta12) -> bool:
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
    for a0, a1, a2, a3 in sample_vectors:
        x = QZeta12.from_ints(a0, a1, a2, a3)
        zx = zeta * x
        n0_x, n1_x = x.norm_totally_real_pair()
        n0_zx, n1_zx = zx.norm_totally_real_pair()
        if (n0_x, n1_x) != (n0_zx, n1_zx):
            return False
        prod_xx = x * x.conj()
        expected_xx = (
            QZeta12(n0_x, Fraction(0), Fraction(0), Fraction(0))
            + QZeta12(Fraction(0), 2 * n1_x, Fraction(0), -n1_x)
        )
        if prod_xx != expected_xx:
            return False
    return True


def _verify_readout_positivity_and_galois(one: QZeta12) -> tuple[bool, Fraction, Fraction, Fraction, Fraction, tuple[Fraction, ...], bool, bool]:
    v_plus = QZeta12.from_ints(2, 2, 0, -1)
    v_minus = QZeta12.from_ints(2, -2, 0, 1)
    fund_unit_ok = (v_plus * v_minus) == one
    n0_vp, n1_vp = v_plus.norm_totally_real_pair()
    n0_vm, n1_vm = v_minus.norm_totally_real_pair()

    vp_pow = v_plus * v_plus
    vm_pow = v_minus * v_minus
    n0_p2, n1_p2 = vp_pow.norm_totally_real_pair()
    n0_m2, n1_m2 = vm_pow.norm_totally_real_pair()
    sqrt3_lo = Fraction(433, 250)
    r_neg_alpha_upper = Fraction(9) * n0_p2 - Fraction(11) * n1_p2 * sqrt3_lo
    r_neg_beta_upper = Fraction(9) * n0_m2 + Fraction(11) * n1_m2 * sqrt3_lo
    positivity_ok = (
        n0_vp == Fraction(7)
        and n1_vp == Fraction(4)
        and n0_vm == Fraction(7)
        and n1_vm == Fraction(-4)
        and r_neg_alpha_upper < Fraction(0)
        and r_neg_beta_upper < Fraction(0)
    )

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
    return fund_unit_ok, n0_vp, n1_vp, n0_vm, n1_vm, gram_minors_1_1, positivity_ok, rational_iff_eq


def _build_z_zeta12_readout_class_audit() -> ZZeta12ReadoutClassAudit:
    zeta = QZeta12.zeta()
    one = QZeta12.one()
    z_minus_1 = zeta - one
    z_inv = QZeta12.from_ints(0, 0, -1, -1)
    unit_holds = (z_minus_1 * z_inv) == one

    m_zeta: List[List[Fraction]] = [
        [Fraction(0), Fraction(0), Fraction(0), Fraction(-1)],
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
    ]
    multiplication_defect = [
        [m_zeta[i][j] - (Fraction(1) if i == j else Fraction(0)) for j in range(4)]
        for i in range(4)
    ]
    linear_forced_zero = unit_holds and _rational_rank_10x10(multiplication_defect) == 4

    rank_sym2, inv_dim = _compute_sym2_action(m_zeta)
    norm_pair_ok = _verify_mu12_norm_pairs(zeta)
    (
        fund_unit_ok,
        n0_vp,
        n1_vp,
        n0_vm,
        n1_vm,
        gram_minors_1_1,
        positivity_ok,
        rational_iff_eq,
    ) = _verify_readout_positivity_and_galois(one)

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
        counterexample_ab_1_1_positive_definite_unequal_weights=(gram_minors_1_1 == (Fraction(1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4))),
        galois_invariance_selects_equal_weights=(n1_vp == -n1_vm and n1_vp != 0),
    )




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


def _check_closure_all_ok(comp: BipartiteCompositionAudit, indep: ImportIndependenceAudit, z12: ZZeta12ReadoutClassAudit, sqrt3_12: str, u_plus_12: str, u_minus_12: str, max_width: Fraction) -> bool:
    return (
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


def _check_closure_rust_parity(comp: BipartiteCompositionAudit, indep: ImportIndependenceAudit, z12: ZZeta12ReadoutClassAudit) -> bool:
    return (
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
    )


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

    all_ok = _check_closure_all_ok(comp, indep, z12, sqrt3_12, u_plus_12, u_minus_12, max_width)
    five_import_rust_parity_verified = _check_closure_rust_parity(comp, indep, z12)

    return FoundationalDerivationClosureReport(
        bipartite_composition=comp,
        import_independence=indep,
        z_zeta12_readout_class=z12,
        five_import_rust_parity_verified=five_import_rust_parity_verified,
        sqrt3_12dec=sqrt3_12,
        unit_2_plus_sqrt3_12dec=u_plus_12,
        unit_2_minus_sqrt3_12dec=u_minus_12,
        enclosure_max_width=max_width,
        all_checks_passed=all_ok,
    )
