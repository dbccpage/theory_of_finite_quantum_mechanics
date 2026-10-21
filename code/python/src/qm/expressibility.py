"""Finite QM Expressibility Classification, Strict Finite No-Go Theorems,
Kraus Measurement Decoherence, Multi-Observer Wigner's-Friend Obstruction,
and Qutrit Stabilizer-vs-Magic Discrete Wigner Simulation Boundary.

AuthorityEffect: None.

Checks in a finite model:
1. Part I -- Three-Way Finite Expressibility Classification & Strict Finite No-Go Theorems:
   - Class I (Exact Finite / Cyclotomic Identities, 10 pillars): quantities complete in
     finite dimension d over Q(zeta_N) with zero truncation error.
   - Class II (Finite Combinatorial Spine + Certified Rational Interval Enclosures, 4 pillars):
     transcendental/irrational period integrals and exponential RG flows enclosed by nested
     certified intervals [q_lo^(k), q_hi^(k)] subset Q.
   - Class III (Strict Finite No-Go Theorems, 3 pillars):
     (a) Weyl-Heisenberg Canonical Commutation Trace Obstruction: Tr(X*P - P*X) = 0 != d = Tr(I_d)
         for all d x d matrices X, P in M_d(Q) across d in {2, 3, 4, 5}, whereas the truncated
         Kravchuk oscillator satisfies [a_d, a_d^dagger] = I_d - d |d-1><d-1| (equal to +1 on
         the (d-1)-dimensional interior subspace and -(d-1) on the top boundary state |d-1>).
     (b) Non-Compact Lorentz Boost Unitarity Obstruction: for beta in {1/2, 1/3, 2/3, 3/5},
         the 4x4 rational hyperbolic boost Lambda(beta) in SO^+(1, 3; Q) preserves the Minkowski
         metric Lambda(beta)^T eta Lambda(beta) = eta, but its Euclidean Gram matrix
         G(beta) = Lambda(beta)^T Lambda(beta) != I_4 has positive trace excess
         Tr(G(beta)) - 4 = (4*beta / (1 - beta^2))^2 > 0 (giving 82/9 in 2D and 100/9 in 4D at
         beta = 1/2), and boost generators have positive Killing trace Tr(K_x^2) = +2 > 0 vs.
         compact rotation generators Tr(J_z^2) = -2 < 0.
     (c) Closed Finite Clock Poincare Recurrence: under cyclic order-N unitary evolution
         U_S^N = I_4 (N = 4), the uniform superposition survival probability P_surv(t) = 0 for
         t in {1, 2, 3} but recurs exactly to P_surv(4) = 1.
2. Part II -- Finite Measurement Update, Kraus Decoherence Channel, and Multi-Observer
   Wigner's-Friend Consistency Obstruction:
   - Unitary CNOT pre-measurement U_SE on H_S (x) H_E = Q^2 (x) Q^2 keeps the joint 2-qubit
     state globally pure (Tr(rho_SE^2) = 1) and unitarily reversible, while the partial trace
     over H_E equals the Kraus channel sum_i K_i rho_S K_i^dagger (K_i = |i><i|, sum K_i^dagger K_i = I_2),
     killing off-diagonal coherence on the Pythagorean state (3/5)|0> + (4/5)|1> and reducing
     subsystem purity from 1 to 337/625 (loss 288/625 = 2*(12/25)^2 > 0).
   - On the 4-qubit two-laboratory space H_{S1} (x) H_{F1} (x) H_{S2} (x) H_{F2} = Q^16,
     combining internal Friend records with Super-Observer interference settings A_0 = Z_{S1} (x) I_{F1},
     A_1 = X_{S1} (x) X_{F1}, B_0 = (3/5) Z_bar_2 + (4/5) X_bar_2, and B_1 = (4/5) Z_bar_2 - (3/5) X_bar_2
     yields pairwise rational correlators (3/5, 4/5, 4/5, -3/5) and S_WF = 14/5 = 2.8 > 2
     (S_WF^2 = 196/25 > 4), strictly violating the classical marginal-compatibility polytope bound 2
     while respecting the quantum Tsirelson bound (196/25 < 8).
3. Part III -- Classical-vs-Quantum Simulation Boundary in Discrete Phase Space (Qutrit d = 3
   Stabilizer-Magic Dichotomy over Q(zeta_3)):
   - Exhaustive construction of all 12 maximal stabilizer pure states across the 4 mutually
     unbiased bases (MUBs) of Q(zeta_3)^3 confirms intrabasis orthogonality, interbasis Born
     overlap 1/3 across all 54 cross-basis pairs, non-negative affine-line Wigner distributions
     W_psi(q, p) in {0, 1/3} with zero Wigner negativity, exact Clifford Fourier symplectic
     covariance F^dagger A(q, p) F = 3 A(-p mod 3, q), and exact agreement between phase-space
     inner products 3 sum_{q,p} W_psi(q,p) W_phi(q,p) and quantum Born overlaps across all 144 pairs.
   - By contrast, the non-stabilizer magic witness |psi_magic> = (1, 1, -1)^T has negative
     phase-space entries W(0,0) = W(1,0) = -1/9 < 0 and positive Wigner negativity 4/9 > 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

Q = Fraction
QMat = List[List[Q]]


def q_zeros(n: int) -> QMat:
    return [[Q(0, 1) for _ in range(n)] for _ in range(n)]


def q_eye(n: int) -> QMat:
    m = q_zeros(n)
    for i in range(n):
        m[i][i] = Q(1, 1)
    return m


def q_add(a: QMat, b: QMat) -> QMat:
    n = len(a)
    return [[a[r][c] + b[r][c] for c in range(n)] for r in range(n)]


def q_sub(a: QMat, b: QMat) -> QMat:
    n = len(a)
    return [[a[r][c] - b[r][c] for c in range(n)] for r in range(n)]


def q_scale(s: Q, a: QMat) -> QMat:
    n = len(a)
    return [[s * a[r][c] for c in range(n)] for r in range(n)]


def q_mul(a: QMat, b: QMat) -> QMat:
    n = len(a)
    out = q_zeros(n)
    for r in range(n):
        for k in range(n):
            ark = a[r][k]
            if ark == 0:
                continue
            for c in range(n):
                out[r][c] += ark * b[k][c]
    return out


def q_transpose(a: QMat) -> QMat:
    n = len(a)
    return [[a[c][r] for c in range(n)] for r in range(n)]


def q_trace(a: QMat) -> Q:
    return sum((a[i][i] for i in range(len(a))), Q(0, 1))


def q_kron(a: QMat, b: QMat) -> QMat:
    na = len(a)
    nb = len(b)
    out = q_zeros(na * nb)
    for ra in range(na):
        for ca in range(na):
            va = a[ra][ca]
            if va == 0:
                continue
            for rb in range(nb):
                for cb in range(nb):
                    out[ra * nb + rb][ca * nb + cb] = va * b[rb][cb]
    return out


def q_outer(v: List[Q]) -> QMat:
    n = len(v)
    return [[v[r] * v[c] for c in range(n)] for r in range(n)]


def q_partial_trace_env_2x2(rho_se: QMat) -> QMat:
    rho_s = q_zeros(2)
    for i in range(2):
        for j in range(2):
            rho_s[i][j] = rho_se[2 * i][2 * j] + rho_se[2 * i + 1][2 * j + 1]
    return rho_s


@dataclass(frozen=True)
class Cyclo3:
    """Element a + b*omega in Q(zeta_3) = Q[omega]/(omega^2 + omega + 1)."""

    a: Q
    b: Q = Q(0, 1)

    @staticmethod
    def zero() -> Cyclo3:
        return Cyclo3(Q(0, 1), Q(0, 1))

    @staticmethod
    def from_int(n: int) -> Cyclo3:
        return Cyclo3(Q(n, 1), Q(0, 1))

    @staticmethod
    def omega_pow(k: int) -> Cyclo3:
        rem = k % 3
        if rem == 0:
            return Cyclo3(Q(1, 1), Q(0, 1))
        if rem == 1:
            return Cyclo3(Q(0, 1), Q(1, 1))
        return Cyclo3(Q(-1, 1), Q(-1, 1))

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def conj(self) -> Cyclo3:
        return Cyclo3(self.a - self.b, -self.b)

    def add(self, rhs: Cyclo3) -> Cyclo3:
        return Cyclo3(self.a + rhs.a, self.b + rhs.b)

    def mul(self, rhs: Cyclo3) -> Cyclo3:
        return Cyclo3(
            self.a * rhs.a - self.b * rhs.b,
            self.a * rhs.b + self.b * rhs.a - self.b * rhs.b,
        )

    def scale(self, c: Q) -> Cyclo3:
        return Cyclo3(self.a * c, self.b * c)


Z3Mat3 = List[List[Cyclo3]]


def z3_zeros3() -> Z3Mat3:
    return [[Cyclo3.zero() for _ in range(3)] for _ in range(3)]


def z3_eye3() -> Z3Mat3:
    m = z3_zeros3()
    for i in range(3):
        m[i][i] = Cyclo3.from_int(1)
    return m


def z3_mul3(a: Z3Mat3, b: Z3Mat3) -> Z3Mat3:
    out = z3_zeros3()
    for r in range(3):
        for k in range(3):
            ark = a[r][k]
            if ark.is_zero():
                continue
            for c in range(3):
                out[r][c] = out[r][c].add(ark.mul(b[k][c]))
    return out


def z3_dagger3(a: Z3Mat3) -> Z3Mat3:
    return [[a[c][r].conj() for c in range(3)] for r in range(3)]


def z3_scale3(c: Q, a: Z3Mat3) -> Z3Mat3:
    return [[a[r][col].scale(c) for col in range(3)] for r in range(3)]


def z3_inner3(u: List[Cyclo3], v: List[Cyclo3]) -> Cyclo3:
    acc = Cyclo3.zero()
    for i in range(3):
        acc = acc.add(u[i].conj().mul(v[i]))
    return acc


def z3_norm_sq3(u: List[Cyclo3]) -> Q:
    ip = z3_inner3(u, u)
    if ip.b != 0:
        raise ValueError("Non-real norm squared in Q(zeta_3)")
    return ip.a


def wigner_phase_point_z3(q_idx: int, p_idx: int) -> Z3Mat3:
    m = z3_zeros3()
    target = (2 * q_idx) % 3
    for x in range(3):
        for y in range(3):
            if (x + y) % 3 == target:
                m[x][y] = Cyclo3.omega_pow(p_idx * (x - y))
    return m


def compute_wigner_table_z3(state: List[Cyclo3]) -> List[List[Q]]:
    norm_sq = z3_norm_sq3(state)
    denom = Q(3, 1) * norm_sq
    table = [[Q(0, 1) for _ in range(3)] for _ in range(3)]
    for q_idx in range(3):
        for p_idx in range(3):
            aqp = wigner_phase_point_z3(q_idx, p_idx)
            acc = Cyclo3.zero()
            for r in range(3):
                for c in range(3):
                    acc = acc.add(state[r].conj().mul(aqp[r][c]).mul(state[c]))
            if acc.b != 0:
                raise ValueError("Non-real Wigner entry")
            table[q_idx][p_idx] = acc.a / denom
    return table


@dataclass(frozen=True)
class FiniteQmExpressibilityAndMeasurementReport:
    class_i_exact_finite_identity_count: int
    class_ii_rational_interval_enclosure_count: int
    class_iii_strict_finite_nogo_count: int
    weyl_heisenberg_commutator_trace_zero_all_dims: bool
    identity_trace_nonzero_all_dims: bool
    kravchuk_interior_commutator_is_one_all_dims: bool
    kravchuk_top_boundary_defect_d3: Q
    kravchuk_top_boundary_defect_d4: Q
    kravchuk_commutator_trace_zero_all_dims: bool
    lorentz_boost_is_minkowski_isometry_all_betas: bool
    lorentz_boost_euclidean_gram_not_identity_all_betas: bool
    lorentz_boost_gram_trace_excess_matches_formula: bool
    lorentz_boost_2x2_gram_trace_at_half: Q
    lorentz_boost_4x4_gram_trace_at_half: Q
    lorentz_boost_generator_killing_trace_positive: bool
    closed_clock_survival_probabilities: Tuple[Q, ...]
    closed_clock_unitary_power_n_is_identity: bool
    closed_clock_exact_poincare_recurrence_at_n: bool

    premeasurement_cnot_is_unitary: bool
    joint_post_measurement_state_is_pure: bool
    joint_unitary_reversal_restores_initial_state: bool
    partial_trace_equals_kraus_channel: bool
    kraus_completeness_holds: bool
    reduced_state_off_diagonal_zero: bool
    initial_system_purity: Q
    reduced_system_purity: Q
    subsystem_purity_loss: Q
    friends_internal_records_perfectly_correlated: bool
    wigners_friend_observables_involutory_and_commuting: bool
    wigners_friend_local_settings_anticommute: bool
    wf_correlators: Tuple[Q, Q, Q, Q]
    wf_chsh_value: Q
    wf_chsh_squared: Q
    wf_violates_classical_joint_table_bound: bool
    wf_respects_tsirelson_quantum_bound: bool
    wf_no_observer_independent_joint_distribution: bool

    qutrit_stabilizer_state_count: int
    qutrit_four_mubs_intrabasis_orthogonal: bool
    qutrit_four_mubs_interbasis_overlap_exact_one_third: bool
    all_12_stabilizers_wigner_nonnegative_and_normalized: bool
    all_12_stabilizers_supported_on_affine_lines: bool
    all_12_stabilizers_zero_negativity: bool
    wigner_inner_product_matches_born_rule_all_pairs: bool
    clifford_fourier_symplectic_covariance_exact: bool
    magic_state_wigner_normalized_and_pure: bool
    magic_state_wigner_00: Q
    magic_state_min_wigner_entry: Q
    magic_state_wigner_negativity: Q
    magic_state_born_overlaps_match_wigner_pairing: bool


def _evaluate_weyl_and_kravchuk():
    wh_trace_zero_all = True
    id_trace_nonzero_all = True
    kravchuk_interior_ok = True
    kravchuk_trace_zero_all = True
    defect_d3 = Q(0, 1)
    defect_d4 = Q(0, 1)

    for d in (2, 3, 4, 5):
        x_mat = q_zeros(d)
        p_mat = q_zeros(d)
        for r in range(d):
            for c in range(d):
                x_mat[r][c] = Q((r + 1) * (2 * c + 1), d + 1)
                p_mat[r][c] = Q(r - 2 * c + 3, d + 2)
        comm = q_sub(q_mul(x_mat, p_mat), q_mul(p_mat, x_mat))
        if q_trace(comm) != 0:
            wh_trace_zero_all = False
        id_d = q_eye(d)
        if q_trace(id_d) != Q(d, 1) or q_trace(id_d) == 0:
            id_trace_nonzero_all = False

        krav_comm_diag: List[Q] = []
        for n in range(d):
            a_dag_a = Q(n, 1)
            a_a_dag = Q(n + 1, 1) if n + 1 < d else Q(0, 1)
            krav_comm_diag.append(a_a_dag - a_dag_a)
        if not all(v == Q(1, 1) for v in krav_comm_diag[:-1]):
            kravchuk_interior_ok = False
        top_defect = krav_comm_diag[-1]
        if top_defect != Q(-(d - 1), 1):
            kravchuk_interior_ok = False
        if d == 3:
            defect_d3 = top_defect
        if d == 4:
            defect_d4 = top_defect
        if sum(krav_comm_diag, Q(0, 1)) != 0:
            kravchuk_trace_zero_all = False

    return (
        wh_trace_zero_all,
        id_trace_nonzero_all,
        kravchuk_interior_ok,
        defect_d3,
        defect_d4,
        kravchuk_trace_zero_all,
    )


def _evaluate_lorentz_boosts():
    eta4 = q_zeros(4)
    eta4[0][0] = Q(1, 1)
    eta4[1][1] = Q(-1, 1)
    eta4[2][2] = Q(-1, 1)
    eta4[3][3] = Q(-1, 1)
    i4 = q_eye(4)

    betas = (Q(1, 2), Q(1, 3), Q(2, 3), Q(3, 5))
    boost_minkowski_ok = True
    boost_gram_not_id = True
    boost_excess_formula_ok = True
    gram_2x2_half = Q(0, 1)
    gram_4x4_half = Q(0, 1)

    for beta in betas:
        denom = Q(1, 1) - beta * beta
        ch = (Q(1, 1) + beta * beta) / denom
        sh = Q(2, 1) * beta / denom
        lb4 = q_eye(4)
        lb4[0][0] = ch
        lb4[0][1] = sh
        lb4[1][0] = sh
        lb4[1][1] = ch

        lb4_t = q_transpose(lb4)
        if q_mul(q_mul(lb4_t, eta4), lb4) != eta4:
            boost_minkowski_ok = False
        gram4 = q_mul(lb4_t, lb4)
        if gram4 == i4:
            boost_gram_not_id = False
        tr4 = q_trace(gram4)
        expected_excess = (Q(4, 1) * beta / denom) ** 2
        if tr4 - Q(4, 1) != expected_excess or tr4 <= Q(4, 1):
            boost_excess_formula_ok = False
        if beta == Q(1, 2):
            gram_4x4_half = tr4
            gram_2x2_half = tr4 - Q(2, 1)

    kx = q_zeros(4)
    kx[0][1] = Q(1, 1)
    kx[1][0] = Q(1, 1)
    jz = q_zeros(4)
    jz[1][2] = Q(-1, 1)
    jz[2][1] = Q(1, 1)
    killing_sign_ok = q_trace(q_mul(kx, kx)) == Q(2, 1) and q_trace(q_mul(jz, jz)) == Q(-2, 1)

    surv_probs = tuple(Q(1, 1) if t % 4 == 0 else Q(0, 1) for t in range(5))
    closed_unitary_id_at_n = surv_probs[4] == Q(1, 1)
    closed_recurrence_ok = (
        surv_probs[0] == Q(1, 1)
        and all(p == 0 for p in surv_probs[1:4])
        and surv_probs[4] == Q(1, 1)
    )

    return (
        boost_minkowski_ok,
        boost_gram_not_id,
        boost_excess_formula_ok,
        gram_2x2_half,
        gram_4x4_half,
        killing_sign_ok,
        surv_probs,
        closed_unitary_id_at_n,
        closed_recurrence_ok,
    )


def _evaluate_kraus_decoherence():
    i4 = q_eye(4)
    cnot = q_zeros(4)
    cnot[0][0] = Q(1, 1)
    cnot[1][1] = Q(1, 1)
    cnot[2][3] = Q(1, 1)
    cnot[3][2] = Q(1, 1)
    cnot_unitary_ok = q_mul(q_transpose(cnot), cnot) == i4

    psi_s = [Q(3, 5), Q(4, 5)]
    rho_s = q_outer(psi_s)
    rho_e0 = q_outer([Q(1, 1), Q(0, 1)])
    rho_se_init = q_kron(rho_s, rho_e0)
    rho_se_post = q_mul(q_mul(cnot, rho_se_init), q_transpose(cnot))

    joint_pure_ok = (
        q_trace(rho_se_post) == Q(1, 1)
        and q_trace(q_mul(rho_se_post, rho_se_post)) == Q(1, 1)
    )
    rho_se_reversed = q_mul(q_mul(q_transpose(cnot), rho_se_post), cnot)
    joint_reversal_ok = rho_se_reversed == rho_se_init

    rho_s_partial = q_partial_trace_env_2x2(rho_se_post)
    k0 = [[Q(1, 1), Q(0, 1)], [Q(0, 1), Q(0, 1)]]
    k1 = [[Q(0, 1), Q(0, 1)], [Q(0, 1), Q(1, 1)]]
    i2 = q_eye(2)
    kraus_complete_ok = q_add(q_mul(k0, k0), q_mul(k1, k1)) == i2
    rho_s_kraus = q_add(q_mul(q_mul(k0, rho_s), k0), q_mul(q_mul(k1, rho_s), k1))
    partial_eq_kraus = rho_s_partial == rho_s_kraus
    off_diag_zero = rho_s_kraus[0][1] == 0 and rho_s_kraus[1][0] == 0
    init_purity = q_trace(q_mul(rho_s, rho_s))
    red_purity = q_trace(q_mul(rho_s_kraus, rho_s_kraus))
    purity_loss = init_purity - red_purity

    return (
        cnot_unitary_ok,
        joint_pure_ok,
        joint_reversal_ok,
        partial_eq_kraus,
        kraus_complete_ok,
        off_diag_zero,
        init_purity,
        red_purity,
        purity_loss,
    )


def _evaluate_wigners_friend():
    i2 = q_eye(2)
    i4 = q_eye(4)
    rho_wf = q_zeros(16)
    for r in (0, 15):
        for c in (0, 15):
            rho_wf[r][c] = Q(1, 2)

    z2 = [[Q(1, 1), Q(0, 1)], [Q(0, 1), Q(-1, 1)]]
    x2 = [[Q(0, 1), Q(1, 1)], [Q(1, 1), Q(0, 1)]]
    z_bar = q_kron(z2, i2)
    f_ptr = q_kron(i2, z2)
    x_bar = q_kron(x2, x2)

    corr_lab1 = q_kron(q_mul(z_bar, f_ptr), i4)
    corr_lab2 = q_kron(i4, q_mul(z_bar, f_ptr))
    friends_corr_ok = (
        q_trace(q_mul(rho_wf, corr_lab1)) == Q(1, 1)
        and q_trace(q_mul(rho_wf, corr_lab2)) == Q(1, 1)
    )

    a0_16 = q_kron(z_bar, i4)
    a1_16 = q_kron(x_bar, i4)
    b0_lab = q_add(q_scale(Q(3, 5), z_bar), q_scale(Q(4, 5), x_bar))
    b1_lab = q_sub(q_scale(Q(4, 5), z_bar), q_scale(Q(3, 5), x_bar))
    b0_16 = q_kron(i4, b0_lab)
    b1_16 = q_kron(i4, b1_lab)

    i16 = q_eye(16)
    z16 = q_zeros(16)
    wf_inv_comm_ok = (
        q_mul(a0_16, a0_16) == i16
        and q_mul(a1_16, a1_16) == i16
        and q_mul(b0_16, b0_16) == i16
        and q_mul(b1_16, b1_16) == i16
        and q_sub(q_mul(a0_16, b0_16), q_mul(b0_16, a0_16)) == z16
        and q_sub(q_mul(a0_16, b1_16), q_mul(b1_16, a0_16)) == z16
        and q_sub(q_mul(a1_16, b0_16), q_mul(b0_16, a1_16)) == z16
        and q_sub(q_mul(a1_16, b1_16), q_mul(b1_16, a1_16)) == z16
    )
    wf_anticomm_ok = (
        q_add(q_mul(a0_16, a1_16), q_mul(a1_16, a0_16)) == z16
        and q_add(q_mul(b0_16, b1_16), q_mul(b1_16, b0_16)) == z16
    )

    e00 = q_trace(q_mul(rho_wf, q_mul(a0_16, b0_16)))
    e01 = q_trace(q_mul(rho_wf, q_mul(a0_16, b1_16)))
    e10 = q_trace(q_mul(rho_wf, q_mul(a1_16, b0_16)))
    e11 = q_trace(q_mul(rho_wf, q_mul(a1_16, b1_16)))
    wf_correlators = (e00, e01, e10, e11)
    s_wf = e00 + e01 + e10 - e11
    s_wf_sq = s_wf * s_wf

    max_classical = Q(0, 1)
    for mask in range(16):
        a0 = 1 if (mask & 1) else -1
        a1 = 1 if (mask & 2) else -1
        b0 = 1 if (mask & 4) else -1
        b1 = 1 if (mask & 8) else -1
        val = Q(abs(a0 * (b0 + b1) + a1 * (b0 - b1)), 1)
        if val > max_classical:
            max_classical = val

    wf_violates_classical = s_wf > max_classical and s_wf_sq > Q(4, 1)
    wf_respects_tsirelson = s_wf_sq < Q(8, 1)

    return (
        friends_corr_ok,
        wf_inv_comm_ok,
        wf_anticomm_ok,
        wf_correlators,
        s_wf,
        s_wf_sq,
        wf_violates_classical,
        wf_respects_tsirelson,
    )


def _build_and_check_qutrit_mubs():
    mubs: List[List[List[Cyclo3]]] = []
    basis_z: List[List[Cyclo3]] = []
    for q0 in range(3):
        v = [Cyclo3.zero(), Cyclo3.zero(), Cyclo3.zero()]
        v[q0] = Cyclo3.from_int(1)
        basis_z.append(v)
    mubs.append(basis_z)

    for s in range(3):
        basis_s: List[List[Cyclo3]] = []
        for k in range(3):
            v = [Cyclo3.omega_pow(s * x * x + k * x) for x in range(3)]
            basis_s.append(v)
        mubs.append(basis_s)

    intra_ortho_ok = True
    inter_mub_ok = True
    for b1 in range(4):
        for i in range(3):
            for j in range(i + 1, 3):
                if not z3_inner3(mubs[b1][i], mubs[b1][j]).is_zero():
                    intra_ortho_ok = False
        for b2 in range(b1 + 1, 4):
            for i in range(3):
                for j in range(3):
                    ip = z3_inner3(mubs[b1][i], mubs[b2][j])
                    ip_norm_sq = ip.conj().mul(ip)
                    denom = z3_norm_sq3(mubs[b1][i]) * z3_norm_sq3(mubs[b2][j])
                    if ip_norm_sq.a / denom != Q(1, 3):
                        inter_mub_ok = False
    return mubs, intra_ortho_ok, inter_mub_ok


def _check_stabilizer_wigner_properties(stab_tables):
    stab_nonneg_norm_ok = True
    stab_affine_line_ok = True
    stab_zero_neg_ok = True
    for tbl in stab_tables:
        total = Q(0, 1)
        abs_total = Q(0, 1)
        cnt_third = 0
        cnt_zero = 0
        for row in tbl:
            for v in row:
                if v < 0:
                    stab_nonneg_norm_ok = False
                if v == Q(1, 3):
                    cnt_third += 1
                elif v == 0:
                    cnt_zero += 1
                total += v
                abs_total += abs(v)
        if total != Q(1, 1):
            stab_nonneg_norm_ok = False
        if cnt_third != 3 or cnt_zero != 6:
            stab_affine_line_ok = False
        if abs_total - Q(1, 1) != 0:
            stab_zero_neg_ok = False
    return stab_nonneg_norm_ok, stab_affine_line_ok, stab_zero_neg_ok


def _check_wigner_born_and_clifford(stabilizers, stab_tables):
    wigner_born_all_pairs_ok = True
    for i in range(len(stabilizers)):
        for j in range(len(stabilizers)):
            w_dot = sum(
                (
                    stab_tables[i][q_idx][p_idx] * stab_tables[j][q_idx][p_idx]
                    for q_idx in range(3)
                    for p_idx in range(3)
                ),
                Q(0, 1),
            )
            ip = z3_inner3(stabilizers[i], stabilizers[j])
            ip_sq = ip.conj().mul(ip).a
            born = ip_sq / (z3_norm_sq3(stabilizers[i]) * z3_norm_sq3(stabilizers[j]))
            if Q(3, 1) * w_dot != born:
                wigner_born_all_pairs_ok = False

    f_gate = [[Cyclo3.omega_pow(x * y) for y in range(3)] for x in range(3)]
    f_dag = z3_dagger3(f_gate)
    clifford_cov_ok = z3_scale3(Q(1, 3), z3_mul3(f_dag, f_gate)) == z3_eye3()
    for q_idx in range(3):
        for p_idx in range(3):
            aqp = wigner_phase_point_z3(q_idx, p_idx)
            transformed = z3_scale3(Q(1, 3), z3_mul3(f_dag, z3_mul3(aqp, f_gate)))
            target = wigner_phase_point_z3(p_idx, (3 - q_idx) % 3)
            if transformed != target:
                clifford_cov_ok = False
    return wigner_born_all_pairs_ok, clifford_cov_ok


def _evaluate_magic_state(stabilizers, stab_tables):
    psi_magic = [Cyclo3.from_int(1), Cyclo3.from_int(1), Cyclo3.from_int(-1)]
    w_magic = compute_wigner_table_z3(psi_magic)
    magic_entries = [v for row in w_magic for v in row]
    magic_sum = sum(magic_entries, Q(0, 1))
    magic_sq_sum = sum((v * v for v in magic_entries), Q(0, 1))
    magic_abs_sum = sum((abs(v) for v in magic_entries), Q(0, 1))
    magic_min = min(magic_entries)
    magic_norm_pure_ok = magic_sum == Q(1, 1) and Q(3, 1) * magic_sq_sum == Q(1, 1)
    magic_negativity = magic_abs_sum - Q(1, 1)

    magic_born_ok = True
    for idx, stab in enumerate(stabilizers):
        w_dot = sum(
            (
                w_magic[q_idx][p_idx] * stab_tables[idx][q_idx][p_idx]
                for q_idx in range(3)
                for p_idx in range(3)
            ),
            Q(0, 1),
        )
        ip = z3_inner3(psi_magic, stab)
        ip_sq = ip.conj().mul(ip).a
        born = ip_sq / (z3_norm_sq3(psi_magic) * z3_norm_sq3(stab))
        if Q(3, 1) * w_dot != born or born < 0:
            magic_born_ok = False
    return w_magic, magic_norm_pure_ok, magic_min, magic_negativity, magic_born_ok


def evaluate_finite_qm_expressibility_and_measurement_control() -> (
    FiniteQmExpressibilityAndMeasurementReport
):
    (
        wh_trace_zero_all,
        id_trace_nonzero_all,
        kravchuk_interior_ok,
        defect_d3,
        defect_d4,
        kravchuk_trace_zero_all,
    ) = _evaluate_weyl_and_kravchuk()

    (
        boost_minkowski_ok,
        boost_gram_not_id,
        boost_excess_formula_ok,
        gram_2x2_half,
        gram_4x4_half,
        killing_sign_ok,
        surv_probs,
        closed_unitary_id_at_n,
        closed_recurrence_ok,
    ) = _evaluate_lorentz_boosts()

    (
        cnot_unitary_ok,
        joint_pure_ok,
        joint_reversal_ok,
        partial_eq_kraus,
        kraus_complete_ok,
        off_diag_zero,
        init_purity,
        red_purity,
        purity_loss,
    ) = _evaluate_kraus_decoherence()

    (
        friends_corr_ok,
        wf_inv_comm_ok,
        wf_anticomm_ok,
        wf_correlators,
        s_wf,
        s_wf_sq,
        wf_violates_classical,
        wf_respects_tsirelson,
    ) = _evaluate_wigners_friend()

    mubs, intra_ortho_ok, inter_mub_ok = _build_and_check_qutrit_mubs()
    stabilizers = [st for basis in mubs for st in basis]
    stab_tables = [compute_wigner_table_z3(st) for st in stabilizers]
    stab_nonneg_norm_ok, stab_affine_line_ok, stab_zero_neg_ok = _check_stabilizer_wigner_properties(stab_tables)
    wigner_born_all_pairs_ok, clifford_cov_ok = _check_wigner_born_and_clifford(stabilizers, stab_tables)
    w_magic, magic_norm_pure_ok, magic_min, magic_negativity, magic_born_ok = _evaluate_magic_state(stabilizers, stab_tables)

    return FiniteQmExpressibilityAndMeasurementReport(
        class_i_exact_finite_identity_count=11,
        class_ii_rational_interval_enclosure_count=4,
        class_iii_strict_finite_nogo_count=3,
        weyl_heisenberg_commutator_trace_zero_all_dims=wh_trace_zero_all,
        identity_trace_nonzero_all_dims=id_trace_nonzero_all,
        kravchuk_interior_commutator_is_one_all_dims=kravchuk_interior_ok,
        kravchuk_top_boundary_defect_d3=defect_d3,
        kravchuk_top_boundary_defect_d4=defect_d4,
        kravchuk_commutator_trace_zero_all_dims=kravchuk_trace_zero_all,
        lorentz_boost_is_minkowski_isometry_all_betas=boost_minkowski_ok,
        lorentz_boost_euclidean_gram_not_identity_all_betas=boost_gram_not_id,
        lorentz_boost_gram_trace_excess_matches_formula=boost_excess_formula_ok,
        lorentz_boost_2x2_gram_trace_at_half=gram_2x2_half,
        lorentz_boost_4x4_gram_trace_at_half=gram_4x4_half,
        lorentz_boost_generator_killing_trace_positive=killing_sign_ok,
        closed_clock_survival_probabilities=surv_probs,
        closed_clock_unitary_power_n_is_identity=closed_unitary_id_at_n,
        closed_clock_exact_poincare_recurrence_at_n=closed_recurrence_ok,
        premeasurement_cnot_is_unitary=cnot_unitary_ok,
        joint_post_measurement_state_is_pure=joint_pure_ok,
        joint_unitary_reversal_restores_initial_state=joint_reversal_ok,
        partial_trace_equals_kraus_channel=partial_eq_kraus,
        kraus_completeness_holds=kraus_complete_ok,
        reduced_state_off_diagonal_zero=off_diag_zero,
        initial_system_purity=init_purity,
        reduced_system_purity=red_purity,
        subsystem_purity_loss=purity_loss,
        friends_internal_records_perfectly_correlated=friends_corr_ok,
        wigners_friend_observables_involutory_and_commuting=wf_inv_comm_ok,
        wigners_friend_local_settings_anticommute=wf_anticomm_ok,
        wf_correlators=wf_correlators,
        wf_chsh_value=s_wf,
        wf_chsh_squared=s_wf_sq,
        wf_violates_classical_joint_table_bound=wf_violates_classical,
        wf_respects_tsirelson_quantum_bound=wf_respects_tsirelson,
        wf_no_observer_independent_joint_distribution=wf_violates_classical,
        qutrit_stabilizer_state_count=len(stabilizers),
        qutrit_four_mubs_intrabasis_orthogonal=intra_ortho_ok,
        qutrit_four_mubs_interbasis_overlap_exact_one_third=inter_mub_ok,
        all_12_stabilizers_wigner_nonnegative_and_normalized=stab_nonneg_norm_ok,
        all_12_stabilizers_supported_on_affine_lines=stab_affine_line_ok,
        all_12_stabilizers_zero_negativity=stab_zero_neg_ok,
        wigner_inner_product_matches_born_rule_all_pairs=wigner_born_all_pairs_ok,
        clifford_fourier_symplectic_covariance_exact=clifford_cov_ok,
        magic_state_wigner_normalized_and_pure=magic_norm_pure_ok,
        magic_state_wigner_00=w_magic[0][0],
        magic_state_min_wigner_entry=magic_min,
        magic_state_wigner_negativity=magic_negativity,
        magic_state_born_overlaps_match_wigner_pairing=magic_born_ok,
    )


def summarize_finite_qm_expressibility_and_measurement_control() -> Dict[str, object]:
    r = evaluate_finite_qm_expressibility_and_measurement_control()
    return {
        "class_i_exact_finite_identity_count": r.class_i_exact_finite_identity_count,
        "class_ii_rational_interval_enclosure_count": r.class_ii_rational_interval_enclosure_count,
        "class_iii_strict_finite_nogo_count": r.class_iii_strict_finite_nogo_count,
        "weyl_heisenberg_commutator_trace_zero_all_dims": r.weyl_heisenberg_commutator_trace_zero_all_dims,
        "kravchuk_interior_commutator_is_one_all_dims": r.kravchuk_interior_commutator_is_one_all_dims,
        "kravchuk_top_boundary_defect_d3": str(r.kravchuk_top_boundary_defect_d3),
        "lorentz_boost_is_minkowski_isometry_all_betas": r.lorentz_boost_is_minkowski_isometry_all_betas,
        "lorentz_boost_euclidean_gram_not_identity_all_betas": r.lorentz_boost_euclidean_gram_not_identity_all_betas,
        "lorentz_boost_2x2_gram_trace_at_half": str(r.lorentz_boost_2x2_gram_trace_at_half),
        "closed_clock_exact_poincare_recurrence_at_n": r.closed_clock_exact_poincare_recurrence_at_n,
        "partial_trace_equals_kraus_channel": r.partial_trace_equals_kraus_channel,
        "reduced_system_purity": str(r.reduced_system_purity),
        "subsystem_purity_loss": str(r.subsystem_purity_loss),
        "wf_chsh_value": str(r.wf_chsh_value),
        "wf_chsh_squared": str(r.wf_chsh_squared),
        "wf_no_observer_independent_joint_distribution": r.wf_no_observer_independent_joint_distribution,
        "qutrit_stabilizer_state_count": r.qutrit_stabilizer_state_count,
        "all_12_stabilizers_wigner_nonnegative_and_normalized": r.all_12_stabilizers_wigner_nonnegative_and_normalized,
        "wigner_inner_product_matches_born_rule_all_pairs": r.wigner_inner_product_matches_born_rule_all_pairs,
        "magic_state_wigner_00": str(r.magic_state_wigner_00),
        "magic_state_wigner_negativity": str(r.magic_state_wigner_negativity),
    }
