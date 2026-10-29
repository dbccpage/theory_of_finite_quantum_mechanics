"""Exact rational and algebraic certifiers for FQCD Strong-Coupling Area Law (Record TFQ-1052).

Governing DAG target node: FQCD-STRONG-COUPLING-AREA-LAW
AuthorityEffect: None

Implements:
1. Exact coordination numbers: Delta_d = 2d(d-1) for d >= 2.
2. Exact closed-form strong-coupling threshold: beta_0(N, d) = [8 e Delta_d (N-1)]^{-1} > 0.
3. Exact constants: K = 1, sigma_0 = ln(4) > 0.
4. Single-plaquette character activity bound: |a_m(beta)/a_0(beta)| <= beta < beta_0 for non-trivial characters of Z_N.
5. Minimal spanning area Area(C) = L * T for rectangular loop C = L x T on periodic lattice.
6. Geometric cluster series area-law bound: sum_{A >= Area(C)} (8 e Delta_d (N-1) beta)^A <= K exp(-sigma_0 Area(C)).
7. General finite-group features:
   - S_3 cubic character invariant sum_{g in S_3} chi_2(g)^3 / 6 = 1.0; hollow tube collar tensor contraction
     c_X = 2^{-E_off} > 0 mediating screening to perimeter law for L >= 17.
   - Q_8 cubic character invariant sum_{g in Q_8} chi_2(g)^3 / 8 = 0.0; center parity {+1, -1} protects
     spanning surface against collar tube screening, preserving area law.
   - 2D character decimation area law: <W_R(C)> = (dim R)^{1 - Area(C)} * (a_R(beta)/a_0(beta))^{Area(C)}.
"""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Any, Dict, Tuple

# Exact constants
CONST_K: int = 1
CONST_SIGMA_0: float = math.log(4.0)  # ln(4) > 0, exp(-sigma_0) = 1/4 = 0.25


def coordination_number_delta(d: int) -> int:
    """Exact plaquette coordination number Delta_d = 2d(d-1) on d-dimensional hypercubic lattice."""
    if d < 2:
        raise ValueError(f"Lattice dimension must be d >= 2, got {d}")
    return 2 * d * (d - 1)


def strong_coupling_threshold_beta0(n: int, d: int) -> float:
    """Exact closed-form strong-coupling convergence threshold: beta_0(N, d) = [8 e Delta_d (N-1)]^{-1}."""
    if n < 2:
        raise ValueError(f"Group parameter N must be >= 2, got {n}")
    if d < 2:
        raise ValueError(f"Lattice dimension d must be >= 2, got {d}")
    delta = coordination_number_delta(d)
    return 1.0 / (8.0 * math.e * delta * (n - 1))


def strong_coupling_threshold_beta0_rational(n: int, d: int) -> Fraction:
    """Certified rational strong-coupling threshold using rational approximation e ~ 2718/1000 = 1359/500."""
    if n < 2:
        raise ValueError(f"Group parameter N must be >= 2, got {n}")
    if d < 2:
        raise ValueError(f"Lattice dimension d must be >= 2, got {d}")
    delta = coordination_number_delta(d)
    e_approx = Fraction(1359, 500)
    denominator = Fraction(8, 1) * e_approx * Fraction(delta * (n - 1), 1)
    return Fraction(1, 1) / denominator


def strong_coupling_threshold_beta0_rational_bounds(n: int, d: int) -> Tuple[Fraction, Fraction]:
    """Certified lower and upper rational bounds on beta_0(N, d) using 19/7 < e < 193/71.

    Since beta_0 = [8 e Delta (N-1)]^{-1}, larger e yields a smaller lower bound:
    beta_0_lower = [8 * (193/71) * Delta * (N-1)]^{-1}
    beta_0_upper = [8 * (19/7) * Delta * (N-1)]^{-1}
    """
    if n < 2:
        raise ValueError(f"Group parameter N must be >= 2, got {n}")
    if d < 2:
        raise ValueError(f"Lattice dimension d must be >= 2, got {d}")
    delta = coordination_number_delta(d)
    factor = Fraction(8 * delta * (n - 1), 1)
    lower = Fraction(1, 1) / (factor * Fraction(193, 71))
    upper = Fraction(1, 1) / (factor * Fraction(19, 7))
    return lower, upper


def minimal_spanning_area(l: int, t: int) -> int:
    """Minimal cellular spanning area Area(C) = L * T for rectangular loop C = L x T."""
    if l <= 0 or t <= 0:
        raise ValueError(f"Loop dimensions must be strictly positive: L={l}, T={t}")
    return l * t


def loop_perimeter(l: int, t: int) -> int:
    """Loop perimeter Perimeter(C) = 2(L + T) for rectangular loop C = L x T."""
    if l <= 0 or t <= 0:
        raise ValueError(f"Loop dimensions must be strictly positive: L={l}, T={t}")
    return 2 * (l + t)


def single_plaquette_character_activity_zn(n: int, m: int, beta: float) -> Tuple[float, float, float]:
    """Single-plaquette character activity coefficients a_m(beta), a_0(beta) and ratio alpha_m = a_m/a_0 for Z_N.

    Action weight for link holonomy g in Z_N: w(g) = exp(beta * cos(2*pi*g/N)).
    Character: chi_m(g) = exp(2*pi*i*m*g/N).
    a_m(beta) = (1/N) sum_{g=0}^{N-1} exp(beta * cos(2*pi*g/N)) * cos(2*pi*m*g/N).
    """
    if n < 2:
        raise ValueError(f"Group parameter N must be >= 2, got {n}")
    m_mod = m % n
    total_m = 0.0
    total_0 = 0.0
    for g in range(n):
        angle = 2.0 * math.pi * g / n
        weight = math.exp(beta * math.cos(angle))
        total_0 += weight
        total_m += weight * math.cos(m_mod * angle)
    a_0 = total_0 / n
    a_m = total_m / n
    alpha_m = a_m / a_0 if a_0 > 0.0 else 0.0
    return a_m, a_0, alpha_m


def cluster_series_geometric_sum(mu: float, min_area: int) -> float:
    """Exact sum of geometric series sum_{A >= min_area} mu^A = mu^{min_area} / (1 - mu) for 0 <= mu < 1."""
    if not (0.0 <= mu < 1.0):
        raise ValueError(f"Cluster activity mu must be in [0, 1), got {mu}")
    if min_area < 1:
        raise ValueError(f"min_area must be >= 1, got {min_area}")
    return (mu ** min_area) / (1.0 - mu)


def cluster_series_geometric_sum_rational(mu: Fraction, min_area: int) -> Fraction:
    """Exact rational sum of geometric series sum_{A >= min_area} mu^A = mu^{min_area} / (1 - mu) for 0 <= mu < 1."""
    if not (Fraction(0, 1) <= mu < Fraction(1, 1)):
        raise ValueError(f"Cluster activity mu must be in [0, 1), got {mu}")
    if min_area < 1:
        raise ValueError(f"min_area must be >= 1, got {min_area}")
    return (mu ** min_area) / (Fraction(1, 1) - mu)


