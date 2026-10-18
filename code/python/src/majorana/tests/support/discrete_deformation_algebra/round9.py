"""Round 9 Red Team Audit — Hard Runtime Invariants Implementation.

Enforces:
1. DiagnosticResidualPacket closed family registry & source_locus validation.
2. LossLedger unresolved loss monotonicity across sequential projection adapters (A -> S -> K).
3. GlobalRunEnvelope & ReentryReceipt budget subtraction and trace containment for CODA re-entry.
"""

from __future__ import annotations
import enum
import hashlib
from dataclasses import field
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple


class DiagnosticFamily(str, enum.Enum):
    GrammarRepairPacket = "GrammarRepairPacket"
    ModelSelectionResidual = "ModelSelectionResidual"
    UnitGaugePacket = "UnitGaugePacket"
    OutputTypeResidual = "OutputTypeResidual"
    ParameterCompletenessResidual = "ParameterCompletenessResidual"
    TaskIntentPacket = "TaskIntentPacket"


@dataclass(frozen=True)
class SourceLocus:
    artifact_hash: str
    span_start: int
    span_end: int
    source_text_hash: str


@dataclass
class DiagnosticResidualPacket:
    family_id: str
    family_version: str
    source_locus: SourceLocus
    carrier: Dict[str, str]
    observer: Dict[str, str]
    primitive_difference: Dict[str, str]
    zero_rel: Dict[str, str]
    witness_or_refusal: Dict[str, Any]
    residual_fingerprint: str
    support_grade: str = "DiagnosticOnly"
    authority_effect: str = "None"
    additional_fields: Dict[str, Any] = field(default_factory=dict)


def compute_content_addressed_fingerprint(
    family_id: str,
    artifact_hash: str,
    span_start: int,
    span_end: int,
    observer_id: str,
    zero_rel_id: str,
    diff_id: str,
) -> str:
    """Compute content-addressed SHA256 fingerprint for a diagnostic residual packet."""
    raw_key = f"{family_id}|{artifact_hash}|{span_start}|{span_end}|{observer_id}|{zero_rel_id}|{diff_id}"
    return "fp_" + hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]


def verify_content_addressed_fingerprint(packet_dict: Dict[str, Any]) -> str:
    """Verify that a packet's residual_fingerprint matches its content-addressed formula."""
    family_id = str(packet_dict.get("family_id", ""))
    locus = packet_dict.get("source_locus") or {}
    obs = packet_dict.get("observer") or {}
    zero = packet_dict.get("zero_rel") or {}
    diff = packet_dict.get("primitive_difference") or {}

    artifact_hash = str(locus.get("artifact_hash", ""))
    span_start = int(locus.get("span_start", 0))
    span_end = int(locus.get("span_end", 0))

    observer_id = str(obs.get("observer_id", ""))
    zero_rel_id = str(zero.get("zero_rel_id", ""))
    diff_id = str(diff.get("diff_id", ""))

    expected_fp = compute_content_addressed_fingerprint(
        family_id=family_id,
        artifact_hash=artifact_hash,
        span_start=span_start,
        span_end=span_end,
        observer_id=observer_id,
        zero_rel_id=zero_rel_id,
        diff_id=diff_id,
    )

    actual_fp = str(packet_dict.get("residual_fingerprint", ""))
    if actual_fp != expected_fp:
        raise ValueError(
            f"Content-addressed fingerprint mismatch: expected '{expected_fp}', got arbitrary string '{actual_fp}'"
        )

    return expected_fp


