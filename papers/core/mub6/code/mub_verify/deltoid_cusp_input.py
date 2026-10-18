"""Exact audit and rational encoding of the matrix in the 2026-09-23 prompt.

AuthorityEffect: None.
stated region only; mints no authority

This input is NOT accepted as a cusp Hadamard matrix.  The polynomial sources
encode its literal overlap equations; an input rejection is not an emptiness
certificate for those equations.  No catalog matrix is silently substituted.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


# Entry (a, b) denotes a + i*sqrt(3)*b. All arithmetic is exact.
Pair = tuple[Q, Q]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Q]
ZERO: Pair = (Q(0), Q(0))
ONE: Pair = (Q(1), Q(0))
ROOTS: tuple[Pair, ...] = (
    ONE, (Q(1, 2), Q(1, 2)), (Q(-1, 2), Q(1, 2)),
    (Q(-1), Q(0)), (Q(-1, 2), Q(-1, 2)), (Q(1, 2), Q(-1, 2)),
)
D_EXPONENTS = (
    (0, 0, 0, 0, 0, 0),
    (0, 0, 2, 4, 5, 1),
    (0, 2, 0, 5, 1, 4),
    (0, 4, 5, 0, 2, 1),
    (0, 5, 1, 2, 0, 4),
    (0, 1, 4, 1, 4, 0),
)
F_EXPONENTS = tuple(tuple((j * k) % 6 for k in range(6)) for j in range(6))
VARIABLES = tuple(name for k in range(2, 7) for name in (f"x{k}", f"t{k}"))
CONSTANT = (0,) * 10


def add(a: Pair, b: Pair) -> Pair:
    return a[0] + b[0], a[1] + b[1]


def mul(a: Pair, b: Pair) -> Pair:
    return a[0] * b[0] - 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def conj(a: Pair) -> Pair:
    return a[0], -a[1]


def norm_squared(a: Pair) -> Q:
    return a[0] ** 2 + 3 * a[1] ** 2


def matrix(exponents: tuple[tuple[int, ...], ...]) -> tuple[tuple[Pair, ...], ...]:
    return tuple(tuple(ROOTS[e] for e in row) for row in exponents)


def inner(a: tuple[Pair, ...], b: tuple[Pair, ...]) -> Pair:
    if len(a) != len(b):
        raise ValueError("inner product dimension mismatch")
    result = ZERO
    for av, bv in zip(a, b):
        result = add(result, mul(conj(av), bv))
    return result


def gram(rows: tuple[tuple[Pair, ...], ...]) -> tuple[tuple[Pair, ...], ...]:
    return tuple(tuple(inner(a, b) for b in rows) for a in rows)


def poly_add(*polynomials: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for p in polynomials:
        for m, c in p.items():
            out[m] = out.get(m, Q(0)) + c
    return {m: c for m, c in out.items() if c}


def scale(p: Polynomial, c: Q) -> Polynomial:
    return {m: c * a for m, a in p.items() if c * a}


def poly_mul(p: Polynomial, q: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for m, a in p.items():
        for n, b in q.items():
            key = tuple(x + y for x, y in zip(m, n))
            out[key] = out.get(key, Q(0)) + a * b
    return {m: c for m, c in out.items() if c}


def variable(i: int) -> Polynomial:
    return {tuple(int(k == i) for k in range(10)): Q(1)}


def overlap_polynomial(row: tuple[Pair, ...]) -> Polynomial:
    """|sum conj(row[k]) (x_k + i sqrt(3) t_k)|^2 - 6.

    x_1=1, t_1=0.  u=z/sqrt(6), so the required RHS in z is 6.
    """
    real: Polynomial = {CONSTANT: row[0][0]}
    imag: Polynomial = {CONSTANT: -row[0][1]}
    for k, (a, b) in enumerate(row[1:]):
        x, t = variable(2 * k), variable(2 * k + 1)
        real = poly_add(real, scale(x, a), scale(t, 3 * b))
        imag = poly_add(imag, scale(t, a), scale(x, -b))
    return poly_add(poly_mul(real, real), scale(poly_mul(imag, imag), Q(3)), {CONSTANT: Q(-6)})


def sources() -> tuple[tuple[str, Polynomial], ...]:
    result: list[tuple[str, Polynomial]] = []
    for k in range(5):
        x, t = variable(2 * k), variable(2 * k + 1)
        result.append((f"unit_{k + 2}", poly_add(poly_mul(x, x), scale(poly_mul(t, t), Q(3)), {CONSTANT: Q(-1)})))
    for name, exp in (("fourier", F_EXPONENTS), ("literal_D", D_EXPONENTS)):
        result.extend((f"{name}_{j}", overlap_polynomial(row)) for j, row in enumerate(matrix(exp)))
    return tuple(result)


def evaluate(p: Polynomial, values: tuple[Q | int, ...]) -> Q:
    if len(values) != 10 or any(type(v) not in (int, Q) for v in values):
        raise TypeError("provide ten exact int or Fraction coordinates")
    out = Q(0)
    for monomial, coefficient in p.items():
        term = coefficient
        for value, exponent in zip(values, monomial):
            term *= value ** exponent
        out += term
    return out


def encode_q(q: Q) -> list[int]:
    return [q.numerator, q.denominator]


def encode_pair(p: Pair) -> list[list[int]]:
    return [encode_q(p[0]), encode_q(p[1])]


def audit_receipt() -> dict:
    d, f = matrix(D_EXPONENTS), matrix(F_EXPONENTS)
    dg, fg = gram(d), gram(f)
    return {
        "schema": "mub6.literal-cusp-input.v1",
        "AuthorityEffect": "None",
        "firewall": "stated region only; mints no authority",
        "status": "REJECTED_AS_HADAMARD_INPUT",
        "literal_system_feasibility": "NOT_DECIDED_BY_THIS_INPUT_AUDIT",
        "coefficient_pair_meaning": "a + i*sqrt(3)*b; each rational is [numerator, denominator]",
        "D_exponents": D_EXPONENTS,
        "F_exponents": F_EXPONENTS,
        "D_row_gram": [[encode_pair(v) for v in row] for row in dg],
        "F_row_gram": [[encode_pair(v) for v in row] for row in fg],
        "D_all_entries_unit": all(norm_squared(e) == 1 for row in d for e in row),
        "D_is_hadamard": all(dg[j][k] == ((Q(6), Q(0)) if j == k else ZERO) for j in range(6) for k in range(6)),
        "F_is_hadamard": all(fg[j][k] == ((Q(6), Q(0)) if j == k else ZERO) for j in range(6) for k in range(6)),
        "first_row_cross_overlap_squared_normalized": encode_q(norm_squared(inner(f[0], d[0])) / 36),
        "required_cross_overlap_squared_normalized": [1, 6],
        "variable_order": VARIABLES,
        "real_coordinate_change": "y_k = sqrt(3)*t_k; x_1=1, t_1=0; u=(x+i*sqrt(3)*t)/sqrt(6)",
        "overlap_rhs_after_dephasing": 6,
        "sources": [
            {"id": name, "terms": [{"powers": m, "coefficient": encode_q(c)} for m, c in sorted(p.items())]}
            for name, p in sources()
        ],
        "duplicate_sources": [["fourier_0", "literal_D_0"]],
        "emptiness_certificate": None,
    }


def source_sha256() -> str:
    payload = json.dumps(audit_receipt()["sources"], sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def decode_polynomial(terms: object) -> Polynomial:
    if type(terms) is not list:
        raise ValueError("polynomial terms must be a list")
    out: Polynomial = {}
    for term in terms:
        if type(term) is not dict or set(term) != {"powers", "coefficient"}:
            raise ValueError("invalid polynomial term")
        powers, coefficient = term["powers"], term["coefficient"]
        if type(powers) is not list or len(powers) != 10 or any(type(e) is not int or e < 0 for e in powers):
            raise ValueError("invalid monomial")
        if type(coefficient) is not list or len(coefficient) != 2 or any(type(c) is not int for c in coefficient):
            raise ValueError("coefficient must be two exact integers")
        num, den = coefficient
        if den <= 0 or num == 0:
            raise ValueError("coefficient must be nonzero with positive denominator")
        value = Q(num, den)
        if encode_q(value) != coefficient:
            raise ValueError("coefficient must be reduced")
        key = tuple(powers)
        if key in out:
            raise ValueError("duplicate monomial")
        out[key] = value
    return out


def verify_certificate(cert: object) -> None:
    """Replay a pure identity against the computed, fixed literal sources.

    Metadata does not establish membership: all polynomial products are expanded
    and their exact coefficients summed. A failed check raises ValueError.
    """
    if type(cert) is not dict or cert.get("schema") != "mub6.literal-cusp-nullstellensatz.v1":
        raise ValueError("unsupported certificate schema")
    if cert.get("variable_order") != list(VARIABLES):
        raise ValueError("wrong variable order")
    if cert.get("target") != [-1, 1] or any(type(c) is not int for c in cert["target"]):
        raise ValueError("wrong identity target")
    if cert.get("source_sha256") != source_sha256():
        raise ValueError("certificate is not bound to the literal sources")
    multipliers = cert.get("multipliers")
    fixed_sources = sources()
    if type(multipliers) is not list or len(multipliers) != len(fixed_sources):
        raise ValueError("require exactly seventeen multipliers")
    total: Polynomial = {}
    for entry, (name, source) in zip(multipliers, fixed_sources):
        if type(entry) is not dict or set(entry) != {"id", "terms"} or entry["id"] != name:
            raise ValueError("source identifier or multiplier order mismatch")
        total = poly_add(total, poly_mul(decode_polynomial(entry["terms"]), source))
    if total != {CONSTANT: Q(-1)}:
        raise ValueError("polynomial identity does not equal -1")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-certificate", type=Path)
    args = parser.parse_args()
    if args.verify_certificate:
        verify_certificate(json.loads(args.verify_certificate.read_text(encoding="utf-8")))
        print("PASS: exact identity -1 for the fixed literal overlap system; no cusp identification.")
        return
    payload = json.dumps(audit_receipt(), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
