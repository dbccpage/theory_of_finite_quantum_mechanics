"""Executable witness for PROD-P2-NEXT-2 (Fixture per G.5 step that fails exactly that step)."""

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

from omega_engine_applications.wdp_products.p2_provenance_gate.adapter import (  # noqa: E402
    WdpOutputGate,
    mutate_for_g5_step,
)
from omega_engine_applications.wdp_products.p2_provenance_gate.contracts import (  # noqa: E402
    G5Step,
    ValidationReport,
)


def witness() -> dict[str, object]:
    gate = WdpOutputGate()
    isolated_steps: list[str] = []
    for step in G5Step:
        mutated = mutate_for_g5_step(step)
        report = gate.gate(f"claim.g5.{step.name.lower()}", mutated)
        if not isinstance(report, ValidationReport) or report.emitted:
            raise RuntimeError(f"fixture for {step.value} was unexpectedly admitted")
        failed = [f.step.value for f in report.failures]
        if failed != [step.value]:
            raise RuntimeError(f"fixture for {step.value} failed {failed} instead of [{step.value}]")
        isolated_steps.append(step.value)

    return {
        "goal_id": "PROD-P2-NEXT-2",
        "step_count": len(isolated_steps),
        "isolated_steps": isolated_steps,
        "authority_effect": "None",
    }


def refuse_admitted_report_with_failure_fixture() -> None:
    gate = WdpOutputGate()
    mutated = mutate_for_g5_step(G5Step.UNCERTAINTY)
    report = gate.gate("claim.g5.uncertainty", mutated)
    if isinstance(report, ValidationReport) and not report.emitted and len(report.failures) == 1:
        raise ValueError(f"G5 step failure: {report.failures[0].step.value}")
