#!/usr/bin/env python3
"""Reproduce small-chain review observations; sampled estimates are uncertified."""

import argparse
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import numpy as np
import scipy
import caqd
from caqd.adaptive import QuantumCluster, _cluster_residual_rates


def observations():
    times = np.linspace(0, 0.4, 9)
    rows = []
    for model_name, n, observable in [("TFIM", 4, "C_mid"), ("XXZ", 4, "M_stag"), ("TFIM", 6, "C_mid")]:
        if model_name == "TFIM":
            model, rho0 = caqd.TFIMChain(n, J=1, h=1), caqd.polarized_x_state(n)
        else:
            model, rho0 = caqd.XXZChain(n, J=1, delta=1, h=0.2), caqd.neel_state(n)
        obs = {observable: caqd.center_correlation(n) if observable == "C_mid" else caqd.staggered_magnetization(n)}
        exact = caqd.evolve_exact(model, rho0, times, obs)
        for method in ["mean_field", "adaptive"]:
            result = (caqd.evolve_mean_field(model, rho0, times, obs) if method == "mean_field"
                      else caqd.evolve_adaptive(model, rho0, obs, times, tol=0.1,
                                                max_bond=4, refine_threshold=0.03))
            comparison = caqd.verify_bound_honesty(exact, result, obs)[observable]
            rows.append({
                "model": model_name, "N": n, "observable": observable, "method": method,
                "max_reference_error": float(comparison.true_errors.max()),
                "final_sampled_estimate": float(comparison.certified_bounds[-1]),
                "min_sampled_margin": comparison.min_margin,
                "sampled_margin_nonnegative": comparison.is_honest,
                "final_clusters": result.metadata.get("final_clusters"),
                "estimated_target_met": result.metadata.get("estimated_target_met"),
            })
    model, rho = caqd.TFIMChain(2), caqd.all_up_state(2)
    obs = {"ZZ": caqd.center_correlation(2)}
    result = caqd.evolve_adaptive(model, rho, obs, [0, 0.2], max_bond=1)
    exact = caqd.evolve_exact(model, rho, [0, 0.2], obs)
    bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
    boundary_model = caqd.SpinChainModel(3)
    h = np.kron(caqd.pauli_matrices()["Z"], caqd.pauli_matrices()["Z"])
    from caqd.spin_chains import LocalTerm
    boundary_model.terms.append(LocalTerm("2-local", (1, 2), h, np.kron(np.eye(2), h)))
    clusters = [QuantumCluster([0, 1], np.outer(bell, bell)), QuantumCluster([2], np.eye(2) / 2)]
    _, marginal_rate = caqd.compute_edge_residual(np.eye(2) / 2, np.eye(2) / 2, h)
    return {
        "certificate_status": "HEURISTIC_UNCERTIFIED",
        "configuration": {"times": times.tolist(), "adaptive_tol": 0.1,
                          "cluster_ceiling_qubits": 4, "refine_threshold": 0.03,
                          "TFIM": {"J": 1, "h": 1, "initial": "polarized_x"},
                          "XXZ": {"J": 1, "delta": 1, "h": 0.2, "initial": "neel"},
                          "periodic": False},
        "rows": rows,
        "counterexamples": {
            "two_qubit_final_rate": float(result.total_rates[-1]),
            "two_qubit_final_sampled_estimate": float(caqd.compute_cumulative_bounds(result, 1)[-1]),
            "two_qubit_reference_ZZ_error": float(abs(exact.expectation("ZZ")[-1] - result.expectation("ZZ")[-1])),
            "bell_boundary_site_marginal_rate": marginal_rate,
            "bell_boundary_full_cluster_rate": _cluster_residual_rates(boundary_model, clusters)[(1, 2)],
        },
    }


def close_records(actual, stored):
    """Numerical replay with stated tolerance; environment labels are historical."""
    if isinstance(actual, dict):
        return actual.keys() == stored.keys() and all(close_records(v, stored[k]) for k, v in actual.items())
    if isinstance(actual, list):
        return len(actual) == len(stored) and all(close_records(a, b) for a, b in zip(actual, stored))
    if isinstance(actual, float):
        return bool(np.isclose(actual, stored, rtol=1e-10, atol=1e-12))
    return actual == stored


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Replace the committed review observations")
    parser.add_argument("--check", action="store_true", help="Compare a fresh replay with the committed observations")
    args = parser.parse_args()
    report = observations()
    destination = ROOT / "review_observations.json"
    if args.write:
        report["recorded_environment"] = {"python": platform.python_version(), "numpy": np.__version__,
                                          "scipy": scipy.__version__, "caqd": caqd.__version__}
        destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {destination.name}: {len(report['rows'])} numerical reference comparisons")
    elif args.check:
        stored = json.loads(destination.read_text(encoding="utf-8"))
        stored.pop("recorded_environment")
        if not close_records(report, stored):
            raise SystemExit("FAIL: numerical review observations changed")
        print("OK: review observations reproduced (rtol=1e-10, atol=1e-12); no numerical certificate")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
