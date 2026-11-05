"""Executable witness for PROD-P3-NEXT-1 (WdpGuardTransferChecker transfer & price)."""

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

from antibody_transfer.replay_examples import example_input  # noqa: E402
from omega_engine_applications.wdp_products.kernel.contracts import TypedRefusal  # noqa: E402
from omega_engine_applications.wdp_products.p3_guard_transfer.adapter import (  # noqa: E402
    WdpGuardTransferChecker,
    make_source_guard_rule,
    q4_worked_example_ledger,
)
from omega_engine_applications.wdp_products.p3_guard_transfer.contracts import (  # noqa: E402
    BreakEven,
    GuardRule,
)


def witness() -> dict[str, object]:
    checker = WdpGuardTransferChecker()
    transfer_problem = example_input()["transfer"]
    source_task = transfer_problem["source"]

    circulation = make_source_guard_rule("circulation", source_task)
    transferred = checker.transfer(circulation, transfer_problem)
    if not isinstance(transferred, GuardRule):
        raise RuntimeError("expected circulation rule to transfer soundly")

    unsafe_rule = make_source_guard_rule("unsafe-point", source_task)
    refused_unsafe = checker.transfer(unsafe_rule, transfer_problem)
    if not isinstance(refused_unsafe, TypedRefusal) or refused_unsafe.code != "transfer_unsafe":
        raise RuntimeError("expected unsafe-point to be refused with transfer_unsafe")

    unsound_rule = make_source_guard_rule("invalid-source-rule", source_task)
    refused_unsound = checker.transfer(unsound_rule, transfer_problem)
    if not isinstance(refused_unsound, TypedRefusal) or refused_unsound.code != "source_unsound":
        raise RuntimeError("expected invalid-source-rule to be refused with source_unsound")

    ref_ledger = BreakEven(
        candidates=4,
        hits=2,
        verify_cost="1",
        guard_cost="1/10",
        setup_cost="1",
    )
    ref_saving = checker.price(circulation, ref_ledger)
    q4_12 = checker.price(circulation, q4_worked_example_ledger(hits=12))
    q4_13 = checker.price(circulation, q4_worked_example_ledger(hits=13))

    return {
        "goal_id": "PROD-P3-NEXT-1",
        "transferred_rule_id": transferred.rule_id,
        "unsafe_refusal_code": refused_unsafe.code,
        "unsound_refusal_code": refused_unsound.code,
        "reference_saving": str(ref_saving),
        "q4_saving_at_12_hits": str(q4_12),
        "q4_saving_at_13_hits": str(q4_13),
        "authority_effect": transferred.authority_effect,
    }


def refuse_hits_exceeding_candidates() -> None:
    BreakEven(
        candidates=4,
        hits=5,
        verify_cost="1",
        guard_cost="1/10",
        setup_cost="1",
    )
