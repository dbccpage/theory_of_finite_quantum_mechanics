"""Finite staged execution with exact certificates and replayable snapshots.

The declared state observers measure the protected skeleton and pending lift IDs
at stage boundaries. Hidden external work and semantic truth are outside this
finite model. AuthorityEffect: None.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Generic, Optional, Sequence, Tuple, TypeVar, Union

from cochain_presentation import QuotientDistanceCertificate, exact_equal, exact_matrix_from_matrix
from coda_fda_core import (
    AuthorizationResult,
    DescentPacket,
    GuardEvidence,
    RefusalCode,
    _validate_exact_bool,
    evaluate_authorization,
)
from sympy import ImmutableMatrix, Rational
from sympy.matrices.matrixbase import MatrixBase

T = TypeVar("T")

@dataclass(frozen=True)
class StageSuccess(Generic[T]):
    value: T

@dataclass(frozen=True)
class StageRefusal(Generic[T]):
    code: RefusalCode
    reason: str

StageResult = Union[StageSuccess[T], StageRefusal[T]]

def _encode(value: Any) -> Any:
    """Encode declared exact finite data; arbitrary repr and floats are excluded."""
    if value is None or type(value) in (bool, str, int):
        return value
    if isinstance(value, (Rational, Fraction)):
        q = Rational(value)
        return {"rational": [int(q.p), int(q.q)]}
    if isinstance(value, MatrixBase):
        m = exact_matrix_from_matrix(value)
        return {"matrix": {"rows": m.rows, "cols": m.cols, "entries": [_encode(v) for v in m]}}
    if isinstance(value, QuotientDistanceCertificate):
        return {n: _encode(getattr(value, n)) for n in ("distance", "repair_witness",
            "residual", "cochain", "dual_witness", "dual_pairing", "repair_map")}
    if isinstance(value, DescentPacket):
        return {n: _encode(getattr(value, n)) for n in ("carrier_k", "evaluator_class_e",
            "verifier_v", "terminalizer_tau", "discipline_lambda")}
    if isinstance(value, (list, tuple)):
        return {"tuple" if isinstance(value, tuple) else "list": [_encode(v) for v in value]}
    if isinstance(value, dict) and all(type(k) is str for k in value):
        return {"dict": [[k, _encode(v)] for k, v in sorted(value.items())]}
    raise TypeError(f"Unsupported trace value: {type(value).__name__}; use exact finite data")

def _json(value: Any) -> str:
    return json.dumps(_encode(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class StageExecutionRecord:
    stage_name: str
    status: str
    input_json: str
    output_json: str
    candidate_id: Optional[str] = None
    error_code: Optional[str] = None

    @property
    def input_digest(self) -> str:
        return hashlib.sha256(self.input_json.encode("utf-8")).hexdigest()

    @property
    def output_digest(self) -> str:
        return hashlib.sha256(self.output_json.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {"stage_name": self.stage_name, "status": self.status,
            "candidate_id": self.candidate_id, "error_code": self.error_code,
            "input": json.loads(self.input_json), "output": json.loads(self.output_json)}

@dataclass(frozen=True)
class CandidateTraceRecord:
    candidate_id: str
    status: str
    skeleton_preserved: bool
    residual_mass: Rational
    descent_json: str
    witness_json: str
    certificate: QuotientDistanceCertificate

    def to_dict(self) -> dict[str, Any]:
        return {"candidate_id": self.candidate_id, "status": self.status,
            "skeleton_preserved": self.skeleton_preserved, "residual_mass": _encode(self.residual_mass),
            "descent": json.loads(self.descent_json), "witness": json.loads(self.witness_json),
            "certificate": _encode(self.certificate)}

@dataclass(frozen=True)
class PipelineTrace:
    pipeline_name: str
    packet: Optional[DescentPacket]
    proposal_id: str
    proposal_json: str
    repair_map_json: str
    stages: Tuple[StageExecutionRecord, ...]
    candidate_records: Tuple[CandidateTraceRecord, ...]
    terminal: Optional[str]
    refusal: Optional[RefusalCode]
    refusal_reason: Optional[str] = None
    residual_certificate: Optional[QuotientDistanceCertificate] = None
    skeleton_before: Optional[str] = None
    skeleton_after: Optional[str] = None
    skeleton_preserved: bool = False
    pending_lifts: Optional[Tuple[str, ...]] = None
    selected_candidate_id: Optional[str] = None

    def payload(self) -> dict[str, Any]:
        return {"schema": 1, "pipeline_name": self.pipeline_name,
            "packet": _encode(self.packet), "proposal_id": self.proposal_id,
            "proposal": json.loads(self.proposal_json), "repair_map": json.loads(self.repair_map_json),
            "stages": [s.to_dict() for s in self.stages],
            "candidate_records": [c.to_dict() for c in self.candidate_records],
            "terminal": self.terminal, "refusal": self.refusal.value if self.refusal else None,
            "refusal_reason": self.refusal_reason, "selected_candidate_id": self.selected_candidate_id,
            "residual_certificate": _encode(self.residual_certificate),
            "skeleton_before": json.loads(self.skeleton_before) if self.skeleton_before is not None else None,
            "skeleton_after": json.loads(self.skeleton_after) if self.skeleton_after is not None else None,
            "skeleton_preserved": self.skeleton_preserved,
            "pending_lifts": list(self.pending_lifts) if self.pending_lifts is not None else None}

    def compute_trace_hash(self) -> str:
        return _hash(self.payload())

    @property
    def trace_id(self) -> str:
        return "trace_" + self.compute_trace_hash()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {**self.payload(), "trace_hash": self.compute_trace_hash()}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @staticmethod
    def verify_serialized(data: dict[str, Any]) -> bool:
        """Verify integrity, not callback soundness or semantic truth."""
        payload = dict(data)
        digest = payload.pop("trace_hash", None)
        return isinstance(digest, str) and _hash(payload) == digest

    def to_guard_evidence(self, replay_deterministic: bool = False) -> GuardEvidence:
        _validate_exact_bool(replay_deterministic, "replay_deterministic")
        checked = tuple(c.candidate_id for c in self.candidate_records if c.status == "verified")
        return GuardEvidence(
            pipeline_accepted=self.terminal is not None and self.refusal is None,
            replay_deterministic=replay_deterministic,
            residual_mass=max((c.residual_mass for c in self.candidate_records), default=Rational(1)),
            skeleton_preserved=self.skeleton_preserved, candidates_checked=len(checked),
            candidates_declared=len(self.packet.evaluator_class_e) if self.packet else 0,
            pending_lifts=len(self.pending_lifts) if self.pending_lifts is not None else 1,
            active_refusal=self.refusal is not None, checked_candidate_ids=checked)

class SealedPipeline:
    """Callbacks plus an independently declared repair map and finite-state observers.

    pending_lifts reads IDs from the routed state. skeleton defaults to the whole
    state; a narrower declared projection permits intentional auxiliary updates.
    """
    def __init__(self, name: str, route: Callable, descend: Callable,
                 verify: Callable, terminalize: Callable, *, repair_map: MatrixBase,
                 pending_lifts: Callable[[Any], Sequence[str]],
                 skeleton: Callable[[Any], Any] = lambda state: state):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Pipeline name must be non-empty")
        self.name, self.route, self.descend = name, route, descend
        self.verify, self.terminalize = verify, terminalize
        self.repair_map = ImmutableMatrix(exact_matrix_from_matrix(repair_map))
        self.pending_lifts, self.skeleton = pending_lifts, skeleton

    def run(self, packet: Optional[DescentPacket], proposal_id: str,
            proposal_data: Any = None) -> PipelineTrace:
        stages: list[StageExecutionRecord] = []
        candidates: list[CandidateTraceRecord] = []
        proposal_json = _json(proposal_data)
        repair_map = self.repair_map
        state = before = after = lifts = selected_id = selected_certificate = None
        preserved = False

        def finish(terminal=None, refusal=None, reason=None):
            return PipelineTrace(self.name, packet, proposal_id, proposal_json,
                _json(repair_map), tuple(stages), tuple(candidates), terminal, refusal,
                reason, selected_certificate, before, after, preserved, lifts, selected_id)

        def invoke(stage, callback, args, candidate_id=None):
            input_json = _json(args)
            try:
                result = callback(*args)
                if not isinstance(result, (StageSuccess, StageRefusal)):
                    raise TypeError("Stage must return StageSuccess or StageRefusal")
                if isinstance(result, StageRefusal):
                    output, error = {"reason": result.reason}, result.code.value
                else:
                    output, error = result.value, None
                output_json = _json(output)
            except Exception as exc:
                result = StageRefusal(RefusalCode.R_contradictory_evidence,
                                      f"{type(exc).__name__}: {exc}")
                output_json, error = _json({"reason": result.reason}), result.code.value
            stages.append(StageExecutionRecord(stage, "refused" if error else "ok",
                input_json, output_json, candidate_id, error))
            return result

        def observe():
            nonlocal after, preserved, lifts
            after = _json(self.skeleton(state))
            preserved = preserved and after == before
            current = self.pending_lifts(state)
            if not isinstance(current, (list, tuple)) or any(type(v) is not str or not v for v in current):
                raise TypeError("pending_lifts must return a finite list/tuple of non-empty IDs")
            if len(set(current)) != len(current):
                raise ValueError("pending lift IDs must be unique")
            lifts = tuple(current)

        if packet is None or not packet.is_valid():
            return finish(refusal=RefusalCode.R_nopacket, reason="Missing or invalid DescentPacket")
        routed = invoke("route", self.route, (proposal_id, proposal_data))
        if isinstance(routed, StageRefusal):
            return finish(refusal=routed.code, reason=routed.reason)
        state = routed.value
        try:
            before = _json(self.skeleton(state))
            preserved = True
            observe()
            selected_descent = selected_witness = None
            for candidate_id in packet.evaluator_class_e:
                descent = invoke("descend", self.descend, (state, proposal_id, candidate_id), candidate_id)
                observe()
                if isinstance(descent, StageRefusal):
                    return finish(refusal=descent.code, reason=descent.reason)
                descent_json = _json(descent.value)
                verified = invoke("verify", self.verify, (state, descent.value), candidate_id)
                observe()
                if isinstance(verified, StageRefusal):
                    return finish(refusal=verified.code, reason=verified.reason)
                witness, certificate = verified.value
                if not isinstance(certificate, QuotientDistanceCertificate):
                    raise TypeError("Verifier must return an exact quotient certificate")
                certificate = certificate.snapshot()
                if (not certificate.verify() or not isinstance(descent.value, MatrixBase)
                    or not exact_equal(certificate.cochain, descent.value)
                    or not exact_equal(certificate.repair_map, repair_map)
                    or _json(descent.value) != descent_json):
                    raise ValueError("Certificate does not verify against descended cochain and declared repair map")
                candidates.append(CandidateTraceRecord(candidate_id, "verified", preserved,
                    certificate.distance, descent_json, _json(witness), certificate))
                if selected_id is None:
                    selected_id, selected_descent, selected_witness = candidate_id, descent.value, witness
                    selected_certificate = certificate
            if not preserved:
                return finish(refusal=RefusalCode.R_candidate, reason="Protected skeleton changed")
            if lifts:
                return finish(refusal=RefusalCode.R_candidate, reason="Pending lifts remain")
            if any(c.residual_mass != 0 for c in candidates):
                return finish(refusal=RefusalCode.R_obstruction, reason="A declared candidate has nonzero residual")
            if (_json(selected_descent) != candidates[0].descent_json
                    or _json(selected_witness) != candidates[0].witness_json):
                return finish(refusal=RefusalCode.R_candidate,
                              reason="A later candidate changed selected evidence")
            selected_before = _json((selected_descent, selected_witness))
            terminal = invoke("terminalize", self.terminalize,
                (state, selected_descent, selected_witness), selected_id)
            observe()
            if isinstance(terminal, StageRefusal):
                return finish(refusal=terminal.code, reason=terminal.reason)
            if type(terminal.value) is not str or not terminal.value:
                raise TypeError("Terminal must be a non-empty string")
            if not preserved or _json((selected_descent, selected_witness)) != selected_before:
                return finish(refusal=RefusalCode.R_candidate, reason="Terminalization changed protected evidence")
            if lifts:
                return finish(refusal=RefusalCode.R_candidate, reason="Terminalization left pending lifts")
            return finish(terminal=terminal.value)
        except Exception as exc:
            return finish(refusal=RefusalCode.R_contradictory_evidence,
                          reason=f"{type(exc).__name__}: {exc}")

@dataclass(frozen=True)
class PipelineAuthorizationReceipt:
    trace: PipelineTrace
    evidence: GuardEvidence
    authorization: AuthorizationResult
    terminal: Optional[str]
    is_authorized: bool
    trace_hash: str
    authority_effect: str = "None"

    def to_dict(self) -> dict[str, Any]:
        return {"trace": self.trace.to_dict(), "terminal": self.terminal,
            "is_authorized": self.is_authorized, "trace_hash": self.trace_hash,
            "authority_effect": self.authority_effect,
            "authorization": {"inhabited": self.authorization.inhabited,
                              "refusal_code": self.authorization.refusal_code}}

class SealedPipelineHarness:
    @staticmethod
    def execute_and_authorize(pipeline: SealedPipeline, packet: Optional[DescentPacket],
            proposal_id: str, proposal_data: Any = None,
            check_replay: bool = True) -> PipelineAuthorizationReceipt:
        _validate_exact_bool(check_replay, "check_replay")
        trace = pipeline.run(packet, proposal_id, proposal_data)
        deterministic = False
        if check_replay and packet is not None and packet.is_valid():
            replay = pipeline.run(packet, proposal_id, proposal_data)
            deterministic = trace.compute_trace_hash() == replay.compute_trace_hash()
        evidence = trace.to_guard_evidence(deterministic)
        # The guard uses all candidates; selected-candidate evidence stays bound in trace.
        authorization = evaluate_authorization(proposal_id, packet, evidence)
        authorized = authorization.inhabited and trace.terminal is not None and trace.refusal is None
        return PipelineAuthorizationReceipt(trace, evidence, authorization,
            trace.terminal if authorized else None, authorized, trace.compute_trace_hash())

