"""Exact relational point-coincidence certificates over the rationals.

Origin: papers/derivations/relational_point_coincidence/relational_point_coincidence_and_witnessed_difference_claim_ledger.md
Claim: urn:omega:fqm:gr003:relational-point-coincidence-certificate:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by papers/derivations/relational_point_coincidence/code/tests/test_relational_spacetime.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 6; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: This file does not derive continuous general relativity or quantum gravity, does not claim scalar fields are universally independent, and does not treat a passing dual witness as an authority grant. The carrier is finite.

CLM-GR003-001 through CLM-GR003-008 are discharged only as exact checks on the rows supplied to this module.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, cast


class RelationalCertificateError(ValueError):
    """One violated relational invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> RelationalCertificateError:
    return RelationalCertificateError(invariant, parameters)


def _refuse_if_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def require_rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float and bool are refused."""
    _refuse_if_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _require_name(value: object, role: str) -> str:
    _refuse_if_float(value, role)
    if type(value) is not str:
        raise _fail("attribute name is not a nonempty string", role=role, received=type(value).__name__)
    if value == "":
        raise _fail("attribute name is not a nonempty string", role=role, received="empty")
    return value


def _iter_names(value: object, role: str) -> Iterable[object]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise _fail("name set is not a collection of attribute names", role=role, received=type(value).__name__)
    return value


def _require_names(value: object, role: str) -> frozenset[str]:
    return frozenset(_require_name(item, role) for item in _iter_names(value, role))


def _event_items(data: object) -> tuple[tuple[str, Fraction], ...]:
    if not isinstance(data, Mapping):
        raise _fail("event is not a mapping", received=type(data).__name__)
    pairs = [
        (_require_name(key, "event attribute"), require_rational(value, "event value"))
        for key, value in data.items()
    ]
    pairs.sort()
    return tuple(pairs)


@dataclass(frozen=True, init=False)
class EventTuple:
    """One witnessed event, stored as sorted exact rational attributes."""

    items: tuple[tuple[str, Fraction], ...]

    def __init__(self, data: object) -> None:
        object.__setattr__(self, "items", _event_items(data))

    def get(self, attr: object) -> Fraction:
        name = _require_name(attr, "attribute")
        for key, value in self.items:
            if key == name:
                return value
        raise _fail("attribute is absent", attribute=name)

    def project(self, attributes: object) -> EventTuple:
        names = _require_names(attributes, "projection")
        kept = {key: value for key, value in self.items if key in names}
        return EventTuple(kept)


def _require_row(row: object, attributes: frozenset[str]) -> EventTuple:
    if not isinstance(row, EventTuple):
        raise _fail("tuple is not an EventTuple", received=type(row).__name__)
    extra = frozenset(key for key, _value in row.items) - attributes
    if len(extra) != 0:
        raise _fail("tuple contains undeclared attributes", missing=tuple(sorted(extra)))
    return row


def _require_rows(tuples: object, attributes: frozenset[str]) -> tuple[EventTuple, ...]:
    if tuples is None:
        return ()
    if isinstance(tuples, (str, bytes)) or not isinstance(tuples, Sequence):
        raise _fail("tuples are not a sequence", received=type(tuples).__name__)
    return tuple(_require_row(row, attributes) for row in tuples)


def _key_values(row: EventTuple, names: frozenset[str]) -> tuple[Fraction, ...]:
    return tuple(row.get(name) for name in sorted(names))


def _fd_row(
    seen: dict[tuple[Fraction, ...], tuple[Fraction, ...]],
    row: EventTuple,
    left: frozenset[str],
    right: frozenset[str],
) -> bool:
    lhs_vals = _key_values(row, left)
    rhs_vals = _key_values(row, right)
    if lhs_vals in seen:
        return seen[lhs_vals] == rhs_vals
    seen[lhs_vals] = rhs_vals
    return True


def _fd_holds(rows: tuple[EventTuple, ...], left: frozenset[str], right: frozenset[str]) -> bool:
    seen: dict[tuple[Fraction, ...], tuple[Fraction, ...]] = {}
    for row in rows:
        if not _fd_row(seen, row, left, right):
            return False
    return True


def _agrees(left: EventTuple, right: EventTuple, common: frozenset[str]) -> bool:
    for name in common:
        if left.get(name) != right.get(name):
            return False
    return True


def _merge(left: EventTuple, right: EventTuple) -> EventTuple:
    merged = dict(left.items)
    merged.update(dict(right.items))
    return EventTuple(merged)


def _join_against(
    left: EventTuple,
    rights: tuple[EventTuple, ...],
    common: frozenset[str],
    rows: list[EventTuple],
) -> None:
    for right in rights:
        if _agrees(left, right, common):
            merged = _merge(left, right)
            if merged not in rows:
                rows.append(merged)


@dataclass(frozen=True, init=False)
class SpacetimeRelation:
    """A finite relation of witnessed events."""

    attributes: frozenset[str]
    tuples: tuple[EventTuple, ...]

    def __init__(self, attributes: object, tuples: object = None) -> None:
        names = _require_names(attributes, "attributes")
        object.__setattr__(self, "attributes", names)
        object.__setattr__(self, "tuples", _require_rows(tuples, names))

    def project(self, attributes: object) -> SpacetimeRelation:
        names = _require_names(attributes, "projection") & self.attributes
        projected = tuple(row.project(names) for row in self.tuples)
        return SpacetimeRelation(set(names), projected)

    def natural_join(self, other: SpacetimeRelation) -> SpacetimeRelation:
        common = self.attributes & other.attributes
        rows: list[EventTuple] = []
        for left in self.tuples:
            _join_against(left, other.tuples, common, rows)
        return SpacetimeRelation(set(self.attributes | other.attributes), rows)

    def check_functional_dependency(self, lhs: object, rhs: object) -> bool:
        left = _require_names(lhs, "lhs")
        right = _require_names(rhs, "rhs")
        return _fd_holds(self.tuples, left, right)

    def is_superkey(self, candidate_key: object) -> bool:
        return self.check_functional_dependency(candidate_key, set(self.attributes))

    def _heath_rebuilds(self, key: frozenset[str], set_a: frozenset[str], set_b: frozenset[str]) -> bool:
        rebuilt = self.project(key | set_a).natural_join(self.project(key | set_b))
        same_rows = set(self.tuples) == set(rebuilt.tuples)
        return same_rows and self.attributes == rebuilt.attributes

    def verify_heaths_theorem(self, key: object, attr_set_a: object, attr_set_b: object) -> bool:
        key_names = _require_names(key, "key")
        set_a = _require_names(attr_set_a, "attr_set_a")
        set_b = _require_names(attr_set_b, "attr_set_b")
        if not self.check_functional_dependency(key_names, set_a):
            return False
        return self._heath_rebuilds(key_names, set_a, set_b)

    def _coordinate_violation(self, forbidden: frozenset[str]) -> str | None:
        present = self.attributes & forbidden
        if len(present) == 0:
            return None
        listed = ", ".join(sorted(present))
        return f"Forbidden coordinate attributes present: {listed}"

    def _width_violation(self, key: frozenset[str]) -> str | None:
        if len(key) != 4:
            return f"Candidate key size {len(key)} != 4"
        return None

    def _superkey_violation(self, key: frozenset[str]) -> str | None:
        if self.is_superkey(key):
            return None
        listed = ", ".join(sorted(key))
        return f"Declared key {listed} does not functionally determine all attributes"

    def check_rpcnf(self, candidate_key: object, forbidden_coordinates: object) -> RpcnfCertificate:
        key = _require_names(candidate_key, "candidate_key")
        forbidden = _require_names(forbidden_coordinates, "forbidden_coordinates")
        violations = (
            self._coordinate_violation(forbidden),
            self._width_violation(key),
            self._superkey_violation(key),
        )
        kept = tuple(item for item in violations if item is not None)
        return RpcnfCertificate(
            len(kept) == 0,
            kept,
            tuple(sorted(key)),
            len(self.attributes),
            len(self.tuples),
        )


@dataclass(frozen=True)
class RpcnfCertificate:
    """RPCNF decision for one finite relation and one declared key."""

    is_rpcnf: bool
    violations: tuple[str, ...]
    candidate_key: tuple[str, ...]
    attribute_count: int
    tuple_count: int


@dataclass(frozen=True)
class DressingFieldProjection:
    """Dressing-field retraction checked only on the states it is given."""

    gauge_action: Callable[[object, object], object]
    dressing_field: Callable[[object], object]

    def dress(self, field_state: object) -> object:
        _refuse_float_value(field_state, "field_state")
        dressed = self.gauge_action(self.dressing_field(field_state), field_state)
        _refuse_float_value(dressed, "dressed")
        return dressed

    def verify_idempotence(self, field_state: object) -> bool:
        dressed_1 = self.dress(field_state)
        dressed_2 = self.dress(dressed_1)
        return dressed_1 == dressed_2

    def verify_gauge_invariance(self, field_state: object, gauge_element: object) -> bool:
        _refuse_float_value(gauge_element, "gauge_element")
        transformed = self.gauge_action(gauge_element, field_state)
        return self.dress(field_state) == self.dress(transformed)


def _refuse_float_value(value: object, role: str) -> None:
    _refuse_if_float(value, role)
    if isinstance(value, tuple):
        _refuse_float_items(value, role)


def _refuse_float_items(values: tuple[object, ...], role: str) -> None:
    for index, item in enumerate(values):
        _refuse_if_float(item, f"{role}[{index}]")


def _as_sequence(values: object, role: str) -> Sequence[object]:
    if isinstance(values, (str, bytes)):
        raise _fail("matrix row is empty or not a vector", role=role)
    if not isinstance(values, Sequence):
        raise _fail("matrix row is empty or not a vector", role=role)
    if len(values) == 0:
        raise _fail("matrix row is empty or not a vector", role=role)
    return cast(Sequence[object], values)


def _parse_row(values: object, role: str, width: int | None) -> tuple[Fraction, ...]:
    parsed = tuple(require_rational(item, role) for item in _as_sequence(values, role))
    if width is not None and len(parsed) != width:
        raise _fail("jagged rational matrix", role=role, expected=width, actual=len(parsed))
    return parsed


def _parse_matrix(values: object, role: str) -> tuple[tuple[Fraction, ...], ...]:
    rows: list[tuple[Fraction, ...]] = []
    width: int | None = None
    for index, row in enumerate(_as_sequence(values, role)):
        parsed = _parse_row(row, f"{role}[{index}]", width)
        width = len(parsed)
        rows.append(parsed)
    return tuple(rows)


def _parse_vector(values: object, role: str, length: int) -> tuple[Fraction, ...]:
    parsed = tuple(require_rational(item, role) for item in _as_sequence(values, role))
    if len(parsed) != length:
        raise _fail("vector length does not match the matrix", role=role, expected=length, actual=len(parsed))
    return parsed


def _transpose_product(matrix: tuple[tuple[Fraction, ...], ...], witness: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    width = len(matrix[0])
    column_sums: list[Fraction] = []
    for column in range(width):
        total = Fraction(0)
        for row_index, row in enumerate(matrix):
            total += row[column] * witness[row_index]
        column_sums.append(total)
    return tuple(column_sums)


def _require_divergence_free(divergence: tuple[Fraction, ...]) -> None:
    for index, value in enumerate(divergence):
        if value != 0:
            raise _fail("dual witness is not divergence-free", index=index, value=str(value))


def _inf_norm(witness: tuple[Fraction, ...]) -> Fraction:
    norm = Fraction(0)
    for value in witness:
        magnitude = abs(value)
        if magnitude > norm:
            norm = magnitude
    return norm


def _require_unit_ball(norm: Fraction) -> Fraction:
    if norm > Fraction(1):
        raise _fail("dual witness violates the unit infinity ball", inf_norm=str(norm))
    return norm


def _pairing(witness: tuple[Fraction, ...], omega: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for left, right in zip(witness, omega, strict=True):
        total += left * right
    return total


def _require_lower_bound(dual_value: Fraction, claimed: Fraction) -> Fraction:
    if dual_value < claimed:
        raise _fail(
            "dual pairing is below the claimed quotient",
            dual_value=str(dual_value),
            claimed=str(claimed),
        )
    return dual_value


@dataclass(frozen=True)
class DualWitnessCertificate:
    """Exact rational lower bound carried by one divergence-free unit witness."""

    dual_value: Fraction
    inf_norm: Fraction
    is_divergence_free: bool
    certified_lower_bound: Fraction


class ExactRationalDualWitness:
    """Verifier for one rational cochain obstruction witness."""

    @staticmethod
    def verify_dual_witness(
        boundary: object,
        omega: object,
        witness: object,
        claimed_quotient: object,
    ) -> DualWitnessCertificate:
        matrix = _parse_matrix(boundary, "boundary")
        length = len(matrix)
        omega_row = _parse_vector(omega, "omega", length)
        witness_row = _parse_vector(witness, "witness", length)
        claimed = require_rational(claimed_quotient, "claimed_quotient")
        divergence = _transpose_product(matrix, witness_row)
        _require_divergence_free(divergence)
        norm = _require_unit_ball(_inf_norm(witness_row))
        dual_value = _require_lower_bound(_pairing(witness_row, omega_row), claimed)
        return DualWitnessCertificate(dual_value, norm, True, dual_value)


__all__ = [
    "DressingFieldProjection",
    "DualWitnessCertificate",
    "EventTuple",
    "ExactRationalDualWitness",
    "RelationalCertificateError",
    "RpcnfCertificate",
    "SpacetimeRelation",
    "require_rational",
]
