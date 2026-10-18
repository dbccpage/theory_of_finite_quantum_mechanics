"""DDA Operation & Trace Tape Recorder for omega_engine/dda.

Records DDA steps (Foundation, DDA Step, Window Lift, Termination) and outputs
structured trace logs and DAG JSON files into this `code/` directory
(`latest_dda_trace.json`). Set `CODA_DDA_TRACE_MIRROR_DIR` to opt in to an
external mirror.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class DDAOperationRecord:
    operation_id: str
    operation_type: str  # e.g., 'FOUNDATION', 'DDA_STEP', 'WINDOW_LIFT', 'TERMINATION'
    tape_token: str       # e.g., 'E', 'R', 'C', 'I', 'L', 'Λ', 'D', 'M', 'T'
    residual_before: float
    residual_after: float
    delta_residual: float
    authority_effect: str = "None"
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DDATraceRecorder:
    """Recorder for logging DDA operations and emitting DAG trace receipts."""

    def __init__(self, trace_dir: Optional[str] = None):
        if trace_dir is None:
            self.trace_dir = Path(__file__).resolve().parent
        else:
            self.trace_dir = Path(trace_dir)

        self.trace_dir.mkdir(parents=True, exist_ok=True)

        # External trace mirroring is opt-in; this package must not infer or
        # create repository-escaping paths during ordinary tests.
        self.agents_dir: Optional[Path] = None
        mirror_dir = os.environ.get("CODA_DDA_TRACE_MIRROR_DIR")
        if mirror_dir:
            try:
                workspace_dir = Path(mirror_dir)
                workspace_dir.mkdir(parents=True, exist_ok=True)
                probe = workspace_dir / ".write_probe"
                probe.write_text("", encoding="utf-8")
                probe.unlink(missing_ok=True)
                self.agents_dir = workspace_dir
            except OSError:
                self.agents_dir = None

        self.records: List[DDAOperationRecord] = []
        self.tape: List[str] = []

    def record_step(
        self,
        op_type: str,
        tape_token: str,
        res_before: float,
        res_after: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DDAOperationRecord:
        """Record an individual DDA step."""
        op_id = f"dda_op_{len(self.records):04d}_{int(time.time()*1000)}"
        rec = DDAOperationRecord(
            operation_id=op_id,
            operation_type=op_type,
            tape_token=tape_token,
            residual_before=res_before,
            residual_after=res_after,
            delta_residual=res_before - res_after,
            metadata=metadata or {},
        )
        self.records.append(rec)
        self.tape.append(tape_token)
        self.flush_to_disk()
        return rec

    def flush_to_disk(self) -> None:
        """Write trace record log and DAG trace JSON to disk."""
        tape_str = "".join(self.tape)
        data = {
            "tape": self.tape,
            "tape_sequence": tape_str,
            "total_steps": len(self.records),
            "operations": [asdict(r) for r in self.records],
        }

        trace_file = self.trace_dir / "latest_dda_trace.json"
        with open(trace_file, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)

        if self.agents_dir:
            agents_file = self.agents_dir / "latest_dda_trace.json"
            with open(agents_file, "w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=2)


_global_recorder: Optional[DDATraceRecorder] = None


def get_global_trace_recorder() -> DDATraceRecorder:
    """Retrieve or initialize the global descent trace recorder."""
    global _global_recorder
    if _global_recorder is None:
        _global_recorder = DDATraceRecorder()
    return _global_recorder


DescentTraceRecorder = DDATraceRecorder
DescentOperationRecord = DDAOperationRecord
