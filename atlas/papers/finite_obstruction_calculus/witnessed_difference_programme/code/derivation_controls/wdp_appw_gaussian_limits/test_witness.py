import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appw_gaussian_limits_witness", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("witness loader is missing")
    spec.loader.exec_module(module)
    return module


def _expected():
    f = Fraction
    return {
        "L": 4,
        "M": 1,
        "r": f(0),
        "r_max": f(1, 192),
        "r_inside_disk": 1,
        "fock": 16,
        "half_steps": 2,
        "sites": 4,
        "labels": 8,
        "sqrt_L": 2,
        "scale_denominator": 4,
        "zero_source_trace": 16,
        "weighted_histories": 16,
        "off_support_histories": 240,
        "layers_identity": 1,
        "constant_kappa_1": f(0),
        "constant_kappa_2": f(1, 4),
        "constant_kappa_3": f(0),
        "constant_kappa_4": f(-1, 32),
        "constant_mu_2": f(1, 4),
        "constant_mu_4": f(5, 32),
        "one_site_kappa_2": f(1, 16),
        "one_site_kappa_4": f(-1, 128),
        "carrier_kappa_is_one_site": 0,
        "alternating_supported_zero_count": 16,
        "alternating_supported_phi_sum": f(0),
        "alternating_kappa_1": f(0),
        "alternating_kappa_2": f(0),
        "alternating_kappa_3": f(0),
        "alternating_kappa_4": f(0),
        "alternating_mu_2": f(0),
        "alternating_every_cumulant_zero": 1,
        "alternating_off_support_nonzero": 186,
        "alternating_off_support_zero": 54,
        "alternating_off_support_phi": f(-1, 4),
        "alternating_off_support_weight": 0,
        "chi_0": f(1, 4),
        "chi_equals_constant_kappa_2": 1,
        "chi_equals_alternating_kappa_2": 0,
        "constant_fourth_is_gaussian": 0,
        "gaussian_fourth": f(0),
        "constant_time_independent": 1,
        "alternating_time_independent": 0,
        "schedule_k": 1,
        "schedule_L": 4,
        "schedule_M": 16,
        "on_static_schedule": 0,
        "alternating_in_static_class": 0,
        "majorant_kappa_2": f(16384, 19),
        "constant_inside_majorant": 1,
        "alternating_inside_majorant": 1,
        "majorant_equals_constant_kappa_2": 0,
        "majorant_equals_alternating_kappa_2": 0,
        "joint_spacetime_field_limit": 0,
        "continuum_limit": 0,
    }


def test_finite_carrier_cumulants_are_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    for value in result.values():
        assert type(value) is int or type(value) is Fraction
    assert result["constant_kappa_2"] == Fraction(1, 4)
    assert result["constant_kappa_4"] == Fraction(-1, 32)
    assert result["constant_kappa_4"] == result["constant_mu_4"] - 3 * result["constant_mu_2"] ** 2
    assert result["constant_kappa_1"] == result["constant_kappa_3"] == 0
    assert result["alternating_kappa_2"] == 0
    assert result["alternating_kappa_4"] == 0
    assert result["alternating_supported_phi_sum"] == 0
    assert result["alternating_supported_zero_count"] == result["fock"] == 16
    assert result["alternating_kappa_2"] != result["chi_0"]
    assert result["chi_equals_constant_kappa_2"] == 1
    assert result["chi_equals_alternating_kappa_2"] == 0
    assert result["constant_fourth_is_gaussian"] == 0
    assert result["one_site_kappa_2"] == Fraction(1, 16)
    assert result["one_site_kappa_4"] == Fraction(-1, 128)
    assert result["constant_kappa_2"] != result["one_site_kappa_2"]
    assert result["alternating_kappa_2"] != result["one_site_kappa_2"]
    assert result["carrier_kappa_is_one_site"] == 0
    assert result["schedule_M"] == result["L"] ** 2 == 16
    assert result["M"] != result["schedule_M"]
    assert result["on_static_schedule"] == 0
    assert result["alternating_time_independent"] == 0
    assert result["alternating_in_static_class"] == 0
    assert result["alternating_off_support_nonzero"] + result["alternating_off_support_zero"] == 240
    assert result["alternating_off_support_phi"] == Fraction(-1, 4)
    assert result["alternating_off_support_weight"] == 0
    assert result["zero_source_trace"] == 16
    bound = result["majorant_kappa_2"]
    assert bound == Fraction(16384, 19)
    assert -bound < result["constant_kappa_2"] < bound
    assert -bound < result["alternating_kappa_2"] < bound
    assert result["majorant_equals_constant_kappa_2"] == 0
    assert result["majorant_equals_alternating_kappa_2"] == 0
    assert result["joint_spacetime_field_limit"] == 0
    assert result["continuum_limit"] == 0
    assert result["r"] == 0
    assert 0 <= result["r"] <= result["r_max"]


def test_static_class_and_field_limit_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="alternating 8-label"):
        module.refuse_static_membership("alternating")
    with pytest.raises(ValueError, match="not a Gaussian field"):
        module.refuse_static_membership("constant")
    with pytest.raises(ValueError, match="joint spacetime"):
        module.refuse_joint_spacetime_field()
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(4, Fraction(1, 16))
    module.refuse_higher_dimensional_sum(1, Fraction(1, 16))
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_higher_dimensional_sum(1, 1 / 16)
    with pytest.raises(ValueError, match="outside"):
        module.refuse_outside_temperature(Fraction(1, 10))
    module.refuse_outside_temperature(0)
    module.refuse_outside_temperature(Fraction(1, 192))
