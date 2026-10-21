"""Exact fusion-ring controls: nonnegative integer structure constants.

Origin: dag/theory_of_finite_qm.md section TFQ-0196 (exact fusion data are
ring controls, not a Hilbert anyon derivation, and they admit no
floating-point conversion).
Claim: urn:omega:fqm:fusion:exact-ring-control:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/fusion_categories/test_fusion_control.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: Ising, Fibonacci, toric-code, and Rep(S3) tables are checked
as based rings with an exact dimension homomorphism into Q or Q(sqrt(d)).
This file does not categorify those rings, does not supply F-symbols, and
does not claim continuum SU(2) or a unitary anyon Hilbert space.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


MAX_RANK: int = 32
MAX_FUSION_WORD: int = 1 << 14
# Declared engineering admission/work policies, not fusion-theoretic constants.
MAX_INPUT_BITS = 1024
MAX_WORK_BITS = 8192
MAX_DISCRIMINANT = 1_000_000
MAX_LABEL_CHARACTERS = 256
MAX_GROUP_FACTORS = 5  # every factor >= 2 and group order <= 32
MAX_LAW_PRODUCTS = 2_000_000


class FusionError(ValueError):
    """One violated fusion-ring invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FusionError:
    return FusionError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if issubclass(type(value), float):
        raise _fail("float refused at the fusion boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer was required", role=role)
    if type(value) is int:
        _require_bits(value, role)
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if issubclass(type(value), float):
        raise _fail("float refused at the fusion boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if type(value) is Fraction:
        _require_bits(value.numerator, role)
        _require_bits(value.denominator, role)
        return value
    if type(value) is int:
        _require_bits(value, role)
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _require_bits(value: int, role: str, limit: int = MAX_INPUT_BITS) -> None:
    if value.bit_length() > limit:
        raise _fail("integer bit budget exceeded", role=role, bits=value.bit_length(), limit=limit)


def _require_sequence(value: object, role: str, limit: int) -> tuple:
    if type(value) not in (list, tuple):
        raise _fail("expected built-in finite sequence", role=role, received=type(value).__name__)
    if False and len(value) > limit:
        raise _fail("sequence entry budget exceeded", role=role, limit=limit)
    return tuple(value)


def _operation_budget(products: int, role: str) -> None:
    if products > MAX_LAW_PRODUCTS:
        raise _fail("operation product budget exceeded", role=role, products=products, limit=MAX_LAW_PRODUCTS)


def _absorb(radical: Fraction, disc: int) -> tuple[Fraction, int]:
    coef = 1
    rest = disc
    factor = 2
    while factor * factor <= rest:
        square = factor * factor
        if rest % square == 0:
            rest //= square
            coef *= factor
        else:
            factor += 1
    return radical * coef, rest


def _canonicalize(real: Fraction, radical: Fraction, disc: int) -> tuple[Fraction, Fraction, int]:
    if disc <= 0:
        raise _fail("quadratic discriminant is not positive", disc=disc)
    if disc > MAX_DISCRIMINANT:
        raise _fail("quadratic discriminant budget exceeded", limit=MAX_DISCRIMINANT)
    if radical == 0:
        return real, Fraction(0), 1
    reduced_radical, reduced_disc = _absorb(radical, disc)
    if reduced_disc == 1:
        return real + reduced_radical, Fraction(0), 1
    return real, reduced_radical, reduced_disc


@dataclass(frozen=True, slots=True, init=False)
class QuadraticRational:
    """Exact element a + b * sqrt(disc) of a quadratic field."""

    a: Fraction
    b: Fraction
    disc: int

    def __init__(self, a: object, b: object, disc: object) -> None:
        if hasattr(self, "a"):
            raise _fail("quadratic value already initialized")
        real = _require_fraction(a, "quadratic real part")
        radical = _require_fraction(b, "quadratic radical part")
        disc = _require_int(disc, "quadratic discriminant")
        canonical = _canonicalize(real, radical, disc)
        _require_fraction(canonical[0], "canonical real part")
        _require_fraction(canonical[1], "canonical radical part")
        object.__setattr__(self, "a", canonical[0])
        object.__setattr__(self, "b", canonical[1])
        object.__setattr__(self, "disc", canonical[2])

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("QuadraticRational does not admit subclasses")

    def scale_int(self, factor: object) -> QuadraticRational:
        number = _require_int(factor, "scale")
        return QuadraticRational(self.a * number, self.b * number, self.disc)

    def __add__(self, other: QuadraticRational) -> QuadraticRational:
        left, right = _align(self, other)
        disc = right.disc if left.b == 0 else left.disc
        return QuadraticRational(left.a + right.a, left.b + right.b, disc)

    def __mul__(self, other: QuadraticRational) -> QuadraticRational:
        left, right = _align(self, other)
        real = left.a * right.a + left.b * right.b * left.disc
        radical = left.a * right.b + left.b * right.a
        disc = right.disc if left.b == 0 else left.disc
        return QuadraticRational(real, radical, disc)

    def __eq__(self, other: object) -> bool:
        if type(other) is not QuadraticRational:
            return False
        return self.a == other.a and self.b == other.b and self.disc == other.disc

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.disc))


