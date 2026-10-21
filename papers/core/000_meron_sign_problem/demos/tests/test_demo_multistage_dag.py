"""Tests for multi-stage Symbol Game DDC DAG traces in demos/code/demo_multistage_symbol_game.py.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from symbol_game_stage_controller import (
    SymbolGameStageController,
    replay_certified_dag,
)
from omega_engine_pfp.domain.tower.parser import (
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
    LexicalError,
    GAMMA_38,
)


def test_4site_multistage_dag_execution(tmp_path: Path):
    """Verify that the 4-site multi-stage pipeline emits a valid 6-node DAG with EXACT_REPAIR."""
    out_file = tmp_path / "test_4site_dag.jsonl"
    res = replay_certified_dag(sites=4, target_path=out_file)

    assert res["sites"] == 4
    assert res["nodes"] == 6
    assert res["terminal_status"] == "EXACT_REPAIR"
    assert res["exact_partition_z"] == 912
    assert res["gamma38_valid"] is True
    assert res["verified"] is True
    assert out_file.exists()

    # Verify DAG causality: every parent_id must exist in earlier lines
    seen_ids = set()
    with out_file.open("r", encoding="utf-8") as f:
        for line in f:
            node = json.loads(line.strip())
            for pid in node["parent_ids"]:
                assert pid in seen_ids, f"Parent ID {pid} not seen before child {node['node_id']}"
            seen_ids.add(node["node_id"])


def test_gamma38_wire_grammar_strictness():
    """Verify that all wire strings in the controller satisfy Gamma38 and roundtrip losslessly."""
    controller = SymbolGameStageController(sites=4)
    nodes = controller.run_pipeline()

    for node in nodes:
        wire = node["gamma38_wire"]
        # Character set audit
        for ch in wire:
            assert ch in GAMMA_38, f"Illegal character '{ch}' in wire string: {wire}"

        # Roundtrip parse and serialize
        parsed = parse_packet(wire)
        validate_packet_semantics(parsed)
        serialized = serialize_packet(parsed)
        assert serialized == wire

    # Negative control: non-Gamma38 character must raise LexicalError
    with pytest.raises(LexicalError):
        parse_packet("op<<11>_illegal_underscore_>")


def test_lift_request_mechanics():
    """Verify that Stage 3 contains a typed LIFT_REQUEST followed by a causal LIFT_GRANT."""
    controller = SymbolGameStageController(sites=4)
    nodes = controller.run_pipeline()

    node_map = {n["node_id"]: n for n in nodes}
    assert "DAG_N03_LIFT_REQ" in node_map
    assert "DAG_N03_LIFT_GRANT" in node_map

    req = node_map["DAG_N03_LIFT_REQ"]
    grant = node_map["DAG_N03_LIFT_GRANT"]

    assert req["action"] == "REQUEST_LIFT"
    assert req["payload"]["request_type"] == "ACTION_REQUEST_LIFT"
    assert "DAG_N03_LIFT_REQ" in grant["parent_ids"]
    assert grant["action"] == "GRANT_LIFT"
    assert grant["payload"]["decision"] == "LIFT_GRANTED"
    assert grant["payload"]["authorized"] is True
    assert grant["payload"]["weight_preservation"] == "w(tau(C)) == w(C)"
    assert grant["payload"]["sign_inversion"] == "sigma(tau(C)) == -sigma(C)"
