"""Executable witness for PROD-P1-KILL (Evaluate P1 kill conditions on pilot arenas)."""

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

from omega_engine_applications.wdp_products.p1_abstention_governor.adapter import (  # noqa: E402
    evaluate_pilot_p1_kill_conditions,
    operator_decision_for_label,
)


def witness() -> dict[str, object]:
    res = evaluate_pilot_p1_kill_conditions()
    if res["any_kill_condition_holds"]:
        raise RuntimeError("expected no P1 kill conditions to hold on the pilot arenas")
    return res


def refuse_invalid_termination_label() -> None:
    operator_decision_for_label("NotALabel")  # type: ignore[arg-type]
