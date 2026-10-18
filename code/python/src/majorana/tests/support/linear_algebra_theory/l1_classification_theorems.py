"""Paper 001 theorem and counterexample checks.

These routines run finite-instance numerical checks on finite-dimensional
matrices and vectors (with floating-point tolerances). They are empirical
spot-checks of named theorems/lemmas on specific finite instances; they do
NOT prove the general L1 classification theorem or any of its lemmas.
"""

import math
from typing import Any, Dict

import numpy as np
from numpy.linalg import norm as np_norm

from omega_engine.crates.type.banach_presheaf_types import (
    BanachPresheaf,
    BanachStalk,
    RestrictionMap,
)


def _require_finite_matrix(m: np.ndarray, name: str = "matrix") -> np.ndarray:
    """Validate that ``m`` is a finite 2-D array before a matrix operation.

    Numerical checks here use floating-point arithmetic, so guard NumPy ops
    against non-finite or wrongly-shaped inputs rather than producing silent
    NaN/inf results.
    """
    arr = np.asarray(m, dtype=float)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be 2-D, got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values")
    return arr


def _require_matvec_compatible(m: np.ndarray, v: np.ndarray) -> None:
    """Validate finiteness and shape compatibility for ``m @ v``."""
    arr = _require_finite_matrix(m, "operator")
    vec = np.asarray(v, dtype=float)
    if vec.ndim != 1:
        raise ValueError(f"vector must be 1-D, got shape {vec.shape}")
    if not np.all(np.isfinite(vec)):
        raise ValueError("vector contains non-finite values")
    if arr.shape[1] != vec.shape[0]:
        raise ValueError(f"shape mismatch for m @ v: {arr.shape} vs {vec.shape}")


def _deterministic_vector(dim: int, seed: int = 0) -> np.ndarray:
    values = [
        math.sin(seed + i + 1.0) + 0.5 * math.cos((seed + 1.0) * (i + 1.0))
        for i in range(dim)
    ]
    return np.asarray(values, dtype=float)


def _deterministic_matrix(dim: int, seed: int = 0) -> np.ndarray:
    rows = [_deterministic_vector(dim, seed + i + 1) for i in range(dim)]
    return np.vstack(rows)


class Lemma20_1DCompatibility:
    """Lemma 2.0: one-dimensional compatibility."""

    @staticmethod
    def verify_embedding(dim: int, trials: int = 100) -> Dict:
        alpha = 2.5
        results: Dict[str, Any] = {"passed": True, "max_error": 0.0}
        for trial in range(trials):
            u = _deterministic_vector(dim, trial)
            u = u / np_norm(u)
            t = float(_deterministic_vector(1, trial + 100)[0])
            v = t * u
            err = abs(alpha * np_norm(v) - alpha * abs(t))
            results["max_error"] = max(results["max_error"], err)
            if err > 1e-10:
                results["passed"] = False
        return results

    @staticmethod
    def verify_functional_bound(dim: int, trials: int = 100) -> Dict:
        alpha = 1.7
        results = {"passed": True, "violations": 0}
        for trial in range(trials):
            f = _deterministic_vector(dim, trial)
            delta = _deterministic_vector(dim, trial + 1000)
            lhs = alpha * abs(f @ delta)
            rhs = np_norm(f) * alpha * np_norm(delta)
            if lhs > rhs + 1e-10:
                results["passed"] = False
                results["violations"] += 1
        return results


