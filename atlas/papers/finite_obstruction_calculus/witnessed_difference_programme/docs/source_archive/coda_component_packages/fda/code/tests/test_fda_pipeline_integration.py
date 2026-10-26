"""Contract regressions for measured FDA execution; all callbacks use finite data."""
import hashlib
import json
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction

import pytest
from cochain_presentation import LinearRepairProblem
from coda_fda_core import DescentPacket, RefusalCode
from coda_fda_pipeline import (
    PipelineTrace,
    SealedPipeline,
    SealedPipelineHarness,
    StageRefusal,
    StageSuccess,
    _encode,
)
from sympy import Matrix, Rational

MAP = Matrix([[1], [-1]])
GOOD = Matrix([2, -2])
BAD = Matrix([1, 1])

def packet(ids=("first", "second")):
    return DescentPacket("K", list(ids), "V", "tau", "Lambda")

def pipeline(**overrides):
    callbacks = dict(
        route=lambda p, data: StageSuccess({"K": "frozen", "pending": [], "data": data}),
        descend=lambda s, p, c: StageSuccess(GOOD.copy()),
        verify=lambda s, x: StageSuccess(("witness", LinearRepairProblem(MAP).quotient_l1_distance(x))),
        terminalize=lambda s, x, w: StageSuccess(str(list(x))),
        repair_map=MAP,
        pending_lifts=lambda s: s["pending"])
    callbacks.update(overrides)
    return SealedPipeline("finite", **callbacks)

def execute(p=None, **kwargs):
    return SealedPipelineHarness.execute_and_authorize(p or pipeline(), packet(), "proposal", **kwargs)

