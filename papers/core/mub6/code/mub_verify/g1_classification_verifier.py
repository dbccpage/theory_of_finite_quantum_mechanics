"""
Exact Rational G1 Master Classification & Orbit Exhaustiveness Verifier.

This module validates:
1. Structural integrity and schema compliance of research/g1_foundation/classification_manifest.json.
2. The 5 canonical certified moduli components of the 6x6 complex Hadamard catalog:
   - Fourier-Diță (affine orbit, F_6^(4))
   - Szöllősi Deltoid (1-parameter curve, B_6(θ), singular Segre cusps P_corner = 0)
   - Karlsson Volume (3-parameter manifold, K_6^(3), regular corner P_corner != 0)
   - Chernyavsky-Tao Confluence (S_6 boundary confluence)
   - Haagerup Isolated (H_6 isolated circulant)
3. Elimination of empty subvarieties via Nullstellensatz and Positivstellensatz certificates.
4. Algebraic corner determinant routing:
   P_corner(a, b, c, d) = ad - bc - a + b + c - d = (a-1)(d-1) - (b-1)(c-1).
5. Strict zero-float enforcement via recursive assert_no_float and exact Fraction arithmetic.

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


def corner_determinant(a: Fraction, b: Fraction, c: Fraction, d: Fraction) -> Fraction:
    """
    Evaluate the 3x3 corner determinant identity:
      P_corner(a, b, c, d) = ad - bc - a + b + c - d
    Equivalent to:
      (a - 1) * (d - 1) - (b - 1) * (c - 1)
    """
    return (a - Fraction(1)) * (d - Fraction(1)) - (b - Fraction(1)) * (c - Fraction(1))


def classify_corner(a: Fraction, b: Fraction, c: Fraction, d: Fraction) -> str:
    """
    Classify a dephased corner point into either the singular Segre cusp or regular corner chart.
    """
    det = corner_determinant(a, b, c, d)
    if det == Fraction(0):
        return "szollosi_deltoid"
    else:
        return "karlsson_volume"


def eval_annihilated_nullstellensatz(x: Fraction, y: Fraction) -> Fraction:
    """
    Evaluate the Nullstellensatz identity for the annihilated entry branch:
      (-1) * (x^2 + y^2 - 1) + x * (x) + y * (y)
    This identically evaluates to 1 in Q[x, y].
    """
    p_circle = x * x + y * y - Fraction(1)
    return Fraction(-1) * p_circle + x * x + y * y


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
    return Fraction(1, 6) * row_orth - sum(subs)


def eval_upper_boundary_positivstellensatz(
    x: Fraction, y: Fraction
) -> Tuple[Fraction, Fraction, Fraction]:
    """
    Evaluate Stengle Positivstellensatz SOS certificate for x >= 2:
      Identity: -1 = (-1/3) * f + sigma_0 + sigma_1 * g
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
    Evaluate Stengle Positivstellensatz SOS certificate for x <= -2:
      Identity: -1 = (-1/3) * f + sigma_0 + sigma_1 * g
    """
    f = x * x + y * y - Fraction(1)
    g = Fraction(-2) - x
    sigma_0 = Fraction(1, 3) * (x + Fraction(2)) ** 2 + Fraction(1, 3) * (y**2)
    sigma_1 = Fraction(4, 3)
    rhs = Fraction(-1, 3) * f + sigma_0 + sigma_1 * g
    return rhs, sigma_0, sigma_1


def verify_classification_manifest(filepath: Path) -> Dict[str, Any]:
    """
    Validate research/g1_foundation/classification_manifest.json against all Target C3 criteria.
    """
    data = parse_exact_json(filepath)

    if data.get("schema") != "omega.mub.g1_classification_manifest.v1":
        raise ValueError(f"Invalid schema: {data.get('schema')!r}")

    # 1. Authority and Firewall Checks
    if data.get("authority_effect") != "None":
        raise ValueError("AuthorityEffect must be strictly 'None'")
    firewall = data.get("firewall_line", "")
    if "stated region only" not in firewall:
        raise ValueError(f"Invalid or missing firewall line: {firewall!r}")

    # 2. Moduli Components Validation
    components = data.get("moduli_components", [])
    if len(components) != 5:
        raise ValueError(f"Expected exactly 5 moduli components, got {len(components)}")

    expected_comp_ids = {
        "fourier_dita",
        "szollosi_deltoid",
        "karlsson_volume",
        "tao_confluence",
        "haagerup_isolated",
    }
    actual_comp_ids = {c["component_id"] for c in components}
    if actual_comp_ids != expected_comp_ids:
        raise ValueError(f"Moduli component mismatch: {actual_comp_ids} != {expected_comp_ids}")

    for c in components:
        if c["component_id"] == "szollosi_deltoid":
            if c["chart_routing"] != "branch_segre_cusp":
                raise ValueError("Szollosi deltoid must route to branch_segre_cusp")
        else:
            if c["chart_routing"] != "branch_regular_corner":
                raise ValueError(f"{c['component_id']} must route to branch_regular_corner")

    # 3. Eliminated Subvarieties Validation
    subvarieties = data.get("eliminated_subvarieties", [])
    if len(subvarieties) != 4:
        raise ValueError(f"Expected exactly 4 eliminated subvarieties, got {len(subvarieties)}")

    for sub in subvarieties:
        if sub.get("status") != "DISCHARGED_EMPTY":
            raise ValueError(f"Subvariety {sub.get('subvariety_id')} status is not DISCHARGED_EMPTY")

    # 4. Theorems Validation
    theorems = data.get("theorems", [])
    if len(theorems) < 4:
        raise ValueError(f"Expected at least 4 master theorems, got {len(theorems)}")

    axiom_allowlist = {"propext", "Classical.choice", "Quot.sound"}
    for thm in theorems:
        axioms = thm.get("axioms", [])
        if "sorryAx" in axioms:
            raise ValueError(f"Theorem {thm.get('name')} contains uncertified axiom 'sorryAx'")
        if not isinstance(axioms, list) or not set(axioms).issubset(axiom_allowlist):
            raise ValueError(
                f"Theorem {thm.get('name')} contains disallowed axioms: {set(axioms) - axiom_allowlist}"
            )

    # 5. Verification Summary
    summary = data.get("verification_summary", {})
    if summary.get("unconditional_grand_synthesis_proved") or summary.get("unconditional_no_fourth_basis_proved"):
        raise ValueError("No audited discharge term is bound to this manifest")
    if summary.get("sorry_count") != 0 or summary.get("admit_count") != 0:
        raise ValueError("sorry_count and admit_count must be 0")

    return {
        "status": "METADATA_ONLY",
        "premises_discharged": False,
        "components_checked": len(components),
        "subvarieties_eliminated": len(subvarieties),
        "theorems_checked": len(theorems),
        "zero_float_verified": True,
    }