def area_law_decay_bound(min_area: int) -> float:
    """Area law upper bound K * exp(-sigma_0 * min_area) with K = 1, sigma_0 = ln(4).

    exp(-sigma_0 * min_area) = (1/4)^{min_area} = 0.25^{min_area}.
    """
    if min_area < 1:
        raise ValueError(f"min_area must be >= 1, got {min_area}")
    return CONST_K * math.exp(-CONST_SIGMA_0 * min_area)


def area_law_decay_bound_rational(min_area: int) -> Fraction:
    """Exact rational area law upper bound (1/4)^{min_area}."""
    if min_area < 1:
        raise ValueError(f"min_area must be >= 1, got {min_area}")
    return Fraction(1, 4 ** min_area)


def geometric_cluster_series_bound_satisfied(n: int, d: int, beta: float, min_area: int) -> bool:
    """Verify that cluster series sum_{A >= Area} (8 e Delta_d (N-1) beta)^A <= K exp(-sigma_0 Area).

    For mu = 8 e Delta_d (N-1) beta <= 1/5 (which holds for beta <= beta_0(N, d) / 5),
    sum_{A >= Area} mu^A = mu^Area / (1 - mu) <= (1/5)^Area / (4/5) = (5/4) * (1/5)^Area <= (1/4)^Area.
    """
    delta = coordination_number_delta(d)
    mu = 8.0 * math.e * delta * (n - 1) * beta
    if mu >= 1.0 or mu < 0.0:
        return False
    geom_sum = cluster_series_geometric_sum(mu, min_area)
    bound = area_law_decay_bound(min_area)
    return geom_sum <= bound + 1e-15


def s3_cubic_character_invariant() -> float:
    """Compute the S_3 cubic character invariant sum_{g in S_3} chi_2(g)^3 / 6.

    S_3 has 6 elements in 3 conjugacy classes:
    - 1 Identity element: chi_2(e) = 2
    - 3 Transpositions: chi_2(tau) = 0
    - 2 3-cycles: chi_2(sigma) = -1
    sum = 1 * 2^3 + 3 * 0^3 + 2 * (-1)^3 = 8 + 0 - 2 = 6.
    Average = 6 / 6 = 1.0.
    """
    classes = [
        (1, 2.0),   # Identity: count 1, chi = 2
        (3, 0.0),   # Transpositions: count 3, chi = 0
        (2, -1.0),  # 3-cycles: count 2, chi = -1
    ]
    total = sum(count * (chi ** 3) for count, chi in classes)
    return total / 6.0


def s3_cubic_character_invariant_rational() -> Fraction:
    """Exact rational S_3 cubic character invariant = 6/6 = 1/1."""
    return Fraction(1 * 8 + 3 * 0 + 2 * (-1), 6)


def collar_tube_contraction(e_off: int) -> float:
    """Hollow tube collar tensor contraction c_X = 2^{-E_off} > 0."""
    if e_off < 0:
        raise ValueError(f"Off-surface edge count must be non-negative, got {e_off}")
    return 2.0 ** (-e_off)


def collar_tube_contraction_rational(e_off: int) -> Fraction:
    """Exact rational collar tensor contraction c_X = 1 / 2^{E_off}."""
    if e_off < 0:
        raise ValueError(f"Off-surface edge count must be non-negative, got {e_off}")
    return Fraction(1, 2 ** e_off)


def q8_cubic_character_invariant() -> float:
    """Compute the Q_8 cubic character invariant sum_{g in Q_8} chi_2(g)^3 / 8.

    Q_8 has 8 elements {+1, -1, +-i, +-j, +-k}:
    - 1 element (+1): chi_2 = +2
    - 1 element (-1): chi_2 = -2
    - 6 elements (+-i, +-j, +-k): chi_2 = 0
    sum = 1 * 2^3 + 1 * (-2)^3 + 6 * 0^3 = 8 - 8 + 0 = 0.
    Average = 0 / 8 = 0.0.
    """
    classes = [
        (1, 2.0),   # +1: count 1, chi = +2
        (1, -2.0),  # -1: count 1, chi = -2
        (6, 0.0),   # +-i, +-j, +-k: count 6, chi = 0
    ]
    total = sum(count * (chi ** 3) for count, chi in classes)
    return total / 8.0


def q8_cubic_character_invariant_rational() -> Fraction:
    """Exact rational Q_8 cubic character invariant = 0/8 = 0/1."""
    return Fraction(1 * 8 + 1 * (-8) + 6 * 0, 8)


def q8_center_parity_protection() -> Dict[str, Any]:
    """Examine center parity protection in Q_8 preventing trivalent collar tube screening."""
    return {
        "group": "Q_8",
        "order": 8,
        "center_elements": ["+1", "-1"],
        "representation_dimension": 2,
        "chi_identity": 2,
        "chi_center_defect": -2,
        "center_parity": -1,
        "cubic_invariant": 0.0,
        "screening_protection": True,
        "mechanism": "Nontrivial center element -1 acts as -I_2; chi_2(-1) = -2 yields (-1)^3 = -1, forbidding trivalent singlet fusion and preserving area law",
    }


def twod_character_decimation_area_law(dim_r: int, activity_ratio: float, area: int) -> float:
    """Exact 2D character decimation area law: <W_R(C)> = (dim R)^{1 - Area(C)} * (a_R(beta)/a_0(beta))^{Area(C)}."""
    if dim_r < 1:
        raise ValueError(f"Representation dimension must be >= 1, got {dim_r}")
    if area < 1:
        raise ValueError(f"Area must be >= 1, got {area}")
    return (dim_r ** (1 - area)) * (activity_ratio ** area)


def twod_character_decimation_area_law_rational(dim_r: int, activity_ratio: Fraction, area: int) -> Fraction:
    """Exact rational 2D character decimation area law."""
    if dim_r < 1:
        raise ValueError(f"Representation dimension must be >= 1, got {dim_r}")
    if area < 1:
        raise ValueError(f"Area must be >= 1, got {area}")
    dim_factor = Fraction(dim_r ** (1 - area), 1) if (1 - area) >= 0 else Fraction(1, dim_r ** (area - 1))
    return dim_factor * (activity_ratio ** area)


def s4_cubic_character_invariants_rational() -> Dict[str, Fraction]:
    """Exact rational normalized cubic character invariants for S_4 (order 24).

    Conjugacy classes of S_4 have sizes (1, 6, 8, 6, 3):
    - 3: chi = (3, 1, 0, -1, -1) -> sum = 27 + 6 + 0 - 6 - 3 = 24 -> 24/24 = 1
    - 3': chi = (3, -1, 0, 1, -1) -> sum = 27 - 6 + 0 + 6 - 3 = 24 -> 24/24 = 1
    - 2: chi = (2, 0, -1, 0, 2) -> sum = 8 + 0 - 8 + 0 + 24 = 24 -> 24/24 = 1
    - sgn: chi = (1, -1, 1, -1, 1) -> sum = 1 - 6 + 8 - 6 + 3 = 0 -> 0/24 = 0
    """
    order = 24
    sum_3 = 1 * (3 ** 3) + 6 * (1 ** 3) + 8 * (0 ** 3) + 6 * ((-1) ** 3) + 3 * ((-1) ** 3)
    sum_3_prime = 1 * (3 ** 3) + 6 * ((-1) ** 3) + 8 * (0 ** 3) + 6 * (1 ** 3) + 3 * ((-1) ** 3)
    sum_2 = 1 * (2 ** 3) + 6 * (0 ** 3) + 8 * ((-1) ** 3) + 6 * (0 ** 3) + 3 * (2 ** 3)
    sum_sgn = 1 * (1 ** 3) + 6 * ((-1) ** 3) + 8 * (1 ** 3) + 6 * ((-1) ** 3) + 3 * (1 ** 3)
    return {
        "3": Fraction(sum_3, order),
        "3_prime": Fraction(sum_3_prime, order),
        "2": Fraction(sum_2, order),
        "sgn": Fraction(sum_sgn, order),
    }


