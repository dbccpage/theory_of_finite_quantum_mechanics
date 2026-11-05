import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_chs_o02_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_is_the_no_fallback_triple() -> None:
    result = _load().witness()
    assert result == {
        "witness": (1, 0, 6),
        "original_solutions": 1,
        "winning_strategies_from_initial": 0,
        "restored_value": 6,
        "emittable_valid": 0,
        "vacuous_soundness": 1,
        "coverage": 0,
        "carrier_rows": 9,
        "named_proposal": 4,
        "guarded_operating": Fraction(9, 2),
        "guarded_with_setup": Fraction(15, 2),
        "blind_scan_with_setup": Fraction(39, 2),
        "ledger": 17,
        "a1_proved": 0,
        "a3_proved": 0,
        "goal_closed": 0,
    }


def test_assumption_label_and_other_menus_are_refused() -> None:
    module = _load()
    result = module.witness()
    with pytest.raises(ValueError, match="WDP-CHS-N03"):
        module.refuse_as_strategy_count("A1")
    with pytest.raises(ValueError, match="WDP-CHS-N03"):
        module.refuse_as_strategy_count("A3")
    with pytest.raises(ValueError, match="not the no-fallback"):
        module.refuse_as_strategy_count(result["original_solutions"])
    for key in (
        "named_proposal",
        "guarded_operating",
        "guarded_with_setup",
        "blind_scan_with_setup",
        "ledger",
        "restored_value",
    ):
        with pytest.raises(ValueError, match="not the no-fallback"):
            module.refuse_as_strategy_count(result[key])
    with pytest.raises(TypeError, match="float"):
        module.refuse_as_strategy_count(0.0)
    module.refuse_as_strategy_count(result["winning_strategies_from_initial"])