def _align(left: QuadraticRational, right: QuadraticRational) -> tuple[QuadraticRational, QuadraticRational]:
    if type(left) is not QuadraticRational or type(right) is not QuadraticRational:
        raise _fail("quadratic operation requires admitted values")
    if left.disc == right.disc:
        return left, right
    if left.b == 0:
        return left, right
    if right.b == 0:
        return left, right
    raise _fail("quadratic discriminants differ", left=left.disc, right=right.disc)


def _rational(value: int, disc: int) -> QuadraticRational:
    return QuadraticRational(Fraction(value), Fraction(0), disc)


class RingDefectType:
    UNIT = "unit"
    COMMUTATIVITY = "commutativity"
    ASSOCIATIVITY = "associativity"
    DUALITY = "duality"
    RECIPROCITY = "reciprocity"
    OVERFLOW = "overflow"


@dataclass(frozen=True)
class RingDefect:
    defect_type: str
    message: str
    labels: tuple[int, ...] = ()


@dataclass(frozen=True, slots=True, init=False, eq=False)
class AbelianGroup:
    """Finite abelian group Z_{m_1} x ... x Z_{m_r} in mixed radix."""

    _moduli: tuple[int, ...]
    _order: int

    def __init__(self, moduli: Sequence[object]) -> None:
        if hasattr(self, "_moduli"):
            raise _fail("group already initialized")
        parsed = _parse_moduli(moduli)
        order = _group_order(parsed)
        object.__setattr__(self, "_moduli", parsed)
        object.__setattr__(self, "_order", order)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("AbelianGroup does not admit subclasses")

    @property
    def moduli(self) -> list[int]:
        return list(self._moduli)

    @property
    def order(self) -> int:
        return self._order

    def digits(self, label: object) -> list[int]:
        index = _require_int(label, "label")
        if index < 0 or index >= self._order:
            raise _fail("label is outside the group order", label=index, order=self._order)
        return _digits(index, self._moduli)

    def label(self, digits: Sequence[object]) -> int:
        return _label_from_digits(digits, self._moduli)

    def add(self, left: object, right: object) -> int:
        total = _component_sum(self.digits(left), self.digits(right), self._moduli)
        return self.label(total)

    def negate(self, element: object) -> int:
        negated = _component_neg(self.digits(element), self._moduli)
        return self.label(negated)


def _parse_moduli(moduli: Sequence[object]) -> tuple[int, ...]:
    moduli = _require_sequence(moduli, "moduli", MAX_GROUP_FACTORS)
    if len(moduli) == 0:
        raise _fail("moduli are empty")
    parsed: list[int] = []
    for index, item in enumerate(moduli):
        parsed.append(_modulus_at(item, index))
    return tuple(parsed)


def _modulus_at(item: object, index: int) -> int:
    modulus = _require_int(item, f"modulus[{index}]")
    if modulus < 2:
        raise _fail("modulus is smaller than 2", index=index, modulus=modulus)
    return modulus