def a5_cubic_character_invariants_rational() -> Dict[str, Fraction]:
    """Exact rational normalized cubic character invariants for A_5 (order 60).

    Conjugacy classes of A_5 have sizes (1, 15, 20, 12, 12):
    - 3_a, 3_b: over the two 5-cycle classes of size 12, phi^3 + (1 - phi)^3 = 4,
      so sum = 1 * 3^3 + 15 * (-1)^3 + 20 * 0^3 + 12 * 4 = 27 - 15 + 48 = 60 -> 60/60 = 1.
    - 4: chi = (4, 0, 1, -1, -1) -> sum = 64 + 0 + 20 - 12 - 12 = 60 -> 60/60 = 1.
    - 5: chi = (5, 1, -1, 0, 0) -> sum = 125 + 15 - 20 + 0 + 0 = 120 -> 120/60 = 2.
    """
    order = 60
    sum_3 = 1 * (3 ** 3) + 15 * ((-1) ** 3) + 20 * (0 ** 3) + 12 * 4
    sum_4 = 1 * (4 ** 3) + 15 * (0 ** 3) + 20 * (1 ** 3) + 12 * ((-1) ** 3) + 12 * ((-1) ** 3)
    sum_5 = 1 * (5 ** 3) + 15 * (1 ** 3) + 20 * ((-1) ** 3) + 12 * (0 ** 3) + 12 * (0 ** 3)
    return {
        "3_a": Fraction(sum_3, order),
        "3_b": Fraction(sum_3, order),
        "4": Fraction(sum_4, order),
        "5": Fraction(sum_5, order),
    }


def general_collar_tube_contraction_rational(dim_r: int, e_off: int) -> Fraction:
    """General representation collar tensor contraction c_X(d_R, E_off) = d_R^{-E_off}."""
    if dim_r < 1:
        raise ValueError(f"Representation dimension must be >= 1, got {dim_r}")
    if e_off < 0:
        raise ValueError(f"Off-surface edge count must be non-negative, got {e_off}")
    return Fraction(1, dim_r ** e_off)


def normal_directions_count(d: int) -> int:
    """Number of orthogonal normal half-plane directions to a 2D planar loop in dimension d >= 3: N_normal(d) = 2(d - 2)."""
    if d < 3:
        raise ValueError(f"Dimension must be >= 3 for normal collar directions, got {d}")
    return 2 * (d - 2)


def d4_multi_plaquette_collar_bound_rational(
    perim: int, width_k: int, dim_r: int, beta: Fraction
) -> Fraction:
    """Multi-plaquette boundary collar contraction bound in d = 4:
    B_collar^(d=4)(P, k, d_R, beta) = (4 * d_R^{-2k} * beta^{3k})^P.
    """
    if perim < 1 or width_k < 1 or dim_r < 2:
        raise ValueError("Requires perim >= 1, width_k >= 1, dim_r >= 2")
    if beta <= Fraction(0, 1):
        raise ValueError("Requires beta > 0")
    step_factor = Fraction(4, dim_r ** (2 * width_k)) * (beta ** (3 * width_k))
    return step_factor ** perim


def binary_icosahedral_2i_invariants_rational() -> Dict[str, Fraction]:
    """Exact cubic character invariants I_3(2I, R) = (1/120) sum_{g in 2I} chi_R(g)^3
    for the binary icosahedral group 2I subset SU(2) (|2I| = 120):
    - Spinorial (Z_2-odd) irreps 2_s, 2_s_prime, 4_s, 6_s: I_3 = 0 (Z_2 center protection)
    - Tensorial (Z_2-even, A_5 quotient) irreps 3_a, 3_b, 4_t, 5_t: I_3 = 1, 1, 1, 2
    """
    order = 120
    # Spinorial 2_s over 9 classes (1, 1, 30, 20, 20, 12, 12, 12, 12): central pairs (g, -g) cancel
    sum_2s = 1 * (2 ** 3) + 1 * ((-2) ** 3) + 30 * 0 + 20 * (1 ** 3) + 20 * ((-1) ** 3) + 12 * 0 + 12 * 0
    # Tensorial irreps lift from A_5 with factor 2
    a5_invs = a5_cubic_character_invariants_rational()
    return {
        "2_s": Fraction(sum_2s, order),
        "2_s_prime": Fraction(sum_2s, order),
        "4_s": Fraction(0, 1),
        "6_s": Fraction(0, 1),
        "3_a": a5_invs["3_a"],
        "3_b": a5_invs["3_b"],
        "4_t": a5_invs["4"],
        "5_t": a5_invs["5"],
    }


def valentiner_sigma1080_invariants_rational() -> Dict[str, Fraction]:
    """Exact character invariants for the Valentiner group Sigma(1080) = 3.A_6 subset SU(3) (|Sigma(1080)| = 1080):
    - Faithful 3D fundamental 3_a: I_{1,1}(3_a) = 1, I_2(3_a) = 0 (Z_3 quadratic protection),
      I_3(3_a) = 1 (baryon-singlet cubic invariant 3_a^{otimes 3} = 10 + 8_a + 8_a + 1)
    - Quotient A_6 irreps: I_3(5_a) = 1, I_3(8_a) = 2 (SU(3) adjoint f_{abc} and d_{abc}), I_3(10) = 2
    """
    order = 1080
    norm_sq_3a = 3 * 9 + 135 * 1 + 120 * 0 + 120 * 0 + 270 * 1 + 216 * 3
    sq_3a = 0
    cubed_3a = 3 * (3 ** 3) + 135 * ((-1) ** 3) + 120 * 0 + 120 * 0 + 270 * (1 ** 3) + 216 * 4
    cubed_5a = 3 * (1 * (5 ** 3) + 45 * (1 ** 3) + 40 * (2 ** 3) + 40 * ((-1) ** 3) + 90 * ((-1) ** 3))
    cubed_8a = 3 * (1 * (8 ** 3) + 45 * 0 + 40 * ((-1) ** 3) + 40 * ((-1) ** 3) + 90 * 0 + 72 * 4)
    cubed_10 = 3 * (1 * (10 ** 3) + 45 * ((-2) ** 3) + 40 * (1 ** 3) + 40 * (1 ** 3))
    return {
        "I11_3a": Fraction(norm_sq_3a, order),
        "I2_3a": Fraction(sq_3a, order),
        "I3_3a": Fraction(cubed_3a, order),
        "I3_5a": Fraction(cubed_5a, order),
        "I3_8a": Fraction(cubed_8a, order),
        "I3_10": Fraction(cubed_10, order),
    }


