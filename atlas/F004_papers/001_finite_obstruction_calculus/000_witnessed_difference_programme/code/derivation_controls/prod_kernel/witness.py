from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
_WDP_CODE = (
    _REPO_ROOT
    / "omega_engine_atlas"
    / "coda_atlas"
    / "F004_papers"
    / "001_finite_obstruction_calculus"
    / "000_witnessed_difference_programme"
    / "code"
)
if str(_WDP_CODE) not in sys.path:
    sys.path.insert(0, str(_WDP_CODE))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from certified_progress import producer as cp_producer
from omega_engine_applications.wdp_products.kernel.adapter import (
    WdpCertificateChecker,
    WdpReceiptIssuer,
    declare_pilot_agent_loop_arena,
    evaluate_pilot_kernel_kill_conditions,
)
from omega_engine_applications.wdp_products.kernel.contracts import TypedRefusal


def witness() -> dict[str, object]:
    kill_report = evaluate_pilot_kernel_kill_conditions()
    arena = declare_pilot_agent_loop_arena()
    cert = cp_producer.solve_progress(arena)["certificate"]

    checker = WdpCertificateChecker()
    issuer = WdpReceiptIssuer()

    check_receipt = checker.check(arena, cert)
    receipt = issuer.issue(
        subject="prod-kernel-closure",
        inputs={"arena_digest": check_receipt.model_digest},
        output={
            "certificate_digest": check_receipt.certificate_digest,
            "value": check_receipt.initial_value,
        },
        claim_ids=("WDP-CH12-D01", "WDP-CHS-D03"),
    )
    receipt_verified = issuer.verify(
        receipt,
        inputs={"arena_digest": check_receipt.model_digest},
        output={
            "certificate_digest": check_receipt.certificate_digest,
            "value": check_receipt.initial_value,
        },
    )
    tampered = issuer.verify(
        receipt,
        inputs={"arena_digest": check_receipt.model_digest},
        output={"certificate_digest": check_receipt.certificate_digest, "value": "999"},
    )

    return {
        "goal_id": "PROD-KERNEL",
        "certificate_valid": check_receipt.accepted,
        "claim": check_receipt.claim,
        "initial_value": check_receipt.initial_value,
        "receipt_sha256": receipt.receipt_digest,
        "receipt_verified": receipt_verified is True,
        "tampered_rejected": isinstance(tampered, TypedRefusal),
        "refusal_code": tampered.code if isinstance(tampered, TypedRefusal) else "",
        "any_kill_condition_holds": kill_report["any_kill_condition_holds"],
        "authority_effect": kill_report["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
