"""Contract tests for Fable's packet-first continuation handoff."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from omega_engine_pfp.domain.shared_kernel.canonical import (
    canonical_unwire,
    domain_digest,
)
import pytest

try:
    from omega_engine_pfp.fable_long_horizon_packet import (
        FABLE_V1_PACKET_ID,
        FABLE_V2_INITIAL_STATE_DOMAIN,
        build_fable_long_horizon_packet_v2,
    )
except (ImportError, AttributeError):
    pytestmark = pytest.mark.skip(reason="fable_long_horizon_packet module not present")
from omega_engine_pfp.domain.entities.packet_envelope import PacketEnvelopeV2


SYMBOL_GAME_ROOT = Path(__file__).parents[1] / "omega_engine" / "symbol_game"
TASK_PACKET = SYMBOL_GAME_ROOT / "FABLE_LONG_HORIZON_TASK_PACKET_V2.json"
VERIFICATION_RECEIPT = SYMBOL_GAME_ROOT / "evidence" / "verification_receipt.md"


def _lf_digest(path: Path) -> str:
    text = path.read_bytes().decode("utf-8", errors="strict")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


def test_fable_v2_packet_is_parent_linked_packet_first_and_receipt_bound() -> None:
    wire = json.loads(TASK_PACKET.read_text("utf-8"))
    packet = PacketEnvelopeV2.from_dict(wire)
    payload_text = canonical_unwire(wire["payload"])
    payload = json.loads(payload_text)

    assert packet.to_dict() == wire
    assert packet == build_fable_long_horizon_packet_v2(
        _lf_digest(VERIFICATION_RECEIPT)
    )
    assert packet.parent_event_id == FABLE_V1_PACKET_ID
    assert packet.source_digest == _lf_digest(VERIFICATION_RECEIPT)
    assert packet.initial_state_hash == domain_digest(
        FABLE_V2_INITIAL_STATE_DOMAIN, payload_text
    )
    assert packet.packet_family == "code_change_proposal.bootstrap.v2"
    assert packet.authority_effect == "None"
    assert payload["status"] == "BOOTSTRAP_REFUSED"
    assert payload["authority_effect"] == "None"
    assert payload["communication_protocol"]["primary_surface"] == (
        "packet -> artifact -> receipt -> run_root -> DDA"
    )
    assert payload["communication_protocol"]["prose_role"] == (
        "non-authoritative rendering after machine identifiers"
    )
    assert payload["next_work"][0]["work_id"] == "CODE_CHANGE_PROPOSAL_V1"
    assert payload["next_work"][3]["work_id"] == "RUST_STAGE_ENUM_REFACTOR_V1"
    assert payload["next_work"][4]["work_id"] == "BRIDGE_ROOT_REPLAY_V1"
    assert payload["next_work"][6]["work_id"] == "RESEARCH_PACKET_EXTENSION_V1"
    assert "AUTHENTICATED_ATTESTATION_ABSENT" in payload["blockers"]
    assert "PRIME000_OWNER_LAWS_PARTIAL" in payload["blockers"]
    assert "PYTHON_IMPORT_SOURCE_ATOMICITY_UNPROVEN" in payload["blockers"]


