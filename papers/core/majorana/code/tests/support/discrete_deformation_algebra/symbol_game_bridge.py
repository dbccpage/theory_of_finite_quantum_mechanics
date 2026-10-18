"""Project a verified Python Symbol Game run into an outer DDA evidence tape.

This module is deliberately a proposal-rail bridge.  The Python
``Prime000ShapeReceipt`` and ``Prime001ShapeReceipt`` remain shape evidence,
``LocalContinuationCheck`` is not Prime 002, and the exact Rust OESOS replay is
not forged here.  Intermediate Symbol Game ``M`` events stay nested evidence;
only the final unresolved outer outcome becomes experimental ``Z·T``.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

from omega_engine_governance.contracts.dda_packets import DDATapeDFA
from omega_engine.crates.discrete_deformation_algebra.dda_trace_logger import TraceLogger
from omega_engine.crates.discrete_deformation_algebra.trajectory_recorder import (
    verify_trajectory_chain,
)
from omega_engine.crates.type.runtime_axes import DdaDialect
from omega_engine_pfp.domain.shared_kernel.canonical import (
    domain_digest,
    thaw,
)
from omega_engine.crates.engine.eng_symbol_game import RunReceipt


BRIDGE_SCHEMA = "omega.symbol-game.dda-bridge.v2"
BRIDGE_V3_SCHEMA = "omega.symbol-game.dda-bridge.v3"
RUST_HOST_OUTCOME_SCHEMA = "omega.oesos.rust-prime-host-outcome.v1"
PRIME_EVIDENCE_LEVEL = "PYTHON_SHAPE_ONLY"
SEALED_PRIME002_STATUS = "NOT_RUN"
RESIDUAL_METRIC = "aggregate_obstruction_mass(phi1+gamma2)"
ADMISSION_RESIDUAL_METRIC = "admission_obstruction_count"

_RUST_HOST_OUTCOME_FIELDS = frozenset(
    {
        "schema_version",
        "request_id_sha256",
        "challenge_hex",
        "outcome_root_sha256",
        "host_registry_hash_sha256",
        "host_source_revision",
        "authority_effect",
        "execution_status",
        "source_bindings",
        "carrier_manifest",
        "prime001_result",
        "oesos_result",
        "prime000_result",
        "prime002_result",
        "diagnostic_kind",
        "admission",
        "attestation",
        "refusal",
    }
)
_SOURCE_BINDING_FIELDS = frozenset(
    {
        "packet_id",
        "runtime_id_sha256",
        "runtime_id_verdict",
        "candidate_id_sha256",
        "candidate_id_verdict",
        "candidate_state_hash_sha256",
        "candidate_state_verdict",
        "source_event_root_sha256",
        "source_event_root_verdict",
        "source_wire_receipt_id_sha256",
        "source_wire_receipt_verdict",
        "solver_registry_hash_sha256",
        "solver_registry_verdict",
        "source_revision",
        "source_revision_verdict",
    }
)
_RUST_CANONICAL_LETTERS = frozenset({"E", "R", "C", "I", "Λ", "D", "M", "T"})
_RUST_SOURCE_BINDING_VERDICTS = {
    "runtime_id_verdict": (
        "BOUND_ONLY_RUNTIME_ARTIFACT_SCHEMA_NOT_YET_PUBLISHED"
    ),
    "candidate_id_verdict": (
        "BOUND_ONLY_CANDIDATE_ARTIFACT_BYTES_NOT_SUPPLIED"
    ),
    "candidate_state_verdict": (
        "BOUND_ONLY_PYTHON_IDENTITY;HOST_VECTOR_HASH_REPORTED_SEPARATELY"
    ),
    "source_event_root_verdict": (
        "BOUND_ONLY_EVENT_BUNDLE_SCHEMA_NOT_YET_PUBLISHED"
    ),
    "source_wire_receipt_verdict": (
        "BOUND_ONLY_SOURCE_RECEIPT_BYTES_NOT_SUPPLIED"
    ),
    "solver_registry_verdict": (
        "BOUND_ONLY_SOURCE_REGISTRY_MANIFEST_NOT_SUPPLIED"
    ),
}
_RUST_SOURCE_BINDING_OBSTRUCTIONS = {
    "runtime_id_verdict": "RUST_HOST_RUNTIME_ID_BOUND_ONLY",
    "candidate_id_verdict": "RUST_HOST_CANDIDATE_ID_BOUND_ONLY",
    "candidate_state_verdict": "RUST_HOST_CANDIDATE_STATE_BOUND_ONLY",
    "source_event_root_verdict": "RUST_HOST_SOURCE_EVENT_ROOT_BOUND_ONLY",
    "source_wire_receipt_verdict": "RUST_HOST_WIRE_RECEIPT_BOUND_ONLY",
    "solver_registry_verdict": "RUST_HOST_SOLVER_REGISTRY_BOUND_ONLY",
}
_RUST_SOURCE_REVISION_VERDICTS = frozenset(
    {"MATCH_HOST_BUILD_STAMP", "BOUND_ONLY_DISTINCT_SOURCE_REVISION"}
)


@dataclass(frozen=True, slots=True)
class SymbolGameDdaBridgeReceipt:
    """Commit one Symbol Game event root to one outer DDA terminal head."""

    packet_id: str
    runtime_id: str
    source_event_root: str
    source_wire_receipt_id: str
    source_terminal_status: str
    source_process_tape: tuple[str, ...]
    dda_dialect: str
    dda_tape: tuple[str, ...]
    dda_run_id: str
    dda_terminal_hash: str
    dda_trace_path: str
    bridge_root: str
    initial_residual: float | None
    final_residual: float | None
    residual_metric: str
    initial_raw_mass: float | None
    initial_phi1: float | None
    initial_gamma2: float | None
    final_raw_mass: float | None
    final_phi1: float | None
    final_gamma2: float | None
    locally_resolved: bool
    prime_evidence_level: str = PRIME_EVIDENCE_LEVEL
    sealed_prime002_status: str = SEALED_PRIME002_STATUS
    rust_oesos_replay_status: str = "NOT_RUN"
    schema_version: str = BRIDGE_SCHEMA
    authority_effect: str = "None"


@dataclass(frozen=True, slots=True)
class ValidatedRustHostOutcome:
    """A Rust v1 outcome whose root, request, and source bindings reconcile.

    Validation establishes integrity and provenance binding only.  The current
    Rust v1 protocol carries an ``unsigned_lab`` attestation, so validation is
    deliberately not global admission.
    """

    outcome_root_sha256: str
    request_id_sha256: str
    challenge_hex: str
    execution_status: str
    admission_kind: str
    admission_codes: tuple[str, ...]
    attestation: str
    prime000_conformance_verdict: str | None
    source_binding_verdicts: Mapping[str, str]
    exact_axes: Mapping[str, Any]
    rust_canonical_letters: tuple[str, ...]
    outcome: Mapping[str, Any]
    authority_effect: str = "None"


@dataclass(frozen=True, slots=True)
class SymbolGameDdaBridgeReceiptV3:
    """Bind local mathematical descent to a separate global admission result."""

    packet_id: str
    runtime_id: str
    source_event_root: str
    source_wire_receipt_id: str
    v2_bridge: SymbolGameDdaBridgeReceipt
    rust_host_outcome_root: str | None
    rust_host_request_id_sha256: str | None
    rust_host_outcome_validated: bool
    global_admission: str
    admission_codes: tuple[str, ...]
    admission_obstruction_count: int
    admission_residual_metric: str
    local_initial_residual: float
    local_final_residual: float
    local_residual_metric: str
    dda_dialect: str
    dda_tape: tuple[str, ...]
    dda_run_id: str
    dda_terminal_hash: str
    dda_trace_path: str
    bridge_root: str
    schema_version: str = BRIDGE_V3_SCHEMA
    authority_effect: str = "None"


def _checked_axis(value: Any, name: str, *, optional: bool = False) -> float | None:
    if value is None and optional:
        return None
    if (
        isinstance(value, Mapping)
        and set(value) == {"$float_hex"}
        and isinstance(value.get("$float_hex"), str)
    ):
        try:
            value = float.fromhex(value["$float_hex"])
        except ValueError as exc:
            raise ValueError(f"{name} has an invalid canonical float") from exc
    if type(value) not in {int, float}:
        raise TypeError(f"{name} must be numeric")
    normalized = float(value)
    if not math.isfinite(normalized) or normalized < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return normalized


def _measure_axes(measure: tuple[float, float, int]) -> tuple[float, float, float]:
    gamma2, phi1, _active_count = measure
    checked_phi1 = _checked_axis(phi1, "Phi1")
    checked_gamma2 = _checked_axis(gamma2, "Gamma2")
    assert checked_phi1 is not None and checked_gamma2 is not None
    return checked_phi1, checked_gamma2, checked_phi1 + checked_gamma2


def _final_axes(
    receipt: RunReceipt,
) -> tuple[float | None, float | None, float | None, float | None]:
    if receipt.final_projection is None:
        return None, None, None, None
    phi1, gamma2, aggregate = _measure_axes(receipt.final_projection.measure)
    raw_mass = _checked_axis(
        receipt.final_projection.raw_mass,
        "final raw mass",
        optional=True,
    )
    return raw_mass, phi1, gamma2, aggregate


def _event_axes(event: Any) -> tuple[float | None, float, float, float]:
    details = thaw(event.details)
    if not isinstance(details, Mapping):
        raise ValueError("projection event details must be a mapping")
    raw_mass = _checked_axis(details.get("raw_mass"), "event raw mass", optional=True)
    phi1 = _checked_axis(details.get("phi1"), "event Phi1")
    gamma2 = _checked_axis(details.get("gamma2"), "event Gamma2")
    aggregate = _checked_axis(details.get("obstruction_mass"), "event obstruction mass")
    assert phi1 is not None and gamma2 is not None and aggregate is not None
    if aggregate != phi1 + gamma2:
        raise ValueError("event obstruction mass does not equal Phi1 plus Gamma2")
    return raw_mass, phi1, gamma2, aggregate


def _initial_axes(
    receipt: RunReceipt,
) -> tuple[float | None, float | None, float | None, float | None]:
    projection_event = next(
        (
            event
            for event in receipt.process_events
            if event.event_type == "residual-projection"
        ),
        None,
    )
    if projection_event is None:
        if receipt.final_projection is None:
            return None, None, None, None
        return _final_axes(receipt)
    raw_mass, phi1, gamma2, aggregate = _event_axes(projection_event)
    expected_measure = (
        receipt.attempts[0].before_measure
        if receipt.attempts
        else (
            receipt.final_projection.measure
            if receipt.final_projection is not None
            else None
        )
    )
    if expected_measure is not None:
        expected_phi1, expected_gamma2, expected_aggregate = _measure_axes(
            expected_measure
        )
        if (phi1, gamma2, aggregate) != (
            expected_phi1,
            expected_gamma2,
            expected_aggregate,
        ):
            raise ValueError("initial projection axes do not match solver evidence")
    return raw_mass, phi1, gamma2, aggregate


def _process_event_payload(event: Any) -> dict[str, Any]:
    return {
        "sequence": event.sequence,
        "event_type": event.event_type,
        "dda_letter": event.dda_letter,
        "input_state_hash": event.input_state_hash,
        "output_state_hash": event.output_state_hash,
        "details": thaw(event.details),
        "parent_hash": event.parent_hash,
        "event_hash": event.event_hash,
        "authority_effect": event.authority_effect,
    }


def _bridge_root_payload(
    *,
    packet_id: str,
    runtime_id: str,
    source_event_root: str,
    source_wire_receipt_id: str,
    source_terminal_status: str,
    source_process_tape: tuple[str, ...],
    dda_dialect: str,
    dda_tape: tuple[str, ...],
    dda_run_id: str,
    dda_terminal_hash: str,
    initial_residual: float | None,
    final_residual: float | None,
    residual_metric: str,
    initial_raw_mass: float | None,
    initial_phi1: float | None,
    initial_gamma2: float | None,
    final_raw_mass: float | None,
    final_phi1: float | None,
    final_gamma2: float | None,
    locally_resolved: bool,
) -> dict[str, Any]:
    return {
        "schema_version": BRIDGE_SCHEMA,
        "packet_id": packet_id,
        "runtime_id": runtime_id,
        "source_event_root": source_event_root,
        "source_wire_receipt_id": source_wire_receipt_id,
        "source_terminal_status": source_terminal_status,
        "source_process_tape": source_process_tape,
        "dda_dialect": dda_dialect,
        "dda_tape": dda_tape,
        "dda_run_id": dda_run_id,
        "dda_terminal_hash": dda_terminal_hash,
        "initial_residual": initial_residual,
        "final_residual": final_residual,
        "residual_metric": residual_metric,
        "initial_raw_mass": initial_raw_mass,
        "initial_phi1": initial_phi1,
        "initial_gamma2": initial_gamma2,
        "final_raw_mass": final_raw_mass,
        "final_phi1": final_phi1,
        "final_gamma2": final_gamma2,
        "locally_resolved": locally_resolved,
        "prime_evidence_level": PRIME_EVIDENCE_LEVEL,
        "sealed_prime002_status": SEALED_PRIME002_STATUS,
        "authority_effect": "None",
    }


def _source_evidence(
    receipt: RunReceipt,
    wire_receipt_id: str,
    extra_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "packet_id": receipt.packet_id,
        "runtime_id": receipt.runtime_id,
        "solver_registry_hash": receipt.solver_registry_hash,
        "wire_receipt_id": wire_receipt_id,
        "source_event_root": receipt.event_root,
        "source_terminal_status": receipt.terminal_status.value,
        "source_process_tape": [event.dda_letter for event in receipt.process_events],
        "process_events": [
            _process_event_payload(event) for event in receipt.process_events
        ],
        "solver_attempts": [asdict(attempt) for attempt in receipt.attempts],
        "obstruction_events": [asdict(event) for event in receipt.obstruction_events],
        "active_obstructions": list(receipt.active_obstructions),
        "prime000_shape_receipt": asdict(receipt.prime000),
        "prime001_shape_receipt": asdict(receipt.adapter),
        "detector_adequacy_receipt": asdict(receipt.detector),
        "prime_evidence_level": PRIME_EVIDENCE_LEVEL,
        "sealed_prime002_status": SEALED_PRIME002_STATUS,
        "residual_axis_contract": {
            "raw_mass": "declared representative weighted L1 mass or null",
            "phi1": "quotient residual",
            "gamma2": "closure residual",
            "outer_dda_scalar": RESIDUAL_METRIC,
            "outer_dda_scalar_is_raw_mass": False,
        },
        "replay_required": True,
        "authority_effect": "None",
        "campaign_evidence": dict(extra_evidence or {}),
    }


def emit_symbol_game_dda_trace(
    receipt: RunReceipt,
    *,
    trace_dir: Path,
    runner_id: str,
    campaign_name: str,
    extra_evidence: Mapping[str, Any] | None = None,
) -> SymbolGameDdaBridgeReceipt:
    """Emit a conservative experimental DDA projection of ``receipt``."""

    if not isinstance(receipt, RunReceipt) or not receipt.evidence_valid():
        raise ValueError("Symbol Game run receipt does not reconcile its evidence")
    wire_receipt = receipt.to_wire_receipt()
    if not wire_receipt.transport_valid():
        raise ValueError("Symbol Game wire receipt failed transport validation")
    if receipt.authority_effect != "None":
        raise ValueError("Symbol Game DDA bridge cannot expand authority")

    (
        initial_raw_mass,
        initial_phi1,
        initial_gamma2,
        initial_residual,
    ) = _initial_axes(receipt)
    (
        final_raw_mass,
        final_phi1,
        final_gamma2,
        final_residual,
    ) = _final_axes(receipt)
    source_process_tape = tuple(event.dda_letter for event in receipt.process_events)
    base_evidence = _source_evidence(
        receipt,
        wire_receipt.receipt_id,
        extra_evidence,
    )
    base_evidence["residual_axes"] = {
        "initial": {
            "raw_mass": initial_raw_mass,
            "phi1": initial_phi1,
            "gamma2": initial_gamma2,
            "aggregate_obstruction_mass": initial_residual,
        },
        "final": {
            "raw_mass": final_raw_mass,
            "phi1": final_phi1,
            "gamma2": final_gamma2,
            "aggregate_obstruction_mass": final_residual,
        },
        "outer_dda_scalar": RESIDUAL_METRIC,
    }
    projection_events = tuple(
        event
        for event in receipt.process_events
        if event.event_type == "residual-projection"
    )
    accepted_events = tuple(
        event
        for event in receipt.process_events
        if event.event_type == "verified-retraction"
    )
    accepted_attempts = tuple(
        attempt for attempt in receipt.attempts if attempt.accepted
    )
    if len(accepted_events) != len(accepted_attempts):
        raise ValueError("accepted attempts do not match verified retraction events")

    initial_state = (
        projection_events[0].output_state_hash
        if projection_events
        else receipt.output_state_hash
    )
    logger = TraceLogger(
        runner_id,
        campaign_name=campaign_name,
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step(
        letter="R",
        action_name="bind_symbol_game_run_evidence",
        input_state=receipt.input_state_hash,
        output_state=initial_state,
        witness=wire_receipt.receipt_id,
        residual_before=initial_residual,
        residual_after=initial_residual,
        effect="residual_carried",
        obstruction_id=(
            "|".join(receipt.active_obstructions)
            if receipt.active_obstructions
            else None
        ),
        evidence=base_evidence,
        cochain_dim="SymbolGameRun",
        coboundary_map="proposal-rail-projection",
    )
    logger.record_step(
        letter="C",
        action_name="expose_shape_and_detector_context",
        input_state=initial_state,
        output_state=initial_state,
        witness=receipt.runtime_id,
        residual_before=initial_residual,
        residual_after=initial_residual,
        effect="context_exposed",
        evidence={
            "packet_id": receipt.packet_id,
            "prime000_shape_receipt": asdict(receipt.prime000),
            "prime001_shape_receipt": asdict(receipt.adapter),
            "detector_adequacy_receipt": asdict(receipt.detector),
            "residual_axes": {
                "raw_mass": initial_raw_mass,
                "phi1": initial_phi1,
                "gamma2": initial_gamma2,
                "aggregate_obstruction_mass": initial_residual,
                "outer_dda_scalar": RESIDUAL_METRIC,
            },
            "not_prime002": True,
            "authority_effect": "None",
        },
        cochain_dim="SymbolGameRun",
        coboundary_map="proposal-rail-projection",
    )

    current_state = initial_state
    current_raw_mass = initial_raw_mass
    current_phi1 = initial_phi1
    current_gamma2 = initial_gamma2
    for accepted_index, (attempt, event) in enumerate(
        zip(accepted_attempts, accepted_events),
        start=1,
    ):
        before_phi1, before_gamma2, before = _measure_axes(attempt.before_measure)
        if attempt.after_measure is None:
            raise ValueError("accepted Symbol Game attempt has no after measure")
        after_phi1, after_gamma2, after = _measure_axes(attempt.after_measure)
        if after >= before:
            raise ValueError(
                "accepted Symbol Game attempt lacks strict residual descent"
            )
        if event.input_state_hash != current_state:
            raise ValueError("Symbol Game accepted-event state chain is discontinuous")
        if (current_phi1, current_gamma2) != (before_phi1, before_gamma2):
            raise ValueError("Symbol Game accepted-attempt axes are discontinuous")
        after_raw_mass, event_phi1, event_gamma2, event_aggregate = _event_axes(event)
        if (event_phi1, event_gamma2, event_aggregate) != (
            after_phi1,
            after_gamma2,
            after,
        ):
            raise ValueError("verified-retraction event axes do not match its attempt")
        ledger_events = tuple(
            item for item in receipt.obstruction_events if item.step == accepted_index
        )
        discharged = tuple(
            item.obstruction_id
            for item in ledger_events
            if item.disposition == "DISCHARGED"
        )
        reduced = tuple(
            item.obstruction_id
            for item in ledger_events
            if item.disposition == "UPDATED"
        )
        if not discharged and not reduced:
            raise ValueError("strict descent has no obstruction-ledger witness")
        letter = "E" if discharged else "D"
        effect = "obstruction_eliminated" if discharged else "residual_reduced"
        logger.record_step(
            letter=letter,
            action_name="project_verified_symbol_retraction",
            input_state=event.input_state_hash,
            output_state=event.output_state_hash,
            witness=event.event_hash,
            residual_before=before,
            residual_after=after,
            effect=effect,
            obstruction_id="|".join(discharged or reduced),
            evidence={
                "symbol_process_event": _process_event_payload(event),
                "solver_attempt": asdict(attempt),
                "obstruction_ledger_events": [asdict(item) for item in ledger_events],
                "residual_axes": {
                    "before": {
                        "raw_mass": current_raw_mass,
                        "phi1": before_phi1,
                        "gamma2": before_gamma2,
                        "aggregate_obstruction_mass": before,
                    },
                    "after": {
                        "raw_mass": after_raw_mass,
                        "phi1": after_phi1,
                        "gamma2": after_gamma2,
                        "aggregate_obstruction_mass": after,
                    },
                    "outer_dda_scalar": RESIDUAL_METRIC,
                },
                "authority_effect": "None",
            },
            cochain_dim="SymbolGameRun",
            coboundary_map="same-carrier-retraction",
        )
        current_state = event.output_state_hash
        current_raw_mass = after_raw_mass
        current_phi1 = after_phi1
        current_gamma2 = after_gamma2

    if current_state != receipt.output_state_hash:
        raise ValueError("outer DDA state does not reach the Symbol Game output")
    if (current_raw_mass, current_phi1, current_gamma2) != (
        final_raw_mass,
        final_phi1,
        final_gamma2,
    ):
        raise ValueError("outer DDA residual axes do not reach the final projection")

    if receipt.locally_resolved:
        if final_residual != 0.0 or receipt.active_obstructions:
            raise ValueError("locally resolved Symbol Game run retained an obstruction")
        logger.finalize_success(
            current_state,
            receipt.output_state_hash,
            receipt.event_root,
            residual=final_residual,
            evidence={
                "source_event_root": receipt.event_root,
                "wire_receipt_id": wire_receipt.receipt_id,
                "scope": "ReplayableLabEvidence",
                "residual_axes": {
                    "raw_mass": final_raw_mass,
                    "phi1": final_phi1,
                    "gamma2": final_gamma2,
                    "aggregate_obstruction_mass": final_residual,
                    "outer_dda_scalar": RESIDUAL_METRIC,
                },
                "rust_replay_required": True,
                "authority_effect": "None",
            },
        )
    else:
        refusal_reason = ";".join(receipt.stop_reasons) or receipt.terminal_status.value
        logger.refuse(
            reason=refusal_reason,
            input_state=current_state,
            output_state=current_state,
            witness=receipt.event_root,
            residual=final_residual,
            obstruction_id=(
                "|".join(receipt.active_obstructions)
                if receipt.active_obstructions
                else f"SYMBOL_GAME:{receipt.terminal_status.value}"
            ),
            evidence={
                "source_event_root": receipt.event_root,
                "wire_receipt_id": wire_receipt.receipt_id,
                "source_terminal_status": receipt.terminal_status.value,
                "stop_reasons": list(receipt.stop_reasons),
                "active_obstructions": list(receipt.active_obstructions),
                "source_process_tape": list(source_process_tape),
                "residual_axes": {
                    "raw_mass": final_raw_mass,
                    "phi1": final_phi1,
                    "gamma2": final_gamma2,
                    "aggregate_obstruction_mass": final_residual,
                    "outer_dda_scalar": RESIDUAL_METRIC,
                },
                "authority_effect": "None",
            },
        )

    dda_tape = tuple(logger.tape)
    terminal_hash = str(logger.steps[-1]["step_hash"])
    payload = _bridge_root_payload(
        packet_id=receipt.packet_id,
        runtime_id=receipt.runtime_id,
        source_event_root=receipt.event_root,
        source_wire_receipt_id=wire_receipt.receipt_id,
        source_terminal_status=receipt.terminal_status.value,
        source_process_tape=source_process_tape,
        dda_dialect=logger.dialect,
        dda_tape=dda_tape,
        dda_run_id=logger.run_id,
        dda_terminal_hash=terminal_hash,
        initial_residual=initial_residual,
        final_residual=final_residual,
        residual_metric=RESIDUAL_METRIC,
        initial_raw_mass=initial_raw_mass,
        initial_phi1=initial_phi1,
        initial_gamma2=initial_gamma2,
        final_raw_mass=final_raw_mass,
        final_phi1=final_phi1,
        final_gamma2=final_gamma2,
        locally_resolved=receipt.locally_resolved,
    )
    return SymbolGameDdaBridgeReceipt(
        packet_id=receipt.packet_id,
        runtime_id=receipt.runtime_id,
        source_event_root=receipt.event_root,
        source_wire_receipt_id=wire_receipt.receipt_id,
        source_terminal_status=receipt.terminal_status.value,
        source_process_tape=source_process_tape,
        dda_dialect=logger.dialect,
        dda_tape=dda_tape,
        dda_run_id=logger.run_id,
        dda_terminal_hash=terminal_hash,
        dda_trace_path=str(logger.jsonl_path.resolve()),
        bridge_root=domain_digest(BRIDGE_SCHEMA, payload),
        initial_residual=initial_residual,
        final_residual=final_residual,
        residual_metric=RESIDUAL_METRIC,
        initial_raw_mass=initial_raw_mass,
        initial_phi1=initial_phi1,
        initial_gamma2=initial_gamma2,
        final_raw_mass=final_raw_mass,
        final_phi1=final_phi1,
        final_gamma2=final_gamma2,
        locally_resolved=receipt.locally_resolved,
    )


def verify_symbol_game_dda_bridge(
    source_receipt: RunReceipt,
    bridge_receipt: SymbolGameDdaBridgeReceipt,
) -> bool:
    """Reconcile a bridge anchor, source receipt, JSONL chain, and DDA grammar."""

    try:
        if (
            not source_receipt.evidence_valid()
            or source_receipt.authority_effect != "None"
            or bridge_receipt.authority_effect != "None"
            or bridge_receipt.schema_version != BRIDGE_SCHEMA
            or bridge_receipt.prime_evidence_level != PRIME_EVIDENCE_LEVEL
            or bridge_receipt.sealed_prime002_status != SEALED_PRIME002_STATUS
            or bridge_receipt.residual_metric != RESIDUAL_METRIC
        ):
            return False
        wire_receipt = source_receipt.to_wire_receipt()
        expected_initial = _initial_axes(source_receipt)
        expected_final = _final_axes(source_receipt)
        if (
            bridge_receipt.packet_id != source_receipt.packet_id
            or bridge_receipt.runtime_id != source_receipt.runtime_id
            or bridge_receipt.source_event_root != source_receipt.event_root
            or bridge_receipt.source_wire_receipt_id != wire_receipt.receipt_id
            or bridge_receipt.source_terminal_status
            != source_receipt.terminal_status.value
            or bridge_receipt.source_process_tape
            != tuple(event.dda_letter for event in source_receipt.process_events)
            or bridge_receipt.locally_resolved != source_receipt.locally_resolved
            or (
                bridge_receipt.initial_raw_mass,
                bridge_receipt.initial_phi1,
                bridge_receipt.initial_gamma2,
                bridge_receipt.initial_residual,
            )
            != expected_initial
            or (
                bridge_receipt.final_raw_mass,
                bridge_receipt.final_phi1,
                bridge_receipt.final_gamma2,
                bridge_receipt.final_residual,
            )
            != expected_final
        ):
            return False

        trace_path = Path(bridge_receipt.dda_trace_path)
        records = [
            json.loads(line)
            for line in trace_path.read_text("utf-8").splitlines()
            if line.strip()
        ]
        if not records or not verify_trajectory_chain(records)[0]:
            return False
        tape = tuple(str(record.get("letter", "")) for record in records)
        if (
            tape != bridge_receipt.dda_tape
            or str(records[0].get("dda_dialect")) != bridge_receipt.dda_dialect
            or str(records[0].get("run_id")) != bridge_receipt.dda_run_id
            or str(records[-1].get("step_hash")) != bridge_receipt.dda_terminal_hash
            or records[0].get("residual_before") != bridge_receipt.initial_residual
            or records[0].get("residual_after") != bridge_receipt.initial_residual
        ):
            return False
        DDATapeDFA.validate(".".join(tape), dialect=bridge_receipt.dda_dialect)
        first_evidence = records[0].get("evidence", {})
        if (
            first_evidence.get("source_event_root") != source_receipt.event_root
            or first_evidence.get("wire_receipt_id") != wire_receipt.receipt_id
            or first_evidence.get("prime_evidence_level") != PRIME_EVIDENCE_LEVEL
            or first_evidence.get("residual_axis_contract", {}).get("outer_dda_scalar")
            != RESIDUAL_METRIC
            or first_evidence.get("residual_axes", {})
            .get("initial", {})
            .get("raw_mass")
            != bridge_receipt.initial_raw_mass
        ):
            return False
        if bridge_receipt.locally_resolved:
            if "Z" in tape or tape[-2:] != ("I", "T"):
                return False
        elif tape[-2:] != ("Z", "T"):
            return False

        payload = _bridge_root_payload(
            packet_id=bridge_receipt.packet_id,
            runtime_id=bridge_receipt.runtime_id,
            source_event_root=bridge_receipt.source_event_root,
            source_wire_receipt_id=bridge_receipt.source_wire_receipt_id,
            source_terminal_status=bridge_receipt.source_terminal_status,
            source_process_tape=bridge_receipt.source_process_tape,
            dda_dialect=bridge_receipt.dda_dialect,
            dda_tape=bridge_receipt.dda_tape,
            dda_run_id=bridge_receipt.dda_run_id,
            dda_terminal_hash=bridge_receipt.dda_terminal_hash,
            initial_residual=bridge_receipt.initial_residual,
            final_residual=bridge_receipt.final_residual,
            residual_metric=bridge_receipt.residual_metric,
            initial_raw_mass=bridge_receipt.initial_raw_mass,
            initial_phi1=bridge_receipt.initial_phi1,
            initial_gamma2=bridge_receipt.initial_gamma2,
            final_raw_mass=bridge_receipt.final_raw_mass,
            final_phi1=bridge_receipt.final_phi1,
            final_gamma2=bridge_receipt.final_gamma2,
            locally_resolved=bridge_receipt.locally_resolved,
        )
        return bridge_receipt.bridge_root == domain_digest(
            BRIDGE_SCHEMA,
            payload,
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return False


def _require_exact_mapping(
    value: Any,
    name: str,
    fields: frozenset[str] | set[str],
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    if set(value) != set(fields):
        raise ValueError(f"{name} fields do not match the Rust v1 contract")
    return value


def _require_string(value: Any, name: str, *, nonempty: bool = True) -> str:
    if type(value) is not str or (nonempty and not value):
        raise TypeError(f"{name} must be a{' nonempty' if nonempty else ''} string")
    return value


def _require_lower_hex(value: Any, name: str, *, length: int | None = None) -> str:
    text = _require_string(value, name)
    if length is not None and len(text) != length:
        raise ValueError(f"{name} must contain exactly {length} hexadecimal digits")
    if any(character not in "0123456789abcdef" for character in text):
        raise ValueError(f"{name} must be lowercase hexadecimal")
    return text


def _json_value_copy(value: Any, name: str) -> Any:
    try:
        encoded = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} is not canonical JSON data") from exc
    return json.loads(encoded)


def compute_rust_host_outcome_root(outcome: Mapping[str, Any]) -> str:
    """Reproduce the Rust host's framed SHA-256 outcome commitment."""

    normalized = _json_value_copy(outcome, "Rust host outcome")
    if not isinstance(normalized, dict):
        raise TypeError("Rust host outcome must be a mapping")
    normalized.pop("outcome_root_sha256", None)
    payload = json.dumps(
        normalized,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    domain = RUST_HOST_OUTCOME_SCHEMA.encode("utf-8")
    framed = (
        len(domain).to_bytes(4, "big")
        + domain
        + len(payload).to_bytes(8, "big")
        + payload
    )
    return hashlib.sha256(framed).hexdigest()


def _exact_rational(value: Any, name: str) -> dict[str, str]:
    wire = _require_exact_mapping(value, name, {"n", "d"})
    numerator_text = _require_string(wire["n"], f"{name}.n")
    denominator_text = _require_string(wire["d"], f"{name}.d")
    try:
        numerator = int(numerator_text)
        denominator = int(denominator_text)
    except ValueError as exc:
        raise ValueError(f"{name} must contain base-ten integers") from exc
    if str(numerator) != numerator_text or str(denominator) != denominator_text:
        raise ValueError(f"{name} integers must use their minimal base-ten spelling")
    if denominator <= 0:
        raise ValueError(f"{name}.d must be positive")
    reduced = Fraction(numerator, denominator)
    if (reduced.numerator, reduced.denominator) != (numerator, denominator):
        raise ValueError(f"{name} must be reduced")
    return {"n": numerator_text, "d": denominator_text}


def _validated_exact_axes(oesos_result: Any) -> dict[str, Any]:
    if oesos_result is None:
        return {}
    result = _require_exact_mapping(
        oesos_result,
        "oesos_result",
        {
            "kind",
            "input_commitment_sha256",
            "fresh_solve_commitment_sha256",
            "replay_commitment_sha256",
            "pipeline_declaration_carrier_hash_blake3",
            "gauge",
            "final_stage",
            "normal_form",
            "b1_over_q",
            "span_distance",
            "closure_premium",
            "candidate_relation",
        },
    )

    def stage(value: Any, name: str) -> dict[str, Any]:
        item = _require_exact_mapping(
            value,
            name,
            {"status", "raw_weighted_l1", "phi1", "gamma2"},
        )
        return {
            "status": _require_string(item["status"], f"{name}.status"),
            "raw_weighted_l1": _exact_rational(
                item["raw_weighted_l1"], f"{name}.raw_weighted_l1"
            ),
            "phi1": _exact_rational(item["phi1"], f"{name}.phi1"),
            "gamma2": _exact_rational(item["gamma2"], f"{name}.gamma2"),
        }

    normal_form = result["normal_form"]
    if type(normal_form) is not list:
        raise TypeError("oesos_result.normal_form must be a list")
    if type(result["b1_over_q"]) is not int or result["b1_over_q"] < 0:
        raise ValueError("oesos_result.b1_over_q must be a nonnegative integer")
    return {
        "gauge": stage(result["gauge"], "oesos_result.gauge"),
        "final_stage": stage(result["final_stage"], "oesos_result.final_stage"),
        "normal_form": [
            _exact_rational(item, f"oesos_result.normal_form[{index}]")
            for index, item in enumerate(normal_form)
        ],
        "b1_over_q": result["b1_over_q"],
        "span_distance": _exact_rational(
            result["span_distance"], "oesos_result.span_distance"
        ),
        "closure_premium": _exact_rational(
            result["closure_premium"], "oesos_result.closure_premium"
        ),
    }


def _validated_prime000_verdict(prime000_result: Any) -> str | None:
    if prime000_result is None:
        return None
    result = _require_exact_mapping(
        prime000_result,
        "prime000_result",
        {
            "kind",
            "receipt_commitment_sha256",
            "terminal",
            "evidence_provenance",
            "letter_tape",
            "phi1_u64",
            "gamma2_u64",
            "conformance",
        },
    )
    conformance = _require_exact_mapping(
        result["conformance"],
        "prime000_result.conformance",
        {
            "verdict",
            "conforms",
            "no_decidable_violation",
            "violations",
            "unchecked_laws",
        },
    )
    verdict = _require_string(
        conformance["verdict"], "prime000_result.conformance.verdict"
    )
    if type(conformance["conforms"]) is not bool:
        raise TypeError("prime000_result.conformance.conforms must be boolean")
    if type(conformance["no_decidable_violation"]) is not bool:
        raise TypeError(
            "prime000_result.conformance.no_decidable_violation must be boolean"
        )
    for field in ("violations", "unchecked_laws"):
        values = conformance[field]
        if type(values) is not list or any(type(item) is not str for item in values):
            raise TypeError(f"prime000_result.conformance.{field} must be strings")
    return verdict


def _validated_rust_letters(prime002_result: Any) -> tuple[str, ...]:
    if prime002_result is None:
        return ()
    result = _require_exact_mapping(
        prime002_result,
        "prime002_result",
        {
            "kind",
            "scope_commitments_sha256",
            "claim_commitments_sha256",
            "evidence_commitments_sha256",
            "permit_bindings_sha256",
            "rust_letters",
            "terminal_head_sha256",
            "budget_before",
            "budget_after",
            "refusal_laws",
            "evidence_caveat",
        },
    )
    letters = result["rust_letters"]
    if type(letters) is not list or any(type(letter) is not str for letter in letters):
        raise TypeError("prime002_result.rust_letters must be a list of strings")
    if any(letter not in _RUST_CANONICAL_LETTERS for letter in letters):
        raise ValueError("prime002_result contains a noncanonical Rust letter")
    return tuple(letters)


def validate_rust_host_outcome(
    outcome: Mapping[str, Any],
    *,
    source_receipt: RunReceipt,
    expected_request_id_sha256: str,
    expected_challenge_hex: str,
) -> ValidatedRustHostOutcome:
    """Validate the exact Rust v1 outcome envelope and its source bindings."""

    if not source_receipt.evidence_valid() or source_receipt.authority_effect != "None":
        raise ValueError("Symbol Game source receipt does not reconcile")
    normalized = _json_value_copy(outcome, "Rust host outcome")
    host = _require_exact_mapping(
        normalized,
        "Rust host outcome",
        _RUST_HOST_OUTCOME_FIELDS,
    )
    if host["schema_version"] != RUST_HOST_OUTCOME_SCHEMA:
        raise ValueError("Rust host outcome schema is not v1")
    if host["authority_effect"] != "None":
        raise ValueError("Rust host outcome cannot expand authority")
    supplied_root = _require_lower_hex(
        host["outcome_root_sha256"], "outcome_root_sha256", length=64
    )
    if supplied_root != compute_rust_host_outcome_root(host):
        raise ValueError("Rust host outcome root does not reconcile")

    expected_request = _require_lower_hex(
        expected_request_id_sha256,
        "expected_request_id_sha256",
        length=64,
    )
    expected_challenge = _require_lower_hex(
        expected_challenge_hex,
        "expected_challenge_hex",
    )
    request_id = _require_lower_hex(
        host["request_id_sha256"], "request_id_sha256", length=64
    )
    challenge = _require_lower_hex(host["challenge_hex"], "challenge_hex")
    if request_id != expected_request or challenge != expected_challenge:
        raise ValueError("Rust host outcome does not bind the expected request")

    bindings = _require_exact_mapping(
        host["source_bindings"],
        "source_bindings",
        _SOURCE_BINDING_FIELDS,
    )
    packet_binding = _require_exact_mapping(
        bindings["packet_id"],
        "source_bindings.packet_id",
        {"supplied", "derived", "verdict"},
    )
    if (
        packet_binding["supplied"] != source_receipt.packet_id
        or packet_binding["derived"] != source_receipt.packet_id
        or packet_binding["verdict"] != "MATCH"
    ):
        raise ValueError("Rust host packet binding does not match the source")
    wire_receipt_id = source_receipt.to_wire_receipt().receipt_id
    expected_bindings = {
        "runtime_id_sha256": source_receipt.runtime_id,
        "source_event_root_sha256": source_receipt.event_root,
        "source_wire_receipt_id_sha256": wire_receipt_id,
        "solver_registry_hash_sha256": source_receipt.solver_registry_hash,
    }
    for field, expected in expected_bindings.items():
        if bindings[field] != expected:
            raise ValueError(f"Rust host {field} does not match the source")
    for verdict_field, expected_verdict in _RUST_SOURCE_BINDING_VERDICTS.items():
        if bindings[verdict_field] != expected_verdict:
            raise ValueError(
                f"Rust host {verdict_field} is not the exact v1 verdict"
            )
    source_revision_verdict = bindings["source_revision_verdict"]
    if source_revision_verdict not in _RUST_SOURCE_REVISION_VERDICTS:
        raise ValueError("Rust host source_revision_verdict is not a v1 verdict")
    candidate_id = _require_lower_hex(
        bindings["candidate_id_sha256"],
        "source_bindings.candidate_id_sha256",
        length=64,
    )
    candidate_state_hash = _require_lower_hex(
        bindings["candidate_state_hash_sha256"],
        "source_bindings.candidate_state_hash_sha256",
        length=64,
    )
    accepted_attempts = tuple(
        attempt for attempt in source_receipt.attempts if attempt.accepted
    )
    if not accepted_attempts:
        raise ValueError("Rust host candidate binding requires an accepted candidate")
    final_accepted = accepted_attempts[-1]
    if (
        candidate_id != final_accepted.candidate_id
        or candidate_state_hash != final_accepted.candidate_state_hash
        or candidate_state_hash != source_receipt.output_state_hash
    ):
        raise ValueError(
            "Rust host candidate does not bind the final accepted artifact"
        )
    source_revision = _require_string(
        bindings["source_revision"], "source_bindings.source_revision"
    )
    revision_matches_host = source_revision == host["host_source_revision"]
    if revision_matches_host != (
        source_revision_verdict == "MATCH_HOST_BUILD_STAMP"
    ):
        raise ValueError("Rust host source revision verdict is internally inconsistent")

    admission = _require_exact_mapping(
        host["admission"],
        "admission",
        {"kind", "codes", "reason_commitment_sha256"},
    )
    admission_kind = _require_string(admission["kind"], "admission.kind")
    codes_value = admission["codes"]
    if type(codes_value) is not list or any(
        type(code) is not str for code in codes_value
    ):
        raise TypeError("admission.codes must be a list of strings")
    _require_lower_hex(
        admission["reason_commitment_sha256"],
        "admission.reason_commitment_sha256",
        length=64,
    )
    _require_lower_hex(
        host["host_registry_hash_sha256"],
        "host_registry_hash_sha256",
        length=64,
    )
    _require_string(host["host_source_revision"], "host_source_revision")
    execution_status = _require_string(host["execution_status"], "execution_status")
    attestation = _require_string(host["attestation"], "attestation")
    exact_axes = _validated_exact_axes(host["oesos_result"])
    prime000_verdict = _validated_prime000_verdict(host["prime000_result"])
    rust_letters = _validated_rust_letters(host["prime002_result"])
    source_binding_verdicts = {
        "packet_id": str(packet_binding["verdict"]),
        **{
            field: str(bindings[field])
            for field in _RUST_SOURCE_BINDING_VERDICTS
        },
        "source_revision_verdict": str(source_revision_verdict),
    }
    return ValidatedRustHostOutcome(
        outcome_root_sha256=supplied_root,
        request_id_sha256=request_id,
        challenge_hex=challenge,
        execution_status=execution_status,
        admission_kind=admission_kind,
        admission_codes=tuple(codes_value),
        attestation=attestation,
        prime000_conformance_verdict=prime000_verdict,
        source_binding_verdicts=source_binding_verdicts,
        exact_axes=exact_axes,
        rust_canonical_letters=rust_letters,
        outcome=host,
    )


def _normalized_admission_codes(codes: Iterable[str]) -> tuple[str, ...]:
    normalized: set[str] = set()
    for code in codes:
        if (
            type(code) is not str
            or not code
            or len(code) > 128
            or code[0] == "_"
            or code[-1] == "_"
            or any(
                character not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
                for character in code
            )
        ):
            raise ValueError("admission codes must be canonical uppercase tokens")
        normalized.add(code)
    return tuple(sorted(normalized))


def _global_admission_obstructions(
    outcome: ValidatedRustHostOutcome | None,
    additional_codes: Iterable[str] = (),
) -> tuple[str, ...]:
    if outcome is None:
        return _normalized_admission_codes(
            (
                "RUST_HOST_OUTCOME_ABSENT",
                "NO_AUTHENTICATED_HOST_ATTESTATION",
                *additional_codes,
            )
        )
    codes = set(_normalized_admission_codes(outcome.admission_codes))
    codes.update(_normalized_admission_codes(additional_codes))
    codes.update(_RUST_SOURCE_BINDING_OBSTRUCTIONS.values())
    if (
        outcome.source_binding_verdicts.get("source_revision_verdict")
        == "BOUND_ONLY_DISTINCT_SOURCE_REVISION"
    ):
        codes.add("RUST_HOST_SOURCE_REVISION_BOUND_ONLY")
    if outcome.admission_kind != "Admitted":
        codes.add("RUST_HOST_ADMISSION_REFUSED")
    if outcome.attestation == "unsigned_lab":
        codes.add("UNSIGNED_LAB_ATTESTATION")
    else:
        codes.add("NO_AUTHENTICATED_HOST_ATTESTATION")
    if outcome.prime000_conformance_verdict != "Conforms":
        codes.add("PRIME000_CONFORMANCE_PARTIAL")
    # HostOutcomeV1 has no signature/key/certificate fields.  Therefore no v1
    # mapping, even one claiming a different attestation string, can establish
    # the fully authenticated premise required for outer I.
    codes.add("RUST_HOST_V1_HAS_NO_AUTHENTICATED_ATTESTATION")
    return tuple(sorted(code for code in codes if code))


def _v3_root_payload(
    receipt: SymbolGameDdaBridgeReceiptV3,
) -> dict[str, Any]:
    return {
        "schema_version": BRIDGE_V3_SCHEMA,
        "packet_id": receipt.packet_id,
        "runtime_id": receipt.runtime_id,
        "source_event_root": receipt.source_event_root,
        "source_wire_receipt_id": receipt.source_wire_receipt_id,
        "v2_bridge_root": receipt.v2_bridge.bridge_root,
        "rust_host_outcome_root": receipt.rust_host_outcome_root,
        "rust_host_request_id_sha256": receipt.rust_host_request_id_sha256,
        "rust_host_outcome_validated": receipt.rust_host_outcome_validated,
        "global_admission": receipt.global_admission,
        "admission_codes": receipt.admission_codes,
        "admission_obstruction_count": receipt.admission_obstruction_count,
        "admission_residual_metric": receipt.admission_residual_metric,
        "local_initial_residual": receipt.local_initial_residual,
        "local_final_residual": receipt.local_final_residual,
        "local_residual_metric": receipt.local_residual_metric,
        "dda_dialect": receipt.dda_dialect,
        "dda_tape": receipt.dda_tape,
        "dda_run_id": receipt.dda_run_id,
        "dda_terminal_hash": receipt.dda_terminal_hash,
        "authority_effect": receipt.authority_effect,
    }


def emit_symbol_game_dda_trace_v3(
    receipt: RunReceipt,
    *,
    trace_dir: Path,
    runner_id: str,
    campaign_name: str,
    rust_host_outcome: Mapping[str, Any] | None = None,
    expected_host_request_id_sha256: str | None = None,
    expected_host_challenge_hex: str | None = None,
    additional_admission_codes: Iterable[str] = (),
    extra_evidence: Mapping[str, Any] | None = None,
) -> SymbolGameDdaBridgeReceiptV3:
    """Emit local ``E`` followed by fail-closed global admission ``Z``.

    The v2 bridge is emitted and retained as nested mathematical evidence.  A
    supplied Rust outcome is evidence only after its outcome root, request, and
    source bindings validate.  Rust v1 is unsigned, so every v3 run currently
    ends ``Z.T``; no Rust canonical letter is projected into ``Z``.
    """

    if not isinstance(receipt, RunReceipt) or not receipt.evidence_valid():
        raise ValueError("Symbol Game run receipt does not reconcile its evidence")
    if receipt.authority_effect != "None":
        raise ValueError("Symbol Game DDA bridge cannot expand authority")
    if rust_host_outcome is not None and (
        expected_host_request_id_sha256 is None
        or expected_host_challenge_hex is None
    ):
        raise ValueError("Rust host request id and challenge are required")
    validated_host = (
        validate_rust_host_outcome(
            rust_host_outcome,
            source_receipt=receipt,
            expected_request_id_sha256=expected_host_request_id_sha256,
            expected_challenge_hex=expected_host_challenge_hex,
        )
        if rust_host_outcome is not None
        else None
    )

    v2_bridge = emit_symbol_game_dda_trace(
        receipt,
        trace_dir=trace_dir,
        runner_id=f"{runner_id}-v2-local",
        campaign_name=f"{campaign_name} [v2 local evidence]",
        extra_evidence=extra_evidence,
    )
    if not verify_symbol_game_dda_bridge(receipt, v2_bridge):
        raise ValueError("generated v2 bridge did not verify")
    if (
        not v2_bridge.locally_resolved
        or v2_bridge.initial_residual is None
        or v2_bridge.final_residual is None
        or v2_bridge.initial_residual <= v2_bridge.final_residual
        or "E" not in v2_bridge.dda_tape
    ):
        raise ValueError("v3 bridge requires verified local mathematical E evidence")

    v2_records = [
        json.loads(line)
        for line in Path(v2_bridge.dda_trace_path).read_text("utf-8").splitlines()
        if line.strip()
    ]
    local_e_records = [record for record in v2_records if record.get("letter") == "E"]
    if not local_e_records:
        raise ValueError("v2 bridge contains no mathematical E record")
    local_obstruction_ids = tuple(
        str(record["obstruction_id"])
        for record in local_e_records
        if record.get("obstruction_id")
    )
    if not local_obstruction_ids:
        raise ValueError("local mathematical E has no obstruction witness")

    admission_codes = _global_admission_obstructions(
        validated_host,
        additional_admission_codes,
    )
    admission_obstruction_count = len(admission_codes)
    if admission_obstruction_count <= 0:
        raise ValueError("global refusal requires a nonzero admission obstruction")
    exact_axes = dict(validated_host.exact_axes) if validated_host else {}
    rust_letters = (
        list(validated_host.rust_canonical_letters) if validated_host else []
    )
    source_binding_verdicts = (
        dict(validated_host.source_binding_verdicts) if validated_host else {}
    )
    host_evidence = dict(validated_host.outcome) if validated_host else None
    wire_receipt_id = receipt.to_wire_receipt().receipt_id
    anchors = {
        "source_event_root": receipt.event_root,
        "source_wire_receipt_id": wire_receipt_id,
        "v2_bridge_root": v2_bridge.bridge_root,
        "v2_dda_terminal_hash": v2_bridge.dda_terminal_hash,
        "rust_host_outcome_root": (
            validated_host.outcome_root_sha256 if validated_host else None
        ),
        "authority_effect": "None",
    }
    mathematical_axes = {
        "metric": RESIDUAL_METRIC,
        "initial": {
            "raw_mass": v2_bridge.initial_raw_mass,
            "phi1": v2_bridge.initial_phi1,
            "gamma2": v2_bridge.initial_gamma2,
            "aggregate_obstruction_mass": v2_bridge.initial_residual,
        },
        "final": {
            "raw_mass": v2_bridge.final_raw_mass,
            "phi1": v2_bridge.final_phi1,
            "gamma2": v2_bridge.final_gamma2,
            "aggregate_obstruction_mass": v2_bridge.final_residual,
        },
    }
    admission_evidence = {
        **anchors,
        "global_admission": "Refused",
        "admission_codes": list(admission_codes),
        "admission_obstruction_count": admission_obstruction_count,
        "residual_metric": RESIDUAL_METRIC,
        "admission_residual_metric": ADMISSION_RESIDUAL_METRIC,
        "local_mathematical_axes": mathematical_axes,
        "rust_exact_axes": exact_axes,
        "rust_canonical_letters": rust_letters,
        "rust_source_binding_verdicts": source_binding_verdicts,
        "rust_letters_projected_to_outer_tape": False,
        "rust_host_outcome": host_evidence,
        "authority_effect": "None",
    }

    initial_state = str(v2_records[0]["output_state"])
    final_state = receipt.output_state_hash
    logger = TraceLogger(
        runner_id,
        campaign_name=campaign_name,
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step(
        letter="R",
        action_name="bind_symbol_game_v2_and_rust_host_evidence",
        input_state=receipt.input_state_hash,
        output_state=initial_state,
        witness=v2_bridge.bridge_root,
        residual_before=v2_bridge.initial_residual,
        residual_after=v2_bridge.initial_residual,
        effect="residual_carried",
        obstruction_id="|".join(local_obstruction_ids),
        evidence={
            **anchors,
            "local_mathematical_axes": mathematical_axes,
            "rust_exact_axes": exact_axes,
            "rust_host_outcome_validated": validated_host is not None,
            "rust_canonical_letters": rust_letters,
            "rust_source_binding_verdicts": source_binding_verdicts,
            "campaign_evidence": dict(extra_evidence or {}),
            "authority_effect": "None",
        },
        cochain_dim="SymbolGameRun+RustHostOutcomeV1",
        coboundary_map="evidence-root-binding",
    )
    logger.record_step(
        letter="C",
        action_name="separate_mathematical_and_admission_residual_axes",
        input_state=initial_state,
        output_state=initial_state,
        witness=receipt.runtime_id,
        residual_before=v2_bridge.initial_residual,
        residual_after=v2_bridge.initial_residual,
        effect="context_exposed",
        evidence={
            **anchors,
            "local_mathematical_axes": mathematical_axes,
            "admission_residual_metric": ADMISSION_RESIDUAL_METRIC,
            "axes_are_not_interchangeable": True,
            "authority_effect": "None",
        },
        cochain_dim="SymbolGameRun+AdmissionLattice",
        coboundary_map="axis-separation",
    )
    logger.record_step(
        letter="E",
        action_name="retain_verified_local_mathematical_elimination",
        input_state=initial_state,
        output_state=final_state,
        witness=v2_bridge.dda_terminal_hash,
        residual_before=v2_bridge.initial_residual,
        residual_after=v2_bridge.final_residual,
        effect="obstruction_eliminated",
        obstruction_id="|".join(local_obstruction_ids),
        evidence={
            **anchors,
            "residual_metric": RESIDUAL_METRIC,
            "local_mathematical_axes": mathematical_axes,
            "v2_local_e_records": local_e_records,
            "rust_exact_axes": exact_axes,
            "rust_canonical_letters": rust_letters,
            "rust_source_binding_verdicts": source_binding_verdicts,
            "rust_letters_projected_to_outer_tape": False,
            "authority_effect": "None",
        },
        cochain_dim="SymbolGameRun",
        coboundary_map="verified-local-mathematical-retraction",
    )
    logger.refuse(
        reason="global admission refused: " + ",".join(admission_codes),
        input_state=final_state,
        output_state=final_state,
        witness=(
            validated_host.outcome_root_sha256
            if validated_host
            else v2_bridge.bridge_root
        ),
        residual=v2_bridge.final_residual,
        obstruction_id="GLOBAL_ADMISSION:" + "|".join(admission_codes),
        evidence=admission_evidence,
    )

    draft = SymbolGameDdaBridgeReceiptV3(
        packet_id=receipt.packet_id,
        runtime_id=receipt.runtime_id,
        source_event_root=receipt.event_root,
        source_wire_receipt_id=wire_receipt_id,
        v2_bridge=v2_bridge,
        rust_host_outcome_root=(
            validated_host.outcome_root_sha256 if validated_host else None
        ),
        rust_host_request_id_sha256=(
            validated_host.request_id_sha256 if validated_host else None
        ),
        rust_host_outcome_validated=validated_host is not None,
        global_admission="Refused",
        admission_codes=admission_codes,
        admission_obstruction_count=admission_obstruction_count,
        admission_residual_metric=ADMISSION_RESIDUAL_METRIC,
        local_initial_residual=v2_bridge.initial_residual,
        local_final_residual=v2_bridge.final_residual,
        local_residual_metric=RESIDUAL_METRIC,
        dda_dialect=logger.dialect,
        dda_tape=tuple(logger.tape),
        dda_run_id=logger.run_id,
        dda_terminal_hash=str(logger.steps[-1]["step_hash"]),
        dda_trace_path=str(logger.jsonl_path.resolve()),
        bridge_root="",
    )
    return SymbolGameDdaBridgeReceiptV3(
        **{
            **asdict(draft),
            "v2_bridge": v2_bridge,
            "bridge_root": domain_digest(BRIDGE_V3_SCHEMA, _v3_root_payload(draft)),
        }
    )


def verify_symbol_game_dda_bridge_v3(
    source_receipt: RunReceipt,
    bridge_receipt: SymbolGameDdaBridgeReceiptV3,
    *,
    rust_host_outcome: Mapping[str, Any] | None = None,
    expected_host_request_id_sha256: str | None = None,
    expected_host_challenge_hex: str | None = None,
    additional_admission_codes: Iterable[str] = (),
) -> bool:
    """Verify all v3 anchors and the mathematical/admission axis boundary."""

    try:
        if (
            not source_receipt.evidence_valid()
            or source_receipt.authority_effect != "None"
            or bridge_receipt.authority_effect != "None"
            or bridge_receipt.schema_version != BRIDGE_V3_SCHEMA
            or bridge_receipt.global_admission != "Refused"
            or bridge_receipt.admission_residual_metric
            != ADMISSION_RESIDUAL_METRIC
            or bridge_receipt.local_residual_metric != RESIDUAL_METRIC
            or type(bridge_receipt.admission_obstruction_count) is not int
            or bridge_receipt.admission_obstruction_count <= 0
            or bridge_receipt.dda_tape != ("R", "C", "E", "Z", "T")
        ):
            return False
        wire_receipt_id = source_receipt.to_wire_receipt().receipt_id
        if (
            bridge_receipt.packet_id != source_receipt.packet_id
            or bridge_receipt.runtime_id != source_receipt.runtime_id
            or bridge_receipt.source_event_root != source_receipt.event_root
            or bridge_receipt.source_wire_receipt_id != wire_receipt_id
            or not verify_symbol_game_dda_bridge(
                source_receipt, bridge_receipt.v2_bridge
            )
            or bridge_receipt.local_initial_residual
            != bridge_receipt.v2_bridge.initial_residual
            or bridge_receipt.local_final_residual
            != bridge_receipt.v2_bridge.final_residual
            or bridge_receipt.local_initial_residual
            <= bridge_receipt.local_final_residual
        ):
            return False

        if rust_host_outcome is None:
            if (
                bridge_receipt.rust_host_outcome_validated
                or bridge_receipt.rust_host_outcome_root is not None
                or bridge_receipt.rust_host_request_id_sha256 is not None
            ):
                return False
            validated_host = None
        else:
            if (
                expected_host_request_id_sha256 is None
                or expected_host_challenge_hex is None
            ):
                return False
            validated_host = validate_rust_host_outcome(
                rust_host_outcome,
                source_receipt=source_receipt,
                expected_request_id_sha256=expected_host_request_id_sha256,
                expected_challenge_hex=expected_host_challenge_hex,
            )
            if (
                not bridge_receipt.rust_host_outcome_validated
                or bridge_receipt.rust_host_outcome_root
                != validated_host.outcome_root_sha256
                or bridge_receipt.rust_host_request_id_sha256
                != validated_host.request_id_sha256
            ):
                return False
        admission_codes = _global_admission_obstructions(
            validated_host,
            additional_admission_codes,
        )
        if (
            bridge_receipt.admission_codes != admission_codes
            or bridge_receipt.admission_obstruction_count != len(admission_codes)
        ):
            return False

        records = [
            json.loads(line)
            for line in Path(bridge_receipt.dda_trace_path)
            .read_text("utf-8")
            .splitlines()
            if line.strip()
        ]
        if not records or not verify_trajectory_chain(records)[0]:
            return False
        if any(
            previous.get("residual_after") != current.get("residual_before")
            for previous, current in zip(records, records[1:])
        ):
            return False
        tape = tuple(str(record.get("letter", "")) for record in records)
        if (
            tape != bridge_receipt.dda_tape
            or str(records[0].get("dda_dialect")) != bridge_receipt.dda_dialect
            or str(records[0].get("run_id")) != bridge_receipt.dda_run_id
            or str(records[-1].get("step_hash"))
            != bridge_receipt.dda_terminal_hash
        ):
            return False
        DDATapeDFA.validate(".".join(tape), dialect=bridge_receipt.dda_dialect)
        r_evidence = records[0].get("evidence", {})
        if (
            r_evidence.get("source_event_root") != source_receipt.event_root
            or r_evidence.get("source_wire_receipt_id") != wire_receipt_id
            or r_evidence.get("v2_bridge_root")
            != bridge_receipt.v2_bridge.bridge_root
            or r_evidence.get("v2_dda_terminal_hash")
            != bridge_receipt.v2_bridge.dda_terminal_hash
            or r_evidence.get("rust_host_outcome_root")
            != bridge_receipt.rust_host_outcome_root
        ):
            return False
        elimination = records[2]
        if (
            elimination.get("letter") != "E"
            or elimination.get("effect") != "obstruction_eliminated"
            or elimination.get("residual_before")
            != bridge_receipt.local_initial_residual
            or elimination.get("residual_after")
            != bridge_receipt.local_final_residual
            or elimination.get("evidence", {}).get("residual_metric")
            != RESIDUAL_METRIC
        ):
            return False
        refusal = records[3]
        refusal_evidence = refusal.get("evidence", {})
        exact_axes = dict(validated_host.exact_axes) if validated_host else {}
        rust_letters = (
            list(validated_host.rust_canonical_letters) if validated_host else []
        )
        source_binding_verdicts = (
            dict(validated_host.source_binding_verdicts)
            if validated_host
            else {}
        )
        if (
            refusal.get("letter") != "Z"
            or refusal.get("effect") != "refusal"
            or refusal.get("residual_before")
            != bridge_receipt.local_final_residual
            or refusal.get("residual_after")
            != bridge_receipt.local_final_residual
            or refusal_evidence.get("residual_metric")
            != RESIDUAL_METRIC
            or refusal_evidence.get("admission_residual_metric")
            != ADMISSION_RESIDUAL_METRIC
            or refusal_evidence.get("admission_obstruction_count")
            != bridge_receipt.admission_obstruction_count
            or tuple(refusal_evidence.get("admission_codes", ()))
            != bridge_receipt.admission_codes
            or refusal_evidence.get("rust_exact_axes") != exact_axes
            or refusal_evidence.get("rust_canonical_letters") != rust_letters
            or refusal_evidence.get("rust_source_binding_verdicts")
            != source_binding_verdicts
            or refusal_evidence.get("rust_letters_projected_to_outer_tape")
            is not False
            or "Z" in rust_letters
        ):
            return False
        if records[-1].get("letter") != "T":
            return False
        return bridge_receipt.bridge_root == domain_digest(
            BRIDGE_V3_SCHEMA,
            _v3_root_payload(bridge_receipt),
        )
    except (
        KeyError,
        OSError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ):
        return False


__all__ = [
    "ADMISSION_RESIDUAL_METRIC",
    "BRIDGE_SCHEMA",
    "BRIDGE_V3_SCHEMA",
    "PRIME_EVIDENCE_LEVEL",
    "RESIDUAL_METRIC",
    "RUST_HOST_OUTCOME_SCHEMA",
    "SEALED_PRIME002_STATUS",
    "SymbolGameDdaBridgeReceipt",
    "SymbolGameDdaBridgeReceiptV3",
    "ValidatedRustHostOutcome",
    "compute_rust_host_outcome_root",
    "emit_symbol_game_dda_trace",
    "emit_symbol_game_dda_trace_v3",
    "validate_rust_host_outcome",
    "verify_symbol_game_dda_bridge",
    "verify_symbol_game_dda_bridge_v3",
]


