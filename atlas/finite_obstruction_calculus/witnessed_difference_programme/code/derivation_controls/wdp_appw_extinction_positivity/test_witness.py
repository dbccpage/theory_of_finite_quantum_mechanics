import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appw_extinction_positivity_witness", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("witness loader is missing")
    spec.loader.exec_module(module)
    return module


def _expected():
    theta = Fraction(1, 10)
    e4 = Fraction(80, 79) ** 32
    e16 = Fraction(20, 19) ** 32
    margin = Fraction(
        "5297450670659957549009604563595170759963655420038456036451841"
        "/31691265005705735037417580134400000000000000000000000000000000"
    )
    numerator = Fraction(
        "30560470964558734288104504638287074496011024223750634559368395993854771200000000000000000000000000000000"
        "/440739679775466657209593615746337787110017959752239652332942001202028305587856238247631064241116048001"
    )
    if e4 != (1 - theta / 8) ** (-32) or e16 != (1 - theta / 2) ** (-32):
        raise AssertionError("closed majorant disagrees with the envelope")
    if margin != Fraction(79 ** 32, 4 * 80 ** 32):
        raise AssertionError("stored margin disagrees with 79^32/(4*80^32)")
    if numerator != 4 * (30 * (theta + theta ** 2) * e16 + 2 * theta * e4):
        raise AssertionError("stored numerator disagrees with the schedule")
    return {
        "L": 4,
        "fock": 16,
        "theta": theta,
        "B": 1,
        "D": 0,
        "E4": e4,
        "E16": e16,
        "margin": margin,
        "numerator": numerator,
        "M0": 415,
        "floor_quotient": 414,
        "one_point_eigenvalue": Fraction(-1, 706440),
        "one_point_quadratic": Fraction(-1, 88305),
        "edge_lambda": Fraction(-1, 87426958080),
        "one_point_psd": 0,
        "one_point_outside_edge": 1,
        "edge_is_positivity_certificate": 0,
        "g_m_positive": 0,
        "field_limit_extinction": 0,
        "beyond_one_point_closed": 0,
        "continuum_limit": 0,
    }


def test_constant_profile_schedule_is_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    for key in (
        "theta",
        "E4",
        "E16",
        "margin",
        "numerator",
        "one_point_eigenvalue",
        "one_point_quadratic",
        "edge_lambda",
    ):
        assert type(result[key]) is Fraction
    for key in (
        "L",
        "fock",
        "B",
        "D",
        "M0",
        "floor_quotient",
        "one_point_psd",
        "one_point_outside_edge",
        "edge_is_positivity_certificate",
        "g_m_positive",
        "field_limit_extinction",
        "beyond_one_point_closed",
        "continuum_limit",
    ):
        assert type(result[key]) is int
    assert result["M0"] * result["margin"] > result["numerator"]
    assert (result["M0"] - 1) * result["margin"] <= result["numerator"]
    assert result["floor_quotient"] == result["numerator"] // result["margin"]
    assert 8 * result["one_point_eigenvalue"] == result["one_point_quadratic"]
    assert result["edge_lambda"] < 0
    assert result["margin"] != result["one_point_eigenvalue"]
    assert result["beyond_one_point_closed"] == 0
    assert result["g_m_positive"] == 0
    assert result["field_limit_extinction"] == 0
    assert result["continuum_limit"] == 0


def test_extinction_or_positivity_beyond_the_record_is_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="stays open"):
        module.refuse_extinction_or_positivity("field-limit-extinction")
    with pytest.raises(ValueError, match="not positivity"):
        module.refuse_extinction_or_positivity("one-point-record")
    with pytest.raises(ValueError, match="Gate E"):
        module.refuse_gate_e_matrix()
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(8, Fraction(-1, 706440))
    module.refuse_higher_dimensional_sum(1, Fraction(-1, 706440))
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
    with pytest.raises(ValueError, match="L is outside"):
        module.schedule(sites=5)
    with pytest.raises(ValueError, match="profile"):
        module.schedule(amplitude=2)
    with pytest.raises(ValueError, match="exact rational"):
        module.schedule(theta=0.1)
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_higher_dimensional_sum(1, -1 / 706440)
