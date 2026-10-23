import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_joint_continuum_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_three_node_moments_and_cubic_aliasing_are_exact() -> None:
    module = _load()
    w = module.witness()
    assert w["nodes"] == (Fraction(1, 16), Fraction(1, 36), Fraction(1, 64))
    assert w["weights_over_105"] == (28, -243, 320)
    assert w["h_on_nodes"] == (Fraction(0), Fraction(0), Fraction(0))
    assert w["h_at_zero"] == Fraction(-1, 36864)
    assert w["moment_0"] == Fraction(1)
    assert w["moment_1"] == Fraction(0)
    assert w["moment_2"] == Fraction(0)
    assert w["neville_on_h"] == Fraction(0)
    assert w["neville_on_h"] != w["h_at_zero"]
    assert w["neville_z0"] == Fraction(20241820, 7)
    assert w["target_3_optimum"] == Fraction(15, 4)
    assert w["target_4_optimum"] == 4
    assert w["target_5_class_count"] == 29771


def test_continuum_and_torus_promotions_are_refused() -> None:
    module = _load()
    for invalid in (
        "-1/36864 is remainder bound",
        "Z=912 is 16-site torus",
        "Q-continuum closed",
    ):
        with pytest.raises(ValueError, match="WDP-JOINT-CONTINUUM"):
            module.reject_continuum_or_torus_promotion(invalid)
