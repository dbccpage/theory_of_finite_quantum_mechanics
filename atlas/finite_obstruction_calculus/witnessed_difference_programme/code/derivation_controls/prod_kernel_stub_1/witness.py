"""Executable witness for PROD-KERNEL-STUB-1 (WdpCertificateChecker parity)."""

from __future__ import annotations

import copy
import sys
from pathlib import Path


def _ensure_paths() -> Path:
    here = Path(__file__).resolve()
    repo_root = next((p for p in here.parents if (p / ".git").exists()), None)
    if repo_root is None:
        raise FileNotFoundError("repository root not found")
    for candidate in (
        repo_root,
        repo_root
        / "omega_engine_atlas"
        / "coda_atlas"
        / "papers"
        / "finite_obstruction_calculus"
        / "witnessed_difference_programme"
        / "code",
    ):
        s = str(candidate)
        if s not in sys.path:
            sys.path.insert(0, s)
    return repo_root


_ensure_paths()

from certified_progress.checker import check_certificate  # noqa: E402
from certified_progress.fixtures import cheaper_route  # noqa: E402
from certified_progress.model import graph_model  # noqa: E402
from certified_progress.producer import solve_progress  # noqa: E402
from omega_engine_applications.wdp_products.kernel.adapter import (  # noqa: E402
    WdpCertificateChecker,
)


def witness() -> dict[str, object]:
    checker = WdpCertificateChecker()

    model = cheaper_route()
    optimal_cert = solve_progress(model)["certificate"]
    opt_receipt = checker.check(model, optimal_cert)
    ref_opt = check_certificate(model, optimal_cert)
    if not opt_receipt.accepted or opt_receipt.claim != "WIN_OPTIMAL" or opt_receipt.initial_value != "2":
        raise RuntimeError("optimal WIN_OPTIMAL check failed")
    if opt_receipt.model_digest != ref_opt["model_digest"]:
        raise RuntimeError("model_digest mismatch against check_certificate")

    feasible_cert = copy.deepcopy(optimal_cert)
    feasible_cert["kind"] = "WIN_FEASIBLE"
    feasible_cert["optimality_requested"] = False
    feasible_cert["strategy"] = [
        {"belief": ["s"], "action": "direct"},
        {"belief": ["u"], "action": "finish"},
    ]
    feasible_cert["ranks"] = [
        {"belief": ["s"], "rank": 1},
        {"belief": ["t"], "rank": 0},
        {"belief": ["u"], "rank": 1},
    ]
    feasible_cert["values"] = [
        {"belief": ["s"], "value": "5"},
        {"belief": ["t"], "value": "0"},
        {"belief": ["u"], "value": "1"},
    ]
    feas_receipt = checker.check(model, feasible_cert)
    if not feas_receipt.accepted or feas_receipt.claim != "WIN_FEASIBLE" or feas_receipt.initial_value != "5":
        raise RuntimeError("checker failed to preserve suboptimal WIN_FEASIBLE value 5")

    forged_optimal = copy.deepcopy(feasible_cert)
    forged_optimal["kind"] = "WIN_OPTIMAL"
    forged_optimal["optimality_requested"] = True
    forged_receipt = checker.check(model, forged_optimal)
    if forged_receipt.accepted or forged_receipt.claim is not None:
        raise RuntimeError("checker failed to reject forged WIN_OPTIMAL certificate")

    stalled_model = graph_model({"s": []}, targets=("t",))
    stalled_cert = solve_progress(stalled_model)["certificate"]
    stalled_receipt = checker.check(stalled_model, stalled_cert)

    trapped_model = graph_model({"s": [("go", "1", ["d"])]}, targets=("t",))
    trapped_cert = solve_progress(trapped_model)["certificate"]
    trapped_receipt = checker.check(trapped_model, trapped_cert)

    return {
        "goal_id": "PROD-KERNEL-STUB-1",
        "optimal_claim": opt_receipt.claim,
        "optimal_initial_value": opt_receipt.initial_value,
        "feasible_claim": feas_receipt.claim,
        "feasible_initial_value": feas_receipt.initial_value,
        "forged_accepted": forged_receipt.accepted,
        "forged_failures": forged_receipt.failures,
        "stalled_initial_stalled": stalled_receipt.initial_stalled,
        "trapped_initial_stalled": trapped_receipt.initial_stalled,
        "authority_effect": opt_receipt.authority_effect,
    }


def refuse_producer_substitution(substitute_solver_answer: bool = True) -> None:
    if substitute_solver_answer:
        raise ValueError("CertificateChecker never calls the producer or substitutes its own answer")
