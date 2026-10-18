from __future__ import annotations
"""Frozen-fixture tests for the sealed GtlaReceipt (frozen_fixtures_v1.md).

Covers F1 (golden pin + F1-analog construct/bind), F2 (tamper), F3 (forged
constructor), F4 (authority widening), F8 (scope widening), F11 (forged hash
fields), and the four-axis layer-path validation. Tests invoke repository
code only — no mocks, no weakened fixtures.
"""


import dataclasses
import json

import pytest

from omega_engine.crates.replay import DescentWitness, GtlaReceipt, ReplayTracePacket

# Behavior pins frozen in
# omega_engine/research/published/001_coda/007_gtla/tests/fixtures/frozen_fixtures_v1.md
GOLDEN_F1_REPLAY_HASH = (
    "00d4f4499db810b77f6a16320e6ea2ff7ce13065532d0aaec140bc1e81b89351"
)
GOLDEN_F1_PACKET = {
    "paper_sha256": "541a24e49c97ec678db613d09aa06dda12497853d79975db3dc46cca5e7cb18e",
    "proposal_sha256": "a" * 64,
    "gate_receipt_sha256": "b" * 64,
    "loop_pass": 1,
    "step_index": 1,
    "status": "CheckPassed",
}
GOLDEN_F1_CANONICAL = (
    '{"authority_effect":"none","gate_receipt_sha256":"' + "b" * 64 + '",'
    '"loop_pass":1,"paper_sha256":'
    '"541a24e49c97ec678db613d09aa06dda12497853d79975db3dc46cca5e7cb18e",'
    '"proposal_sha256":"' + "a" * 64 + '",'
    '"schema_version":"omega.replay_trace.v1","status":"CheckPassed",'
    '"step_index":1}'
)

CLAIM_SHA256 = "541a24e49c97ec678db613d09aa06dda12497853d79975db3dc46cca5e7cb18e"


def _step(**overrides):
    step = {
        "diagnostic_class": "ClosedResidual",
        "routing_terminal": "CheckPassed",
        "extension_status": "NoExtensionNeeded",
        "authority_status": "None",
    }
    step.update(overrides)
    return step


def _receipt(**overrides) -> GtlaReceipt:
    kwargs = dict(
        claim_id="RABBIT_PROMPT_V1",
        claim_sha256=CLAIM_SHA256,
        scope="rabbit-intake-finite-example",
        layer_path=(
            _step(diagnostic_class="NotComputed", routing_terminal="ShapeChecked"),
            _step(diagnostic_class="ExactClass", routing_terminal="Repair"),
            _step(),
        ),
        dda_tape="C · E · T",
        residuals=("fp_grammar", "fp_model_selection"),
        debt=("numeric_answer_uncomputed",),
        unresolved_obligations=("MODEL_UNDERDECLARED",),
    )
    kwargs.update(overrides)
    return GtlaReceipt(**kwargs)


def test_f1_replay_trace_packet_golden_pin() -> None:
    """The frozen F1 golden replay hash of the live owner must not drift."""
    packet = ReplayTracePacket(**GOLDEN_F1_PACKET)
    assert packet.canonical_bytes() == GOLDEN_F1_CANONICAL.encode("utf-8")
    assert packet.replay_hash == GOLDEN_F1_REPLAY_HASH
    witness = DescentWitness.from_verified_replay(packet, GOLDEN_F1_REPLAY_HASH)
    assert witness.replay_hash == GOLDEN_F1_REPLAY_HASH


