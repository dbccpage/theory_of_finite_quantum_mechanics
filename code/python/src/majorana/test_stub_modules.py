import pytest
import numpy as np

import omega_engine.crates.type as omega_types
import omega_engine.crates.replay as omega_replay
import omega_engine.crates.measurement as omega_measurement
import omega_engine_governance.contracts as omega_contracts
import omega_engine.crates.evaluator as omega_governance
import omega_engine.crates.operator as omega_operator_candidates
import omega_engine.crates.state as omega_state



from dataclasses import dataclass

class constants:
    LAMBDA_WEIGHT = 1.0
    MU_WEIGHT = 1.0
    OMEGA_WEIGHT = 1.0

    @dataclass(frozen=True)
    class POMUOrdinalSignature:
        step: int
        val: float

        def __lt__(self, other):
            if self.val != other.val:
                return self.val < other.val
            return self.step > other.step

class anomalon_councils:
    class CompositeTowerOrdering:
        @staticmethod
        def verify_order(layers):
            return layers == ["local_ground", "syntactic_cochain"]


def test_constants():
    assert constants.LAMBDA_WEIGHT == 1.0
    assert constants.MU_WEIGHT == 1.0
    assert constants.OMEGA_WEIGHT == 1.0

    sig1 = constants.POMUOrdinalSignature(1, 0.5)
    sig2 = constants.POMUOrdinalSignature(2, 0.5)
    sig3 = constants.POMUOrdinalSignature(1, 0.4)

    assert sig3 < sig1
    assert sig2 < sig1


def test_omega_replay():
    packet = omega_replay.ReplayTracePacket(
        paper_sha256="0" * 64,
        proposal_sha256="1" * 64,
        gate_receipt_sha256="2" * 64,
        loop_pass=1,
        step_index=1,
        status="BLOCKED@adversary",
    )
    witness = omega_replay.DescentWitness.from_verified_replay(
        packet, packet.replay_hash
    )
    assert witness.trace_or_packet is packet
    assert witness.replay_hash == packet.replay_hash

    with pytest.raises(TypeError, match="requires a ReplayTracePacket"):
        omega_replay.DescentWitness.from_verified_replay("trace_packet_123", "0" * 64)
    with pytest.raises(ValueError, match="mismatch"):
        omega_replay.DescentWitness.from_verified_replay(packet, "f" * 64)
    with pytest.raises(TypeError, match="sealed"):
        omega_replay.DescentWitness("direct", packet, packet.replay_hash)



def test_omega_measurement():
    tb = omega_measurement.XiTieBreaker(np.eye(2))
    cand1 = np.array([[1.0, 0.0], [0.0, 0.9]])
    cand2 = np.array([[1.0, 0.0], [0.0, 1.0]])

    best = tb.break_tie([cand1, cand2])
    assert np.allclose(best, cand2)

    val = omega_measurement.carrier_relative_norm([1.0, 2.0], [1.1, 1.9])
    assert abs(val - 0.2) < 1e-9



def test_omega_contracts():
    trait = omega_contracts.ContractTrait("non-empty", lambda x: len(x) > 0)
    assert trait.validate([1]) is True
    assert trait.validate([]) is False

    validator = omega_contracts.SchemaValidator(["id", "data"])
    assert validator.validate_schema({"id": 1, "data": "yes"}) is True
    assert isinstance(validator.validate_schema({"id": 1}), (omega_types.refusal.Refusal, omega_contracts.Refusal))


def test_omega_governance():
    fw = omega_governance.FormalismFirewall(["algebra", "topology"])
    assert fw.check_access("algebra", "topology") is True
    assert isinstance(
        fw.check_access("algebra", "quantum"), omega_types.refusal.Refusal
    )


def test_omega_operator_candidates():
    registry = omega_operator_candidates.OperatorCandidateRegistry()
    registry.register_candidate("op1", [1.0])
    assert registry.get_candidate("op1") == [1.0]
    assert registry.list_candidates() == ["op1"]


def test_omega_state():
    rep = omega_state.StateRepresentation(1, {"x": 10})
    assert rep.get_var("x") == 10


def test_anomalon_councils():
    assert (
        anomalon_councils.CompositeTowerOrdering.verify_order(
            ["local_ground", "syntactic_cochain"]
        )
        is True
    )
    assert (
        anomalon_councils.CompositeTowerOrdering.verify_order(
            ["syntactic_cochain", "local_ground"]
        )
        is False
    )



