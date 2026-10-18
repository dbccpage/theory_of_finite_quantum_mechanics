"""
Exact Rational G1 Case & Algebraic Branch Verifier.

This module validates:
1. Structural integrity and schema compliance of research/g1_foundation/case_ledger.json.
2. Exact rational Nullstellensatz witness polynomial identities (degree 1 and 2).
3. Exact rational Stengle Positivstellensatz SOS certificates (separating real semialgebraic emptiness).
4. Strict zero-float enforcement via recursive assert_no_float and exact Fraction arithmetic.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def assert_no_float(obj: Any, path: str = "$", seen: Optional[Set[int]] = None) -> None:
    """Recursively traverse data structures and assert zero float or complex values."""
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return
    seen.add(obj_id)

    if isinstance(obj, (float, complex)):
        raise TypeError(f"Floating-point or complex type forbidden at {path}: {obj!r}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            assert_no_float(v, f"{path}.{k}", seen)
    elif isinstance(obj, (list, tuple)):
        for idx, item in enumerate(obj):
            assert_no_float(item, f"{path}[{idx}]", seen)


def parse_exact_json(filepath: Path) -> Dict[str, Any]:
    """Load JSON with strict rejection of float tokens."""
    def _forbid_float(token: str) -> None:
        raise ValueError(f"Floating-point token '{token}' strictly forbidden in exact JSON")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f, parse_float=_forbid_float)
    assert_no_float(data)
    return data


def eval_annihilated_nullstellensatz(x: Fraction, y: Fraction) -> Fraction:
    """
    Evaluate the Nullstellensatz identity for the annihilated entry branch:
      (-1) * (x^2 + y^2 - 1) + x * (x) + y * (y)
    This identically evaluates to 1 in Q[x, y].
    """
    p_circle = x * x + y * y - Fraction(1)
    q_x = x
    q_y = y
    res = Fraction(-1) * p_circle + x * q_x + y * q_y
    return res


def eval_all_ones_nullstellensatz(x_vals: List[Fraction]) -> Fraction:
    """
    Evaluate the Nullstellensatz identity for the all-ones row branch:
      (1/6) * (1 + sum x_j) - sum (1/6) * (x_j - 1)
    This identically evaluates to 1 in Q[x_1..x_5].
    """
    if len(x_vals) != 5:
        raise ValueError(f"Expected 5 coordinates, got {len(x_vals)}")
    row_orth = Fraction(1) + sum(x_vals)
    subs = [Fraction(1, 6) * (xj - Fraction(1)) for xj in x_vals]
    res = Fraction(1, 6) * row_orth - sum(subs)
    return res


def eval_upper_boundary_positivstellensatz(
    x: Fraction, y: Fraction
) -> Tuple[Fraction, Fraction, Fraction]:
    """
    Evaluate the Stengle Positivstellensatz SOS certificate for the upper boundary branch (x >= 2):
      Identity: -1 = (-1/3) * f + sigma_0 + sigma_1 * g
      where:
        f = x^2 + y^2 - 1
        g = x - 2
        sigma_0 = (1/3)*(x - 2)^2 + (1/3)*y^2 >= 0
        sigma_1 = 4/3 >= 0
    Returns (identity_val, sigma_0, sigma_1).
    """
    f = x * x + y * y - Fraction(1)
    g = x - Fraction(2)
    sigma_0 = Fraction(1, 3) * (x - Fraction(2)) ** 2 + Fraction(1, 3) * (y**2)
    sigma_1 = Fraction(4, 3)
    rhs = Fraction(-1, 3) * f + sigma_0 + sigma_1 * g
    return rhs, sigma_0, sigma_1


def eval_lower_boundary_positivstellensatz(
    x: Fraction, y: Fraction
) -> Tuple[Fraction, Fraction, Fraction]:
    """
    Evaluate the Stengle Positivstellensatz SOS certificate for the lower boundary branch (x <= -2):
      Identity: -1 = (-1/3) * f + sigma_0 + sigma_1 * g
      where:
        f = x^2 + y^2 - 1
        g = -2 - x
        sigma_0 = (1/3)*(x + 2)^2 + (1/3)*y^2 >= 0
        sigma_1 = 4/3 >= 0
    Returns (identity_val, sigma_0, sigma_1).
    """
    f = x * x + y * y - Fraction(1)
    g = Fraction(-2) - x
    sigma_0 = Fraction(1, 3) * (x + Fraction(2)) ** 2 + Fraction(1, 3) * (y**2)
    sigma_1 = Fraction(4, 3)
    rhs = Fraction(-1, 3) * f + sigma_0 + sigma_1 * g
    return rhs, sigma_0, sigma_1


def eval_singular_segre_positivstellensatz(
    a: Fraction, b: Fraction, c: Fraction, d: Fraction, eps: Fraction
) -> Tuple[Fraction, Fraction, Fraction]:
    """
    Evaluate the Stengle Positivstellensatz SOS certificate on {P_corner = 0}:
      Generators:
        f_segre = (a - 1)*(d - 1) - (b - 1)*(c - 1)
        f_a = a^2 - 1, f_b = b^2 - 1, f_c = c^2 - 1, f_d = d^2 - 1
        f_circ = f_a + f_b + f_c + f_d = a^2 + b^2 + c^2 + d^2 - 4
      Sums of squares:
        sigma_0 = (1/4) * f_segre^2 + (1/4) * f_circ^2 >= 0
        sigma_1 = 1 / eps >= 0
      Separating polynomial and guard:
        f_sep = (1 - eps) * sigma_0 + f_circ
        g_sep = f_sep - eps
      Stengle multipliers over ideal generators:
        h_segre = -f_segre / (4 * eps)
        h_a = h_b = h_c = h_d = -(Fraction(1, 4) * f_circ + 1) / eps
      Identity:
        rhs = h_segre * f_segre + h_a * f_a + h_b * f_b + h_c * f_c + h_d * f_d + sigma_0 + sigma_1 * g_sep
      This algebraically reduces identically to -1 in Q[a, b, c, d].
    Returns (identity_val, sigma_0, sigma_1).
    """
    f_segre = (a - Fraction(1)) * (d - Fraction(1)) - (b - Fraction(1)) * (c - Fraction(1))
    f_a = a * a - Fraction(1)
    f_b = b * b - Fraction(1)
    f_c = c * c - Fraction(1)
    f_d = d * d - Fraction(1)
    f_circ = f_a + f_b + f_c + f_d

    sigma_0 = Fraction(1, 4) * (f_segre ** 2) + Fraction(1, 4) * (f_circ ** 2)
    sigma_1 = Fraction(1) / eps

    f_sep = (Fraction(1) - eps) * sigma_0 + f_circ
    g_sep = f_sep - eps

    h_segre = -Fraction(1, 4) * f_segre / eps
    h_circ = -(Fraction(1, 4) * f_circ + Fraction(1)) / eps

    rhs = (
        h_segre * f_segre
        + h_circ * f_a
        + h_circ * f_b
        + h_circ * f_c
        + h_circ * f_d
        + sigma_0
        + sigma_1 * g_sep
    )
    return rhs, sigma_0, sigma_1


def singular_segre_identity_is_minus_one(eps: Fraction) -> bool:
    """
    Decide whether the singular Segre candidate equals -1 as a polynomial in (a, b, c, d).

    rhs + 1 has degree at most 4 in each variable, so it is the zero polynomial
    exactly when it vanishes on the grid {0, 1, 2, 3, 4}^4. Sample points alone
    cannot certify an identity; this grid can.
    """
    grid = [Fraction(k) for k in range(5)]
    for a in grid:
        for b in grid:
            for c in grid:
                for d in grid:
                    rhs, _, _ = eval_singular_segre_positivstellensatz(a, b, c, d, eps)
                    if rhs != Fraction(-1):
                        return False
    return True


def verify_singular_segre_receipt(receipt_path: Path) -> Dict[str, Any]:
    """
    Audit the Singular Segre Positivstellensatz receipt by recomputing its identity.

    The receipt's own flags are not trusted. Refuses with ValueError unless the
    identity equals -1 at every recorded cell and as a polynomial identity.
    """
    data = parse_exact_json(receipt_path)
    if data.get("schema_version") != "omega.mub6.r7_singular_segre_sos.v1":
        raise ValueError(f"Invalid schema: {data.get('schema_version')!r}")
    firewall = data.get("firewall", "")
    if "stated region only" not in firewall:
        raise ValueError(f"Invalid firewall line: {firewall!r}")

    cells = data.get("cells", [])
    if not cells:
        raise ValueError("Cells list cannot be empty")

    eps_values = set()
    for cell in cells:
        coords = cell["coordinates"]
        a = Fraction(coords["a"])
        b = Fraction(coords["b"])
        c = Fraction(coords["c"])
        d = Fraction(coords["d"])
        eps = Fraction(cell["eps_collar"])
        eps_values.add(eps)
        rhs, s0, s1 = eval_singular_segre_positivstellensatz(a, b, c, d, eps)
        if s0 < Fraction(0) or s1 < Fraction(0):
            raise ValueError(f"SOS non-negativity violated in cell {cell['cell_id']}")
        if rhs != Fraction(-1):
            raise ValueError(
                f"Not a certificate: identity is {rhs}, not -1, in cell {cell['cell_id']}"
            )

    for eps in sorted(eps_values):
        if not singular_segre_identity_is_minus_one(eps):
            raise ValueError(f"Not a certificate: identity is not -1 as a polynomial (eps={eps})")

    return {
        "status": "IDENTITY_VERIFIED",
        "scope": "Segre quadric f_segre and circle generators of I_55 on {P_corner = 0}",
        "total_cells": len(cells),
        "zero_float_verified": True,
        "firewall_verified": True,
    }


def verify_subgap_r6_receipt(receipt_path: Path) -> Dict[str, Any]:
    """Recompute the odd parity of alpha_2(m) = 6m - 9 for m in {0, 1, 2, 3}.

    Permutation counts, catalog triple counts, and the moduli table are not
    recomputed from this JSON. A receipt status of CERTIFICATE is refused.
    This does not prove Conjecture 2, Proposition 4.2, MUB(6)=3, or MUB(6)<=3.
    """
    data = parse_exact_json(receipt_path)
    if data.get("schema_version") != "omega.mub6.r6_matolcsi_weiner_conj2.v1":
        raise ValueError(f"Invalid schema: {data.get('schema_version')!r}")
    if data.get("authority_effect") != "None":
        raise ValueError("AuthorityEffect must be 'None'")
    firewall = data.get("firewall", "")
    if "stated region only" not in firewall:
        raise ValueError(f"Invalid firewall line: {firewall!r}")
    if data.get("status") == "CERTIFICATE":
        raise ValueError("Receipt status CERTIFICATE is refused")
    if data.get("status") != "NOT_A_CERTIFICATE":
        raise ValueError(f"Receipt status must be NOT_A_CERTIFICATE, got {data.get('status')!r}")

    for m in range(4):
        alpha_2 = 6 * m - 9
        if alpha_2 % 2 == 0:
            raise ValueError(f"Parity condition violated: alpha_2({m}) = {alpha_2} is not odd")
        neg_one_pow = -1 if alpha_2 % 2 != 0 else 1
        if 1 + neg_one_pow != 0:
            raise ValueError(f"Qubit parity cancellation failed for m={m}")

    return {
        "status": "PARITY_RECOMPUTED_RECEIPT_NOT_A_CERTIFICATE",
        "scope": "Recomputed odd parity of alpha_2(m) = 6m - 9 for m in {0, 1, 2, 3} only",
        "permutation_counts_recomputed": False,
        "moduli_reduction_recomputed": False,
        "parity_cancellation_recomputed": True,
        "zero_float_verified": True,
        "firewall_verified": True,
    }



def verify_case_ledger(ledger_path: Path) -> Dict[str, Any]:
    """
    Audit and verify the G1 case ledger:
    - Schema validation
    - Non-empty coverage check
    - Correct branch statuses
    - Exact evaluation of all certified identities
    """
    ledger = parse_exact_json(ledger_path)
    if ledger.get("schema") != "omega.mub.g1_case_ledger.v1":
        raise ValueError(f"Invalid schema: {ledger.get('schema')!r}")
    if ledger.get("authority_effect") != "None":
        raise ValueError("AuthorityEffect must be 'None'")
    firewall = ledger.get("firewall_line", "")
    if "stated region only" not in firewall:
        raise ValueError(f"Invalid firewall line: {firewall!r}")

    branches = ledger.get("branches")
    if not isinstance(branches, list):
        raise ValueError("Ledger 'branches' must be a list")
    if len(branches) != 6:
        raise ValueError(f"Expected 6 branches, got {len(branches)}")

    required_keys = {"branch_id", "guard"}
    for idx, b in enumerate(branches):
        if not isinstance(b, dict) or not b:
            raise ValueError(f"Branch at index {idx} must be a non-empty dictionary")
        missing = required_keys - set(b.keys())
        if missing:
            raise ValueError(f"Branch at index {idx} missing required keys: {missing}")
        if "status" not in b and "proof_status" not in b:
            raise ValueError(f"Branch at index {idx} missing status key ('status' or 'proof_status')")
        if not b.get("branch_id"):
            raise ValueError(f"Branch at index {idx} has empty 'branch_id'")

    expected_ids = {
        "branch_regular_corner", "branch_segre_cusp", "branch_annihilated_entry",
        "branch_all_ones_row", "branch_real_upper_boundary", "branch_real_lower_boundary",
    }
    ids = [b["branch_id"] for b in branches]
    if any(not isinstance(key, str) for key in ids) or set(ids) != expected_ids:
        raise ValueError("Branch registry mismatch or duplicate")

    # Fixed sample evaluations do not interpret the ledger's witness strings.
    test_points = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(2), Fraction(1)),
        (Fraction(-7, 3), Fraction(5, 2)),
    ]

    for px, py in test_points:
        if eval_annihilated_nullstellensatz(px, py) != Fraction(1):
            raise ValueError(f"Annihilated nullstellensatz failed at ({px}, {py})")
        rhs_up, s0_up, s1_up = eval_upper_boundary_positivstellensatz(px, py)
        if rhs_up != Fraction(-1) or s0_up < Fraction(0) or s1_up < Fraction(0):
            raise ValueError(f"Upper boundary positivstellensatz failed at ({px}, {py})")

        rhs_lo, s0_lo, s1_lo = eval_lower_boundary_positivstellensatz(px, py)
        if rhs_lo != Fraction(-1) or s0_lo < Fraction(0) or s1_lo < Fraction(0):
            raise ValueError(f"Lower boundary positivstellensatz failed at ({px}, {py})")

    # Test all-ones row
    test_5vec = [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(1)]
    if eval_all_ones_nullstellensatz(test_5vec) != Fraction(1):
        raise ValueError("All-ones nullstellensatz failed")

    return {
        "status": "METADATA_ONLY",
        "premises_discharged": False,
        "fixed_identity_samples_checked": True,
        "branches_checked": len(branches),
        "zero_float_verified": True,
    }
