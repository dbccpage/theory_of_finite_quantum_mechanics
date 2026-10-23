"""Independent check for FSP-U1-WILSON-ACTION.

AuthorityEffect: None.

Run: python -I -X utf8 checks/independent/fsp-u1-wilson-action.py

This script imports no repository code. It rebuilds periodic hypercubic lattices,
U(1) link fields and local gauge transformations from scratch and recomputes the
Wilson action S = beta * sum_p (1 - Re U_p) with exact arithmetic:

* unit complex numbers with rational coordinates, z(t) = ((1 - t^2) + 2 t i) / (1 + t^2),
  held as pairs of fractions.Fraction (no floating point anywhere in parts 1-4);
* SymPy exact trigonometry for the angle form U = exp(i A) in part 5.

It exits 0 when every check passes and 1 otherwise, and prints what it checked.
"""

from __future__ import annotations

import itertools
import random
import sys
from fractions import Fraction

import sympy as sp

FAILURES: list[str] = []
COUNTS: dict[str, int] = {}


def check(name: str, ok: bool) -> None:
    COUNTS[name] = COUNTS.get(name, 0) + 1
    if not ok:
        FAILURES.append(name)


# ---------------------------------------------------------------- exact unit complex numbers

ONE = (Fraction(1), Fraction(0))


def cmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def conj(z):
    return (z[0], -z[1])


def norm_sq(z):
    return z[0] * z[0] + z[1] * z[1]


def unit_from_t(t: Fraction):
    d = 1 + t * t
    return ((1 - t * t) / d, (2 * t) / d)


def random_unit(rng: random.Random):
    if rng.random() < 0.1:
        return rng.choice([ONE, (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(1)),
                           (Fraction(0), Fraction(-1))])
    return unit_from_t(Fraction(rng.randint(-40, 40), rng.randint(1, 40)))


# ---------------------------------------------------------------- periodic hypercubic lattice


def sites(d: int, L: int):
    return list(itertools.product(range(L), repeat=d))


def shift(x, mu: int, L: int, step: int = 1):
    y = list(x)
    y[mu] = (y[mu] + step) % L
    return tuple(y)


def plaquettes(d: int, L: int):
    """Closed paths x -> x+mu -> x+mu+nu -> x+nu -> x for every site and mu < nu."""
    out = []
    for x in sites(d, L):
        for mu in range(d):
            for nu in range(mu + 1, d):
                a = shift(x, mu, L)
                b = shift(a, nu, L)
                c = shift(x, nu, L)
                out.append([x, a, b, c, x])
    return out


class LinkField:
    """Forward links U(x, x+mu) stored once; U(x+mu, x) = conj U(x, x+mu)."""

    def __init__(self, d: int, L: int, forward: dict):
        self.d, self.L, self.forward = d, L, forward

    def __call__(self, a, b):
        for mu in range(self.d):
            if shift(a, mu, self.L) == b and (a, mu) in self.forward:
                return self.forward[(a, mu)]
        for mu in range(self.d):
            if shift(b, mu, self.L) == a and (b, mu) in self.forward:
                return conj(self.forward[(b, mu)])
        raise KeyError((a, b))


def random_field(d: int, L: int, rng: random.Random) -> LinkField:
    return LinkField(d, L, {(x, mu): random_unit(rng) for x in sites(d, L) for mu in range(d)})


def gauge(U: LinkField, g: dict) -> LinkField:
    fwd = {(x, mu): cmul(cmul(g[x], U.forward[(x, mu)]), conj(g[shift(x, mu, U.L)]))
           for (x, mu) in U.forward}
    return LinkField(U.d, U.L, fwd)


def holonomy(U, path):
    h = ONE
    for a, b in zip(path, path[1:]):
        h = cmul(h, U(a, b))
    return h


def wilson(U, plaqs, beta: Fraction) -> Fraction:
    return beta * sum((1 - holonomy(U, p)[0] for p in plaqs), Fraction(0))


# ---------------------------------------------------------------- part 1: gauge invariance and nonnegativity


