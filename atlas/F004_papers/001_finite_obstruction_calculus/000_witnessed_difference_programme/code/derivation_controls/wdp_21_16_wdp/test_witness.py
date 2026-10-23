import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_21_16_wdp_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_packet_l_and_packet_s_identities_are_exact() -> None:
    module = _load()
    w = module.witness()
    assert w["marginals_equal_half_id"] is True
    assert w["prod_residual_01_expectation"] == Fraction(-1, 4)
    assert w["r_03"] == Fraction(1)
    assert w["r_30"] == Fraction(1)
    assert w["trace_r"] == Fraction(0)
    assert w["trace_r_or"] == Fraction(0)
    assert w["trace_r_zz"] == Fraction(0)
    assert w["trace_rho_or"] == Fraction(0)
    assert w["trace_sigma_or"] == Fraction(0)
    assert w["trace_rho_o"] == Fraction(1, 8)
    assert w["trace_sigma_o"] == Fraction(-1, 8)
    assert w["trace_r_o"] == Fraction(1, 4)
    assert w["r_schatten_1_norm"] * w["beta"] == w["trace_r_o"]
    assert w["l4_alpha_lower_bound"] == Fraction(1, 8)
    assert w["f2_support_sum_xx_yy"] == (0, 0, 1, 1)
    assert len(w["packet_s_kernel"]) == 4
    assert len(w["packet_s_repair"]) == 2
    assert (0, 0, 1) in w["packet_s_unrepaired"]
    assert w["packet_s_quotient_dim"] == 1


def test_cross_packet_and_lieb_robinson_promotions_are_refused() -> None:
    module = _load()
    for invalid in (
        "R_{0,3} == dim(ker Q / B)",
        "Lieb-Robinson triple (C, mu, v)",
        "waiting threshold T >= r/v",
    ):
        with pytest.raises(ValueError, match="WDP-21-16-WDP"):
            module.reject_packet_conjunction_or_lr_adapter(invalid)
