"""Executable witness for PROD-KERNEL-NEXT-1 (WdpReceiptIssuer parity)."""

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

from omega_engine_applications.wdp_products.kernel.adapter import (  # noqa: E402
    WdpReceiptIssuer,
    from_receipt_record,
    to_receipt_record,
    to_typed_refusal,
)
from omega_engine_applications.wdp_products.kernel.contracts import (  # noqa: E402
    ReceiptRecord,
    TypedRefusal,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused  # noqa: E402
from witnessed_difference.receipts import make_receipt, verify_receipt  # noqa: E402


def witness() -> dict[str, object]:
    issuer = WdpReceiptIssuer(implementation_version="0.1.0")
    inputs = {"alpha": [1, 2], "beta": "payload"}
    output = {"result": "ok", "count": 2}
    claims = ("claim_b", "claim_a", "claim_b")

    record = issuer.issue("parity_subject", inputs, output, claims)
    if not isinstance(record, ReceiptRecord):
        raise RuntimeError("expected ReceiptRecord on valid inputs")

    ref_outcome = make_receipt(
        "parity_subject", inputs, output, claims, implementation_version="0.1.0"
    )
    if not isinstance(ref_outcome, Accepted):
        raise RuntimeError("reference make_receipt refused valid inputs")
    if record != to_receipt_record(ref_outcome.value):
        raise RuntimeError("adapter ReceiptRecord differs from reference Receipt")
    if from_receipt_record(record) != ref_outcome.value:
        raise RuntimeError("round-trip from_receipt_record differs from reference Receipt")

    verified = issuer.verify(record, inputs, output)
    ref_verified = verify_receipt(ref_outcome.value, inputs, output)
    if verified is not True or not isinstance(ref_verified, Accepted) or ref_verified.value is not True:
        raise RuntimeError("receipt replay verification failed")

    tampered_verify = issuer.verify(record, {"alpha": [999]}, output)
    if not isinstance(tampered_verify, TypedRefusal) or tampered_verify.code != "digest_mismatch":
        raise RuntimeError("tampered input was not refused with digest_mismatch")

    refused_empty = issuer.issue("", inputs, output, claims)
    if not isinstance(refused_empty, TypedRefusal) or refused_empty.code != "invalid_input":
        raise RuntimeError("empty subject was not refused with invalid_input")

    mapped_refusal = to_typed_refusal(Refused(RefusalCode.RECEIPT_MISMATCH, "body modified"))
    return {
        "goal_id": "PROD-KERNEL-NEXT-1",
        "claim_ids": record.claim_ids,
        "input_digest": record.input_digest,
        "output_digest": record.output_digest,
        "receipt_digest": record.receipt_digest,
        "verified": verified,
        "tampered_refusal_code": tampered_verify.code,
        "empty_subject_refusal_code": refused_empty.code,
        "mapped_refusal_code": mapped_refusal.code,
        "authority_effect": record.authority_effect,
    }


def refuse_authority_promotion(authority_effect: str = "Granted") -> None:
    if authority_effect != "None":
        raise ValueError("ReceiptRecord and TypedRefusal forbid authority_effect != 'None'")