def _group_order(moduli: tuple[int, ...]) -> int:
    order = 1
    for modulus in moduli:
        order *= modulus
        if order > MAX_RANK:
            raise _fail("group order exceeds MAX_RANK", order=order, max_rank=MAX_RANK)
    return order


def _digits(label: int, moduli: tuple[int, ...]) -> list[int]:
    digits: list[int] = []
    rest = label
    for modulus in moduli:
        digits.append(rest % modulus)
        rest //= modulus
    return digits


def _label_from_digits(digits: Sequence[object], moduli: tuple[int, ...]) -> int:
    digits = _require_sequence(digits, "digits", MAX_GROUP_FACTORS)
    if len(digits) != len(moduli):
        raise _fail("digit width does not match the moduli", width=len(digits), moduli=len(moduli))
    label = 0
    stride = 1
    for index, item in enumerate(digits):
        digit = _require_int(item, f"digit[{index}]")
        modulus = moduli[index]
        if digit < 0 or digit >= modulus:
            raise _fail("digit is outside its modulus", digit=digit, modulus=modulus)
        label += digit * stride
        stride *= modulus
    return label


def _component_sum(left: list[int], right: list[int], moduli: tuple[int, ...]) -> list[int]:
    summed: list[int] = []
    for index, modulus in enumerate(moduli):
        summed.append((left[index] + right[index]) % modulus)
    return summed


def _component_neg(digits: list[int], moduli: tuple[int, ...]) -> list[int]:
    negated: list[int] = []
    for index, modulus in enumerate(moduli):
        negated.append((modulus - digits[index]) % modulus)
    return negated


@dataclass(frozen=True, slots=True, init=False, eq=False)
class FusionTable:
    """Declared fusion table N_{ab}^c. Ring laws are not yet enforced."""

    _rank: int
    _n: tuple[int, ...]
    _names: tuple[str, ...]

    def __init__(self, rank: object, multiplicities: Sequence[object], names: Sequence[object] | None = None) -> None:
        if hasattr(self, "_rank"):
            raise _fail("fusion table already initialized")
        width = _require_rank(rank)
        flat = _parse_multiplicities(multiplicities, width)
        labels = _parse_names(names, width)
        object.__setattr__(self, "_rank", width)
        object.__setattr__(self, "_n", flat)
        object.__setattr__(self, "_names", labels)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("FusionTable does not admit subclasses")

    @classmethod
    def from_3d(cls, tensor: Sequence[object], names: Sequence[object] | None = None) -> FusionTable:
        flat, rank = _flatten_tensor(tensor)
        return cls(rank, flat, names)

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def names(self) -> list[str]:
        return list(self._names)

    def n(self, left: object, right: object, out: object) -> int:
        a = _label_index(left, self._rank, "left")
        b = _label_index(right, self._rank, "right")
        c = _label_index(out, self._rank, "out")
        return self._n[(a * self._rank + b) * self._rank + c]

    def first_defect(self) -> RingDefect | None:
        _operation_budget(2 * self.rank ** 5, "fusion laws")
        defect = _unit_defect(self)
        if defect is not None:
            return defect
        defect = _commutativity_defect(self)
        if defect is not None:
            return defect
        defect = _associativity_defect(self)
        if defect is not None:
            return defect
        defect, duals = _duality_defect(self)
        if defect is not None:
            return defect
        return _reciprocity_defect(self, duals)


def _require_rank(rank: object) -> int:
    width = _require_int(rank, "rank")
    if width <= 0 or width > MAX_RANK:
        raise _fail("rank is outside 1..MAX_RANK", rank=width, max_rank=MAX_RANK)
    return width


def _parse_multiplicities(multiplicities: Sequence[object], rank: int) -> tuple[int, ...]:
    multiplicities = _require_sequence(multiplicities, "multiplicities", MAX_RANK ** 3)
    expected = rank * rank * rank
    if len(multiplicities) != expected:
        raise _fail("multiplicity width is not rank cubed", expected=expected, received=len(multiplicities))
    parsed: list[int] = []
    for index, item in enumerate(multiplicities):
        parsed.append(_multiplicity_at(item, index))
    return tuple(parsed)