def validate_diagnostic_packet(
    packet_dict: Dict[str, Any], verify_fingerprint: bool = False
) -> DiagnosticResidualPacket:
    """Validate a raw diagnostic packet dict against Round 9 hard constraints.

    Rejects unknown fields, unregistered family IDs, missing source_locus, invalid authority/support grade.
    If verify_fingerprint is True, rejects arbitrary static fingerprints.
    """
    allowed_keys = {
        "family_id",
        "family_version",
        "source_locus",
        "carrier",
        "observer",
        "primitive_difference",
        "zero_rel",
        "witness_or_refusal",
        "residual_fingerprint",
        "support_grade",
        "authority_effect",
    }

    extra_keys = set(packet_dict.keys()) - allowed_keys
    if extra_keys:
        raise ValueError(
            f"Diagnostic validation failed: unknown fields detected {sorted(list(extra_keys))}"
        )

    family_id = packet_dict.get("family_id")
    valid_families = {f.value for f in DiagnosticFamily}
    if not family_id or family_id not in valid_families:
        raise ValueError(
            f"Diagnostic validation failed: family_id '{family_id}' not in closed registry {sorted(list(valid_families))}"
        )

    locus_raw = packet_dict.get("source_locus")
    if not locus_raw or not isinstance(locus_raw, dict):
        raise ValueError(
            "Diagnostic validation failed: source_locus anchor is required"
        )

    if not locus_raw.get("artifact_hash") or not locus_raw.get("source_text_hash"):
        raise ValueError(
            "Diagnostic validation failed: source_locus missing required artifact_hash or source_text_hash"
        )

    if not packet_dict.get("observer"):
        raise ValueError(
            "Diagnostic validation failed: observer identification is required"
        )
    if not packet_dict.get("zero_rel"):
        raise ValueError(
            "Diagnostic validation failed: zero_rel specification is required"
        )

    if packet_dict.get("support_grade", "DiagnosticOnly") != "DiagnosticOnly":
        raise ValueError(
            f"Diagnostic validation failed: support_grade must be 'DiagnosticOnly', got '{packet_dict.get('support_grade')}'"
        )

    if packet_dict.get("authority_effect", "None") != "None":
        raise ValueError(
            f"Diagnostic validation failed: authority_effect must be 'None', got '{packet_dict.get('authority_effect')}'"
        )

    if verify_fingerprint:
        verify_content_addressed_fingerprint(packet_dict)

    locus = SourceLocus(
        artifact_hash=locus_raw["artifact_hash"],
        span_start=int(locus_raw.get("span_start", 0)),
        span_end=int(locus_raw.get("span_end", 0)),
        source_text_hash=locus_raw["source_text_hash"],
    )

    return DiagnosticResidualPacket(
        family_id=family_id,
        family_version=str(packet_dict.get("family_version", "v1")),
        source_locus=locus,
        carrier=dict(packet_dict.get("carrier", {})),
        observer=dict(packet_dict.get("observer", {})),
        primitive_difference=dict(packet_dict.get("primitive_difference", {})),
        zero_rel=dict(packet_dict.get("zero_rel", {})),
        witness_or_refusal=dict(packet_dict.get("witness_or_refusal", {})),
        residual_fingerprint=str(packet_dict.get("residual_fingerprint", "")),
        support_grade="DiagnosticOnly",
        authority_effect="None",
    )




@dataclass
class LossEntry:
    loss_id: str
    source_anchor: str
    original_carrier: str
    current_carrier_status: str
    discharge_status: str
    discharge_receipt: Optional[str] = None
    authority_effect: str = "None"


class LossMonotonicityViolationError(Exception):
    pass


@dataclass
class LossLedger:
    entries: Dict[str, LossEntry] = field(default_factory=dict)

    def add_entry(self, entry: LossEntry) -> None:
        self.entries[entry.loss_id] = entry

    def pushforward(
        self,
        adapter_name: str,
        target_carrier: str,
        projected_away_loci: Set[str],
        new_losses: List[LossEntry] = None,
        coherence_loss: Optional[LossEntry] = None,
    ) -> LossLedger:
        """Transport loss ledger into target carrier frame.

        Enforces:
        - Unresolved losses cannot be silently deleted during projection.
        - Projection updates carrier_status to 'projected_away' while retaining the entry.
        """
        new_ledger = LossLedger()

        for loss_id, entry in self.entries.items():
            new_status = entry.current_carrier_status
            if entry.source_anchor in projected_away_loci:
                new_status = "projected_away"

            transported_entry = LossEntry(
                loss_id=entry.loss_id,
                source_anchor=entry.source_anchor,
                original_carrier=entry.original_carrier,
                current_carrier_status=new_status,
                discharge_status=entry.discharge_status,
                discharge_receipt=entry.discharge_receipt,
                authority_effect="None",
            )
            new_ledger.add_entry(transported_entry)

        if new_losses:
            for nl in new_losses:
                new_ledger.add_entry(nl)

        if coherence_loss:
            new_ledger.add_entry(coherence_loss)

        source_unresolved = {
            lid for lid, e in self.entries.items() if e.discharge_status == "unresolved"
        }
        target_unresolved = {
            lid
            for lid, e in new_ledger.entries.items()
            if e.discharge_status == "unresolved"
        }

        missing = source_unresolved - target_unresolved
        if missing:
            raise LossMonotonicityViolationError(
                f"Loss monotonicity violated by adapter '{adapter_name}': unresolved loss IDs {sorted(list(missing))} were dropped"
            )

        return new_ledger

    def discharge(self, loss_id: str, receipt_id: str) -> None:
        if loss_id not in self.entries:
            raise KeyError(f"Loss ID '{loss_id}' not found in ledger")
        entry = self.entries[loss_id]
        self.entries[loss_id] = LossEntry(
            loss_id=entry.loss_id,
            source_anchor=entry.source_anchor,
            original_carrier=entry.original_carrier,
            current_carrier_status="discharged",
            discharge_status="discharged",
            discharge_receipt=receipt_id,
            authority_effect="None",
        )




