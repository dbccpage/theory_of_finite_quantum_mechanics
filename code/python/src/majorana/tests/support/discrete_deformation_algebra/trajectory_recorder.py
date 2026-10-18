"""Real-World Discrete Deformation Calculus (DDC) Trajectory Recorder.

Records actual human and agent reasoning steps, primitive differences, state transitions,
and cochain/obstruction energy changes to JSON-L and Markdown trajectory logs.

Honesty constraints
-------------------
- The square-zero report is **computed** from a supplied cochain complex via
  ``FiniteCochainComplex.complex_defect()``. With no complex it reports
  ``NOT_COMPUTED``; with a defective one it reports ``REFUTED``. It is never
  stamped ``VERIFIED`` on the strength of a letter or a label.
- ``lift_label`` / ``projection_label`` / ``invariant_claim`` are **descriptive
  strings supplied by the caller**. No functor laws are checked and no invariant
  is verified, so they are named as labels and claims rather than as functors and
  facts.
- Residual energy is reported exactly as supplied. It is not zeroed on the basis
  of the DDA letter, because a diagnostic derived from the author's own label
  cannot fail.
- Every record is chained to its predecessor, so a dropped, reordered, or edited
  step is detectable by ``verify_trajectory_chain``.

AuthorityEffect: None. These records are diagnostic; they mint no authority.
"""

from __future__ import annotations
import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .dda import DdaTraceEngine
from omega_engine.crates.homology_theory.finite_cochain_complex import FiniteCochainComplex
from omega_engine.crates.type.runtime_axes import DdaLetter

SQUARE_ZERO_VERIFIED = "VERIFIED"
SQUARE_ZERO_REFUTED = "REFUTED"
SQUARE_ZERO_NOT_COMPUTED = "NOT_COMPUTED"
SQUARE_ZERO_VACUOUS = "VACUOUS"

_HASH_EXCLUDED = ("step_hash",)


def _step_hash(record: Dict[str, Any]) -> str:
    """Hash every field except the hash itself; ``prev_step_hash`` is inside the payload."""
    payload = {k: v for k, v in record.items() if k not in _HASH_EXCLUDED}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def verify_trajectory_chain(records: Sequence[Dict[str, Any]]) -> Tuple[bool, str]:
    """Re-derive every step hash and confirm the chain links.

    Returns ``(ok, detail)``. Detects edited fields, dropped steps, and reordering.
    Records from more than one run are refused: filter by ``run_id`` first.
    """
    if not records:
        return True, "empty trajectory"

    run_ids = {record.get("run_id") for record in records}
    if len(run_ids) != 1:
        return False, f"records span {len(run_ids)} runs: {sorted(map(str, run_ids))}"

    previous_hash: Optional[str] = None
    for index, record in enumerate(records):
        step_id = record.get("step_id", f"<index {index}>")

        recomputed = _step_hash(record)
        if recomputed != record.get("step_hash"):
            return False, f"{step_id}: content does not match its step_hash (edited)"

        if record.get("prev_step_hash") != previous_hash:
            return False, (
                f"{step_id}: prev_step_hash does not match the preceding step "
                "(dropped or reordered)"
            )
        previous_hash = recomputed

    return True, f"chain intact across {len(records)} steps"