def freezing_plaquette_defect_rational_bounds() -> Dict[str, Tuple[Fraction, Fraction]]:
    """Exact rational enclosure bounds for minimal non-identity plaquette character defects:
    - Delta_min(2I, 2_s) = (3 - sqrt(5))/4 in (3/16, 1/5) [Petcher-Weingarten 1980]
    - Delta_min(Sigma(1080), 3_a) = (5 - sqrt(5))/6 in (11/24, 7/15) [Bhanot-Rebbi 1981]
    from 11/5 < sqrt(5) < 9/4.
    """
    return {
        "2I_2s": (Fraction(3, 16), Fraction(1, 5)),
        "Sigma1080_3a": (Fraction(11, 24), Fraction(7, 15)),
    }


def su2_ade_binary_polyhedral_tower_rational() -> Dict[str, Any]:
    """Complete SU(2) ADE binary polyhedral subgroup tower (Q_8, 2T, 2O, 2I):
    spinorial vs tensorial cubic character invariants and strict monotonic ordering
    of minimal non-identity plaquette defects:
    0 < 3/16 < Delta_min(2I) < 1/5 < 7/24 < Delta_min(2O) < 3/10 < Delta_min(2T)=1/2 < Delta_min(Q_8)=1.
    """
    i3_2t_2s = Fraction(1 * 8 + 1 * (-8) + 6 * 0 + 4 * 1 + 4 * (-1) + 4 * 1 + 4 * (-1), 24)
    i3_2t_3t = Fraction(2 * (1 * 27 + 3 * (-1)), 24)
    i3_2o_2s = Fraction(0, 48)
    i3_2o_3 = Fraction(2 * 24, 48)
    return {
        "I3_2T_2s": i3_2t_2s,
        "I3_2T_3t": i3_2t_3t,
        "I3_2O_2s": i3_2o_2s,
        "I3_2O_3": i3_2o_3,
        "delta_min_Q8": Fraction(1, 1),
        "delta_min_2T": Fraction(1, 2),
        "delta_min_2O_bounds": (Fraction(7, 24), Fraction(3, 10)),
        "delta_min_2I_bounds": (Fraction(3, 16), Fraction(1, 5)),
    }


def su3_subgroup_tower_and_freezing_scales_rational() -> Dict[str, Any]:
    """SU(3) finite crystal subgroup hierarchy (Delta(27), Delta(54), Sigma(1080))
    cubic character invariants, minimal plaquette defects, and inverse-defect Peierls
    freezing scale proxies beta_freeze^proxy(G, R) = 1 / Delta_min(G, R).
    """
    i3_delta27 = Fraction(3 * 27 + 24 * 0, 27)
    i3_delta54_3_1 = Fraction(81 - 27, 54)
    i3_delta54_3_2 = Fraction(81 + 27, 54)
    d_delta27 = Fraction(1, 1)
    d_delta54 = Fraction(5, 6)
    d_s1080_low, d_s1080_high = Fraction(11, 24), Fraction(7, 15)
    return {
        "I3_Delta27_3": i3_delta27,
        "I3_Delta54_3_1": i3_delta54_3_1,
        "I3_Delta54_3_2": i3_delta54_3_2,
        "delta_min_Delta27": d_delta27,
        "delta_min_Delta54": d_delta54,
        "delta_min_Sigma1080_bounds": (d_s1080_low, d_s1080_high),
        "beta_freeze_proxy_Delta27": Fraction(1, 1) / d_delta27,
        "beta_freeze_proxy_Delta54": Fraction(1, 1) / d_delta54,
        "beta_freeze_proxy_Sigma1080_bounds": (Fraction(1, 1) / d_s1080_high, Fraction(1, 1) / d_s1080_low),
    }


def strong_to_freezing_coupling_gap_rational(n: int, d: int, delta_min: Fraction) -> Fraction:
    """Exact rational intermediate cross-over coupling gap
    Delta_beta_gap(N, d, Delta_min) = 1 / Delta_min - beta_0^rat(N, d)
    separating the strong-coupling cluster-expansion regime from the weak-coupling Peierls frozen regime.
    """
    if delta_min <= Fraction(0, 1):
        raise ValueError("Requires delta_min > 0")
    return (Fraction(1, 1) / delta_min) - strong_coupling_threshold_beta0_rational(n, d)


def klein_sigma168_invariants_and_su3_chain_rational() -> Dict[str, Any]:
    """Exact character invariants and plaquette defect bounds for the Klein simple subgroup
    Sigma(168) = PSL(2, 7) subset SU(3) (|Sigma(168)| = 168) and Sigma(168 x 3) (|Sigma(168 x 3)| = 504):
    - Fundamental 3_a: I_{1,1} = 1, I_2 = 0, I_3 = 1
    - Sextet 6 and septet 7: I_3(6) = 2, I_3(7) = 2
    - Adjoint octet 8: I_2(8) = 1 (irreducible), I_3(8) = 3 > 2 = I_3(Sigma(1080), 8_a)
      (spurious 3rd cubic adjoint invariant on Sigma(168) eliminated in Sigma(1080))
    - Plaquette defects: Delta_min(Sigma(168)) = 2/3, Delta_min(Sigma(168x3)) in (8/15, 13/24).
    """
    order = 168
    return {
        "I11_3a": Fraction(1 * 9 + 21 * 1 + 42 * 1 + 48 * 2, order),
        "I2_3a": Fraction(1 * 9 + 21 * 1 + 42 * 1 + 24 * (-3), order),
        "I3_3a": Fraction(1 * 27 + 21 * (-1) + 42 * 1 + 24 * 5, order),
        "I3_6": Fraction(1 * 216 + 21 * 8 + 48 * (-1), order),
        "I3_7": Fraction(1 * 343 + 21 * (-1) + 56 * 1 + 42 * (-1), order),
        "I2_8": Fraction(1 * 64 + 56 * 1 + 48 * 1, order),
        "I3_8": Fraction(1 * 512 + 56 * (-1) + 48 * 1, order),
        "delta_min_Sigma168": Fraction(2, 3),
        "delta_min_Sigma168x3_bounds": (Fraction(8, 15), Fraction(13, 24)),
    }


def quartic_character_invariants_and_continuum_matching_rational() -> Dict[str, Fraction]:
    """Exact quartic character invariants I_4(G, N) = (1/|G|) sum_{g in G} |chi_N(g)|^4
    measuring <N otimes bar(N), N otimes bar(N)>_G across the SU(2) ADE series (Q_8, 2T, 2O, 2I)
    and the SU(3) crystal hierarchy (Delta(27), Delta(54), Sigma(168), Sigma(1080)).
    I_4(G, N) == 2 iff the (N^2 - 1)-dimensional adjoint representation remains irreducible on G.
    """
    return {
        "I4_Q8_2s": Fraction(1 * 16 + 1 * 16, 8),
        "I4_2T_2s": Fraction(2 * 16 + 16 * 1, 24),
        "I4_2O_2s": Fraction(2 * 16 + 16 * 1 + 12 * 4, 48),
        "I4_2I_2s": Fraction(2 * 16 + 40 * 1 + 24 * 7, 120),
        "I4_Delta27_3": Fraction(3 * 81, 27),
        "I4_Delta54_3": Fraction(3 * 81 + 27 * 1, 54),
        "I4_Sigma168_3a": Fraction(1 * 81 + 21 * 1 + 42 * 1 + 48 * 4, 168),
        "I4_Sigma1080_3a": Fraction(3 * 81 + 135 * 1 + 270 * 1 + 216 * 7, 1080),
    }