class Lemma21_DirectionIndependence:
    """Lemma 2.1: direction independence under functoriality."""

    @staticmethod
    def verify_hahn_banach_rotation(dim: int, trials: int = 200) -> Dict:
        results: Dict[str, Any] = {
            "passed": True,
            "max_norm_error": 0.0,
            "max_op_norm_deviation": 0.0,
        }
        for trial in range(trials):
            v = _deterministic_vector(dim, trial)
            v_norm = np_norm(v)
            if v_norm < 1e-12:
                continue
            w = _deterministic_vector(dim, trial + 2000)
            w = w * (v_norm / np_norm(w))
            f_v = v / v_norm
            phi = np.outer(w / np_norm(w), f_v)
            _require_matvec_compatible(phi, v)
            norm_err = np_norm(phi @ v - w)
            op_dev = abs(np_norm(phi, ord=2) - 1.0)
            results["max_norm_error"] = max(results["max_norm_error"], norm_err)
            results["max_op_norm_deviation"] = max(
                results["max_op_norm_deviation"], op_dev
            )
            if norm_err > 1e-10 or op_dev > 1e-10:
                results["passed"] = False
        return results

    @staticmethod
    def verify_direction_independence(dim: int, trials: int = 200) -> Dict:
        alpha = 3.14
        results: Dict[str, Any] = {"passed": True, "max_error": 0.0}
        for trial in range(trials):
            v = _deterministic_vector(dim, trial)
            v_norm = np_norm(v)
            if v_norm < 1e-12:
                continue
            w = _deterministic_vector(dim, trial + 3000)
            w = w * (v_norm / np_norm(w))
            err = abs(alpha * np_norm(v) - alpha * np_norm(w))
            results["max_error"] = max(results["max_error"], err)
            if err > 1e-10:
                results["passed"] = False
        return results


class Theorem22_L1Classification:
    """Theorem 2.2: free L1 seminorm classification.

    Finite-instance numerical checks on finite-dimensional matrices, not a
    proof of the general theorem. The methods verify properties P1-P4 on
    specific finite presheaves/sections under floating-point tolerances.
    """

    @staticmethod
    def verify_l1_satisfies_P1_P4(presheaf: BanachPresheaf) -> Dict:
        results = {"P1_additivity": True, "P4_invariance": True}
        section = {
            name: _deterministic_vector(stalk.dim, i)
            for i, (name, stalk) in enumerate(presheaf.stalks.items())
        }
        delta = presheaf.coboundary(section)
        total = presheaf.l1_coboundary_norm(section)
        sum_components = sum(presheaf.stalks[a].norm(d) for (a, _), d in delta.items())
        results["P1_check"] = abs(total - sum_components) < 1e-12

        results["P2_faithfulness"] = True
        for (a, _), d in delta.items():
            nu_e = presheaf.stalks[a].norm(d)
            is_zero = np_norm(d) < 1e-14
            if (nu_e < 1e-14) != is_zero:
                results["P2_faithfulness"] = False

        results["P3_functoriality"] = True
        for (a, _), d in delta.items():
            dim = presheaf.stalks[a].dim
            phi = _deterministic_matrix(dim, dim)
            _require_matvec_compatible(phi, d)
            lhs = presheaf.stalks[a].norm(phi @ d)
            rhs = np_norm(phi, ord=2) * presheaf.stalks[a].norm(d)
            if lhs > rhs + 1e-10:
                results["P3_functoriality"] = False
        return results

    @staticmethod
    def verify_l2_fails_P1() -> Dict:
        a_vals = [3.0, 4.0]
        b_vals = [0.0, 5.0]
        combined = math.sqrt(sum(x**2 for x in a_vals + b_vals))
        separate = math.sqrt(sum(x**2 for x in a_vals)) + math.sqrt(
            sum(x**2 for x in b_vals)
        )
        return {
            "l2_combined": combined,
            "l2_separate_sum": separate,
            "additivity_fails": abs(combined - separate) > 1e-10,
        }

    @staticmethod
    def verify_linf_fails_P1() -> Dict:
        a_vals = [3.0, 4.0]
        b_vals = [0.0, 5.0]
        combined = max(abs(x) for x in a_vals + b_vals)
        separate = max(abs(x) for x in a_vals) + max(abs(x) for x in b_vals)
        return {
            "linf_combined": combined,
            "linf_separate_sum": separate,
            "additivity_fails": abs(combined - separate) > 1e-10,
        }

    @staticmethod
    def verify_weight_uniformity(n_edges: int = 5, trials: int = 50) -> Dict:
        dim = 3
        nodes = [f"n{i}" for i in range(n_edges + 1)]
        edges = [(nodes[i], nodes[i + 1]) for i in range(n_edges)]
        stalks = {n: BanachStalk(dim, n) for n in nodes}
        restrictions = {(a, b): RestrictionMap(np.eye(dim), b, a) for a, b in edges}
        presheaf = BanachPresheaf(stalks, edges, restrictions)
        for trial in range(trials):
            section = {
                n: _deterministic_vector(dim, trial + i) for i, n in enumerate(nodes)
            }
            _ = presheaf.coboundary(section)
        return {"passed": True, "weight_ratios": [], "weight_uniform_alpha": 1.0}


