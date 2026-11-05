"""Independent submitted-witness checker; this module never calls a proposer."""

from __future__ import annotations

from dataclasses import dataclass

from state_effect_readout.model import add, dagger, matmul

from .model import (
    ONE,
    ZERO,
    Carrier,
    Exhausted,
    Fuel,
    G,
    I,
    Q,
    apply,
    basis_unit,
    conjugate,
    digest,
    gaussian,
    inverse,
    linear_extension,
    matrix,
    rational,
    scale,
    subtract,
    vector,
)


class InvalidWitness(ValueError):
    """Well-typed submitted evidence fails its mathematical obligation."""


def require(predicate: bool, message: str) -> None:
    if not predicate:
        raise InvalidWitness(message)


def fields(raw: object, expected: set[str]) -> dict:
    if type(raw) is not dict or set(raw) != expected:
        raise ValueError(f"expected exactly these fields: {sorted(expected)}")
    return raw


def admit_problem(raw: object) -> tuple[dict, Carrier]:
    if type(raw) is not dict or type(raw.get("kind")) is not str:
        raise ValueError("task kind is missing")
    extras = {
        "reachability": {"source", "target"},
        "luders": {"source", "target"},
        "preserver": {"frame", "images"},
        "generator": {"derivation"},
    }
    if raw["kind"] not in extras:
        raise ValueError("unknown task kind")
    fields(raw, {"schema", "field", "kind", "gram"} | extras[raw["kind"]])
    if raw["schema"] != "wdp.preserver.task.v1" or raw["field"] != "Q(i)":
        raise ValueError("wrong task schema or coefficient domain")
    carrier = Carrier.from_wire(raw["gram"])
    d = carrier.dimension
    if raw["kind"] in ("reachability", "luders"):
        for key in ("source", "target"):
            if carrier.norm(vector(raw[key], d)) == 0:
                raise ValueError("task names a zero ray")
    elif raw["kind"] == "preserver":
        inverse(matrix(raw["frame"], d))
        matrix(raw["images"], d)
    else:
        if type(raw["derivation"]) not in (list, tuple) or len(raw["derivation"]) != d * d:
            raise ValueError("derivation table must supply every matrix unit")
        for entry in raw["derivation"]:
            matrix(entry, d)
    return raw, carrier


def check_prime(prime: int, fuel: Fuel) -> bool:
    if type(prime) is not int or prime < 2:
        return False
    divisor = 2
    while divisor * divisor <= prime:
        fuel.spend()
        if prime % divisor == 0:
            return False
        divisor += 1
    return True


def valuation(number: Q, prime: int, fuel: Fuel) -> int:
    values = []
    for part in (number.numerator, number.denominator):
        exponent = 0
        while part % prime == 0:
            fuel.spend()
            part //= prime
            exponent += 1
        values.append(exponent)
    return values[0] - values[1]


def _preserver(problem, carrier, evidence, claim, fuel):
    fields(evidence, {"matrix", "branch", "multiplier"})
    require(claim == "global_semisimilarity", "wrong preserver claim")
    if evidence["branch"] not in ("identity", "conjugate"):
        raise ValueError("unknown automorphism branch")
    m = matrix(evidence["matrix"], carrier.dimension)
    c = rational(evidence["multiplier"])
    require(c > 0, "nonpositive similarity multiplier")
    h = carrier.gram
    twisted = conjugate(h) if evidence["branch"] == "conjugate" else h
    fuel.spend()
    require(
        matmul(dagger(m), matmul(h, m)) == scale(G.of(c), twisted),
        "complete semisimilarity Gram identity failed",
    )
    frame = matrix(problem["frame"], carrier.dimension)
    images = matrix(problem["images"], carrier.dimension)
    for source, target in zip(frame, images, strict=True):
        source = (
            tuple(x.conjugate() for x in source) if evidence["branch"] == "conjugate" else source
        )
        fuel.spend()
        require(apply(m, source) == target, "declared frame action failed")


def _reachability(problem, carrier, evidence, claim, fuel):
    f = vector(problem["source"], carrier.dimension)
    g = vector(problem["target"], carrier.dimension)
    ratio = carrier.norm(f) / carrier.norm(g)
    if claim == "unitary_impossible":
        fields(evidence, {"prime", "valuation"})
        prime = evidence["prime"]
        require(check_prime(prime, fuel), "obstruction has no verified prime")
        require(prime % 4 == 3, "prime is not 3 modulo 4")
        if type(evidence["valuation"]) is not int:
            raise ValueError("valuation must be an integer")
        actual = valuation(ratio, prime, fuel)
        require(
            actual == evidence["valuation"] and actual % 2 == 1, "exact odd valuation check failed"
        )
        return
    require(claim == "unitary_reachable", "wrong reachability claim")
    fields(evidence, {"matrix", "scalar"})
    u = matrix(evidence["matrix"], carrier.dimension)
    a = gaussian(evidence["scalar"])
    require(a.norm() == ratio, "submitted norm scalar failed")
    fuel.spend()
    require(
        matmul(dagger(u), matmul(carrier.gram, u)) == carrier.gram,
        "submitted matrix is not unitary for the original Gram form",
    )
    require(apply(u, f) == tuple(a * x for x in g), "submitted source-to-target map failed")