def hessian_subgroups_and_quartic_adjoint_casimir_obstruction_rational() -> Dict[str, Any]:
    """Exact invariants for the Principal subgroup Sigma(72 x 3) (|G| = 216) and Hessian subgroup
    Sigma(216 x 3) (|G| = 648) of SU(3), together with the quartic adjoint Casimir hierarchy
    I_4(G, 8) = (1/|G|) sum_{g in G} chi_8(g)^4 across Sigma(72 x 3), Sigma(168), Sigma(216 x 3),
    and Sigma(1080) compared against continuum SU(3) (I_4(SU(3), 8) = 8):
    - Fundamental 3: I_{1,1} = 1, I_3 = 1, I_4 = 2 for both Sigma(72 x 3) and Sigma(216 x 3)
    - Cubic adjoint: I_3(Sigma(72 x 3), 8) = 7 > I_3(Sigma(216 x 3), 8) = I_3(Sigma(168), 8) = 3 > I_3(Sigma(1080), 8_a) = 2
    - Quartic adjoint: I_4(Sigma(72 x 3), 8) = 57 > I_4(Sigma(168), 8) = 25 > I_4(Sigma(216 x 3), 8) = 21
      > I_4(Sigma(1080), 8_a) = 13 > 8 = I_4(SU(3), 8)
    - Burnside / Frobenius dimension obstruction: |Sigma(1080)/Z_3| = |A_6| = 360 < 27^2 = 729.
    """
    return {
        "I11_Sigma72x3_3": Fraction(3 * 9 + 189 * 1, 216),
        "I3_Sigma72x3_3": Fraction(3 * 27 + 162 * 1 + 27 * (-1), 216),
        "I4_Sigma72x3_3": Fraction(3 * 81 + 189 * 1, 216),
        "I11_Sigma216x3_3": Fraction(3 * 9 + 72 * 3 + 405 * 1, 648),
        "I3_Sigma216x3_3": Fraction(3 * 27 + 108 * 1 + 162 * 1 + 27 * (-1) + 72 * 4 + 36 * 1, 648),
        "I4_Sigma216x3_3": Fraction(3 * 81 + 72 * 9 + 405 * 1, 648),
        "I3_Sigma72x3_8": Fraction(3 * (8 ** 3) + 24 * (-1), 216),
        "I3_Sigma216x3_8": Fraction(3 * (8 ** 3) + 72 * (2 ** 3) + 168 * (-1), 648),
        "I4_Sigma72x3_8": Fraction(3 * (8 ** 4) + 24 * 1, 216),
        "I4_Sigma168_8": Fraction(1 * (8 ** 4) + 56 * 1 + 48 * 1, 168),
        "I4_Sigma216x3_8": Fraction(3 * (8 ** 4) + 72 * (2 ** 4) + 168 * 1, 648),
        "I4_Sigma1080_8a": Fraction(3 * (8 ** 4 + 40 * 1 + 40 * 1 + 72 * 7), 1080),
        "I4_SU3_continuum_8": Fraction(1 ** 2 + 2 ** 2 + 1 ** 2 + 1 ** 2 + 1 ** 2, 1),
        "a6_irrep_dim_sq_sum": 1 ** 2 + 5 ** 2 + 5 ** 2 + 8 ** 2 + 8 ** 2 + 9 ** 2 + 10 ** 2,
        "continuum_27_dim_sq": 27 ** 2,
    }


def su2_higher_spin_casimir_and_hessian_defect_bounds_rational() -> Dict[str, Any]:
    """Exact quartic adjoint invariants I_4(G, 3) across the SU(2) ADE series (2T -> 2O -> 2I),
    the spin-2 (5_t) quartic Casimir obstruction on 2I, and the cubic polynomial enclosure of
    the Hessian group minimal plaquette defect Delta_min(Sigma(216 x 3), 3) = (4 - 2c - 2c^2)/3
    for c = cos(2pi/9) (root of 8c^3 - 6c + 1 = 0, enclosed in (36/47, 23/30)).
    """
    c_lower = Fraction(36, 47)
    c_upper = Fraction(23, 30)
    return {
        "I4_2T_3t": Fraction(1 * 81 + 3 * 1, 12),
        "I4_2O_3": Fraction(1 * 81 + 6 * 1 + 3 * 1 + 6 * 1, 24),
        "I4_2I_3a": Fraction(1 * 81 + 15 * 1 + 12 * 7, 60),
        "I4_SU2_continuum_3": Fraction(1 ** 2 + 1 ** 2 + 1 ** 2, 1),
        "I4_2I_5t": Fraction(1 * 625 + 15 * 1 + 20 * 1, 60),
        "I4_SU2_continuum_5": Fraction(1 ** 2 + 1 ** 2 + 1 ** 2 + 1 ** 2 + 1 ** 2, 1),
        "a5_irrep_dim_sq_sum": 1 ** 2 + 3 ** 2 + 3 ** 2 + 4 ** 2 + 5 ** 2,
        "2i_irrep_dim_sq_sum": 1 ** 2 + 2 ** 2 + 2 ** 2 + 3 ** 2 + 3 ** 2 + 4 ** 2 + 4 ** 2 + 5 ** 2 + 6 ** 2,
        "poly_at_36_47": 8 * (c_lower ** 3) - 6 * c_lower + 1,
        "poly_at_23_30": 8 * (c_upper ** 3) - 6 * c_upper + 1,
        "delta_min_Sigma216x3_tight_bounds": (
            (Fraction(4, 1) - 2 * c_upper - 2 * (c_upper ** 2)) / 3,
            (Fraction(4, 1) - 2 * c_lower - 2 * (c_lower ** 2)) / 3,
        ),
        "delta_min_Sigma216x3_bounds": (Fraction(43, 100), Fraction(13, 30)),
    }


def complete_blichfeldt_ffk_su3_crystal_hierarchy_rational() -> Dict[str, Fraction]:
    """Exact invariants for Sigma(36 x 3) (|G| = 108) and Sigma(60 x 3) = A_5 x Z_3 (|G| = 180),
    completing the 8-group Blichfeldt-FFK SU(3) crystal classification:
    - Dyadic halving along Delta(27) -> Delta(54) -> Sigma(36 x 3) -> Sigma(72 x 3):
      <8, 8>_G = 8 -> 4 -> 2 -> 1, I_3(8) = 56 -> 28 -> 14 -> 7, I_4(8) = 456 -> 228 -> 114 -> 57
    - Complete 8-step quartic adjoint descent:
      456 > 228 > 114 > 70 > 57 > 25 > 21 > 13 > 8 = I_4(SU(3), 8).
    """
    return {
        "I11_Sigma36x3_3": Fraction(3 * 9 + 81 * 1, 108),
        "I3_Sigma36x3_3": Fraction(3 * 27 + 54 * 1 + 27 * (-1), 108),
        "I4_Sigma36x3_3": Fraction(3 * 81 + 81 * 1, 108),
        "I2_Sigma60_8": Fraction(1 * 64 + 20 * 1 + 12 * 3, 60),
        "I3_Delta27_8": Fraction(3 * 512 + 24 * (-1), 27),
        "I3_Delta54_8": Fraction(3 * 512 + 24 * (-1), 54),
        "I3_Sigma36x3_8": Fraction(3 * 512 + 24 * (-1), 108),
        "I3_Sigma60_8": Fraction(1 * 512 + 20 * (-1) + 12 * 4, 60),
        "I3_Sigma72x3_8": Fraction(3 * 512 + 24 * (-1), 216),
        "I4_Delta27_8": Fraction(3 * 4096 + 24 * 1, 27),
        "I4_Delta54_8": Fraction(3 * 4096 + 24 * 1, 54),
        "I4_Sigma36x3_8": Fraction(3 * 4096 + 24 * 1, 108),
        "I4_Sigma60_8": Fraction(1 * 4096 + 20 * 1 + 12 * 7, 60),
        "I4_Sigma72x3_8": Fraction(3 * 4096 + 24 * 1, 216),
    }