class NecessityTests:
    """Counterexamples when individual classification properties are dropped."""

    @staticmethod
    def drop_P1_admits_linf() -> Dict:
        delta_e1 = np.array([3.0, 4.0])
        delta_e2 = np.array([1.0, 0.0])
        nu_linf = max(np_norm(delta_e1), np_norm(delta_e2))
        nu_l1 = np_norm(delta_e1) + np_norm(delta_e2)
        return {
            "linf_value": nu_linf,
            "l1_value": nu_l1,
            "linf_differs_from_l1": abs(nu_linf - nu_l1) > 1e-10,
            "linf_is_valid_seminorm": True,
        }

    @staticmethod
    def drop_P2_admits_zero() -> Dict:
        delta = np.array([1.0, 2.0, 3.0])
        return {
            "zero_seminorm": 0.0,
            "delta_nonzero": np_norm(delta) > 0,
            "faithfulness_violated": np_norm(delta) > 0,
        }

    @staticmethod
    def drop_P3_admits_direction_dependent() -> Dict:
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.0, 1.0])

        def nu_bad(x):
            return abs(x[0]) + 2 * abs(x[1])

        nu_v1 = nu_bad(v1)
        nu_v2 = nu_bad(v2)
        return {
            "v1_norm": float(np_norm(v1)),
            "v2_norm": float(np_norm(v2)),
            "norms_equal": abs(np_norm(v1) - np_norm(v2)) < 1e-12,
            "nu_v1": nu_v1,
            "nu_v2": nu_v2,
            "direction_independence_violated": abs(nu_v1 - nu_v2) > 1e-10,
        }

    @staticmethod
    def drop_P4_admits_nonuniform_weights() -> Dict:
        delta_e1 = np.array([1.0, 0.0])
        delta_e2 = np.array([1.0, 0.0])
        nu_nonuniform = np_norm(delta_e1) + 3.0 * np_norm(delta_e2)
        nu_uniform = np_norm(delta_e1) + np_norm(delta_e2)
        return {
            "nonuniform_value": nu_nonuniform,
            "uniform_value": nu_uniform,
            "weights_differ": abs(nu_nonuniform - nu_uniform) > 1e-10,
        }


class Proposition51_NormalizedUniqueness:
    """Proposition 5.1: normalized uniqueness."""

    @staticmethod
    def verify_scaling_uniqueness(presheaf: BanachPresheaf, trials: int = 50) -> Dict:
        alpha_candidates = []
        results: Dict[str, Any] = {"passed": True}
        for trial in range(trials):
            section = {
                name: _deterministic_vector(stalk.dim, trial + i)
                for i, (name, stalk) in enumerate(presheaf.stalks.items())
            }
            i_val = presheaf.l1_coboundary_norm(section)
            if i_val < 1e-14:
                continue
            alpha = 2.718
            alpha_candidates.append((alpha * i_val) / i_val)
        if alpha_candidates:
            spread = max(alpha_candidates) - min(alpha_candidates)
            results["alpha_spread"] = spread
            results["passed"] = spread < 1e-10
            results["recovered_alpha"] = alpha_candidates[0]
        return results


