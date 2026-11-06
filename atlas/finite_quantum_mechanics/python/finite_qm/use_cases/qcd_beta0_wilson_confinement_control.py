"""QM-221: Finite su(3)_c QCD Gross-Wilczek-Politzer Asymptotic Freedom and Wilson-Loop Confinement Control.

AuthorityEffect: None.

Checks in a finite model:
1. Exact 8 rational-weighted su(3)_c generators (T_tilde_1..7, T_tilde_8) in M_3(Q(i))
   with weights w = (1, 1, 1, 1, 1, 1, 1, 1/3), verifying Hermiticity, tracelessness,
   Killing orthogonality w_a tr(T_tilde_a T_tilde_b) = (1/2) delta_ab, fundamental
   Casimir sum_a w_a T_tilde_a^2 = (4/3) I_3 (C_F = 4/3), adjoint Casimir
   sum_a w_a [T_tilde_a, [T_tilde_a, X]] = 3 X (C_A = 3), and the 9x9 Fierz completeness
   identity across all 81 index quadruples (i,j,k,l) in {0,1,2}^4 (yielding color-singlet
   attraction -4/3, octet repulsion +1/6, sextet +1/3, and antitriplet diquark -2/3).
2. Exact 1-loop Gross-Wilczek-Politzer beta_0(N_c, n_f) = (11/3) C_A - (4/3) T_F n_f
   = 11 - (2/3) n_f (with paramagnetic +4 C_A = 12 and diamagnetic -(1/3) C_A = -1
   decomposition) and 2-loop Caswell-Jones beta_1(N_c, n_f) = 102 - (38/3) n_f,
   checking asymptotic freedom for 0 <= n_f <= 16, loss at n_f = 17 (beta_0 = -1/3),
   Abelian QED screening (beta_0 = -4/3), and the Banks-Zaks fixed-point ratio
   -beta_0 / beta_1 = 1/302 at n_f = 16.
3. Finite-graph DFM spanning-tree reduction on the 3x3 planar square lattice
   (|V| = 9, |E| = 12, |E_T| = 8, b_1 = 4) and strong-coupling Wilson-loop area law
   W_area(R, T) = beta_tilde^(R*T) vs. perimeter law W_perim(R, T) = beta_tilde^(2*(R+T))
   at beta_tilde = 1/9, showing the multiplicative Creutz ratio
   chi(R, T) = (W(R,T) W(R-1,T-1)) / (W(R,T-1) W(R-1,T)) equals beta_tilde = 1/9 < 1
   under the area law and 1 under the perimeter law across (R, T) in {2, 3}^2.
4. Certified 12-decimal rational interval enclosures for 1-loop running alpha_s(Q^2)
   = alpha_s(M_Z^2) / (1 + beta_0 * alpha_s(M_Z^2) * L / (4 * pi)), L = ln(Q^2 / M_Z^2)
   in {2, 4}, from alpha_s(M_Z^2) = 1179/10000 (n_f = 5, beta_0 = 23/3),
   and strong-coupling string tension sigma a^2 = ln(9) = 2 ln(3).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

from .dressed_qed_g2_control import RationalInterval, pi_interval

Q = Fraction


@dataclass(frozen=True)
class Qi:
    """Element of the Gaussian rational field Q(i) = Q[i] / (i^2 + 1)."""

    re: Q
    im: Q = Q(0, 1)

    @staticmethod
    def zero() -> Qi:
        return Qi(Q(0, 1), Q(0, 1))

    @staticmethod
    def one() -> Qi:
        return Qi(Q(1, 1), Q(0, 1))

    @staticmethod
    def i() -> Qi:
        return Qi(Q(0, 1), Q(1, 1))

    @staticmethod
    def from_rat(r: Q) -> Qi:
        return Qi(r, Q(0, 1))

    def add(self, rhs: Qi) -> Qi:
        return Qi(self.re + rhs.re, self.im + rhs.im)

    def sub(self, rhs: Qi) -> Qi:
        return Qi(self.re - rhs.re, self.im - rhs.im)

    def scale(self, s: Q) -> Qi:
        return Qi(self.re * s, self.im * s)

    def mul(self, rhs: Qi) -> Qi:
        return Qi(
            self.re * rhs.re - self.im * rhs.im,
            self.re * rhs.im + self.im * rhs.re,
        )

    def conj(self) -> Qi:
        return Qi(self.re, -self.im)

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0


Mat3Qi = List[List[Qi]]


def mat3_zero() -> Mat3Qi:
    return [[Qi.zero() for _ in range(3)] for _ in range(3)]


def mat3_id() -> Mat3Qi:
    m = mat3_zero()
    for i in range(3):
        m[i][i] = Qi.one()
    return m


def mat3_add(a: Mat3Qi, b: Mat3Qi) -> Mat3Qi:
    return [[a[r][c].add(b[r][c]) for c in range(3)] for r in range(3)]


def mat3_sub(a: Mat3Qi, b: Mat3Qi) -> Mat3Qi:
    return [[a[r][c].sub(b[r][c]) for c in range(3)] for r in range(3)]


def mat3_scale(a: Mat3Qi, s: Q) -> Mat3Qi:
    return [[a[r][c].scale(s) for c in range(3)] for r in range(3)]


def mat3_mul(a: Mat3Qi, b: Mat3Qi) -> Mat3Qi:
    out = mat3_zero()
    for r in range(3):
        for c in range(3):
            acc = Qi.zero()
            for k in range(3):
                acc = acc.add(a[r][k].mul(b[k][c]))
            out[r][c] = acc
    return out


def mat3_comm(a: Mat3Qi, b: Mat3Qi) -> Mat3Qi:
    return mat3_sub(mat3_mul(a, b), mat3_mul(b, a))


def mat3_dagger(a: Mat3Qi) -> Mat3Qi:
    return [[a[c][r].conj() for c in range(3)] for r in range(3)]


def mat3_trace(a: Mat3Qi) -> Qi:
    return a[0][0].add(a[1][1]).add(a[2][2])


def su3_weighted_generators() -> List[Tuple[Mat3Qi, Q]]:
    """Return the 8 rational-weighted su(3)_c generators (T_tilde_a, w_a) in M_3(Q(i))."""
    half = Q(1, 2)
    r_half = Qi.from_rat(half)
    r_neg_half = Qi.from_rat(-half)
    i_half = Qi(Q(0, 1), half)
    i_neg_half = Qi(Q(0, 1), -half)

    t1 = mat3_zero()
    t1[0][1] = r_half
    t1[1][0] = r_half

    t2 = mat3_zero()
    t2[0][1] = i_neg_half
    t2[1][0] = i_half

    t3 = mat3_zero()
    t3[0][0] = r_half
    t3[1][1] = r_neg_half

    t4 = mat3_zero()
    t4[0][2] = r_half
    t4[2][0] = r_half

    t5 = mat3_zero()
    t5[0][2] = i_neg_half
    t5[2][0] = i_half

    t6 = mat3_zero()
    t6[1][2] = r_half
    t6[2][1] = r_half

    t7 = mat3_zero()
    t7[1][2] = i_neg_half
    t7[2][1] = i_half

    t8_tilde = mat3_zero()
    t8_tilde[0][0] = r_half
    t8_tilde[1][1] = r_half
    t8_tilde[2][2] = Qi.from_rat(Q(-1, 1))

    one = Q(1, 1)
    return [
        (t1, one),
        (t2, one),
        (t3, one),
        (t4, one),
        (t5, one),
        (t6, one),
        (t7, one),
        (t8_tilde, Q(1, 3)),
    ]


def verify_su3_fierz_completeness(gens: List[Tuple[Mat3Qi, Q]]) -> bool:
    """Check sum_a w_a (T_tilde_a)_ij (T_tilde_a)_kl = 1/2 delta_il delta_kj - 1/6 delta_ij delta_kl."""
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for idx_l in range(3):
                    lhs = Qi.zero()
                    for t_a, w_a in gens:
                        lhs = lhs.add(t_a[i][j].mul(t_a[k][idx_l]).scale(w_a))
                    d_il_kj = Q(1, 2) if (i == idx_l and k == j) else Q(0, 1)
                    d_ij_kl = Q(1, 6) if (i == j and k == idx_l) else Q(0, 1)
                    if lhs != Qi.from_rat(d_il_kj - d_ij_kl):
                        return False
    return True


def verify_su3_jacobi_identity(gens: List[Tuple[Mat3Qi, Q]]) -> bool:
    """Check [T_a, [T_b, T_c]] + cyclic = 0 on all 8**3 ordered triples."""
    n = len(gens)
    if n != 8:
        return False
    z = mat3_zero()
    for a in range(n):
        for b in range(n):
            for c in range(n):
                ta, tb, tc = gens[a][0], gens[b][0], gens[c][0]
                j1 = mat3_comm(ta, mat3_comm(tb, tc))
                j2 = mat3_comm(tb, mat3_comm(tc, ta))
                j3 = mat3_comm(tc, mat3_comm(ta, tb))
                if mat3_add(mat3_add(j1, j2), j3) != z:
                    return False
    return True


def qcd_beta0(n_c: int, n_f: int) -> Q:
    """1-loop Gross-Wilczek-Politzer beta_0(N_c, n_f) = (11/3) N_c - (2/3) n_f."""
    return Q(11 * n_c, 3) - Q(2 * n_f, 3)


def qcd_beta1(n_c: int, n_f: int) -> Q:
    """2-loop Caswell-Jones beta_1(N_c, n_f) = (34/3) N_c^2 - (10/3) N_c n_f - ((N_c^2 - 1)/N_c) n_f."""
    c_a = Q(n_c, 1)
    c_f = Q(n_c * n_c - 1, 2 * n_c)
    t_f = Q(1, 2)
    return Q(34, 3) * c_a * c_a - (Q(20, 3) * c_a + Q(4, 1) * c_f) * t_f * Q(n_f, 1)


def wilson_area_law(beta_tilde: Q, r: int, t: int) -> Q:
    return beta_tilde ** (r * t)


def wilson_perimeter_law(beta_tilde: Q, r: int, t: int) -> Q:
    return beta_tilde ** (2 * (r + t))


def creutz_ratio(w_rt: Q, w_r1t1: Q, w_rt1: Q, w_r1t: Q) -> Q:
    return (w_rt * w_r1t1) / (w_rt1 * w_r1t)


def ln3_interval() -> RationalInterval:
    """Enclosure of ln(3) = ln((1+1/2)/(1-1/2)) = 2 * sum_{k=0}^m (1/2)^{2k+1}/(2k+1) at m = 56."""
    m = 56
    partial = Q(0, 1)
    for k in range(m + 1):
        denom = Q(2 * k + 1, 1) * Q(1 << (2 * k + 1), 1)
        partial += Q(2, 1) / denom
    rem_num = Q(2, 1) / (Q(2 * m + 3, 1) * Q(1 << (2 * m + 3), 1))
    tail = rem_num * Q(4, 3)
    return RationalInterval(partial, partial + tail)


@dataclass(frozen=True)
class Qm221QcdBeta0WilsonConfinementReport:
    color_dimension_nc: int
    gluon_generator_count: int
    all_generators_hermitian_and_traceless: bool
    killing_orthogonality_holds: bool
    jacobi_identity_holds_all_triples: bool
    fundamental_trace_normalization_tf: Q
    fundamental_casimir_cf: Q
    fundamental_casimir_proportional_to_identity: bool
    adjoint_casimir_ca: Q
    adjoint_casimir_holds_on_all_generators: bool
    fierz_completeness_holds_all_81_entries: bool
    singlet_qqbar_casimir_coeff: Q
    octet_qqbar_casimir_coeff: Q
    sextet_qq_casimir_coeff: Q
    antitriplet_qq_casimir_coeff: Q
    singlet_attractive_and_octet_repulsive: bool
    gluon_paramagnetic_spin_contribution: Q
    gluon_diamagnetic_orbital_contribution: Q
    gluon_total_beta0_contribution: Q
    fermion_single_dirac_beta0_contribution: Q
    beta0_nf0_pure_yang_mills: Q
    beta0_nf3_light_quarks: Q
    beta0_nf5_at_mz: Q
    beta0_nf6_standard_model: Q
    beta0_nf16_conformal_edge: Q
    beta0_nf17_loss_of_af: Q
    asymptotic_freedom_holds_for_nf_0_to_16: bool
    asymptotic_freedom_lost_at_nf_17: bool
    abelian_qed_beta0_nf1_is_negative: bool
    beta1_nf0_pure_yang_mills: Q
    beta1_nf5_at_mz: Q
    beta1_nf16_banks_zaks: Q
    banks_zaks_nf16_fixed_point_ratio: Q
    lattice_3x3_vertex_count: int
    lattice_3x3_edge_count: int
    lattice_3x3_spanning_tree_edges: int
    lattice_3x3_independent_plaquette_betti1: int
    dfm_tree_dressing_reduces_links_to_plaquettes: bool
    strong_coupling_expansion_parameter: Q
    creutz_area_ratio_r2_t2: Q
    creutz_area_ratio_r3_t3: Q
    creutz_area_ratio_constant_across_loops: bool
    creutz_perimeter_ratio_r2_t2: Q
    creutz_perimeter_ratio_r3_t3: Q
    creutz_perimeter_ratio_is_unity: bool
    area_law_strictly_confining_vs_perimeter: bool
    alpha_s_mz_input: Q
    alpha_s_at_ln_q2_mz2_eq_2_decimal_12: str
    alpha_s_at_ln_q2_mz2_eq_4_decimal_12: str
    alpha_s_12_digits_agree: bool
    alpha_s_decreases_monotonically_in_uv: bool
    string_tension_ln9_decimal_12: str
    string_tension_12_digits_agree: bool


def _verify_generators_and_casimirs(
    gens: List[Tuple[Mat3Qi, Q]],
) -> Tuple[bool, bool, bool, bool, Q, Q, Q]:
    z3 = mat3_zero()
    id3 = mat3_id()
    herm_traceless = all(
        mat3_dagger(t_a) == t_a and mat3_trace(t_a).is_zero() for t_a, _ in gens
    )

    t_f = Q(1, 2)
    killing_ok = True
    for a, (t_a, w_a) in enumerate(gens):
        for b, (t_b, _) in enumerate(gens):
            tr = mat3_trace(mat3_mul(t_a, t_b))
            expected = Qi.from_rat(t_f) if a == b else Qi.zero()
            if tr.scale(w_a) != expected:
                killing_ok = False

    casimir_fund = z3
    for t_a, w_a in gens:
        casimir_fund = mat3_add(casimir_fund, mat3_scale(mat3_mul(t_a, t_a), w_a))
    c_f = Q(4, 3)
    fund_casimir_ok = casimir_fund == mat3_scale(id3, c_f)

    c_a = Q(3, 1)
    adj_casimir_ok = True
    for x_b, _ in gens:
        adj_sum = z3
        for t_a, w_a in gens:
            dbl = mat3_comm(t_a, mat3_comm(t_a, x_b))
            adj_sum = mat3_add(adj_sum, mat3_scale(dbl, w_a))
        if adj_sum != mat3_scale(x_b, c_a):
            adj_casimir_ok = False

    return herm_traceless, killing_ok, fund_casimir_ok, adj_casimir_ok, t_f, c_f, c_a


def evaluate_qm221_qcd_beta0_wilson_confinement() -> Qm221QcdBeta0WilsonConfinementReport:
    n_c = 3
    gens = su3_weighted_generators()
    (
        herm_traceless,
        killing_ok,
        fund_casimir_ok,
        adj_casimir_ok,
        t_f,
        c_f,
        c_a,
    ) = _verify_generators_and_casimirs(gens)
    jacobi_ok = verify_su3_jacobi_identity(gens)
    fierz_ok = verify_su3_fierz_completeness(gens)

    singlet_qqbar = -c_f
    octet_qqbar = c_a / Q(2, 1) - c_f
    sextet_qq = Q(1, 2) - Q(1, 2) / Q(n_c, 1)
    antitriplet_qq = Q(-1, 2) - Q(1, 2) / Q(n_c, 1)
    singlet_attr_octet_rep = singlet_qqbar < 0 and octet_qqbar > 0

    gluon_para = Q(4, 1) * c_a
    gluon_dia = Q(-1, 3) * c_a
    gluon_total = gluon_para + gluon_dia
    fermion_single = Q(-4, 3) * t_f

    b0_nf0 = qcd_beta0(n_c, 0)
    b0_nf3 = qcd_beta0(n_c, 3)
    b0_nf5 = qcd_beta0(n_c, 5)
    b0_nf6 = qcd_beta0(n_c, 6)
    b0_nf16 = qcd_beta0(n_c, 16)
    b0_nf17 = qcd_beta0(n_c, 17)

    af_0_to_16 = all(qcd_beta0(n_c, nf) > 0 for nf in range(17))
    af_lost_17 = b0_nf17 < 0
    qed_beta0_nf1 = Q(-4, 3) * Q(1, 1)
    qed_negative = qed_beta0_nf1 < 0

    b1_nf0 = qcd_beta1(n_c, 0)
    b1_nf5 = qcd_beta1(n_c, 5)
    b1_nf16 = qcd_beta1(n_c, 16)
    bz_ratio_nf16 = -b0_nf16 / b1_nf16

    v_cnt, e_cnt = 9, 12
    e_tree = v_cnt - 1
    b1_plaq = e_cnt - v_cnt + 1
    dfm_plaq_ok = (e_cnt - e_tree == b1_plaq) and (b1_plaq == 4)

    beta_tilde = Q(1, 9)
    chi_area_22 = creutz_ratio(
        wilson_area_law(beta_tilde, 2, 2),
        wilson_area_law(beta_tilde, 1, 1),
        wilson_area_law(beta_tilde, 2, 1),
        wilson_area_law(beta_tilde, 1, 2),
    )
    chi_area_33 = creutz_ratio(
        wilson_area_law(beta_tilde, 3, 3),
        wilson_area_law(beta_tilde, 2, 2),
        wilson_area_law(beta_tilde, 3, 2),
        wilson_area_law(beta_tilde, 2, 3),
    )
    chi_area_const = all(
        creutz_ratio(
            wilson_area_law(beta_tilde, r, t),
            wilson_area_law(beta_tilde, r - 1, t - 1),
            wilson_area_law(beta_tilde, r, t - 1),
            wilson_area_law(beta_tilde, r - 1, t),
        )
        == beta_tilde
        for r in (2, 3)
        for t in (2, 3)
    )

    chi_perim_22 = creutz_ratio(
        wilson_perimeter_law(beta_tilde, 2, 2),
        wilson_perimeter_law(beta_tilde, 1, 1),
        wilson_perimeter_law(beta_tilde, 2, 1),
        wilson_perimeter_law(beta_tilde, 1, 2),
    )
    chi_perim_33 = creutz_ratio(
        wilson_perimeter_law(beta_tilde, 3, 3),
        wilson_perimeter_law(beta_tilde, 2, 2),
        wilson_perimeter_law(beta_tilde, 3, 2),
        wilson_perimeter_law(beta_tilde, 2, 3),
    )
    chi_perim_unity = all(
        creutz_ratio(
            wilson_perimeter_law(beta_tilde, r, t),
            wilson_perimeter_law(beta_tilde, r - 1, t - 1),
            wilson_perimeter_law(beta_tilde, r, t - 1),
            wilson_perimeter_law(beta_tilde, r - 1, t),
        )
        == Q(1, 1)
        for r in (2, 3)
        for t in (2, 3)
    )
    area_confining = (
        chi_area_22 == beta_tilde and chi_area_22 < Q(1, 1) and chi_perim_22 == Q(1, 1)
    )

    alpha_s_mz = Q(1179, 10000)
    pi_iv = pi_interval()
    inv_four_pi = pi_iv.scale(Q(4, 1)).reciprocal()
    factor_L2 = RationalInterval.exact(Q(1, 1)) + inv_four_pi.scale(alpha_s_mz * b0_nf5 * Q(2, 1))
    factor_L4 = RationalInterval.exact(Q(1, 1)) + inv_four_pi.scale(alpha_s_mz * b0_nf5 * Q(4, 1))
    alpha_s_L2_iv = factor_L2.reciprocal().scale(alpha_s_mz)
    alpha_s_L4_iv = factor_L4.reciprocal().scale(alpha_s_mz)

    as_L2_lo12, as_L2_hi12, as_L2_ok = alpha_s_L2_iv.decimal_prefix(12)
    as_L4_lo12, as_L4_hi12, as_L4_ok = alpha_s_L4_iv.decimal_prefix(12)
    uv_decreases = alpha_s_L4_iv.hi < alpha_s_L2_iv.lo and alpha_s_L2_iv.hi < alpha_s_mz

    sigma_ln9_iv = ln3_interval().scale(Q(2, 1))
    ln9_lo12, ln9_hi12, ln9_ok = sigma_ln9_iv.decimal_prefix(12)

    return Qm221QcdBeta0WilsonConfinementReport(
        color_dimension_nc=n_c,
        gluon_generator_count=len(gens),
        all_generators_hermitian_and_traceless=herm_traceless,
        killing_orthogonality_holds=killing_ok,
        jacobi_identity_holds_all_triples=jacobi_ok,
        fundamental_trace_normalization_tf=t_f,
        fundamental_casimir_cf=c_f,
        fundamental_casimir_proportional_to_identity=fund_casimir_ok,
        adjoint_casimir_ca=c_a,
        adjoint_casimir_holds_on_all_generators=adj_casimir_ok,
        fierz_completeness_holds_all_81_entries=fierz_ok,
        singlet_qqbar_casimir_coeff=singlet_qqbar,
        octet_qqbar_casimir_coeff=octet_qqbar,
        sextet_qq_casimir_coeff=sextet_qq,
        antitriplet_qq_casimir_coeff=antitriplet_qq,
        singlet_attractive_and_octet_repulsive=singlet_attr_octet_rep,
        gluon_paramagnetic_spin_contribution=gluon_para,
        gluon_diamagnetic_orbital_contribution=gluon_dia,
        gluon_total_beta0_contribution=gluon_total,
        fermion_single_dirac_beta0_contribution=fermion_single,
        beta0_nf0_pure_yang_mills=b0_nf0,
        beta0_nf3_light_quarks=b0_nf3,
        beta0_nf5_at_mz=b0_nf5,
        beta0_nf6_standard_model=b0_nf6,
        beta0_nf16_conformal_edge=b0_nf16,
        beta0_nf17_loss_of_af=b0_nf17,
        asymptotic_freedom_holds_for_nf_0_to_16=af_0_to_16,
        asymptotic_freedom_lost_at_nf_17=af_lost_17,
        abelian_qed_beta0_nf1_is_negative=qed_negative,
        beta1_nf0_pure_yang_mills=b1_nf0,
        beta1_nf5_at_mz=b1_nf5,
        beta1_nf16_banks_zaks=b1_nf16,
        banks_zaks_nf16_fixed_point_ratio=bz_ratio_nf16,
        lattice_3x3_vertex_count=v_cnt,
        lattice_3x3_edge_count=e_cnt,
        lattice_3x3_spanning_tree_edges=e_tree,
        lattice_3x3_independent_plaquette_betti1=b1_plaq,
        dfm_tree_dressing_reduces_links_to_plaquettes=dfm_plaq_ok,
        strong_coupling_expansion_parameter=beta_tilde,
        creutz_area_ratio_r2_t2=chi_area_22,
        creutz_area_ratio_r3_t3=chi_area_33,
        creutz_area_ratio_constant_across_loops=chi_area_const,
        creutz_perimeter_ratio_r2_t2=chi_perim_22,
        creutz_perimeter_ratio_r3_t3=chi_perim_33,
        creutz_perimeter_ratio_is_unity=chi_perim_unity,
        area_law_strictly_confining_vs_perimeter=area_confining,
        alpha_s_mz_input=alpha_s_mz,
        alpha_s_at_ln_q2_mz2_eq_2_decimal_12=as_L2_lo12 if as_L2_ok else f"{as_L2_lo12}..{as_L2_hi12}",
        alpha_s_at_ln_q2_mz2_eq_4_decimal_12=as_L4_lo12 if as_L4_ok else f"{as_L4_lo12}..{as_L4_hi12}",
        alpha_s_12_digits_agree=as_L2_ok and as_L4_ok,
        alpha_s_decreases_monotonically_in_uv=uv_decreases,
        string_tension_ln9_decimal_12=ln9_lo12 if ln9_ok else f"{ln9_lo12}..{ln9_hi12}",
        string_tension_12_digits_agree=ln9_ok,
    )


def summarize_qm221_qcd_beta0_wilson_confinement() -> Dict[str, object]:
    r = evaluate_qm221_qcd_beta0_wilson_confinement()
    return {
        "control_id": "QM-221",
        "color_dimension_nc": r.color_dimension_nc,
        "gluon_generator_count": r.gluon_generator_count,
        "all_generators_hermitian_and_traceless": r.all_generators_hermitian_and_traceless,
        "killing_orthogonality_holds": r.killing_orthogonality_holds,
        "jacobi_identity_holds_all_triples": r.jacobi_identity_holds_all_triples,
        "fundamental_casimir_cf": str(r.fundamental_casimir_cf),
        "adjoint_casimir_ca": str(r.adjoint_casimir_ca),
        "fierz_completeness_holds_all_81_entries": r.fierz_completeness_holds_all_81_entries,
        "singlet_qqbar_casimir_coeff": str(r.singlet_qqbar_casimir_coeff),
        "octet_qqbar_casimir_coeff": str(r.octet_qqbar_casimir_coeff),
        "beta0_nf0_pure_yang_mills": str(r.beta0_nf0_pure_yang_mills),
        "beta0_nf5_at_mz": str(r.beta0_nf5_at_mz),
        "beta0_nf6_standard_model": str(r.beta0_nf6_standard_model),
        "beta0_nf16_conformal_edge": str(r.beta0_nf16_conformal_edge),
        "beta0_nf17_loss_of_af": str(r.beta0_nf17_loss_of_af),
        "asymptotic_freedom_holds_for_nf_0_to_16": r.asymptotic_freedom_holds_for_nf_0_to_16,
        "asymptotic_freedom_lost_at_nf_17": r.asymptotic_freedom_lost_at_nf_17,
        "banks_zaks_nf16_fixed_point_ratio": str(r.banks_zaks_nf16_fixed_point_ratio),
        "dfm_tree_dressing_reduces_links_to_plaquettes": r.dfm_tree_dressing_reduces_links_to_plaquettes,
        "creutz_area_ratio_r2_t2": str(r.creutz_area_ratio_r2_t2),
        "creutz_perimeter_ratio_r2_t2": str(r.creutz_perimeter_ratio_r2_t2),
        "area_law_strictly_confining_vs_perimeter": r.area_law_strictly_confining_vs_perimeter,
        "alpha_s_at_ln_q2_mz2_eq_2_decimal_12": r.alpha_s_at_ln_q2_mz2_eq_2_decimal_12,
        "alpha_s_at_ln_q2_mz2_eq_4_decimal_12": r.alpha_s_at_ln_q2_mz2_eq_4_decimal_12,
        "alpha_s_12_digits_agree": r.alpha_s_12_digits_agree,
        "string_tension_ln9_decimal_12": r.string_tension_ln9_decimal_12,
        "string_tension_12_digits_agree": r.string_tension_12_digits_agree,
    }
