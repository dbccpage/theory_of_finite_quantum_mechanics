r"""
Chern-Simons Character-Variety Action & Knot Invariants.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.quantum_physics.chern_simons
"""

from __future__ import annotations
import cmath
import math
from typing import List, Tuple

from omega_engine.crates.homology_theory.thimble_state import AnalyticAction

# Hyperbolic volume of figure-eight knot 4_1 (exact to 12 decimal places)
FIGURE_EIGHT_VOLUME = 2.029883212819


class FigureEightCharacterVariety:
    r"""SL(2, C) character variety (A-polynomial) for the figure-eight knot 4_1."""

    @staticmethod
    def eval_A(m: complex, l: complex) -> complex:
        if abs(m) < 1e-14 or abs(l) < 1e-14:
            return complex(float("inf"), float("inf"))
        term_m = (m**4) - (m**2) - 2.0 - (1.0 / (m**2)) + (1.0 / (m**4))
        term_l = l + (1.0 / l)
        return term_l - term_m

    @staticmethod
    def cs_value(branch: str) -> complex:
        """Returns complex CS invariant value for named flat connection branch."""
        if branch == "abelian":
            return 0.0 + 0.0j
        elif branch == "non_abelian_plus":
            return 1j * (FIGURE_EIGHT_VOLUME / (2.0 * math.pi))
        elif branch == "non_abelian_minus":
            return -1j * (FIGURE_EIGHT_VOLUME / (2.0 * math.pi))
        else:
            raise ValueError(f"Unknown branch {branch}")

    @staticmethod
    def non_abelian_flat_connections() -> List[Tuple[complex, complex]]:
        """Returns (m, l) pairs for non-abelian flat connections on 4_1."""
        m1 = cmath.exp(1j * math.pi / 6.0)
        m2 = cmath.exp(-1j * math.pi / 6.0)
        l1 = complex(-2.0 + math.sqrt(3.0), 0.0)
        l2 = complex(-2.0 - math.sqrt(3.0), 0.0)
        return [(m1, l1), (m2, l2)]


class TrefoilCharacterVariety:
    r"""SL(2, C) character variety for the trefoil knot 3_1."""

    @staticmethod
    def eval_A(m: complex, l: complex) -> complex:
        return l + (m**6)

    @staticmethod
    def cs_value(k: int) -> complex:
        """CS value for branch k in {1, 5}."""
        return complex((k**2) / 6.0, 0.0)


class ChernSimonsKnotAction(AnalyticAction):
    r"""AnalyticAction defined on (m, l) space whose critical points lie on the character variety A(m, l) = 0."""

    def __init__(self, variety_type: str = "figure_eight"):
        self.variety_type = variety_type

    @property
    def n_vars(self) -> int:
        return 2

    def _eval_A_and_derivs(self, m: complex, l: complex) -> tuple:
        """Returns (A, dA/dm, dA/dl, d2A/dm2, d2A/dmdl, d2A/dl2)."""
        if self.variety_type == "figure_eight":
            if abs(m) < 1e-14 or abs(l) < 1e-14:
                inf = complex(float("inf"), float("inf"))
                return inf, inf, inf, inf, inf, inf
            A = (l + 1.0 / l) - (m**4 - m**2 - 2.0 - 1.0 / m**2 + 1.0 / m**4)
            dA_dm = -(4.0 * m**3 - 2.0 * m + 2.0 / m**3 - 4.0 / m**5)
            dA_dl = 1.0 - 1.0 / l**2
            d2A_dm2 = -(12.0 * m**2 - 2.0 - 6.0 / m**4 + 20.0 / m**6)
            d2A_dmdl = 0.0 + 0.0j
            d2A_dl2 = 2.0 / l**3
        else:
            A = l + m**6
            dA_dm = 6.0 * m**5
            dA_dl = 1.0 + 0.0j
            d2A_dm2 = 30.0 * m**4
            d2A_dmdl = 0.0 + 0.0j
            d2A_dl2 = 0.0 + 0.0j
        return A, dA_dm, dA_dl, d2A_dm2, d2A_dmdl, d2A_dl2

    def eval(self, z: List[complex]) -> complex:
        m, l = z[0], z[1]
        A, *_ = self._eval_A_and_derivs(m, l)
        return 0.5 * (A * A.conjugate())

    def gradient(self, z: List[complex]) -> List[complex]:
        m, l = z[0], z[1]
        A, dA_dm, dA_dl, *_ = self._eval_A_and_derivs(m, l)
        grad_m = (A * dA_dm.conjugate()).real
        grad_l = (A * dA_dl.conjugate()).real
        return [grad_m, grad_l]

    def hessian(self, z: List[complex]) -> List[List[complex]]:
        h = 1e-7
        g0 = self.gradient(z)
        hess = [[0.0 + 0.0j for _ in range(2)] for _ in range(2)]
        for j in range(2):
            z_shifted = list(z)
            z_shifted[j] += h
            gj = self.gradient(z_shifted)
            for i in range(2):
                hess[i][j] = (gj[i] - g0[i]) / h
        return hess


