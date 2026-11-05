"""Exact integer obstruction controls for the Hilbert, Stone and U1 slices.

AuthorityEffect: None. Root calculations and bounded integer censuses do not
select a scalar field, completion, continuous-time generator or circle group.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, sequence
from checker_support.integer_quadratic_equation import IntegerQuadraticEquation as Equation, _integer, _square_root
from checker_support.outcome import Outcome


@dataclass(frozen=True, slots=True, init=False)
class IntegerObstructionControls:
    """Owns four bounded census domains and their exact equation models."""
    hilbert_radius: int
    pair_bound: int
    natural_bound: int
    box_radius: int
    linear_equation: Equation
    hilbert_equation: Equation
    square_equation: Equation
    four_fifths_equation: Equation

    def __init__(self, hilbert_radius: object = 32, pair_bound: object = 30,
                 natural_bound: object = 2000, box_radius: object = 12) -> None:
        object.__setattr__(self, 'hilbert_radius', integer(hilbert_radius, 'Hilbert radius', 0, 64))
        object.__setattr__(self, 'pair_bound', integer(pair_bound, 'natural pair bound', 0, 64))
        object.__setattr__(self, 'natural_bound', integer(natural_bound, 'natural scan bound', 0, 10000))
        object.__setattr__(self, 'box_radius', integer(box_radius, 'integer box radius', 0, 16))
        object.__setattr__(self, 'linear_equation', Equation((0, 2, -1)))
        object.__setattr__(self, 'hilbert_equation', Equation((1, -1, -1)))
        object.__setattr__(self, 'square_equation', Equation((1, 0, -5)))
        object.__setattr__(self, 'four_fifths_equation', Equation((5, 0, -4)))

    def _root_certificates(self, cases: Cases) -> None:
        cases.require(self.linear_equation._rational_roots() == (Q(1, 2),), 'linear rational root is one half')
        cases.require(self.linear_equation._integer_roots() == (), 'linear equation has no integer root')
        for equation in (self.hilbert_equation, self.square_equation, self.four_fifths_equation):
            cases.require(equation._rational_roots() == (), 'nonsquare discriminant excludes rational roots')
            cases.require(equation._integer_roots() == (), 'no integer roots in selected equation')
        cases.require(Equation((1, -3, 2))._integer_roots() == (1, 2), 'positive two-root control')
        cases.require(Equation((4, 0, -4))._rational_roots() == (Q(-1), Q(1)), 'square ratio admits nonzero roots')

    def _hilbert_window(self, cases: Cases) -> int:
        visited = 0
        cases.require(1 % 2 == 1, 'one is odd')
        for value in range(-self.hilbert_radius, self.hilbert_radius+1):
            visited += 1
            cases.require((2*value) % 2 == 0 and self.linear_equation._evaluate(value) != 0, 'even double is not one')
            polynomial = self.hilbert_equation._evaluate(value)
            cases.require(4*polynomial+5 == (2*value-1)**2 == 4*value*value-4*value+1, 'discriminant identity sample')
            cases.require(self.square_equation._evaluate(value) != 0, 'integer square is not five sample')
            cases.require(abs(value) < 3 or value*value >= 9, 'large integer square bound sample')
            cases.require(polynomial != 0, 'quadratic integer nonroot sample')
        return visited

    def _zero_pair(self, candidate: object) -> tuple[int, int]:
        a, b = (_integer(v) for v in sequence(candidate, 'natural equation solution', 2))
        if a < 0 or b < 0:
            raise Violation('input', 'natural equation solution requires nonnegative integers')
        if self.four_fifths_equation._homogeneous_value((a, b)) != 0:
            raise Violation('input', 'candidate does not satisfy 5*a*a = 4*b*b')
        if a != 0 or b != 0:
            raise Violation('check', 'four-fifths equation admitted a nonzero integer solution')
        return a, b

    def zero_pair(self, candidate: object) -> Outcome[tuple[int, int]]:
        """Validate the exact natural solution; invalid candidates never exit Python."""
        return evaluate(self._zero_pair, candidate)

    def _residue_controls(self, cases: Cases) -> tuple[int, ...]:
        residues = tuple(r*r % 5 for r in range(5))
        cases.require(residues == (0, 1, 4, 4, 1), 'complete square residue table modulo five')
        cases.require(tuple(r for r, square in enumerate(residues) if square == 0) == (0,), 'only zero class has square zero')
        cases.require(tuple(r for r, square in enumerate(residues) if 4*square % 5 == 0) == (0,), 'four times square zero requires zero class')
        for residue in (0, 1, 4):
            cases.require(((4*residue) % 5 == 0) == (residue == 0), 'selected residue zero equivalence')
        cases.require(3*3+4*4 == 5*5 == 25, 'three-four-five Pythagorean scale')
        cases.require(self._zero_pair((0, 0)) == (0, 0), 'zero natural solution')
        for value in range(6):
            cases.require(5*(5*value)**2 == 125*value*value, 'left descent scaling sample')
            cases.require(4*(5*value)**2 == 100*value*value, 'right descent scaling sample')
        return residues

    def _natural_pairs(self, cases: Cases) -> int:
        visited = 0
        for a, b in product(range(self.pair_bound+1), repeat=2):
            visited += 1
            is_solution = self.four_fifths_equation._homogeneous_value((a, b)) == 0
            cases.require(is_solution == (a == b == 0), 'natural pair equation census')
            if is_solution:
                cases.require(self._zero_pair((a, b)) == (0, 0), 'natural pair solution replay')
        cases.require(visited == (self.pair_bound+1)**2, 'natural pair population count')
        return visited

    def _positive_denominators(self, cases: Cases) -> int:
        hits = 0
        for denominator in range(1, self.natural_bound+1):
            numerator = 4*denominator*denominator
            square = _square_root(numerator//5) if numerator % 5 == 0 else None
            is_hit = numerator % 5 == 0 and square is not None
            hits += int(is_hit)
            cases.require(not is_hit, 'positive denominator has no four-fifths square root')
        cases.require(hits == 0, 'positive denominator census has no solutions')
        return hits

    @staticmethod
    def _cleared(a: int, b: int, d: int) -> bool:
        # Internal census coordinates are bounded by 16 before any multiplication.
        return 5*(a*a-b*b) == 3*d*d and a*a+b*b == d*d

    def _cleared_box(self, cases: Cases) -> tuple[tuple[int, int, int], ...]:
        cases.require(self._cleared(0, 0, 0), 'cleared equations admit zero')
        cases.require(3*3+4*4 == 5*5 and 5*(3*3-4*4) != 3*5*5, 'Pythagorean triple fails the additional equation')
        hits = []
        for a, b, d in product(range(-self.box_radius, self.box_radius+1), repeat=3):
            is_solution = self._cleared(a, b, d)
            if is_solution:
                hits.append((a, b, d))
                cases.require(5*a*a == 4*d*d, 'cleared equations imply four-fifths relation')
            cases.require(is_solution == (a == b == d == 0), 'cleared integer box census')
        cases.require(hits == [(0, 0, 0)], 'cleared box has only the zero solution')
        return tuple(hits)

    def _verify(self) -> dict[str, object]:
        cases = Cases(); self._root_certificates(cases)
        hilbert_points = self._hilbert_window(cases); residues = self._residue_controls(cases)
        pairs = self._natural_pairs(cases); natural_hits = self._positive_denominators(cases)
        box_hits = self._cleared_box(cases)
        return {'status': 'PASS', 'authority_effect': 'None', 'failures': 0, 'checks': cases.checks,
                'hilbert_points': hilbert_points, 'pair_points': pairs,
                'positive_denominators': self.natural_bound, 'natural_hits': natural_hits,
                'square_residues_mod5': list(residues), 'box_points': (2*self.box_radius+1)**3,
                'box_hits': [list(point) for point in box_hits],
                'scope': 'Exact low-degree root calculations and bounded integer censuses; no scalar-field selection, completion, Stone theorem or circle-group conclusion.'}

    def verify(self) -> Outcome[dict[str, object]]:
        return evaluate(self._verify)


def verify() -> Outcome[dict[str, object]]:
    return evaluate(IntegerObstructionControls).bind(lambda controls: controls.verify())


def _main() -> None:
    print(json.dumps(IntegerObstructionControls()._verify(), sort_keys=True))


def main() -> int:
    return cli(_main)


if __name__ == '__main__':
    raise SystemExit(main())
