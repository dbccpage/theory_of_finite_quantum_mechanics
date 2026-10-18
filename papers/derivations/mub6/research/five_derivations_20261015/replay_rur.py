"""Check a supplied RUR, isolate its real roots, and enclose common-ray pairs.

The output separates soundness and injectivity of this parametrization from
completeness for the original ideal. An independent quotient-dimension upper
bound is still required for the latter.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import flint
import sympy as sp
from flint import arb, arb_poly, ctx, fmpq, fmpq_poly

SCRIPTS = Path(__file__).resolve().parents[1] / "szollosi_vectors" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from param import load_param


def exact_dyadic(value: arb) -> fmpq:
    mantissa, exponent = value.man_exp()
    return (
        fmpq(int(mantissa) * 2 ** int(exponent))
        if exponent >= 0
        else fmpq(int(mantissa), 2 ** (-int(exponent)))
    )


def exact_bounds(value: arb) -> tuple[fmpq, fmpq]:
    midpoint, radius = exact_dyadic(value.mid()), exact_dyadic(value.rad())
    return midpoint - radius, midpoint + radius


def check_parametrization(system: Path, names, linear, elim, denominator, numerators) -> dict:
    variables = sp.symbols([name for name in names if name != "A"])
    body = system.read_text().split("\n", 2)[2].strip().rstrip(",")
    equations = [
        sp.Poly(sp.sympify(e.replace("^", "**")), *variables)
        for e in body.replace("\n", "").split(",")
    ]
    h, d = fmpq_poly(elim), fmpq_poly(denominator)
    if h.gcd(h.derivative()).degree() != 0 or h.gcd(d).degree() != 0:
        raise ValueError("Non-squarefree eliminant or non-invertible denominator")
    ys = [-fmpq_poly(n) / int(c) for n, c in numerators]
    if len(variables) != len(ys) or not equations or h.degree() < 1:
        raise ValueError("Parametrization dimension or nonempty-system mismatch")
    degree = max(p.total_degree() for p in equations)
    cache = {}
    for equation in equations:
        result = fmpq_poly([])
        for exponents, coefficient in equation.terms():
            if exponents not in cache:
                monomial = (d ** (degree - sum(exponents))) % h
                for y, power in zip(ys, exponents):
                    monomial = (monomial * y**power) % h
                cache[exponents] = monomial
            result += fmpq(int(coefficient.p), int(coefficient.q)) * cache[exponents]
        if result % h != 0:
            raise ValueError("RUR substitution fails an original equation")
    if len(linear) != len(ys) + 1 or linear[-1] == 0:
        raise ValueError("Missing separating linear form")
    separation = sum(int(c) * y for c, y in zip(linear[:-1], ys))
    separation += int(linear[-1]) * fmpq_poly([0, 1]) * d
    if separation % h != 0:
        raise ValueError("Separating linear form is inconsistent")
    return {
        "equations_checked": len(equations),
        "degree": elim.degree(),
        "squarefree": True,
        "denominator_invertible": True,
        "substitution": True,
        "separating_form": True,
        "completeness": "requires independent quotient-dimension upper bound",
    }


def sturm_counts(factors: list, gp: str) -> list[int]:
    commands = "\n".join(
        "print(polsturm(Polrev([" + ",".join(map(str, f.coeffs())) + "])));" for f, _ in factors
    )
    result = subprocess.run(
        [gp, "-q", "-f"], input=commands + "\nquit;\n", text=True, capture_output=True, check=True
    )
    counts = [int(line) for line in result.stdout.splitlines() if line.strip()]
    if len(counts) != len(factors):
        raise ValueError("Incomplete PARI Sturm output: " + result.stderr[-500:])
    return counts


def isolate(factors, counts, approximations: Path, denominator, numerators) -> list:
    hints = [
        ast.literal_eval(line.replace("~", ""))
        for line in approximations.read_text().splitlines()
        if line.strip()
    ]
    if len(hints) != len(factors):
        raise ValueError("Approximation factor count mismatch")
    ctx.prec = 24000
    d = arb_poly([arb(c) for c in denominator.coeffs()])
    nums = [(arb_poly([arb(c) for c in n.coeffs()]), int(scale)) for n, scale in numerators]
    roots = []
    for index, ((factor, multiplicity), count, hint) in enumerate(zip(factors, counts, hints)):
        k, old_count, guesses = hint
        if k != index or old_count != count or len(guesses) != count or multiplicity != 1:
            raise ValueError("Root count mismatch")
        f = arb_poly([arb(c) for c in factor.coeffs()])
        df = f.derivative()
        for guess in guesses:
            point = arb(guess)
            for _ in range(9):
                point = arb(exact_dyadic((point - f(point) / df(point)).mid()))
            midpoint = exact_dyadic(point.mid())
            midpoint = fmpq(int(midpoint.p * 2**3064 // midpoint.q), 2**3064)
            low, high = midpoint - fmpq(1, 2**3000), midpoint + fmpq(1, 2**3000)
            if factor(low) * factor(high) >= 0:
                raise ValueError("Root interval lacks an exact sign change")
            interval = arb(low).union(arb(high))
            if d(interval).contains(0):
                raise ValueError("Coordinate denominator is not separated from zero")
            values = [-n(interval) / (scale * d(interval)) for n, scale in nums]
            ctx.prec = 300
            boxes = [exact_bounds(+v) for v in values]
            ctx.prec = 24000
            roots.append(
                {
                    "factor": index,
                    "interval": [str(low), str(high)],
                    "coordinates": [[str(a), str(b)] for a, b in boxes],
                }
            )
    intervals = sorted((fmpq(r["interval"][0]), fmpq(r["interval"][1])) for r in roots)
    if any(a[1] >= b[0] for a, b in zip(intervals, intervals[1:])):
        raise ValueError("Root intervals are not pairwise disjoint")
    return roots


def check_pairs(roots: list) -> dict:
    ctx.prec = 300
    groups = {}
    for root in roots:
        values = [arb(fmpq(low)).union(arb(fmpq(high))) for low, high in root["coordinates"]]
        label = "fixed"
        if len(values) == 12:
            low, high = map(fmpq, root["coordinates"][10])
            if low <= 0 <= high:
                raise ValueError("The two sample parameter branches are not separated")
            label = "aw_positive" if low > 0 else "aw_negative"
        elif len(values) != 10:
            raise ValueError("Unsupported common-ray coordinate layout")
        groups.setdefault(label, []).append(values)
    output = {}
    for label, values in groups.items():
        orthogonal = unbiased = pairs = 0
        separation = None
        for index, p in enumerate(values):
            for q in values[index + 1 :]:
                pairs += 1
                real = 1 + sum(p[j] * q[j] + p[j + 5] * q[j + 5] for j in range(5))
                imag = sum(p[j] * q[j + 5] - p[j + 5] * q[j] for j in range(5))
                residual = real * real + imag * imag - 6
                orthogonal += int(real.contains(0) and imag.contains(0))
                unbiased += int(residual.contains(0))
                low, high = exact_bounds(residual)
                gap = low if low > 0 else -high
                separation = gap if separation is None else min(separation, gap)
        output[label] = {
            "represented_rays": len(values),
            "pairs_checked": pairs,
            "orthogonal_candidates": orthogonal,
            "unbiased_candidates": unbiased,
            "minimum_pair_residual_separation": str(separation),
        }
    return output


def check_jacobians(system: Path, roots: list, factors: list, denominator, numerators) -> dict:
    """Check nonsingularity in exact number fields for factors with real roots."""
    header, _, body = system.read_text().split("\n", 2)
    variables = sp.symbols(header.strip(), seq=True)
    equations = [
        sp.sympify(e.replace("^", "**"))
        for e in body.replace("\n", "").strip().rstrip(",").split(",")
    ]
    if len(equations) != len(variables):
        raise ValueError("Expected a square common-ray system")
    jacobian = sp.Matrix(equations).jacobian(variables)
    parameter = sp.Symbol("t")

    def expression(poly):
        return sum(
            sp.Rational(int(c.p), int(c.q)) * parameter**k for k, c in enumerate(poly.coeffs())
        )

    records = []
    for index in sorted(set(root["factor"] for root in roots)):
        factor = fmpq_poly(factors[index][0])
        _, inverse, _ = fmpq_poly(denominator).xgcd(factor)
        coordinates = [(-fmpq_poly(n) * inverse / int(c)) % factor for n, c in numerators]
        substitution = {v: expression(y) for v, y in zip(variables, coordinates)}
        matrix = jacobian.subs(substitution, simultaneous=True).applyfunc(sp.expand)
        modulus = sp.Poly(expression(factor), parameter)
        determinant = sp.Poly(matrix.det(method="domain-ge"), parameter).rem(modulus)
        if sp.gcd(determinant, modulus).degree() != 0:
            raise ValueError(f"Jacobian singular on eliminant factor {index}")
        records.append(
            {"factor": index, "gcd_degree": 0, "determinant_remainder": str(determinant.as_expr())}
        )
    return {
        "method": "exact determinant modulo each real-root factor",
        "nonsingular_roots": len(roots),
        "factors": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("system", "param", "approx", "output"):
        parser.add_argument("--" + key, type=Path, required=True)
    parser.add_argument("--gp", required=True)
    parser.add_argument("--check-jacobians", action="store_true")
    args = parser.parse_args()
    names, linear, elim, denominator, numerators, _ = load_param(str(args.param))
    checks = check_parametrization(args.system, names, linear, elim, denominator, numerators)
    print(json.dumps(checks), flush=True)
    _, factors = elim.factor()
    factors = sorted(factors, key=lambda item: item[0].degree())
    counts = sturm_counts(factors, args.gp)
    roots = isolate(factors, counts, args.approx, denominator, numerators)
    pairs = check_pairs(roots)
    jacobians = (
        check_jacobians(args.system, roots, factors, denominator, numerators)
        if args.check_jacobians
        else {"status": "not requested"}
    )
    output = {
        "status": "PASS_FOR_REPRESENTED_SOLUTIONS",
        "rur": checks,
        "sturm_counts": counts,
        "real_solutions": len(roots),
        "groups": pairs,
        "jacobians": jacobians,
        "sources": {
            k: hashlib.sha256(getattr(args, k).read_bytes()).hexdigest()
            for k in ("system", "param", "approx")
        },
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_flint_version": flint.__version__,
        "parser_sha256": {
            name: hashlib.sha256((SCRIPTS / name).read_bytes()).hexdigest()
            for name in ("param.py", "parse.py")
        },
        "roots": roots,
    }
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"real_solutions": len(roots), "groups": pairs}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
