import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appm_m4_remainder_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_is_the_three_point_conditional_radius() -> None:
    result = _load().witness()
    assert result == {
        "repetitions": 2,
        "q": 3,
        "L": (4, 6, 8),
        "Z": (912, 33012, 973824),
        "fock": (16, 64, 256),
        "x": (Fraction(1, 16), Fraction(1, 36), Fraction(1, 64)),
        "w": (Fraction(4, 15), Fraction(-81, 35), Fraction(64, 21)),
        "moment_0": Fraction(1),
        "moment_1": Fraction(0),
        "moment_2": Fraction(0),
        "H0": Fraction(-1, 36864),
        "H_nodes": (Fraction(0), Fraction(0), Fraction(0)),
        "unit_triangle": Fraction(197, 35),
        "external_f": Fraction(1),
        "external_c1": Fraction(2, 3),
        "external_c2": Fraction(-4, 5),
        "external_b": (Fraction(1, 5), Fraction(1, 7), Fraction(1, 11)),
        "external_r": (Fraction(1, 5), Fraction(-1, 7), Fraction(1, 11)),
        "gap": Fraction(8907, 13475),
        "carried": Fraction(8907, 13475),
        "radius": Fraction(8907, 13475),
        "weight_over_length": Fraction(5, 6),
        "unlicensed_over_direct_l8": Fraction(20, 3),
        "unlicensed_adopted": 0,
        "bounds_from_samples": 0,
    }
    assert result["H0"] != 0
    assert result["gap"] == result["carried"] == result["radius"]
    assert result["unlicensed_adopted"] == 0
    assert result["bounds_from_samples"] == 0


def test_interior_gap_stays_inside_the_external_radius() -> None:
    module = _load()
    gap, carried = module.projection_gap(
        Fraction(1),
        Fraction(2, 3),
        Fraction(-4, 5),
        (Fraction(1, 10), Fraction(1, 14), Fraction(-1, 22)),
    )
    assert gap == carried == Fraction(-22409, 80850)
    assert abs(gap) < Fraction(8907, 13475)
    overshoot, carried_overshoot = module.projection_gap(
        0,
        0,
        0,
        (1, -1, 1),
    )
    assert overshoot == carried_overshoot == Fraction(197, 35)
    assert module.model_radius((Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))) == Fraction(197, 70)
    assert overshoot > Fraction(197, 70)


def test_samples_do_not_supply_a_scaling_remainder() -> None:
    module = _load()
    result = module.witness()
    with pytest.raises(ValueError, match="scaling remainder"):
        module.refuse_scaling_remainder(result["Z"])
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(2, 912)
    module.refuse_higher_dimensional_sum(1, 912)
    with pytest.raises(ValueError, match="exact integer or rational"):
        module.model_radius((0.1, 0.1, 0.1))
