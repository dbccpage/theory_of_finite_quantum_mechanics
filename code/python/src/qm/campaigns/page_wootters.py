"""QM-218 Relational Page-Wootters Clock Dressing, Cyclotomic Q(zeta_8) Tsirelson Bound, and Discrete Weyl-Wigner Control.

Establishes a finite-to-continuum bridge for three foundational pillars of
quantum mechanics:

1. **Part (a) -- Relational Page-Wootters Clock Dressing over Q(i) (Z_4 Clock):**
   - On the joint history space H_hist = H_C (x) H_S = Q(i)^4 (x) Q(i)^2 = Q(i)^8
     with cyclic clock shift S_C |t> = |t + 1 mod 4> (S_C^4 = I_4) and system
     step unitary U_S = diag(1, i) (U_S^4 = I_2), the history shift operator
     W = S_C (x) U_S satisfies W^dagger W = I_8 and W^4 = I_8.
   - The Page-Wootters constraint C_PW = I_8 - W annihilates the group-averaging
     projector Pi_PW = (1/4) sum_{k=0}^3 W^k (Pi_PW^2 = Pi_PW, Pi_PW^dagger = Pi_PW,
     tr(Pi_PW) = 2 = dim(H_S)).
   - The clock-controlled dressing unitary D = sum_{t=0}^3 |t><t| (x) U_S^t
     satisfies the exact DFM intertwining identity D^dagger W D = S_C (x) I_2
     and decouples the static constraint projector D^dagger Pi_PW D = Pi_{C,0} (x) I_2.
   - While bare observables I_4 (x) sigma_x fail to commute with W ([I_4 (x) sigma_x, W] != 0),
     the group-averaged relational dressed observables O_rel(tau; O_S) commute
     with W and Pi_PW, satisfy the discrete Heisenberg step equation
     O_rel(tau + 1; O_S) = O_rel(tau; U_S^dagger O_S U_S), and on the static
     history state |Psi_hist> = 2 Pi_PW(|0> (x) |psi_0>) (C_PW |Psi_hist> = 0)
     reproduce the exact Schrödinger/Heisenberg tick expectations
     <sigma_x>_tau = (1, 0, -1, 0) and <sigma_y>_tau = (0, 1, 0, -1).

2. **Part (b) -- Cyclotomic Q(zeta_8) Bell/CHSH Tsirelson Bound & Algebraic SOS Certificate:**
   - Exhaustive enumeration over all 16 deterministic vertices (a_0, a_1, b_0, b_1) in {-1, +1}^4
     of the classical marginal compatibility polytope confirms |S_classical| <= 2.
   - In Q(zeta_8) = Q[z]/(z^4 + 1), the element s_2 = z - z^3 satisfies s_2^2 = 2
     and s_2^* = s_2, with inverse s_2^{-1} = (1/2)(z - z^3).
   - For A_0 = Z (x) I_2, A_1 = X (x) I_2, B_0 = I_2 (x) (Z + X)/s_2, and
     B_1 = I_2 (x) (Z - X)/s_2 in M_4(Q(zeta_8)), verifies A_i^2 = B_j^2 = I_4,
     [A_i, B_j] = 0, the Landau identity B_CHSH^2 = 4 I_4 - [A_0, A_1][B_0, B_1],
     and the exact algebraic Sum-of-Squares (SOS) decomposition
     4 I_4 - s_2 B_CHSH = W_1^dagger W_1 + W_2^dagger W_2
     with W_1 = s_2^{-1}(A_0 + A_1) - B_0 and W_2 = s_2^{-1}(A_0 - A_1) - B_1.
   - On the maximally entangled Bell state |Phi^+> = (1, 0, 0, 1)^T, W_1 |Phi^+> = W_2 |Phi^+> = 0
     and B_CHSH |Phi^+> = 2 s_2 |Phi^+> (expectation 2 s_2 = 2*sqrt(2)), whereas
     the separable product state |00> achieves only s_2 = sqrt(2) < 2.

3. **Part (c) -- Discrete Weyl-Wigner Phase Space on (Z_3)^2 over Q(zeta_3) & 12-Decimal Enclosures:**
   - Constructs the 9 phase-point operators A(q, p)_{x, y} = delta_{x+y = 2q mod 3} omega^{p(x-y)}
     in M_3(Q(zeta_3)) (omega^2 + omega + 1 = 0), verifying A(q, p)^dagger = A(q, p),
     A(q, p)^2 = I_3, tr(A(q, p) A(q', p')) = 3 delta_{q,q'} delta_{p,p'}, and
     exact line marginals (1/3) sum_p A(q, p) = |q><q| and (1/3) sum_q A(q, p) = |p_tilde><p_tilde|.
   - Shows that the stabilizer state |0> has a non-negative rational Wigner
     distribution W_{|0>}(q, p) in {0, 1/3} (negativity 0), whereas the superposition
     state |psi_neg> = |0> - |1> has exact rational Wigner values achieving
     strictly negative quasi-probability W(2, 0) = -1/3 < 0 (negativity 2/3)
     while matching all position and Fourier momentum Born marginals.
   - Certifies sqrt(2) via exact rational endpoint squaring lo^2 <= 2 <= hi^2 and
     encloses 2*sqrt(2) (2.828427124746), 2*sqrt(2) - 2 (0.828427124746), and
     sqrt(2)/2 (0.707106781186) to 12 decimal places (width < 10^{-14}).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction

from .dressed_qed import RationalInterval



@dataclass(frozen=True)
class Qi:
    """Exact Gaussian rational a + b*i in Q(i)."""

    re: Fraction
    im: Fraction = Fraction(0)

    @staticmethod
    def from_int(n: int) -> Qi:
        return Qi(Fraction(n), Fraction(0))

    @staticmethod
    def i() -> Qi:
        return Qi(Fraction(0), Fraction(1))

    def conj(self) -> Qi:
        return Qi(self.re, -self.im)

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0

    def __add__(self, other: Qi) -> Qi:
        return Qi(self.re + other.re, self.im + other.im)

    def __sub__(self, other: Qi) -> Qi:
        return Qi(self.re - other.re, self.im - other.im)

    def __neg__(self) -> Qi:
        return Qi(-self.re, -self.im)

    def __mul__(self, other: Qi) -> Qi:
        return Qi(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def scale(self, c: Fraction) -> Qi:
        return Qi(self.re * c, self.im * c)


QiMat = list[list[Qi]]
QiVec = list[Qi]


def qi_zeros(n: int) -> QiMat:
    z = Qi.from_int(0)
    return [[z for _ in range(n)] for _ in range(n)]


def qi_eye(n: int) -> QiMat:
    out = qi_zeros(n)
    one = Qi.from_int(1)
    for k in range(n):
        out[k][k] = one
    return out


def qi_add(a: QiMat, b: QiMat) -> QiMat:
    n = len(a)
    return [[a[r][c] + b[r][c] for c in range(n)] for r in range(n)]


def qi_sub(a: QiMat, b: QiMat) -> QiMat:
    n = len(a)
    return [[a[r][c] - b[r][c] for c in range(n)] for r in range(n)]


def qi_scale(c: Fraction, a: QiMat) -> QiMat:
    n = len(a)
    return [[a[r][col].scale(c) for col in range(n)] for r in range(n)]


def qi_matmul(a: QiMat, b: QiMat) -> QiMat:
    n = len(a)
    out = qi_zeros(n)
    for r in range(n):
        for k in range(n):
            ark = a[r][k]
            if ark.is_zero():
                continue
            for c in range(n):
                out[r][c] = out[r][c] + ark * b[k][c]
    return out


def qi_dagger(a: QiMat) -> QiMat:
    n = len(a)
    return [[a[c][r].conj() for c in range(n)] for r in range(n)]


def qi_comm(a: QiMat, b: QiMat) -> QiMat:
    return qi_sub(qi_matmul(a, b), qi_matmul(b, a))


def qi_kron(a: QiMat, b: QiMat) -> QiMat:
    na = len(a)
    nb = len(b)
    out = qi_zeros(na * nb)
    for ra in range(na):
        for ca in range(na):
            val_a = a[ra][ca]
            if val_a.is_zero():
                continue
            for rb in range(nb):
                for cb in range(nb):
                    out[ra * nb + rb][ca * nb + cb] = val_a * b[rb][cb]
    return out


def qi_mat_eq(a: QiMat, b: QiMat) -> bool:
    return all(a[r][c] == b[r][c] for r in range(len(a)) for c in range(len(a)))


def qi_is_zero(a: QiMat) -> bool:
    return all(a[r][c].is_zero() for r in range(len(a)) for c in range(len(a)))


def qi_trace(a: QiMat) -> Qi:
    acc = Qi.from_int(0)
    for k in range(len(a)):
        acc = acc + a[k][k]
    return acc


def qi_matvec(a: QiMat, v: QiVec) -> QiVec:
    n = len(a)
    out: QiVec = []
    for r in range(n):
        acc = Qi.from_int(0)
        for c in range(n):
            acc = acc + a[r][c] * v[c]
        out.append(acc)
    return out


def qi_inner(u: QiVec, v: QiVec) -> Qi:
    acc = Qi.from_int(0)
    for uk, vk in zip(u, v, strict=True):
        acc = acc + uk.conj() * vk
    return acc




@dataclass(frozen=True)
class QZeta8:
    """Element c0 + c1*z + c2*z^2 + c3*z^3 in Q(zeta_8) where z^4 = -1."""

    c0: Fraction = Fraction(0)
    c1: Fraction = Fraction(0)
    c2: Fraction = Fraction(0)
    c3: Fraction = Fraction(0)

    @staticmethod
    def from_int(n: int) -> QZeta8:
        return QZeta8(Fraction(n))

    @staticmethod
    def from_frac(f: Fraction) -> QZeta8:
        return QZeta8(f)

    @staticmethod
    def sqrt2() -> QZeta8:
        """s_2 = z + z^{-1} = z - z^3, satisfying s_2^2 = 2."""
        return QZeta8(Fraction(0), Fraction(1), Fraction(0), Fraction(-1))

    @staticmethod
    def inv_sqrt2() -> QZeta8:
        """s_2^{-1} = (1/2)(z - z^3), satisfying s_2 * s_2^{-1} = 1."""
        h = Fraction(1, 2)
        return QZeta8(Fraction(0), h, Fraction(0), -h)

    def conj(self) -> QZeta8:
        """Complex conjugation z -> z^{-1} = -z^3, z^2 -> -z^2, z^3 -> -z."""
        return QZeta8(self.c0, -self.c3, -self.c2, -self.c1)

    def is_zero(self) -> bool:
        return self.c0 == 0 and self.c1 == 0 and self.c2 == 0 and self.c3 == 0

    def __add__(self, other: QZeta8) -> QZeta8:
        return QZeta8(
            self.c0 + other.c0,
            self.c1 + other.c1,
            self.c2 + other.c2,
            self.c3 + other.c3,
        )

    def __sub__(self, other: QZeta8) -> QZeta8:
        return QZeta8(
            self.c0 - other.c0,
            self.c1 - other.c1,
            self.c2 - other.c2,
            self.c3 - other.c3,
        )

    def __neg__(self) -> QZeta8:
        return QZeta8(-self.c0, -self.c1, -self.c2, -self.c3)

    def __mul__(self, other: QZeta8) -> QZeta8:
        a = (self.c0, self.c1, self.c2, self.c3)
        b = (other.c0, other.c1, other.c2, other.c3)
        res = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
        for i in range(4):
            if a[i] == 0:
                continue
            for j in range(4):
                if b[j] == 0:
                    continue
                k = i + j
                if k < 4:
                    res[k] += a[i] * b[j]
                else:
                    res[k - 4] -= a[i] * b[j]
        return QZeta8(res[0], res[1], res[2], res[3])


Z8Mat = list[list[QZeta8]]
Z8Vec = list[QZeta8]


def z8_zeros(n: int) -> Z8Mat:
    z = QZeta8.from_int(0)
    return [[z for _ in range(n)] for _ in range(n)]


def z8_eye(n: int) -> Z8Mat:
    out = z8_zeros(n)
    one = QZeta8.from_int(1)
    for k in range(n):
        out[k][k] = one
    return out


def z8_add(a: Z8Mat, b: Z8Mat) -> Z8Mat:
    n = len(a)
    return [[a[r][c] + b[r][c] for c in range(n)] for r in range(n)]


def z8_sub(a: Z8Mat, b: Z8Mat) -> Z8Mat:
    n = len(a)
    return [[a[r][c] - b[r][c] for c in range(n)] for r in range(n)]


def z8_scale(s: QZeta8, a: Z8Mat) -> Z8Mat:
    n = len(a)
    return [[s * a[r][c] for c in range(n)] for r in range(n)]


def z8_matmul(a: Z8Mat, b: Z8Mat) -> Z8Mat:
    n = len(a)
    out = z8_zeros(n)
    for r in range(n):
        for k in range(n):
            ark = a[r][k]
            if ark.is_zero():
                continue
            for c in range(n):
                out[r][c] = out[r][c] + ark * b[k][c]
    return out


def z8_dagger(a: Z8Mat) -> Z8Mat:
    n = len(a)
    return [[a[c][r].conj() for c in range(n)] for r in range(n)]


def z8_comm(a: Z8Mat, b: Z8Mat) -> Z8Mat:
    return z8_sub(z8_matmul(a, b), z8_matmul(b, a))


def z8_kron(a: Z8Mat, b: Z8Mat) -> Z8Mat:
    na = len(a)
    nb = len(b)
    out = z8_zeros(na * nb)
    for ra in range(na):
        for ca in range(na):
            val_a = a[ra][ca]
            if val_a.is_zero():
                continue
            for rb in range(nb):
                for cb in range(nb):
                    out[ra * nb + rb][ca * nb + cb] = val_a * b[rb][cb]
    return out


def z8_mat_eq(a: Z8Mat, b: Z8Mat) -> bool:
    return all(a[r][c] == b[r][c] for r in range(len(a)) for c in range(len(a)))


def z8_is_zero(a: Z8Mat) -> bool:
    return all(a[r][c].is_zero() for r in range(len(a)) for c in range(len(a)))


def z8_matvec(a: Z8Mat, v: Z8Vec) -> Z8Vec:
    n = len(a)
    out: Z8Vec = []
    for r in range(n):
        acc = QZeta8.from_int(0)
        for c in range(n):
            acc = acc + a[r][c] * v[c]
        out.append(acc)
    return out


def z8_inner(u: Z8Vec, v: Z8Vec) -> QZeta8:
    acc = QZeta8.from_int(0)
    for uk, vk in zip(u, v, strict=True):
        acc = acc + uk.conj() * vk
    return acc




@dataclass(frozen=True)
class QZeta3:
    """Element a + b*omega in Q(zeta_3) where omega^2 = -1 - omega."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    @staticmethod
    def from_int(n: int) -> QZeta3:
        return QZeta3(Fraction(n), Fraction(0))

    @staticmethod
    def omega_pow(k: int) -> QZeta3:
        r = k % 3
        if r == 0:
            return QZeta3(Fraction(1), Fraction(0))
        if r == 1:
            return QZeta3(Fraction(0), Fraction(1))
        return QZeta3(Fraction(-1), Fraction(-1))

    def conj(self) -> QZeta3:
        """Conjugation omega -> omega^2 = -1 - omega."""
        return QZeta3(self.a - self.b, -self.b)

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def __add__(self, other: QZeta3) -> QZeta3:
        return QZeta3(self.a + other.a, self.b + other.b)

    def __sub__(self, other: QZeta3) -> QZeta3:
        return QZeta3(self.a - other.a, self.b - other.b)

    def __mul__(self, other: QZeta3) -> QZeta3:
        return QZeta3(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    def scale(self, c: Fraction) -> QZeta3:
        return QZeta3(self.a * c, self.b * c)


Z3Mat = list[list[QZeta3]]
Z3Vec = list[QZeta3]


def z3_zeros(n: int) -> Z3Mat:
    z = QZeta3.from_int(0)
    return [[z for _ in range(n)] for _ in range(n)]


def z3_eye(n: int) -> Z3Mat:
    out = z3_zeros(n)
    one = QZeta3.from_int(1)
    for k in range(n):
        out[k][k] = one
    return out


def z3_add(a: Z3Mat, b: Z3Mat) -> Z3Mat:
    n = len(a)
    return [[a[r][c] + b[r][c] for c in range(n)] for r in range(n)]


def z3_scale(c: Fraction, a: Z3Mat) -> Z3Mat:
    n = len(a)
    return [[a[r][col].scale(c) for col in range(n)] for r in range(n)]


def z3_matmul(a: Z3Mat, b: Z3Mat) -> Z3Mat:
    n = len(a)
    out = z3_zeros(n)
    for r in range(n):
        for k in range(n):
            ark = a[r][k]
            if ark.is_zero():
                continue
            for c in range(n):
                out[r][c] = out[r][c] + ark * b[k][c]
    return out


def z3_dagger(a: Z3Mat) -> Z3Mat:
    n = len(a)
    return [[a[c][r].conj() for c in range(n)] for r in range(n)]


def z3_trace(a: Z3Mat) -> QZeta3:
    acc = QZeta3.from_int(0)
    for k in range(len(a)):
        acc = acc + a[k][k]
    return acc


def z3_mat_eq(a: Z3Mat, b: Z3Mat) -> bool:
    return all(a[r][c] == b[r][c] for r in range(len(a)) for c in range(len(a)))


def z3_quad_form(a: Z3Mat, v: Z3Vec) -> QZeta3:
    n = len(a)
    acc = QZeta3.from_int(0)
    for r in range(n):
        for c in range(n):
            acc = acc + v[r].conj() * a[r][c] * v[c]
    return acc


def wigner_phase_point_operator_z3(q: int, p: int) -> Z3Mat:
    """Return the 3x3 Weyl-Wigner phase-point operator A(q, p) on (Z_3)^2 over Q(zeta_3)."""
    if q not in (0, 1, 2) or p not in (0, 1, 2):
        raise ValueError(f"(q, p) must lie in {{0, 1, 2}}^2; got ({q}, {p})")
    mat = z3_zeros(3)
    target = (2 * q) % 3
    for x in range(3):
        for y in range(3):
            if (x + y) % 3 == target:
                mat[x][y] = QZeta3.omega_pow(p * (x - y))
    return mat


def compute_wigner_table_z3(state: Z3Vec) -> list[list[Fraction]]:
    """Return the 3x3 rational discrete Wigner quasi-probability table W_psi(q, p)."""
    norm_sq_z3 = sum((c.conj() * c for c in state), start=QZeta3.from_int(0))
    if norm_sq_z3.b != 0 or norm_sq_z3.a <= 0:
        raise ValueError("State norm squared must be a positive rational number")
    denom = Fraction(3) * norm_sq_z3.a
    table: list[list[Fraction]] = []
    for q in range(3):
        row: list[Fraction] = []
        for p in range(3):
            aqp = wigner_phase_point_operator_z3(q, p)
            val = z3_quad_form(aqp, state)
            if val.b != 0:
                raise ValueError("Hermitian phase-point expectation must be real rational")
            row.append(val.a / denom)
        table.append(row)
    return table




def certified_sqrt2_interval() -> RationalInterval:
    """Return a 25-digit rational interval for sqrt(2) certified by lo^2 <= 2 <= hi^2."""
    denom = 10**24
    lo = Fraction(1414213562373095048801688, denom)
    hi = Fraction(1414213562373095048801689, denom)
    if not (lo * lo <= Fraction(2) <= hi * hi):
        raise ValueError("Invalid sqrt(2) rational bracket")
    return RationalInterval(lo, hi)


def _format_certified_12(iv: RationalInterval) -> str:
    lo_s, hi_s, ok = iv.decimal_prefix(12)
    if not ok:
        raise ValueError(f"Interval bounds do not agree to 12 decimal places: {lo_s} vs {hi_s}")
    return lo_s


@dataclass(frozen=True)
class PageWoottersTsirelsonWignerReport:
    """Complete finite-to-continuum report for QM-218."""

    pw_history_shift_unitary_and_order_4: bool
    pw_constraint_projector_idempotent_hermitian: bool
    pw_constraint_projector_trace: int
    pw_constraint_annihilates_projector: bool
    pw_dressing_intertwines_history_shift: bool
    pw_dressing_decouples_projector: bool
    pw_bare_observable_breaks_constraint: bool
    pw_relational_observables_commute_with_constraint: bool
    pw_heisenberg_step_covariance_exact: bool
    pw_static_state_sigma_x_ticks: tuple[Fraction, ...]
    pw_static_state_sigma_y_ticks: tuple[Fraction, ...]

    chsh_classical_polytope_vertex_count: int
    chsh_classical_polytope_max: Fraction
    chsh_cyclotomic_sqrt2_squares_to_2: bool
    chsh_cyclotomic_sqrt2_inverse_exact: bool
    chsh_observables_involutory_and_spacelike_commuting: bool
    chsh_landau_identity_exact: bool
    chsh_sos_decomposition_exact: bool
    chsh_bell_state_annihilated_by_sos_witnesses: bool
    chsh_bell_state_eigenvalue_is_2_sqrt2: bool
    chsh_separable_state_expectation_is_sqrt2: bool

    wigner_phase_point_hermitian_involutory_unit_trace: bool
    wigner_phase_point_orthogonality_and_completeness: bool
    wigner_line_marginals_match_projectors: bool
    wigner_stabilizer_nonnegative_and_normalized: bool
    wigner_stabilizer_negativity: Fraction
    wigner_superposition_normalized_and_marginals_exact: bool
    wigner_superposition_min_value: Fraction
    wigner_superposition_negativity: Fraction
    sqrt2_square_bounds_enclose_two: bool
    tsirelson_bound_interval: RationalInterval
    tsirelson_bound_decimal_12: str
    bell_violation_excess_interval: RationalInterval
    bell_violation_excess_decimal_12: str
    tsirelson_per_correlator_interval: RationalInterval
    tsirelson_per_correlator_decimal_12: str


def _evaluate_page_wootters_relational_dressing():
    """Execute Part (a): Page-Wootters Relational Clock Dressing over Q(i)."""
    i4 = qi_eye(4)
    i2 = qi_eye(2)
    i8 = qi_eye(8)

    s_c = qi_zeros(4)
    for t in range(4):
        s_c[(t + 1) % 4][t] = Qi.from_int(1)

    u_s = qi_zeros(2)
    u_s[0][0] = Qi.from_int(1)
    u_s[1][1] = Qi.i()

    w_hist = qi_kron(s_c, u_s)
    w2 = qi_matmul(w_hist, w_hist)
    w3 = qi_matmul(w2, w_hist)
    w4 = qi_matmul(w3, w_hist)
    w_powers = [i8, w_hist, w2, w3]

    unitary_order4_ok = qi_mat_eq(qi_matmul(qi_dagger(w_hist), w_hist), i8) and qi_mat_eq(w4, i8)

    c_pw = qi_sub(i8, w_hist)
    pi_pw = qi_scale(Fraction(1, 4), qi_add(qi_add(i8, w_hist), qi_add(w2, w3)))
    proj_idem_herm_ok = qi_mat_eq(qi_matmul(pi_pw, pi_pw), pi_pw) and qi_mat_eq(qi_dagger(pi_pw), pi_pw)
    tr_pi = qi_trace(pi_pw)
    assert tr_pi.im == 0
    proj_trace = int(tr_pi.re)
    annihilates_ok = qi_is_zero(qi_matmul(c_pw, pi_pw)) and qi_is_zero(qi_matmul(pi_pw, c_pw))

    u_s_pows = [i2, u_s, qi_matmul(u_s, u_s), qi_matmul(qi_matmul(u_s, u_s), u_s)]
    d_dress = qi_zeros(8)
    for t in range(4):
        proj_t = qi_zeros(4)
        proj_t[t][t] = Qi.from_int(1)
        d_dress = qi_add(d_dress, qi_kron(proj_t, u_s_pows[t]))

    d_dag = qi_dagger(d_dress)
    intertwine_ok = qi_mat_eq(qi_matmul(d_dag, qi_matmul(w_hist, d_dress)), qi_kron(s_c, i2))

    sc2 = qi_matmul(s_c, s_c)
    sc3 = qi_matmul(sc2, s_c)
    pi_c0 = qi_scale(Fraction(1, 4), qi_add(qi_add(i4, s_c), qi_add(sc2, sc3)))
    decouple_ok = qi_mat_eq(qi_matmul(d_dag, qi_matmul(pi_pw, d_dress)), qi_kron(pi_c0, i2))

    sigma_x = [[Qi.from_int(0), Qi.from_int(1)], [Qi.from_int(1), Qi.from_int(0)]]
    sigma_y = [[Qi.from_int(0), -Qi.i()], [Qi.i(), Qi.from_int(0)]]

    bare_breaks_ok = not qi_is_zero(qi_comm(qi_kron(i4, sigma_x), w_hist))

    def relational_observable(tau: int, obs_s: QiMat) -> QiMat:
        proj_tau = qi_zeros(4)
        proj_tau[tau][tau] = Qi.from_int(1)
        seed = qi_kron(proj_tau, obs_s)
        acc = qi_zeros(8)
        for k in range(4):
            wk = w_powers[k]
            wk_dag = qi_dagger(wk)
            acc = qi_add(acc, qi_matmul(wk_dag, qi_matmul(seed, wk)))
        return acc

    psi0_hist = [Qi.from_int(0) for _ in range(8)]
    psi0_hist[0] = Qi.from_int(1)
    psi0_hist[1] = Qi.from_int(1)
    psi_hist = [c.scale(Fraction(2)) for c in qi_matvec(pi_pw, psi0_hist)]
    assert all(c.is_zero() for c in qi_matvec(c_pw, psi_hist))
    norm_hist = qi_inner(psi_hist, psi_hist)
    assert norm_hist == Qi.from_int(2)

    rel_comm_ok = True
    heisenberg_ok = True
    sx_ticks: list[Fraction] = []
    sy_ticks: list[Fraction] = []
    us_dag_sx_us = qi_matmul(qi_dagger(u_s), qi_matmul(sigma_x, u_s))
    for tau in range(4):
        orel_x = relational_observable(tau, sigma_x)
        orel_y = relational_observable(tau, sigma_y)
        if not qi_is_zero(qi_comm(orel_x, w_hist)) or not qi_is_zero(qi_comm(orel_x, pi_pw)):
            rel_comm_ok = False
        if not qi_is_zero(qi_comm(orel_y, w_hist)) or not qi_is_zero(qi_comm(orel_y, pi_pw)):
            rel_comm_ok = False
        orel_x_next = relational_observable((tau + 1) % 4, sigma_x)
        orel_x_heis = relational_observable(tau, us_dag_sx_us)
        if not qi_mat_eq(orel_x_next, orel_x_heis):
            heisenberg_ok = False
        ex = qi_inner(psi_hist, qi_matvec(orel_x, psi_hist))
        ey = qi_inner(psi_hist, qi_matvec(orel_y, psi_hist))
        assert ex.im == 0 and ey.im == 0
        sx_ticks.append(ex.re / norm_hist.re)
        sy_ticks.append(ey.re / norm_hist.re)

    return (
        unitary_order4_ok,
        proj_idem_herm_ok,
        proj_trace,
        annihilates_ok,
        intertwine_ok,
        decouple_ok,
        bare_breaks_ok,
        rel_comm_ok,
        heisenberg_ok,
        tuple(sx_ticks),
        tuple(sy_ticks),
    )


def _evaluate_cyclotomic_tsirelson_bound():
    """Execute Part (b): Cyclotomic Q(zeta_8) Tsirelson Bound & SOS Certificate."""
    det_values: list[Fraction] = []
    for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4):
        val = a0 * (b0 + b1) + a1 * (b0 - b1)
        det_values.append(Fraction(abs(val)))
    polytope_count = len(det_values)
    polytope_max = max(det_values)

    s2 = QZeta8.sqrt2()
    inv_s2 = QZeta8.inv_sqrt2()
    one_z8 = QZeta8.from_int(1)
    zero_z8 = QZeta8.from_int(0)
    sqrt2_sq_ok = (s2 * s2 == QZeta8.from_int(2)) and (s2.conj() == s2)
    sqrt2_inv_ok = (s2 * inv_s2 == one_z8) and (inv_s2.conj() == inv_s2)

    z_pauli: Z8Mat = [[one_z8, zero_z8], [zero_z8, -one_z8]]
    x_pauli: Z8Mat = [[zero_z8, one_z8], [one_z8, zero_z8]]
    i2_z8 = z8_eye(2)
    i4_z8 = z8_eye(4)

    a0_op = z8_kron(z_pauli, i2_z8)
    a1_op = z8_kron(x_pauli, i2_z8)
    b0_single = z8_scale(inv_s2, z8_add(z_pauli, x_pauli))
    b1_single = z8_scale(inv_s2, z8_sub(z_pauli, x_pauli))
    b0_op = z8_kron(i2_z8, b0_single)
    b1_op = z8_kron(i2_z8, b1_single)

    inv_comm_ok = True
    for op in (a0_op, a1_op, b0_op, b1_op):
        if not z8_mat_eq(z8_matmul(op, op), i4_z8) or not z8_mat_eq(z8_dagger(op), op):
            inv_comm_ok = False
    for ai in (a0_op, a1_op):
        for bj in (b0_op, b1_op):
            if not z8_is_zero(z8_comm(ai, bj)):
                inv_comm_ok = False

    b_chsh = z8_add(
        z8_matmul(a0_op, z8_add(b0_op, b1_op)),
        z8_matmul(a1_op, z8_sub(b0_op, b1_op)),
    )
    b_chsh_sq = z8_matmul(b_chsh, b_chsh)
    landau_rhs = z8_sub(
        z8_scale(QZeta8.from_int(4), i4_z8),
        z8_matmul(z8_comm(a0_op, a1_op), z8_comm(b0_op, b1_op)),
    )
    landau_ok = z8_mat_eq(b_chsh_sq, landau_rhs)

    w1_sos = z8_sub(z8_scale(inv_s2, z8_add(a0_op, a1_op)), b0_op)
    w2_sos = z8_sub(z8_scale(inv_s2, z8_sub(a0_op, a1_op)), b1_op)
    sos_sum = z8_add(
        z8_matmul(z8_dagger(w1_sos), w1_sos),
        z8_matmul(z8_dagger(w2_sos), w2_sos),
    )
    sos_lhs = z8_sub(z8_scale(QZeta8.from_int(4), i4_z8), z8_scale(s2, b_chsh))
    sos_equiv_lhs = z8_sub(z8_scale(QZeta8.from_int(2) * s2, i4_z8), b_chsh)
    sos_equiv_rhs = z8_scale(inv_s2, sos_sum)
    sos_ok = z8_mat_eq(sos_lhs, sos_sum) and z8_mat_eq(sos_equiv_lhs, sos_equiv_rhs)

    phi_plus: Z8Vec = [one_z8, zero_z8, zero_z8, one_z8]
    w1_phi = z8_matvec(w1_sos, phi_plus)
    w2_phi = z8_matvec(w2_sos, phi_plus)
    bell_annihilated_ok = all(c.is_zero() for c in w1_phi) and all(c.is_zero() for c in w2_phi)

    b_phi = z8_matvec(b_chsh, phi_plus)
    two_s2 = QZeta8.from_int(2) * s2
    bell_eigen_ok = all(b_phi[k] == two_s2 * phi_plus[k] for k in range(4))

    sep_00: Z8Vec = [one_z8, zero_z8, zero_z8, zero_z8]
    sep_exp = z8_inner(sep_00, z8_matvec(b_chsh, sep_00))
    sep_ok = sep_exp == s2

    return (
        polytope_count,
        polytope_max,
        sqrt2_sq_ok,
        sqrt2_inv_ok,
        inv_comm_ok,
        landau_ok,
        sos_ok,
        bell_annihilated_ok,
        bell_eigen_ok,
        sep_ok,
    )


