"""Independent bounded certificate for the Gaussian residue-modulo-two ansatz.

AuthorityEffect: None. The56 explicit frames are preserved from the original
checker and compared with BornGaussianMod2ClassRigidity.lean in independent
tests. This certifies the finite class-incidence system, not general Gleason
rigidity, ray continuity or a continuum extension.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys
from typing import cast

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, sequence
from checker_support.outcome import Outcome
from checker_support.rational_inverse import _inverse, inverse
from checker_support.rational_matrix import RationalMatrix

GaussianInteger = tuple[int, int]
Vector = tuple[GaussianInteger, GaussianInteger, GaussianInteger]
Frame = tuple[Vector, Vector, Vector]
Residue = tuple[int, ...]


def _integer(value: object) -> int:
    admitted = integer(value, "Gaussian integer component")
    if admitted.bit_length() > 4096:
        raise Violation("resource", "Gaussian component/intermediate exceeds4096 bits")
    return admitted


def _vector(value: object) -> Vector:
    result = tuple(tuple(_integer(x) for x in sequence(pair, "Gaussian component", 2, 2))
                   for pair in sequence(value, "Gaussian vector", 3, 3))
    return cast(Vector, result)


def _inner(left: Vector, right: Vector) -> GaussianInteger:
    real = imaginary = 0
    for (a, b), (c, d) in zip(left, right):
        real = _integer(real+_integer(_integer(a*c)+_integer(b*d)))
        imaginary = _integer(imaginary+_integer(_integer(a*d)-_integer(b*c)))
    return real, imaginary


def inner(left: object, right: object) -> Outcome[GaussianInteger]:
    return evaluate(lambda: _inner(_vector(left), _vector(right)))


def _primitive(value: Vector) -> bool:
    return any(a % 2 != b % 2 for a, b in value)


def _class(value: Vector) -> Residue:
    return tuple(component % 2 for pair in value for component in pair)


def residue(value: object) -> Outcome[Residue]:
    return evaluate(lambda: _class(_vector(value)))


def _frame(value: object) -> Frame:
    frame = cast(Frame, tuple(_vector(vector) for vector in sequence(value, "frame", 3, 3)))
    if not all(_primitive(vector) for vector in frame):
        raise Violation("input", "each frame vector must be primitive at1+i")
    if any(_inner(left, right) != (0, 0) for left, right in combinations(frame, 2)):
        raise Violation("input", "frame vectors must be pairwise Hermitian orthogonal")
    return frame


def _classes() -> tuple[Residue, ...]:
    return tuple(bits for bits in product((0, 1), repeat=6)
                 if any(bits[2*k] != bits[2*k+1] for k in range(3)))


@dataclass(frozen=True, slots=True, init=False)
class GaussianMod2FrameSystem:
    """Own56 primitive orthogonal Gaussian frames; queries certify class rigidity."""
    frames: tuple[Frame, ...]

    def __init__(self, frames: object) -> None:
        owned = tuple(_frame(frame) for frame in sequence(frames, "frame system", 56, 56))
        object.__setattr__(self, "frames", owned)

    def _incidence(self) -> RationalMatrix:
        classes = _classes()
        observed = {_class(vector) for frame in self.frames for vector in frame}
        if observed != set(classes):
            raise Violation("check", "frame system does not cover all56 admissible residue classes")
        return RationalMatrix(tuple(tuple(sum(_class(vector) == label for vector in frame) for label in classes)
                                    for frame in self.frames))

    def incidence(self) -> Outcome[RationalMatrix]:
        return evaluate(self._incidence)

    def certificate(self) -> Outcome[RationalMatrix]:
        return self.incidence().bind(inverse)

    def _verify(self, cases: Cases) -> None:
        if type(cases) is not Cases:
            raise Violation("input", "per-run Cases recorder required")
        cases.require(len(self.frames) == 56, "56 frames")
        for frame in self.frames:
            for vector in frame:
                cases.require(any(pair != (0, 0) for pair in vector), "frame vector nonzero")
                cases.require(_primitive(vector), "frame vector primitive at1+i")
            for left, right in combinations(frame, 2):
                cases.require(_inner(left, right) == (0, 0), "frame vectors orthogonal")
        cases.require(len(_classes()) == 56, "56 admissible classes")
        matrix = self._incidence()
        cases.require(matrix.shape == (56, 56), "coverage and incidence dimensions")
        certificate = _inverse(matrix)
        cases.require(certificate.shape == matrix.shape, "two-sided inverse certificate verified")
        ones = RationalMatrix(tuple((Q(1),) for _ in self.frames))
        solution = certificate.mul(ones)
        cases.require(all(row == (Q(1, 3),) for row in solution.rows), "unique class value is1/3")
        for row in matrix.mul(solution).rows:
            cases.require(row == (Q(1),), "frame sum equals1")
        cases.require(all(abs(x) <= 1 for row in certificate.rows for x in row), "inverse entries bounded by1")
        cases.require(all(12 % x.denominator == 0 for row in certificate.rows for x in row), "inverse denominators divide12")

    def verify(self, cases: Cases) -> Outcome[None]:
        return evaluate(self._verify, cases)


FRAMES: tuple[Frame, ...] = (
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, -1)), ((0, 0), (1, 0), (0, 0))),
    (((0, -1), (0, 0), (0, 0)), ((0, 0), (-1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((-1, 0), (1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((0, -1), (0, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((-1, 0), (0, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((0, -1), (-1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, 0), (-1, 0)), ((-1, 0), (0, 0), (1, 0)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (-1, 0)), ((0, -1), (0, 0), (0, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, -1)), ((-1, 0), (0, 0), (0, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, -1)), ((0, -1), (0, 0), (-1, 0)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, 0), (-1, 0)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, 0), (0, -1)), ((0, 0), (0, 1), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (-1, 0)), ((0, 0), (0, -1), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (0, -1)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, 0)), ((-1, 0), (1, -1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, 0)), ((0, -1), (1, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, -1), (0, -1), (0, 0)), ((-1, 0), (1, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, -1), (0, 0), (-1, 0)), ((-1, 0), (0, 0), (1, -1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, -1), (0, 0), (-1, 0)), ((0, -1), (0, 0), (1, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, -1), (0, 0), (0, -1)), ((-1, 0), (0, 0), (1, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, -1), (-1, 0)), ((0, 0), (1, 0), (-1, 1))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, -1), (0, -1)), ((0, 0), (1, 0), (-1, -1))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (-1, -1)), ((0, 0), (-1, -1), (1, 0))),
    (((-1, -1), (-1, 0), (-1, 0)), ((-1, -1), (1, 0), (1, 0)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, -1), (-1, 0), (-1, 0)), ((-1, 1), (0, -1), (0, -1)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, -1)), ((-1, -1), (1, 0), (0, 1)), ((0, 0), (0, 1), (1, 0))),
    (((-1, -1), (-1, 0), (0, -1)), ((-1, 1), (0, -1), (1, 0)), ((0, 0), (0, 1), (1, 0))),
    (((-1, 0), (-1, -1), (-1, 0)), ((-1, 0), (1, 1), (-1, 0)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, -1), (-1, 0)), ((0, -1), (-1, 1), (0, -1)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, -1), (0, -1)), ((-1, 0), (1, 1), (0, -1)), ((0, 1), (0, 0), (1, 0))),
    (((-1, 0), (-1, -1), (0, -1)), ((0, -1), (-1, 1), (1, 0)), ((0, 1), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (-1, -1)), ((-1, 0), (-1, 0), (1, 1)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, 0), (-1, 0), (-1, -1)), ((0, -1), (0, -1), (-1, 1)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, -1), (-1, -1)), ((-1, 0), (0, -1), (1, 1)), ((0, 1), (1, 0), (0, 0))),
    (((-1, 0), (0, -1), (-1, -1)), ((0, -1), (1, 0), (-1, 1)), ((0, 1), (1, 0), (0, 0))),
    (((-1, 0), (-1, 0), (-1, 0)), ((-2, 0), (1, 0), (1, 0)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, 0), (-1, 0), (-1, 0)), ((-1, 0), (-1, 0), (2, 0)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, 0), (-1, 0), (-1, 0)), ((-1, 0), (2, 0), (-1, 0)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (0, -1)), ((-2, 0), (1, 0), (0, 1)), ((0, 0), (0, 1), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((-1, 0), (1, 0), (0, -2)), ((0, 1), (0, -1), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((0, -1), (0, 1), (0, -1)), ((-1, 0), (1, 0), (2, 0))),
    (((-1, 0), (0, -1), (-1, 0)), ((-2, 0), (0, 1), (1, 0)), ((0, 0), (0, -1), (1, 0))),
    (((-1, 0), (0, -1), (0, -1)), ((-2, 0), (0, 1), (0, 1)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((-1, 0), (0, 1), (0, -2)), ((0, 1), (1, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((0, -1), (-1, 0), (0, -1)), ((0, 1), (1, 0), (0, -2))),
    (((-1, -1), (-1, -1), (-1, 0)), ((-1, -1), (0, 1), (1, -1)), ((1, 0), (-1, 1), (-1, -1))),
    (((-1, -1), (-1, -1), (-1, 0)), ((-1, -1), (1, 0), (1, 1)), ((1, 0), (-1, -1), (1, 1))),
    (((-1, -1), (-1, -1), (-1, 0)), ((0, -1), (-1, 1), (1, -1)), ((-1, -1), (1, 0), (1, 1))),
    (((-1, -1), (-1, -1), (0, -1)), ((-1, -1), (0, 1), (1, 1)), ((1, 0), (-1, 1), (1, -1))),
    (((-1, -1), (-1, -1), (-1, 0)), ((-1, 0), (-1, 0), (2, -2)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, -1), (-1, 0), (-1, -1)), ((-1, 0), (2, -2), (-1, 0)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, 0)), ((-1, 0), (1, -1), (-1, 0)), ((1, 0), (-1, 1), (-3, 0))),
    (((-1, -1), (0, 0), (-1, 0)), ((-1, 0), (-1, 0), (1, -1)), ((1, 0), (-3, 0), (-1, 1))),
    (((0, 0), (-1, -1), (-1, 0)), ((-1, 0), (-1, 0), (1, -1)), ((-3, 0), (1, 0), (-1, 1))),
)


def main() -> None:
    cases = Cases()
    GaussianMod2FrameSystem(FRAMES)._verify(cases)
    print(f"checked {cases.checks} conditions, 0 failures")


if __name__ == "__main__":
    raise SystemExit(cli(main))
