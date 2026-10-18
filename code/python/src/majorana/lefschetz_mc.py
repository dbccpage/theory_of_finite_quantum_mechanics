from __future__ import annotations
r"""
Lefschetz Thimble Monte Carlo (LTMC) Sampler.

AuthorityEffect: None.

Performs Monte Carlo sampling on Lefschetz thimbles J_\sigma using local chart parameterization,
weighting by e^{-\operatorname{Re} S(z)} |\det J|, and reweighting by residual phase e^{i \phi_{\text{res}}}.

Implements:
1. ThimbleMetropolisSampler: 1D and multi-D thimble Metropolis sampling.
2. AiryIntegralEstimator: Reconstructs the Airy integral Z(\lambda) = \sum n_\sigma \int_{J_\sigma} e^{-S(z)} dz.
"""


import cmath
import math
import random
from typing import Any, Callable, Dict, List, Tuple

import numpy as np

from omega_engine.crates.homology_theory.lefschetz_thimble import (
    AiryAction,
    AnalyticAction,
    steepest_descent_flow_with_frame,
)
from omega_engine.crates.homology_theory.thimble_state import IntegrationCycle, ThimbleFlowResult


class ThimbleMetropolisSampler:
    """Metropolis-Hastings sampler on Lefschetz thimbles with residual phase reweighting."""

    def __init__(self, action: AnalyticAction, seed: int = 42):
        self.action = action
        self.rng = random.Random(seed)

    def sample_1d_thimble(
        self,
        cp: List[complex],
        unstable_dir: List[complex],
        flow_time: float = 0.5,
        n_samples: int = 10000,
        step_size: float = 0.2,
        t_max: float = 3.0,
    ) -> Tuple[List[complex], float, float]:
        r"""Samples points on a 1-D thimble parameterized by \tau \in [-t_max, t_max] along unstable_dir.

        Returns:
            samples: list of complex points z(\tau) on the thimble.
            acceptance_rate: fraction of accepted Metropolis steps.
            partition_weight: estimated \int_{J_\sigma} e^{-S(z)} dz.
        """
        tau = 0.0
        samples: List[complex] = []
        accepted = 0

        def get_point_and_weight(tau_val: float) -> Tuple[complex, float, float]:
            z_init = [cp[i] + tau_val * unstable_dir[i] for i in range(self.action.n_vars)]
            flow_res = steepest_descent_flow_with_frame(
                self.action, z_init, dt=0.01, steps=int(flow_time / 0.01)
            )
            z_end = flow_res.trajectory[-1][0]
            s_val = self.action.eval([z_end])
            weight = math.exp(-s_val.real) * flow_res.jacobian_determinant
            phase = flow_res.residual_phase
            return z_end, weight, phase

        curr_z, curr_w, curr_phi = get_point_and_weight(tau)

        phase_sum = 0.0 + 0.0j

        for _ in range(n_samples):
            tau_prop = tau + self.rng.uniform(-step_size, step_size)
            if abs(tau_prop) > t_max:
                samples.append(curr_z)
                phase_sum += cmath.exp(1j * curr_phi)
                continue

            prop_z, prop_w, prop_phi = get_point_and_weight(tau_prop)

            ratio = prop_w / curr_w if curr_w > 0 else 1.0
            if self.rng.random() < ratio:
                tau = tau_prop
                curr_z, curr_w, curr_phi = prop_z, prop_w, prop_phi
                accepted += 1

            samples.append(curr_z)
            phase_sum += cmath.exp(1j * curr_phi)

        acc_rate = accepted / n_samples
        partition_weight = (phase_sum / n_samples).real
        return samples, acc_rate, partition_weight


def estimate_airy_integral(lam: complex, n_samples: int = 5000) -> complex:
    r"""Estimates the Airy integral Z(\lambda) = \int_{\mathbb{R}} e^{-i(z^3/3 + \lambda z)} dz

    by deforming the contour onto the relevant Lefschetz thimble(s).
    """
    action = AiryAction(lam)
    cps = action.exact_critical_points()
    sampler = ThimbleMetropolisSampler(action)

    total_z = 0.0 + 0.0j

    for cp in cps:
        dir_v = [1.0 + 0.0j]
        _, _, p_weight = sampler.sample_1d_thimble(
            cp=[cp], unstable_dir=dir_v, flow_time=0.2, n_samples=n_samples
        )
        s_cp = action.eval([cp])
        total_z += cmath.exp(-s_cp) * p_weight

    return total_z


