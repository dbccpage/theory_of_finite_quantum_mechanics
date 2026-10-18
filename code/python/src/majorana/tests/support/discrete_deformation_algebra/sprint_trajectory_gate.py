"""ORT / process NDJSON gate for ``dda_sprint_trajectory`` tapes.

Schema id: ``dda_sprint_trajectory.v1``

Integrity mode requires each record to carry:

- ``run_id``
- step index: ``step_index`` or ``step_id``
- residual norm Φ₁: ``phi1`` or ``residual_norm`` or ``residual_energy``
- state fingerprint: ``state_vector`` or ``state_fingerprint`` or
  both ``input_hash`` and ``output_hash``
- ``authority_effect`` exactly equal to the string ``\"None\"``

When any record carries ``step_hash``, the full chain is checked via
``verify_trajectory_chain`` (edit / drop / reorder detection).

Historical ORT process tapes that only have
``run_id, date, authority_effect, stage, dda_letter, name, note`` classify as
``LEGACY_PROCESS_TAPE`` and fail integrity mode without rewriting those files.

AuthorityEffect: None. Diagnostic gate only; mints no authority.
"""

from __future__ import annotations
import json
from dataclasses import field
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from .trajectory_recorder import verify_trajectory_chain

SCHEMA_ID = "dda_sprint_trajectory.v1"

CLASS_EMPTY = "EMPTY"
CLASS_LEGACY = "LEGACY_PROCESS_TAPE"
CLASS_INTEGRITY_V1 = "INTEGRITY_V1"
CLASS_MIXED = "MIXED"
CLASS_INVALID = "INVALID"

PathLike = Union[str, Path]
Record = Dict[str, Any]

_STEP_KEYS = ("step_index", "step_id")
_PHI_KEYS = ("phi1", "residual_norm", "residual_energy")
_STATE_SINGLE = ("state_vector", "state_fingerprint")


@dataclass
class Violation:
    """One gate refusal for a line or the whole tape."""

    line: Optional[int]
    code: str
    detail: str

    def as_dict(self) -> Dict[str, Any]:
        return {"line": self.line, "code": self.code, "detail": self.detail}


@dataclass
class TrajectoryGateResult:
    """Outcome of ``validate_dda_sprint_trajectory``."""

    ok: bool
    classification: str
    schema_id: str = SCHEMA_ID
    record_count: int = 0
    violations: List[Violation] = field(default_factory=list)
    authority_effect: str = "None"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "classification": self.classification,
            "schema_id": self.schema_id,
            "record_count": self.record_count,
            "violations": [v.as_dict() for v in self.violations],
            "authority_effect": self.authority_effect,
        }


def _has_any(record: Record, keys: Sequence[str]) -> bool:
    return any(k in record and record[k] is not None for k in keys)


def _has_step_index(record: Record) -> bool:
    return _has_any(record, _STEP_KEYS)


def _has_phi1(record: Record) -> bool:
    return _has_any(record, _PHI_KEYS)


def _has_state_fingerprint(record: Record) -> bool:
    if _has_any(record, _STATE_SINGLE):
        return True
    return (
        record.get("input_hash") is not None and record.get("output_hash") is not None
    )


def _is_legacy_shape(record: Record) -> bool:
    """ORT process tape: stage/name/note style without integrity keys."""
    if _has_step_index(record) or _has_phi1(record) or _has_state_fingerprint(record):
        return False
    return "stage" in record and "name" in record


def _record_integrity_violations(line: int, record: Record) -> List[Violation]:
    out: List[Violation] = []
    if not record.get("run_id"):
        out.append(Violation(line, "MISSING_RUN_ID", "run_id required"))
    if not _has_step_index(record):
        out.append(
            Violation(
                line,
                "MISSING_STEP_INDEX",
                "need step_index or step_id",
            )
        )
    if not _has_phi1(record):
        out.append(
            Violation(
                line,
                "MISSING_PHI1",
                "need phi1 or residual_norm or residual_energy",
            )
        )
    if not _has_state_fingerprint(record):
        out.append(
            Violation(
                line,
                "MISSING_STATE_FINGERPRINT",
                "need state_vector or state_fingerprint or input_hash+output_hash",
            )
        )
    ae = record.get("authority_effect")
    if ae != "None":
        out.append(
            Violation(
                line,
                "AUTHORITY_EFFECT_NOT_NONE",
                f"authority_effect must be string 'None', got {ae!r}",
            )
        )
    return out


