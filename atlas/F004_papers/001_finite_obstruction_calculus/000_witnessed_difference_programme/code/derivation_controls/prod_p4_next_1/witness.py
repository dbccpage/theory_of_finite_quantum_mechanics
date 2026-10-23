"""Executable witness for PROD-P4-NEXT-1 (WdpObservationPlanner over finite_observation.solve and verify)."""

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

from omega_engine_applications.wdp_products.p4_observation_budget.adapter import (  # noqa: E402
    WdpObservationPlanner,
)
from omega_engine_applications.wdp_products.p4_observation_budget.contracts import (  # noqa: E402
    CompletionTarget,
    Instrument,
    SuiteVerdict,
)


def witness() -> dict[str, object]:
    outcome_map = {
        "I_all_expensive": {"s0": "0", "s1": "1", "s2": "2"},
        "I_pair01": {"s0": "0", "s1": "1", "s2": "1"},
        "I_pair12": {"s0": "0", "s1": "0", "s2": "1"},
    }
    planner = WdpObservationPlanner(outcome_map)
    instruments = (
        Instrument(instrument_id="I_all_expensive", price="5"),
        Instrument(instrument_id="I_pair01", price="3/2"),
        Instrument(instrument_id="I_pair12", price="2"),
    )
    target = CompletionTarget(
        kind="raw",
        pairs_to_separate=(("s0", "s1"), ("s1", "s2"), ("s0", "s2")),
    )

    verdict = planner.plan(instruments, target)
    if not isinstance(verdict, SuiteVerdict) or not verdict.feasible:
        raise RuntimeError("expected feasible SuiteVerdict")
    if not planner.verify(instruments, target, verdict):
        raise RuntimeError("expected planner.verify to accept optimal verdict")

    infeasible_planner = WdpObservationPlanner(
        {"I_partial": {"s0": "0", "s1": "1", "s2": "1"}}
    )
    infeasible_verdict = infeasible_planner.plan(
        (Instrument(instrument_id="I_partial", price="1"),),
        target,
    )
    if not isinstance(infeasible_verdict, SuiteVerdict) or infeasible_verdict.feasible:
        raise RuntimeError("expected infeasible SuiteVerdict")

    return {
        "goal_id": "PROD-P4-NEXT-1",
        "feasible_suite": list(verdict.suite),
        "feasible_cost": verdict.cost,
        "verified_optimal": planner.verify(instruments, target, verdict),
        "infeasible_unresolved_pairs": [list(p) for p in infeasible_verdict.unresolved_pairs],
        "authority_effect": verdict.authority_effect,
    }


def refuse_suboptimal_suite_verdict() -> None:
    outcome_map = {
        "I_all_expensive": {"s0": "0", "s1": "1", "s2": "2"},
        "I_pair01": {"s0": "0", "s1": "1", "s2": "1"},
        "I_pair12": {"s0": "0", "s1": "0", "s2": "1"},
    }
    planner = WdpObservationPlanner(outcome_map)
    instruments = (
        Instrument(instrument_id="I_all_expensive", price="5"),
        Instrument(instrument_id="I_pair01", price="3/2"),
        Instrument(instrument_id="I_pair12", price="2"),
    )
    target = CompletionTarget(
        kind="raw",
        pairs_to_separate=(("s0", "s1"), ("s1", "s2"), ("s0", "s2")),
    )
    suboptimal = SuiteVerdict(
        feasible=True,
        suite=("I_all_expensive",),
        cost="5",
        unresolved_pairs=(),
    )
    if not planner.verify(instruments, target, suboptimal):
        raise ValueError("suboptimal suite rejected by independent verifier")
