import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appw_uniform_volume_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_lambda_1_at_1_192_and_m1_are_exact() -> None:
    module = _load()
    w = module.witness()
    assert w["r_plus_2"] == Fraction(385, 192)
    assert w["r2_plus_4r_plus_8"] == Fraction(295681, 36864)
    assert w["factored_den"] == Fraction(455348740, 192**3)
    assert w["denominators_equal"] is True
    assert w["lambda_1_at_1_192"] == Fraction(-1, 87426958080)
    assert w["m1_constant"] == Fraction(24576, 43)


def test_uniform_volume_promotions_are_refused() -> None:
    module = _load()
    for invalid in (
        "uniform in L for G_M",
        "O.12 discharges Appendix W",
        "-1/87426958080 bounds all volumes",
    ):
        with pytest.raises(ValueError, match="G_M"):
            module.reject_uniform_volume_promotion(invalid)
