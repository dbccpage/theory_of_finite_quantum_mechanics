"""DDA Operation & Trace Tape Recorder for omega_engine/dda.

Records DDA steps (Foundation, DDA Step, Window Lift, Termination) and outputs
structured trace logs and DAG JSON files into:
- omega_engine/dda/traces/
- _intelligence/dda_traces/

AuthorityEffect: None.
"""

from __future__ import annotations
import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from omega_engine.crates.type.refusal import Refusal, Result
from omega_engine.crates.type.witness import IdentityWitness


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
            base_dir = Path(__file__).resolve().parents[2] / "_intelligence"
            self.trace_dir = base_dir / "traces_dda"
        else:
            self.trace_dir = Path(trace_dir)

        self.trace_dir.mkdir(parents=True, exist_ok=True)

        workspace_dir = Path(__file__).resolve().parents[4] / "_intelligence" / "dda_traces"
        try:
            workspace_dir.mkdir(parents=True, exist_ok=True)
            self.agents_dir: Optional[Path] = workspace_dir
        except Exception:
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
    """Retrieve or initialize the global DDA trace recorder."""
    global _global_recorder
    if _global_recorder is None:
        _global_recorder = DDATraceRecorder()
    return _global_recorder



