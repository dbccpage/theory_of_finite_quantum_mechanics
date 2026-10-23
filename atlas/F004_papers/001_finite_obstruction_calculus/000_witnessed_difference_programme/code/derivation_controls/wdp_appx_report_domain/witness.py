"""Executable witness for WDP-APPX-REPORT-DOMAIN.

Aligns calibrated model admission (`ideal_calibrated_interval_product`) and
bounded 256-bit raw report semantics over `calibrated_recovery.bridge`.
AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
from fractions import Fraction
from typing import Any

REPO_ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / ".git").exists())
CALIBRATED_CODE_DIR = (
    REPO_ROOT
    / "omega_engine_atlas"
    / "coda_atlas"
    / "F004_papers"
    / "001_finite_obstruction_calculus"
    / "000_witnessed_difference_programme"
    / "code"
)
if str(CALIBRATED_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CALIBRATED_CODE_DIR))

from calibrated_recovery.bridge import (  # noqa: E402
    COST_DOMAIN,
    Channel,
    Model,
    _parse_fraction,
    evaluate,
    model_hash,
    propose_cost,
    validate,
    verify_cost,
)

AUTHORITY_EFFECT = "None"
MAX_RAW_BITS = 256
MAX_RATIONAL_CHARS = 160


def is_canonical_raw_admissible(value: Fraction) -> bool:
    """Return True iff `value` satisfies the 256-bit and 160-char raw parser cap."""
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_RAW_BITS:
        return False
    text = str(value)
    if len(text) > MAX_RATIONAL_CHARS:
        return False
    try:
        parsed = _parse_fraction(text)
    except ValueError:
        return False
    return parsed == value


def raw_preimage_interval(channel: Channel, low: Fraction, high: Fraction) -> tuple[Fraction, Fraction]:
    """Return the exact raw interval `[r_min, r_max]` mapping into calibrated `[low, high]`."""
    r0 = (low - channel.offset) / channel.gain
    r1 = (high - channel.offset) / channel.gain
    return (r0, r1) if r0 <= r1 else (r1, r0)


def check_executable_raw_domain(model: Model) -> dict[str, Any]:
    """Check whether every state's calibrated interval cell admits a canonical 256-bit raw witness."""
    validate(model)
    inadmissible_cells: list[dict[str, Any]] = []
    sample_witnesses: dict[str, dict[str, str]] = {state: {} for state in model.states}
    for channel in model.channels:
        for idx, state in enumerate(model.states):
            low, high = channel.intervals[idx]
            r_min, r_max = raw_preimage_interval(channel, low, high)
            candidates = [r_min, r_max, (r_min + r_max) / 2]
            ceil_int = -(-r_min.numerator // r_min.denominator)
            if Fraction(ceil_int) <= r_max:
                candidates.append(Fraction(ceil_int))
            chosen: str | None = None
            for cand in candidates:
                if r_min <= cand <= r_max and is_canonical_raw_admissible(cand):
                    chosen = str(cand)
                    break
            if chosen is None:
                inadmissible_cells.append(
                    {
                        "channel": channel.name,
                        "state": state,
                        "raw_min_bits": max(r_min.numerator.bit_length(), r_min.denominator.bit_length()),
                        "raw_max_bits": max(r_max.numerator.bit_length(), r_max.denominator.bit_length()),
                    }
                )
            else:
                sample_witnesses[state][channel.name] = chosen
    return {
        "cost_domain": COST_DOMAIN,
        "executable_raw_domain_admissible": len(inadmissible_cells) == 0,
        "inadmissible_cells": inadmissible_cells,
        "sample_witnesses": sample_witnesses,
        "authority_effect": AUTHORITY_EFFECT,
    }


def _make_report(model: Model, visible: str, channel: str, raw_unit: str, value: str) -> dict[str, Any]:
    return {
        "model_sha256": model_hash(model),
        "visible": visible,
        "readings": [{"channel": channel, "raw_unit": raw_unit, "value": value}],
    }


def witness() -> dict[str, Any]:
    """Run the R1 witness, executable raw-domain alignment, and parser boundary controls."""
    # 1. Review R1 witness: ideal cost = 1, raw reading for "high" = 2^510 > 2^256 cap
    r1_model = Model(
        states=("low", "high"),
        visible=("*", "*"),
        answers=("low", "high"),
        channels=(
            Channel(
                name="M",
                raw_unit="raw",
                unit="cal",
                gain=Fraction(1, 2**255),
                offset=Fraction(0),
                intervals=(
                    (Fraction(0), Fraction(0)),
                    (Fraction(2**255), Fraction(2**255)),
                ),
                price=Fraction(1),
            ),
        ),
    )
    r1_cert = propose_cost(r1_model)
    r1_verdict = verify_cost(r1_model, r1_cert)
    r1_domain_check = check_executable_raw_domain(r1_model)
    r1_eval_low = evaluate(
        r1_model,
        _make_report(r1_model, "*", "M", "raw", "0"),
        "low",
    )
    r1_eval_high = evaluate(
        r1_model,
        _make_report(r1_model, "*", "M", "raw", str(2**510)),
        "high",
    )

    # 2. Signed-gain (-1/2) and offset (3/4) calibrated model with executable raw domain
    signed_model = Model(
        states=("s0", "s1"),
        visible=("v", "v"),
        answers=("a0", "a1"),
        channels=(
            Channel(
                name="C_signed",
                raw_unit="tick",
                unit="kelvin",
                gain=Fraction(-1, 2),
                offset=Fraction(3, 4),
                intervals=(
                    (Fraction(-1, 4), Fraction(1, 4)),
                    (Fraction(5, 4), Fraction(7, 4)),
                ),
                price=Fraction(1),
            ),
        ),
    )
    signed_cert = propose_cost(signed_model)
    signed_verdict = verify_cost(signed_model, signed_cert)
    signed_domain_check = check_executable_raw_domain(signed_model)
    # For s1: y in [5/4, 7/4] with y = -1/2 * r + 3/4 => r in [-2, -1]
    signed_eval_s1 = evaluate(
        signed_model,
        _make_report(signed_model, "v", "C_signed", "tick", "-1"),
        "a1",
    )

    # 3. Cap boundary and hostile parser controls
    # Note: bit_length() of 2**255 is 256 (<= 256 cap); bit_length() of 2**256 is 257 (> 256 cap).
    cap_255_eval = evaluate(
        signed_model,
        _make_report(signed_model, "v", "C_signed", "tick", str(2**255)),
        "a0",
    )
    cap_256_eval = evaluate(
        signed_model,
        _make_report(signed_model, "v", "C_signed", "tick", str(2**256)),
        "a0",
    )
    non_canonical_leading_zero = evaluate(
        signed_model,
        _make_report(signed_model, "v", "C_signed", "tick", "01"),
        "a0",
    )
    non_canonical_unreduced = evaluate(
        signed_model,
        _make_report(signed_model, "v", "C_signed", "tick", "2/4"),
        "a0",
    )

    return {
        "target_id": "WDP-APPX-REPORT-DOMAIN",
        "cost_domain": COST_DOMAIN,
        "r1_ideal_verified": r1_verdict.accepted,
        "r1_fixed_cost": r1_cert["finite_certificate"]["fixed"]["value"],
        "r1_adaptive_cost": r1_cert["finite_certificate"]["adaptive"]["value"],
        "r1_executable_raw_domain_admissible": r1_domain_check["executable_raw_domain_admissible"],
        "r1_eval_low_status": r1_eval_low.status,
        "r1_eval_high_2_510_status": r1_eval_high.status,
        "signed_ideal_verified": signed_verdict.accepted,
        "signed_executable_raw_domain_admissible": signed_domain_check["executable_raw_domain_admissible"],
        "signed_eval_s1_status": signed_eval_s1.status,
        "cap_255_status": cap_255_eval.status,
        "cap_256_status": cap_256_eval.status,
        "non_canonical_leading_zero_status": non_canonical_leading_zero.status,
        "non_canonical_unreduced_status": non_canonical_unreduced.status,
        "authority_effect": AUTHORITY_EFFECT,
    }


run_witness = witness


if __name__ == "__main__":
    import json

    print(json.dumps(witness(), indent=2, sort_keys=True))
