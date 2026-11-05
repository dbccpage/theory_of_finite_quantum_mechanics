from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_woland.infrastructure.wdp_claim_ledger_certification_adapter import (
    WdpClaimLedgerCertificationAdapter,
)
from omega_engine_woland.use_cases.claim_ledger_certification_use_case import (
    ClaimLedgerEntrySpecV1,
    evaluate_claim_ledger_certification,
)


def witness() -> dict[str, object]:
    adapter = WdpClaimLedgerCertificationAdapter()
    entries = (
        ClaimLedgerEntrySpecV1(
            claim_id="C1_BASE",
            raw_status="Exact-Checked",
            evidence_pointers=("proof/c1.py",),
            depends_on=(),
            requires_numeric_provenance=True,
        ),
        ClaimLedgerEntrySpecV1(
            claim_id="C2_DERIVED",
            raw_status="Lean-Proved",
            evidence_pointers=("lean/c2.lean",),
            depends_on=("C1_BASE",),
            requires_numeric_provenance=False,
        ),
        ClaimLedgerEntrySpecV1(
            claim_id="C3_OPEN",
            raw_status="Open",
            evidence_pointers=(),
            depends_on=(),
            requires_numeric_provenance=False,
        ),
    )

    all_present = evaluate_claim_ledger_certification(
        entries,
        frozenset({"proof/c1.py", "lean/c2.lean"}),
        adapter,
        p2_provenance_verified=True,
    )
    assert all_present.is_ok
    full_report = all_present.value

    missing_ptr = evaluate_claim_ledger_certification(
        entries,
        frozenset({"lean/c2.lean"}),
        adapter,
        p2_provenance_verified=True,
    )
    assert missing_ptr.is_ok
    missing_report = missing_ptr.value

    p2_unverified = evaluate_claim_ledger_certification(
        entries,
        frozenset({"proof/c1.py", "lean/c2.lean"}),
        adapter,
        p2_provenance_verified=False,
    )
    assert p2_unverified.is_ok
    p2_report = p2_unverified.value

    return {
        "goal_id": "PROD-P5",
        "runtime_package": "omega_engine_woland",
        "full_statuses": full_report["statuses"],
        "missing_pointer_statuses": missing_report["statuses"],
        "p2_unverified_statuses": p2_report["statuses"],
        "full_proved_count": full_report["proved_count"],
        "missing_proved_count": missing_report["proved_count"],
        "authority_effect": full_report["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