class AnalyticContinuationCS(AnalyticAction):
    r"""Chern-Simons action with analytically continued level t = k + i*s."""

    def __init__(self, base_action: AnalyticAction, t: complex):
        self.base_action = base_action
        self.t = t

    @property
    def n_vars(self) -> int:
        return self.base_action.n_vars

    def eval(self, z: List[complex]) -> complex:
        return self.t * self.base_action.eval(z)

    def gradient(self, z: List[complex]) -> List[complex]:
        g = self.base_action.gradient(z)
        return [self.t * gi for gi in g]

    def hessian(self, z: List[complex]) -> List[List[complex]]:
        h = self.base_action.hessian(z)
        return [[self.t * h[i][j] for j in range(self.n_vars)] for i in range(self.n_vars)]

    def stokes_wall_crossing_scan(
        self,
        t_mag: float,
        num_angles: int = 72,
    ) -> List[dict]:
        from omega_engine.crates.homology_theory.lefschetz_thimble import find_critical_points

        results = []
        for k in range(num_angles):
            angle = (2.0 * math.pi * k) / num_angles
            t_val = cmath.rect(t_mag, angle)
            self.t = t_val

            if hasattr(self.base_action, "exact_critical_points"):
                cps_raw = self.base_action.exact_critical_points()
                cps = [[cp] if not isinstance(cp, list) else cp for cp in cps_raw]
            else:
                seeds = [[cmath.rect(1.0, 2.0 * math.pi * j / 8) + 0.0j] for j in range(8)]
                if self.n_vars > 1:
                    seeds = [
                        [cmath.rect(0.5, 2 * math.pi * j / 6) for _ in range(self.n_vars)]
                        for j in range(6)
                    ]
                cps = find_critical_points(self, seeds)

            s_vals = [self.eval(cp) for cp in cps]

            re_diffs = []
            for i in range(len(s_vals)):
                for j in range(i + 1, len(s_vals)):
                    re_diffs.append(abs(s_vals[i].real - s_vals[j].real))

            min_re_diff = min(re_diffs) if re_diffs else float("inf")

            results.append({
                "angle": angle,
                "t": t_val,
                "critical_points": cps,
                "critical_values": s_vals,
                "min_re_diff": min_re_diff,
                "is_near_stokes_wall": min_re_diff < 0.1,
            })

        return results


def knot_vanishing_cycle_intersection_matrix(knot_type: str = "figure_eight") -> List[List[int]]:
    r"""Returns the exact vanishing cycle intersection matrix M_{ij} = <\delta_i, \delta_j> for knot character varieties."""
    if knot_type == "figure_eight":
        return [
            [0, 1, -1],
            [-1, 0, 2],
            [1, -2, 0],
        ]
    elif knot_type == "trefoil":
        return [
            [0, 1],
            [-1, 0],
        ]
    else:
        raise ValueError(f"Unknown knot type {knot_type}")


__all__ = [
    "FIGURE_EIGHT_VOLUME",
    "FigureEightCharacterVariety",
    "TrefoilCharacterVariety",
    "ChernSimonsKnotAction",
    "AnalyticContinuationCS",
    "knot_vanishing_cycle_intersection_matrix",
]



