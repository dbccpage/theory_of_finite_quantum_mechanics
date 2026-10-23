"""Executable witness for PROD-P3-NEXT-2 (Appendix Q.4 13-hit break-even example)."""

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

from antibody_transfer.replay_examples import example_input  # noqa: E402
from omega_engine_applications.wdp_products.p3_guard_transfer.adapter import (  # noqa: E402
    WdpGuardTransferChecker,
    make_source_guard_rule,
    q4_worked_example_ledger,
)


def witness() -> dict[str, object]:
    checker = WdpGuardTransferChecker()
    source_task = example_input()["transfer"]["source"]
    rule = make_source_guard_rule("circulation", source_task)

    ledger_12 = q4_worked_example_ledger(hits=12)
    saving_12 = checker.price(rule, ledger_12)
    if saving_12 != Fraction(0) or ledger_12.strict_benefit():
        raise RuntimeError("expected 0 saving and no strict benefit at 12 hits")

    ledger_13 = q4_worked_example_ledger(hits=13)
    saving_13 = checker.price(rule, ledger_13)
    if saving_13 != Fraction(1) or not ledger_13.strict_benefit():
        raise RuntimeError("expected saving 1 and strict benefit at 13 hits")

    min_strict_hits = next(
        h for h in range(0, 20) if q4_worked_example_ledger(hits=h).strict_benefit()
    )
    if min_strict_hits != 13:
        raise RuntimeError(f"expected minimum strict-benefit hits == 13, got {min_strict_hits}")

    return {
        "goal_id": "PROD-P3-NEXT-2",
        "candidates": ledger_13.candidates,
        "saving_at_12_hits": str(saving_12),
        "strict_benefit_at_12": ledger_12.strict_benefit(),
        "saving_at_13_hits": str(saving_13),
        "strict_benefit_at_13": ledger_13.strict_benefit(),
        "minimum_strict_benefit_hits": min_strict_hits,
        "authority_effect": rule.authority_effect,
    }


def refuse_twelve_hits_as_strict_benefit() -> None:
    ledger_12 = q4_worked_example_ledger(hits=12)
    if not ledger_12.strict_benefit():
        raise ValueError("12 hits yields saving 0; strict benefit requires at least 13 hits")
