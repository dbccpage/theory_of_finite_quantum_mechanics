import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_chs_o01_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_is_the_five_belief_parity_count() -> None:
    result = _load().witness()
    assert result == {
        "beliefs": 5,
        "winning_cardinality": 2,
        "hi_wins": 1,
        "lo_wins": 1,
        "fork_wins": 0,
        "sink_wins": 0,
        "bait_wins": 0,
        "oscillation_max_priority": 2,
        "sink_cycle_max_priority": 1,
        "fall_cycle_max_priority": 1,
        "cooperative_fork_cycle_max": 2,
        "empty_target_attractor": 0,
        "even_priority_attractor": 3,
        "priority_sum": 7,
        "reachability_trap_contains_hi": 1,
    }


def test_reachability_stand_in_is_refused() -> None:
    module = _load()
    result = module.witness()
    with pytest.raises(ValueError, match="WDP-CHS-N04"):
        module.refuse_reachability_as_parity(result["empty_target_attractor"])
    with pytest.raises(ValueError, match="WDP-CHS-N04"):
        module.refuse_reachability_as_parity(result["even_priority_attractor"])
    with pytest.raises(ValueError, match="WDP-CHS-N04"):
        module.refuse_reachability_as_parity(result["beliefs"])
    with pytest.raises(ValueError, match="priority sum"):
        module.refuse_reachability_as_parity(result["priority_sum"])
    module.refuse_reachability_as_parity(result["winning_cardinality"])
