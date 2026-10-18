from __future__ import annotations
r"""
Airy Lefschetz Thimble demo — geometry + residual phase + minimal Monte Carlo.
Matches Witten 1001.2933 §3 (Airy function as the prototype for Stokes / thimbles).

AuthorityEffect: None.
"""


import cmath
import math
import random
from typing import List, Tuple

from omega_engine.crates.homology_theory.lefschetz_thimble import (
    AiryAction,
    steepest_descent_flow,
    steepest_descent_flow_with_frame,
)


def residual_orientation(action: AiryAction, traj: List[List[complex]]) -> complex:
    """Track continuous argument of the velocity along the flow."""
    phase = 0.0
    for i in range(1, len(traj)):
        dz = traj[i][0] - traj[i - 1][0]
        if abs(dz) < 1e-14:
            continue
        g = action.gradient(traj[i - 1])
        v = -g[0].conjugate()
        phase += cmath.phase(v / (traj[i][0] - traj[i - 1][0] + 1e-30))
    return cmath.exp(1j * phase)


def stokes_scan(lam_mag: float = 1.0, n_angles: int = 24) -> List[Tuple[float, complex, float]]:
    """Scan angles for near-Stokes ray conditions where Re(S(z_+)) == Re(S(z_-))."""
    rays = []
    for k in range(n_angles):
        theta = 2 * math.pi * k / n_angles
        lam = cmath.rect(lam_mag, theta)
        a = AiryAction(lam)
        cps = a.exact_critical_points()
        s_p, s_m = a.eval([cps[0]]), a.eval([cps[1]])
        re_diff = abs(s_p.real - s_m.real)
        if re_diff < 0.15:
            rays.append((theta, lam, re_diff))
    return rays


def thimble_metropolis(
    action: AiryAction,
    z_crit: complex,
    n_samples: int = 2000,
    dt_prop: float = 0.05,
    flow_steps: int = 40,
    seed: int = 42,
) -> Tuple[List[complex], float]:
    """Simple 1-D Metropolis on the downward thimble of z_crit."""
    rng = random.Random(seed)
    z = [z_crit + 0.02]
    traj, _ = steepest_descent_flow(action, z, dt=0.01, steps=flow_steps)
    z = traj[-1]

    samples = []
    accepts = 0
    for _ in range(n_samples):
        z_prop = [z[0] + (rng.gauss(0, dt_prop) + 0j)]
        traj_p, _ = steepest_descent_flow(action, z_prop, dt=0.01, steps=8)
        z_new = traj_p[-1]

        d_re = action.eval(z_new).real - action.eval(z).real
        if d_re < 0 or rng.random() < math.exp(-d_re):
            z = z_new
            accepts += 1
        samples.append(z[0])

    return samples, accepts / n_samples


def tempered_airy_demo(lam: complex, t_short: float = 0.2, t_long: float = 1.5) -> Tuple[float, float, float]:
    """Parallel-tempering ratio sketch between short and long flow times."""
    a = AiryAction(lam)
    cps = a.exact_critical_points()

    def flow_for_time(z0: complex, t_target: float, dt: float = 0.01) -> complex:
        steps = max(1, int(t_target / dt))
        traj, _ = steepest_descent_flow(a, [z0], dt=dt, steps=steps)
        return traj[-1][0]

    rep_short = flow_for_time(cps[0] + 0.05, t_short)
    rep_long = flow_for_time(cps[1] + 0.05, t_long)

    s_short = a.eval([rep_short]).real
    s_long = a.eval([rep_long]).real
    log_alpha = -(s_long - s_short)
    return s_short, s_long, log_alpha


def run_airy_demo() -> dict:
    """Runs full demo suite and returns validation metrics."""
    lam = 1.0 + 0.0j
    action = AiryAction(lam)

    cps = action.exact_critical_points()
    H = action.hessian([0.5 + 0.3j])

    z0 = [cps[0] + 0.08 + 0.03j]
    traj, max_im_dev = steepest_descent_flow(action, z0, dt=0.003, steps=300)
    ori = residual_orientation(action, traj)
    rays = stokes_scan()
    samples, acc = thimble_metropolis(action, cps[0])
    s_short, s_long, log_alpha = tempered_airy_demo(lam)

    return {
        "critical_points": cps,
        "hessian_at_test": H[0][0],
        "max_im_dev": max_im_dev,
        "residual_orientation": ori,
        "stokes_rays": rays,
        "metropolis_acceptance": acc,
        "tempered_log_alpha": log_alpha,
    }


def airy_residual_phase_jacobian_transporter(lam: complex = 1.0 + 0.0j, steps: int = 100) -> Tuple[complex, complex]:
    r"""Jacobian frame transporter along Airy thimbles dz/dt = -\bar{\nabla S(z)}.

    Transports tangent frame e_t = d\Phi/dt with d\Phi/dt = -\bar{H(z) \Phi}
    and computes the residual orientation phases e^{i\theta_+} and e^{i\theta_-}.
    """
    action = AiryAction(lam)
    cps = action.exact_critical_points()

    phases = []
    for cp in cps:
        H_cp = action.hessian([cp])[0][0]
        v_unstable = cmath.sqrt(-H_cp.conjugate()) if abs(H_cp) > 0 else 1.0 + 0.0j
        if abs(v_unstable) == 0:
            v_unstable = 1.0 + 0.0j
        v_unstable /= abs(v_unstable)

        flow_res = steepest_descent_flow_with_frame(
            action, [cp + 0.01 * v_unstable], dt=0.01, steps=steps, initial_frame=[[v_unstable]]
        )
        phase = cmath.exp(1j * flow_res.residual_phase)
        phases.append(phase)

    return phases[0], phases[1]



def build_airy_fukaya_seidel_demo(lam: complex = 1.0 + 0.0j) -> dict:
    """Builds the local Fukaya-Seidel category FS(Airy) with frame-transported residual phases."""
    from omega_engine.crates.homology_theory.hms_fukaya_seidel import build_airy_fukaya_seidel_category

    ph_plus, ph_minus = airy_residual_phase_jacobian_transporter(lam)
    fs = build_airy_fukaya_seidel_category(lam=lam, residual_phase=ph_plus)
    return {
        "fukaya_seidel_category": fs,
        "phase_plus": ph_plus,
        "phase_minus": ph_minus,
        "morphisms": fs.category.get_hom("J_+", "J_-"),
    }


if __name__ == "__main__":
    res = run_airy_demo()
    print("Airy Lefschetz Thimble Demo Results:")
    print(f"  Critical points: {res['critical_points']}")
    print(f"  Analytic Hessian: {res['hessian_at_test']}")
    print(f"  Max |Δ Im(S)|: {res['max_im_dev']:.2e}")
    print(f"  Residual orientation: {res['residual_orientation']}")
    print(f"  Metropolis acceptance: {res['metropolis_acceptance']:.2f}")
    print(f"  Tempered swap log-α: {res['tempered_log_alpha']:.4f}")




