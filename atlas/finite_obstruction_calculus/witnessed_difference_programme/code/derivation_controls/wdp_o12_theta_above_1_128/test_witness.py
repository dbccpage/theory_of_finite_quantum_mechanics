import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_o12_theta_above_1_128_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_closed_disk_and_endpoint_ratios_are_exact() -> None:
    module = _load()
    w = module.witness()
    assert w["ratio_128_over_192"] == Fraction(2, 3)
    assert w["gap_128_minus_192"] == Fraction(1, 384)
    assert w["polymer_bond_label_norm"] == Fraction(1, 128)
    assert w["polymer_source_label_norm"] == Fraction(1, 128)
    assert w["image_ratio_at_128"] == Fraction(3, 4)
    assert w["geometric_wrap_tail"] == Fraction(512, 175)
    assert w["wrap_factor_total"] == Fraction(687, 175)
    assert w["wrap_margin_below_4"] == Fraction(13, 175)
    assert w["formal_endpoint_prefactor"] == Fraction(98304, 43)
    assert w["formal_endpoint_l4"] == Fraction(393216, 43)


def test_lift_error_bound_refuses_at_and_above_1_128() -> None:
    module = _load()
    for invalid_theta in (Fraction(1, 128), Fraction(1, 96), Fraction(1, 64)):
        with pytest.raises(ValueError, match="1/128"):
            module.lift_error_bound(10, invalid_theta)