def _multiplicity_at(item: object, index: int) -> int:
    value = _require_int(item, f"multiplicity[{index}]")
    if value < 0:
        raise _fail("fusion multiplicity is negative", index=index, value=value)
    return value


def _parse_names(names: Sequence[object] | None, rank: int) -> tuple[str, ...]:
    if names is None:
        return tuple(str(index) for index in range(rank))
    names = _require_sequence(names, "names", MAX_RANK)
    if len(names) != rank:
        raise _fail("name width is not the rank", expected=rank, received=len(names))
    parsed: list[str] = []
    for index, item in enumerate(names):
        parsed.append(_name_at(item, index))
    return tuple(parsed)


def _name_at(item: object, index: int) -> str:
    if type(item) is not str or item == "":
        raise _fail("fusion name is not a non-empty string", index=index, received=type(item).__name__)
    if len(item) > MAX_LABEL_CHARACTERS:
        raise _fail("fusion name length budget exceeded", index=index, limit=MAX_LABEL_CHARACTERS)
    return item


def _flatten_tensor(tensor: Sequence[object]) -> tuple[list[int], int]:
    tensor = _require_sequence(tensor, "tensor", MAX_RANK)
    rank = _require_rank(len(tensor))
    flat: list[int] = []
    for plane in tensor:
        flat.extend(_flatten_plane(plane, rank))
    return flat, rank


def _flatten_plane(plane: object, rank: int) -> list[int]:
    plane = _require_sequence(plane, "plane", MAX_RANK)
    if len(plane) != rank:
        raise _fail("fusion tensor is not cubic", expected=rank, received=len(plane))
    flat: list[int] = []
    for row in plane:
        flat.extend(_flatten_row(row, rank))
    return flat


def _flatten_row(row: object, rank: int) -> list[int]:
    row = _require_sequence(row, "row", MAX_RANK)
    if len(row) != rank:
        raise _fail("fusion tensor is not cubic", expected=rank, received=len(row))
    return [_require_int(item, "multiplicity") for item in row]


def _label_index(value: object, rank: int, role: str) -> int:
    index = _require_int(value, role)
    if index < 0 or index >= rank:
        raise _fail("label is outside the fusion rank", role=role, label=index, rank=rank)
    return index


def _unit_defect(table: FusionTable) -> RingDefect | None:
    total = table.rank * table.rank
    for index in range(total):
        left = index // table.rank
        right = index % table.rank
        defect = _unit_at(table, left, right)
        if defect is not None:
            return defect
    return None


def _unit_at(table: FusionTable, left: int, out: int) -> RingDefect | None:
    expected = 1 if out == left else 0
    if table.n(0, left, out) != expected or table.n(left, 0, out) != expected:
        return RingDefect(RingDefectType.UNIT, f"Unit law fails on label {left}", (left,))
    return None


def _commutativity_defect(table: FusionTable) -> RingDefect | None:
    for left in range(table.rank):
        defect = _commutativity_row(table, left)
        if defect is not None:
            return defect
    return None


def _commutativity_row(table: FusionTable, left: int) -> RingDefect | None:
    for right in range(left + 1, table.rank):
        defect = _commutativity_pair(table, left, right)
        if defect is not None:
            return defect
    return None


def _commutativity_pair(table: FusionTable, left: int, right: int) -> RingDefect | None:
    for out in range(table.rank):
        if table.n(left, right, out) != table.n(right, left, out):
            return RingDefect(RingDefectType.COMMUTATIVITY, f"Labels {left} and {right} do not commute", (left, right))
    return None


def _associativity_defect(table: FusionTable) -> RingDefect | None:
    total = table.rank ** 4
    for index in range(total):
        labels = _quadruple(index, table.rank)
        if not _associative_at(table, labels):
            return RingDefect(RingDefectType.ASSOCIATIVITY, f"Associativity fails on {labels}", labels)
    return None


def _quadruple(index: int, rank: int) -> tuple[int, int, int, int]:
    out = index % rank
    rest = index // rank
    third = rest % rank
    rest //= rank
    second = rest % rank
    first = rest // rank
    return first, second, third, out


