"""Replay exact identities used in the five MUB(6) derivations.

AuthorityEffect: None. This verifies the specified identities and the explicit
three-basis construction, not a classification of arbitrary MUB triples.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


def circulant(row: list[sp.Expr]) -> sp.Matrix:
    return sp.Matrix(3, 3, lambda i, j: row[(j - i) % 3])


def phase_adjoint(matrix: sp.Matrix, phases: tuple) -> sp.Matrix:
    return matrix.conjugate().T.xreplace({sp.conjugate(t): 1 / t for t in phases})


def source_matrix(phases: tuple) -> sp.Matrix:
    a = circulant(list(phases[:3]))
    b = circulant(list(phases[3:]))
    return a.row_join(b).col_join(phase_adjoint(b, phases).row_join(-phase_adjoint(a, phases)))


def require_zero(expressions, label: str) -> None:
    for index, expression in enumerate(expressions):
        if sp.cancel(sp.expand(expression)) != 0:
            raise ValueError(f"{label}: nonzero residual {index}")


def family_transport() -> dict:
    phases = sp.symbols("a b c d e f", nonzero=True)
    a, b, c, d, e, f = phases
    raw = source_matrix(phases)
    left = sp.diag(1 / a, 1 / a, 1 / a, d, d, d)
    right = sp.diag(1, 1, 1, a / d, a / d, a / d)
    aa = circulant([sp.Integer(1), b / a, c / a])
    bb = circulant([sp.Integer(1), e / d, f / d])
    target = aa.row_join(bb).col_join(
        phase_adjoint(bb, phases).row_join(-phase_adjoint(aa, phases))
    )
    require_zero(left * raw * right - target, "family transport")
    return {"matrix_entries_checked": 36, "identity": "L H R = S(b/a,c/b,e/d,f/e)"}


def special_system_binding() -> dict:
    """Bind the saved ten equations to the actual matrix and dephased rays."""
    path = (
        Path(__file__).resolve().parents[1] / "szollosi_vectors" / "special_1_m1_1_i" / "special.ms"
    )
    header, characteristic, body = path.read_text().split("\n", 2)
    if characteristic.strip() != "0":
        raise ValueError("Expected a characteristic-zero system")
    variables = sp.symbols(header.strip(), real=True)
    if len(variables) != 10:
        raise ValueError("Expected ten common-ray coordinates")
    a, b = variables[:5], variables[5:]
    z = sp.Matrix([1] + [a[j] + sp.I * b[j] for j in range(5)])
    aa = circulant([sp.Integer(1), sp.Integer(1), sp.Integer(-1)])
    bb = circulant([sp.Integer(1), sp.Integer(1), sp.I])
    matrix = aa.row_join(bb).col_join(bb.conjugate().T.row_join(-aa.conjugate().T))
    require_zero(matrix.conjugate().T * matrix - 6 * sp.eye(6), "sample Hadamard")
    overlaps = matrix.conjugate().T * z
    residuals = [sp.expand(w * sp.conjugate(w) - 6) for w in overlaps]
    circles = [a[j] ** 2 + b[j] ** 2 - 1 for j in range(5)]
    saved = [
        sp.sympify(e.replace("^", "**"), locals={str(v): v for v in variables})
        for e in body.replace("\n", "").strip().rstrip(",").split(",")
    ]
    expected = residuals[:5] + circles
    if len(saved) != len(expected):
        raise ValueError("Saved system equation count mismatch")
    require_zero([s - e for s, e in zip(saved, expected)], "sample system binding")
    require_zero([sum(residuals) - 6 * sum(circles)], "sixth equation redundancy")
    return {
        "system_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "equations_bound": 10,
        "sixth_overlap_redundancy": True,
        "parameter": ["1", "-1", "1", "i"],
    }


def monomial_terms(matrix: sp.Matrix, phases: tuple, positive: tuple) -> list:
    terms = []
    for column in range(6):
        term = sp.cancel(
            sp.prod(matrix[row, column] ** (1 if row in positive else -1) for row in range(6))
        )
        powers = term.as_powers_dict()
        exponent = tuple(int(powers.get(t, 0)) for t in phases)
        coefficient = sp.cancel(term / sp.prod(t**k for t, k in zip(phases, exponent)))
        if coefficient not in (1, -1):
            raise ValueError("Unexpected signed Laurent coefficient")
        terms.append((int(coefficient), exponent))
    return terms


def verify_pairing(terms: list, permutation: tuple) -> None:
    if sorted(permutation) != [3, 4, 5]:
        raise ValueError("Pairing must use each right column exactly once")
    for column, other in enumerate(permutation):
        if terms[column][0] != -terms[other][0] or terms[column][1] != terms[other][1]:
            raise ValueError("Laurent monomials do not cancel")


def laurent_pairings() -> list[dict]:
    phases = sp.symbols("a b c d e f", nonzero=True)
    raw = source_matrix(phases)
    witnesses = []
    for positive in itertools.combinations(range(6), 3):
        terms = monomial_terms(raw, phases, positive)
        valid = []
        for permutation in itertools.permutations((3, 4, 5)):
            try:
                verify_pairing(terms, permutation)
            except ValueError:
                continue
            valid.append(permutation)
        if not valid:
            raise ValueError(f"No cancelling pairing for {positive}")
        for exponent in (1, 3):
            require_zero(
                [
                    sum(
                        sp.prod(
                            raw[row, column] ** (exponent if row in positive else -exponent)
                            for row in range(6)
                        )
                        for column in range(6)
                    )
                ],
                "Laurent identity",
            )
        witnesses.append(
            {
                "positive_rows": list(positive),
                "right_columns": list(valid[0]),
                "left_exponents": [list(t[1]) for t in terms[:3]],
            }
        )
    return witnesses


def deltoid_discriminants() -> dict:
    s, t, z = sp.symbols("s t z", real=True)
    alpha = s + sp.I * t
    cubic = z**3 - alpha * z**2 + sp.conjugate(alpha) * z - 1
    delta = sp.expand(sp.discriminant(cubic, z))
    expected = (s * s + t * t) ** 2 + 18 * (s * s + t * t) - 27 - 8 * s * (s * s - 3 * t * t)
    require_zero([delta - expected], "phase discriminant")
    reflected = sp.expand(delta.subs({s: -s, t: -t}, simultaneous=True))
    difference = sp.factor(delta - reflected)
    require_zero([difference + 16 * s * (s * s - 3 * t * t)], "boundary intersection")
    return {
        "delta_plus": str(delta),
        "delta_minus": str(reflected),
        "boundary_difference": str(difference),
        "boundary_radius_squared_equation": "rho^2 + 18*rho - 27 = 0",
        "positive_boundary_radius_squared": "-9 + 6*sqrt(3)",
    }


def three_bases() -> list[sp.Matrix]:
    i = sp.I
    omega = (-1 + i * sp.sqrt(3)) / 2
    qubits = [
        sp.eye(2),
        sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2),
        sp.Matrix([[1, 1], [i, -i]]) / sp.sqrt(2),
    ]
    fourier = sp.Matrix(3, 3, lambda j, k: sp.expand(omega ** ((j * k) % 3))) / sp.sqrt(3)
    qutrits = [sp.eye(3), fourier, sp.diag(1, omega, omega) * fourier]
    return [sp.kronecker_product(q, r) for q, r in zip(qubits, qutrits)]


def verify_three_bases(bases: list[sp.Matrix]) -> dict:
    for basis in bases:
        require_zero(basis.conjugate().T * basis - sp.eye(6), "unitary basis")
    for left, right in itertools.combinations(bases, 2):
        gram = left.conjugate().T * right
        require_zero([v * sp.conjugate(v) - sp.Rational(1, 6) for v in gram], "unbiased bases")
    return {
        "bases": 3,
        "dimension": 6,
        "gram_entries_checked": 108,
        "cross_overlap_entries_checked": 108,
        "squared_overlap": "1/6",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = {
        "family_transport": family_transport(),
        "special_system_binding": special_system_binding(),
        "laurent_pairings": laurent_pairings(),
        "phase_domain": deltoid_discriminants(),
        "three_basis_construction": verify_three_bases(three_bases()),
    }
    receipt = {
        "status": "PASS",
        "scope": "specified symbolic identities and three explicit bases",
        "sympy_version": sp.__version__,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "results": results,
    }
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "balanced_masks": len(results["laurent_pairings"]),
                "scope": receipt["scope"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
