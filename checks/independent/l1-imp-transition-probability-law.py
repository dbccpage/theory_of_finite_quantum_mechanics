"""Independent exact checks for the transition-law hypothesis map.

AuthorityEffect: None. No repository imports. Fraction arithmetic checks witnesses
and a declared finite sample; SymPy independently checks symbolic identities.
The unrestricted claims belong to Lean, not to this finite enumeration.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from typing import Callable

import sympy as sp  # type: ignore[import-untyped]


class CheckFailure(RuntimeError):
    """A mathematical identity or expected rejection did not hold."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


@dataclass(frozen=True)
class G:
    """A Gaussian rational with strict exact admission at construction."""

    re: Q
    im: Q

    def __post_init__(self) -> None:
        if type(self.re) is not Q or type(self.im) is not Q:
            raise TypeError("Gaussian components must be Fraction objects")

    def __add__(self, other: G) -> G:
        return G(self.re + other.re, self.im + other.im)

    def __neg__(self) -> G:
        return G(-self.re, -self.im)

    def __sub__(self, other: G) -> G:
        return self + (-other)

    def __mul__(self, other: G) -> G:
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    def conjugate(self) -> G:
        return G(self.re, -self.im)

    def norm(self) -> Q:
        return self.re * self.re + self.im * self.im

    def inverse(self) -> G:
        d = self.norm()
        if d == 0:
            raise ZeroDivisionError("zero Gaussian scalar has no inverse")
        return G(self.re / d, -self.im / d)


def gaussian(re: int, im: int = 0) -> G:
    if type(re) is not int or type(im) is not int:
        raise TypeError("integer components required; bool and float are excluded")
    return G(Q(re), Q(im))


V = tuple[G, G]
ZERO, ONE, I = gaussian(0), gaussian(1), gaussian(0, 1)
E0, E1 = (ONE, ZERO), (ZERO, ONE)
REAL, PHASE = (ONE, ONE), (ONE, I)
A, B = PHASE, (ONE, gaussian(0, 2))


def norm(x: V) -> Q:
    return x[0].norm() + x[1].norm()


def inner(x: V, y: V) -> G:
    return x[0].conjugate() * y[0] + x[1].conjugate() * y[1]


def probability(x: V, y: V) -> Q:
    d = norm(x) * norm(y)
    if d == 0:
        raise ValueError("transition probability requires two nonzero states")
    return inner(x, y).norm() / d


def scaled(c: G, x: V) -> V:
    return c * x[0], c * x[1]


def ray_key(x: V) -> V:
    """Canonical projective representative; reject the zero vector."""
    anchor = x[0] if x[0] != ZERO else x[1]
    if anchor == ZERO:
        raise ValueError("the zero vector is not a ray")
    return scaled(anchor.inverse(), x)


def transform(x: V) -> V:
    if x[0].norm() == x[1].norm():
        return x[0].conjugate(), x[1].conjugate()
    return x


def stretch(x: V) -> V:
    return x[0], gaussian(2) * x[1]


def unstretch(x: V) -> V:
    return x[0], gaussian(2).inverse() * x[1]


def orthogonal_partner(x: V) -> V:
    return -x[1].conjugate(), x[0].conjugate()


def check_symbolic() -> list[str]:
    a, b, c, d = sp.symbols("a b c d", real=True)
    z, w = a + sp.I * b, c + sp.I * d
    def squared(v: sp.Expr) -> sp.Expr:
        return sp.expand(v * sp.conjugate(v))
    identities = {
        "norm_multiplicative": squared(z * w) - (a*a+b*b)*(c*c+d*d),
        "orthogonal_partner": sp.conjugate(z)*(-sp.conjugate(w))
                              + sp.conjugate(w)*sp.conjugate(z),
        "real_probe": squared(1 + z) - (1 + 2*a + a*a + b*b),
        "imaginary_probe": squared(1 - sp.I*z) - (1 + 2*b + a*a + b*b),
        "gram_calibration": sp.expand(a - (c + sp.I*d) + (c - sp.I*d) - b)
                            - (a-b-2*sp.I*d),
    }
    for label, residual in identities.items():
        require(sp.simplify(residual) == 0, label)
    # Independent matrix Born formula for the two explicit counterexamples.
    def born(u: V, v: V) -> Q:
        def column(x: V) -> sp.Matrix:
            return sp.Matrix([sp.Rational(t.re.numerator, t.re.denominator)
                              + sp.I*sp.Rational(t.im.numerator, t.im.denominator) for t in x])
        su, sv = column(u), column(v)
        projector = su * su.conjugate().T / (su.conjugate().T * su)[0]
        value = sp.simplify((sv.conjugate().T * projector * sv)[0] /
                            (sv.conjugate().T * sv)[0])
        return Q(int(sp.numer(value)), int(sp.denom(value)))
    for u, v in ((A, B), (transform(A), transform(B)), (E0, REAL),
                 (stretch(E0), stretch(REAL))):
        require(born(u, v) == probability(u, v), "Born/projector cross-check")
    return list(identities)