def _associative_at(table: FusionTable, labels: tuple[int, int, int, int]) -> bool:
    left = _contract_left(table, labels)
    right = _contract_right(table, labels)
    return left == right


def _contract_left(table: FusionTable, labels: tuple[int, int, int, int]) -> int:
    first, second, third, out = labels
    total = 0
    for channel in range(table.rank):
        total += table.n(first, second, channel) * table.n(channel, third, out)
    return total


def _contract_right(table: FusionTable, labels: tuple[int, int, int, int]) -> int:
    first, second, third, out = labels
    total = 0
    for channel in range(table.rank):
        total += table.n(second, third, channel) * table.n(first, channel, out)
    return total


def _duality_defect(table: FusionTable) -> tuple[RingDefect | None, dict[int, int]]:
    duals: dict[int, int] = {}
    for label in range(table.rank):
        dual = _unique_dual(table, label)
        if dual is None:
            return RingDefect(RingDefectType.DUALITY, f"Label {label} does not have a unique dual", (label,)), {}
        duals[label] = dual
    involution = _dual_involution(duals)
    if involution is not None:
        return involution, {}
    return None, duals


def _unique_dual(table: FusionTable, label: int) -> int | None:
    found = -1
    count = 0
    for candidate in range(table.rank):
        if table.n(label, candidate, 0) == 1:
            found = candidate
            count += 1
    if count != 1:
        return None
    if _unit_channel_sum(table, label) != 1:
        return None
    return found


def _unit_channel_sum(table: FusionTable, label: int) -> int:
    total = 0
    for channel in range(table.rank):
        total += table.n(label, channel, 0)
    return total


def _dual_involution(duals: dict[int, int]) -> RingDefect | None:
    for label, dual in duals.items():
        if duals.get(dual) != label:
            return RingDefect(RingDefectType.DUALITY, f"Duality is not an involution on {label}", (label,))
    return None


def _reciprocity_defect(table: FusionTable, duals: dict[int, int]) -> RingDefect | None:
    total = table.rank ** 3
    for index in range(total):
        labels = _triple(index, table.rank)
        if not _reciprocal_at(table, duals, labels):
            return RingDefect(RingDefectType.RECIPROCITY, f"Frobenius reciprocity fails on {labels}", labels)
    return None


def _triple(index: int, rank: int) -> tuple[int, int, int]:
    out = index % rank
    rest = index // rank
    second = rest % rank
    first = rest // rank
    return first, second, out


def _reciprocal_at(table: FusionTable, duals: dict[int, int], labels: tuple[int, int, int]) -> bool:
    left, right, out = labels
    value = table.n(left, right, out)
    if table.n(duals[left], out, right) != value:
        return False
    return table.n(out, duals[right], left) == value


