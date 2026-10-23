import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_7d_preflight_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_staged_runner_preflight_and_unknown_cost_retention() -> None:
    module = _load()
    result = module.witness()
    assert result == {
        "runner_exists": True,
        "controller_exists": True,
        "jsonschema_available": True,
        "help_exit_code": 0,
        "legacy_live_refusal_exit_code": 2,
        "guard_code": "LEGACY_LIVE_REQUIRES_CANONICAL_PFP",
        "unknown_cost_committed_cents": 250,
        "collated_committed_cents": 180,
    }


def test_reservation_collation_refuses_invalid_inputs() -> None:
    module = _load()
    with pytest.raises(ValueError, match="within cap"):
        module.check_reservation_collation(100, 200, None)
    with pytest.raises(ValueError, match="exceeds budget cap"):
        module.check_reservation_collation(100, 50, 120)
    with pytest.raises(ValueError, match="positive ints"):
        module.check_reservation_collation(True, 1, None)
