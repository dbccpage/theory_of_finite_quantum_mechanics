"""Bounded exact finite-clock schedules, reversible histories and rational client.

AuthorityEffect: None. The executable uses S3 and supplied rational matrices.
Arbitrary-group statements belong to Lean; no continuous-time generator is built.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations, product
import json
from pathlib import Path as _Path
import sys as _sys
from typing import Literal

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, permutation3, rational, sequence
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix, Rows

Perm = tuple[int, int, int]
Closure = Literal["emptyPeriod", "nontrivialHolonomy", "ok"]
UNIT: Perm = (0, 1, 2)
PERMS: tuple[Perm, ...] = tuple((a, b, c) for a, b, c in permutations(range(3)))


def mat(rows: object) -> Rows:
    return RationalMatrix(rows).rows


def mul(a: object, b: object) -> Rows:
    left, right = RationalMatrix(a), RationalMatrix(b)
    return left.mul(right).rows


def transp(a: object) -> Rows:
    return RationalMatrix(a).transpose().rows


def apply(a: object, vector: object) -> tuple[Q, ...]:
    matrix = RationalMatrix(a)
    values = tuple(rational(value, "vector component") for value in sequence(vector, "vector", matrix.shape[1], 64))
    column = RationalMatrix(tuple((value,) for value in values))
    return tuple(row[0] for row in matrix.mul(column).rows)


def _compose(a: Perm, b: Perm) -> Perm:
    return a[b[0]], a[b[1]], a[b[2]]


def compose(a: object, b: object) -> Perm:
    return _compose(permutation3(a), permutation3(b))


def _inverse(a: Perm) -> Perm:
    return a.index(0), a.index(1), a.index(2)


def inverse(a: object) -> Perm:
    return _inverse(permutation3(a))


def _state(value: object) -> int:
    state = integer(value, "S3 state")
    if not 0 <= state < 3:
        raise Violation("input", "S3 state must be0,1 or2")
    return state


def _gauges(values: object, length: int) -> tuple[Perm, ...]:
    return tuple(permutation3(value) for value in sequence(values, "endpoint gauges", length, 65))


def _history(values: object, length: int) -> tuple[int, ...]:
    return tuple(_state(value) for value in sequence(values, "history", length, 65))


@dataclass(frozen=True, slots=True, init=False)
class PermutationSchedule:
    """Owns0..64 S3 links and65 or fewer chronological frames, rooted at identity."""
    links: tuple[Perm, ...]
    frame_values: tuple[Perm, ...]

    def __init__(self, links: object) -> None:
        owned = tuple(permutation3(value) for value in sequence(links, "schedule", maximum=64))
        frames = [UNIT]
        for link in owned:
            frames.append(_compose(link, frames[-1]))
        object.__setattr__(self, "links", owned)
        object.__setattr__(self, "frame_values", tuple(frames))

    def closure_tag(self) -> Closure:
        if not self.links:
            return "emptyPeriod"
        if self.frame_values[-1] != UNIT:
            return "nontrivialHolonomy"
        return "ok"

    def _closed(self) -> PermutationSchedule:
        tag = self.closure_tag()
        if tag != "ok":
            raise Violation("input", tag)
        return self

    def closed(self) -> Outcome[PermutationSchedule]:
        return evaluate(self._closed)

    def _blocks(self) -> tuple[Perm, ...]:
        if not self.links:
            raise Violation("input", "emptyPeriod")
        return tuple(_compose(_inverse(self.frame_values[(t+1) % len(self.links)]), _compose(link, self.frame_values[t]))
                     for t, link in enumerate(self.links))

    def blocks(self) -> Outcome[tuple[Perm, ...]]:
        return evaluate(self._blocks)

    def _changed(self, gauges: object) -> PermutationSchedule:
        owned = _gauges(gauges, len(self.frame_values))
        return PermutationSchedule(tuple(_compose(_inverse(owned[t+1]), _compose(link, owned[t]))
                                         for t, link in enumerate(self.links)))

    def changed(self, gauges: object) -> Outcome[PermutationSchedule]:
        return evaluate(self._changed, gauges)

    def _history(self, initial: object) -> tuple[int, ...]:
        state = _state(initial)
        return tuple(frame[state] for frame in self.frame_values)

    def history(self, initial: object) -> Outcome[tuple[int, ...]]:
        return evaluate(self._history, initial)

    def _evolves(self, history: object) -> bool:
        owned = _history(history, len(self.frame_values))
        return all(owned[t+1] == link[owned[t]] for t, link in enumerate(self.links))

    def evolves(self, history: object) -> Outcome[bool]:
        return evaluate(self._evolves, history)

    def _coordinates(self, history: object, gauges: object) -> tuple[int, ...]:
        states = _history(history, len(self.frame_values))
        owned = _gauges(gauges, len(self.frame_values))
        return tuple(_inverse(gauge)[state] for state, gauge in zip(states, owned))

    def coordinates(self, history: object, gauges: object) -> Outcome[tuple[int, ...]]:
        return evaluate(self._coordinates, history, gauges)


def frames(links: object) -> tuple[Perm, ...]:
    return PermutationSchedule(links).frame_values


def closure(links: object) -> Closure:
    return PermutationSchedule(links).closure_tag()


def _cases(cases: object) -> Cases:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    return cases


def _vector_controls(powers: tuple[Rows, ...], run: Cases) -> None:
    psi = (Q(3, 5), Q(4, 5))
    run.require(psi[0]*psi[0]+psi[1]*psi[1] == 1, "vector norm")
    for power in powers[:4]:
        run.require(apply(transp(power), apply(power, psi)) == psi, "transport recovery")
    run.require(apply(powers[1], psi)[0] != psi[0], "one step changes vector")
    run.require(apply(powers[2], psi)[0] != psi[0], "two steps change vector")


def _packed_product(powers: tuple[Rows, ...], step: Rows, identity: Rows) -> tuple[Rows, Rows]:
    walk = [[Q(0) for _ in range(8)] for _ in range(8)]
    shift = [[Q(0) for _ in range(8)] for _ in range(8)]
    dressing = [[Q(0) for _ in range(8)] for _ in range(8)]
    for t in range(4):
        nxt = (t+1) % 4
        for row, column in product(range(2), repeat=2):
            walk[2*nxt+row][2*t+column] = step[row][column]
            shift[2*nxt+row][2*t+column] = identity[row][column]
            dressing[2*t+row][2*t+column] = powers[t][row][column]
    return mul(transp(dressing), mul(walk, dressing)), mat(shift)


def matrix_regression(cases: Cases) -> None:
    run = _cases(cases)
    identity, minus = mat(((1, 0), (0, 1))), mat(((-1, 0), (0, -1)))
    step = mat(((0, -1), (1, 0)))
    first, second = step, mul(step, step)
    third = mul(second, step)
    fourth = mul(third, step)
    powers = (identity, first, second, third, fourth)
    run.require(second == minus, "step square")
    run.require(fourth == identity, "step order")
    run.require(mul(transp(step), step) == identity, "step orthogonality")
    for t in range(4):
        run.require(mul(mul(transp(powers[t+1]), step), powers[t]) == identity, "clock block")
    _vector_controls(powers, run)
    packed, shift = _packed_product(powers, step, identity)
    run.require(packed == shift, "packed8x8 product")


def _gauge_controls(schedule: PermutationSchedule, gauges: tuple[Perm, ...], run: Cases) -> None:
    changed = schedule._changed(gauges)
    for t, frame in enumerate(schedule.frame_values):
        expected = _compose(_inverse(gauges[t]), _compose(frame, gauges[0]))
        run.require(changed.frame_values[t] == expected, "frame covariance")
    for initial in range(3):
        history = schedule._history(initial)
        coords = schedule._coordinates(history, gauges)
        run.require(all(gauge[state] == value for gauge, state, value in zip(gauges, coords, history)), "history inverse")
        run.require(changed._evolves(coords), "evolution covariance")
        stationary = schedule._coordinates(history, schedule.frame_values)
        run.require(all(value == initial for value in stationary), "stationary coordinates")
        bad = history[:-1]+((history[-1]+1) % 3,)
        bad_coords = schedule._coordinates(bad, gauges)
        run.require(not changed._evolves(bad_coords), "nonevolving history remains nonevolving")


def gauge_regression(links: object, gauges: object, cases: Cases) -> None:
    run = _cases(cases)
    schedule = PermutationSchedule(links)
    if not schedule.links:
        raise Violation("input", "nonempty gauge regression required")
    _gauge_controls(schedule, _gauges(gauges, len(schedule.frame_values)), run)


def _cycle_controls(schedule: PermutationSchedule, run: Cases) -> None:
    for initial in range(3):
        state = initial
        for t, link in enumerate(schedule.links):
            state = link[state]
            run.require(schedule.frame_values[t+1][initial] == state, "chronological transport")
    for t, block in enumerate(schedule._blocks()):
        run.require(block == (UNIT if t+1 < len(schedule.links) else schedule.frame_values[-1]), "seam normal form")
    expected_status = "ok" if schedule.frame_values[-1] == UNIT else "nontrivialHolonomy"
    run.require(schedule.closure_tag() == expected_status, "closure decision")
    for initial_frame in PERMS:
        gauges = tuple(_compose(frame, initial_frame) for frame in schedule.frame_values)
        run.require((gauges[-1] == gauges[0]) == (schedule.frame_values[-1] == UNIT), "periodic obstruction iff")
        _gauge_controls(schedule, gauges, run)
    for offset in range(6):
        gauges = tuple(PERMS[(offset+t*2) % 6] for t in range(len(schedule.frame_values)))
        _gauge_controls(schedule, gauges, run)


def cycle_regression(links: object, cases: Cases) -> None:
    run = _cases(cases)
    schedule = PermutationSchedule(links)
    if not schedule.links:
        raise Violation("input", "nonempty cycle regression required")
    _cycle_controls(schedule, run)


def fault_regression(cases: Cases) -> None:
    """Four incorrect expression witnesses; separate source mutations supply sensitivity evidence."""
    run = _cases(cases)
    a, b = (1, 0, 2), (0, 2, 1)
    actual = tuple(b[a[state]] for state in range(3))
    run.require(compose(a, b) != actual, "reversed-order witness")
    run.require(UNIT != frames((a,))[-1], "erased-seam witness")
    value = compose(b, a)
    run.require(compose(value, value) != UNIT, "omitted-inverse witness")
    run.require(closure(()) != "ok", "empty-period witness")


def main() -> None:
    run = Cases()
    matrix_regression(run)
    run.require(closure(()) == "emptyPeriod", "zero-period refusal")
    count, closed = 0, 0
    for length in range(1, 5):
        for links in product(PERMS, repeat=length):
            cycle_regression(links, run)
            count += 1
            closed += closure(links) == "ok"
    for step in PERMS:
        for length in range(9):
            expected = UNIT
            for _ in range(length):
                expected = (step[expected[0]], step[expected[1]], step[expected[2]])
            run.require(frames((step,)*length)[-1] == expected, "constant-step power")
    fault_regression(run)
    print(json.dumps({"status": "passed", "checks": run.checks, "schedules": count, "closed": closed,
                      "nonclosing": count-closed, "scope": "bounded S3 schedules and rational matrix client; no continuous-time generator"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
