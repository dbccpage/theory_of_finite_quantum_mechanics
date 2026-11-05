"""Terminating proposals; their outputs acquire evidence only through checking."""

from __future__ import annotations

from math import isqrt

from state_effect_readout.model import add, identity, matmul

from .checker import admit_problem
from .model import (
    ZERO,
    Exhausted,
    Fuel,
    G,
    I,
    Q,
    apply,
    basis_unit,
    digest,
    inv,
    inverse,
    matrix,
    projection,
    scale,
    subtract,
    vector,
    wire,
)


def factor(n: int, fuel: Fuel) -> dict[int, int]:
    if type(n) is not int or n < 1:
        raise ValueError("factorization requires a positive integer")
    out = {}
    p = 2
    while p * p <= n:
        fuel.spend()
        while n % p == 0:
            fuel.spend()
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def norm_class(r: Q, fuel: Fuel) -> tuple[int, ...]:
    if r <= 0:
        raise ValueError("norm class requires a positive rational")
    parities = {}
    for part in (r.numerator, r.denominator):
        for p, exponent in factor(part, fuel).items():
            parities[p] = (parities.get(p, 0) + exponent) % 2
    return tuple(sorted(p for p, odd in parities.items() if p % 4 == 3 and odd))


def integer_norm(n: int, fuel: Fuel) -> G:
    for a in range(isqrt(n) + 1):
        fuel.spend()
        b = isqrt(n - a * a)
        if a * a + b * b == n:
            return G.of(a, b)
    raise ValueError("integer is not a two-squares norm")


def _reachability(task, carrier, fuel):
    f = vector(task["source"], carrier.dimension)
    g = vector(task["target"], carrier.dimension)
    ratio = carrier.norm(f) / carrier.norm(g)
    classes = norm_class(ratio, fuel)
    if classes:
        prime = classes[0]
        # Independent checking recomputes primality and this valuation.
        numerator, denominator = factor(ratio.numerator, fuel), factor(ratio.denominator, fuel)
        return "unitary_impossible", {
            "prime": prime,
            "valuation": numerator.get(prime, 0) - denominator.get(prime, 0),
        }
    a = integer_norm(ratio.numerator, fuel) * inv(integer_norm(ratio.denominator, fuel))
    v = tuple(a * x for x in g)
    u = identity(carrier.dimension)
    if v != f:
        w = tuple(x + -y for x, y in zip(f, v, strict=True))
        beta = carrier.inner(w, f)
        covector = tuple(x.conjugate() for x in apply(carrier.gram, w))
        correction = tuple(tuple(x * y * inv(beta) for y in covector) for x in w)
        u = subtract(u, correction)
    return "unitary_reachable", {"matrix": u, "scalar": a}


def propose(problem: object, operation_limit: int = 100_000) -> dict:
    task, carrier = admit_problem(problem)
    fuel = Fuel(operation_limit)
    try:
        if task["kind"] == "reachability":
            claim, evidence = _reachability(task, carrier, fuel)
        elif task["kind"] == "luders":
            f, g = (
                vector(task["source"], carrier.dimension),
                vector(task["target"], carrier.dimension),
            )
            p = projection(carrier, g)
            probability = carrier.probability(f, g)
            claim = "positive_postselection" if probability > 0 else "zero_branch"
            evidence = {"projection": p, "probability": probability, "branch_vector": apply(p, f)}
        elif task["kind"] == "preserver":
            # The identity branch is a proposal only; checking decides whether it works.
            frame, images = matrix(task["frame"]), matrix(task["images"])
            columns = tuple(zip(*frame, strict=True))
            image_columns = tuple(zip(*images, strict=True))
            m = matmul(image_columns, inverse(columns))
            f, target = frame[0], images[0]
            claim = "global_semisimilarity"
            evidence = {
                "matrix": m,
                "branch": "identity",
                "multiplier": carrier.norm(target) / carrier.norm(f),
            }
        else:
            n = carrier.dimension
            table = tuple(matrix(a, n) for a in task["derivation"])
            s = scale(ZERO, identity(n))
            for j in range(n):
                fuel.spend()
                s = add(s, matmul(table[j * n], basis_unit(n, 0, j)))
            s = scale(G.of(Q(1, 2)), subtract(s, carrier.adjoint(s)))
            claim = "inner_dagger_derivation"
            evidence = {"implementer": s, "hermitian_generator": scale(I, s)}
        certificate = {
            "schema": "wdp.preserver.certificate.v1",
            "problem_sha256": digest(task),
            "claim": claim,
            "evidence": wire(evidence),
        }
        return {"status": "PROPOSED", "operations": fuel.used, "certificate": certificate}
    except Exhausted:
        return {"status": "UNDETERMINED", "operations": fuel.used, "certificate": None}