def test_f1_analog_construct_canonical_bytes_stable_and_witness_binds() -> None:
    first = _receipt()
    second = _receipt()
    assert first.canonical_bytes() == second.canonical_bytes()
    assert first.replay_hash == second.replay_hash

    # Canonical discipline mirrors ReplayTracePacket: sorted keys, tight
    # separators, tuples serialized as lists.
    payload = json.loads(first.canonical_bytes().decode("utf-8"))
    assert list(payload.keys()) == sorted(payload.keys())
    assert isinstance(payload["layer_path"], list)
    assert isinstance(payload["residuals"], list)
    assert payload["schema_version"] == "omega.gtla_receipt.v1"
    assert payload["authority_effect"] == "none"

    witness = DescentWitness.from_verified_replay(first, first.replay_hash)
    assert witness.trace_packet is first
    assert witness.replay_hash == first.replay_hash


def test_f2_tampered_hash_is_refused() -> None:
    receipt = _receipt()
    good = receipt.replay_hash
    flipped = ("0" if good[0] != "0" else "1") + good[1:]
    with pytest.raises(ValueError, match="replay hash mismatch"):
        DescentWitness.from_verified_replay(receipt, flipped)


def test_f2_tampered_payload_is_refused_by_frozen_hash() -> None:
    receipt = _receipt()
    frozen_hash = receipt.replay_hash
    tampered_sha = ("0" if CLAIM_SHA256[0] != "0" else "1") + CLAIM_SHA256[1:]
    tampered = _receipt(claim_sha256=tampered_sha)
    assert tampered.replay_hash != frozen_hash
    with pytest.raises(ValueError, match="replay hash mismatch"):
        DescentWitness.from_verified_replay(tampered, frozen_hash)


def test_f3_forged_witness_constructor_is_sealed() -> None:
    receipt = _receipt()
    with pytest.raises(TypeError, match="sealed"):
        DescentWitness(object(), receipt, receipt.replay_hash)


def test_f4_authority_effect_widening_is_refused() -> None:
    with pytest.raises(ValueError, match="AuthorityEffect::None"):
        _receipt(authority_effect="certified")


def test_f8_scope_widening_changes_bytes_and_old_witness_refuses() -> None:
    receipt = _receipt()
    frozen_hash = receipt.replay_hash
    widened = dataclasses.replace(
        receipt, scope="rabbit-intake-finite-example-plus-everything-else"
    )
    assert widened.canonical_bytes() != receipt.canonical_bytes()
    with pytest.raises(ValueError, match="replay hash mismatch"):
        DescentWitness.from_verified_replay(widened, frozen_hash)


def test_f8_scope_is_frozen_at_construction() -> None:
    receipt = _receipt()
    with pytest.raises(dataclasses.FrozenInstanceError):
        receipt.scope = "widened-scope"  # type: ignore[misc]


@pytest.mark.parametrize(
    "bad_sha",
    [
        "z" * 64,  # non-hex
        CLAIM_SHA256.upper(),  # uppercase
        CLAIM_SHA256[:63],  # truncated
    ],
)
def test_f11_forged_hash_fields_are_refused(bad_sha: str) -> None:
    with pytest.raises(ValueError, match="claim_sha256"):
        _receipt(claim_sha256=bad_sha)


@pytest.mark.parametrize(
    "missing_axis",
    ["diagnostic_class", "routing_terminal", "extension_status", "authority_status"],
)
def test_four_axis_missing_key_is_refused(missing_axis: str) -> None:
    step = _step()
    del step[missing_axis]
    with pytest.raises(ValueError, match=missing_axis):
        _receipt(layer_path=(step,))


def test_four_axis_authority_status_must_be_none_on_every_step() -> None:
    widened_step = _step(authority_status="ContractScopedOnly")
    with pytest.raises(ValueError, match="authority_status must be 'None'"):
        _receipt(layer_path=(_step(), widened_step))


def test_layer_path_step_must_be_a_dict() -> None:
    with pytest.raises(ValueError, match="four axes"):
        _receipt(layer_path=("not-a-step",))


def test_empty_claim_id_and_scope_are_refused() -> None:
    with pytest.raises(ValueError, match="claim_id"):
        _receipt(claim_id="")
    with pytest.raises(ValueError, match="scope"):
        _receipt(scope="")