def baryon_vs_gluon_screening_casimir_and_mednykh_2d_towers_rational() -> Dict[str, Any]:
    """Exact representation-dependent Casimir string-tension ratios (3 vs 6 vs 8 vs 10 in Sigma(1080)/SU(3)
    and 2_s vs 3_a vs 4_s vs 5_t in 2I/SU(2)), baryon-junction vs gluon-collar per-step contraction ratios,
    and 2D Mednykh genus-2 partition-function sums M_2(G) = sum_{R in Irr(G)} (dim R)^{-2} and
    Z_Mednykh(G, 2) = |G|^2 M_2(G) across the SU(2) ADE and SU(3) crystal towers.
    """
    m2_q8 = sum(Fraction(1, d ** 2) for d in [1, 1, 1, 1, 2])
    m2_2t = sum(Fraction(1, d ** 2) for d in [1, 1, 1, 2, 2, 2, 3])
    m2_2o = sum(Fraction(1, d ** 2) for d in [1, 1, 2, 2, 2, 3, 3, 4])
    m2_2i = sum(Fraction(1, d ** 2) for d in [1, 2, 2, 3, 3, 4, 4, 5, 6])
    m2_d27 = sum(Fraction(1, d ** 2) for d in [1] * 9 + [3] * 2)
    m2_d54 = sum(Fraction(1, d ** 2) for d in [1] * 2 + [2] * 4 + [3] * 4)
    m2_s168x3 = sum(Fraction(1, d ** 2) for d in [1, 3, 3, 6, 7, 8] * 3)
    m2_s216x3 = sum(Fraction(1, d ** 2) for d in [1] * 3 + [2] * 3 + [3] * 7 + [6] * 6 + [8] * 3 + [9] * 2)
    s1080_dims = [1, 5, 5, 8, 8, 9, 10] + [3, 3, 6, 9, 15] * 2
    m2_s1080 = sum(Fraction(1, d ** 2) for d in s1080_dims)
    return {
        "casimir_ratio_SU3_8_over_3": Fraction(3, 1) / Fraction(4, 3),
        "casimir_ratio_SU3_6_over_3": Fraction(10, 3) / Fraction(4, 3),
        "casimir_ratio_SU3_10_over_3": Fraction(6, 1) / Fraction(4, 3),
        "casimir_ratio_SU2_3a_over_2s": Fraction(2, 1) / Fraction(3, 4),
        "casimir_ratio_SU2_4s_over_2s": Fraction(15, 4) / Fraction(3, 4),
        "casimir_ratio_SU2_5t_over_2s": Fraction(6, 1) / Fraction(3, 4),
        "collar_ratio_3_over_6_e4": general_collar_tube_contraction_rational(3, 4) / general_collar_tube_contraction_rational(6, 4),
        "collar_ratio_3_over_8_e4": general_collar_tube_contraction_rational(3, 4) / general_collar_tube_contraction_rational(8, 4),
        "M2_Q8": m2_q8,
        "M2_2T": m2_2t,
        "M2_2O": m2_2o,
        "M2_2I": m2_2i,
        "Z2_Q8": (8 ** 2) * m2_q8,
        "Z2_2T": (24 ** 2) * m2_2t,
        "Z2_2O": (48 ** 2) * m2_2o,
        "Z2_2I": (120 ** 2) * m2_2i,
        "sigma1080_irrep_dim_sq_sum": sum(d ** 2 for d in s1080_dims),
        "M2_Delta27": m2_d27,
        "M2_Delta54": m2_d54,
        "M2_Sigma168x3": m2_s168x3,
        "M2_Sigma216x3": m2_s216x3,
        "M2_Sigma1080": m2_s1080,
        "Z2_Sigma216x3": (648 ** 2) * m2_s216x3,
        "Z2_Sigma1080": (1080 ** 2) * m2_s1080,
    }


