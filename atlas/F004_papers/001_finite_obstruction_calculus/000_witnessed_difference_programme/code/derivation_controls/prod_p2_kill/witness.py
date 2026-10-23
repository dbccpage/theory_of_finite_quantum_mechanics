"""Executable witness for PROD-P2-KILL (Evaluate P2 kill conditions: G.5 pass share, failure-list use)."""

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

from omega_engine_applications.wdp_products.p2_provenance_gate.adapter import (  # noqa: E402
    WdpOutputGate,
    evaluate_pilot_p2_kill_conditions,
    valid_candidate_record,
)


def witness() -> dict[str, object]:
    res = evaluate_pilot_p2_kill_conditions()
    if res["any_kill_condition_holds"]:
        raise RuntimeError("expected no P2 kill conditions to hold on the pilot batch")
    return res


def refuse_empty_claim_id() -> None:
    gate = WdpOutputGate()
    res = gate.gate("", valid_candidate_record())
    if hasattr(res, "code"):
        raise ValueError(f"{res.code}: {res.reason}")
