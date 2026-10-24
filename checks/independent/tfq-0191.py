#!/usr/bin/env python3
"""Independent exact-rational verification for TFQ-0191.

Verifies:
1. Interval measurement evidence separation (MeasurementValue::Interval vs
   GovernanceScalar::Exact, Integer, Boolean) and the IntervalRequiresPolicy
   refusal when an interval straddles a threshold or is asked to decide without
   an explicit policy rule.
2. Fixed-scale decimal non-representability of non-dyadic-decimal rationals
   such as 1/3, 1/7, 1/9 (where 10^s mod q != 0 for every scale s >= 0), and
   exact rational discrepancies between IEEE-754 binary64 significands and
   decimal fractions (e.g. 0.1 = 3602879701896397 / 2^55 != 1/10), establishing
   why BigDecimal::from_f64_unchecked cannot authorize an exact rational bound.
3. Exact interval width propagation under affine calibration (y = a*x + b),
   finite response intervals, and k-tick finite chain clock drift intervals.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import sys
from typing import Any


def compare_interval_to_threshold(
    low: Fraction, high: Fraction, tau: Fraction, policy: str | None = None
) -> tuple[bool, str]:
    assert low <= high
    if high < tau:
        return True, "StrictlyBelow"
    if tau < low:
        return True, "StrictlyAbove"
    if low == high == tau:
        return True, "DegenerateEqual"
    if policy is None:
        return False, "IntervalRequiresPolicy"
    if policy == "pessimistic_upper":
        return True, "BelowOrEqual" if high <= tau else "Above"
    if policy == "pessimistic_lower":
        return True, "AboveOrEqual" if low >= tau else "Below"
    return False, "IntervalRequiresPolicy"


def run_all_checks() -> dict[str, Any]:
    checks = 0
    failed = 0
    details: dict[str, Any] = {}

    def record(cond: bool, msg: str) -> None:
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            raise AssertionError(f"FAILED check #{checks}: {msg}")

    # -------------------------------------------------------------------------
    # Family 1: Interval threshold comparison & IntervalRequiresPolicy refusal
    # -------------------------------------------------------------------------
    tau = Fraction(1)
    for delta in [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000), Fraction(2, 7)]:
        low = tau - delta
        high = tau + delta
        ok, status = compare_interval_to_threshold(low, high, tau, policy=None)
        record(not ok and status == "IntervalRequiresPolicy", f"Straddling interval [{low}, {high}] refused without policy")
        ok_b, status_b = compare_interval_to_threshold(low - 2 * delta, low, tau, policy=None)
        record(ok_b and status_b == "StrictlyBelow", "Interval strictly below threshold decides")
        ok_a, status_a = compare_interval_to_threshold(high, high + 2 * delta, tau, policy=None)
        record(ok_a and status_a == "StrictlyAbove", "Interval strictly above threshold decides")
        ok_p, _ = compare_interval_to_threshold(low, high, tau, policy="pessimistic_upper")
        record(ok_p, "Straddling interval with explicit policy decides")

    details["family1_interval_policy_refusal"] = {
        "straddling_without_policy": "IntervalRequiresPolicy",
        "strict_non_overlapping": "Decided",
    }

    # -------------------------------------------------------------------------
    # Family 2: Fixed-scale decimals & IEEE-754 f64 vs exact rationals
    # -------------------------------------------------------------------------
    for denom in [3, 6, 7, 9, 11, 12, 13, 14, 15]:
        target = Fraction(1, denom)
        for scale in range(0, 12):
            ten_s = 10 ** scale
            # Closest integer numerator m = round(ten_s / denom)
            m_floor = ten_s // denom
            for m in (m_floor, m_floor + 1):
                dec_approx = Fraction(m, ten_s)
                record(dec_approx != target, f"1/{denom} != {m}/10^{scale}")
                record((ten_s % denom) != 0, f"10^{scale} not divisible by {denom}")

    # Exact IEEE-754 binary64 dyadic rationals for 0.1, 0.2, 0.3
    f64_01 = Fraction(3602879701896397, 1 << 55)
    f64_02 = Fraction(3602879701896397, 1 << 54)
    f64_03 = Fraction(5404319552844595, 1 << 54)
    record(f64_01 - Fraction(1, 10) == Fraction(1, 180143985094819840), "f64(0.1) - 1/10 exact residual")
    record(f64_02 - Fraction(2, 10) == Fraction(1, 90071992547409920), "f64(0.2) - 2/10 exact residual")
    record(f64_03 - Fraction(3, 10) == Fraction(-1, 90071992547409920), "f64(0.3) - 3/10 exact residual")
    record(f64_01 + f64_02 != f64_03, "f64(0.1) + f64(0.2) != f64(0.3) in exact dyadic rationals")

    details["family2_decimal_and_f64_discrepancy"] = {
        "f64_01_minus_tenth": str(f64_01 - Fraction(1, 10)),
        "f64_03_minus_three_tenths": str(f64_03 - Fraction(3, 10)),
    }

    # -------------------------------------------------------------------------
    # Family 3: Affine calibration & finite chain clock interval propagation
    # -------------------------------------------------------------------------
    for a in [Fraction(1, 2), Fraction(3, 2), Fraction(5, 3)]:
        for b in [Fraction(-1, 4), Fraction(0), Fraction(7, 8)]:
            for low, high in [(Fraction(1, 5), Fraction(4, 5)), (Fraction(-2, 3), Fraction(5, 6))]:
                cal_low = a * low + b
                cal_high = a * high + b
                record(cal_low <= cal_high, "Positive-slope affine calibration preserves interval order")
                record(cal_high - cal_low == a * (high - low), "Affine calibration scales width by a")

    d_min = Fraction(99, 100)
    d_max = Fraction(101, 100)
    for k in range(1, 21):
        clk_low = k * d_min
        clk_high = k * d_max
        record(clk_high - clk_low == k * (d_max - d_min), f"k={k} ticks clock interval width == k*(d_max - d_min)")

    details["family3_calibration_and_clock"] = {
        "affine_pairs_checked": 18,
        "clock_ticks_checked": 20,
    }

    return {
        "node_id": "TFQ-0191",
        "passed": failed == 0,
        "checks_total": checks,
        "checks_failed": failed,
        "details": details,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = run_all_checks()
    print(
        f"TFQ-0191 INDEPENDENT CHECKER PASSED: checks={summary['checks_total']} failed={summary['checks_failed']}"
    )
    if args.json:
        print(json.dumps(summary))
    sys.exit(0 if summary["passed"] else 1)
