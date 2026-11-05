import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_o8_susceptibility_witness", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("witness loader is missing")
    spec.loader.exec_module(module)
    return module


def _expected():
    return {
        "L": 4,
        "dimension": 16,
        "M": 2,
        "q": 3,
        "r_ceiling": Fraction(1, 192),
        "q_ar1_max": Fraction(385, 384),
        "cleared_gap": 767,
        "q_gap": Fraction(767, 384),
        "euler_r": 4,
        "r_gap": Fraction(767, 192),
        "denominator": 384,
        "ar8_factor": 384,
        "denominator_reason_is_ar8": 0,
        "ar1_member": 0,
        "endpoint_admitted": 1,
        "log3_three_term_lower": Fraction(263, 240),
        "theta_three_term_lower": Fraction(263, 120),
        "temperature_separation": Fraction(2099, 960),
        "temperature_above_ceiling": 1,
        "exp_below_three": 1,
        "factorial_three": 6,
        "two_to_the_two": 4,
        "bond_norm": Fraction(3, 4),
        "bond_lower": Fraction(3, 2),
        "bond_ceiling": Fraction(1, 256),
        "bond_excess": Fraction(383, 256),
        "bond_above_ceiling": 1,
        "schedule_theta": Fraction(1, 48),
        "schedule_gap": Fraction(1, 64),
        "schedule_theta_over_L": Fraction(1, 192),
        "schedule_bound_vanishes": 0,
        "pointwise_susceptibility_supplied": 0,
        "parity_sector_ratio_supplied": 0,
        "theta_scaling_law_supplied": 0,
        "sql_reused": 0,
        "p_second_supplied": 0,
        "p_second_is_gap": 0,
        "continuum_limit": 0,
        "higher_dimensional_sum": 0,
        "outside_limit_fails": 0,
    }


def test_ar1_gap_is_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    assert 3 * 384 - 385 == 767
    assert result["q_ar1_max"] == Fraction(385, 384)
    assert result["cleared_gap"] == 767
    assert result["q_gap"] == Fraction(767, 384)
    assert result["q_gap"] == Fraction(result["cleared_gap"], result["denominator"])
    assert result["r_gap"] / result["M"] == result["q_gap"]
    assert result["euler_r"] == result["M"] * (result["q"] - 1) == 4
    assert result["dimension"] == 1 << result["L"] == 16
    assert result["denominator"] == result["M"] * 192 == 384
    assert result["ar8_factor"] == result["denominator"]
    assert result["denominator_reason_is_ar8"] == 0
    assert result["q"] - result["q_ar1_max"] == result["q_gap"] > 0
    assert result["temperature_separation"] == Fraction(2099, 960) > 0
    assert result["bond_excess"] == Fraction(383, 256) > 0
    assert result["schedule_gap"] == Fraction(1, 64) > 0
    assert result["schedule_bound_vanishes"] == 0
    for value in result.values():
        assert type(value) is int or type(value) is Fraction
        assert type(value) is not float
    for banned in (Fraction(48, 19), Fraction(149, 57), Fraction(12, 19), Fraction(5, 57)):
        assert banned not in result.values()
    assert result["pointwise_susceptibility_supplied"] == 0
    assert result["parity_sector_ratio_supplied"] == 0
    assert result["theta_scaling_law_supplied"] == 0
    assert result["sql_reused"] == 0
    assert result["p_second_supplied"] == 0
    assert result["p_second_is_gap"] == 0
    assert result["continuum_limit"] == 0
    assert result["higher_dimensional_sum"] == 0
    assert result["outside_limit_fails"] == 0
    assert result["ar1_member"] == 0


def test_endpoint_is_admitted_and_fixture_is_refused() -> None:
    module = _load()
    assert module.ring_dimension(4) == 16
    assert module.admit_ar1(2, Fraction(1, 192), Fraction(0)) == Fraction(385, 384)
    assert module.admit_ar1(2, Fraction(0), Fraction(0)) == 1
    with pytest.raises(ValueError, match="1/192"):
        module.admit_ar1(2, Fraction(4), Fraction(0))
    with pytest.raises(ValueError, match="1/192"):
        module.admit_ar1(2, Fraction(1, 192), Fraction(1, 1000))
    with pytest.raises(ValueError, match="exact rational"):
        module.admit_ar1(2, 1 / 192, 0)
    with pytest.raises(ValueError, match="not a law in L"):
        module.ring_dimension(6)
    with pytest.raises(ValueError, match="not an integer"):
        module.ring_dimension(4.0)


def test_excluded_claims_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="susceptibility"):
        module.refuse_pointwise_susceptibility()
    with pytest.raises(ValueError, match="parity-sector"):
        module.refuse_sector_ratio()
    with pytest.raises(ValueError, match="theta growing"):
        module.refuse_theta_scaling()
    with pytest.raises(ValueError, match="not reused"):
        module.refuse_sql_ratio(Fraction(48, 19))
    with pytest.raises(ValueError, match="not reused"):
        module.refuse_sql_ratio(Fraction(149, 57))
    with pytest.raises(ValueError, match="not an SQL ratio"):
        module.refuse_sql_ratio(Fraction(767, 384))
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_sql_ratio(48 / 19)
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(2, Fraction(48, 19))
    with pytest.raises(ValueError, match="outside limit fails"):
        module.refuse_outside_limit()
