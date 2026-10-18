"""Reconstruct the literal-system certificate using exact rational arithmetic.

AuthorityEffect: None.
stated region only; mints no authority

Dependency: python-flint==0.9.0 (fmpq_mat rational Dixon linear solver).
The persisted pivot selections are untrusted hints, not rank evidence. Acceptance
requires an exact rational solve and replay of the full polynomial identity.
The supplied D matrix is not Hadamard; no corrected matrix is substituted.
Run from any directory with --output pointing to a desired receipt path.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

import flint
from flint import fmpq_mat

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from mub_verify.deltoid_cusp_input import (
    CONSTANT, VARIABLES, audit_receipt, poly_add, poly_mul, scale, sources,
)


def exponents(n: int, degree: int):
    if n == 1:
        yield (degree,)
    else:
        for k in range(degree + 1):
            for rest in exponents(n - 1, degree - k):
                yield (k, *rest)


def encode_polynomial(p):
    return [
        {"powers": list(m), "coefficient": [c.numerator, c.denominator]}
        for m, c in sorted(p.items()) if c
    ]


def reconstruct(hints_path: Path) -> dict:
    if flint.__version__ != "0.9.0":
        raise RuntimeError("reconstruction requires python-flint==0.9.0")
    hints = json.loads(hints_path.read_text(encoding="utf-8"))
    if hints["schema"] != "mub6.literal-cusp-rational-pivot-hints.v1" or hints["degree"] != 4:
        raise ValueError("unexpected pivot hint schema or degree")
    canonical = sources()
    monomials = [m for degree in range(4, -1, -1) for m in exponents(10, degree)]
    columns = {m: j for j, m in enumerate(monomials)}
    rows, labels = [], []
    for i, (_, polynomial) in enumerate(canonical):
        for degree in range(3):
            for multiplier_monomial in exponents(10, degree):
                row = [Q(0)] * len(monomials)
                for monomial, coefficient in polynomial.items():
                    combined = tuple(a + b for a, b in zip(multiplier_monomial, monomial))
                    row[columns[combined]] = coefficient
                rows.append(row)
                labels.append((i, multiplier_monomial))
    selected_rows, selected_columns = hints["rows"], hints["columns"]
    for indices, length in ((selected_rows, len(rows)), (selected_columns, len(monomials))):
        if (not indices or len(set(indices)) != len(indices)
                or any(type(i) is not int or i < 0 or i >= length for i in indices)):
            raise ValueError("invalid pivot indices")
    if len(selected_rows) != len(selected_columns):
        raise ValueError("pivot subsystem must be square")
    matrix = fmpq_mat([[str(rows[i][j]) for i in selected_rows] for j in selected_columns])
    target = fmpq_mat([[int(monomials[j] == CONSTANT)] for j in selected_columns])
    coefficients = matrix.solve(target, algorithm="dixon")
    if matrix * coefficients != target:
        raise ArithmeticError("rational linear-system replay failed")
    multipliers = [{} for _ in canonical]
    for k, row_index in enumerate(selected_rows):
        coefficient = -Q(str(coefficients[k, 0]))
        source_index, monomial = labels[row_index]
        if coefficient:
            multipliers[source_index][monomial] = coefficient
    total = poly_add(*(poly_mul(a, p) for a, (_, p) in zip(multipliers, canonical)))
    if total != {CONSTANT: Q(-1)}:
        raise ArithmeticError("complete exact rational polynomial identity replay failed")
    source_data = audit_receipt()["sources"]
    digest = hashlib.sha256(json.dumps(source_data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "schema": "mub6.literal-cusp-nullstellensatz.v1",
        "AuthorityEffect": "None",
        "firewall": "stated region only; mints no authority",
        "scope": "Literal prompt equations only. Supplied D is not a Hadamard matrix; no cusp-family claim.",
        "variable_order": list(VARIABLES),
        "target": [-1, 1],
        "source_sha256": digest,
        "multipliers": [
            {"id": name, "terms": encode_polynomial(p)}
            for (name, _), p in zip(canonical, multipliers)
        ],
        "solver": {
            "method": "exact rational degree-4 Macaulay linear solve with untrusted pivot hints",
            "arithmetic": "Q only; fmpq_mat.solve algorithm=dixon; complete Fraction polynomial replay",
            "python_flint_version": flint.__version__,
            "macaulay_rows": len(rows),
            "macaulay_columns": len(monomials),
            "selected_square_subsystem_size": len(selected_rows),
            "max_multiplier_degree": 2,
            "exact_expanded_replay": "sum a_j*f_j + 1 is the zero polynomial",
            "sum_of_squares_terms": [],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hints", type=Path, default=Path(__file__).with_name("rational_pivot_hints.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = reconstruct(args.hints)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS_EXACT_RATIONAL_RECONSTRUCTION", "output": str(args.output)}))


if __name__ == "__main__":
    main()
