"""Bounded finite fermionic Fock matrices over Q(i), in occupation-bit order.

Origin: code/rust/src/majorana/majorana_fock_algebra.rs; local exact model.
Claim: urn:omega:fqm:majorana:finite-fock-occupation:v1
AuthorityEffect: None.
Scope: declared finite matrices, not a continuum field or a proof of a device.
The first mode is the most significant bit. gamma_(2j-1)=Z...ZX and
gamma_(2j)=Z...ZY, with Y|0>=i|1>. Thus c_j=(gamma_odd+i gamma_even)/2
lowers occupation and c_j* c_j is the occupied-bit projector.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence

from .majorana_modes import (
    MajoranaError, MajoranaMonomial, MajoranaOperator, anticommutator,
    commutator, kitaev_chain_parity, _require_int, _require_fraction,
)

AUTHORITY_EFFECT = "AuthorityEffect: None"
MAX_MODES = 5
MAX_MATRIX_DIMENSION = 1 << MAX_MODES
MAX_FAMILY_SIZE = 32
MAX_RELATION_PRODUCTS = 4_000_000


def _fail(invariant: str, **parameters: object) -> MajoranaError:
    return MajoranaError(invariant, parameters)


def _gaussian(value: object) -> GaussianRat:
    if type(value) is not GaussianRat:
        raise _fail("matrix scalar must be an admitted Gaussian rational", received=type(value).__name__)
    return value


@dataclass(frozen=True, slots=True, init=False, eq=False)
class GaussianRat:
    """Owned exact components, with guarded construction and reinitialization."""
    re: Fraction
    im: Fraction

    def __init__(self, re: object, im: object) -> None:
        if hasattr(self, "re"):
            raise _fail("Gaussian rational already initialized")
        real = _require_fraction(re, "Gaussian real part")
        imaginary = _require_fraction(im, "Gaussian imaginary part")
        object.__setattr__(self, "re", real)
        object.__setattr__(self, "im", imaginary)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("GaussianRat does not admit subclasses")

    @classmethod
    def from_ints(cls, re: object, im: object = 0) -> GaussianRat:
        return cls(Fraction(_require_int(re, "real integer")), Fraction(_require_int(im, "imaginary integer")))

    def __eq__(self, other: object) -> bool:
        return type(other) is GaussianRat and (self.re, self.im) == (other.re, other.im)

    def __hash__(self) -> int:
        return hash((self.re, self.im))

    def __add__(self, other: object) -> GaussianRat:
        other = _gaussian(other)
        return GaussianRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: object) -> GaussianRat:
        other = _gaussian(other)
        return GaussianRat(self.re - other.re, self.im - other.im)

    def __mul__(self, other: object) -> GaussianRat:
        other = _gaussian(other)
        return GaussianRat(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0


def gi(re: object, im: object = 0) -> GaussianRat:
    return GaussianRat.from_ints(re, im)


def _sequence(value: object, role: str, limit: int) -> tuple:
    if type(value) not in (list, tuple):
        raise _fail("matrix sequence must be a built-in list or tuple", role=role)
    if len(value) > limit:
        raise _fail("matrix sequence budget exceeded", role=role, limit=limit)
    return tuple(value)


def _matrix(value: object, expected: int | None = None) -> tuple[tuple[GaussianRat, ...], ...]:
    rows = _sequence(value, "matrix", MAX_MATRIX_DIMENSION)
    dimension = len(rows)
    if expected is not None and dimension != expected:
        raise _fail("operator dimension does not match Fock carrier", expected=expected, actual=dimension)
    admitted = []
    for row in rows:
        entries = _sequence(row, "matrix row", MAX_MATRIX_DIMENSION)
        if len(entries) != dimension:
            raise _fail("matrix must be square", dimension=dimension, columns=len(entries))
        admitted.append(tuple(_gaussian(value) for value in entries))
    return tuple(admitted)


def _product_entry(left: Sequence, right: Sequence, row: int, col: int) -> GaussianRat:
    total = gi(0)
    for index in range(len(left)):
        if not left[row][index].is_zero() and not right[index][col].is_zero():
            total = total + left[row][index] * right[index][col]
    return total


def _pair_fails(left: Sequence, right: Sequence, equal: bool) -> bool:
    for row in range(len(left)):
        for col in range(len(left)):
            actual = _product_entry(left, right, row, col) + _product_entry(right, left, row, col)
            if actual != gi(2 if equal and row == col else 0):
                return True
    return False


def first_anticommutation_failure(family: object) -> Optional[tuple[int, int]]:
    """First one-based failing pair, or None after full bounded checks.

    Empty families and equal-size 0x0 matrices satisfy these equations vacuously;
    this is not an assertion of a nonzero or faithful representation.
    """
    values = _sequence(family, "family", MAX_FAMILY_SIZE)
    matrices = tuple(_matrix(value) for value in values)
    if not matrices:
        return None
    dimension = len(matrices[0])
    if any(len(matrix) != dimension for matrix in matrices):
        raise _fail("family matrices have different dimensions")
    products = len(matrices) * (len(matrices) + 1) * dimension ** 3
    if products > MAX_RELATION_PRODUCTS:
        raise _fail("CAR product budget exceeded", limit=MAX_RELATION_PRODUCTS)
    for a, left in enumerate(matrices):
        for b in range(a, len(matrices)):
            if _pair_fails(left, matrices[b], a == b):
                return a + 1, b + 1
    return None


@dataclass(frozen=True, slots=True, init=False, eq=False)
class FockCarrier:
    _modes: int
    _dim: int

    def __init__(self, modes: object) -> None:
        if hasattr(self, "_modes"):
            raise _fail("Fock carrier already initialized")
        modes = _require_int(modes, "Fock modes")
        if not 1 <= modes <= MAX_MODES:
            raise _fail("Fock modes outside declared range", limit=MAX_MODES)
        object.__setattr__(self, "_modes", modes)
        object.__setattr__(self, "_dim", 1 << modes)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("FockCarrier does not admit subclasses")

    def modes(self) -> int:
        return self._modes

    def dimension(self) -> int:
        return self._dim

    def _index(self, index: object, count: int, role: str) -> int:
        index = _require_int(index, role)
        if not 1 <= index <= count:
            raise _fail("Fock index outside declared range", role=role, count=count)
        return index

    def majorana_generator(self, a: object) -> list[list[GaussianRat]]:
        a = self._index(a, 2 * self._modes, "Majorana index")
        mode = (a - 1) // 2
        mask = 1 << (self._modes - 1 - mode)
        matrix = [[gi(0) for _ in range(self._dim)] for _ in range(self._dim)]
        for state in range(self._dim):
            parity = -1 if (state >> (self._modes - mode)).bit_count() % 2 else 1
            bit = bool(state & mask)
            value = gi(0, -parity if bit else parity) if a % 2 == 0 else gi(parity)
            matrix[state ^ mask][state] = value
        return matrix

    def lowering_operator(self, j: object) -> list[list[GaussianRat]]:
        j = self._index(j, self._modes, "mode index")
        odd, even = self.majorana_generator(2 * j - 1), self.majorana_generator(2 * j)
        half, i_half = GaussianRat(Fraction(1, 2), Fraction(0)), GaussianRat(Fraction(0), Fraction(1, 2))
        return [[odd[r][c] * half - even[r][c] * i_half for c in range(self._dim)] for r in range(self._dim)]

    def number_operator(self, j: object) -> list[list[GaussianRat]]:
        j = self._index(j, self._modes, "mode index")
        mask = 1 << (self._modes - j)
        return [[gi(1 if row == col and row & mask else 0) for col in range(self._dim)] for row in range(self._dim)]

    def parity_operator(self) -> list[list[GaussianRat]]:
        return [[gi((-1 if row.bit_count() % 2 else 1) if row == col else 0) for col in range(self._dim)] for row in range(self._dim)]

    def braid_unitary(self, a: object) -> list[list[GaussianRat]]:
        a = self._index(a, 2 * self._modes - 1, "braid index")
        left, right = self.majorana_generator(a + 1), self.majorana_generator(a)
        phase = GaussianRat(Fraction(1, 2), Fraction(1, 2))
        return [[(gi(1 if r == c else 0) + _product_entry(left, right, r, c)) * phase for c in range(self._dim)] for r in range(self._dim)]

    def restrict_to_sector(self, op: object, even: object) -> list[list[GaussianRat]]:
        if type(even) is not bool:
            raise _fail("sector selector must be a built-in boolean")
        matrix = _matrix(op, self._dim)
        _require_parity_preserving(matrix)
        indices = [s for s in range(self._dim) if (s.bit_count() % 2 == 0) == even]
        return [[matrix[r][c] for c in indices] for r in indices]


def _require_parity_preserving(matrix: Sequence) -> None:
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if (row.bit_count() - col.bit_count()) % 2 and not matrix[row][col].is_zero():
                raise _fail("operator mixes parity sectors")
