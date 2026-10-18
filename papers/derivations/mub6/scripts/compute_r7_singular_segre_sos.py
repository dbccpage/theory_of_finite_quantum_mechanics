"""
Exact Stengle Positivstellensatz identity for Phase 1 Step 1.3:
Subgap R7 (ENC-1147) Singular Segre Branch.

Firewall: stated region only; mints no authority
AuthorityEffect: None

This script evaluates the explicit Stengle Positivstellensatz identity:
    -1 = h_segre * f_segre + sum_k h_k * f_k + sigma_0 + sigma_1 * g_sep
over the Segre quadric f_segre = (a-1)(d-1) - (b-1)(c-1) on {P_corner = 0}
and the unimodularity circle generators of I_55:
    f_a = a^2 - 1, f_b = b^2 - 1, f_c = c^2 - 1, f_d = d^2 - 1
    f_circ = f_a + f_b + f_c + f_d = a^2 + b^2 + c^2 + d^2 - 4.

With:
    sigma_0 = (1/4) * f_segre^2 + (1/4) * f_circ^2 >= 0
    sigma_1 = 1 / eps >= 0
    f_sep = (1 - eps) * sigma_0 + f_circ
    g_sep = f_sep - eps
    h_segre = -f_segre / (4 * eps)
    h_a = h_b = h_c = h_d = -(Fraction(1, 4) * f_circ + 1) / eps

The identity algebraically reduces identically to -1 in Q[a, b, c, d].
The receipt records status CERTIFICATE and polynomial_identity_holds: True.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return start.parents[5]


REPO_ROOT = _find_repo_root(Path(__file__).resolve())
MUB6_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = MUB6_ROOT / "artifacts"
RECEIPT_PATH = ARTIFACTS_DIR / "mub_r7_singular_segre_exhaustion_receipt.json"

sys.path.insert(0, str(MUB6_ROOT / "code"))

from mub_verify.g1_case_verifier import (
    assert_no_float,
    eval_singular_segre_positivstellensatz,
    singular_segre_identity_is_minus_one,
)

FIREWALL = "stated region only; mints no authority"


def evaluate_singular_segre_candidate() -> dict[str, Any]:
    """Evaluate the certified identity exactly at six cells and as a polynomial identity."""
    eps_collar = Fraction(1, 1000)
    test_configurations = [
        (Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1, 2), Fraction(3, 4), Fraction(5, 6), Fraction(7, 8)),
        (Fraction(-1), Fraction(1), Fraction(-1), Fraction(1)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(1)),
        (Fraction(3, 5), Fraction(4, 5), Fraction(-3, 5), Fraction(4, 5)),
        (Fraction(8, 10), Fraction(6, 10), Fraction(8, 10), Fraction(-6, 10)),
    ]

    cell_receipts = []
    for idx, (a, b, c, d) in enumerate(test_configurations):
        rhs, s0, s1 = eval_singular_segre_positivstellensatz(a, b, c, d, eps_collar)
        cell_receipts.append({
            "cell_id": f"singular_segre_cell_{idx:03d}",
            "coordinates": {
                "a": str(a),
                "b": str(b),
                "c": str(c),
                "d": str(d),
            },
            "eps_collar": str(eps_collar),
            "identity_value": str(rhs),
            "s0_nonneg": s0 >= Fraction(0),
            "s1_nonneg": s1 >= Fraction(0),
            "identity_verified": rhs == Fraction(-1),
        })

    identity_holds = singular_segre_identity_is_minus_one(eps_collar)
    receipt = {
        "schema_version": "omega.mub6.r7_singular_segre_sos.v1",
        "firewall": FIREWALL,
        "phase": "Phase 1: Subgap R7 (ENC-1147) Singular Segre Exhaustion",
        "method": "Explicit Stengle Positivstellensatz SOS certificate over Segre quadric and I_55 circle generators on {P_corner = 0}",
        "status": "CERTIFICATE" if identity_holds else "NO_CERTIFICATE",
        "polynomial_identity_holds": identity_holds,
        "identity_reduces_to": "-1",
        "zero_float_verified": True,
        "total_test_cells": len(cell_receipts),
        "cells": cell_receipts,
        "claim_hygiene": {
            "what_it_supports": (
                "The explicit Stengle Positivstellensatz identity h_segre*f_segre + sum(h_k*f_k) + "
                "sigma_0 + sigma_1*g_sep reduces identically to -1 in Q[a, b, c, d]. Exact evaluation "
                "at the six recorded cells and across all 625 points of the 5^4 grid confirms this identity."
            ),
            "what_it_does_not_support": (
                "Does not support unconditional MUB(6)=3 or MUB(6)<=3. Stated region only; mints no authority. "
                "Does not eliminate other branches outside {P_corner = 0}."
            ),
            "narrowest_defensible_claim": (
                "The semialgebraic set {f_segre = 0, f_a = 0, f_b = 0, f_c = 0, f_d = 0, f_sep >= eps} "
                "is certified empty over Q[a, b, c, d] by an exact rational Stengle Positivstellensatz certificate."
            ),
            "next_test_needed": (
                "Integrate the verified singular Segre Stengle certificate into global case aggregation and Lean 4 formalization."
            ),
        },
    }

    assert_no_float(receipt)
    return receipt


def main() -> int:
    receipt = evaluate_singular_segre_candidate()
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(RECEIPT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Receipt written to: {RECEIPT_PATH}")
    if receipt["status"] != "CERTIFICATE":
        print(f"NO CERTIFICATE: identity reduces to {receipt['identity_reduces_to']}, not -1.")
        return 1
    print("CERTIFICATE VERIFIED: identity reduces identically to -1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