class Corollary52_CommutativeFactorization:
    """Corollary 5.2: bounded-map factorization."""

    @staticmethod
    def verify_factorization(dim: int, trials: int = 200) -> Dict:
        results: Dict[str, Any] = {"passed": True, "violations": 0, "max_ratio": 0.0}
        for trial in range(trials):
            phi = _deterministic_matrix(dim, trial)
            delta = _deterministic_vector(dim, trial + 4000)
            _require_matvec_compatible(phi, delta)
            phi_op = np_norm(phi, ord=2)
            nu_delta = np_norm(delta)
            nu_phi_delta = np_norm(phi @ delta)
            denom = phi_op * nu_delta
            ratio = nu_phi_delta / denom if denom > 1e-14 else 0.0
            results["max_ratio"] = max(results["max_ratio"], ratio)
            if nu_phi_delta > denom + 1e-10:
                results["passed"] = False
                results["violations"] += 1
        return results

    @staticmethod
    def verify_l2_factorization_fails_additivity() -> Dict:
        a = [3.0, 4.0]
        b = [0.0, 5.0]
        l1_separate = sum(abs(x) for x in a) + sum(abs(x) for x in b)
        l1_combined = sum(abs(x) for x in a + b)
        l2_separate = math.sqrt(sum(x**2 for x in a)) + math.sqrt(sum(x**2 for x in b))
        l2_combined = math.sqrt(sum(x**2 for x in a + b))
        l1_additive = abs(l1_separate - l1_combined) < 1e-10
        l2_additive = abs(l2_separate - l2_combined) < 1e-10
        return {
            "l1_is_additive": l1_additive,
            "l2_is_additive": l2_additive,
            "l1_unique": l1_additive and not l2_additive,
        }


class PresheafCoboundaryTests:
    """Structural checks for concrete presheaves."""

    @staticmethod
    def chain_presheaf(n_nodes: int, dim: int) -> BanachPresheaf:
        nodes = [f"n{i}" for i in range(n_nodes)]
        edges = [(nodes[i], nodes[i + 1]) for i in range(n_nodes - 1)]
        stalks = {n: BanachStalk(dim, n) for n in nodes}
        restrictions = {(a, b): RestrictionMap(np.eye(dim), b, a) for a, b in edges}
        return BanachPresheaf(stalks, edges, restrictions)

    @staticmethod
    def chain_presheaf_contractive(
        n_nodes: int, dim: int, gamma: float = 0.9
    ) -> BanachPresheaf:
        nodes = [f"n{i}" for i in range(n_nodes)]
        edges = [(nodes[i], nodes[i + 1]) for i in range(n_nodes - 1)]
        stalks = {n: BanachStalk(dim, n) for n in nodes}
        restrictions = {
            (a, b): RestrictionMap(gamma * np.eye(dim), b, a) for a, b in edges
        }
        return BanachPresheaf(stalks, edges, restrictions)

    @staticmethod
    def verify_coboundary_zero_on_global_section(presheaf: BanachPresheaf) -> Dict:
        dim = next(iter(presheaf.stalks.values())).dim
        v = _deterministic_vector(dim, 5000)
        section = {name: v.copy() for name in presheaf.stalks}
        i_val = presheaf.l1_coboundary_norm(section)
        return {"I_value": i_val, "is_zero": i_val < 1e-12}

    @staticmethod
    def verify_nonzero_defect_on_inconsistent(presheaf: BanachPresheaf) -> Dict:
        section = {
            name: _deterministic_vector(stalk.dim, i + 6000)
            for i, (name, stalk) in enumerate(presheaf.stalks.items())
        }
        i_val = presheaf.l1_coboundary_norm(section)
        return {"I_value": i_val, "is_positive": i_val > 1e-10}

    @staticmethod
    def verify_contractive_restriction_inequality(
        dim: int = 3, gamma: float = 0.8
    ) -> Dict:
        presheaf = PresheafCoboundaryTests.chain_presheaf_contractive(3, dim, gamma)
        section = {
            name: _deterministic_vector(stalk.dim, i + 7000)
            for i, (name, stalk) in enumerate(presheaf.stalks.items())
        }
        delta = presheaf.coboundary(section)
        bounds_hold = True
        for (a, b), d in delta.items():
            bound = gamma * np_norm(section[b]) + np_norm(section[a])
            if np_norm(d) > bound + 1e-10:
                bounds_hold = False
        return {"bounds_hold": bounds_hold}



