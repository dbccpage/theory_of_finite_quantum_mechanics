"""Hash-chained DDA trace emission with explicit residual semantics."""

from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from omega_engine_governance.contracts.dda_packets import DDATapeDFA
from omega_engine.crates.type.runtime_axes import DdaDialect, DdaLetter


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return Path(__file__).resolve().parents[2]


def _get_default_trace_dir() -> Path:
    trace_dir = (
        _find_repo_root(Path(__file__).resolve().parent) / "_intelligence" / "dda_traces"
    )
    trace_dir.mkdir(parents=True, exist_ok=True)
    return trace_dir


def _step_hash(record: Dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "step_hash"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _default_effect(letter: str) -> str:
    return {
        "C": "context_exposed",
        "R": "residual_carried",
        "E": "obstruction_eliminated",
        "I": "integration",
        "Λ": "structure_added",
        "Lambda": "structure_added",
        "L": "structure_added",
        "D": "descent",
        "M": "refusal",
        "Z": "refusal",
        "T": "terminalization",
    }.get(letter, "unclassified")


class TraceLogger:
    """Append-only JSONL logger for replayable letter-algebra experiments.

    ``experimental-z-v1`` is deliberately non-canonical.  In that dialect a
    refused or still-unresolved target is recorded as ``Z·T`` and retains its
    residual.  It is never counted as an obstruction removal.
    """

    def __init__(
        self,
        runner_id: str,
        campaign_name: str = "",
        trace_dir: Optional[Path] = None,
        dialect: DdaDialect | str = DdaDialect.LEGACY_V1,
        auto_lifecycle: bool = True,
    ) -> None:
        self.runner_id = runner_id
        self.campaign_name = campaign_name or runner_id
        self.trace_dir = Path(trace_dir) if trace_dir else _get_default_trace_dir()
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.dialect = (
            dialect.value if isinstance(dialect, DdaDialect) else str(dialect)
        )
        self.auto_lifecycle = auto_lifecycle
        self.run_id = uuid.uuid4().hex[:12]
        safe_runner = (
            re.sub(r"[^A-Za-z0-9_.-]+", "_", self.runner_id).strip("_") or "runner"
        )
        self.jsonl_path = (
            self.trace_dir / f"{safe_runner}_{self.run_id}_dda_trace.jsonl"
        )
        self._last_hash: Optional[str] = None
        self._step_counter = 0
        self._finalized = False
        self.steps: List[Dict[str, Any]] = []

    @property
    def tape(self) -> List[str]:
        return [str(step["letter"]) for step in self.steps]

    def __enter__(self) -> "TraceLogger":
        if self.auto_lifecycle:
            start_letter = (
                DdaLetter.R
                if self.dialect == DdaDialect.EXPERIMENTAL_Z_V1.value
                else DdaLetter.C
            )
            self.record_step(
                letter=start_letter,
                action_name=f"start:{self.runner_id}",
                input_state=f"INITIAL_EXPOSURE:{self.runner_id}",
                output_state=f"RUNNING:{self.runner_id}",
                witness=f"WIT_START_{self.run_id}",
                effect="context_exposed",
            )
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._finalized or not self.auto_lifecycle:
            return
        if exc_type is not None:
            self.refuse(
                reason=str(exc_val) or exc_type.__name__,
                input_state=f"RUNNING:{self.runner_id}",
                output_state=f"FAILED:{self.runner_id}",
                witness=f"WIT_FAIL_{self.run_id}",
            )
        else:
            self.finalize_success(
                input_state=f"RUNNING:{self.runner_id}",
                output_state=f"COMPLETED:{self.runner_id}",
                witness=f"WIT_INTEGRATE_{self.run_id}",
            )

    def record_step(
        self,
        letter: DdaLetter | str,
        action_name: str,
        input_state: str,
        output_state: str,
        witness: str,
        residual_energy: Optional[float] = None,
        refusal_reason: Optional[str] = None,
        cochain_dim: str = "C1",
        coboundary_map: str = "d1",
        *,
        residual_before: Optional[float] = None,
        residual_after: Optional[float] = None,
        effect: Optional[str] = None,
        obstruction_id: Optional[str] = None,
        structure_delta: Optional[Dict[str, Any]] = None,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self._finalized:
            raise RuntimeError("Cannot append a DDA step after terminalization.")

        letter_str = letter.value if isinstance(letter, DdaLetter) else str(letter)
        after = residual_after if residual_after is not None else residual_energy
        energy = 0.0 if after is None else float(after)
        effect_value = effect or _default_effect(letter_str)
        if letter_str == "Z":
            if self.dialect != DdaDialect.EXPERIMENTAL_Z_V1.value:
                raise ValueError("Z is only valid in the experimental-z-v1 dialect.")
            if effect_value != "refusal":
                raise ValueError("Z is a refusal and cannot carry another effect.")
            if residual_before is not None and after is not None:
                if float(residual_before) != float(after):
                    raise ValueError("Z must retain the unresolved residual unchanged.")
        if letter_str == "E" and effect_value != "obstruction_eliminated":
            raise ValueError("DDA letter E requires the obstruction_eliminated effect.")
        if letter_str in {"L", "Lambda", "Λ"} and effect_value != "structure_added":
            raise ValueError("A lift letter requires the structure_added effect.")
        if effect_value == "obstruction_eliminated" and letter_str in {"M", "Z"}:
            raise ValueError("A refusal letter cannot eliminate an obstruction.")
        if effect_value == "obstruction_eliminated":
            if letter_str != "E":
                raise ValueError("Obstruction elimination requires DDA letter E.")
            if not obstruction_id:
                raise ValueError("Obstruction elimination requires an obstruction id.")
            if residual_before is None or after is None:
                raise ValueError(
                    "Obstruction elimination requires before/after residuals."
                )
            if not math.isfinite(float(residual_before)) or not math.isfinite(
                float(after)
            ):
                raise ValueError("Obstruction elimination residuals must be finite.")
            if float(after) >= float(residual_before):
                raise ValueError(
                    "Obstruction elimination requires strict residual decrease."
                )
        if effect_value == "structure_added":
            if letter_str not in {"L", "Lambda", "Λ"}:
                raise ValueError("Structure addition requires a lift letter.")
            if not structure_delta:
                raise ValueError(
                    "Structure addition requires a nonempty structure delta."
                )

        candidate_tape = ".".join([*self.tape, letter_str])
        is_terminal = letter_str == "T" or (
            letter_str == "M" and self.dialect == DdaDialect.OEARS_V1.value
        )
        if is_terminal:
            DDATapeDFA.validate(candidate_tape, dialect=self.dialect)
        else:
            DDATapeDFA.validate_prefix(candidate_tape, dialect=self.dialect)

        self._step_counter += 1
        delta = None
        if residual_before is not None and after is not None:
            delta = float(after) - float(residual_before)

        record: Dict[str, Any] = {
            "schema_version": "omega.dda.trace.v2",
            "dda_dialect": self.dialect,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "runner_id": self.runner_id,
            "campaign": self.campaign_name,
            "run_id": self.run_id,
            "step_id": f"DDA_STEP_{self._step_counter:03d}",
            "letter": letter_str,
            "effect": effect_value,
            "action_name": action_name,
            "cochain_dim": cochain_dim,
            "coboundary_map": coboundary_map,
            "input_state": input_state,
            "output_state": output_state,
            "witness": witness,
            "obstruction_id": obstruction_id,
            "residual_before": residual_before,
            "residual_after": after,
            "residual_delta": delta,
            "residual_energy": energy,
            "structure_delta": structure_delta or {},
            "evidence": evidence or {},
            "refusal_reason": refusal_reason,
            "authority_effect": "None",
            "prev_step_hash": self._last_hash,
        }
        record["step_hash"] = _step_hash(record)
        self._last_hash = record["step_hash"]
        self.steps.append(record)

        with self.jsonl_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, default=str) + "\n")

        if letter_str == "T" or (
            letter_str == "M" and self.dialect == DdaDialect.OEARS_V1.value
        ):
            self._finalized = True
        return record

    def finalize_success(
        self,
        input_state: str,
        output_state: str,
        witness: str,
        *,
        residual: Optional[float] = None,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.record_step(
            letter=DdaLetter.I,
            action_name=f"integrate:{self.runner_id}",
            input_state=input_state,
            output_state=output_state,
            witness=witness,
            residual_before=residual,
            residual_after=residual,
            effect="integration",
            evidence=evidence,
        )
        self.record_step(
            letter=DdaLetter.T,
            action_name=f"terminalize:{self.runner_id}",
            input_state=output_state,
            output_state=f"TERMINALIZED:{self.runner_id}",
            witness=f"WIT_TERMINAL_{self.run_id}",
            residual_before=residual,
            residual_after=residual,
            effect="terminalization",
        )

    def refuse(
        self,
        reason: str,
        input_state: str,
        output_state: str,
        witness: str,
        *,
        residual: Optional[float] = None,
        obstruction_id: Optional[str] = None,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> None:
        refusal_letter = (
            "Z" if self.dialect == DdaDialect.EXPERIMENTAL_Z_V1.value else "M"
        )
        self.record_step(
            letter=refusal_letter,
            action_name=f"refuse:{self.runner_id}",
            input_state=input_state,
            output_state=output_state,
            witness=witness,
            residual_before=residual,
            residual_after=residual,
            effect="refusal",
            obstruction_id=obstruction_id,
            refusal_reason=reason,
            evidence=evidence,
        )
        if self.dialect != DdaDialect.OEARS_V1.value:
            self.record_step(
                letter=DdaLetter.T,
                action_name=f"terminalize:{self.runner_id}",
                input_state=output_state,
                output_state=f"TERMINALIZED:{self.runner_id}",
                witness=f"WIT_TERMINAL_{self.run_id}",
                residual_before=residual,
                residual_after=residual,
                effect="terminalization",
            )


