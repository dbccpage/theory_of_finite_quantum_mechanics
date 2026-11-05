"""Executable witness for PROD-KERNEL-NEXT-2 (Pilot agent loop finite arena declaration)."""

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
from omega_engine_applications.wdp_products.kernel.adapter import (  # noqa: E402
    PILOT_ARENA_TASK_ID,
    PILOT_ARENA_USABLE_BUDGET,
    WdpCertificateChecker,
    declare_pilot_agent_loop_arena,
)
from omega_engine_applications.wdp_products.p1_abstention_governor.adapter import (  # noqa: E402
    WdpAbstentionGovernor,
)
from omega_engine_applications.wdp_products.p1_abstention_governor.contracts import (  # noqa: E402
    GovernorReport,
    TerminationLabel,
)


def witness() -> dict[str, object]:
    arena = declare_pilot_agent_loop_arena()
    cert = cp_producer.solve_progress(arena)["certificate"]
    checker = WdpCertificateChecker()
    check_rec = checker.check(arena, cert)
    if not check_rec.accepted or check_rec.initial_value != PILOT_ARENA_USABLE_BUDGET:
        raise RuntimeError("expected pilot arena optimal value to equal PILOT_ARENA_USABLE_BUDGET")

    governor = WdpAbstentionGovernor(checker=checker)
    resolved_rep = governor.report(
        arena,
        cert,
        PILOT_ARENA_USABLE_BUDGET,
        task_admits_impossibility=False,
    )
    exhausted_rep = governor.report(
        arena,
        cert,
        "2",
        task_admits_impossibility=False,
    )
    if (
        not isinstance(resolved_rep, GovernorReport)
        or resolved_rep.label is not TerminationLabel.RESOLVED_WITHIN_BUDGET
    ):
        raise RuntimeError("expected pilot arena to resolve within usable budget")
    if (
        not isinstance(exhausted_rep, GovernorReport)
        or exhausted_rep.label is not TerminationLabel.EXHAUSTED
    ):
        raise RuntimeError("expected pilot arena to report Exhausted at budget 2")

    return {
        "goal_id": "PROD-KERNEL-NEXT-2",
        "task_id": PILOT_ARENA_TASK_ID,
        "states": list(arena["states"]),
        "usable_budget": PILOT_ARENA_USABLE_BUDGET,
        "initial_value": check_rec.initial_value,
        "label_at_usable_budget": resolved_rep.label.value,
        "label_at_tight_budget": exhausted_rep.label.value,
        "authority_effect": resolved_rep.authority_effect,
    }


def refuse_negative_pilot_budget() -> None:
    arena = declare_pilot_agent_loop_arena()
    cert = cp_producer.solve_progress(arena)["certificate"]
    governor = WdpAbstentionGovernor()
    res = governor.report(arena, cert, "-1", task_admits_impossibility=False)
    if hasattr(res, "code"):
        raise ValueError(f"{res.code}: {res.reason}")
