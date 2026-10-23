"""Source-bound closeout control for PLAN-WDP-REVIEW-CLOSEOUT (R1-R4 and E1-E12).

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
CONTROLS_ROOT = Path(__file__).resolve().parents[1]


def _load_sibling(folder: str):
    path = CONTROLS_ROOT / folder / "witness.py"
    spec = importlib.util.spec_from_file_location(f"{folder}_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_r1_raw_report_domain(value: int) -> bool:
    """R1: Admit 0 <= value < 2^256; refuse bool, negative, or >= 2^256."""
    if type(value) is not int:
        raise ValueError("report value must be an exact integer")
    if value < 0 or value >= (1 << 256):
        raise ValueError("report value outside 256-bit domain")
    return True


def verify_closeout_ledger(root: Path = PACKAGE_ROOT) -> dict[str, object]:
    """Verify R1-R4 and E1-E12 controls together with review_closeout_receipt.json."""
    receipt_path = root / "manifests" / "review_closeout_receipt.json"
    if not receipt_path.is_file():
        raise ValueError("missing manifests/review_closeout_receipt.json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("authority_effect") != "None":
        raise ValueError("review_closeout_receipt authority_effect must be None")
    executions = receipt.get("executions", [])
    if not isinstance(executions, list) or not executions:
        raise ValueError("review_closeout_receipt lacks execution records")

    # R1 check
    admitted_max = check_r1_raw_report_domain((1 << 256) - 1)
    refused_510 = False
    try:
        check_r1_raw_report_domain(1 << 510)
    except ValueError:
        refused_510 = True

    # R2-R4 check from plan_wdp_math_premises
    math_premises = _load_sibling("plan_wdp_math_premises").witness()

    # E1-E12 check from plan_wdp_editorial
    editorial = _load_sibling("plan_wdp_editorial").witness()

    if not admitted_max or not refused_510:
        raise RuntimeError("R1 raw report domain check failed")
    return {
        "r1_max_256_admitted": admitted_max,
        "r1_2_pow_510_refused": refused_510,
        "r2_covariance": math_premises["r2_covariance"],
        "r2_signed_factor": math_premises["r2_signed_factor"],
        "r2_absolute_ratio": math_premises["r2_absolute_ratio"],
        "r3_n2_readout": math_premises["r3_readout"],
        "r4_norm_one": math_premises["r4_norm_one"],
        "r4_norm_two": math_premises["r4_norm_two"],
        "e1_singleton_factors": editorial["e1_singleton_factors"],
        "e2_bounded_min": editorial["e2_bounded_min"],
        "e3_sign_values": editorial["e3_sign_values"],
        "e4_filtered_on_b": editorial["e4_filtered_on_b"],
        "e11_cross_outcome_sum": editorial["e11_cross_outcome_sum"],
        "chapter_11_anchor_ordered": editorial["chapter_11_anchor_ordered"],
        "no_bare_directory_links": editorial["no_bare_directory_links"],
        "execution_record_count": len(executions),
    }


def witness() -> dict[str, object]:
    result = verify_closeout_ledger()
    if (
        result["r2_covariance"] != Fraction(1, 4)
        or result["r2_signed_factor"] != Fraction(0)
        or result["r2_absolute_ratio"] != Fraction(1)
        or result["r3_n2_readout"] != Fraction(3, 4)
        or result["r4_norm_two"] != Fraction(2)
        or result["e1_singleton_factors"] != 1
        or result["e3_sign_values"] != (-2, 2)
        or result["e11_cross_outcome_sum"] != Fraction(0)
        or not result["chapter_11_anchor_ordered"]
        or not result["no_bare_directory_links"]
    ):
        raise RuntimeError("review closeout invariant failed")
    return result
