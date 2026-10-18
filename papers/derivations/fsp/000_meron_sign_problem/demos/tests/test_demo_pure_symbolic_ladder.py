"""Tests for certified pure-wire model ladder results in demos/results/certified_pure_wire_ladder_results.json.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
if str(DEMOS_DIR / "code") not in sys.path:
    sys.path.insert(0, str(DEMOS_DIR / "code"))
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from demo_pure_symbolic_meron import assert_wire_purity

RESULTS_DIR = DEMOS_DIR / "results"
LADDER_FILE = RESULTS_DIR / "certified_pure_wire_ladder_results.json"


def test_pure_wire_model_ladder_reproducibility():
    """Inspect retained packet examples without certifying provider measurements."""
    assert LADDER_FILE.exists()
    data = json.loads(LADDER_FILE.read_text(encoding="utf-8"))

    assert data["protocol"] == "The Symbol Game Pure Gamma38 Symbolic Ladder"
    assert data["alphabet_size"] == 38
    assert data["models_tested"] == 3
    assert data["all_lift_requests_emitted"] is None
    assert data["live_provider_evidence"] is False
    assert data["verified"] is False
    assert data["evidence_scope"] == "unverified_retained_summary"
    assert data["all_terminal_repairs_certified"] is None

    model_map = {m["model"]: m for m in data["model_results"]}
    assert "stealth/space-bunny-alpha" in model_map
    assert "meta-llama/llama-3.3-70b-instruct" in model_map
    assert "meta-llama/llama-3.1-8b-instruct" in model_map

    for model_id, m in model_map.items():
        assert m["lift_request_emitted"] is None
        assert m["exact_repair_certified"] is None
        assert m["exact_partition_z"] == 912
        assert len(m["turns"]) == 4

        for t in m["turns"]:
            assert t["gamma38_pure"] is True
            assert assert_wire_purity(t["emitted_wire"]) is True

        assert m["turns"][2]["stage"] == "LIFT_REQUEST"
        assert m["turns"][2]["emitted_wire"] == "op<<1100><liftreq>>"

        assert m["turns"][3]["stage"] == "EXACT_REPAIR"
        assert m["turns"][3]["emitted_wire"] == "op<<10010><0><1110010000><1>>"
