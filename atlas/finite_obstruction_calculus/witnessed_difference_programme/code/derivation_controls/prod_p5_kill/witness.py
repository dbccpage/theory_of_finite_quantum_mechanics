"""Executable witness for PROD-P5-KILL (Evaluate P5 kill conditions on a pilot ledger)."""

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

from omega_engine_applications.wdp_products.p5_claim_certification.adapter import (  # noqa: E402
    evaluate_pilot_p5_kill_conditions,
)
from omega_engine_applications.wdp_products.p5_claim_certification.contracts import (  # noqa: E402
    ClaimNode,
    EvidencePointers,
    Status,
)


def witness() -> dict[str, object]:
    full_ev = EvidencePointers(
        prose_statement="sec 4.1",
        claim_ledger_row="WDP-CH04-P01",
        implementation="code/witnessed_difference/exact.py",
        tests="tests/test_exact.py",
        formal_theorem="lean4/WitnessedDifference/Exact.lean",
        axiom_or_import_report="none",
        source_revision_and_hash="sha256:abc",
        release_artifact="MANIFEST.sha256",
    )
    missing_ev = EvidencePointers(
        prose_statement="sec 4.2",
        claim_ledger_row="WDP-CH04-P02",
    )
    c1 = ClaimNode(claim_id="C1", status=Status.PROVED, evidence=full_ev, depends_on=())
    c2 = ClaimNode(claim_id="C2", status=Status.PROVED, evidence=missing_ev, depends_on=("C1",))

    res = evaluate_pilot_p5_kill_conditions((c1, c2), changed=("C2",), ci_executed=True)
    if not isinstance(res, dict) or res["kill_triggered"]:
        raise RuntimeError("expected no P5 kill conditions to hold on the pilot ledger")
    return {
        "goal_id": "PROD-P5-KILL",
        "total_claims": int(res["total_claims"]),
        "proved_with_missing_d3": list(res["proved_with_missing_d3"]),
        "demoted_to_undetermined": list(res["demoted_to_undetermined"]),
        "kill_1_manual_maintenance": bool(res["kill_1_manual_maintenance"]),
        "kill_2_proved_with_missing_d3": bool(res["kill_2_proved_with_missing_d3"]),
        "kill_triggered": bool(res["kill_triggered"]),
        "authority_effect": str(res["authority_effect"]),
    }


def refuse_non_bool_ci_flag() -> None:
    res = evaluate_pilot_p5_kill_conditions((), (), ci_executed=1)  # type: ignore[arg-type]
    if hasattr(res, "code"):
        raise ValueError(f"{res.code}: {res.reason}")
