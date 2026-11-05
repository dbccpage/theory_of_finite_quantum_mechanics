"""Executable witness for PROD-P1-NEXT-2 (Negative controls: Impossible without task policy, forged certificate rejected)."""

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

import certified_progress.producer as cp_producer  # noqa: E402
from certified_progress.fixtures import cheaper_route  # noqa: E402
from certified_progress.model import graph_model  # noqa: E402
from omega_engine_applications.wdp_products.p1_abstention_governor.adapter import (  # noqa: E402
    WdpAbstentionGovernor,
)
from omega_engine_applications.wdp_products.p1_abstention_governor.contracts import (  # noqa: E402
    GovernorReport,
    TerminationLabel,
)


def witness() -> dict[str, object]:
    governor = WdpAbstentionGovernor()
    trapped_model = graph_model({"s": [("go", "1", ["d"])]}, targets=("t",))
    trapped_cert = cp_producer.solve_progress(trapped_model)["certificate"]

    rep_no_policy = governor.report(
        trapped_model,
        trapped_cert,
        "5",
        task_admits_impossibility=False,
    )
    if not isinstance(rep_no_policy, GovernorReport) or (
        rep_no_policy.label is not TerminationLabel.LOSING_IN_DECLARED_ARENA
    ):
        raise RuntimeError("expected LosingInDeclaredArena when task_admits_impossibility=False")

    rep_with_policy = governor.report(
        trapped_model,
        trapped_cert,
        "5",
        task_admits_impossibility=True,
    )
    if not isinstance(rep_with_policy, GovernorReport) or (
        rep_with_policy.label is not TerminationLabel.IMPOSSIBLE
    ):
        raise RuntimeError("expected Impossible when task_admits_impossibility=True")

    win_model = cheaper_route()
    win_opt_cert = cp_producer.solve_progress(win_model)["certificate"]
    forged_task_cert = copy.deepcopy(win_opt_cert)
    forged_task_cert["task_id"] = "forged-task-id"
    rep_forged_task = governor.report(
        win_model,
        forged_task_cert,
        "5",
        task_admits_impossibility=False,
    )
    if (
        not isinstance(rep_forged_task, GovernorReport)
        or rep_forged_task.label is not TerminationLabel.REFUSED_CERTIFICATE
        or rep_forged_task.check is None
        or rep_forged_task.check.accepted
    ):
        raise RuntimeError("expected forged task_id certificate to be RefusedCertificate")

    forged_win_cert = copy.deepcopy(trapped_cert)
    forged_win_cert["kind"] = "WIN_OPTIMAL"
    rep_forged_win = governor.report(
        trapped_model,
        forged_win_cert,
        "5",
        task_admits_impossibility=False,
    )
    if (
        not isinstance(rep_forged_win, GovernorReport)
        or rep_forged_win.label is not TerminationLabel.REFUSED_CERTIFICATE
        or rep_forged_win.check is None
        or rep_forged_win.check.accepted
    ):
        raise RuntimeError("expected forged WIN_OPTIMAL certificate to be RefusedCertificate")

    return {
        "goal_id": "PROD-P1-NEXT-2",
        "label_without_policy": rep_no_policy.label.value,
        "label_with_policy": rep_with_policy.label.value,
        "forged_task_id_label": rep_forged_task.label.value,
        "forged_task_id_verified": rep_forged_task.check.accepted,
        "forged_win_label": rep_forged_win.label.value,
        "forged_win_verified": rep_forged_win.check.accepted,
        "authority_effect": rep_no_policy.authority_effect,
    }


def refuse_impossible_without_task_policy() -> None:
    governor = WdpAbstentionGovernor()
    trapped_model = graph_model({"s": [("go", "1", ["d"])]}, targets=("t",))
    trapped_cert = cp_producer.solve_progress(trapped_model)["certificate"]
    rep = governor.report(
        trapped_model,
        trapped_cert,
        "5",
        task_admits_impossibility=False,
    )
    assert isinstance(rep, GovernorReport)
    GovernorReport(
        label=TerminationLabel.IMPOSSIBLE,
        task_admits_impossibility=False,
        budget="5",
        check=rep.check,
    )
