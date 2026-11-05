"""Executable witness for PROD-P2-NEXT-1 (WdpOutputGate 12-step G.5 validator)."""

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

from omega_engine_applications.wdp_products.kernel.contracts import (  # noqa: E402
    ReceiptRecord,
    TypedRefusal,
)
from omega_engine_applications.wdp_products.p2_provenance_gate.adapter import (  # noqa: E402
    WdpOutputGate,
    mutate_for_g5_step,
    valid_candidate_record,
)
from omega_engine_applications.wdp_products.p2_provenance_gate.contracts import (  # noqa: E402
    G5Step,
    ValidationFailure,
    ValidationReport,
)


def witness() -> dict[str, object]:
    gate = WdpOutputGate()
    rec = valid_candidate_record()
    pass_report = gate.gate("claim.p2.001", rec)
    if not isinstance(pass_report, ValidationReport) or not pass_report.emitted:
        raise RuntimeError("expected valid candidate record to pass WdpOutputGate")
    if not isinstance(pass_report.receipt, ReceiptRecord):
        raise RuntimeError("passing ValidationReport must carry a ReceiptRecord")

    isolated_steps: list[str] = []
    for step in G5Step:
        mutated = mutate_for_g5_step(step)
        fail_report = gate.gate(f"claim.p2.{step.name.lower()}", mutated)
        if not isinstance(fail_report, ValidationReport) or fail_report.emitted:
            raise RuntimeError(f"expected mutation for {step} to fail")
        if fail_report.receipt is not None:
            raise RuntimeError(f"failing ValidationReport for {step} must not carry a receipt")
        if tuple(f.step for f in fail_report.failures) != (step,):
            raise RuntimeError(
                f"mutation for {step} did not isolate step: got {fail_report.failures}"
            )
        isolated_steps.append(step.value)

    bad_claim = gate.gate("", rec)
    if not isinstance(bad_claim, TypedRefusal) or bad_claim.code != "invalid_input":
        raise RuntimeError("empty claim_id was not refused with invalid_input")

    return {
        "goal_id": "PROD-P2-NEXT-1",
        "emitted": pass_report.emitted,
        "receipt_digest": pass_report.receipt.receipt_digest,
        "isolated_g5_steps": tuple(isolated_steps),
        "g5_step_count": len(isolated_steps),
        "empty_claim_refusal": bad_claim.code,
        "authority_effect": pass_report.authority_effect,
    }


def refuse_receipt_on_failing_report() -> None:
    gate = WdpOutputGate()
    pass_report = gate.gate("claim.p2.001", valid_candidate_record())
    assert isinstance(pass_report, ValidationReport) and pass_report.receipt is not None
    ValidationReport(
        claim_id="claim.p2.001",
        failures=(ValidationFailure(step=G5Step.IDS, detail="mismatch"),),
        receipt=pass_report.receipt,
    )
