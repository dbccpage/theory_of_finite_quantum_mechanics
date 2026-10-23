import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_o12_xlm_comparison_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_free_cosh_hessian_and_row_sums_are_exact() -> None:
    module = _load()
    w = module.witness()
    assert w["x_4_1_at_zero"] == 16
    assert w["unrescaled_row_sum"] == Fraction(1, 16)
    assert w["rescaled_row_sums_all_jk"] == (
        (Fraction(1, 4), Fraction(1, 4)),
        (Fraction(1, 4), Fraction(1, 4)),
    )
    assert w["time_summed_rescaled_row"] == Fraction(1, 2)
    assert w["k_4_0"] == Fraction(1, 4)
    assert w["k_0"] == Fraction(1, 4)
    assert w["gap_r_minus_k0"] == Fraction(0)


def test_positive_theta_and_wrong_rescaling_promotions_are_refused() -> None:
    module = _load()
    for invalid in ("valid for r > 0", "valid for theta > 0", "1/16 == k_0", "1/2 == k_0"):
        with pytest.raises(ValueError, match="X_\\{LM\\}"):
            module.reject_xlm_positive_theta_promotion(invalid)