def _check_phase_point_operators():
    """Verify phase point operator Hermiticity, trace, involution, and completeness."""
    i3_z3 = z3_eye(3)
    herm_inv_tr_ok = True
    ortho_comp_ok = True
    sum_all_aqp = z3_zeros(3)
    all_aqp = [[wigner_phase_point_operator_z3(q, p) for p in range(3)] for q in range(3)]

    for q in range(3):
        for p in range(3):
            aqp = all_aqp[q][p]
            sum_all_aqp = z3_add(sum_all_aqp, aqp)
            if (
                not z3_mat_eq(z3_dagger(aqp), aqp)
                or not z3_mat_eq(z3_matmul(aqp, aqp), i3_z3)
                or z3_trace(aqp) != QZeta3.from_int(1)
            ):
                herm_inv_tr_ok = False
            for q2 in range(3):
                for p2 in range(3):
                    tr_prod = z3_trace(z3_matmul(aqp, all_aqp[q2][p2]))
                    expected_tr = QZeta3.from_int(3 if (q == q2 and p == p2) else 0)
                    if tr_prod != expected_tr:
                        ortho_comp_ok = False

    if not z3_mat_eq(z3_scale(Fraction(1, 3), sum_all_aqp), i3_z3):
        ortho_comp_ok = False

    return herm_inv_tr_ok, ortho_comp_ok, all_aqp