class TemperedLefschetzThimbleSampler:
    r"""Tempered Lefschetz Thimble Method (TLTM) sampler.

    Runs parallel replicas along a flow time ladder 0 = t_0 < t_1 < ... < t_A = T.
    Allows Metropolis chains to tunnel between thimbles at t=0 (where action barriers are low)
    while measuring observables at target flow time t=T (where the sign problem is mild).
    """

    def __init__(
        self,
        action: AnalyticAction,
        flow_times: List[float] | None = None,
        seed: int = 42,
    ):
        self.action = action
        self.flow_times = flow_times if flow_times is not None else [0.0, 0.05, 0.1, 0.15, 0.2]
        self.n_replicas = len(self.flow_times)
        self.rng = random.Random(seed)

    def _evaluate_state(self, x: List[float], t: float) -> Tuple[List[complex], float, float]:
        """Flows real configuration x for flow time t and computes weight and residual phase."""
        z_init = [complex(xi, 0.0) for xi in x]
        if t <= 1e-7:
            s_val = self.action.eval(z_init)
            weight = math.exp(-s_val.real)
            return z_init, weight, 0.0

        steps = max(5, int(t / 0.01))
        dt = t / steps
        flow_res = steepest_descent_flow_with_frame(self.action, z_init, dt=dt, steps=steps)
        z_final = flow_res.trajectory[-1]
        s_val = self.action.eval(z_final)
        weight = math.exp(-s_val.real) * flow_res.jacobian_determinant
        return z_final, weight, flow_res.residual_phase

    def sample(
        self,
        n_samples: int = 2000,
        step_size: float = 0.2,
        swap_interval: int = 5,
    ) -> Dict[str, Any]:
        """Runs parallel-tempered Metropolis sampling across flow-time replicas.

        Returns dict containing:
            target_samples: samples at flow time T
            target_phases: residual phases at flow time T
            swap_acceptance: fraction of accepted replica swaps
            reweighted_integral: estimate of Z on the target surface
        """
        n_vars = self.action.n_vars
        replicas_x = [[self.rng.uniform(-1.0, 1.0) for _ in range(n_vars)] for _ in range(self.n_replicas)]

        target_samples: List[List[complex]] = []
        target_phases: List[float] = []

        total_swaps_proposed = 0
        total_swaps_accepted = 0

        for step in range(n_samples):
            for alpha in range(self.n_replicas):
                t_alpha = self.flow_times[alpha]
                x_curr = replicas_x[alpha]
                _, w_curr, _ = self._evaluate_state(x_curr, t_alpha)

                x_prop = [x_curr[i] + self.rng.uniform(-step_size, step_size) for i in range(n_vars)]
                _, w_prop, _ = self._evaluate_state(x_prop, t_alpha)

                ratio = w_prop / w_curr if w_curr > 0 else 1.0
                if self.rng.random() < ratio:
                    replicas_x[alpha] = x_prop

            if step > 0 and step % swap_interval == 0:
                alpha = self.rng.randint(0, self.n_replicas - 2)
                t_a, t_b = self.flow_times[alpha], self.flow_times[alpha + 1]
                x_a, x_b = replicas_x[alpha], replicas_x[alpha + 1]

                _, w_a_ta, _ = self._evaluate_state(x_a, t_a)
                _, w_b_tb, _ = self._evaluate_state(x_b, t_b)
                _, w_a_tb, _ = self._evaluate_state(x_a, t_b)
                _, w_b_ta, _ = self._evaluate_state(x_b, t_a)

                swap_ratio = (w_b_ta * w_a_tb) / (w_a_ta * w_b_tb) if (w_a_ta * w_b_tb) > 0 else 1.0
                total_swaps_proposed += 1
                if self.rng.random() < swap_ratio:
                    replicas_x[alpha], replicas_x[alpha + 1] = x_b, x_a
                    total_swaps_accepted += 1

            z_target, _, phi_target = self._evaluate_state(replicas_x[-1], self.flow_times[-1])
            target_samples.append(z_target)
            target_phases.append(phi_target)

        phase_reweight = sum(cmath.exp(1j * phi) for phi in target_phases) / n_samples
        swap_acc = total_swaps_accepted / total_swaps_proposed if total_swaps_proposed > 0 else 0.0

        return {
            "target_samples": target_samples,
            "target_phases": target_phases,
            "swap_acceptance": swap_acc,
            "reweighted_integral": phase_reweight.real,
        }




