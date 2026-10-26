import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_wdp_math_premises_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_three_carriers_are_exact() -> None:
    result = _load().witness()
    assert result == {
        "r2_states": 16,
        "r2_covariance": Fraction(1, 4),
        "r2_signed_factor": Fraction(0),
        "r2_absolute_ratio": Fraction(1),
        "r3_readout": Fraction(3, 4),
        "r4_norm_one": Fraction(1),
        "r4_norm_two": Fraction(2),
        "r4_unit_product": Fraction(1),
    }
    assert all(type(value) in (int, Fraction) for value in result.values())
    assert result["r2_signed_factor"] < result["r2_covariance"]
    assert result["r3_readout"] != Fraction(1, 3)
    assert result["r4_norm_one"] == result["r4_unit_product"]
    assert result["r4_norm_two"] != result["r4_unit_product"]


def test_dimension_one_value_is_refused_as_input() -> None:
    with pytest.raises(ValueError, match="not an input"):
        _load().sharp_readout(2, Fraction(1, 2), external=Fraction(1, 3))


def test_absolute_endpoint_is_refused() -> None:
    with pytest.raises(ValueError, match="96"):
        _load().refuse_absolute_endpoint()