def part1(rng: random.Random) -> None:
    for d, L, trials in ((2, 3, 40), (2, 4, 20), (3, 2, 20), (3, 3, 8), (4, 2, 8)):
        plaqs = plaquettes(d, L)
        check("plaquette count = L^d * d(d-1)/2", len(plaqs) == L ** d * d * (d - 1) // 2)
        for _ in range(trials):
            U = random_field(d, L, rng)
            check("links have modulus 1", all(norm_sq(z) == 1 for z in U.forward.values()))
            g = {x: random_unit(rng) for x in sites(d, L)}
            Ug = gauge(U, g)
            check("gauged links have modulus 1", all(norm_sq(z) == 1 for z in Ug.forward.values()))
            for beta in (Fraction(0), Fraction(1), Fraction(7, 2)):
                s, sg = wilson(U, plaqs, beta), wilson(Ug, plaqs, beta)
                check("S(gauged) == S exactly", s == sg)
                check("S >= 0 for beta >= 0", s >= 0)
            for p in plaqs:
                check("each plaquette holonomy is gauge invariant", holonomy(U, p) == holonomy(Ug, p))
                check("each plaquette term 1 - Re U_p >= 0", 1 - holonomy(U, p)[0] >= 0)


# ---------------------------------------------------------------- part 2: open-path covariance, composition, reversal


def part2(rng: random.Random) -> None:
    d, L = 3, 3
    for _ in range(20):
        U = random_field(d, L, rng)
        g = {x: random_unit(rng) for x in sites(d, L)}
        h = {x: random_unit(rng) for x in sites(d, L)}
        Ug = gauge(U, g)
        # random open walk along links
        x = rng.choice(sites(d, L))
        path = [x]
        for _ in range(rng.randint(0, 9)):
            mu = rng.randrange(d)
            path.append(shift(path[-1], mu, L, rng.choice((1, -1))))
        lhs = holonomy(Ug, path)
        rhs = cmul(cmul(g[path[0]], holonomy(U, path)), conj(g[path[-1]]))
        check("open-path holonomy: H(gU) = g(start) H(U) conj g(end)", lhs == rhs)
        # composition: gauge by h then by g equals gauge by g*h
        gh = {x: cmul(g[x], h[x]) for x in g}
        check("gauge(g, gauge(h, U)) == gauge(g*h, U)",
              gauge(gauge(U, h), g).forward == gauge(U, gh).forward)
        check("trivial gauge is the identity", gauge(U, {x: ONE for x in g}).forward == U.forward)
        # reversal convention survives gauging
        a = rng.choice(sites(d, L))
        mu = rng.randrange(d)
        b = shift(a, mu, L)
        check("U(b, a) == conj U(a, b) after gauging", Ug(b, a) == conj(Ug(a, b)))


# ---------------------------------------------------------------- part 3: zero exactly on flat fields (beta > 0)


def part3(rng: random.Random) -> None:
    for d, L in ((2, 3), (3, 2), (4, 2)):
        plaqs = plaquettes(d, L)
        for _ in range(10):
            g = {x: random_unit(rng) for x in sites(d, L)}
            pure = LinkField(d, L, {(x, mu): cmul(g[x], conj(g[shift(x, mu, L)]))
                                    for x in sites(d, L) for mu in range(d)})
            check("pure-gauge field has S = 0", wilson(pure, plaqs, Fraction(5, 3)) == 0)
            check("pure-gauge field has every U_p = 1", all(holonomy(pure, p) == ONE for p in plaqs))
            U = random_field(d, L, rng)
            s = wilson(U, plaqs, Fraction(5, 3))
            flat = all(holonomy(U, p) == ONE for p in plaqs)
            check("S = 0 iff every U_p = 1 (beta > 0)", (s == 0) == flat)


# ---------------------------------------------------------------- part 4: necessity of beta >= 0 and negative controls


def part4(rng: random.Random) -> None:
    # One vertex, one self-link plaquette, link phase -1, beta = -1: S = -1 * (1 - (-1)) = -2.
    minus_one = (Fraction(-1), Fraction(0))
    s = Fraction(-1) * (1 - cmul(minus_one, ONE)[0])
    check("one-plaquette witness: S = -2 at beta = -1", s == -2)
    # On a lattice, a negative beta makes S negative for some field.
    d, L = 2, 3
    plaqs = plaquettes(d, L)
    U = random_field(d, L, rng)
    while all(holonomy(U, p) == ONE for p in plaqs):
        U = random_field(d, L, rng)
    check("negative beta gives S < 0 on a non-flat field", wilson(U, plaqs, Fraction(-1)) < 0)
    # Mutation controls: a change that is not a gauge transformation must be detected.
    killed = 0
    for _ in range(20):
        U = random_field(d, L, rng)
        key = rng.choice(list(U.forward))
        phase = unit_from_t(Fraction(rng.randint(1, 30), rng.randint(1, 30)))
        if phase == ONE:
            continue
        mutated = LinkField(d, L, dict(U.forward))
        mutated.forward[key] = cmul(phase, U.forward[key])
        # A single-link rotation changes the two plaquettes through that link (d = 2).
        if any(holonomy(U, p) != holonomy(mutated, p) for p in plaqs):
            killed += 1
    check("single-link non-gauge mutations change some plaquette (20 of 20)", killed == 20)
    # Mutating the gauge rule (forgetting the conjugate at the far end) breaks invariance.
    U = random_field(d, L, rng)
    g = {x: random_unit(rng) for x in sites(d, L)}
    while all(z == ONE for z in g.values()):
        g = {x: random_unit(rng) for x in sites(d, L)}
    wrong = LinkField(d, L, {(x, mu): cmul(g[x], U.forward[(x, mu)]) for (x, mu) in U.forward})
    check("wrong gauge rule g(a) U(a,b) changes some plaquette",
          any(holonomy(U, p) != holonomy(wrong, p) for p in plaqs))


# ---------------------------------------------------------------- part 5: angle form with SymPy


def part5() -> None:
    d, L = 2, 2
    plaqs = plaquettes(d, L)
    rng = random.Random(20261023)
    for _ in range(6):
        A = {(x, mu): sp.Rational(rng.randint(-11, 11), 6) * sp.pi
             for x in sites(d, L) for mu in range(d)}
        theta = {x: sp.Rational(rng.randint(-11, 11), 4) * sp.pi for x in sites(d, L)}

        def angle(Af, a, b):
            for mu in range(d):
                if shift(a, mu, L) == b and (a, mu) in Af:
                    return Af[(a, mu)]
            for mu in range(d):
                if shift(b, mu, L) == a and (b, mu) in Af:
                    return -Af[(b, mu)]
            raise KeyError((a, b))

        Ag = {(x, mu): A[(x, mu)] + theta[x] - theta[shift(x, mu, L)] for (x, mu) in A}
        beta = sp.Rational(9, 4)

        def action(Af):
            total = 0
            for p in plaqs:
                phase = sum(angle(Af, a, b) for a, b in zip(p, p[1:]))
                prod = sp.Integer(1)
                for a, b in zip(p, p[1:]):
                    prod = prod * sp.exp(sp.I * angle(Af, a, b))
                check("Re prod exp(iA) == cos(sum A) (SymPy exact)",
                      sp.simplify(sp.re(sp.expand_complex(prod)) - sp.cos(phase)) == 0)
                total += 1 - sp.cos(phase)
            return beta * total

        s, sg = action(A), action(Ag)
        check("angle form: S(A + d theta) == S(A) (SymPy exact)", sp.simplify(s - sg) == 0)
        check("angle form: S >= 0 for beta >= 0", bool(sp.nsimplify(s) >= 0))


def main() -> int:
    rng = random.Random(1196)
    part1(rng)
    part2(rng)
    part3(rng)
    part4(rng)
    part5()
    for name in sorted(COUNTS):
        print(f"{COUNTS[name]:6d}  {name}")
    print(f"checks={sum(COUNTS.values())} distinct={len(COUNTS)} failures={len(FAILURES)}")
    if FAILURES:
        for name in sorted(set(FAILURES)):
            print("FAILED:", name)
        return 1
    print("OK: exact U(1) Wilson-action gauge invariance, nonnegativity for beta >= 0, "
          "flatness criterion and beta >= 0 necessity witness recomputed independently.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