def _check_line_marginals(all_aqp: list[list[Z3Mat]]) -> bool:
    """Verify position and momentum line marginals match corresponding projectors."""
    for q in range(3):
        sum_p = z3_zeros(3)
        for p in range(3):
            sum_p = z3_add(sum_p, all_aqp[q][p])
        proj_q = z3_zeros(3)
        proj_q[q][q] = QZeta3.from_int(1)
        if not z3_mat_eq(z3_scale(Fraction(1, 3), sum_p), proj_q):
            return False

    for p in range(3):
        sum_q = z3_zeros(3)
        for q in range(3):
            sum_q = z3_add(sum_q, all_aqp[q][p])
        proj_p = z3_zeros(3)
        for x in range(3):
            for y in range(3):
                proj_p[x][y] = QZeta3.omega_pow(p * (x - y)).scale(Fraction(1, 3))
        if not z3_mat_eq(z3_scale(Fraction(1, 3), sum_q), proj_p):
            return False

    return True


def _evaluate_discrete_weyl_wigner_and_enclosures():
    """Execute Part (c): Discrete Weyl-Wigner on (Z_3)^2 & 12-Decimal Enclosures."""
    herm_inv_tr_ok, ortho_comp_ok, all_aqp = _check_phase_point_operators()
    line_marginals_ok = _check_line_marginals(all_aqp)

    psi_stab: Z3Vec = [QZeta3.from_int(1), QZeta3.from_int(0), QZeta3.from_int(0)]
    w_stab = compute_wigner_table_z3(psi_stab)
    stab_flat = [val for row in w_stab for val in row]
    stab_nonneg_norm_ok = all(v >= 0 for v in stab_flat) and sum(stab_flat) == Fraction(1)
    stab_negativity = sum((abs(v) for v in stab_flat), start=Fraction(0)) - Fraction(1)

    psi_neg: Z3Vec = [QZeta3.from_int(1), QZeta3.from_int(-1), QZeta3.from_int(0)]
    w_neg = compute_wigner_table_z3(psi_neg)
    neg_flat = [val for row in w_neg for val in row]
    pos_marginals = [sum(w_neg[q][p] for p in range(3)) for q in range(3)]
    mom_marginals = [sum(w_neg[q][p] for q in range(3)) for p in range(3)]
    super_ok = (
        sum(neg_flat) == Fraction(1)
        and pos_marginals == [Fraction(1, 2), Fraction(1, 2), Fraction(0)]
        and mom_marginals == [Fraction(0), Fraction(1, 2), Fraction(1, 2)]
        and w_neg[2][0] == Fraction(-1, 3)
    )
    super_min = min(neg_flat)
    super_negativity = sum((abs(v) for v in neg_flat), start=Fraction(0)) - Fraction(1)

    sqrt2_iv = certified_sqrt2_interval()
    sqrt2_bounds_ok = sqrt2_iv.lo * sqrt2_iv.lo <= Fraction(2) <= sqrt2_iv.hi * sqrt2_iv.hi
    two_iv = RationalInterval.exact(Fraction(2))
    half_iv = RationalInterval.exact(Fraction(1, 2))

    tsirelson_iv = two_iv * sqrt2_iv
    excess_iv = tsirelson_iv - two_iv
    per_corr_iv = half_iv * sqrt2_iv

    return (
        herm_inv_tr_ok,
        ortho_comp_ok,
        line_marginals_ok,
        stab_nonneg_norm_ok,
        stab_negativity,
        super_ok,
        super_min,
        super_negativity,
        sqrt2_bounds_ok,
        tsirelson_iv,
        excess_iv,
        per_corr_iv,
    )


