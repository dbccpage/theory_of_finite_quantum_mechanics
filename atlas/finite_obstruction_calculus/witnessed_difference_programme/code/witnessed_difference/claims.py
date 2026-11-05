"""Machine-readable claim-to-code map inventory preflight validation.

Checks file presence, unique IDs, and nonempty labels; does not execute tests or certify mathematical truth.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .relative_status import ClaimStatus


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    status: ClaimStatus
    module: str
    tests: tuple[str, ...]
    evidence_type: str


def load_claim_map(path: Path) -> tuple[ClaimRecord, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = []
    for item in payload["claims"]:
        records.append(
            ClaimRecord(
                item["claim_id"],
                ClaimStatus(item["status"]),
                item["module"],
                tuple(item["tests"]),
                item["evidence_type"],
            )
        )
    return tuple(records)


def validate_claim_map(records: tuple[ClaimRecord, ...], root: Path) -> tuple[str, ...]:
    errors: list[str] = []
    ids = [record.claim_id for record in records]
    if len(ids) != len(set(ids)):
        errors.append("claim ids must be unique")
    for record in records:
        if not record.claim_id or not record.evidence_type:
            errors.append("claim id and evidence type must be nonempty")
        if not (root / record.module).is_file():
            errors.append(f"missing module: {record.module}")
        if not record.tests:
            errors.append(f"claim has no tests: {record.claim_id}")
        for test in record.tests:
            if not (root / test).is_file():
                errors.append(f"missing test: {test}")
    return tuple(errors)
# Executable finite evidence; AuthorityEffect: None.