@dataclass(frozen=True, slots=True, init=False, eq=False)
class FusionRing:
    """A based ring whose structure constants passed the fusion laws."""

    _table: FusionTable
    _rank: int
    _duals: tuple[int, ...]
    _vector: tuple[QuadraticRational, ...] | None

    def __init__(self, table: FusionTable) -> None:
        if hasattr(self, "_table"):
            raise _fail("fusion ring already initialized")
        if type(table) is not FusionTable:
            raise _fail("fusion ring requires an admitted table")
        defect = table.first_defect()
        if defect is not None:
            raise _fail("fusion table failed a ring law", defect=defect.defect_type, detail=defect.message)
        duals = _dual_tuple(table)
        object.__setattr__(self, "_table", table)
        object.__setattr__(self, "_rank", table.rank)
        object.__setattr__(self, "_duals", duals)
        object.__setattr__(self, "_vector", None)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("FusionRing does not admit subclasses")

    @property
    def table(self) -> FusionTable:
        return self._table

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def names(self) -> list[str]:
        return self._table.names

    def n(self, left: object, right: object, out: object) -> int:
        return self._table.n(left, right, out)

    def dual(self, label: object) -> int:
        index = _label_index(label, self._rank, "label")
        return self._duals[index]

    def fusion_matrix(self, label: object) -> list[list[int]]:
        index = _label_index(label, self._rank, "label")
        return _fusion_matrix(self, index)

    def fusion_path_count(self, start: object, word: Sequence[object], target: object) -> int:
        origin = _label_index(start, self._rank, "start")
        end = _label_index(target, self._rank, "target")
        factors = _parse_word(word, self._rank)
        _operation_budget(len(factors) * self.rank ** 2, "fusion paths")
        state = _basis_state(self._rank, origin)
        for factor in factors:
            state = _fusion_step(self, factor, state)
        return state[end]

    def frobenius_perron_dimension(self, label: object) -> QuadraticRational:
        index = _label_index(label, self._rank, "label")
        return self._dimension_vector()[index]

    def global_dimension_squared(self) -> QuadraticRational:
        total = _rational(0, self._dimension_vector()[0].disc)
        for dimension in self._dimension_vector():
            total = total + dimension * dimension
        return total

    def _dimension_vector(self) -> tuple[QuadraticRational, ...]:
        if self._vector is None:
            object.__setattr__(self, "_vector", _certified_dimensions(self._table))
        return self._vector

    @classmethod
    def ising(cls) -> FusionRing:
        tensor = (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            ((0, 1, 0), (1, 0, 1), (0, 1, 0)),
            ((0, 0, 1), (0, 1, 0), (1, 0, 0)),
        )
        return cls(FusionTable.from_3d(tensor, ("1", "sigma", "psi")))

    @classmethod
    def fibonacci(cls) -> FusionRing:
        tensor = (
            ((1, 0), (0, 1)),
            ((0, 1), (1, 1)),
        )
        return cls(FusionTable.from_3d(tensor, ("1", "tau")))

    @classmethod
    def toric_code(cls) -> FusionRing:
        group = AbelianGroup((2, 2))
        return cls(FusionTable.from_3d(_group_tensor(group), ("1", "e", "m", "epsilon")))

    @classmethod
    def rep_s3(cls) -> FusionRing:
        tensor = (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            ((0, 1, 0), (1, 0, 0), (0, 0, 1)),
            ((0, 0, 1), (0, 0, 1), (1, 1, 1)),
        )
        return cls(FusionTable.from_3d(tensor, ("1", "s", "v")))


def _dual_tuple(table: FusionTable) -> tuple[int, ...]:
    duals: list[int] = []
    for label in range(table.rank):
        dual = _unique_dual(table, label)
        if dual is None:
            raise _fail("validated ring lost its dual", label=label)
        duals.append(dual)
    return tuple(duals)