def evaluate_page_wootters_tsirelson_wigner_control() -> PageWoottersTsirelsonWignerReport:
    """Execute the QM-218 three-part algebraic and rational-interval verification."""
    (
        unitary_order4_ok,
        proj_idem_herm_ok,
        proj_trace,
        annihilates_ok,
        intertwine_ok,
        decouple_ok,
        bare_breaks_ok,
        rel_comm_ok,
        heisenberg_ok,
        sx_ticks,
        sy_ticks,
    ) = _evaluate_page_wootters_relational_dressing()

    (
        polytope_count,
        polytope_max,
        sqrt2_sq_ok,
        sqrt2_inv_ok,
        inv_comm_ok,
        landau_ok,
        sos_ok,
        bell_annihilated_ok,
        bell_eigen_ok,
        sep_ok,
    ) = _evaluate_cyclotomic_tsirelson_bound()

    (
        herm_inv_tr_ok,
        ortho_comp_ok,
        line_marginals_ok,
        stab_nonneg_norm_ok,
        stab_negativity,
        super_ok,
        super_min,
        super_negativity,
        sqrt2_bounds_ok,
        tsirelson_iv,
        excess_iv,
        per_corr_iv,
    ) = _evaluate_discrete_weyl_wigner_and_enclosures()

    return PageWoottersTsirelsonWignerReport(
        pw_history_shift_unitary_and_order_4=unitary_order4_ok,
        pw_constraint_projector_idempotent_hermitian=proj_idem_herm_ok,
        pw_constraint_projector_trace=proj_trace,
        pw_constraint_annihilates_projector=annihilates_ok,
        pw_dressing_intertwines_history_shift=intertwine_ok,
        pw_dressing_decouples_projector=decouple_ok,
        pw_bare_observable_breaks_constraint=bare_breaks_ok,
        pw_relational_observables_commute_with_constraint=rel_comm_ok,
        pw_heisenberg_step_covariance_exact=heisenberg_ok,
        pw_static_state_sigma_x_ticks=sx_ticks,
        pw_static_state_sigma_y_ticks=sy_ticks,
        chsh_classical_polytope_vertex_count=polytope_count,
        chsh_classical_polytope_max=polytope_max,
        chsh_cyclotomic_sqrt2_squares_to_2=sqrt2_sq_ok,
        chsh_cyclotomic_sqrt2_inverse_exact=sqrt2_inv_ok,
        chsh_observables_involutory_and_spacelike_commuting=inv_comm_ok,
        chsh_landau_identity_exact=landau_ok,
        chsh_sos_decomposition_exact=sos_ok,
        chsh_bell_state_annihilated_by_sos_witnesses=bell_annihilated_ok,
        chsh_bell_state_eigenvalue_is_2_sqrt2=bell_eigen_ok,
        chsh_separable_state_expectation_is_sqrt2=sep_ok,
        wigner_phase_point_hermitian_involutory_unit_trace=herm_inv_tr_ok,
        wigner_phase_point_orthogonality_and_completeness=ortho_comp_ok,
        wigner_line_marginals_match_projectors=line_marginals_ok,
        wigner_stabilizer_nonnegative_and_normalized=stab_nonneg_norm_ok,
        wigner_stabilizer_negativity=stab_negativity,
        wigner_superposition_normalized_and_marginals_exact=super_ok,
        wigner_superposition_min_value=super_min,
        wigner_superposition_negativity=super_negativity,
        sqrt2_square_bounds_enclose_two=sqrt2_bounds_ok,
        tsirelson_bound_interval=tsirelson_iv,
        tsirelson_bound_decimal_12=_format_certified_12(tsirelson_iv),
        bell_violation_excess_interval=excess_iv,
        bell_violation_excess_decimal_12=_format_certified_12(excess_iv),
        tsirelson_per_correlator_interval=per_corr_iv,
        tsirelson_per_correlator_decimal_12=_format_certified_12(per_corr_iv),
    )