def load_ndjson_records(
    source: Union[PathLike, Sequence[Record]],
) -> Tuple[List[Record], List[Violation]]:
    """Load records from a path or accept an in-memory sequence."""
    if isinstance(source, (str, Path)):
        path = Path(source)
        text = path.read_text(encoding="utf-8")
        records: List[Record] = []
        violations: List[Violation] = []
        for i, raw in enumerate(text.splitlines(), start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                violations.append(Violation(i, "JSON_DECODE", f"line {i}: {exc}"))
                continue
            if not isinstance(obj, dict):
                violations.append(
                    Violation(i, "NOT_OBJECT", f"line {i}: expected JSON object")
                )
                continue
            records.append(obj)
        return records, violations
    return list(source), []


def validate_dda_sprint_trajectory(
    source: Union[PathLike, Sequence[Record]],
    *,
    require_integrity_v1: bool = True,
) -> TrajectoryGateResult:
    """Validate a DDA sprint trajectory tape.

    Parameters
    ----------
    source:
        Path to ``*.ndjson`` / ``*.jsonl`` or an in-memory list of dict records.
    require_integrity_v1:
        When True (default), ``LEGACY_PROCESS_TAPE`` is a hard fail with per-line
        missing-field violations. When False, legacy tapes classify cleanly
        without claiming integrity.

    Returns
    -------
    TrajectoryGateResult
        ``ok`` is True only when there are no violations under the selected mode.
    """
    records, load_violations = load_ndjson_records(source)
    violations: List[Violation] = list(load_violations)

    if not records and not violations:
        return TrajectoryGateResult(ok=True, classification=CLASS_EMPTY, record_count=0)

    if not records and violations:
        return TrajectoryGateResult(
            ok=False,
            classification=CLASS_INVALID,
            record_count=0,
            violations=violations,
        )

    legacy_count = 0
    integrity_count = 0
    for index, record in enumerate(records):
        line = index + 1
        line_violations = _record_integrity_violations(line, record)
        if not line_violations:
            integrity_count += 1
            continue
        if _is_legacy_shape(record) and all(
            v.code
            in {
                "MISSING_STEP_INDEX",
                "MISSING_PHI1",
                "MISSING_STATE_FINGERPRINT",
            }
            or (v.code == "MISSING_RUN_ID" and not record.get("run_id"))
            for v in line_violations
        ):
            legacy_count += 1
            if require_integrity_v1:
                violations.extend(line_violations)
            elif any(v.code == "AUTHORITY_EFFECT_NOT_NONE" for v in line_violations):
                violations.extend(
                    v for v in line_violations if v.code == "AUTHORITY_EFFECT_NOT_NONE"
                )
            else:
                hard = [
                    v
                    for v in line_violations
                    if v.code in {"AUTHORITY_EFFECT_NOT_NONE"}
                ]
                if not record.get("run_id"):
                    hard.append(Violation(line, "MISSING_RUN_ID", "run_id required"))
                violations.extend(hard)
        else:
            violations.extend(line_violations)

    if any("step_hash" in r for r in records):
        chain_ok, chain_detail = verify_trajectory_chain(records)
        if not chain_ok:
            violations.append(Violation(None, "CHAIN_BROKEN", chain_detail))

    if integrity_count == len(records) and not any(
        v.code.startswith("MISSING_") or v.code == "AUTHORITY_EFFECT_NOT_NONE"
        for v in violations
    ):
        classification = CLASS_INTEGRITY_V1
    elif legacy_count == len(records):
        classification = CLASS_LEGACY
    elif integrity_count and legacy_count:
        classification = CLASS_MIXED
    elif load_violations and not integrity_count:
        classification = CLASS_INVALID
    elif integrity_count:
        classification = CLASS_INTEGRITY_V1
    elif legacy_count:
        classification = CLASS_LEGACY
    else:
        classification = CLASS_INVALID

    ok = len(violations) == 0
    if require_integrity_v1 and classification != CLASS_INTEGRITY_V1 and records:
        ok = False
        if classification == CLASS_LEGACY and not any(
            v.code.startswith("MISSING_") for v in violations
        ):
            violations.append(
                Violation(
                    None,
                    "LEGACY_NOT_INTEGRITY_V1",
                    "tape is LEGACY_PROCESS_TAPE; integrity v1 fields absent",
                )
            )
            ok = False

    return TrajectoryGateResult(
        ok=ok,
        classification=classification,
        record_count=len(records),
        violations=violations,
    )