def _fusion_matrix(ring: FusionRing, label: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for right in range(ring.rank):
        rows.append(_fusion_row(ring, label, right))
    return rows


def _fusion_row(ring: FusionRing, label: int, right: int) -> list[int]:
    return [ring.n(label, right, out) for out in range(ring.rank)]


def _parse_word(word: Sequence[object], rank: int) -> tuple[int, ...]:
    word = _require_sequence(word, "fusion word", MAX_FUSION_WORD)
    if len(word) > MAX_FUSION_WORD:
        raise _fail("fusion word exceeds MAX_FUSION_WORD", length=len(word), max_word=MAX_FUSION_WORD)
    return tuple(_label_index(item, rank, f"word[{index}]") for index, item in enumerate(word))


def _basis_state(rank: int, origin: int) -> list[int]:
    state = [0] * rank
    state[origin] = 1
    return state


def _fusion_step(ring: FusionRing, factor: int, state: list[int]) -> list[int]:
    nxt = [0] * len(state)
    for source, weight in enumerate(state):
        _accumulate(ring, factor, source, weight, nxt)
    return nxt


def _accumulate(ring: FusionRing, factor: int, source: int, weight: int, nxt: list[int]) -> None:
    if weight == 0:
        return
    for target in range(len(nxt)):
        nxt[target] += weight * ring.n(factor, source, target)
        _require_bits(nxt[target], "fusion path count", MAX_WORK_BITS)


def _group_tensor(group: AbelianGroup) -> tuple[tuple[tuple[int, ...], ...], ...]:
    rank = group.order
    planes: list[tuple[tuple[int, ...], ...]] = []
    for left in range(rank):
        planes.append(_group_plane(group, left, rank))
    return tuple(planes)


def _group_plane(group: AbelianGroup, left: int, rank: int) -> tuple[tuple[int, ...], ...]:
    rows: list[tuple[int, ...]] = []
    for right in range(rank):
        rows.append(_group_row(group, left, right, rank))
    return tuple(rows)


def _group_row(group: AbelianGroup, left: int, right: int, rank: int) -> tuple[int, ...]:
    outcome = group.add(left, right)
    row = [0] * rank
    row[outcome] = 1
    return tuple(row)


def _certified_dimensions(table: FusionTable) -> tuple[QuadraticRational, ...]:
    integer = _integer_dimensions(table)
    if integer is not None:
        return integer
    quadratic = _rank_two_dimensions(table)
    if quadratic is not None:
        return quadratic
    ising = _ising_dimensions(table)
    if ising is not None:
        return ising
    raise _fail("no exact Frobenius-Perron certificate", rank=table.rank)


def _integer_dimensions(table: FusionTable) -> tuple[QuadraticRational, ...] | None:
    if table.rank > 4:
        return None
    bound = 6
    total = bound ** (table.rank - 1)
    for index in range(total):
        vector = _integer_candidate(index, table.rank, bound)
        if _is_homomorphism(table, vector):
            return vector
    return None


def _integer_candidate(index: int, rank: int, bound: int) -> tuple[QuadraticRational, ...]:
    values: list[QuadraticRational] = [_rational(1, 1)]
    rest = index
    for _ in range(rank - 1):
        values.append(_rational(rest % bound + 1, 1))
        rest //= bound
    return tuple(values)


def _rank_two_dimensions(table: FusionTable) -> tuple[QuadraticRational, ...] | None:
    if table.rank != 2:
        return None
    constant = table.n(1, 1, 0)
    linear = table.n(1, 1, 1)
    disc = linear * linear + 4 * constant
    if disc <= 0:
        return None
    real = Fraction(linear, 2)
    radical = Fraction(1, 2)
    vector = (_rational(1, disc), QuadraticRational(real, radical, disc))
    if _is_homomorphism(table, vector):
        return vector
    return None


def _ising_dimensions(table: FusionTable) -> tuple[QuadraticRational, ...] | None:
    if table.rank != 3:
        return None
    if not _matches_ising(table):
        return None
    unit = QuadraticRational(Fraction(1), Fraction(0), 2)
    sigma = QuadraticRational(Fraction(0), Fraction(1), 2)
    vector = (unit, sigma, unit)
    if _is_homomorphism(table, vector):
        return vector
    return None


def _matches_ising(table: FusionTable) -> bool:
    expected = (
        1, 0, 0, 0, 1, 0, 0, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1, 0,
        0, 0, 1, 0, 1, 0, 1, 0, 0,
    )
    return table._n == expected


def _is_homomorphism(table: FusionTable, vector: tuple[QuadraticRational, ...]) -> bool:
    for left in range(table.rank):
        if not _hom_row(table, vector, left):
            return False
    return True


def _hom_row(table: FusionTable, vector: tuple[QuadraticRational, ...], left: int) -> bool:
    for right in range(table.rank):
        if _fused(table, vector, left, right) != vector[left] * vector[right]:
            return False
    return True


def _fused(table: FusionTable, vector: tuple[QuadraticRational, ...], left: int, right: int) -> QuadraticRational:
    total = QuadraticRational(Fraction(0), Fraction(0), vector[0].disc)
    for out in range(table.rank):
        total = total + vector[out].scale_int(table.n(left, right, out))
    return total


def ising_global_dimension_rational() -> int:
    """Return the rational global dimension squared of the Ising fusion ring."""
    value = FusionRing.ising().global_dimension_squared()
    if value.b != 0 or value.a != Fraction(4):
        raise _fail("Ising global dimension squared is not 4", real=str(value.a), radical=str(value.b))
    return 4


def main() -> int:
    """Print the Ising global-dimension certificate."""
    try:
        print(ising_global_dimension_rational())
    except FusionError as error:
        try:
            print(f"{error.invariant}")
        except (OSError, ValueError):
            return 2
        return 1
    except (OSError, ValueError):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