def test_nominal_bound_trace_and_serialized_integrity():
    data = {"x": [1, Fraction(1, 3)]}
    result = execute(proposal_data=data)
    assert result.is_authorized and result.evidence.checked_candidate_ids == ("first", "second")
    assert result.evidence.pending_lifts == 0 and result.evidence.skeleton_preserved
    assert len(result.trace.stages) == 6
    assert [s.stage_name for s in result.trace.stages] == ["route", "descend", "verify", "descend", "verify", "terminalize"]
    assert result.trace.selected_candidate_id == "first"
    assert result.trace.residual_certificate == result.trace.candidate_records[0].certificate
    serialized = json.loads(result.trace.to_json())
    assert PipelineTrace.verify_serialized(serialized)
    payload = {key: value for key, value in serialized.items() if key != "trace_hash"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert hashlib.sha256(canonical.encode("utf-8")).hexdigest() == serialized["trace_hash"]
    assert result.trace.trace_id.startswith("trace_")
    assert len(result.trace.stages[0].input_digest) == len(result.trace.stages[0].output_digest) == 64
    assert result.to_dict()["is_authorized"]
    original_hash = result.trace.compute_trace_hash()
    data["x"].append(99)
    assert result.trace.compute_trace_hash() == original_hash
    for field in ("packet", "candidate_records", "proposal", "repair_map", "skeleton_before", "pending_lifts"):
        changed = dict(serialized)
        changed[field] = "tampered"
        assert not PipelineTrace.verify_serialized(changed)
    assert not PipelineTrace.verify_serialized({})
    with pytest.raises(FrozenInstanceError):
        result.trace.packet.carrier_k = "changed"
    with pytest.raises(TypeError):
        result.trace.residual_certificate.cochain[0, 0] = 9

@pytest.mark.parametrize("ids", [("bad", "good"), ("good", "bad")])
def test_mixed_candidate_residuals_never_authorize(ids):
    p = pipeline(descend=lambda s, p, c: StageSuccess(BAD.copy() if c == "bad" else GOOD.copy()))
    result = SealedPipelineHarness.execute_and_authorize(p, packet(ids), "p")
    assert not result.is_authorized
    assert result.trace.refusal is RefusalCode.R_obstruction
    assert result.evidence.residual_mass == 2
    assert not any(s.stage_name == "terminalize" for s in result.trace.stages)

@pytest.mark.parametrize("mode", ["cochain", "repair_map", "distance", "untyped", "changed_cochain"])
def test_unbound_or_malformed_certificate_refuses(mode):
    def verify(s, x):
        if mode == "changed_cochain":
            cert = LinearRepairProblem(MAP).quotient_l1_distance(x)
            x[0, 0] = 999
            return StageSuccess(("w", cert))
        cert = LinearRepairProblem(Matrix.eye(2) if mode == "repair_map" else MAP).quotient_l1_distance(
            Matrix([4, -4]) if mode == "cochain" else x)
        if mode == "distance":
            cert = replace(cert, distance=Rational(7))
        if mode == "untyped":
            cert = {"distance": 0}
        return StageSuccess(("w", cert))
    result = execute(pipeline(verify=verify))
    assert not result.is_authorized
    assert result.trace.refusal is RefusalCode.R_contradictory_evidence

@pytest.mark.parametrize("stage", ["route", "descend", "verify", "terminalize"])
@pytest.mark.parametrize("mode", ["refuse", "raise", "unwrapped"])
def test_every_stage_halts_on_refusal_exception_or_invalid_return(stage, mode):
    def stop(*args):
        if mode == "raise":
            raise ValueError("injected callback failure")
        if mode == "unwrapped":
            return "not a StageResult"
        return StageRefusal(RefusalCode.R_candidate, "explicit refusal")
    result = execute(pipeline(**{stage: stop}))
    assert not result.is_authorized and result.trace.stages[-1].stage_name == stage
    assert result.trace.stages[-1].status == "refused"
    assert result.evidence.active_refusal

def test_state_and_terminal_evidence_mutations_refuse():
    def mutate(s, p, c):
        s["K"] = "substituted"
        return StageSuccess(GOOD.copy())
    result = execute(pipeline(descend=mutate))
    assert not result.is_authorized and not result.evidence.skeleton_preserved
    def tamper(s, x, witness):
        x[0, 0] = 9
        return StageSuccess("term")
    result = execute(pipeline(terminalize=tamper))
    assert not result.is_authorized and "protected evidence" in result.trace.refusal_reason

@pytest.mark.parametrize("lifts", [["work"], ["duplicate", "duplicate"], [""], [1], None])
def test_pending_or_invalid_lift_registry_refuses(lifts):
    result = execute(pipeline(pending_lifts=lambda s: lifts))
    assert not result.is_authorized

def test_lift_created_by_terminalizer_is_not_hidden():
    def terminalize(s, x, witness):
        s["pending"].append("new lift")
        return StageSuccess("term")
    result = execute(pipeline(terminalize=terminalize, skeleton=lambda s: s["K"]))
    assert not result.is_authorized and result.evidence.pending_lifts == 1
    assert result.trace.refusal_reason == "Terminalization left pending lifts"

@pytest.mark.parametrize("terminal", ["", None, 1])
def test_terminal_must_be_nonempty_string(terminal):
    result = execute(pipeline(terminalize=lambda *a: StageSuccess(terminal)))
    assert not result.is_authorized

def test_skipped_replay_and_nonselected_witness_nondeterminism_refuse():
    skipped = execute(check_replay=False)
    assert not skipped.is_authorized and not skipped.evidence.replay_deterministic
    counter = 0
    def descend(s, p, c):
        return StageSuccess(GOOD.copy() if c == "first" else Matrix([4, -4]))
    def verify(s, x):
        nonlocal counter
        if x[0] == 4:
            counter += 1
        return StageSuccess((str(counter) if x[0] == 4 else "fixed", LinearRepairProblem(MAP).quotient_l1_distance(x)))
    result = execute(pipeline(descend=descend, verify=verify))
    assert not result.is_authorized and not result.evidence.replay_deterministic
    assert result.authorization.refusal_code == "R_unreplayable"

@pytest.mark.parametrize("input_packet", [None, DescentPacket("", ["x"], "V", "t", "L"),
    DescentPacket("K", [], "V", "t", "L"), DescentPacket("K", ["x", "x"], "V", "t", "L"),
    DescentPacket("K", [""], "V", "t", "L")])
def test_missing_or_invalid_packet(input_packet):
    result = SealedPipelineHarness.execute_and_authorize(pipeline(), input_packet, "p")
    assert not result.is_authorized and result.trace.refusal is RefusalCode.R_nopacket

def test_exact_serialization_and_strict_input_contracts():
    assert _encode((True, 1, "s", Rational(1, 2))) == {"tuple": [True, 1, "s", {"rational": [1, 2]}]}
    assert _encode(Rational(1, 2)) != _encode({"rational": [1, 2]})
    assert _encode([1, 2]) != _encode((1, 2))
    for value in (0.1, object(), {1: "key"}):
        with pytest.raises(TypeError):
            _encode(value)
    with pytest.raises(ValueError):
        SealedPipeline("", None, None, None, None, repair_map=MAP, pending_lifts=lambda s: [])
    with pytest.raises(TypeError):
        execute(check_replay=1)
    with pytest.raises(TypeError):
        execute().trace.to_guard_evidence("yes")



@pytest.mark.parametrize("field", ["cochain", "witness"])
def test_later_candidate_cannot_mutate_selected_evidence(field):
    selected = GOOD.copy()
    witness = ["original"]
    def descend(s, p, candidate):
        if candidate == "second":
            if field == "cochain":
                selected[0], selected[1] = 4, -4
            else:
                witness.append("changed")
            return StageSuccess(Matrix([4, -4]))
        return StageSuccess(selected)
    def verify(s, x):
        return StageSuccess((witness, LinearRepairProblem(MAP).quotient_l1_distance(x)))
    p = pipeline(descend=descend, verify=verify)
    trace = p.run(packet(), "proposal")
    assert trace.refusal is RefusalCode.R_candidate
    assert not any(event.stage_name == "terminalize" for event in trace.stages)


def test_replay_distinguishes_tag_shaped_user_data():
    count = 0
    def verify(s, x):
        nonlocal count
        count += 1
        witness = Rational(1, 2) if count <= 2 else {"rational": [1, 2]}
        return StageSuccess((witness, LinearRepairProblem(MAP).quotient_l1_distance(x)))
    result = execute(pipeline(verify=verify))
    assert not result.is_authorized and not result.evidence.replay_deterministic


def test_declared_repair_model_is_captured_before_callbacks():
    p = pipeline()
    def route(proposal, data):
        p.repair_map = Matrix.eye(2)
        return StageSuccess({"K": "frozen", "pending": []})
    p.route = route
    p.verify = lambda s, x: StageSuccess(("w", LinearRepairProblem(Matrix.eye(2)).quotient_l1_distance(x)))
    trace = p.run(packet(), "proposal")
    assert trace.refusal is RefusalCode.R_contradictory_evidence
    assert json.loads(trace.repair_map_json) == _encode(MAP)

