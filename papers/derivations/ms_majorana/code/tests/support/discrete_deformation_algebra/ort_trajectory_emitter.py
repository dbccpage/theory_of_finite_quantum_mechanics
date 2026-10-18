"""ORT sprint trajectory emitter bound to ``dda_sprint_trajectory.v1``.

Produces NDJSON lines that pass
``sprint_trajectory_gate.validate_dda_sprint_trajectory`` under integrity mode.

Historical LEGACY_PROCESS_TAPE lines are **not** rewritten here; new emissions
use this surface. Optional ``upgrade_legacy_record`` maps process-tape fields
into a v1-shaped dict for re-emit (caller chooses write path).

AuthorityEffect: None. Diagnostic only.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import field
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from .sprint_trajectory_gate import SCHEMA_ID, validate_dda_sprint_trajectory
from .trajectory_recorder import _step_hash

PathLike = Union[str, Path]


def _state_fingerprint(obj: Any) -> str:
    if (
        isinstance(obj, str)
        and len(obj) == 64
        and all(c in "0123456789abcdef" for c in obj)
    ):
        return obj
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def emit_integrity_v1_record(
    *,
    run_id: str,
    step_index: int,
    phi1: float,
    state_fingerprint: str,
    dda_letter: str = "",
    name: str = "",
    note: str = "",
    stage: Optional[int] = None,
    date: Optional[str] = None,
    prev_step_hash: Optional[str] = None,
    chain: bool = True,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build one INTEGRITY_V1 dict (optionally hash-chained)."""
    if not run_id:
        raise ValueError("run_id required")
    if step_index < 0:
        raise ValueError("step_index must be non-negative")
    record: Dict[str, Any] = {
        "schema_id": SCHEMA_ID,
        "run_id": run_id,
        "step_index": int(step_index),
        "phi1": float(phi1),
        "state_fingerprint": state_fingerprint,
        "authority_effect": "None",
        "dda_letter": dda_letter,
        "name": name,
        "note": note,
        "emitted_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if stage is not None:
        record["stage"] = stage
    if date is not None:
        record["date"] = date
    if extra:
        for k, v in extra.items():
            if k not in record:
                record[k] = v
    if chain:
        record["prev_step_hash"] = prev_step_hash
        record["step_hash"] = _step_hash(record)
    return record


def upgrade_legacy_record(
    legacy: Dict[str, Any],
    *,
    step_index: int,
    phi1: float = 0.0,
    state_fingerprint: Optional[str] = None,
    prev_step_hash: Optional[str] = None,
    chain: bool = True,
) -> Dict[str, Any]:
    """Map a LEGACY_PROCESS_TAPE line into INTEGRITY_V1 without inventing authority.

    ``phi1`` defaults to 0.0 = **declared unmeasured residual energy**, not a
    computed Φ₁ unless the caller supplies a measured value.
    """
    run_id = str(legacy.get("run_id") or "")
    if not run_id:
        raise ValueError("legacy record missing run_id")
    fp = state_fingerprint or _state_fingerprint(
        {
            "stage": legacy.get("stage"),
            "dda_letter": legacy.get("dda_letter"),
            "name": legacy.get("name"),
            "note": legacy.get("note"),
            "date": legacy.get("date"),
        }
    )
    return emit_integrity_v1_record(
        run_id=run_id,
        step_index=step_index,
        phi1=phi1,
        state_fingerprint=fp,
        dda_letter=str(legacy.get("dda_letter") or ""),
        name=str(legacy.get("name") or ""),
        note=str(legacy.get("note") or ""),
        stage=legacy.get("stage") if isinstance(legacy.get("stage"), int) else None,
        date=str(legacy["date"]) if legacy.get("date") is not None else None,
        prev_step_hash=prev_step_hash,
        chain=chain,
        extra={"upgraded_from": "LEGACY_PROCESS_TAPE"},
    )


@dataclass
class OrtTrajectoryEmitter:
    """Append-only ORT sprint trajectory writer (INTEGRITY_V1)."""

    run_id: str
    records: List[Dict[str, Any]] = field(default_factory=list)
    _last_hash: Optional[str] = field(default=None, repr=False)

    def emit_step(
        self,
        *,
        phi1: float,
        state: Any,
        dda_letter: str = "",
        name: str = "",
        note: str = "",
        stage: Optional[int] = None,
        date: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
        chain: bool = True,
    ) -> Dict[str, Any]:
        rec = emit_integrity_v1_record(
            run_id=self.run_id,
            step_index=len(self.records),
            phi1=phi1,
            state_fingerprint=_state_fingerprint(state),
            dda_letter=dda_letter,
            name=name,
            note=note,
            stage=stage,
            date=date,
            prev_step_hash=self._last_hash,
            chain=chain,
            extra=extra,
        )
        self.records.append(rec)
        if chain:
            self._last_hash = rec.get("step_hash")
        return rec

    def append_ndjson(self, path: PathLike) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            for rec in self.records:
                fh.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

    def validate(self, *, require_integrity_v1: bool = True):
        return validate_dda_sprint_trajectory(
            self.records, require_integrity_v1=require_integrity_v1
        )


def emit_upgraded_tape_from_legacy(
    legacy_records: Sequence[Dict[str, Any]],
    *,
    phi1_per_step: Optional[Sequence[float]] = None,
) -> List[Dict[str, Any]]:
    """Upgrade a sequence of legacy process lines to INTEGRITY_V1 (in memory)."""
    out: List[Dict[str, Any]] = []
    prev: Optional[str] = None
    for i, leg in enumerate(legacy_records):
        phi = 0.0
        if phi1_per_step is not None and i < len(phi1_per_step):
            phi = float(phi1_per_step[i])
        rec = upgrade_legacy_record(
            leg, step_index=i, phi1=phi, prev_step_hash=prev, chain=True
        )
        prev = rec.get("step_hash")
        out.append(rec)
    return out



