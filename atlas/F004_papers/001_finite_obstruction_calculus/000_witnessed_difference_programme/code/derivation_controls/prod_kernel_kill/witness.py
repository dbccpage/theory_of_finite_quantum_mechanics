"""Executable witness for PROD-KERNEL-KILL (Evaluate kernel kill conditions on a pilot workflow)."""

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

from omega_engine_applications.wdp_products.kernel.adapter import (  # noqa: E402
    evaluate_pilot_kernel_kill_conditions,
    pilot_agent_loop_certificate,
)


def witness() -> dict[str, object]:
    res = evaluate_pilot_kernel_kill_conditions()
    if any(res[name] is None for name in (
        "kill_no_finite_arena", "kill_receipts_unreplayed", "any_kill_condition_holds",
    )):
        raise RuntimeError("WDP_NATIVE_CHECK_UNAVAILABLE: pilot kill conditions are undecided")
    if res["any_kill_condition_holds"]:
        raise RuntimeError("expected no kernel kill conditions to hold on the pilot workflow")
    return {
        "goal_id": str(res["goal_id"]),
        "task_id": str(res["task_id"]),
        "usable_budget": str(res["usable_budget"]),
        "initial_value": str(res["initial_value"]),
        "kill_no_finite_arena": bool(res["kill_no_finite_arena"]),
        "kill_receipts_unreplayed": bool(res["kill_receipts_unreplayed"]),
        "any_kill_condition_holds": bool(res["any_kill_condition_holds"]),
        "authority_effect": str(res["authority_effect"]),
    }


def refuse_tampered_pilot_certificate() -> None:
    bad_cert = copy.deepcopy(pilot_agent_loop_certificate())
    bad_cert["task_id"] = "tampered"
    res = evaluate_pilot_kernel_kill_conditions(certificate=bad_cert)
    if res["kill_no_finite_arena"] is None:
        raise RuntimeError("WDP_NATIVE_CHECK_UNAVAILABLE: tampered certificate was not checked")
    if res["kill_no_finite_arena"]:
        raise ValueError("kill_no_finite_arena: tampered certificate rejected by checker")
