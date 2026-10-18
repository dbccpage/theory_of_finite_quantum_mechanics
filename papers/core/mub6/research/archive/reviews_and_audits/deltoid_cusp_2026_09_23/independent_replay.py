"""Independently reconstruct and replay the fixed literal overlap certificate.

Run with Python and SymPy installed. This script does not import the production
encoder or verifier. All symbolic arithmetic has exact rational coefficients.

AuthorityEffect: None.
stated region only; mints no authority

The supplied matrix is not Hadamard. This replay does not identify a cusp matrix.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


# Independent transcription of the explicit matrix in the attached prompt.
D_EXPONENTS = (
    (0, 0, 0, 0, 0, 0),
    (0, 0, 2, 4, 5, 1),
    (0, 2, 0, 5, 1, 4),
    (0, 4, 5, 0, 2, 1),
    (0, 5, 1, 2, 0, 4),
    (0, 1, 4, 1, 4, 0),
)
VARIABLE_NAMES = tuple(name for k in range(2, 7) for name in (f"x{k}", f"t{k}"))


def independently_reconstruct():
    variables = sp.symbols(" ".join(VARIABLE_NAMES), real=True)
    omega = (1 + sp.I * sp.sqrt(3)) / 2
    z = (sp.Integer(1),) + tuple(
        variables[2 * k] + sp.I * sp.sqrt(3) * variables[2 * k + 1]
        for k in range(5)
    )
    sources = [
        (f"unit_{k + 1}", sp.Poly(z[k] * sp.conjugate(z[k]) - 1, *variables, domain=sp.QQ))
        for k in range(1, 6)
    ]
    fourier = tuple(tuple(j * k for k in range(6)) for j in range(6))
    for name, rows in (("fourier", fourier), ("literal_D", D_EXPONENTS)):
        for j, row in enumerate(rows):
            overlap = sp.expand(sum(sp.conjugate(omega ** row[k]) * z[k] for k in range(6)))
            polynomial = sp.Poly(
                sp.expand(overlap * sp.conjugate(overlap) - 6), *variables, domain=sp.QQ
            )
            sources.append((f"{name}_{j}", polynomial))
    return variables, sources


def encode_sources(sources):
    return [
        {
            "id": name,
            "terms": [
                {"powers": list(powers), "coefficient": [int(coefficient.p), int(coefficient.q)]}
                for powers, coefficient in sorted(polynomial.as_dict().items())
            ],
        }
        for name, polynomial in sources
    ]


def decode_multiplier(terms, variables):
    if type(terms) is not list:
        raise ValueError("multiplier terms must be a list")
    coefficients = {}
    for term in terms:
        if type(term) is not dict or set(term) != {"powers", "coefficient"}:
            raise ValueError("invalid multiplier term")
        powers, coefficient = term["powers"], term["coefficient"]
        if (
            type(powers) is not list
            or len(powers) != len(variables)
            or any(type(exponent) is not int or exponent < 0 for exponent in powers)
        ):
            raise ValueError("invalid multiplier monomial")
        if (
            type(coefficient) is not list
            or len(coefficient) != 2
            or any(type(value) is not int for value in coefficient)
        ):
            raise ValueError("multiplier coefficient requires two exact integers")
        numerator, denominator = coefficient
        if numerator == 0 or denominator <= 0:
            raise ValueError("multiplier coefficient requires nonzero numerator and positive denominator")
        rational = sp.Rational(numerator, denominator)
        if [int(rational.p), int(rational.q)] != coefficient:
            raise ValueError("multiplier coefficient must be reduced")
        key = tuple(powers)
        if key in coefficients:
            raise ValueError("duplicate multiplier monomial")
        coefficients[key] = rational
    return sp.Poly.from_dict(coefficients, variables, domain=sp.QQ)


def main() -> None:
    directory = Path(__file__).resolve().parent
    # Missing artifacts are errors; no partial replay is reported as success.
    audit = json.loads((directory / "input_audit.json").read_text(encoding="utf-8"))
    certificate = json.loads((directory / "literal_certificate.json").read_text(encoding="utf-8"))
    variables, sources = independently_reconstruct()
    encoded_sources = encode_sources(sources)
    if type(audit) is not dict or audit.get("sources") != encoded_sources:
        raise ValueError("archived sources differ from independent complex symbolic reconstruction")
    if audit.get("variable_order") != list(VARIABLE_NAMES):
        raise ValueError("archived source variable order differs")
    payload = json.dumps(encoded_sources, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    if type(certificate) is not dict or certificate.get("schema") != "mub6.literal-cusp-nullstellensatz.v1":
        raise ValueError("unsupported certificate schema")
    if certificate.get("source_sha256") != digest:
        raise ValueError("certificate is not bound to the independently reconstructed sources")
    if certificate.get("variable_order") != list(VARIABLE_NAMES):
        raise ValueError("certificate variable order differs")
    target = certificate.get("target")
    if type(target) is not list or target != [-1, 1] or any(type(value) is not int for value in target):
        raise ValueError("certificate target must be the exact rational -1")
    multipliers = certificate.get("multipliers")
    if type(multipliers) is not list or len(multipliers) != len(sources):
        raise ValueError("certificate must supply all seventeen multipliers")
    total = sp.Poly(0, *variables, domain=sp.QQ)
    for entry, (name, source) in zip(multipliers, sources):
        if type(entry) is not dict or set(entry) != {"id", "terms"} or entry["id"] != name:
            raise ValueError("multiplier source identifier or ordering differs")
        total += decode_multiplier(entry["terms"], variables) * source
    if total.as_dict() != {(0,) * len(variables): sp.Integer(-1)}:
        raise ValueError("independent polynomial expansion does not equal -1")
    print("PASS: all 17 sources match independent complex symbolic reconstruction.")
    print("PASS: independent exact multiplier identity equals -1 for the literal system; no cusp identification.")


if __name__ == "__main__":
    main()