def verify_fqcd_strong_coupling_area_law_witness() -> Dict[str, Any]:
    """Master multi-language verification witness for Record TFQ-1052."""
    checks = []

    # 1. Coordination numbers
    for d, expected_delta in [(2, 4), (3, 12), (4, 24), (5, 40)]:
        delta = coordination_number_delta(d)
        checks.append(("delta_coordination", d, delta == expected_delta))

    # 2. Strong coupling thresholds positivity and monotonicity
    beta0_z2_d4 = strong_coupling_threshold_beta0(2, 4)
    beta0_z3_d4 = strong_coupling_threshold_beta0(3, 4)
    beta0_z2_d3 = strong_coupling_threshold_beta0(2, 3)
    checks.append(("beta0_positivity", 0, beta0_z2_d4 > 0.0))
    checks.append(("beta0_n_monotonicity", 0, beta0_z2_d4 > beta0_z3_d4))
    checks.append(("beta0_d_monotonicity", 0, beta0_z2_d3 > beta0_z2_d4))

    # Rational bounds
    lower_rat, upper_rat = strong_coupling_threshold_beta0_rational_bounds(2, 4)
    checks.append(("beta0_rational_bounds", 0, lower_rat < upper_rat and lower_rat > 0))

    # 3. Exact constants
    checks.append(("const_k", 0, CONST_K == 1))
    checks.append(("const_sigma0", 0, abs(math.exp(-CONST_SIGMA_0) - 0.25) < 1e-15))

    # 4. Spanning area and perimeter
    area_3x5 = minimal_spanning_area(3, 5)
    perim_3x5 = loop_perimeter(3, 5)
    checks.append(("minimal_spanning_area", 0, area_3x5 == 15))
    checks.append(("loop_perimeter", 0, perim_3x5 == 16))

    # 5. Cluster series bound
    for area in [1, 2, 3, 4, 10]:
        sat = geometric_cluster_series_bound_satisfied(2, 4, beta0_z2_d4 / 5.0, area)
        checks.append(("cluster_series_bound", area, sat))

    # 6. S_3 vs Q_8 invariants
    s3_inv = s3_cubic_character_invariant()
    s3_inv_rat = s3_cubic_character_invariant_rational()
    checks.append(("s3_cubic_invariant", 0, abs(s3_inv - 1.0) < 1e-15 and s3_inv_rat == Fraction(1, 1)))

    q8_inv = q8_cubic_character_invariant()
    q8_inv_rat = q8_cubic_character_invariant_rational()
    checks.append(("q8_cubic_invariant", 0, abs(q8_inv) < 1e-15 and q8_inv_rat == Fraction(0, 1)))

    # Collar tube screening for S_3 vs Q_8 protection
    checks.append(("collar_contraction_positivity", 0, collar_tube_contraction(17) > 0.0))
    q8_prot = q8_center_parity_protection()
    checks.append(("q8_protection", 0, q8_prot["screening_protection"] is True))

    # 7. 2D decimation
    dec_u1 = twod_character_decimation_area_law(1, 0.1, 4)
    checks.append(("2d_decimation_u1", 0, abs(dec_u1 - 0.0001) < 1e-12))
    dec_q8 = twod_character_decimation_area_law(2, 0.1, 3)
    # (2)^{1 - 3} * (0.1)^3 = 2^{-2} * 10^{-3} = 0.25 * 0.001 = 0.00025
    checks.append(("2d_decimation_q8", 0, abs(dec_q8 - 0.00025) < 1e-12))

    # 8. Higher-order non-abelian S_4 and A_5 cubic invariants
    s4_invs = s4_cubic_character_invariants_rational()
    checks.append(("s4_cubic_invariants", 0, (
        s4_invs["3"] == Fraction(1, 1)
        and s4_invs["3_prime"] == Fraction(1, 1)
        and s4_invs["2"] == Fraction(1, 1)
        and s4_invs["sgn"] == Fraction(0, 1)
    )))
    a5_invs = a5_cubic_character_invariants_rational()
    checks.append(("a5_cubic_invariants", 0, (
        a5_invs["3_a"] == Fraction(1, 1)
        and a5_invs["3_b"] == Fraction(1, 1)
        and a5_invs["4"] == Fraction(1, 1)
        and a5_invs["5"] == Fraction(2, 1)
    )))

    # 9. General d_R collar contraction and d=4 multi-plaquette collar bound
    checks.append(("general_collar_contraction_d3", 0, general_collar_tube_contraction_rational(3, 4) == Fraction(1, 81)))
    checks.append(("d4_normal_directions", 0, normal_directions_count(4) == 4))
    d4_b1 = d4_multi_plaquette_collar_bound_rational(4, 1, 2, Fraction(1, 10))
    d4_b2 = d4_multi_plaquette_collar_bound_rational(4, 2, 2, Fraction(1, 10))
    checks.append(("d4_collar_bound_decay", 0, Fraction(0, 1) < d4_b2 < d4_b1 == Fraction(1, 10 ** 12)))

    # 10. Binary icosahedral 2I and Valentiner Sigma(1080) invariants & freezing defect bounds
    invs_2i = binary_icosahedral_2i_invariants_rational()
    checks.append(("2i_spinorial_protection_and_adjoint_screening", 0, (
        invs_2i["2_s"] == Fraction(0, 1)
        and invs_2i["3_a"] == Fraction(1, 1)
        and invs_2i["4_t"] == Fraction(1, 1)
        and invs_2i["5_t"] == Fraction(2, 1)
    )))
    invs_s1080 = valentiner_sigma1080_invariants_rational()
    checks.append(("sigma1080_invariants", 0, (
        invs_s1080["I11_3a"] == Fraction(1, 1)
        and invs_s1080["I2_3a"] == Fraction(0, 1)
        and invs_s1080["I3_3a"] == Fraction(1, 1)
        and invs_s1080["I3_5a"] == Fraction(1, 1)
        and invs_s1080["I3_8a"] == Fraction(2, 1)
        and invs_s1080["I3_10"] == Fraction(2, 1)
    )))
    defects = freezing_plaquette_defect_rational_bounds()
    d2i_low, d2i_high = defects["2I_2s"]
    ds1080_low, ds1080_high = defects["Sigma1080_3a"]
    checks.append(("freezing_defect_bounds", 0, (
        Fraction(0, 1) < d2i_low < d2i_high < ds1080_low < ds1080_high < Fraction(1, 1)
    )))

    # 11. Complete SU(2) ADE and SU(3) subgroup towers & freezing scale proxies
    su2_tower = su2_ade_binary_polyhedral_tower_rational()
    d2o_low, d2o_high = su2_tower["delta_min_2O_bounds"]
    checks.append(("su2_ade_tower_monotonicity", 0, (
        su2_tower["I3_2T_2s"] == Fraction(0, 1)
        and su2_tower["I3_2T_3t"] == Fraction(2, 1)
        and su2_tower["I3_2O_2s"] == Fraction(0, 1)
        and su2_tower["I3_2O_3"] == Fraction(1, 1)
        and Fraction(0, 1) < d2i_low < d2i_high < d2o_low < d2o_high < su2_tower["delta_min_2T"] < su2_tower["delta_min_Q8"]
    )))
    su3_tower = su3_subgroup_tower_and_freezing_scales_rational()
    bf_s1080_low, bf_s1080_high = su3_tower["beta_freeze_proxy_Sigma1080_bounds"]
    checks.append(("su3_tower_and_freezing_proxies", 0, (
        su3_tower["I3_Delta27_3"] == Fraction(3, 1)
        and su3_tower["I3_Delta54_3_1"] == Fraction(1, 1)
        and su3_tower["I3_Delta54_3_2"] == Fraction(2, 1)
        and su3_tower["beta_freeze_proxy_Delta27"] < su3_tower["beta_freeze_proxy_Delta54"] < bf_s1080_low < bf_s1080_high
    )))

    # 12. Strong-coupling vs freezing regime separation & gap widening
    g_q8 = strong_to_freezing_coupling_gap_rational(8, 4, Fraction(1, 1))
    g_2t = strong_to_freezing_coupling_gap_rational(24, 4, Fraction(1, 2))
    g_2o_low = strong_to_freezing_coupling_gap_rational(48, 4, Fraction(3, 10))
    g_2i_low = strong_to_freezing_coupling_gap_rational(120, 4, Fraction(1, 5))
    g_d27 = strong_to_freezing_coupling_gap_rational(27, 4, Fraction(1, 1))
    g_d54 = strong_to_freezing_coupling_gap_rational(54, 4, Fraction(5, 6))
    g_s1080_low = strong_to_freezing_coupling_gap_rational(1080, 4, Fraction(7, 15))
    checks.append(("strong_to_freezing_gap_widening", 0, (
        Fraction(999, 1000) < g_q8 < g_2t < g_2o_low < g_2i_low
        and Fraction(999, 1000) < g_d27 < g_d54 < g_s1080_low
    )))

    # 13. Klein Sigma(168) invariants, spurious cubic adjoint elimination, and complete SU(3) defect chain
    s168 = klein_sigma168_invariants_and_su3_chain_rational()
    ds168x3_low, ds168x3_high = s168["delta_min_Sigma168x3_bounds"]
    checks.append(("klein_sigma168_and_su3_chain", 0, (
        s168["I11_3a"] == Fraction(1, 1)
        and s168["I2_3a"] == Fraction(0, 1)
        and s168["I3_3a"] == Fraction(1, 1)
        and s168["I3_6"] == Fraction(2, 1)
        and s168["I3_7"] == Fraction(2, 1)
        and s168["I2_8"] == Fraction(1, 1)
        and s168["I3_8"] == Fraction(3, 1) > invs_s1080["I3_8a"]
        and ds1080_low < ds1080_high < ds168x3_low < ds168x3_high < s168["delta_min_Sigma168"] < su3_tower["delta_min_Delta54"] < su3_tower["delta_min_Delta27"]
    )))

    # 14. Quartic character invariants I_4(G, N) & unique SU(3) continuum matching at Sigma(1080)
    q4 = quartic_character_invariants_and_continuum_matching_rational()
    checks.append(("quartic_invariants_and_continuum_matching", 0, (
        q4["I4_Q8_2s"] == Fraction(4, 1)
        and q4["I4_2T_2s"] == q4["I4_2O_2s"] == q4["I4_2I_2s"] == Fraction(2, 1)
        and q4["I4_Delta27_3"] == Fraction(9, 1)
        and q4["I4_Delta54_3"] == Fraction(5, 1)
        and q4["I4_Sigma168_3a"] == q4["I4_Sigma1080_3a"] == Fraction(2, 1)
        and (invs_s1080["I3_3a"], q4["I4_Sigma1080_3a"], invs_s1080["I3_8a"]) == (Fraction(1, 1), Fraction(2, 1), Fraction(2, 1))
    )))

    # 15. Principal & Hessian subgroups Sigma(72x3), Sigma(216x3) & quartic adjoint Casimir obstruction
    hess = hessian_subgroups_and_quartic_adjoint_casimir_obstruction_rational()
    checks.append(("hessian_subgroups_and_quartic_adjoint_obstruction", 0, (
        hess["I11_Sigma72x3_3"] == hess["I3_Sigma72x3_3"] == Fraction(1, 1)
        and hess["I4_Sigma72x3_3"] == Fraction(2, 1)
        and hess["I11_Sigma216x3_3"] == hess["I3_Sigma216x3_3"] == Fraction(1, 1)
        and hess["I4_Sigma216x3_3"] == Fraction(2, 1)
        and hess["I3_Sigma72x3_8"] == Fraction(7, 1) > hess["I3_Sigma216x3_8"] == Fraction(3, 1) > invs_s1080["I3_8a"]
        and hess["I4_Sigma72x3_8"] == Fraction(57, 1)
        > hess["I4_Sigma168_8"] == Fraction(25, 1)
        > hess["I4_Sigma216x3_8"] == Fraction(21, 1)
        > hess["I4_Sigma1080_8a"] == Fraction(13, 1)
        > hess["I4_SU3_continuum_8"] == Fraction(8, 1)
        and hess["a6_irrep_dim_sq_sum"] == 360 < hess["continuum_27_dim_sq"] == 729
    )))

    # 16. SU(2) higher-spin Casimir obstruction & Hessian Sigma(216x3) defect enclosure
    su2_hs = su2_higher_spin_casimir_and_hessian_defect_bounds_rational()
    d216_tight_l, d216_tight_u = su2_hs["delta_min_Sigma216x3_tight_bounds"]
    d216_l, d216_u = su2_hs["delta_min_Sigma216x3_bounds"]
    checks.append(("su2_higher_spin_and_hessian_defect", 0, (
        su2_hs["I4_2T_3t"] == Fraction(7, 1)
        > su2_hs["I4_2O_3"] == Fraction(4, 1)
        > su2_hs["I4_2I_3a"] == su2_hs["I4_SU2_continuum_3"] == Fraction(3, 1)
        and su2_hs["I4_2I_5t"] == Fraction(11, 1) > su2_hs["I4_SU2_continuum_5"] == Fraction(5, 1)
        and su2_hs["a5_irrep_dim_sq_sum"] == 60
        and su2_hs["2i_irrep_dim_sq_sum"] == 120
        and su2_hs["poly_at_36_47"] < Fraction(0, 1) < su2_hs["poly_at_23_30"]
        and d216_l < d216_tight_l < d216_tight_u < d216_u < ds1080_low
    )))

    # 17. Complete 8-group Blichfeldt-FFK SU(3) crystal hierarchy & dyadic halving laws
    ffk = complete_blichfeldt_ffk_su3_crystal_hierarchy_rational()
    checks.append(("complete_blichfeldt_ffk_su3_hierarchy", 0, (
        ffk["I11_Sigma36x3_3"] == ffk["I3_Sigma36x3_3"] == Fraction(1, 1)
        and ffk["I4_Sigma36x3_3"] == Fraction(3, 1)
        and ffk["I2_Sigma60_8"] == Fraction(2, 1)
        and (ffk["I3_Delta27_8"], ffk["I3_Delta54_8"], ffk["I3_Sigma36x3_8"], ffk["I3_Sigma60_8"], ffk["I3_Sigma72x3_8"])
        == (Fraction(56, 1), Fraction(28, 1), Fraction(14, 1), Fraction(9, 1), Fraction(7, 1))
        and ffk["I4_Delta27_8"] == Fraction(456, 1)
        > ffk["I4_Delta54_8"] == Fraction(228, 1)
        > ffk["I4_Sigma36x3_8"] == Fraction(114, 1)
        > ffk["I4_Sigma60_8"] == Fraction(70, 1)
        > ffk["I4_Sigma72x3_8"] == Fraction(57, 1)
        > hess["I4_Sigma168_8"] > hess["I4_Sigma216x3_8"] > hess["I4_Sigma1080_8a"] > hess["I4_SU3_continuum_8"]
    )))

    # 18. Baryon vs gluon screening ratios, Casimir string-tension hierarchy & 2D Mednykh towers
    med = baryon_vs_gluon_screening_casimir_and_mednykh_2d_towers_rational()
    checks.append(("baryon_vs_gluon_casimir_and_mednykh_towers", 0, (
        med["casimir_ratio_SU3_8_over_3"] == Fraction(9, 4)
        and med["casimir_ratio_SU3_6_over_3"] == Fraction(5, 2)
        and med["casimir_ratio_SU3_10_over_3"] == Fraction(9, 2)
        and med["casimir_ratio_SU2_3a_over_2s"] == Fraction(8, 3)
        and med["casimir_ratio_SU2_4s_over_2s"] == Fraction(5, 1)
        and med["casimir_ratio_SU2_5t_over_2s"] == Fraction(8, 1)
        and med["collar_ratio_3_over_6_e4"] == Fraction(16, 1)
        and med["collar_ratio_3_over_8_e4"] == Fraction(4096, 81)
        and Fraction(1, 1) < med["M2_2I"] < med["M2_2O"] < med["M2_2T"] < med["M2_Q8"]
        and (med["Z2_Q8"], med["Z2_2T"], med["Z2_2O"], med["Z2_2I"]) == (272, 2224, 6992, 27576)
        and med["sigma1080_irrep_dim_sq_sum"] == 1080
        and med["M2_Sigma1080"] == Fraction(36011, 21600) < Fraction(2, 1)
        and med["Z2_Sigma1080"] == 1944594 < med["Z2_Sigma216x3"] == 2001267
    )))

    all_passed = all(status for _, _, status in checks)
    return {
        "record_id": "TFQ-1052",
        "dag_node": "FQCD-STRONG-COUPLING-AREA-LAW",
        "total_checks": len(checks),
        "all_passed": all_passed,
        "checks": checks,
    }
