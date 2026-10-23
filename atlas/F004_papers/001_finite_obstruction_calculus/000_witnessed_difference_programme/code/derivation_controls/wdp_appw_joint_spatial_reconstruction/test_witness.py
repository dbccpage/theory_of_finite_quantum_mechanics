"""Exact checks for the fixed Appendix W spatial-reconstruction obstruction."""

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location(
        "wdp_appw_joint_spatial_reconstruction_witness",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("witness loader is missing")
    spec.loader.exec_module(module)
    return module


def _expected():
    f = Fraction
    return {
        "L": 4,
        "fock": 16,
        "M": 1,
        "N": 2,
        "order": 8,
        "checked_depths": (1, 2, 3, 4),
        "orders": (8, 16, 24, 32),
        "prefactors": (f(1, 16), f(1, 64), f(1, 144), f(1, 256)),
        "quadratic_prefactor": f(1, 16),
        "cell_prefactor": f(1, 16),
        "prefactors_equal": 1,
        "grid_sample": (1, 1, 1, 1),
        "constant_sample": (1, 1, 1, 1),
        "samples_equal": 1,
        "off_grid_value": -1,
        "half_turn_square_is_one": 1,
        "sample_separates": 0,
        "site_count": 4,
        "site_sum": 4,
        "t1_spatial_prefactor": f(1, 4),
        "spatial_reconstruction_defined": 0,
        "probe_bilinear": 10,
        "declared_quadratic": f(5, 8),
        "cell_quadratic": f(5, 8),
        "cell_reproduces_q": 1,
        "reconstructs_kernel": 0,
        "joint_lm_limit": 0,
        "variable_L": 0,
        "continuum_limit": 0,
    }


def _exact(value: object) -> None:
    if type(value) is int or type(value) is Fraction:
        return
    if type(value) is tuple and all(type(item) is int or type(item) is Fraction for item in value):
        return
    raise AssertionError(type(value))


def test_fixed_carrier_obstruction_is_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    for value in result.values():
        _exact(value)
    assert result["fock"] == 2 ** result["L"] == 16
    assert result["N"] == 2 * result["M"] == 2
    assert result["order"] == result["L"] * result["N"] == 8
    assert result["quadratic_prefactor"] == result["cell_prefactor"] == Fraction(1, 16)
    assert result["cell_prefactor"] == Fraction(result["L"], result["order"] ** 2)
    assert result["quadratic_prefactor"] == Fraction(1, result["L"] * result["N"] ** 2)
    for depth, order, prefactor in zip(
        result["checked_depths"],
        result["orders"],
        result["prefactors"],
    ):
        assert order == 8 * depth
        assert prefactor == Fraction(1, 16 * depth * depth)
        assert prefactor == Fraction(result["L"], order ** 2)
        assert prefactor == Fraction(1, result["L"] * (2 * depth) ** 2)
    assert result["prefactors_equal"] == 1
    assert result["grid_sample"] == result["constant_sample"] == (1, 1, 1, 1)
    assert result["samples_equal"] == 1
    assert result["off_grid_value"] == -1
    assert result["off_grid_value"] != result["grid_sample"][0]
    assert result["half_turn_square_is_one"] == 1
    assert result["sample_separates"] == 0
    assert result["site_count"] == 4
    assert result["site_sum"] == sum(result["grid_sample"]) == 4
    assert result["t1_spatial_prefactor"] == Fraction(1, 4)
    assert result["spatial_reconstruction_defined"] == 0
    bilinear = (
        Fraction(1) * Fraction(2) * Fraction(1)
        + Fraction(1) * Fraction(-1) * Fraction(2)
        + Fraction(2) * Fraction(-1) * Fraction(1)
        + Fraction(2) * Fraction(3) * Fraction(2)
    )
    assert bilinear == result["probe_bilinear"] == 10
    assert result["declared_quadratic"] == bilinear / 16 == Fraction(5, 8)
    assert result["cell_quadratic"] == result["declared_quadratic"]
    assert result["cell_quadratic"] == result["quadratic_prefactor"] * result["probe_bilinear"]
    assert result["cell_reproduces_q"] == 1
    assert result["reconstructs_kernel"] == 0
    assert result["joint_lm_limit"] == 0
    assert result["variable_L"] == 0
    assert result["continuum_limit"] == 0


def test_reconstruction_and_continuum_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="spatial reconstruction"):
        module.refuse_joint_spatial_reconstruction()
    with pytest.raises(ValueError, match="kernel K"):
        module.refuse_kernel_reconstruction(Fraction(1, 16))
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_kernel_reconstruction(1 / 16)
    with pytest.raises(ValueError, match="variable L"):
        module.refuse_variable_volume(8)
    with pytest.raises(ValueError, match="no spatial reconstruction"):
        module.refuse_variable_volume(4)
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(4, Fraction(1))
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(8, 1)
    module.refuse_higher_dimensional_sum(1, Fraction(1))
    module.refuse_higher_dimensional_sum(1, 1)
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_higher_dimensional_sum(1, 1.0)
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