class RealWorldDdaTrajectoryRecorder:
    """Records real-world reasoning and execution steps as DDA cochain transitions."""

    def __init__(
        self,
        campaign_name: str,
        log_dir: Optional[Path] = None,
        cochain_complex: Optional[FiniteCochainComplex] = None,
    ):
        self.campaign_name = campaign_name
        self.log_dir = (
            Path(log_dir)
            if log_dir is not None
            else (
                Path(__file__).resolve().parents[2]
                / "omega_engine"
                / "research"
                / "product_planning_office"
                / "sprints"
                / "dda_trajectories"
            )
        )
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.cochain_complex = cochain_complex
        self.run_id = uuid.uuid4().hex[:12]
        self.engine = DdaTraceEngine(campaign_name)
        self.jsonl_path = self.log_dir / f"{campaign_name}_trajectory.jsonl"
        self.markdown_path = self.log_dir / f"{campaign_name}_trajectory.md"
        self.steps: List[Dict[str, Any]] = []
        self._last_hash: Optional[str] = None

    def square_zero_status(self) -> str:
        """Compute d^k . d^(k-1) on the supplied complex, or report that nothing ran."""
        if self.cochain_complex is None:
            return SQUARE_ZERO_NOT_COMPUTED
        if self.cochain_complex.c2_dimension == 0:
            # No 2-cochains means no composite exists to check. "All zero" over an
            # empty family is true but says nothing; VERIFIED here would overclaim.
            return SQUARE_ZERO_VACUOUS
        defect = self.cochain_complex.complex_defect()
        is_zero = all(entry == 0 for row in defect for entry in row)
        return SQUARE_ZERO_VERIFIED if is_zero else SQUARE_ZERO_REFUTED

    def record_step(
        self,
        action_name: str,
        input_state_desc: str,
        output_state_desc: str,
        dda_letter: DdaLetter,
        witness_desc: str,
        residual_obstruction_energy: float = 0.0,
        refusal_reason: Optional[str] = None,
        cochain_dim: str = "C1",
        coboundary_map: str = "d1",
        invariant_claim: str = "AuthorityEffect=None",
        lift_label: Optional[str] = None,
        projection_label: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record a single real-world reasoning or system step."""
        # Reported as supplied at both ends: the recorder does not measure energy,
        # and deriving the exit value from the letter would make it unfalsifiable.
        diagnostic = f"Energy={residual_obstruction_energy:.2f}"

        receipt = self.engine.emit_step(
            letter=dda_letter,
            input_state=input_state_desc,
            output_state=output_state_desc,
            carrier=action_name,
            diag_before=diagnostic,
            diag_after=diagnostic,
            witness=witness_desc,
            refusal_reason=refusal_reason,
        )

        record: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "campaign": self.campaign_name,
            "run_id": self.run_id,
            "step_id": receipt.step_id,
            "dda_letter": dda_letter.value,
            "action_name": action_name,
            "cochain_dim": cochain_dim,
            "coboundary_map": coboundary_map,
            "invariant_claim": invariant_claim,
            "lift_label": lift_label
            or f"lift({action_name}) -> {dda_letter.value} in {cochain_dim}",
            "projection_label": projection_label
            or f"project({cochain_dim}) -> '{action_name}'",
            "input_state": input_state_desc,
            "output_state": output_state_desc,
            "witness": witness_desc,
            "residual_energy": residual_obstruction_energy,
            "diagnostic_before": diagnostic,
            "diagnostic_after": diagnostic,
            "refusal_reason": refusal_reason,
            "input_hash": receipt.input_state_hash,
            "output_hash": receipt.output_state_hash,
            "witness_hash": receipt.witness_hash,
            "square_zero_status": self.square_zero_status(),
            "authority_effect": "None",
            "prev_step_hash": self._last_hash,
        }
        record["step_hash"] = _step_hash(record)
        self._last_hash = record["step_hash"]

        self.steps.append(record)
        self._write_jsonl(record)
        self._write_markdown()
        return record

    def _write_jsonl(self, record: Dict[str, Any]) -> None:
        with open(self.jsonl_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")

    def _write_markdown(self) -> None:
        status = self.square_zero_status()
        chain_ok, chain_detail = verify_trajectory_chain(self.steps)

        lines = [
            f"# DDA Homological & Real-World Execution Trajectory: {self.campaign_name}",
            "",
            f"**Run ID:** `{self.run_id}`  ",
            f"**Recorded at:** `{datetime.now(timezone.utc).isoformat()}`  ",
            f"**Tape String:** `{self.engine.get_tape_string()}`  ",
            "**AuthorityEffect:** `None`  ",
            "",
            "## Homological Cochain Execution Sequence",
            "",
            "| Step ID | Letter | Cochain | Coboundary | Action / Operation | Lift label | Invariant claim (unverified) | Witness | Witness hash | Step hash |",
            "| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for step in self.steps:
            lines.append(
                f"| `{step['step_id']}` | `{step['dda_letter']}` | `{step['cochain_dim']}` "
                f"| `{step['coboundary_map']}` | **{step['action_name']}** "
                f"| `{step['lift_label']}` | `{step['invariant_claim']}` | {step['witness']} "
                f"| `{step['witness_hash'][:16]}` | `{step['step_hash'][:16]}` |"
            )

        lines.extend(
            [
                "",
                "## Homological Algebra & DDA Verification Summary",
                "",
                f"- **Total Steps Recorded:** {len(self.steps)}",
                f"- **Tape Sequence:** `{self.engine.get_tape_string()}`",
                f"- **Square-Zero Check ($d^k \\circ d^{{k-1}} = 0$):** `{status}`",
                f"- **Receipt Chain:** `{'INTACT' if chain_ok else 'BROKEN'}` — {chain_detail}",
                f"- **Terminal Status:** `{'TERMINALIZED' if self.engine.is_terminalized else 'IN_PROGRESS'}`",
                f"- **Law 1 Compliance (AuthorityEffect None):** `{self.engine.check_law1_all_none()}`",
                "",
                "### What these rows do and do not establish",
                "",
                "- `Lift label` and `Invariant claim` are descriptive strings supplied by the",
                "  caller. No functor law is checked and no invariant is verified.",
                f"- The square-zero row is computed from a supplied cochain complex. `{SQUARE_ZERO_NOT_COMPUTED}`",
                "  means no complex was supplied and no check ran.",
                "- Residual energy is reported as supplied; the recorder does not measure it.",
            ]
        )

        self.markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



