"""Executable witness for PROD-P4-KILL (Evaluate P4 kill conditions on pilot instrument menus)."""

from __future__ import annotations

import sys
from fractions import Fraction
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

from finite_observation import replay_examples as fo_examples  # noqa: E402
from omega_engine_applications.wdp_products.p4_observation_budget.adapter import (  # noqa: E402
    WdpObservationPlanner,
)
from omega_engine_applications.wdp_products.p4_observation_budget.contracts import (  # noqa: E402
    CompletionTarget,
    Instrument,
    SuiteVerdict,
)


def witness() -> dict[str, object]:
    bundle = fo_examples.build_bundle()
    summary = fo_examples.replay_bundle(bundle)

    outcome_map = {
        "I_buyer_monolithic": {"s0": "0", "s1": "1", "s2": "2"},
        "I_pair01": {"s0": "0", "s1": "1", "s2": "1"},
        "I_pair12": {"s0": "0", "s1": "0", "s2": "1"},
    }
    instruments = (
        Instrument(instrument_id="I_buyer_monolithic", price="5"),
        Instrument(instrument_id="I_pair01", price="3/2"),
        Instrument(instrument_id="I_pair12", price="2"),
    )
    target = CompletionTarget(
        kind="raw",
        pairs_to_separate=(("s0", "s1"), ("s1", "s2"), ("s0", "s2")),
    )
    buyer_baseline_suite = ("I_buyer_monolithic",)
    buyer_baseline_cost = Fraction(5)

    planner = WdpObservationPlanner(outcome_map)
    verdict = planner.plan(instruments, target)
    if not isinstance(verdict, SuiteVerdict) or not verdict.feasible:
        raise RuntimeError("expected feasible SuiteVerdict on pilot menu")
    verified = planner.verify(instruments, target, verdict)
    planned_cost = Fraction(verdict.cost)

    kill_exceeds_solver = not (verdict.feasible and verified and len(summary) == 5)
    kill_never_differs = verdict.suite == buyer_baseline_suite or planned_cost >= buyer_baseline_cost
    any_kill = kill_exceeds_solver or kill_never_differs
    if any_kill:
        raise RuntimeError("expected no P4 kill condition to hold on pilot menus")

    return {
        "goal_id": "PROD-P4-KILL",
        "replay_fixture_count": len(summary),
        "planned_suite": list(verdict.suite),
        "planned_cost": str(planned_cost),
        "buyer_baseline_cost": str(buyer_baseline_cost),
        "kill_exceeds_solver": kill_exceeds_solver,
        "kill_never_differs": kill_never_differs,
        "any_kill_condition_holds": any_kill,
        "authority_effect": "None",
    }


def refuse_unimproved_buyer_baseline() -> None:
    planned_cost = Fraction(5)
    buyer_cost = Fraction(5)
    if planned_cost >= buyer_cost:
        raise ValueError("kill_never_differs: planned suite does not improve on buyer baseline")
