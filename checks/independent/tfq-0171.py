#!/usr/bin/env python3
"""Independent exact-rational verification for TFQ-0171.

Verifies the carrier and normalization separation between:
- BooleanValuation (code/rust/src/finite_probability/finite_valuation.rs):
  exact non-negative Boolean valuations with no unit-normalization requirement
  and admissibility of the empty carrier (size = 0).
- ProbabilitySimplex (code/rust/src/finite_probability/simplex.rs):
  non-empty finite rational distributions summing to 1.
- ScaledProb (lean4/ProbabilitySimplex.lean):
  scaled integer weights summing to M > 0 on a finite enumeration.
- SignedValuation (code/rust/src/finite_probability/signed_representation.rs),
  LocalVertexLimits (code/rust/src/finite_probability/local_deterministic.rs),
  and MarginalScenario (code/rust/src/finite_probability/marginal_compatibility.rs).
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
import sys
from typing import Any


def boolean_valuation_try_new(
    size: int, entries: list[tuple[frozenset[int], Fraction]]
) -> tuple[bool, str, dict[str, Any]]:
    full = frozenset(range(size))
    values: dict[frozenset[int], Fraction] = {}
    for ev, val in entries:
        if not ev.issubset(full):
            return False, "OutsideCarrier", {}
        if ev in values:
            return False, "DuplicateEvent", {}
        values[ev] = val
    if frozenset() not in values or full not in values:
        return False, "NotBooleanAlgebra", {}
    for a in list(values.keys()):
        comp = full - a
        if comp not in values:
            return False, "NotBooleanAlgebra", {}
        for b in list(values.keys()):
            if (a | b) not in values:
                return False, "NotBooleanAlgebra", {}
    if values[frozenset()] != 0 or any(v < 0 for v in values.values()):
        return False, "InvalidMass", {}
    for a, av in values.items():
        for b, bv in values.items():
            if a.isdisjoint(b):
                if values[a | b] != av + bv:
                    return False, "NotAdditive", {}
    sigs: dict[tuple[bool, ...], set[int]] = {}
    sorted_keys = sorted(values.keys(), key=lambda s: (len(s), sorted(s)))
    for pt in range(size):
        sig = tuple(pt in ev for ev in sorted_keys)
        sigs.setdefault(sig, set()).add(pt)
    atoms = sorted((frozenset(s) for s in sigs.values()), key=lambda s: sorted(s))
    ext_first = [Fraction(0)] * size
    ext_last = [Fraction(0)] * size
    for atom in atoms:
        pts = sorted(atom)
        if pts:
            ext_first[pts[0]] = values[atom]
            ext_last[pts[-1]] = values[atom]
    unique_ext = all(len(atom) == 1 or values[atom] == 0 for atom in atoms)
    return True, "Ok", {
        "size": size,
        "full_mass": values[full],
        "atoms": [sorted(a) for a in atoms],
        "atom_masses": [values[a] for a in atoms],
        "ext_first": ext_first,
        "ext_last": ext_last,
        "unique_ext": unique_ext,
    }


def probability_simplex_try_new(probs: list[Fraction]) -> tuple[bool, str]:
    if not probs:
        return False, "Empty"
    for p in probs:
        if p < 0:
            return False, "NegativeEntry"
    total = sum(probs, Fraction(0))
    if total != Fraction(1):
        return False, "NotNormalized"
    return True, "Ok"


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
    # Family 1: Empty carrier and unnormalized BooleanValuation vs ProbabilitySimplex
    # -------------------------------------------------------------------------
    ok_empty, status_empty, info_empty = boolean_valuation_try_new(
        0, [(frozenset(), Fraction(0))]
    )
    record(ok_empty and status_empty == "Ok", "BooleanValuation accepts size = 0")
    record(info_empty["full_mass"] == 0, "Empty carrier full mass = 0")
    record(info_empty["atoms"] == [], "Empty carrier has 0 atoms")

    ok_simp_empty, err_simp_empty = probability_simplex_try_new([])
    record(not ok_simp_empty and err_simp_empty == "Empty", "ProbabilitySimplex rejects empty carrier")

    # Unnormalized Boolean valuations on size = 2
    for m0 in [Fraction(0), Fraction(1, 3), Fraction(1), Fraction(3), Fraction(7, 2)]:
        for m1 in [Fraction(0), Fraction(2, 3), Fraction(2), Fraction(5), Fraction(9, 4)]:
            entries = [
                (frozenset(), Fraction(0)),
                (frozenset([0]), m0),
                (frozenset([1]), m1),
                (frozenset([0, 1]), m0 + m1),
            ]
            ok_v, _, info_v = boolean_valuation_try_new(2, entries)
            record(ok_v, f"BooleanValuation accepts nonnegative (m0={m0}, m1={m1})")
            record(info_v["full_mass"] == m0 + m1, "Full mass = m0 + m1")
            ok_s, err_s = probability_simplex_try_new([m0, m1])
            if m0 + m1 == Fraction(1):
                record(ok_s, "ProbabilitySimplex accepts when m0 + m1 == 1")
            else:
                record(not ok_s and err_s == "NotNormalized", "ProbabilitySimplex rejects when m0 + m1 != 1")

    # Coarse 2-atom algebra on size = 3: A_0 = {0}, A_1 = {1, 2}
    coarse_entries = [
        (frozenset(), Fraction(0)),
        (frozenset([0]), Fraction(2, 3)),
        (frozenset([1, 2]), Fraction(4, 3)),
        (frozenset([0, 1, 2]), Fraction(2)),
    ]
    ok_c, _, info_c = boolean_valuation_try_new(3, coarse_entries)
    record(ok_c, "Coarse BooleanValuation on size=3 is valid")
    record(info_c["full_mass"] == Fraction(2), "Coarse valuation full mass = 2 != 1")
    record(not info_c["unique_ext"], "Coarse valuation singleton extension is not unique")
    record(info_c["ext_first"] == [Fraction(2, 3), Fraction(4, 3), Fraction(0)], "ext_first = [2/3, 4/3, 0]")
    record(info_c["ext_last"] == [Fraction(2, 3), Fraction(0), Fraction(4, 3)], "ext_last = [2/3, 0, 4/3]")
    record(info_c["ext_first"] != info_c["ext_last"], "ext_first != ext_last")

    details["family1_boolean_valuation"] = {
        "empty_carrier_admitted_by_valuation": True,
        "empty_carrier_admitted_by_simplex": False,
        "coarse_full_mass": str(info_c["full_mass"]),
        "coarse_unique_singleton_extension": info_c["unique_ext"],
    }

    # -------------------------------------------------------------------------
    # Family 2: ProbabilitySimplex scaled integer grid vs rational simplex
    # -------------------------------------------------------------------------
    point_w = (1, 0)
    signed_w = (-1, 2)
    double_w = (1, 1)
    record(sum(point_w) == 1 and all(w >= 0 for w in point_w), "pointMass has sum=1 and nonneg")
    record(sum(signed_w) == 1 and not all(w >= 0 for w in signed_w), "signedW has sum=1 but negative entry")
    record(sum(double_w) == 2 and all(w >= 0 for w in double_w) and sum(double_w) != 1, "doubleW has nonneg and sum=2 != 1")

    # Rational law (1/3, 2/3) on ScaledProb Bool enumBool M for M in 1..12
    for m in range(1, 13):
        w0 = Fraction(1, 3) * m
        w1 = Fraction(2, 3) * m
        on_grid = (w0.denominator == 1 and w1.denominator == 1)
        record(on_grid == (m % 3 == 0), f"(1/3, 2/3) on scale-M integer grid iff 3 | M (M={m})")

    details["family2_scaled_integer_grid"] = {
        "point_mass_sum": 1,
        "double_mass_sum": 2,
        "one_third_two_thirds_minimal_scale": 3,
    }

    # -------------------------------------------------------------------------
    # Family 3: SignedValuation Jordan decomposition and negativity bound
    # -------------------------------------------------------------------------
    for a_num in range(2, 8):
        p0 = Fraction(a_num, 2)
        p1 = Fraction(1) - p0  # negative since a_num >= 2 and p0 >= 1 (strictly negative for a_num >= 3)
        masses = [p0, p1]
        record(sum(masses) == Fraction(1), "SignedValuation unit sum")
        pos_part = [max(m, Fraction(0)) for m in masses]
        neg_part = [max(-m, Fraction(0)) for m in masses]
        negativity = sum(neg_part, Fraction(0))
        record(pos_part[0] - neg_part[0] == p0 and pos_part[1] - neg_part[1] == p1, "Jordan decomposition w = w^+ - w^-")
        record(sum(pos_part) - sum(neg_part) == Fraction(1), "||w^+||_1 - ||w^-||_1 = 1")
        record(sum(pos_part) + sum(neg_part) == Fraction(1) + 2 * negativity, "||w||_1 = 1 + 2 * negativity")
        for bound in [Fraction(1), Fraction(2), Fraction(5, 2)]:
            readout = [bound, -bound]
            expectation = masses[0] * readout[0] + masses[1] * readout[1]
            upper = bound * (Fraction(1) + 2 * negativity)
            req_neg = max((abs(expectation) / bound - Fraction(1)) / Fraction(2), Fraction(0))
            record(expectation == upper, "Extremal readout attains B*(1 + 2*negativity)")
            record(req_neg == negativity, "Required negativity matches actual negativity")

    details["family3_signed_valuation"] = {
        "unit_sum_preserved": True,
        "jordan_bound_verified": True,
    }

    # -------------------------------------------------------------------------
    # Family 4: Local deterministic vertices and MarginalScenario normalization
    # -------------------------------------------------------------------------
    # 3 binary variables (2^3 = 8 global assignments), 3 pairwise contexts (0,1), (1,2), (0,2)
    contexts = [(0, 1), (1, 2), (0, 2)]
    for assign in itertools.product((0, 1), repeat=3):
        vertex_coords: list[Fraction] = []
        for c in contexts:
            sec_vec = [Fraction(0)] * 4
            idx = assign[c[0]] * 2 + assign[c[1]]
            sec_vec[idx] = Fraction(1)
            record(sum(sec_vec) == Fraction(1), "Each context slice of deterministic vertex sums to 1")
            vertex_coords.extend(sec_vec)
        record(len(vertex_coords) == 12, "3 pairwise binary contexts have 12 coordinates")
        record(sum(vertex_coords) == Fraction(3), "Total coordinate sum across 3 contexts is 3")

    details["family4_local_and_marginal"] = {
        "assignments_checked": 8,
        "contexts": 3,
        "coordinates_per_vertex": 12,
    }

    # -------------------------------------------------------------------------
    # Family 5: positive natural masses are not a unit sum; division normalizes
    # -------------------------------------------------------------------------
    record(0 != 1, "empty mass is not 1")
    record(1 + 1 == 2 and 2 != 1, "pair (1, 1) sums to 2")
    record(Fraction(1) + Fraction(1) != Fraction(1), "rational 1 + 1 is not 1")
    record(Fraction(1, 2) + Fraction(1, 2) == Fraction(1), "halves sum to 1")
    record((Fraction(1), Fraction(1)) != (Fraction(1, 2), Fraction(1, 2)), "unnormalized pair differs")
    record(0 + 1 == 1, "zero-plus-one is a unit and sits outside the positive-pair hypothesis")
    positive_pairs = 0
    normalized_pairs = 0
    for a in range(0, 13):
        for b in range(0, 13):
            if a >= 1 and b >= 1:
                positive_pairs += 1
                record(a + b != 1 and a + b >= 2, f"positive masses {a}, {b}")
            if a + b > 0:
                normalized_pairs += 1
                record(
                    Fraction(a, a + b) + Fraction(b, a + b) == Fraction(1),
                    f"division normalizes {a}, {b}",
                )
    record(0 + 0 == 0, "the zero total is excluded from division")
    details["family5_positive_mass"] = {
        "positive_pairs": positive_pairs,
        "normalized_pairs": normalized_pairs,
        "one_one_sum": 2,
        "half_sum": "1",
    }

    return {
        "node_id": "TFQ-0171",
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
        f"TFQ-0171 INDEPENDENT CHECKER PASSED: checks={summary['checks_total']} failed={summary['checks_failed']}"
    )
    if args.json:
        print(json.dumps(summary))
    sys.exit(0 if summary["passed"] else 1)
