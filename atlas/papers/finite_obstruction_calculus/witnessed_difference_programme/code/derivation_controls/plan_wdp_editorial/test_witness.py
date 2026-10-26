import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_wdp_editorial_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_editorial_controls_and_manuscript_reconciliation() -> None:
    module = _load()
    result = module.witness()
    assert result == {
        "e1_two_target_factors": 2,
        "e1_singleton_factors": 1,
        "e1_sections": 0,
        "e2_bounded_min": Fraction(0),
        "e2_unbounded_min": Fraction(-9),
        "e3_sign_values": (-2, 2),
        "e3_raw_bit_values": (-1, 0, 1, 2),
        "e4_raw_on_b": (Fraction(0), Fraction(1)),
        "e4_filtered_on_b": (Fraction(0), Fraction(0)),
        "e11_cross_outcome_sum": Fraction(0),
        "e11_unrestricted_sum": Fraction(1),
        "lean_total": 102,
        "lean_submodule_total": 100,
        "chapter_11_anchor_ordered": True,
        "no_bare_directory_links": True,
    }


def test_invalid_inputs_refuse() -> None:
    module = _load()
    with pytest.raises(ValueError, match="answer_cardinality"):
        module.check_e1_nonsurjective_factor_and_section(0)
    with pytest.raises(ValueError, match="answer_cardinality"):
        module.check_e1_nonsurjective_factor_and_section(True)
    with pytest.raises(ValueError, match="integers"):
        module.check_e2_mixed_sign_weights(True, 2)
