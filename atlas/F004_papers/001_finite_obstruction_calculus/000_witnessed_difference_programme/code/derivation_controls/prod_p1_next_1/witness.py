"""Executable witness for PROD-P1-NEXT-1 (WdpAbstentionGovernor 8-label round-trip)."""

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

import certified_progress.producer as cp_producer  # noqa: E402
from certified_progress.fixtures import cheaper_route  # noqa: E402
from certified_progress.model import graph_model  # noqa: E402
from certified_progress.reporting import report_termination  # noqa: E402
from omega_engine_applications.wdp_products.kernel.contracts import TypedRefusal  # noqa: E402
from omega_engine_applications.wdp_products.p1_abstention_governor.adapter import (  # noqa: E402
    WdpAbstentionGovernor,
)
from omega_engine_applications.wdp_products.p1_abstention_governor.contracts import (  # noqa: E402
    GovernorReport,
    TerminationLabel,
)


def witness() -> dict[str, object]:
    governor = WdpAbstentionGovernor()

    win_model = cheaper_route()
    win_opt_cert = cp_producer.solve_progress(win_model)["certificate"]

    win_feas_cert = copy.deepcopy(win_opt_cert)
    win_feas_cert["kind"] = "WIN_FEASIBLE"
    win_feas_cert["optimality_requested"] = False
    win_feas_cert["strategy"] = [
        {"belief": ["s"], "action": "direct"},
        {"belief": ["u"], "action": "finish"},
    ]
    win_feas_cert["ranks"] = [
        {"belief": ["s"], "rank": 1},
        {"belief": ["t"], "rank": 0},
        {"belief": ["u"], "rank": 1},
    ]
    win_feas_cert["values"] = [
        {"belief": ["s"], "value": "5"},
        {"belief": ["t"], "value": "0"},
        {"belief": ["u"], "value": "1"},
    ]

    forged_cert = copy.deepcopy(win_opt_cert)
    forged_cert["task_id"] = "forged-task"

    stalled_model = graph_model({"s": []}, targets=("t",))
    stalled_cert = cp_producer.solve_progress(stalled_model)["certificate"]

    trapped_model = graph_model({"s": [("go", "1", ["d"])]}, targets=("t",))
    trapped_cert = cp_producer.solve_progress(trapped_model)["certificate"]

    observed: list[str] = []

    refused_rep = governor.report(
        win_model,
        None,
        "5",
        task_admits_impossibility=False,
        refusal_action="missing_calibration",
    )
    if not isinstance(refused_rep, GovernorReport) or refused_rep.label is not TerminationLabel.REFUSED:
        raise RuntimeError("expected Refused label on controller refusal_action")
    if GovernorReport.model_validate_json(refused_rep.model_dump_json()) != refused_rep:
        raise RuntimeError("Refused GovernorReport failed JSON round-trip")
    observed.append(refused_rep.label.value)

    cases = [
        (win_model, forged_cert, "5", False, TerminationLabel.REFUSED_CERTIFICATE),
        (stalled_model, stalled_cert, "5", False, TerminationLabel.STALLED),
        (trapped_model, trapped_cert, "5", True, TerminationLabel.IMPOSSIBLE),
        (trapped_model, trapped_cert, "5", False, TerminationLabel.LOSING_IN_DECLARED_ARENA),
        (win_model, win_opt_cert, "2", False, TerminationLabel.RESOLVED_WITHIN_BUDGET),
        (win_model, win_opt_cert, "1", False, TerminationLabel.EXHAUSTED),
        (win_model, win_feas_cert, "4", False, TerminationLabel.UNDETERMINED_BUDGET),
    ]

    for model, cert, budget, policy, expected in cases:
        ref = report_termination(model, cert, budget, task_admits_impossibility=policy)
        rep = governor.report(model, cert, budget, task_admits_impossibility=policy)
        if not isinstance(rep, GovernorReport) or rep.label is not expected:
            raise RuntimeError(f"expected {expected}, got {rep}")
        if rep.label.value != ref["termination"]:
            raise RuntimeError("adapter label diverged from reference report_termination")
        if GovernorReport.model_validate_json(rep.model_dump_json()) != rep:
            raise RuntimeError(f"{expected} failed JSON round-trip")
        observed.append(rep.label.value)

    bad_budget = governor.report(win_model, win_opt_cert, "-1", task_admits_impossibility=False)
    if not isinstance(bad_budget, TypedRefusal) or bad_budget.code != "invalid_input":
        raise RuntimeError("negative budget was not refused with invalid_input")

    return {
        "goal_id": "PROD-P1-NEXT-1",
        "observed_labels": tuple(observed),
        "label_count": len(set(observed)),
        "negative_budget_refusal": bad_budget.code,
        "authority_effect": "None",
    }


def refuse_impossible_without_policy() -> None:
    governor = WdpAbstentionGovernor()
    trapped_model = graph_model({"s": [("go", "1", ["d"])]}, targets=("t",))
    trapped_cert = cp_producer.solve_progress(trapped_model)["certificate"]
    rep = governor.report(trapped_model, trapped_cert, "5", task_admits_impossibility=False)
    assert isinstance(rep, GovernorReport)
    # Attempting to construct GovernorReport with IMPOSSIBLE when task_admits_impossibility=False raises ValueError
    GovernorReport(
        label=TerminationLabel.IMPOSSIBLE,
        task_admits_impossibility=False,
        budget="5",
        check=rep.check,
    )
