import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_o8_critical_scaling_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_order_theta1_jet_and_mesh_exponent_are_exact() -> None:
    module = _load()
    w = module.witness()
    assert w["trace_4p"] == 4
    assert w["four_p_idempotent_scaled"] is True
    assert w["normalized_trace_p"] == Fraction(1, 4)
    assert w["bond_expectation_p_a0_a1"] == Fraction(1, 16)
    assert w["bond_expectation_k_a0_a1"] == Fraction(-1, 16)
    assert w["c00_at_theta0"] == Fraction(1, 4)
    assert w["c0y_theta1_jet"] == (
        Fraction(0),
        Fraction(1, 16),
        Fraction(0),
        Fraction(1, 16),
    )
    assert w["u_independent"] is True
    assert w["spatial_sum_theta1"] == Fraction(1, 8)
    assert w["zero_mode_1_matches_spatial_sum"] is True
    assert w["ratio_l6_over_l4"] == Fraction(1)
    assert w["mesh_exponent_alpha"] == 0
    assert w["tl3_decay_base_at_1_192"] == Fraction(1, 2)


def test_critical_scaling_promotions_are_refused() -> None:
    module = _load()
    for invalid in (
        "alpha=0 proves critical scaling",
        "L^{-1/2} derived",
        "ZERO_MODE[1]=1/8 is continuum field",
    ):
        with pytest.raises(ValueError, match="WDP-O8-CRITICAL-SCALING"):
            module.reject_critical_scaling_promotion(invalid)