class ReentryLaunderingError(Exception):
    pass


@dataclass
class GlobalRunEnvelope:
    root_run_id: str
    root_artifact_hash: str
    global_budget_total: float
    global_budget_remaining: float
    reentry_depth: int = 0
    max_reentry_depth: int = 5
    residual_fingerprint_history: List[str] = field(default_factory=list)
    trace_roots: List[str] = field(default_factory=list)
    authority_effect: str = "None"


@dataclass
class ReentryReceipt:
    receipt_id: str
    parent_trace_root: str
    child_trace_id: str
    residual_locus: str
    budget_consumed: float
    budget_remaining: float
    inherited_global_budget: bool = True
    inherited_fingerprint_history: bool = True
    authority_effect: str = "None"


def execute_coda_reentry(
    envelope: GlobalRunEnvelope,
    parent_trace_id: str,
    child_carrier: str,
    residual_locus: str,
    residual_fingerprint: str,
    delta_control: float = 1.0,
) -> Tuple[GlobalRunEnvelope, ReentryReceipt]:
    """Execute legal CODA re-entry from parent carrier to child carrier.

    Enforces:
    - Parent trace must exist in global envelope trace_roots.
    - Global budget is decayed by delta_control (B_child <= B_parent - delta_control).
    - Fingerprint history is inherited and appended.
    - Reentry depth ceiling is enforced.
    """
    if parent_trace_id not in envelope.trace_roots:
        raise ReentryLaunderingError(
            f"Re-entry refused: parent trace '{parent_trace_id}' not contained in global envelope trace roots {envelope.trace_roots}"
        )

    if envelope.reentry_depth >= envelope.max_reentry_depth:
        raise ReentryLaunderingError(
            f"Re-entry refused: maximum re-entry depth ({envelope.max_reentry_depth}) exceeded"
        )

    if envelope.global_budget_remaining < delta_control:
        raise ReentryLaunderingError(
            f"Re-entry refused: remaining budget ({envelope.global_budget_remaining}) insufficient for cost floor delta_control ({delta_control})"
        )

    child_trace_id = f"trace_{child_carrier}_{envelope.reentry_depth + 1}"
    new_remaining_budget = envelope.global_budget_remaining - delta_control

    new_fingerprint_history = list(envelope.residual_fingerprint_history) + [
        residual_fingerprint
    ]
    new_trace_roots = list(envelope.trace_roots) + [child_trace_id]

    updated_envelope = GlobalRunEnvelope(
        root_run_id=envelope.root_run_id,
        root_artifact_hash=envelope.root_artifact_hash,
        global_budget_total=envelope.global_budget_total,
        global_budget_remaining=new_remaining_budget,
        reentry_depth=envelope.reentry_depth + 1,
        max_reentry_depth=envelope.max_reentry_depth,
        residual_fingerprint_history=new_fingerprint_history,
        trace_roots=new_trace_roots,
        authority_effect="None",
    )

    receipt = ReentryReceipt(
        receipt_id=f"receipt_reentry_{envelope.reentry_depth + 1}",
        parent_trace_root=parent_trace_id,
        child_trace_id=child_trace_id,
        residual_locus=residual_locus,
        budget_consumed=delta_control,
        budget_remaining=new_remaining_budget,
        inherited_global_budget=True,
        inherited_fingerprint_history=True,
        authority_effect="None",
    )

    return updated_envelope, receipt



