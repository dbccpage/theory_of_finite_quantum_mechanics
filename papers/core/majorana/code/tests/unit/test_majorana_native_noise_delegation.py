"""Refusal and state boundaries of the paper's native noise delegates."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

CODE_DIR = Path(__file__).resolve().parents[2]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import majorana_multiqubit_noise as noise_module
import majorana_noise_sweep as sweep_module

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathRefusal,
)


def test_refused_generator_call_preserves_state_and_refusal_evidence(monkeypatch):
    refusal = NativeMathRefusal("TIMEOUT", "native process exceeded deadline", outcome={"id": 7})

    def refused(action, payload):
        raise refusal

    monkeypatch.setattr(sweep_module, "call_native", refused)
    generator = sweep_module.DeterministicRationalNoiseGenerator(42)
    with pytest.raises(NativeMathRefusal) as caught:
        generator.next_fraction()
    assert caught.value is refusal
    assert caught.value.outcome == {"id": 7}
    assert generator._state == 42


def test_refused_circuit_append_preserves_operations_and_elementary_steps(monkeypatch):
    circuit = noise_module.MultiQubitBraidCircuit(2)
    circuit.operations = [("phase", (1, 0))]
    circuit.underlying_circuit.steps = [(1, False)]

    def refused(action, payload):
        raise NativeMathRefusal("INVALID_OPERATION", "unsupported operation")

    monkeypatch.setattr(noise_module, "call_native", refused)
    with pytest.raises(NativeMathRefusal):
        circuit.append_hadamard(2)
    assert circuit.operations == [("phase", (1, 0))]
    assert circuit.underlying_circuit.steps == [(1, False)]


def test_gate_inverse_flags_use_json_booleans_while_operations_keep_integer_flags(monkeypatch):
    seen = []

    def compiled(action, payload):
        seen.append(payload["operations"])
        return {"steps": []}

    monkeypatch.setattr(noise_module, "call_native", compiled)
    circuit = noise_module.MultiQubitBraidCircuit(2)
    circuit.append_elementary(1).append_phase(1, inverse=True).append_hadamard(2)
    assert seen[-1] == [
        ["elementary", [1, False]],
        ["phase", [1, True]],
        ["hadamard", [2, False]],
    ]
    for _, args in seen[-1]:
        assert type(args[1]) is bool
    assert circuit.operations == [("elementary", (1, 0)), ("phase", (1, 1)), ("hadamard", (2, 0))]
    for _, args in circuit.operations:
        assert type(args[1]) is int


@pytest.mark.parametrize("method", ["append_elementary", "append_phase", "append_hadamard"])
@pytest.mark.parametrize("flag", ["false", 0.0, 1.0, 2, None, Fraction(1)])
def test_invalid_inverse_aliases_refuse_before_native_crossing(monkeypatch, method, flag):
    def must_not_cross(action, payload):
        pytest.fail("invalid inverse flag reached native math")

    monkeypatch.setattr(noise_module, "call_native", must_not_cross)
    circuit = noise_module.MultiQubitBraidCircuit(1)
    with pytest.raises(TypeError, match="inverse must be bool or integer 0/1"):
        getattr(circuit, method)(1, inverse=flag)
    assert circuit.operations == []
    assert circuit.underlying_circuit.steps == []


@pytest.mark.parametrize("flag", [False, True, 0, 1])
def test_inverse_contract_preserves_booleans_and_legacy_zero_one(monkeypatch, flag):
    seen = []

    def compiled(action, payload):
        seen.append(payload["operations"])
        return {"steps": []}

    monkeypatch.setattr(noise_module, "call_native", compiled)
    circuit = noise_module.MultiQubitBraidCircuit(1).append_phase(1, inverse=flag)
    assert seen == [[["phase", [1, flag == 1]]]]
    assert type(seen[0][0][1][1]) is bool
    assert circuit.operations == [("phase", (1, int(flag == 1)))]


@pytest.mark.parametrize("operation", ["elementary", "phase", "hadamard"])
@pytest.mark.parametrize("flag", ["false", 0.0])
def test_referee_rejects_invalid_packet_inverse_without_bool_coercion(monkeypatch, operation, flag):
    def must_not_cross(action, payload):
        pytest.fail("invalid packet flag reached native math")

    monkeypatch.setattr(noise_module, "call_native", must_not_cross)
    proposal = noise_module.MultiQubitNoisyBraidProposalPacket(
        round_id="invalid_inverse",
        proposer_id="test",
        num_qubits=1,
        operations=((operation, (1, flag)),),
        noise_couplings=(),
        tolerance_epsilon=Fraction(0),
    )
    receipt = noise_module.MultiQubitNoisyBraidReferee().evaluate(proposal)
    assert receipt.is_accepted is False
    assert "REFUSAL_CIRCUIT_BUILD_FAILED" in receipt.status_reason
    assert "inverse must be bool or integer 0/1" in receipt.status_reason


def test_invalid_native_inverse_flag_refuses_before_mutating_circuit(monkeypatch):
    def compiled(action, payload):
        return {"steps": [[1, "false"]]}

    monkeypatch.setattr(noise_module, "call_native", compiled)
    circuit = noise_module.MultiQubitBraidCircuit(1)
    with pytest.raises(NativeMathRefusal) as caught:
        circuit.append_phase(1)
    assert caught.value.code == "NATIVE_MATH_BRAID_STEPS"
    assert circuit.operations == []
    assert circuit.underlying_circuit.steps == []


def test_referee_preserves_transport_failure_instead_of_relabeling_as_bad_proposal(monkeypatch):
    refusal = NativeMathRefusal("TIMEOUT", "deadline exceeded", outcome={"deadline_ms": 20})

    def refused(action, payload):
        raise refusal

    monkeypatch.setattr(noise_module, "call_native", refused)
    proposal = noise_module.MultiQubitNoisyBraidProposalPacket(
        round_id="test",
        proposer_id="test",
        num_qubits=1,
        operations=(("phase", (1, 0)),),
        noise_couplings=(),
        tolerance_epsilon=Fraction(0),
    )
    with pytest.raises(NativeMathRefusal) as caught:
        noise_module.MultiQubitNoisyBraidReferee().evaluate(proposal)
    assert caught.value is refusal


@pytest.mark.parametrize("value", [True, False, 0.25])
def test_nonexact_coupling_fails_before_native_crossing(monkeypatch, value):
    def must_not_cross(action, payload):
        pytest.fail("invalid scalar reached native math")

    monkeypatch.setattr(noise_module, "call_native", must_not_cross)
    with pytest.raises(TypeError):
        noise_module.LocalMajoranaNoise.stray_couplings(4, [(1, 2, value)])


def test_generator_commits_only_native_state_and_canonical_exact_result(monkeypatch):
    def generated(action, payload):
        assert action == "majorana_noise_generate"
        assert payload == {
            "operation": "fraction",
            "state": 42,
            "max_denom": 50,
            "scale_bound": "1/10",
        }
        return {"state": 2479403867, "value": "1/24"}

    monkeypatch.setattr(sweep_module, "call_native", generated)
    generator = sweep_module.DeterministicRationalNoiseGenerator(42)
    assert generator.next_fraction() == Fraction(1, 24)
    assert generator._state == 2479403867


@pytest.mark.parametrize("value", [True, 1, 0.25, "1/1", " 1 "])
def test_noncanonical_native_fraction_refuses_without_committing_rng_state(monkeypatch, value):
    def generated(action, payload):
        return {"state": 123, "value": value}

    monkeypatch.setattr(sweep_module, "call_native", generated)
    generator = sweep_module.DeterministicRationalNoiseGenerator(42)
    with pytest.raises(NativeMathRefusal) as caught:
        generator.next_fraction()
    assert caught.value.code == "NATIVE_MATH_RATIONAL"
    assert caught.value.outcome == value
    assert generator._state == 42


@pytest.mark.parametrize("value", [True, 0.25, "0/1"])
def test_noise_decoder_rejects_noncanonical_native_coefficients(value):
    with pytest.raises(NativeMathRefusal) as caught:
        noise_module.LocalMajoranaNoise._from_native({"dim": 2, "data": [["0", value], ["0", "0"]]})
    assert caught.value.code == "NATIVE_MATH_RATIONAL"
