"""Unit tests for symbol_game_stage_controller.py.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path

from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
)

from blind_problem import assert_lexical_hygiene
from symbol_game_stage_controller import (
    SymbolGameStageController,
    replay_certified_dag,
)


def test_stage_controller_4site_dag_and_hygiene(tmp_path: Path):
    """Verify 4-site controller runs, generates DAG, satisfies lexical hygiene, and preserves Gamma38 purity."""
    controller = SymbolGameStageController(sites=4)
    nodes = controller.run_pipeline()
    assert len(nodes) == 6

    for n in nodes:
        raw_text = json.dumps(n)
        assert_lexical_hygiene(raw_text)

    for n in nodes:
        wire = n["gamma38_wire"]
        assert all(ch in GAMMA_38 for ch in wire)
        ast = parse_packet(wire)
        validate_packet_semantics(ast)
        assert serialize_packet(ast) == wire

    term = nodes[-1]
    assert term["action"] == "CERTIFY_EXACT_REPAIR"
    assert term["payload"]["status"] == "EXACT_REPAIR"
    assert term["payload"]["exact_partition_z"] == 912
    assert term["payload"]["transfer_matrix_trace"] == 912
    assert term["payload"]["duality_gap"] == "0"


def test_stage_controller_export_and_replay(tmp_path: Path):
    """Verify JSONL DAG export and certified replay report."""
    target_dag = tmp_path / "replay_4site_dag.jsonl"
    report = replay_certified_dag(sites=4, target_path=target_dag)

    assert report["verified"] is True
    assert report["exact_partition_z"] == 912
    assert report["gamma38_valid"] is True
    assert target_dag.exists()

    with target_dag.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 6
