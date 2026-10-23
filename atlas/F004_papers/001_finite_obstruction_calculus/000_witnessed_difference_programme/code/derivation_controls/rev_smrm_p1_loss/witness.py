"""Executable witness for REV-SMRM-P1-LOSS (Governor refuses LOSS certificates lacking the initial belief)."""

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

    bad_loss_cert = copy.deepcopy(trapped_cert)
    bad_loss_cert["trap_beliefs"] = [["d"]]

    refused_rep = governor.report(
        trapped_model,
        bad_loss_cert,
        "5",
        task_admits_impossibility=True,
    )
    if (
        not isinstance(refused_rep, GovernorReport)
        or refused_rep.label is not TerminationLabel.REFUSED_CERTIFICATE
        or refused_rep.check is None
        or refused_rep.check.accepted
    ):
        raise RuntimeError("expected LOSS certificate lacking b_0 to be RefusedCertificate")

    stalled_model = graph_model({"s": []}, targets=("t",))
    stalled_cert = cp_producer.solve_progress(stalled_model)["certificate"]
    stalled_rep = governor.report(stalled_model, stalled_cert, "5", task_admits_impossibility=False)

    win_model = cheaper_route()
    win_opt_cert = cp_producer.solve_progress(win_model)["certificate"]
    exhausted_rep = governor.report(win_model, win_opt_cert, "1", task_admits_impossibility=False)

    impossible_rep = governor.report(
        trapped_model,
        trapped_cert,
        "5",
        task_admits_impossibility=True,
    )
    assert isinstance(stalled_rep, GovernorReport)
    assert isinstance(exhausted_rep, GovernorReport)
    assert isinstance(impossible_rep, GovernorReport)

    labels = {stalled_rep.label, exhausted_rep.label, impossible_rep.label}
    if len(labels) != 3:
        raise RuntimeError("Stalled, Exhausted, and Impossible must be pairwise distinct")

    return {
        "goal_id": "REV-SMRM-P1-LOSS",
        "initial_belief": ["s"],
        "missing_b0_label": refused_rep.label.value,
        "missing_b0_verified": refused_rep.check.accepted,
        "stalled_label": stalled_rep.label.value,
        "exhausted_label": exhausted_rep.label.value,
        "impossible_label": impossible_rep.label.value,
        "distinct_outcome_count": len(labels),
        "authority_effect": refused_rep.authority_effect,
    }


def refuse_loss_certificate_missing_b0() -> None:
    out = witness()
    if out["missing_b0_label"] == "RefusedCertificate" and not out["missing_b0_verified"]:
        raise ValueError("RefusedCertificate: b_0 not in trap_set")
