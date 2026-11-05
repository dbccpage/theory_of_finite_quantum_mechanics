"""Bounded exact electroweak doublet normalization and residual covariance.

AuthorityEffect: None. Rational roots are supplied and checked, never inferred.
The finite controls do not establish continuum fields or electroweak dynamics.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import rational, sequence
from checker_support.gaussian_rational import GaussianRational as GR
from checker_support.outcome import Outcome

Pair = tuple[GR, GR]
Matrix = tuple[GR, GR, GR, GR]


def _gaussian(value: object) -> GR:
    if type(value) is not GR:
        raise Violation("input", "exact GaussianRational value required")
    return value


def exact(value: object) -> Q:
    return rational(value)


def _divide(value: GR, denominator: Q) -> GR:
    if denominator == 0:
        raise Violation("input", "normalization denominator must be nonzero")
    return GR(value.re / denominator, value.im / denominator)


def _unit_phase(value: object) -> GR:
    phase = _gaussian(value)
    if rational(phase.norm_sq(), "phase squared norm") != 1:
        raise Violation("input", "unit phase required")
    return phase


@dataclass(frozen=True, slots=True, init=False)
class ElectroweakDoublet:
    """Owned Q(i)^2 value; normalization requires a checked positive root."""
    p: GR
    q: GR

    def __init__(self, p: object, q: object) -> None:
        first, second = _gaussian(p), _gaussian(q)
        object.__setattr__(self, "p", first)
        object.__setattr__(self, "q", second)

    @property
    def components(self) -> Pair:
        return self.p, self.q

    def _norm_squared(self) -> Q:
        first = rational(self.p.norm_sq(), "first squared norm")
        second = rational(self.q.norm_sq(), "second squared norm")
        return rational(first + second, "doublet squared norm")

    def norm_squared(self) -> Outcome[Q]:
        return evaluate(self._norm_squared)

    def _scaled(self, phase: object) -> ElectroweakDoublet:
        value = _gaussian(phase)
        return ElectroweakDoublet(value.mul(self.p), value.mul(self.q))

    def scaled(self, phase: object) -> Outcome[ElectroweakDoublet]:
        return evaluate(self._scaled, phase)

    def _normalized(self, root: object) -> ElectroweakDoublet:
        denominator = exact(root)
        norm = self._norm_squared()
        if norm == 0:
            raise Violation("input", "zeroNorm")
        if denominator <= 0:
            raise Violation("input", "nonpositiveScale")
        if rational(denominator * denominator, "root square") != norm:
            raise Violation("input", "mismatchedSquare")
        return ElectroweakDoublet(_divide(self.p, denominator), _divide(self.q, denominator))

    def normalized(self, root: object) -> Outcome[ElectroweakDoublet]:
        return evaluate(self._normalized, root)

    def _acted(self, phase: object) -> ElectroweakDoublet:
        value = _unit_phase(phase)
        if self._norm_squared() != 1:
            raise Violation("input", "unit doublet required")
        return self._scaled(value)

    def acted(self, phase: object) -> Outcome[ElectroweakDoublet]:
        return evaluate(self._acted, phase)

    def dressing(self) -> Matrix:
        return self.q.conj(), self.p, GR(-self.p.re, self.p.im), self.q


def v2(p: object, q: object) -> Q:
    return ElectroweakDoublet(p, q)._norm_squared()


def U(p: object, q: object) -> Matrix:
    return ElectroweakDoublet(p, q).dressing()


def scale(z: object, p: object, q: object) -> Pair:
    return ElectroweakDoublet(p, q)._scaled(z).components


def _entries(entries: object) -> Matrix:
    a, b, c, d = sequence(entries, "2x2 Gaussian matrix", 4)
    return _gaussian(a), _gaussian(b), _gaussian(c), _gaussian(d)


def right_diag(entries: object, c0: object, c1: object) -> Matrix:
    a, b, c, d = _entries(entries)
    left, right = _gaussian(c0), _gaussian(c1)
    return a.mul(left), b.mul(right), c.mul(left), d.mul(right)


def scale_mat(entries: object, s: object) -> Matrix:
    a, b, c, d = _entries(entries)
    denominator = exact(s)
    return _divide(a, denominator), _divide(b, denominator), _divide(c, denominator), _divide(d, denominator)


def checked_normalize(p: object, q: object, root: object) -> Pair:
    return ElectroweakDoublet(p, q)._normalized(root).components


def unit_action(z: object, phi: object) -> Pair:
    p, q = sequence(phi, "doublet", 2)
    return ElectroweakDoublet(p, q)._acted(z).components


def _cases(cases: object) -> Cases:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    return cases


def check_unnormalized(z: object, p: object, q: object, cases: Cases) -> None:
    run = _cases(cases)
    phase, doublet = _gaussian(z), ElectroweakDoublet(p, q)
    transformed = doublet._scaled(phase)
    run.require(transformed.dressing() == right_diag(doublet.dressing(), phase.conj(), phase), "unnormalized covariance")
    expected = rational(rational(phase.norm_sq()) * doublet._norm_squared())
    run.require(transformed._norm_squared() == expected, "squared norm multiplicativity")


def check_action_case(phi: object, root: object, phases: object, cases: Cases) -> None:
    run = _cases(cases)
    p, q = sequence(phi, "doublet", 2)
    doublet = ElectroweakDoublet(p, q)
    labels = tuple(_unit_phase(value) for value in sequence(phases, "unit phases", maximum=64))
    norm = doublet._normalized(root)
    denominator = exact(root)
    run.require(norm._norm_squared() == 1, "normalization unit norm")
    run.require(norm._normalized(Q(1)) == norm, "normalization fixed on unit input")
    for z in labels:
        run.require(doublet._scaled(z)._normalized(root) == norm._acted(z), "normalization covariance")
        run.require(scale_mat(doublet._scaled(z).dressing(), denominator) == right_diag(scale_mat(doublet.dressing(), denominator), z.conj(), z), "matrix covariance")
        for w in labels:
            run.require(norm._acted(w)._acted(z) == norm._acted(z.mul(w)), "unit action composition")


def _invalid_controls(run: Cases) -> None:
    cases: tuple[tuple[Callable[[], object], str], ...] = (
        (lambda: checked_normalize(GR(0), GR(0), 1), "zeroNorm"),
        (lambda: checked_normalize(GR(1), GR(0), 0), "nonpositiveScale"),
        (lambda: checked_normalize(GR(1), GR(0), -1), "nonpositiveScale"),
        (lambda: checked_normalize(GR(1), GR(0), 2), "mismatchedSquare"),
        (lambda: checked_normalize(GR(1), GR(1), 1), "mismatchedSquare"),
        (lambda: checked_normalize(GR(1), GR(0), True), "rational requires int or Fraction, excluding bool/float"),
        (lambda: checked_normalize(GR(1), GR(0), 1.0), "rational requires int or Fraction, excluding bool/float"),
        (lambda: checked_normalize(GR(1), GR(0), "1"), "rational requires int or Fraction, excluding bool/float"),
        (lambda: unit_action(GR(2), (GR(1), GR(0))), "unit phase required"),
        (lambda: unit_action(GR(1), (GR(2), GR(0))), "unit doublet required"),
    )
    for action, message in cases:
        result = evaluate(action)
        run.require(result.error is not None and result.error.kind == "input" and result.error.message == message, "invalid normalization input refused")


def check_normalization_api(cases: Cases) -> None:
    run = _cases(cases)
    ts = (Q(-2), Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1), Q(2))
    phases = tuple(GR((1-t*t)/(1+t*t), 2*t/(1+t*t)) for t in ts) + (GR(-1),)
    base = ((GR(1), GR(0), Q(1)), (GR(3), GR(4), Q(5)), (GR(1, 1), GR(1, 1), Q(2)))
    for p, q, root in base:
        for factor in (Q(1), Q(2), Q(1, 3)):
            check_action_case(scale(GR(factor), p, q), factor*root, phases, run)
    _invalid_controls(run)


def _witness_controls(run: Cases) -> None:
    phase, p, q = GR(Q(3, 5), Q(4, 5)), GR(1), GR(0)
    run.require(phase.norm_sq() == 1, "unit witness norm")
    run.require(v2(p, q) == 1, "axis norm")
    run.require(v2(*scale(phase, p, q)) == 1, "shared root")
    left = scale_mat(U(*scale(phase, p, q)), 1)
    run.require(left == right_diag(scale_mat(U(p, q), 1), phase.conj(), phase), "unit normalized covariance")
    run.require(left[1] == phase, "unit entry01")
    two = GR(2)
    scaled = scale(two, p, q)
    run.require(two.norm_sq() == 4, "nonunit phase norm")
    run.require(v2(*scaled) == 4, "nonunit doublet norm")
    own_left = scale_mat(U(*scaled), 2)[1]
    own_right = right_diag(scale_mat(U(p, q), 1), two.conj(), two)[1]
    run.require(own_left == GR(1), "own-root left entry")
    run.require(own_right == GR(2), "own-root right entry")
    run.require(own_left != own_right, "nonunit own-root counterexample")
    run.require(scale_mat(U(*scaled), 1) == right_diag(scale_mat(U(p, q), 1), two.conj(), two), "nonunit shared denominator")


def main() -> None:
    run = Cases()
    check_normalization_api(run)
    check_unnormalized(GR(Q(1, 2), Q(1, 3)), GR(Q(2, 7), Q(1, 5)), GR(Q(3, 11), 4), run)
    _witness_controls(run)
    print(json.dumps({"status": "passed", "checks": run.checks, "doublets": 9, "phases": 8,
                      "scope": "exact rational supplied-root normalization and residual covariance; no continuum dynamics"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