def _luders(problem, carrier, evidence, claim, fuel):
    fields(evidence, {"projection", "probability", "branch_vector"})
    d = carrier.dimension
    f, g = vector(problem["source"], d), vector(problem["target"], d)
    p = matrix(evidence["projection"], d)
    probability = rational(evidence["probability"])
    branch = vector(evidence["branch_vector"], d)
    fuel.spend()
    require(
        carrier.adjoint(p) == p and matmul(p, p) == p,
        "submitted projection is not a selfadjoint idempotent",
    )
    require(apply(p, g) == g, "submitted projection does not fix its target")
    # Test its complete basis action, not only the single source ray.
    for j in range(d):
        basis = tuple(ONE if k == j else ZERO for k in range(d))
        coefficient = carrier.inner(g, basis) * G.of(1 / carrier.norm(g))
        fuel.spend()
        require(
            apply(p, basis) == tuple(coefficient * x for x in g),
            "submitted projector is not the named rank-one projector",
        )
    require(branch == apply(p, f), "submitted branch vector failed")
    require(probability == carrier.norm(branch) / carrier.norm(f), "branch probability failed")
    require(probability == carrier.probability(f, g), "transition probability failed")
    expected_claim = "positive_postselection" if probability > 0 else "zero_branch"
    require(claim == expected_claim, "zero branch cannot be normalized or called success")


def _generator(problem, carrier, evidence, claim, fuel):
    fields(evidence, {"implementer", "hermitian_generator"})
    require(claim == "inner_dagger_derivation", "wrong generator claim")
    n = carrier.dimension
    table = tuple(matrix(entry, n) for entry in problem["derivation"])
    s, h0 = matrix(evidence["implementer"], n), matrix(evidence["hermitian_generator"], n)
    require(carrier.adjoint(h0) == h0, "generator is not Hermitian")
    require(s == scale(-I, h0), "implementer does not equal -i times generator")
    units = [basis_unit(n, j, k) for j in range(n) for k in range(n)]
    for a, delta_a in zip(units, table, strict=True):
        fuel.spend()
        require(
            subtract(matmul(s, a), matmul(a, s)) == delta_a,
            "submitted generator fails a matrix-unit image",
        )
        require(
            linear_extension(table, carrier.adjoint(a)) == carrier.adjoint(delta_a),
            "matrix-unit dagger law failed",
        )
        for b, delta_b in zip(units, table, strict=True):
            fuel.spend()
            require(
                linear_extension(table, matmul(a, b))
                == add(matmul(delta_a, b), matmul(a, delta_b)),
                "matrix-unit Leibniz law failed",
            )


@dataclass(frozen=True)
class CheckResult:
    status: str
    claim: str | None
    reason: str
    operations: int


def check(problem: object, certificate: object, operation_limit: int = 100_000) -> CheckResult:
    """Check original inputs and submitted evidence without repairing either.

    VERIFIED can mean a certified negative norm result; inspect ``claim``.
    INVALID is a false witness, MALFORMED is inadmissible input, and
    UNDETERMINED is checker resource exhaustion. None grants authorization.
    """
    fuel = Fuel(operation_limit)
    try:
        task, carrier = admit_problem(problem)
        fields(certificate, {"schema", "problem_sha256", "claim", "evidence"})
        if certificate["schema"] != "wdp.preserver.certificate.v1":
            raise ValueError("wrong certificate schema")
        require(certificate["problem_sha256"] == digest(task), "original problem binding failed")
        if type(certificate["claim"]) is not str:
            raise ValueError("certificate claim must be a string")
        dispatch = {
            "preserver": _preserver,
            "reachability": _reachability,
            "luders": _luders,
            "generator": _generator,
        }
        dispatch[task["kind"]](task, carrier, certificate["evidence"], certificate["claim"], fuel)
        return CheckResult(
            "VERIFIED", certificate["claim"], "submitted evidence replayed", fuel.used
        )
    except Exhausted as exc:
        return CheckResult("UNDETERMINED", None, str(exc), fuel.used)
    except InvalidWitness as exc:
        return CheckResult("INVALID", None, str(exc), fuel.used)
    except (ValueError, TypeError, KeyError, ZeroDivisionError, IndexError) as exc:
        return CheckResult("MALFORMED", None, str(exc), fuel.used)
