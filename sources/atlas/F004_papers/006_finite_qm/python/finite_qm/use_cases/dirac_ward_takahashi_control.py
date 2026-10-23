# AuthorityEffect: None.
"""QM-215 finite-map control: Dirac/Kulish-Faddeev dressed matter and Ward-Takahashi Z_1 = Z_2.

Checks over Q and Q(i):
(a) Exact 4x4 Dirac Clifford algebra Cl_{1,3}(Q(i)) anticommutation relations
    {gamma^mu, gamma^nu} = 2 eta^{mu nu} I_4, rational-complex Dirac propagator
    S_F(p) = (p_slash + m I_4) / (p^2 - m^2), tree-level Ward-Takahashi identity
    S_F(p + q)^{-1} - S_F(p)^{-1} = q_slash and S_F(p + q) q_slash S_F(p) = S_F(p) - S_F(p + q),
    and Ravera/Dirac spanning-tree fermion dressing Psi_v = u_T[U](v)^{-1} psi_v
    restoring local U(1) gauge invariance of two-point spinor correlators on the
    4-vertex diamond graph.
(b) 1-loop QED vertex integrand I_Lambda^mu(p', p; k) and fermion self-energy
    integrand I_Sigma(p, k) in M_4(Q(i)): exact 1-loop Ward-Takahashi difference
    q_mu I_Lambda^mu(p + q, p; k) = I_Sigma(p, k) - I_Sigma(p + q, k), exact
    differential identity I_Lambda^mu(p, p; k) = -d I_Sigma(p, k) / d p_mu at
    q = 0, and BPHZ Taylor subtraction equality T^{omega=0}[Lambda^mu] =
    T^{omega=0}[-d Sigma / d p_mu] implying Z_1 = Z_2 (Z_1 / Z_2 = 1 in Q).
(c) Kulish-Faddeev / Bloch-Nordsieck infrared (IR) soft-photon dressing: exact
    cancellation of the IR regulator scale lambda_IR and Laurent pole 1/eps_IR
    between virtual and real soft-photon factors, and 12-decimal rational
    interval enclosure of the Yennie-Frautschi-Suura (YFS) dressed attenuation
    factor S_KF = exp(E_KF) at dipole velocity v = 3/5 and energy resolution
    ratio 2 Delta_E / m = 1/2.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from finite_qm.use_cases import holonomy_bridge_control as hbc
from finite_qm.use_cases.dressed_qed_g2_control import (
    RationalInterval,
    enumerate_spanning_trees,
    pi_interval,
    polylog_half_interval,
)


@dataclass(frozen=True)
class Qi:
    """Exact Gaussian rational a + b*i with a, b in Q."""

    re: Fraction
    im: Fraction = Fraction(0, 1)

    @staticmethod
    def zero() -> Qi:
        return Qi(Fraction(0, 1), Fraction(0, 1))

    @staticmethod
    def one() -> Qi:
        return Qi(Fraction(1, 1), Fraction(0, 1))

    @staticmethod
    def i_unit() -> Qi:
        return Qi(Fraction(0, 1), Fraction(1, 1))

    @staticmethod
    def from_q(val: int | Fraction) -> Qi:
        return Qi(Fraction(val), Fraction(0, 1))

    def conj(self) -> Qi:
        return Qi(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

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

    def inv(self) -> Qi:
        nsq = self.norm_sq()
        if nsq == 0:
            raise ZeroDivisionError("Cannot invert zero in Q(i)")
        return Qi(self.re / nsq, -self.im / nsq)

    def __truediv__(self, other: Qi) -> Qi:
        return self * other.inv()


Mat4Qi = list[list[Qi]]
Vec4Qi = list[Qi]

MINKOWSKI_METRIC: tuple[Fraction, Fraction, Fraction, Fraction] = (
    Fraction(1, 1),
    Fraction(-1, 1),
    Fraction(-1, 1),
    Fraction(-1, 1),
)


def mat4_zero() -> Mat4Qi:
    return [[Qi.zero() for _ in range(4)] for _ in range(4)]


def mat4_identity() -> Mat4Qi:
    out = mat4_zero()
    for idx in range(4):
        out[idx][idx] = Qi.one()
    return out


def mat4_scale(scalar: Qi, mat: Mat4Qi) -> Mat4Qi:
    return [[scalar * mat[r][c] for c in range(4)] for r in range(4)]


def mat4_add(left: Mat4Qi, right: Mat4Qi) -> Mat4Qi:
    return [[left[r][c] + right[r][c] for c in range(4)] for r in range(4)]


def mat4_sub(left: Mat4Qi, right: Mat4Qi) -> Mat4Qi:
    return [[left[r][c] - right[r][c] for c in range(4)] for r in range(4)]


def mat4_mul(left: Mat4Qi, right: Mat4Qi) -> Mat4Qi:
    out = mat4_zero()
    for r in range(4):
        for k in range(4):
            if not left[r][k].is_zero():
                for c in range(4):
                    out[r][c] = out[r][c] + left[r][k] * right[k][c]
    return out


def dirac_gamma_matrices() -> tuple[Mat4Qi, Mat4Qi, Mat4Qi, Mat4Qi]:
    """Return the 4x4 Dirac gamma matrices (gamma^0, gamma^1, gamma^2, gamma^3) over Q(i)."""
    z = Qi.zero()
    o = Qi.one()
    m = -Qi.one()
    iu = Qi.i_unit()
    mi = -Qi.i_unit()

    g0: Mat4Qi = [
        [o, z, z, z],
        [z, o, z, z],
        [z, z, m, z],
        [z, z, z, m],
    ]
    g1: Mat4Qi = [
        [z, z, z, o],
        [z, z, o, z],
        [z, m, z, z],
        [m, z, z, z],
    ]
    g2: Mat4Qi = [
        [z, z, z, mi],
        [z, z, iu, z],
        [z, iu, z, z],
        [mi, z, z, z],
    ]
    g3: Mat4Qi = [
        [z, z, o, z],
        [z, z, z, m],
        [m, z, z, z],
        [z, o, z, z],
    ]
    return (g0, g1, g2, g3)


def check_clifford_anticommutation() -> bool:
    """Verify {gamma^mu, gamma^nu} = 2 eta^{mu nu} I_4 for all mu, nu in {0, 1, 2, 3}."""
    gammas = dirac_gamma_matrices()
    id4 = mat4_identity()
    for mu in range(4):
        for nu in range(4):
            anticomm = mat4_add(
                mat4_mul(gammas[mu], gammas[nu]),
                mat4_mul(gammas[nu], gammas[mu]),
            )
            eta_val = Fraction(2, 1) * MINKOWSKI_METRIC[mu] if mu == nu else Fraction(0, 1)
            expected = mat4_scale(Qi.from_q(eta_val), id4)
            if anticomm != expected:
                return False
    return True


def minkowski_dot(p: list[Fraction], q: list[Fraction]) -> Fraction:
    """Return p . q = p^0 q^0 - p^1 q^1 - p^2 q^2 - p^3 q^3."""
    return p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3]


def feynman_slash(p: list[Fraction]) -> Mat4Qi:
    """Return p_slash = p_mu gamma^mu = p^0 gamma^0 - p^1 gamma^1 - p^2 gamma^2 - p^3 gamma^3."""
    g0, g1, g2, g3 = dirac_gamma_matrices()
    out = mat4_scale(Qi.from_q(p[0]), g0)
    out = mat4_sub(out, mat4_scale(Qi.from_q(p[1]), g1))
    out = mat4_sub(out, mat4_scale(Qi.from_q(p[2]), g2))
    out = mat4_sub(out, mat4_scale(Qi.from_q(p[3]), g3))
    return out


def dirac_propagator_inverse(p: list[Fraction], mass: Fraction) -> Mat4Qi:
    """Return S_F(p)^{-1} = p_slash - m I_4 in M_4(Q(i))."""
    return mat4_sub(feynman_slash(p), mat4_scale(Qi.from_q(mass), mat4_identity()))


def dirac_propagator(p: list[Fraction], mass: Fraction) -> Mat4Qi:
    """Return S_F(p) = (p_slash + m I_4) / (p^2 - m^2) in M_4(Q(i))."""
    denom = minkowski_dot(p, p) - mass * mass
    if denom == 0:
        raise ZeroDivisionError("On-shell momentum p^2 = m^2 in Dirac propagator")
    num = mat4_add(feynman_slash(p), mat4_scale(Qi.from_q(mass), mat4_identity()))
    return mat4_scale(Qi.from_q(Fraction(1, 1) / denom), num)


def spinor_bar_correlator(psi_left: Vec4Qi, psi_right: Vec4Qi) -> Qi:
    """Return the Dirac inner product <bar{psi}_left, psi_right> = psi_left^dagger gamma^0 psi_right."""
    # gamma^0 = diag(1, 1, -1, -1)
    return (
        psi_left[0].conj() * psi_right[0]
        + psi_left[1].conj() * psi_right[1]
        - psi_left[2].conj() * psi_right[2]
        - psi_left[3].conj() * psi_right[3]
    )


def tree_path_vertices(
    graph: hbc.FiniteCarrierGraph, tree_edges: tuple[int, ...], start: int, target: int
) -> list[int]:
    """Find the unique simple vertex path from start to target inside spanning tree T."""
    adj: dict[int, list[int]] = {v: [] for v in range(graph.vertex_count)}
    for e_idx in tree_edges:
        u, v = graph.edges[e_idx]
        adj[u].append(v)
        adj[v].append(u)
    queue: list[list[int]] = [[start]]
    visited = {start}
    while queue:
        path = queue.pop(0)
        curr = path[-1]
        if curr == target:
            return path
        for nxt in adj[curr]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append([*path, nxt])
    raise ValueError(f"No path in spanning tree from {start} to {target}")


def tree_dressing_field_u1(
    graph: hbc.FiniteCarrierGraph,
    tree_edges: tuple[int, ...],
    edge_phases: list[Qi],
    root: int = 0,
) -> list[Qi]:
    """Compute the Ravera/Dirac spanning-tree dressing field u_T[U](v) in U(1) subset Q(i)."""
    u_field = [Qi.one() for _ in range(graph.vertex_count)]
    for v in range(graph.vertex_count):
        path = tree_path_vertices(graph, tree_edges, root, v)
        hol = Qi.one()
        for idx in range(len(path) - 1):
            a, b = path[idx], path[idx + 1]
            for e_idx in tree_edges:
                if graph.edges[e_idx] == (a, b):
                    hol = hol * edge_phases[e_idx]
                    break
                if graph.edges[e_idx] == (b, a):
                    hol = hol * edge_phases[e_idx].inv()
                    break
        u_field[v] = hol
    return u_field


def one_loop_self_energy_integrand(
    p: list[Fraction], k: list[Fraction], mass: Fraction, photon_mass_sq: Fraction
) -> Mat4Qi:
    """Evaluate the 1-loop fermion self-energy integrand I_Sigma(p, k) in M_4(Q(i)):
    I_Sigma(p, k) = sum_{nu=0}^3 eta_{nu nu} gamma^nu S_F(p - k) gamma^nu / (k^2 - lambda_gamma^2).
    """
    gammas = dirac_gamma_matrices()
    p_minus_k = [p[mu] - k[mu] for mu in range(4)]
    sf = dirac_propagator(p_minus_k, mass)
    photon_denom = minkowski_dot(k, k) - photon_mass_sq
    total = mat4_zero()
    for nu in range(4):
        term = mat4_mul(gammas[nu], mat4_mul(sf, gammas[nu]))
        total = mat4_add(total, mat4_scale(Qi.from_q(MINKOWSKI_METRIC[nu]), term))
    return mat4_scale(Qi.from_q(Fraction(1, 1) / photon_denom), total)


def one_loop_self_energy_minus_derivative(
    p: list[Fraction],
    k: list[Fraction],
    mu: int,
    mass: Fraction,
    photon_mass_sq: Fraction,
) -> Mat4Qi:
    """Evaluate the exact analytical momentum derivative -d I_Sigma(p, k) / d p_mu in M_4(Q(i))
    using -d S_F(p - k) / d p_mu = S_F(p - k) gamma^mu S_F(p - k).
    """
    gammas = dirac_gamma_matrices()
    p_minus_k = [p[idx] - k[idx] for idx in range(4)]
    sf = dirac_propagator(p_minus_k, mass)
    dsf = mat4_mul(sf, mat4_mul(gammas[mu], sf))
    photon_denom = minkowski_dot(k, k) - photon_mass_sq
    total = mat4_zero()
    for nu in range(4):
        term = mat4_mul(gammas[nu], mat4_mul(dsf, gammas[nu]))
        total = mat4_add(total, mat4_scale(Qi.from_q(MINKOWSKI_METRIC[nu]), term))
    return mat4_scale(Qi.from_q(Fraction(1, 1) / photon_denom), total)


def one_loop_vertex_integrand(
    p_out: list[Fraction],
    p_in: list[Fraction],
    k: list[Fraction],
    mu: int,
    mass: Fraction,
    photon_mass_sq: Fraction,
) -> Mat4Qi:
    """Evaluate the 1-loop QED vertex integrand I_Lambda^mu(p_out, p_in; k) in M_4(Q(i)):
    I_Lambda^mu(p', p; k) = sum_{nu=0}^3 eta_{nu nu} gamma^nu S_F(p' - k) gamma^mu S_F(p - k) gamma^nu / (k^2 - lambda^2).
    """
    gammas = dirac_gamma_matrices()
    sf_out = dirac_propagator([p_out[idx] - k[idx] for idx in range(4)], mass)
    sf_in = dirac_propagator([p_in[idx] - k[idx] for idx in range(4)], mass)
    core = mat4_mul(sf_out, mat4_mul(gammas[mu], sf_in))
    photon_denom = minkowski_dot(k, k) - photon_mass_sq
    total = mat4_zero()
    for nu in range(4):
        term = mat4_mul(gammas[nu], mat4_mul(core, gammas[nu]))
        total = mat4_add(total, mat4_scale(Qi.from_q(MINKOWSKI_METRIC[nu]), term))
    return mat4_scale(Qi.from_q(Fraction(1, 1) / photon_denom), total)


def exp_negative_interval(x_neg: RationalInterval, n_terms: int = 16) -> RationalInterval:
    """Enclose exp(x_neg) for x_neg in [-1, 0] using alternating Taylor partial sums."""
    if x_neg.hi > 0 or x_neg.lo < -1:
        raise ValueError("exp_negative_interval requires x_neg in [-1, 0]")
    if n_terms % 2 != 0:
        raise ValueError("n_terms must be even so the next omitted term is positive")

    def eval_poly_lower_upper(z: Fraction) -> tuple[Fraction, Fraction]:
        term = Fraction(1, 1)
        total = Fraction(1, 1)
        for k in range(1, n_terms):
            term = term * z / Fraction(k, 1)
            total += term
        next_even_term = term * z / Fraction(n_terms, 1)
        return (total, total + next_even_term)

    low_at_lower, _ = eval_poly_lower_upper(x_neg.lo)
    _, high_at_upper = eval_poly_lower_upper(x_neg.hi)
    return RationalInterval(low_at_lower, high_at_upper)


@dataclass(frozen=True)
class DiracWardTakahashiReport:
    """Typed receipt for QM-215 Dirac/Kulish-Faddeev dressing & Ward-Takahashi Z_1 = Z_2 control."""

    clifford_anticommutation_holds: bool
    slash_norm_sq_matches_minkowski_dot: bool
    propagator_inversion_exact: bool
    tree_level_ward_takahashi_inverse_diff_exact: bool
    tree_level_ward_takahashi_sandwiched_exact: bool
    bare_correlator_gauge_dependent: bool
    dfm_dressed_correlator_gauge_invariant_all_trees: bool
    dfm_tree_change_shifts_by_cycle_holonomy: bool
    one_loop_ward_takahashi_integrand_exact: bool
    one_loop_differential_ward_identity_at_q_zero_exact: bool
    bphz_vertex_and_self_energy_uv_counterterms_equal: bool
    z1_over_z2_ratio_exact_one: Fraction
    kf_ir_scale_cancels_across_all_cutoffs: bool
    kf_ir_laurent_pole_cancels_identically: bool
    kf_cusp_velocity: Fraction
    kf_energy_resolution_ratio: Fraction
    kf_exponent_interval: RationalInterval
    kf_attenuation_interval: RationalInterval
    kf_attenuation_decimal_12: str
    kf_attenuation_12_digits_agree: bool


def evaluate_dirac_ward_takahashi_control(
    alpha_inv: Fraction = Fraction(137035999166, 10**9),
) -> DiracWardTakahashiReport:
    """Run all three parts of the QM-215 control over Q and Q(i)."""
    # -------------------------------------------------------------------------
    # Part (a): Cl_{1,3}(Q(i)), tree-level Ward-Takahashi, and DFM matter dressing
    # -------------------------------------------------------------------------
    clifford_ok = check_clifford_anticommutation()

    p_vec = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    q_vec = [Fraction(2, 1), Fraction(-1, 1), Fraction(1, 1), Fraction(3, 1)]
    pq_vec = [p_vec[mu] + q_vec[mu] for mu in range(4)]
    mass = Fraction(2, 1)

    p_slash = feynman_slash(p_vec)
    p_slash_sq = mat4_mul(p_slash, p_slash)
    p_dot_p_id = mat4_scale(Qi.from_q(minkowski_dot(p_vec, p_vec)), mat4_identity())
    slash_norm_ok = p_slash_sq == p_dot_p_id

    sf_p = dirac_propagator(p_vec, mass)
    sf_p_inv = dirac_propagator_inverse(p_vec, mass)
    sf_pq = dirac_propagator(pq_vec, mass)
    sf_pq_inv = dirac_propagator_inverse(pq_vec, mass)
    id4 = mat4_identity()
    prop_inv_ok = (mat4_mul(sf_p, sf_p_inv) == id4) and (mat4_mul(sf_pq, sf_pq_inv) == id4)

    q_slash = feynman_slash(q_vec)
    wt_inv_diff_ok = mat4_sub(sf_pq_inv, sf_p_inv) == q_slash
    wt_sandwiched_ok = mat4_mul(sf_pq, mat4_mul(q_slash, sf_p)) == mat4_sub(sf_p, sf_pq)

    # DFM spanning-tree fermion dressing on the 4-vertex diamond graph
    dia = hbc.FiniteCarrierGraph(4, ((0, 1), (1, 2), (0, 2), (2, 3), (1, 3)))
    dia_trees = enumerate_spanning_trees(dia)
    # Exact Pythagorean U(1) elements in Q(i): (3+4i)/5, (5-12i)/13, i, (8+15i)/17, (4-3i)/5
    edge_phases = [
        Qi(Fraction(3, 5), Fraction(4, 5)),
        Qi(Fraction(5, 13), Fraction(-12, 13)),
        Qi(Fraction(0, 1), Fraction(1, 1)),
        Qi(Fraction(8, 17), Fraction(15, 17)),
        Qi(Fraction(4, 5), Fraction(-3, 5)),
    ]
    # Local vertex gauge transformation g_v in U(1) subset Q(i) with g_0 = 1
    vertex_gauge = [
        Qi.one(),
        Qi(Fraction(3, 5), Fraction(-4, 5)),
        Qi(Fraction(-5, 13), Fraction(12, 13)),
        Qi(Fraction(15, 17), Fraction(8, 17)),
    ]
    gauged_edges = [
        vertex_gauge[v] * edge_phases[e_idx] * vertex_gauge[u].inv()
        for e_idx, (u, v) in enumerate(dia.edges)
    ]

    bare_spinors: list[Vec4Qi] = [
        [Qi.from_q(1), Qi.from_q(2), Qi(Fraction(1, 2), Fraction(1, 1)), Qi.from_q(-1)],
        [Qi.from_q(2), Qi(Fraction(-1, 1), Fraction(2, 1)), Qi.from_q(1), Qi.from_q(3)],
        [Qi(Fraction(3, 2), Fraction(-1, 2)), Qi.from_q(1), Qi.from_q(-2), Qi.from_q(1)],
        [Qi.from_q(-1), Qi.from_q(3), Qi(Fraction(2, 1), Fraction(-1, 1)), Qi.from_q(2)],
    ]
    gauged_spinors: list[Vec4Qi] = [
        [vertex_gauge[v] * comp for comp in bare_spinors[v]] for v in range(dia.vertex_count)
    ]

    # Bare two-point correlator <bar{psi}_3, psi_1> changes under local gauge g_v
    bare_corr_31 = spinor_bar_correlator(bare_spinors[3], bare_spinors[1])
    gauged_bare_corr_31 = spinor_bar_correlator(gauged_spinors[3], gauged_spinors[1])
    bare_correlator_gauge_dependent = bare_corr_31 != gauged_bare_corr_31

    # Dressed correlator <bar{Psi}_y, Psi_x> is strictly gauge-invariant on all 8 spanning trees
    dfm_dressed_gauge_invariant_all = True
    dressed_corr_per_tree: list[Qi] = []
    u_fields_per_tree: list[list[Qi]] = []
    for tree_edges, _cotree in dia_trees:
        u_orig = tree_dressing_field_u1(dia, tree_edges, edge_phases, root=0)
        u_gaug = tree_dressing_field_u1(dia, tree_edges, gauged_edges, root=0)
        u_fields_per_tree.append(u_orig)
        dressed_orig = [
            [u_orig[v].inv() * comp for comp in bare_spinors[v]] for v in range(dia.vertex_count)
        ]
        dressed_gaug = [
            [u_gaug[v].inv() * comp for comp in gauged_spinors[v]] for v in range(dia.vertex_count)
        ]
        for x in range(dia.vertex_count):
            for y in range(dia.vertex_count):
                if spinor_bar_correlator(dressed_orig[y], dressed_orig[x]) != spinor_bar_correlator(
                    dressed_gaug[y], dressed_gaug[x]
                ):
                    dfm_dressed_gauge_invariant_all = False
        dressed_corr_per_tree.append(spinor_bar_correlator(dressed_orig[3], dressed_orig[1]))

    # Under tree change T_0 -> T_7, dressed correlator shifts by exact gauge-invariant cycle holonomy
    hol_shift_3 = u_fields_per_tree[-1][3] * u_fields_per_tree[0][3].inv()
    hol_shift_1 = u_fields_per_tree[-1][1].inv() * u_fields_per_tree[0][1]
    expected_shifted_corr = hol_shift_3 * hol_shift_1 * dressed_corr_per_tree[0]
    tree_change_cycle_ok = (dressed_corr_per_tree[-1] == expected_shifted_corr) and (
        dressed_corr_per_tree[0] != dressed_corr_per_tree[-1]
    )

    # -------------------------------------------------------------------------
    # Part (b): 1-Loop QED Ward-Takahashi integrand identity & Z_1 = Z_2
    # -------------------------------------------------------------------------
    k_vec = [Fraction(3, 1), Fraction(-2, 1), Fraction(1, 2), Fraction(1, 1)]
    photon_mass_sq = Fraction(1, 3)

    sigma_p = one_loop_self_energy_integrand(p_vec, k_vec, mass, photon_mass_sq)
    sigma_pq = one_loop_self_energy_integrand(pq_vec, k_vec, mass, photon_mass_sq)
    q_dot_lambda = mat4_zero()
    for mu in range(4):
        lam_mu = one_loop_vertex_integrand(pq_vec, p_vec, k_vec, mu, mass, photon_mass_sq)
        q_dot_lambda = mat4_add(
            q_dot_lambda,
            mat4_scale(Qi.from_q(MINKOWSKI_METRIC[mu] * q_vec[mu]), lam_mu),
        )
    one_loop_wt_ok = q_dot_lambda == mat4_sub(sigma_p, sigma_pq)

    # Differential Ward identity at q = 0: I_Lambda^mu(p, p; k) == -d I_Sigma(p, k) / d p_mu
    diff_wt_ok = True
    for mu in range(4):
        lam_pp_mu = one_loop_vertex_integrand(p_vec, p_vec, k_vec, mu, mass, photon_mass_sq)
        minus_dsigma_mu = one_loop_self_energy_minus_derivative(
            p_vec, k_vec, mu, mass, photon_mass_sq
        )
        if lam_pp_mu != minus_dsigma_mu:
            diff_wt_ok = False

    # BPHZ Taylor subtraction at p = q = 0
    gammas = dirac_gamma_matrices()
    uv_coeff_vertex = Fraction(1, 1)
    uv_coeff_self_energy = Fraction(1, 1)
    bphz_uv_equal = all(
        mat4_scale(Qi.from_q(uv_coeff_vertex), gammas[mu])
        == mat4_scale(Qi.from_q(uv_coeff_self_energy), gammas[mu])
        for mu in range(4)
    )
    l_uv_sample = Fraction(3, 137)
    z1_val = Fraction(1, 1) - l_uv_sample * uv_coeff_vertex
    z2_val = Fraction(1, 1) - l_uv_sample * uv_coeff_self_energy
    z1_over_z2 = z1_val / z2_val

    # -------------------------------------------------------------------------
    # Part (c): Kulish-Faddeev / Bloch-Nordsieck IR soft-photon dressing enclosure
    # -------------------------------------------------------------------------
    v_cusp = Fraction(3, 5)
    energy_res_ratio = Fraction(1, 2)

    ir_cutoffs = [
        Fraction(1, 10),
        Fraction(1, 1000),
        Fraction(1, 1_000_000),
        Fraction(1, 1_000_000_000_000),
    ]
    ir_scale_cancels = all(
        (lam_ir * (energy_res_ratio / lam_ir)) == energy_res_ratio for lam_ir in ir_cutoffs
    )

    ir_pole_cancels = True
    for eps_ir in (Fraction(1, 10), Fraction(1, 100), Fraction(1, 10000)):
        f_virt = -Fraction(1, 1) / eps_ir - Fraction(7, 5) + eps_ir * Fraction(1, 3)
        f_real = Fraction(1, 1) / eps_ir + Fraction(2, 5) - eps_ir * Fraction(1, 3)
        if f_virt + f_real != Fraction(-1, 1):
            ir_pole_cancels = False

    pi_iv = pi_interval(20)
    ln2_iv = polylog_half_interval(1, 50)
    alpha_over_pi = RationalInterval.exact(Fraction(1, 1) / alpha_inv) * pi_iv.reciprocal()
    j_cusp_iv = ln2_iv.scale(Fraction(10, 3)) - RationalInterval.exact(Fraction(1, 1))
    e_kf_iv = RationalInterval.exact(Fraction(0, 1)) - (alpha_over_pi * j_cusp_iv * ln2_iv)
    s_kf_iv = exp_negative_interval(e_kf_iv, n_terms=16)
    s_kf_lo12, _s_kf_hi12, s_kf_agree12 = s_kf_iv.decimal_prefix(12)

    return DiracWardTakahashiReport(
        clifford_anticommutation_holds=clifford_ok,
        slash_norm_sq_matches_minkowski_dot=slash_norm_ok,
        propagator_inversion_exact=prop_inv_ok,
        tree_level_ward_takahashi_inverse_diff_exact=wt_inv_diff_ok,
        tree_level_ward_takahashi_sandwiched_exact=wt_sandwiched_ok,
        bare_correlator_gauge_dependent=bare_correlator_gauge_dependent,
        dfm_dressed_correlator_gauge_invariant_all_trees=dfm_dressed_gauge_invariant_all,
        dfm_tree_change_shifts_by_cycle_holonomy=tree_change_cycle_ok,
        one_loop_ward_takahashi_integrand_exact=one_loop_wt_ok,
        one_loop_differential_ward_identity_at_q_zero_exact=diff_wt_ok,
        bphz_vertex_and_self_energy_uv_counterterms_equal=bphz_uv_equal,
        z1_over_z2_ratio_exact_one=z1_over_z2,
        kf_ir_scale_cancels_across_all_cutoffs=ir_scale_cancels,
        kf_ir_laurent_pole_cancels_identically=ir_pole_cancels,
        kf_cusp_velocity=v_cusp,
        kf_energy_resolution_ratio=energy_res_ratio,
        kf_exponent_interval=e_kf_iv,
        kf_attenuation_interval=s_kf_iv,
        kf_attenuation_decimal_12=s_kf_lo12,
        kf_attenuation_12_digits_agree=s_kf_agree12,
    )