def check_grid() -> dict[str, int]:
    scalars = [gaussian(a, b) for a, b in product(range(-1, 2), repeat=2)]
    vectors: list[V] = [(a, b) for a, b in product(scalars, repeat=2)
                        if a != ZERO or b != ZERO]
    for x in vectors:
        tx = transform(x)
        require(transform(tx) == x, "involution")
        require(norm(tx) == norm(x), "norm")
        require(unstretch(stretch(x)) == x, "stretch inverse")
        require(transform((x[1], x[0])) == (tx[1], tx[0]), "report swap")
        require(inner(x, orthogonal_partner(x)) == ZERO, "orthogonal partner")
        for effect in (E0, E1, REAL):
            require(probability(effect, tx) == probability(effect, x),
                    "basis and real-probe statistics")
        for scalar in scalars:
            if scalar != ZERO:
                require(ray_key(transform(scaled(scalar, x))) == ray_key(tx),
                        "ray representative independence")
    orthogonal_pairs = 0
    for x, y in product(vectors, repeat=2):
        source = inner(x, y) == ZERO
        target = inner(transform(x), transform(y)) == ZERO
        require(source == target, "orthogonality iff")
        orthogonal_pairs += int(source)
    return {"vectors": len(vectors), "ordered_pairs": len(vectors)**2,
            "orthogonal_pairs": orthogonal_pairs}


def expect_error(action: Callable[[], object], error: type[Exception], label: str) -> str:
    try:
        action()
    except error:
        return label
    raise CheckFailure("expected rejection missing: " + label)


def check_boundaries() -> list[str]:
    return [
        expect_error(lambda: gaussian(True), TypeError, "boolean scalar"),
        expect_error(lambda: gaussian(0.5), TypeError, "floating scalar"),  # type: ignore[arg-type]
        expect_error(lambda: G(Q(1), 0), TypeError, "unchecked component"),  # type: ignore[arg-type]
        expect_error(lambda: ZERO.inverse(), ZeroDivisionError, "zero inverse"),
        expect_error(lambda: ray_key((ZERO, ZERO)), ValueError, "zero ray"),
        expect_error(lambda: probability((ZERO, ZERO), E0), ValueError, "zero effect"),
        expect_error(lambda: probability(E0, (ZERO, ZERO)), ValueError, "zero state"),
    ]


def check_mutants() -> list[dict[str, str]]:
    """Executable semantic mutations; all generated candidates are accounted for."""
    mutants: list[tuple[str, Callable[[], bool]]] = [
        ("drop probability denominator", lambda: inner(A, B).norm() == Q(9, 10)),
        ("drop conjugation in inner product",
         lambda: (A[0]*A[0] + A[1]*A[1]).norm()/(norm(A)**2) == 1),
        ("remove conditional branch: conjugate every vector",
         lambda: (B[0].conjugate(), B[1].conjugate()) == transform(B)),
        ("replace dynamics by identity", lambda: A == transform(A)),
        ("stretch inverse without reciprocal", lambda: stretch(stretch(REAL)) == REAL),
    ]
    outcomes: list[dict[str, str]] = []
    for label, check in mutants:
        survives = check()
        outcomes.append({"mutation": label, "outcome": "survived" if survives else "killed"})
    require(all(row["outcome"] == "killed" for row in outcomes), "a semantic mutant survived")
    return outcomes


def main() -> None:
    require(norm(A) == 2 and norm(B) == 5, "witness norms")
    require(inner(A, B) == gaussian(3), "original inner product")
    require(inner(transform(A), transform(B)) == gaussian(-1), "transformed inner product")
    require(probability(A, B) == Q(9, 10), "original witness probability")
    require(probability(transform(A), transform(B)) == Q(1, 10), "transformed witness probability")
    require(probability(E0, REAL) == Q(1, 2), "original stretch probability")
    require(probability(stretch(E0), stretch(REAL)) == Q(1, 5), "stretched probability")
    require(probability(PHASE, A) == 1 and probability(PHASE, transform(A)) == 0,
            "imaginary probe distinguishes the countermodel")
    report: dict[str, object] = {
        "status": "PASS",
        "scope": "symbolic identities, exact witnesses, finite grid; no general claim from sampling",
        "witness_norms": [str(norm(A)), str(norm(B))],
        "witness_inner_products": ["3", "-1"],
        "countermodel_probabilities": ["9/10", "1/10"],
        "stretch_probabilities": ["1/2", "1/5"],
        "imaginary_probe_probabilities": ["1", "0"],
        "symbolic_identities": check_symbolic(),
        "grid": check_grid(),
        "boundary_rejections": check_boundaries(),
        "mutations": check_mutants(),
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
