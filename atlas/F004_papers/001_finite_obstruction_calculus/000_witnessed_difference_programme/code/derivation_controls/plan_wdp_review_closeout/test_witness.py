import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_wdp_review_closeout_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_review_closeout_binds_r1_to_r4_and_e1_to_e12() -> None:
    module = _load()
    result = module.witness()
    assert result["r1_max_256_admitted"] is True
    assert result["r1_2_pow_510_refused"] is True
    assert result["r2_covariance"] == Fraction(1, 4)
    assert result["r2_signed_factor"] == Fraction(0)
    assert result["r2_absolute_ratio"] == Fraction(1)
    assert result["r3_n2_readout"] == Fraction(3, 4)
    assert result["r4_norm_one"] == Fraction(1)
    assert result["r4_norm_two"] == Fraction(2)
    assert result["e1_singleton_factors"] == 1
    assert result["e2_bounded_min"] == Fraction(0)
    assert result["e3_sign_values"] == (-2, 2)
    assert result["e4_filtered_on_b"] == (Fraction(0), Fraction(0))
    assert result["e11_cross_outcome_sum"] == Fraction(0)
    assert result["chapter_11_anchor_ordered"] is True
    assert result["no_bare_directory_links"] is True
    assert result["execution_record_count"] >= 1


def test_r1_refuses_bool_negative_and_overflow() -> None:
    module = _load()
    with pytest.raises(ValueError, match="exact integer"):
        module.check_r1_raw_report_domain(True)
    with pytest.raises(ValueError, match="256-bit"):
        module.check_r1_raw_report_domain(-1)
    with pytest.raises(ValueError, match="256-bit"):
        module.check_r1_raw_report_domain(1 << 256)
