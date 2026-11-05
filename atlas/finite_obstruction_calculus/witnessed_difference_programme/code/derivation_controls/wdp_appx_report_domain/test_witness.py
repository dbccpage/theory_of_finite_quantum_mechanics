"""Tests for WDP-APPX-REPORT-DOMAIN executable witness."""

from __future__ import annotations

import pathlib
import sys

THIS_DIR = pathlib.Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from .witness import witness  # noqa: E402


def test_wdp_appx_report_domain_witness() -> None:
    res = witness()
    assert res["target_id"] == "WDP-APPX-REPORT-DOMAIN"
    assert res["cost_domain"] == "ideal_calibrated_interval_product"
    assert res["r1_ideal_verified"] is True
    assert res["r1_fixed_cost"] == "1"
    assert res["r1_adaptive_cost"] == "1"
    assert res["r1_executable_raw_domain_admissible"] is False
    assert res["r1_eval_low_status"] == "VERIFIED"
    assert res["r1_eval_high_2_510_status"] == "INVALID_REPORT"
    assert res["signed_ideal_verified"] is True
    assert res["signed_executable_raw_domain_admissible"] is True
    assert res["signed_eval_s1_status"] == "VERIFIED"
    assert res["cap_255_status"] == "INCONSISTENT"
    assert res["cap_256_status"] == "INVALID_REPORT"
    assert res["non_canonical_leading_zero_status"] == "INVALID_REPORT"
    assert res["non_canonical_unreduced_status"] == "INVALID_REPORT"
    assert res["authority_effect"] == "None"
