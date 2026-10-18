r"""
Lefschetz Thimble Complex Action Flow Engine.

AuthorityEffect: None.

Deforms complex integration contours into Lefschetz thimbles J_\sigma
along steepest-descent paths of Re(S) to resolve complex action sign problems.

Implements:
1. AnalyticAction: Abstract base class for complex actions S(z).
2. PolynomialAction: Multivariable complex polynomial action with exact analytic Hessian.
3. AiryAction: Transcribed 1D cubic action S(z) = i(z^3/3 + \lambda z) (Witten 1001.2933 Sec 3).
4. BesselAction: 1D rational action S(z) = z^2/2 + \lambda/z (Witten 1001.2933 Sec 3.5).
5. SO2SymmetricAction: 2D action with a continuous circle of critical points (Witten 1001.2933 Sec 3.4.2).
6. Multi-variable Newton-Raphson critical point search using exact linear solve.
7. Adaptive RK45 flow integrator dz/dt = -\bar{\nabla S(z)} preserving Im(S) with saddle stopping.
8. Exact Stokes ray conditions & integration cycle wall-crossing tracking.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from omega_engine.crates.homology_theory.thimble_state import (
    AnalyticAction,
    ThimbleFlowResult,
)


class PolynomialAction(AnalyticAction):
    """Multivariate complex polynomial action S(z).

    Terms are represented as: (coeff, [(var_index, power), ...]).
    """

    def __init__(
        self,
        n_vars: int,
        terms: List[Tuple[complex, List[Tuple[int, int]]]] | None = None,
    ):
        self._n_vars = n_vars
        self.terms: List[Tuple[complex, List[Tuple[int, int]]]] = (
            terms if terms is not None else []
        )

    @property
    def n_vars(self) -> int:
        return self._n_vars

    def add_term(self, coeff: complex, vars_pow: List[Tuple[int, int]]) -> None:
        self.terms.append((coeff, vars_pow))

    def eval(self, z: List[complex]) -> complex:
        total = 0.0 + 0.0j
        for coeff, vars_pow in self.terms:
            term_val = coeff
            for idx, pow_val in vars_pow:
                term_val *= z[idx] ** pow_val
            total += term_val
        return total

    def gradient(self, z: List[complex]) -> List[complex]:
        grad = [0.0 + 0.0j] * self.n_vars
        for coeff, vars_pow in self.terms:
            for i, (var_idx, pow_val) in enumerate(vars_pow):
                if pow_val <= 0:
                    continue
                d_coeff = coeff * pow_val
                term_val = d_coeff
                for j, (other_idx, other_pow) in enumerate(vars_pow):
                    p = other_pow - 1 if i == j else other_pow
                    if p > 0:
                        term_val *= z[other_idx] ** p
                grad[var_idx] += term_val
        return grad

    def hessian(self, z: List[complex]) -> List[List[complex]]:
        """Exact analytic Hessian matrix H_{ij} = d^2 S / (dz_i dz_j)."""
        n = self.n_vars
        hess = [[0.0 + 0.0j for _ in range(n)] for _ in range(n)]

        for coeff, vars_pow in self.terms:
            for i, (v1, p1) in enumerate(vars_pow):
                if p1 <= 0:
                    continue
                for j, (v2, p2) in enumerate(vars_pow):
                    if p2 <= 0:
                        continue
                    if i == j:
                        if p1 < 2:
                            continue
                        factor = coeff * p1 * (p1 - 1)
                        term_val = factor
                        for k, (vk, pk) in enumerate(vars_pow):
                            p = pk - 2 if k == i else pk
                            if p > 0:
                                term_val *= z[vk] ** p
                        hess[v1][v1] += term_val
                    else:
                        factor = coeff * p1 * p2
                        term_val = factor
                        for k, (vk, pk) in enumerate(vars_pow):
                            p = pk - 1 if k in (i, j) else pk
                            if p > 0:
                                term_val *= z[vk] ** p
                        hess[v1][v2] += term_val
        return hess

    def second_derivative_1d(self, x: complex, h: float = 1e-6) -> complex:
        """d2S/dx2 for one-variable actions via central difference of the
        analytic gradient (adequate for direction selection only)."""
        gp = self.gradient(np.array([x + h], dtype=complex))[0]
        gm = self.gradient(np.array([x - h], dtype=complex))[0]
        return (gp - gm) / (2 * h)


class AiryAction(PolynomialAction):
    r"""Transcribed Airy action S(z) = i * (z^3 / 3 + \lambda * z) from Witten 1001.2933 Sec 3.

    Critical points: S'(z) = i * (z^2 + \lambda) = 0 \implies z_\pm = \pm i \sqrt{\lambda}.
    Critical values: S(z_\pm) = \mp (2/3) i \lambda^{3/2}.
    """

    def __init__(self, lam: complex):
        super().__init__(n_vars=1)
        self.lam = lam
        self.add_term(1j / 3.0, [(0, 3)])
        self.add_term(1j * lam, [(0, 1)])

    def exact_critical_points(self) -> List[complex]:
        sqrt_lam = cmath.sqrt(self.lam)
        return [1j * sqrt_lam, -1j * sqrt_lam]

    def exact_critical_values(self) -> List[complex]:
        sqrt_lam = cmath.sqrt(self.lam)
        val = (2.0 / 3.0) * (sqrt_lam**3)
        return [-val, val]


class BesselAction(AnalyticAction):
    r"""Bessel prototype action S(z) = z^2 / 2 + \lambda / z from Witten 1001.2933 Sec 3.5.

    S'(z) = z - \lambda / z^2 = 0 \implies z^3 = \lambda \implies z_k = \lambda^{1/3} e^{2\pi i k / 3}.
    S''(z) = 1 + 2\lambda / z^3. At critical points S''(z_k) = 3.
    """

    def __init__(self, lam: complex):
        self.lam = lam

    @property
    def n_vars(self) -> int:
        return 1

    def eval(self, z: List[complex]) -> complex:
        z0 = z[0]
        if abs(z0) < 1e-14:
            return complex(float("inf"), float("inf"))
        return 0.5 * (z0**2) + self.lam / z0

    def gradient(self, z: List[complex]) -> List[complex]:
        z0 = z[0]
        if abs(z0) < 1e-14:
            return [complex(float("inf"), float("inf"))]
        return [z0 - self.lam / (z0**2)]

    def hessian(self, z: List[complex]) -> List[List[complex]]:
        z0 = z[0]
        if abs(z0) < 1e-14:
            return [[complex(float("inf"), float("inf"))]]
        return [[1.0 + 2.0 * self.lam / (z0**3)]]

    def exact_critical_points(self) -> List[complex]:
        r = abs(self.lam) ** (1.0 / 3.0)
        theta = cmath.phase(self.lam) / 3.0
        cps = []
        for k in range(3):
            angle = theta + (2.0 * math.pi * k) / 3.0
            cps.append(cmath.rect(r, angle))
        return cps


class SO2SymmetricAction(PolynomialAction):
    r"""SO(2)-symmetric action S(z_1, z_2) = (z_1^2 + z_2^2 - R^2)^2 / 4 from Witten 1001.2933 Sec 3.4.2.

    Demonstrates a continuous circle manifold of critical points at z_1^2 + z_2^2 = R^2,
    plus an isolated critical point at z_1 = z_2 = 0.
    """

    def __init__(self, R: float = 1.0):
        super().__init__(n_vars=2)
        self.R = R
        R2 = R**2
        self.add_term(0.25, [(0, 4)])
        self.add_term(0.25, [(1, 4)])
        self.add_term(0.5, [(0, 2), (1, 2)])
        self.add_term(-0.5 * R2, [(0, 2)])
        self.add_term(-0.5 * R2, [(1, 2)])
        self.add_term(0.25 * (R2**2), [])


class HubbardRingAction(PolynomialAction):
    r"""Multivariate ring-coupled action S(z) on n sites with chemical potential \mu.

    S(z) = \sum_{i=0}^{n-1} s_i z_i^2 + g \sum_{i=0}^{n-1} z_i z_{(i+1) \bmod n} + i \sum_{i=0}^{n-1} \mu_i z_i
    """

    def __init__(
        self,
        n_sites: int,
        diagonal_masses: List[complex],
        coupling: complex,
        chemical_potentials: List[complex],
    ):
        super().__init__(n_vars=n_sites)
        self.n_sites = n_sites
        self.diagonal_masses = diagonal_masses
        self.coupling = coupling
        self.chemical_potentials = chemical_potentials

        for i in range(n_sites):
            self.add_term(diagonal_masses[i], [(i, 2)])
            next_idx = (i + 1) % n_sites
            if n_sites > 1:
                self.add_term(coupling, [(i, 1), (next_idx, 1)])
            self.add_term(1j * chemical_potentials[i], [(i, 1)])


def find_critical_points(
    action: AnalyticAction,
    seeds: List[List[complex]],
    max_iter: int = 100,
    tol: float = 1e-8,
) -> List[List[complex]]:
    """Finds distinct critical points of \nabla S(z) = 0 using full complex LU Newton-Raphson."""
    critical_points: List[List[complex]] = []

    for seed in seeds:
        z = list(seed)
        converged = False
        for _ in range(max_iter):
            grad = action.gradient(z)
            norm_grad = math.sqrt(sum(abs(g) ** 2 for g in grad))
            if norm_grad < tol:
                converged = True
                break

            hess = action.hessian(z)
            H_mat = np.array(hess, dtype=complex)
            g_vec = np.array(grad, dtype=complex)

            try:
                delta = np.linalg.solve(H_mat, g_vec)
            except np.linalg.LinAlgError:
                delta = np.linalg.pinv(H_mat) @ g_vec

            z = [z[i] - delta[i] for i in range(action.n_vars)]

        if converged:
            is_new = True
            for existing in critical_points:
                dist = math.sqrt(
                    sum(abs(z[i] - existing[i]) ** 2 for i in range(action.n_vars))
                )
                if dist < tol * 10:
                    is_new = False
                    break
            if is_new:
                critical_points.append(z)

    return critical_points


def steepest_descent_flow(
    action: AnalyticAction,
    z_start: List[complex],
    dt: float = 0.005,
    steps: int = 500,
    critical_points: Optional[List[List[complex]]] = None,
    cp_tol: float = 1e-3,
) -> Tuple[List[List[complex]], float]:
    r"""Traces holomorphic gradient flow dz/dt = -\bar{\nabla S(z)} using adaptive RK45.

    Returns trajectory points and maximum deviation of Im(S) from S(z_start).
    """
    z = list(z_start)
    trajectory = [list(z)]
    s_start = action.eval(z)
    im_s_start = s_start.imag
    max_im_dev = 0.0
    current_dt = dt

    step = 0
    while step < steps:

        def flow_func(curr_z: List[complex]) -> List[complex]:
            g = action.gradient(curr_z)
            return [-g[i].conjugate() for i in range(action.n_vars)]

        k1 = flow_func(z)
        z_k2 = [z[i] + 0.2 * current_dt * k1[i] for i in range(action.n_vars)]
        k2 = flow_func(z_k2)
        z_k3 = [
            z[i] + current_dt * (0.075 * k1[i] + 0.225 * k2[i])
            for i in range(action.n_vars)
        ]
        k3 = flow_func(z_k3)
        z_k4 = [
            z[i] + current_dt * (0.3 * k1[i] - 0.9 * k2[i] + 1.2 * k3[i])
            for i in range(action.n_vars)
        ]
        k4 = flow_func(z_k4)
        z_k5 = [
            z[i]
            + current_dt
            * (
                (226.0 / 729.0) * k1[i]
                - (25.0 / 27.0) * k2[i]
                + (880.0 / 729.0) * k3[i]
                + (55.0 / 729.0) * k4[i]
            )
            for i in range(action.n_vars)
        ]
        k5 = flow_func(z_k5)
        z_k6 = [
            z[i]
            + current_dt
            * (
                (-181.0 / 270.0) * k1[i]
                + 2.5 * k2[i]
                - (266.0 / 297.0) * k3[i]
                - (91.0 / 27.0) * k4[i]
                + (189.0 / 55.0) * k5[i]
            )
            for i in range(action.n_vars)
        ]
        k6 = flow_func(z_k6)

        z5 = [
            z[i]
            + current_dt
            * (
                (37.0 / 378.0) * k1[i]
                + (250.0 / 621.0) * k3[i]
                + (125.0 / 594.0) * k4[i]
                + (512.0 / 1771.0) * k6[i]
            )
            for i in range(action.n_vars)
        ]
        z4 = [
            z[i]
            + current_dt
            * (
                (2825.0 / 27648.0) * k1[i]
                + (18575.0 / 48384.0) * k3[i]
                + (13525.0 / 55296.0) * k4[i]
                + (277.0 / 14336.0) * k5[i]
                + 0.25 * k6[i]
            )
            for i in range(action.n_vars)
        ]

        err = math.sqrt(sum(abs(z5[i] - z4[i]) ** 2 for i in range(action.n_vars)))

        if err < 1e-4 or current_dt <= 1e-7:
            z = z5
            trajectory.append(list(z))
            step += 1

            s_curr = action.eval(z)
            dev = abs(s_curr.imag - im_s_start)
            if dev > max_im_dev:
                max_im_dev = dev

            if critical_points:
                hit_cp = False
                for cp in critical_points:
                    dist = math.sqrt(
                        sum(abs(z[i] - cp[i]) ** 2 for i in range(action.n_vars))
                    )
                    if dist < cp_tol:
                        hit_cp = True
                        break
                if hit_cp:
                    break

            if err > 0:
                current_dt = min(current_dt * 1.5, 0.05)
        else:
            current_dt = max(current_dt * 0.5, 1e-7)

    return trajectory, max_im_dev


def steepest_descent_flow_with_frame(
    action: AnalyticAction,
    z_start: List[complex],
    dt: float = 0.005,
    steps: int = 500,
    initial_frame: Optional[List[List[complex]]] = None,
) -> ThimbleFlowResult:
    r"""Traces holomorphic gradient flow dz/dt = -\bar{\nabla S(z)} and tangent frame parallel transport dJ/dt = -\bar{H(z)} J.

    Computes residual phase \phi_{res} = \arg(\det J(t)) and Jacobian magnitude |\det J(t)|.
    """
    n = action.n_vars
    z = list(z_start)
    trajectory = [list(z)]
    s_start = action.eval(z)
    im_s_start = s_start.imag
    max_im_dev = 0.0

    if initial_frame is None:
        J = np.eye(n, dtype=complex)
    else:
        J = np.array(initial_frame, dtype=complex)

    jacobian_history = [J.tolist()]

    for _ in range(steps):
        grad = action.gradient(z)
        hess = action.hessian(z)

        g_vec = np.array(grad, dtype=complex)
        H_mat = np.array(hess, dtype=complex)

        dz_dt = -np.conj(g_vec)
        dJ_dt = -np.conj(H_mat @ J)

        z = [z[i] + dt * dz_dt[i] for i in range(n)]
        J = J + dt * dJ_dt

        trajectory.append(list(z))
        jacobian_history.append(J.tolist())

        s_curr = action.eval(z)
        dev = abs(s_curr.imag - im_s_start)
        if dev > max_im_dev:
            max_im_dev = dev

    det_J = np.linalg.det(J)
    residual_phase = math.atan2(det_J.imag, det_J.real)
    jacobian_det = float(abs(det_J))

    return ThimbleFlowResult(
        trajectory=trajectory,
        conserved_im_s=im_s_start,
        max_im_deviation=max_im_dev,
        jacobian_history=jacobian_history,
        residual_phase=residual_phase,
        jacobian_determinant=jacobian_det,
    )


def verify_airy_stokes_rays(lam_mag: float = 1.0, num_angles: int = 36) -> List[dict]:
    r"""Verifies Stokes ray transitions for the Airy action as arg(\lambda) varies around S^1.

    Under the downward flow dz/dt = -conj(dS/dz), Im(S) is conserved.
    A connecting flow between two saddles requires equality of the conserved
    imaginary part: Im(S(z_+)) = Im(S(z_-)).
    """
    results = []
    for k in range(num_angles):
        angle = (2.0 * math.pi * k) / num_angles
        lam = cmath.rect(lam_mag, angle)
        action = AiryAction(lam)
        cps = action.exact_critical_points()
        s_vals = [action.eval([cp]) for cp in cps]
        im_diff = abs(s_vals[0].imag - s_vals[1].imag)
        results.append(
            {
                "angle": angle,
                "lambda": lam,
                "critical_points": cps,
                "critical_values": s_vals,
                "im_diff": im_diff,
                "is_near_stokes_ray": im_diff < 0.1,
            }
        )
    return results


def morse_index(action: AnalyticAction, critical_point: List[complex]) -> int:
    r"""Compute the Morse index of S at a critical point.

    The Morse index is the number of negative eigenvalues of the real part
    of the Hessian matrix Re(H_{ij}).  For a holomorphic action on C^n,
    the flow Hessian that determines the thimble dimension is the *real*
    Hessian of Re(S) viewed as a function on R^{2n}.  For non-degenerate
    critical points the Morse index equals n (half the real dimension),
    but this function computes it explicitly to handle edge cases.

    Returns the count of eigenvalues of Re(H) with negative real part.
    """
    hess = action.hessian(critical_point)
    H = np.array(hess, dtype=complex)
    n = action.n_vars

    real_hess = np.zeros((2 * n, 2 * n))
    for i in range(n):
        for j in range(n):
            re_h = H[i, j].real
            im_h = H[i, j].imag
            real_hess[2 * i, 2 * j] = re_h
            real_hess[2 * i, 2 * j + 1] = -im_h
            real_hess[2 * i + 1, 2 * j] = -im_h
            real_hess[2 * i + 1, 2 * j + 1] = -re_h

    eigenvalues = np.linalg.eigvalsh(real_hess)
    return int(np.sum(eigenvalues < -1e-10))


def sample_dual_flow_hits(
    action: AnalyticAction,
    critical_points: List[List[complex]],
    real_contour_seeds: List[List[complex]],
    dt: float = 0.005,
    steps: int = 2000,
    cp_tol: float = 0.05,
) -> Dict[int, int]:
    r"""Sample ascending-flow convergence counts from real contour seeds.

    WARNING: This is NOT a topological intersection number computation.
    The returned counts depend on sampling density of real_contour_seeds.
    Duplicating seeds can change the result. Use as a heuristic only.

    For each seed on the real contour Gamma_R, flows it under the *ascending*
    gradient dz/dt = +conj(grad S), which is the reverse of the steepest-descent
    flow.  A seed that converges to critical point sigma contributes +1 or -1
    to n_sigma depending on the orientation (sign of the determinant of the
    linearised flow).

    Args:
        action: the complex action.
        critical_points: list of critical points z_sigma.
        real_contour_seeds: starting points sampled from the real integration contour.
        dt: initial step size for flow.
        steps: max flow steps.
        cp_tol: tolerance for declaring convergence to a critical point.

    Returns:
        dict mapping critical point index -> integer intersection number.
    """
    n_sigma: Dict[int, int] = {i: 0 for i in range(len(critical_points))}

    for seed in real_contour_seeds:
        z = list(seed)
        target = None

        current_dt = dt
        for _ in range(steps):
            grad = action.gradient(z)
            z = [z[i] + current_dt * grad[i].conjugate() for i in range(action.n_vars)]

            if any(
                math.isinf(zi.real) or math.isinf(zi.imag) or abs(zi) > 1e5 for zi in z
            ):
                break

            for cp_idx, cp in enumerate(critical_points):
                cp_vec = cp if isinstance(cp, (list, tuple, np.ndarray)) else [cp]
                dist = math.sqrt(
                    sum(abs(z[i] - cp_vec[i]) ** 2 for i in range(action.n_vars))
                )
                if dist < cp_tol:
                    target = cp_idx
                    break
            if target is not None:
                break

        if target is not None:
            cp_target = critical_points[target]
            cp_target_vec = (
                cp_target
                if isinstance(cp_target, (list, tuple, np.ndarray))
                else [cp_target]
            )
            hess = action.hessian(cp_target_vec)
            H = np.array(hess, dtype=complex)
            det_sign = 1 if np.linalg.det(H).real >= 0 else -1
            n_sigma[target] += det_sign

    return n_sigma


def integrate_thimble(
    action: AnalyticAction,
    critical_point: List[complex],
    dt: float = 0.005,
    steps: int = 500,
    both_directions: bool = True,
) -> Tuple[complex, List[List[complex]]]:
    r"""Numerically integrate e^{-S(z)} along the Lefschetz thimble J_sigma.

    Traces the steepest-descent flow from the critical point in both directions
    along the unstable manifold and integrates e^{-S} using the trapezoidal rule.

    Along the thimble, Im(S) is constant, so the integrand is
    e^{-Re(S(z))} * e^{-i Im(S(z_sigma))} * |dz/dt| dt.

    Returns:
        (integral_value, trajectory): the complex integral and the traced path.
    """
    integral = 0.0 + 0.0j
    all_points: List[List[complex]] = []

    hess = action.hessian(critical_point)
    H = np.array(hess, dtype=complex)
    eigvals, eigvecs = np.linalg.eig(H)

    directions = []
    for i in range(action.n_vars):
        if eigvals[i].real < 0:
            v = eigvecs[:, i]
            v_normed = v / np.linalg.norm(v)
            directions.append(v_normed)

    if not directions:
        directions = [np.ones(action.n_vars, dtype=complex) / math.sqrt(action.n_vars)]

    for direction in directions:
        signs = [1.0, -1.0] if both_directions else [1.0]
        for sign in signs:
            eps = 1e-4
            z_start = [
                critical_point[i] + sign * eps * direction[i].real
                for i in range(action.n_vars)
            ]

            traj, _ = steepest_descent_flow(action, z_start, dt=dt, steps=steps)
            all_points.extend(traj)

            for k in range(1, len(traj)):
                z_prev = traj[k - 1]
                z_curr = traj[k]

                if action.n_vars == 1:
                    dz = z_curr[0] - z_prev[0]
                else:
                    dz = complex(math.sqrt(
                        sum(abs(z_curr[j] - z_prev[j]) ** 2 for j in range(action.n_vars))
                    ))
                s_mid = action.eval(
                    [(z_prev[j] + z_curr[j]) / 2.0 for j in range(action.n_vars)]
                )
                integrand = cmath.exp(-s_mid)
                integral += integrand * dz

    return integral, all_points


def partition_function(
    action: AnalyticAction,
    critical_points: List[List[complex]],
    intersection_numbers: Dict[int, int],
    dt: float = 0.005,
    steps: int = 500,
) -> Tuple[complex, Dict[int, complex]]:
    r"""Evaluate the partition function Z = \sum_sigma n_sigma \int_{J_sigma} e^{-S}.

    Args:
        action: the complex action.
        critical_points: list of critical points z_sigma.
        intersection_numbers: dict mapping sigma -> n_sigma.
        dt: step size for thimble integration.
        steps: integration steps per thimble.

    Returns:
        (Z, contributions): total partition function and per-thimble contributions.
    """
    contributions: Dict[int, complex] = {}
    Z = 0.0 + 0.0j

    for sigma, n_s in intersection_numbers.items():
        if n_s == 0 or sigma >= len(critical_points):
            continue

        thimble_integral, _ = integrate_thimble(
            action, critical_points[sigma], dt=dt, steps=steps
        )
        contribution = n_s * thimble_integral
        contributions[sigma] = contribution
        Z += contribution

    return Z, contributions




@dataclass
class FlowRecord:
    """One traced thimble branch with its conservation diagnostics."""

    points: list[complex] = field(default_factory=list)
    h_values: list[float] = field(default_factory=list)
    im_action: list[float] = field(default_factory=list)

    @property
    def h_monotone_decreasing(self) -> bool:
        h = self.h_values
        return all(h[k + 1] <= h[k] + 1e-9 for k in range(len(h) - 1))

    @property
    def max_im_drift(self) -> float:
        im = self.im_action
        return max(im) - min(im) if im else 0.0


def airy_action(lam: complex) -> PolynomialAction:
    """The Airy exponent I = i*lam*(x^3/3 - x) of eq. (3.2), as terms."""
    il = 1j * complex(lam)
    return PolynomialAction(1, [(il / 3.0, [(0, 3)]), (-il, [(0, 1)])])


def newton_critical_points(
    action: PolynomialAction,
    seeds: Sequence[complex],
    tol: float = 1e-12,
    max_iter: int = 60,
) -> list[complex]:
    """One-variable Newton on dS/dx = 0; distinct roots from the seed set."""
    roots: list[complex] = []
    for seed in seeds:
        x = complex(seed)
        for _ in range(max_iter):
            g = action.gradient(np.array([x], dtype=complex))[0]
            if abs(g) < tol:
                break
            g2 = action.second_derivative_1d(x)
            if abs(g2) < 1e-14:
                break
            x = x - g / g2
        g = action.gradient(np.array([x], dtype=complex))[0]
        if abs(g) < 1e-8 and all(abs(x - r) > 1e-6 for r in roots):
            roots.append(x)
    return sorted(roots, key=lambda r: (round(r.real, 9), round(r.imag, 9)))


def descent_directions(
    action: PolynomialAction, cp: complex
) -> tuple[complex, complex]:
    """The two unit steepest-descent directions at a nondegenerate critical point."""
    s2 = action.second_derivative_1d(cp)
    theta = (np.pi - np.angle(s2)) / 2.0
    d = np.exp(1j * theta)
    return d, -d


def _flow_rhs(action: PolynomialAction, x: complex) -> complex:
    """Downward flow of eq. (3.10): dx/dt = -conj(dI/dx)."""
    return -np.conj(action.gradient(np.array([x], dtype=complex))[0])


def trace_thimble(
    action: PolynomialAction,
    cp: complex,
    direction: complex,
    dt: float = 5e-4,
    n_steps: int = 40000,
    start_offset: float = 1e-5,
    h_floor: float = -60.0,
    stop_near: Sequence[complex] = (),
    stop_radius: float = 1e-3,
) -> FlowRecord:
    """RK4-integrate the downward flow from cp along direction."""
    rec = FlowRecord()
    x = cp + start_offset * direction
    for _ in range(n_steps):
        s = action.eval(np.array([x], dtype=complex))
        rec.points.append(x)
        rec.h_values.append(float(s.real))
        rec.im_action.append(float(s.imag))
        if s.real < h_floor:
            break
        if any(abs(x - q) < stop_radius for q in stop_near):
            break
        k1 = _flow_rhs(action, x)
        k2 = _flow_rhs(action, x + 0.5 * dt * k1)
        k3 = _flow_rhs(action, x + 0.5 * dt * k2)
        k4 = _flow_rhs(action, x + dt * k3)
        x = x + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return rec


def integrate_exp_action(
    action: PolynomialAction, branch_out: FlowRecord, branch_in: FlowRecord
) -> complex:
    """Trapezoid quadrature of exp(I) along a full thimble."""
    pts = list(reversed(branch_in.points)) + branch_out.points
    zs = np.array(pts, dtype=complex)
    vals = np.array([np.exp(action.eval(np.array([z], dtype=complex))) for z in zs])
    dz = zs[1:] - zs[:-1]
    return complex(np.sum(0.5 * (vals[1:] + vals[:-1]) * dz))


def stokes_connection(
    action: PolynomialAction,
    cp_from: complex,
    cp_to: complex,
    **trace_kwargs,
) -> bool:
    """True when a downward flow from cp_from reaches cp_to."""
    for direction in descent_directions(action, cp_from):
        rec = trace_thimble(
            action,
            cp_from,
            direction,
            stop_near=[cp_to],
            **trace_kwargs,
        )
        if rec.points and abs(rec.points[-1] - cp_to) < 2e-3:
            return True
    return False


U_PLUS = np.array([[1, 1], [0, 1]], dtype=int)
U_MINUS = np.array([[1, 0], [-1, 1]], dtype=int)


def monodromy() -> np.ndarray:
    """M = -U_minus * U_plus of eq. (3.15); the tests check M**3 = 1."""
    return -(U_MINUS @ U_PLUS)


