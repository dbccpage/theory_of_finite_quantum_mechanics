"""Exact finite projective representations over the Gaussian rationals Q(i).

U(g) U(h) = omega(g, h) U(gh) defines the phase function omega.  For the Pauli
Klein-four representation, sigma_x sigma_z = -i sigma_y, so omega(x, z) = -i and
omega(z, x) = i; their ratio -1 is unchanged by every unit rephasing.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product as triples
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from .exact import as_fraction
from .outcomes import Accepted, Outcome, RefusalCode, Refused


@dataclass(frozen=True)
class GaussianRational:
    """real + i * imag with exact rational parts; floats are refused."""

    real: Fraction
    imag: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "real", as_fraction(self.real))
        object.__setattr__(self, "imag", as_fraction(self.imag))

    def __add__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(self.real + other.real, self.imag + other.imag)

    def __neg__(self) -> GaussianRational:
        return GaussianRational(-self.real, -self.imag)

    def __mul__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __truediv__(self, other: GaussianRational) -> GaussianRational:
        norm = other.norm_squared()
        if norm == 0:
            raise ZeroDivisionError("division by the Gaussian rational zero")
        return self * GaussianRational(other.real / norm, -other.imag / norm)

    def conjugate(self) -> GaussianRational:
        return GaussianRational(self.real, -self.imag)

    def conj(self) -> GaussianRational:
        return self.conjugate()

    def norm_squared(self) -> Fraction:
        return self.real * self.real + self.imag * self.imag

    def __sub__(self, other: GaussianRational) -> GaussianRational:
        if isinstance(other, GaussianRational):
            return GaussianRational(self.real - other.real, self.imag - other.imag)
        if isinstance(other, (int, Fraction)):
            return GaussianRational(self.real - as_fraction(other), self.imag)
        if type(other) is complex:
            real_ok = (
                isfinite(other.real)
                and other.real.is_integer()
                and float(int(other.real)) == other.real
            )
            imag_ok = (
                isfinite(other.imag)
                and other.imag.is_integer()
                and float(int(other.imag)) == other.imag
            )
            if real_ok and imag_ok:
                return GaussianRational(
                    self.real - Fraction(int(other.real)),
                    self.imag - Fraction(int(other.imag)),
                )
            return NotImplemented
        return NotImplemented

    def __complex__(self) -> complex:
        return complex(float(self.real), float(self.imag))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        assert isinstance(other, GaussianRational)
        return self.real == other.real and self.imag == other.imag

    def __hash__(self) -> int:
        return hash((self.real, self.imag))


ZERO = GaussianRational(0)
ONE = GaussianRational(1)
I_UNIT = GaussianRational(0, 1)
UNIT_PHASES_Z4 = (ONE, I_UNIT, -ONE, -I_UNIT)


@dataclass(frozen=True)
class Matrix2:
    entries: tuple[GaussianRational, GaussianRational, GaussianRational, GaussianRational]

    def __post_init__(self) -> None:
        if (
            type(self.entries) is not tuple
            or len(self.entries) != 4
            or any(not isinstance(entry, GaussianRational) for entry in self.entries)
        ):
            raise ValueError("a 2x2 matrix needs four Gaussian-rational entries")

    def __matmul__(self, other: Matrix2) -> Matrix2:
        a, b, c, d = self.entries
        e, f, g, h = other.entries
        return Matrix2((a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h))

    def scaled(self, phase: GaussianRational) -> Matrix2:
        a, b, c, d = self.entries
        return Matrix2((phase * a, phase * b, phase * c, phase * d))

    def adjoint(self) -> Matrix2:
        a, b, c, d = self.entries
        return Matrix2((a.conjugate(), c.conjugate(), b.conjugate(), d.conjugate()))

    def is_unitary(self) -> bool:
        return self @ self.adjoint() == IDENTITY


def matrix2(*entries: GaussianRational | int) -> Matrix2:
    converted = tuple(entry if isinstance(entry, GaussianRational) else GaussianRational(entry) for entry in entries)
    return Matrix2(converted)  # type: ignore[arg-type]


IDENTITY = matrix2(1, 0, 0, 1)
SIGMA_X = matrix2(0, 1, 1, 0)
SIGMA_Y = matrix2(ZERO, -I_UNIT, I_UNIT, ZERO)
SIGMA_Z = matrix2(1, 0, 0, -1)


@dataclass(frozen=True)
class ProjectiveRepresentation:
    """A finite associative product table with one 2x2 matrix per element."""

    elements: tuple[str, ...]
    product: Mapping[tuple[str, str], str]
    matrices: Mapping[str, Matrix2]

    def __post_init__(self) -> None:
        object.__setattr__(self, "elements", tuple(self.elements))
        if not isinstance(self.product, Mapping):
            raise ValueError("the product table must be total and closed on the carrier")
        if not isinstance(self.matrices, Mapping):
            raise ValueError("every element needs exactly one 2x2 matrix")
        object.__setattr__(self, "product", MappingProxyType(dict(self.product)))
        object.__setattr__(self, "matrices", MappingProxyType(dict(self.matrices)))
        if not self.elements or len(set(self.elements)) != len(self.elements):
            raise ValueError("group elements must be a unique nonempty tuple")
        labels = set(self.elements)
        pairs = {(g, h) for g in self.elements for h in self.elements}
        if set(self.product) != pairs or not set(self.product.values()) <= labels:
            raise ValueError("the product table must be total and closed on the carrier")
        if any(
            self.product[(self.product[(g, h)], k)] != self.product[(g, self.product[(h, k)])]
            for g, h, k in triples(self.elements, repeat=3)
        ):
            raise ValueError("the product table is not associative")
        if (
            set(self.matrices) != labels
            or any(not isinstance(matrix, Matrix2) for matrix in self.matrices.values())
        ):
            raise ValueError("every element needs exactly one 2x2 matrix")


def klein_four_pauli() -> ProjectiveRepresentation:
    """U(e) = I, U(x) = sigma_x, U(z) = sigma_z, U(xz) = sigma_y on Z2 x Z2."""

    bits = {"e": (0, 0), "x": (1, 0), "z": (0, 1), "xz": (1, 1)}
    names = {value: key for key, value in bits.items()}
    table = {
        (g, h): names[(bits[g][0] ^ bits[h][0], bits[g][1] ^ bits[h][1])] for g in bits for h in bits
    }
    matrices = {"e": IDENTITY, "x": SIGMA_X, "z": SIGMA_Z, "xz": SIGMA_Y}
    return ProjectiveRepresentation(tuple(bits), table, matrices)


def projective_cocycle(rep: ProjectiveRepresentation) -> Outcome[dict[tuple[str, str], GaussianRational]]:
    """omega(g, h) with U(g) U(h) = omega(g, h) U(gh), for every pair."""

    if not isinstance(rep, ProjectiveRepresentation):
        return Refused(RefusalCode.INVALID_INPUT, "a projective representation is required")
    for element in rep.elements:
        if not rep.matrices[element].is_unitary():
            return Refused(RefusalCode.NOT_PROJECTIVE, f"U({element}) is not unitary")
    omega: dict[tuple[str, str], GaussianRational] = {}
    for g in rep.elements:
        for h in rep.elements:
            left, target = rep.matrices[g] @ rep.matrices[h], rep.matrices[rep.product[(g, h)]]
            index = next(i for i, entry in enumerate(target.entries) if entry != ZERO)
            phase = left.entries[index] / target.entries[index]
            if target.scaled(phase) != left:
                return Refused(RefusalCode.NOT_PROJECTIVE, f"U({g})U({h}) is not a phase times U({g}{h})")
            omega[(g, h)] = phase
    return Accepted(omega)


def verify_cocycle_identity(
    rep: ProjectiveRepresentation,
    omega: Mapping[tuple[str, str], GaussianRational],
) -> Outcome[int]:
    """omega(g, h) omega(gh, k) = omega(g, hk) omega(h, k) for every triple."""

    if not isinstance(rep, ProjectiveRepresentation):
        return Refused(RefusalCode.INVALID_INPUT, "a projective representation is required")
    pairs = {(g, h) for g in rep.elements for h in rep.elements}
    if (
        not isinstance(omega, Mapping)
        or set(omega) != pairs
        or any(not isinstance(value, GaussianRational) for value in omega.values())
    ):
        return Refused(RefusalCode.INVALID_INPUT, "omega must assign one Gaussian rational to every pair")
    for g, h, k in triples(rep.elements, repeat=3):
        left = omega[(g, h)] * omega[(rep.product[(g, h)], k)]
        right = omega[(g, rep.product[(h, k)])] * omega[(h, k)]
        if left != right:
            return Refused(RefusalCode.CERTIFICATE_MISMATCH, f"2-cocycle identity fails at {(g, h, k)!r}")
    return Accepted(len(rep.elements) ** 3)


def commutator_ratio(rep: ProjectiveRepresentation, x: str, z: str) -> Outcome[GaussianRational]:
    """omega(x, z) / omega(z, x) for commuting x and z."""

    if not isinstance(rep, ProjectiveRepresentation):
        return Refused(RefusalCode.INVALID_INPUT, "a projective representation is required")
    if x not in rep.elements or z not in rep.elements:
        return Refused(RefusalCode.OUTSIDE_CARRIER, "commutator elements must lie in the group")
    if rep.product[(x, z)] != rep.product[(z, x)]:
        return Refused(RefusalCode.INVALID_INPUT, "the ratio is rephasing-invariant only for commuting elements")
    omega = projective_cocycle(rep)
    if isinstance(omega, Refused):
        return omega
    return Accepted(omega.value[(x, z)] / omega.value[(z, x)])


def rephase(
    rep: ProjectiveRepresentation,
    lam: Mapping[str, GaussianRational],
) -> Outcome[ProjectiveRepresentation]:
    """U'(g) = lambda(g) U(g) for a unit-modulus lambda on every element."""

    if not isinstance(rep, ProjectiveRepresentation):
        return Refused(RefusalCode.INVALID_INPUT, "a projective representation is required")
    if (
        not isinstance(lam, Mapping)
        or set(lam) != set(rep.elements)
        or any(not isinstance(value, GaussianRational) for value in lam.values())
    ):
        return Refused(RefusalCode.INVALID_INPUT, "rephasing must assign one Gaussian rational to every element")
    if any(value.norm_squared() != 1 for value in lam.values()):
        return Refused(RefusalCode.NON_UNIT_PHASE, "rephasing phases must have unit modulus")
    matrices = {element: rep.matrices[element].scaled(lam[element]) for element in rep.elements}
    return Accepted(ProjectiveRepresentation(rep.elements, dict(rep.product), matrices))


# Executable finite evidence; AuthorityEffect: None.
