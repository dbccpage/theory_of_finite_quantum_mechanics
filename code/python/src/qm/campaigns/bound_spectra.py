# AuthorityEffect: None.
"""QM-217 Finite-Map Control: Algebraic Bound-State Spectra (su(2) Kravchuk & so(4) Hydrogen).

Establishes over Q and certified RationalInterval enclosures that:
  (a) On the (2j + 1)-dimensional irreducible representation V_j of sl(2, Q) for
      N = 2j in {1, 2, 3, 4}, the rational generators (J_z, J_+, J_-) satisfy exact
      sl(2) commutation relations, Casimir identity C_2 = j(j+1) I, G-metric adjointness
      J_+^T G = G J_- for G = diag(binom(2j, n)^{-1}), equidistant oscillator spectrum
      H_osc = J_z + (j + 1/2) I = diag(1/2, 3/2, ..., 2j + 1/2), ground-state
      Robertson-Schrodinger uncertainty saturation <Q^2>_0 <P^2>_0 = 1/16, and exact
      discrete Kravchuk polynomial binomial orthogonality and difference eigenvalue
      identities without differential equations;
  (b) On the 3D Hydrogen shell carrier H_n = V_j (x) V_j (n = 2j + 1 in {1, 2, 3, 4},
      dim H_n = n^2 in {1, 4, 9, 16}) of Pauli's so(4) ~= su(2)_A (+) su(2)_B algebra,
      the orbital angular momentum L = A + B and Runge-Lenz vector K = A - B satisfy
      exact Pauli orthogonality L . K = 0, so(4) Casimir C_2(so(4)) = L^2 + K^2 = (n^2 - 1) I,
      exact rational Balmer-Rydberg spectrum E_n / E_Ryd = -(C_2(so(4)) + I)^{-1} = -1/n^2,
      and Clebsch-Gordan orbital trace sum tr(L^2) = sum_{l=0}^{n-1}(2l+1)l(l+1) = n^2(n^2-1)/2;
  (c) On the n = 2 shell H_2 (dim = 4), the exact rational projectors Pi_{2S} = I_4 - L^2 / 2
      (rank 1, l = 0, K^2 = 3) and Pi_{2P} = L^2 / 2 (rank 3, l = 1, K^2 = 1) show that
      Dirac fine structure leaves 2S_{1/2} and 2P_{1/2} degenerate at C_FS = -5/128, while
      the short-distance radiative contact perturbation proportional to Pi_{2S} breaks
      Runge-Lenz symmetry ([Pi_{2S}, K_z] != 0), preserves rotational symmetry ([Pi_{2S}, L_a] = 0),
      and encloses both the gross Lyman-alpha (2P -> 1S) transition frequency in THz and
      the 2S_{1/2}-2P_{1/2} radiative contact splitting (91/120)(alpha^5/pi)(m_e c^2/h)
      in MHz to 12 certified decimal places.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb

from .dressed_qed import (
    RationalInterval,
    pi_interval,
)

QMat = list[list[Fraction]]


def q_zeros(rows: int, cols: int) -> QMat:
    """Return a rows x cols zero matrix over Q."""
    return [[Fraction(0, 1) for _ in range(cols)] for _ in range(rows)]


def q_eye(dim: int) -> QMat:
    """Return the dim x dim identity matrix over Q."""
    mat = q_zeros(dim, dim)
    for i in range(dim):
        mat[i][i] = Fraction(1, 1)
    return mat


def q_add(a: QMat, b: QMat) -> QMat:
    """Matrix addition over Q."""
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def q_sub(a: QMat, b: QMat) -> QMat:
    """Matrix subtraction over Q."""
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def q_scale(scalar: Fraction, a: QMat) -> QMat:
    """Scalar multiplication over Q."""
    return [[scalar * a[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def q_mul(a: QMat, b: QMat) -> QMat:
    """Matrix multiplication over Q."""
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    out = q_zeros(rows, cols)
    for i in range(rows):
        for k in range(inner):
            aik = a[i][k]
            if aik != 0:
                for j in range(cols):
                    out[i][j] += aik * b[k][j]
    return out


def q_comm(a: QMat, b: QMat) -> QMat:
    """Commutator [A, B] = A B - B A over Q."""
    return q_sub(q_mul(a, b), q_mul(b, a))


def q_anticomm(a: QMat, b: QMat) -> QMat:
    """Anticommutator {A, B} = A B + B A over Q."""
    return q_add(q_mul(a, b), q_mul(b, a))


def q_transpose(a: QMat) -> QMat:
    """Matrix transpose over Q."""
    rows = len(a)
    cols = len(a[0])
    return [[a[i][j] for i in range(rows)] for j in range(cols)]


def q_trace(a: QMat) -> Fraction:
    """Matrix trace over Q."""
    return sum((a[i][i] for i in range(len(a))), Fraction(0, 1))


def q_kron(a: QMat, b: QMat) -> QMat:
    """Kronecker tensor product A (x) B over Q."""
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out = q_zeros(ra * rb, ca * cb)
    for i in range(ra):
        for j in range(ca):
            aij = a[i][j]
            if aij != 0:
                for k in range(rb):
                    for col_b in range(cb):
                        out[i * rb + k][j * cb + col_b] = aij * b[k][col_b]
    return out


def q_is_zero(a: QMat) -> bool:
    """Check whether a rational matrix is identically zero."""
    return all(entry == 0 for row in a for entry in row)


def sl2_oscillator_generators(twice_j: int) -> tuple[QMat, QMat, QMat, QMat]:
    """Construct rational sl(2, Q) generators (J_z, J_+, J_-) and metric G on V_j (N = 2j).

    Basis states |n> for n = 0, ..., N have weight m = n - j:
      J_z |n> = (n - j) |n>
      J_+ |n> = (N - n) |n + 1>
      J_- |n> = n |n - 1>
    With diagonal metric G_{n,n} = binom(N, n)^{-1}, J_+^T G = G J_- holds over Q.
    """
    if twice_j < 1:
        raise ValueError("twice_j = 2j must be at least 1 for a non-trivial oscillator")
    dim = twice_j + 1
    j_val = Fraction(twice_j, 2)
    jz = q_zeros(dim, dim)
    jp = q_zeros(dim, dim)
    jm = q_zeros(dim, dim)
    g_metric = q_zeros(dim, dim)
    for n in range(dim):
        jz[n][n] = Fraction(n, 1) - j_val
        g_metric[n][n] = Fraction(1, comb(twice_j, n))
        if n + 1 < dim:
            jp[n + 1][n] = Fraction(twice_j - n, 1)
        if n >= 1:
            jm[n - 1][n] = Fraction(n, 1)
    return jz, jp, jm, g_metric


def sl2_casimir_matrix(jz: QMat, jp: QMat, jm: QMat) -> QMat:
    """Compute C_2 = J_z^2 + (J_+ J_- + J_- J_+) / 2 over Q."""
    return q_add(q_mul(jz, jz), q_scale(Fraction(1, 2), q_anticomm(jp, jm)))


def kravchuk_polynomial(k: int, x: int, n_max: int) -> int:
    """Evaluate the discrete Kravchuk polynomial K_k(x; N) = sum_r (-1)^r C(x,r) C(N-x, k-r)."""
    if k < 0 or k > n_max or x < 0 or x > n_max:
        return 0
    total = 0
    for r in range(k + 1):
        term = comb(x, r) * comb(n_max - x, k - r)
        if r % 2 == 1:
            total -= term
        else:
            total += term
    return total


def check_kravchuk_orthogonality_and_difference_eq(n_max: int) -> tuple[bool, bool]:
    """Verify binomial orthogonality and 3-term difference eigenvalue identity for K_k(x; N)."""
    ortho_ok = True
    diff_ok = True
    for k in range(n_max + 1):
        for kp in range(n_max + 1):
            lhs = sum(
                comb(n_max, x) * kravchuk_polynomial(k, x, n_max) * kravchuk_polynomial(kp, x, n_max)
                for x in range(n_max + 1)
            )
            rhs = (1 << n_max) * comb(n_max, k) if k == kp else 0
            if lhs != rhs:
                ortho_ok = False
        for x in range(n_max + 1):
            left_step = (n_max - x) * kravchuk_polynomial(k, x + 1, n_max) if x + 1 <= n_max else 0
            right_step = x * kravchuk_polynomial(k, x - 1, n_max) if x >= 1 else 0
            lhs_diff = left_step - n_max * kravchuk_polynomial(k, x, n_max) + right_step
            rhs_diff = -2 * k * kravchuk_polynomial(k, x, n_max)
            if lhs_diff != rhs_diff:
                diff_ok = False
    return ortho_ok, diff_ok


def sl2_shell_generators(twice_j: int) -> tuple[QMat, QMat, QMat]:
    """Construct rational sl(2, Q) generators for a single chiral factor V_j (twice_j >= 0)."""
    if twice_j < 0:
        raise ValueError("twice_j must be non-negative")
    if twice_j == 0:
        z1 = q_zeros(1, 1)
        return z1, z1, z1
    jz, jp, jm, _ = sl2_oscillator_generators(twice_j)
    return jz, jp, jm


def so4_hydrogen_shell_operators(
    n_principal: int,
) -> dict[str, QMat]:
    """Construct Pauli so(4) ~= su(2)_A (+) su(2)_B operators on H_n = V_j (x) V_j (n = 2j + 1).

    Returns rational n^2 x n^2 matrices for:
      Lz, Lp, Lm (orbital angular momentum L = A + B),
      Kz, Kp, Km (scaled Runge-Lenz vector K = A - B),
      L2 (orbital Casimir L^2),
      K2 (Runge-Lenz square K^2),
      L_dot_K (Pauli orthogonality operator L . K),
      C2_so4 (total Casimir L^2 + K^2).
    """
    if n_principal < 1:
        raise ValueError("Principal quantum number n must be >= 1")
    twice_j = n_principal - 1
    eye_f = q_eye(n_principal)
    jz, jp, jm = sl2_shell_generators(twice_j)

    az = q_kron(jz, eye_f)
    ap = q_kron(jp, eye_f)
    am = q_kron(jm, eye_f)

    bz = q_kron(eye_f, jz)
    bp = q_kron(eye_f, jp)
    bm = q_kron(eye_f, jm)

    lz = q_add(az, bz)
    lp = q_add(ap, bp)
    lm = q_add(am, bm)

    kz = q_sub(az, bz)
    kp = q_sub(ap, bp)
    km = q_sub(am, bm)

    l2 = sl2_casimir_matrix(lz, lp, lm)
    k2 = sl2_casimir_matrix(kz, kp, km)
    l_dot_k = q_add(
        q_mul(lz, kz),
        q_scale(Fraction(1, 2), q_add(q_mul(lp, km), q_mul(lm, kp))),
    )
    c2_so4 = q_add(l2, k2)
    return {
        "Az": az,
        "Bz": bz,
        "Lz": lz,
        "Lp": lp,
        "Lm": lm,
        "Kz": kz,
        "Kp": kp,
        "Km": km,
        "L2": l2,
        "K2": k2,
        "L_dot_K": l_dot_k,
        "C2_so4": c2_so4,
    }


def dirac_fine_structure_coeff(n_principal: int, twice_j_tot: int) -> Fraction:
    """Leading O((Z alpha)^4 m_e c^2) Dirac fine-structure coefficient:

    C_FS(n, j_tot) = -1 / (2 n^3) * (1 / (j_tot + 1/2) - 3 / (4 n)).
    Depends only on (n, j_tot), leaving 2S_{1/2} and 2P_{1/2} exactly degenerate.
    """
    if n_principal < 1 or twice_j_tot < 1 or twice_j_tot % 2 == 0:
        raise ValueError("Require n >= 1 and odd twice_j_tot = 2 j_tot >= 1")
    k_denom = Fraction(twice_j_tot + 1, 2)
    return -Fraction(1, 2 * (n_principal**3)) * (
        Fraction(1, 1) / k_denom - Fraction(3, 4 * n_principal)
    )


@dataclass(frozen=True)
class AlgebraicBoundStateSpectraReport:
    """Typed verification receipt for QM-217 algebraic bound-state spectra control."""

    # Part (a): su(2) Kravchuk finite harmonic oscillator
    kravchuk_sl2_commutators_exact: bool
    kravchuk_casimir_matches_j_j_plus_1: bool
    kravchuk_metric_adjoint_exact: bool
    kravchuk_equidistant_ladder_commutators_exact: bool
    kravchuk_ground_variance_q2: Fraction
    kravchuk_ground_variance_p2: Fraction
    kravchuk_ground_uncertainty_product: Fraction
    kravchuk_ground_saturates_robertson_schrodinger: bool
    kravchuk_polynomial_orthogonality_exact: bool
    kravchuk_difference_eigenvalue_exact: bool

    # Part (b): so(4) Pauli-Runge-Lenz 3D Hydrogen bound-state spectrum
    hydrogen_chiral_factors_commute: bool
    hydrogen_so4_lie_brackets_exact: bool
    hydrogen_pauli_orthogonality_l_dot_k_zero: bool
    hydrogen_asymmetric_control_l_dot_k_nonzero: bool
    hydrogen_casimir_matches_n_squared_minus_1: bool
    hydrogen_balmer_rydberg_energies: tuple[Fraction, ...]
    hydrogen_lyman_alpha_dimensionless_jump: Fraction
    hydrogen_balmer_alpha_dimensionless_jump: Fraction
    hydrogen_orbital_l2_traces: tuple[Fraction, ...]
    hydrogen_orbital_l2_traces_match_clebsch_gordan: bool

    # Part (c): n = 2 (2S_{1/2} vs 2P_{1/2}) degeneracy & QED Lamb-shift lifting
    n2_projectors_idempotent_orthogonal_complete: bool
    n2_2s_rank: Fraction
    n2_2p_rank: Fraction
    n2_pi_2s_commutes_with_so3_l: bool
    n2_pi_2s_breaks_runge_lenz_k: bool
    dirac_fs_2s_half_coeff: Fraction
    dirac_fs_2p_half_coeff: Fraction
    dirac_fs_2p_three_halves_coeff: Fraction
    dirac_fs_2s_2p_half_degenerate: bool
    dirac_fs_fine_structure_splitting_coeff: Fraction
    lyman_alpha_gross_thz_interval: RationalInterval
    lyman_alpha_gross_thz_decimal_12: str
    lyman_alpha_gross_thz_12_digits_agree: bool
    lamb_contact_2s_2p_mhz_interval: RationalInterval
    lamb_contact_2s_2p_mhz_decimal_12: str
    lamb_contact_2s_2p_mhz_12_digits_agree: bool


def evaluate_algebraic_bound_state_spectra_control(
    alpha_inv: Fraction = Fraction(137035999166, 10**9),
    me_c2_over_h_mhz: Fraction = Fraction(123558996383000, 1),
) -> AlgebraicBoundStateSpectraReport:
    """Execute the complete QM-217 algebraic bound-state spectra control."""
    # --- Part (a): su(2) Kravchuk harmonic oscillator across N = 2j in {1, 2, 3, 4} ---
    sl2_comm_ok = True
    casimir_ok = True
    metric_adj_ok = True
    ladder_ok = True
    ground_q2 = Fraction(0, 1)
    ground_p2 = Fraction(0, 1)
    ground_prod = Fraction(0, 1)
    saturates_ok = True
    ortho_all_ok = True
    diff_all_ok = True

    for twice_j in (1, 2, 3, 4):
        dim = twice_j + 1
        j_val = Fraction(twice_j, 2)
        eye = q_eye(dim)
        jz, jp, jm, g_mat = sl2_oscillator_generators(twice_j)

        if (
            q_comm(jz, jp) != jp
            or q_comm(jz, jm) != q_scale(Fraction(-1, 1), jm)
            or q_comm(jp, jm) != q_scale(Fraction(2, 1), jz)
        ):
            sl2_comm_ok = False

        c2 = sl2_casimir_matrix(jz, jp, jm)
        if c2 != q_scale(j_val * (j_val + 1), eye):
            casimir_ok = False

        if q_mul(q_transpose(jp), g_mat) != q_mul(g_mat, jm):
            metric_adj_ok = False

        # Oscillator Hamiltonian H_osc = J_z + (j + 1/2) I = diag(1/2, 3/2, ..., 2j + 1/2)
        h_osc = q_add(jz, q_scale(j_val + Fraction(1, 2), eye))
        expected_diag = [Fraction(2 * n + 1, 2) for n in range(dim)]
        if [h_osc[n][n] for n in range(dim)] != expected_diag:
            ladder_ok = False
        if q_comm(h_osc, jp) != jp or q_comm(h_osc, jm) != q_scale(Fraction(-1, 1), jm):
            ladder_ok = False

        # Ground state |0> quadrature variances for Q^2 = (J_+ + J_-)^2 / (8j), P^2 = -(J_+ - J_-)^2 / (8j)
        jp_plus_jm = q_add(jp, jm)
        jp_minus_jm = q_sub(jp, jm)
        q2_mat = q_scale(Fraction(1, 8) / j_val, q_mul(jp_plus_jm, jp_plus_jm))
        p2_mat = q_scale(Fraction(-1, 8) / j_val, q_mul(jp_minus_jm, jp_minus_jm))
        # Since |0> is an eigenvector of G with G_{0,0} = 1, <0|A|0>_G = A_{0,0}
        q2_0 = q2_mat[0][0]
        p2_0 = p2_mat[0][0]
        # Robertson-Schrodinger bound: (1/4) |<0| J_z / (2j) |0>|^2 = (1/4) * (-j / 2j)^2 = 1/16
        rs_bound = Fraction(1, 4) * (jz[0][0] / (2 * j_val)) ** 2
        if q2_0 != Fraction(1, 4) or p2_0 != Fraction(1, 4) or q2_0 * p2_0 != rs_bound:
            saturates_ok = False
        ground_q2 = q2_0
        ground_p2 = p2_0
        ground_prod = q2_0 * p2_0

        o_ok, d_ok = check_kravchuk_orthogonality_and_difference_eq(twice_j)
        if not o_ok:
            ortho_all_ok = False
        if not d_ok:
            diff_all_ok = False

    # --- Part (b): so(4) Pauli-Runge-Lenz 3D Hydrogen bound-state shells n in {1, 2, 3, 4} ---
    chiral_comm_ok = True
    so4_brackets_ok = True
    pauli_ortho_ok = True
    casimir_so4_ok = True
    energies: list[Fraction] = []
    l2_traces: list[Fraction] = []
    l2_traces_match = True

    for n_prin in (1, 2, 3, 4):
        ops = so4_hydrogen_shell_operators(n_prin)
        dim_shell = n_prin * n_prin
        eye_shell = q_eye(dim_shell)
        lz, lp, lm = ops["Lz"], ops["Lp"], ops["Lm"]
        kz, kp, km = ops["Kz"], ops["Kp"], ops["Km"]
        l2, l_dot_k, c2_so4 = ops["L2"], ops["L_dot_K"], ops["C2_so4"]

        if not q_is_zero(q_comm(ops["Az"], ops["Bz"])):
            chiral_comm_ok = False

        if (
            q_comm(lz, lp) != lp
            or q_comm(lz, lm) != q_scale(Fraction(-1, 1), lm)
            or q_comm(lp, lm) != q_scale(Fraction(2, 1), lz)
            or q_comm(lz, kp) != kp
            or q_comm(kz, lp) != kp
            or q_comm(kp, km) != q_scale(Fraction(2, 1), lz)
        ):
            so4_brackets_ok = False

        if not q_is_zero(l_dot_k):
            pauli_ortho_ok = False

        expected_c2 = Fraction(n_prin * n_prin - 1, 1)
        if c2_so4 != q_scale(expected_c2, eye_shell):
            casimir_so4_ok = False

        energy_n = -Fraction(1, 1) / (expected_c2 + Fraction(1, 1))
        energies.append(energy_n)

        tr_l2 = q_trace(l2)
        l2_traces.append(tr_l2)
        cg_sum = sum(
            Fraction((2 * l_orb + 1) * l_orb * (l_orb + 1), 1)
            for l_orb in range(n_prin)
        )
        if tr_l2 != cg_sum or tr_l2 != Fraction(n_prin * n_prin * (n_prin * n_prin - 1), 2):
            l2_traces_match = False

    # Asymmetric negative control: V_{1/2} (x) V_1 has j_A = 1/2 != j_B = 1 => L . K != 0
    jz_1, jp_1, jm_1 = sl2_shell_generators(1)
    jz_2, jp_2, jm_2 = sl2_shell_generators(2)
    eye_2, eye_3 = q_eye(2), q_eye(3)
    lz_asym = q_add(q_kron(jz_1, eye_3), q_kron(eye_2, jz_2))
    lp_asym = q_add(q_kron(jp_1, eye_3), q_kron(eye_2, jp_2))
    lm_asym = q_add(q_kron(jm_1, eye_3), q_kron(eye_2, jm_2))
    kz_asym = q_sub(q_kron(jz_1, eye_3), q_kron(eye_2, jz_2))
    kp_asym = q_sub(q_kron(jp_1, eye_3), q_kron(eye_2, jp_2))
    km_asym = q_sub(q_kron(jm_1, eye_3), q_kron(eye_2, jm_2))
    l_dot_k_asym = q_add(
        q_mul(lz_asym, kz_asym),
        q_scale(Fraction(1, 2), q_add(q_mul(lp_asym, km_asym), q_mul(lm_asym, kp_asym))),
    )
    asym_nonzero = not q_is_zero(l_dot_k_asym)

    lyman_jump = energies[1] - energies[0]  # -1/4 - (-1) = 3/4
    balmer_jump = energies[2] - energies[1]  # -1/9 - (-1/4) = 5/36

    # --- Part (c): n = 2 (2S_{1/2} vs 2P_{1/2}) projectors & QED Lamb-shift lifting ---
    ops_n2 = so4_hydrogen_shell_operators(2)
    eye_4 = q_eye(4)
    l2_n2 = ops_n2["L2"]
    pi_2p = q_scale(Fraction(1, 2), l2_n2)
    pi_2s = q_sub(eye_4, pi_2p)

    proj_ok = (
        q_mul(pi_2s, pi_2s) == pi_2s
        and q_mul(pi_2p, pi_2p) == pi_2p
        and q_is_zero(q_mul(pi_2s, pi_2p))
        and q_add(pi_2s, pi_2p) == eye_4
    )
    rank_2s = q_trace(pi_2s)
    rank_2p = q_trace(pi_2p)
    comm_so3_ok = (
        q_is_zero(q_comm(pi_2s, ops_n2["Lz"]))
        and q_is_zero(q_comm(pi_2s, ops_n2["Lp"]))
        and q_is_zero(q_comm(pi_2s, ops_n2["Lm"]))
    )
    breaks_rl_ok = not q_is_zero(q_comm(pi_2s, ops_n2["Kz"]))

    fs_2s_half = dirac_fine_structure_coeff(2, 1)
    fs_2p_half = dirac_fine_structure_coeff(2, 1)
    fs_2p_three_halves = dirac_fine_structure_coeff(2, 3)
    fs_deg = fs_2s_half == fs_2p_half == Fraction(-5, 128)
    fs_split = fs_2p_three_halves - fs_2p_half  # -1/128 - (-5/128) = 1/32

    # 12-decimal enclosure of gross Lyman-alpha frequency (3/8) alpha^2 (m_e c^2 / h) in THz
    alpha_exact = RationalInterval.exact(Fraction(1, 1) / alpha_inv)
    me_c2_over_h_thz = me_c2_over_h_mhz / Fraction(10**6, 1)
    lyman_thz_iv = alpha_exact.pow(2).scale(Fraction(3, 8) * me_c2_over_h_thz)
    lyman_dec_12, _lyman_hi_12, lyman_ok = lyman_thz_iv.decimal_prefix(12)

    # 12-decimal enclosure of 2S_{1/2}-2P_{1/2} non-logarithmic radiative contact splitting
    # Delta f_contact = (91/120) * (alpha^5 / pi) * (m_e c^2 / h) in MHz (QM-216 / QM-224 constant)
    pi_iv = pi_interval(20)
    alpha5_over_pi = alpha_exact.pow(5) * pi_iv.reciprocal()
    lamb_contact_iv = alpha5_over_pi.scale(Fraction(91, 120) * me_c2_over_h_mhz)
    lamb_contact_dec_12, _lamb_hi_12, lamb_contact_ok = lamb_contact_iv.decimal_prefix(12)

    return AlgebraicBoundStateSpectraReport(
        kravchuk_sl2_commutators_exact=sl2_comm_ok,
        kravchuk_casimir_matches_j_j_plus_1=casimir_ok,
        kravchuk_metric_adjoint_exact=metric_adj_ok,
        kravchuk_equidistant_ladder_commutators_exact=ladder_ok,
        kravchuk_ground_variance_q2=ground_q2,
        kravchuk_ground_variance_p2=ground_p2,
        kravchuk_ground_uncertainty_product=ground_prod,
        kravchuk_ground_saturates_robertson_schrodinger=saturates_ok,
        kravchuk_polynomial_orthogonality_exact=ortho_all_ok,
        kravchuk_difference_eigenvalue_exact=diff_all_ok,
        hydrogen_chiral_factors_commute=chiral_comm_ok,
        hydrogen_so4_lie_brackets_exact=so4_brackets_ok,
        hydrogen_pauli_orthogonality_l_dot_k_zero=pauli_ortho_ok,
        hydrogen_asymmetric_control_l_dot_k_nonzero=asym_nonzero,
        hydrogen_casimir_matches_n_squared_minus_1=casimir_so4_ok,
        hydrogen_balmer_rydberg_energies=tuple(energies),
        hydrogen_lyman_alpha_dimensionless_jump=lyman_jump,
        hydrogen_balmer_alpha_dimensionless_jump=balmer_jump,
        hydrogen_orbital_l2_traces=tuple(l2_traces),
        hydrogen_orbital_l2_traces_match_clebsch_gordan=l2_traces_match,
        n2_projectors_idempotent_orthogonal_complete=proj_ok,
        n2_2s_rank=rank_2s,
        n2_2p_rank=rank_2p,
        n2_pi_2s_commutes_with_so3_l=comm_so3_ok,
        n2_pi_2s_breaks_runge_lenz_k=breaks_rl_ok,
        dirac_fs_2s_half_coeff=fs_2s_half,
        dirac_fs_2p_half_coeff=fs_2p_half,
        dirac_fs_2p_three_halves_coeff=fs_2p_three_halves,
        dirac_fs_2s_2p_half_degenerate=fs_deg,
        dirac_fs_fine_structure_splitting_coeff=fs_split,
        lyman_alpha_gross_thz_interval=lyman_thz_iv,
        lyman_alpha_gross_thz_decimal_12=lyman_dec_12,
        lyman_alpha_gross_thz_12_digits_agree=lyman_ok,
        lamb_contact_2s_2p_mhz_interval=lamb_contact_iv,
        lamb_contact_2s_2p_mhz_decimal_12=lamb_contact_dec_12,
        lamb_contact_2s_2p_mhz_12_digits_agree=lamb_contact_ok,
    )
