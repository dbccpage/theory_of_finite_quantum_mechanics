"""Executable witness for PROD-P3-KILL (Evaluate P3 kill conditions on pilot workloads)."""

from __future__ import annotations

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
        / "F004_papers"
        / "001_finite_obstruction_calculus"
        / "000_witnessed_difference_programme"
        / "code",
    ):
        s = str(candidate)
        if s not in sys.path:
            sys.path.insert(0, s)
    return repo_root


_ensure_paths()

from antibody_transfer.replay_examples import example_input  # noqa: E402
from omega_engine_applications.wdp_products.p3_guard_transfer.adapter import (  # noqa: E402
    WdpGuardTransferChecker,
    evaluate_pilot_p3_kill_conditions,
    make_source_guard_rule,
)


def witness() -> dict[str, object]:
    res = evaluate_pilot_p3_kill_conditions()
    if res["any_kill_condition_holds"]:
        raise RuntimeError("expected no P3 kill conditions to hold on the pilot workload")
    return res


def refuse_unsafe_point_transfer() -> None:
    checker = WdpGuardTransferChecker()
    tp = example_input()["transfer"]
    unsafe_rule = make_source_guard_rule("unsafe-point", tp["source"])
    res = checker.transfer(unsafe_rule, tp)
    if hasattr(res, "code"):
        raise ValueError(f"{res.code}: {res.reason}")
