"""Finite circle step and higher-inductive shape records.

Origin: lean4/H011Circle.lean theorem cyc3_one_double_ne_zero
((1 : Fin 3) + 1 ≠ 0) and theorem cyc3_meets_connectedness_shadow.
Claim: urn:omega:fqm:hott:circle-step-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/homotopy_type_theory/test_hott_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: circle_step_witness checks that doubling the generator of Z/3Z
is not zero. Path, ContractibleType, and HigherInductiveType are shape
records for S^1, the interval, and the torus presentation. This file does
not prove a univalent universe or a general higher-inductive elimination rule.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


class HoTTError(ValueError):
    """Base failure for homotopy shape records."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class MissingReferenceError(HoTTError):
    """A shape record omitted a required reference."""


class InvalidHITError(HoTTError):
    """A higher-inductive specification names an undeclared point or a bad dimension."""


def _fail(kind: type[HoTTError], invariant: str, **parameters: object) -> HoTTError:
    return kind(invariant, parameters)


def _require_text(value: object, role: str) -> str:
    if isinstance(value, str) and value != "":
        return value
    raise _fail(MissingReferenceError, "reference is empty", role=role, received=type(value).__name__)


def _require_dimension(value: object) -> int:
    if isinstance(value, float):
        raise _fail(InvalidHITError, "float refused where a path dimension was required", received="float")
    if isinstance(value, bool):
        raise _fail(InvalidHITError, "boolean refused where a path dimension was required")
    if not isinstance(value, int):
        raise _fail(InvalidHITError, "path dimension is not an integer", received=type(value).__name__)
    if value < 1:
        raise _fail(InvalidHITError, "path dimension is smaller than 1", dimension=value)
    return value


@dataclass(frozen=True)
class Path:
    """Path record: path_ref witnesses source = target in type_id."""

    type_id: str
    source: str
    target: str
    path_ref: str

    def validate(self) -> None:
        _require_text(self.type_id, "type_id")
        _require_text(self.source, "source")
        _require_text(self.target, "target")
        _require_text(self.path_ref, "path_ref")


@dataclass(frozen=True)
class ContractibleType:
    """Shape record for a center and a contraction reference."""

    type_ref: str
    center_ref: str
    contraction_ref: str

    def validate(self) -> None:
        _require_text(self.type_ref, "type_ref")
        _require_text(self.center_ref, "center_ref")
        _require_text(self.contraction_ref, "contraction_ref")


@dataclass(frozen=True)
class PointConstructor:
    """Point constructor name."""

    name: str
    doc: str = ""


@dataclass(frozen=True)
class PathConstructor:
    """Path constructor between declared points."""

    name: str
    source_point: str
    target_point: str
    dimension: int = 1


@dataclass
class HigherInductiveType:
    """Finite point-and-path specification."""

    type_name: str
    points: list[PointConstructor] = field(default_factory=list)
    paths: list[PathConstructor] = field(default_factory=list)

    def validate(self) -> None:
        _require_text(self.type_name, "type_name")
        names = _point_names(self.points)
        for path in self.paths:
            _validate_path(path, names)

    @classmethod
    def circle_s1(cls) -> HigherInductiveType:
        hit = cls("S^1", [PointConstructor("base", "Base point of S1")], [PathConstructor("loop", "base", "base", 1)])
        hit.validate()
        return hit

    @classmethod
    def interval_i(cls) -> HigherInductiveType:
        hit = cls(
            "Interval",
            [PointConstructor("zero", "Left endpoint 0"), PointConstructor("one", "Right endpoint 1")],
            [PathConstructor("seg", "zero", "one", 1)],
        )
        hit.validate()
        return hit

    @classmethod
    def torus_t2(cls) -> HigherInductiveType:
        hit = cls(
            "T^2",
            [PointConstructor("base", "Base point of T2")],
            [PathConstructor("p_loop", "base", "base", 1), PathConstructor("q_loop", "base", "base", 1)],
        )
        hit.validate()
        return hit


def _point_names(points: list[PointConstructor]) -> set[str]:
    names: set[str] = set()
    for point in points:
        if not isinstance(point, PointConstructor):
            raise _fail(InvalidHITError, "point constructor has the wrong type", received=type(point).__name__)
        name = _require_text(point.name, "point")
        if name in names:
            raise _fail(InvalidHITError, "point name is duplicated", point=name)
        names.add(name)
    return names


def _validate_path(path: PathConstructor, names: set[str]) -> None:
    if not isinstance(path, PathConstructor):
        raise _fail(InvalidHITError, "path constructor has the wrong type", received=type(path).__name__)
    _require_text(path.name, "path")
    if path.source_point not in names:
        raise _fail(InvalidHITError, "path source is not a declared point", path=path.name, source=path.source_point)
    if path.target_point not in names:
        raise _fail(InvalidHITError, "path target is not a declared point", path=path.name, target=path.target_point)
    _require_dimension(path.dimension)


def circle_step_witness() -> int:
    """Return 1 when 1 + 1 is nonzero in Z/3Z."""
    step = (1 + 1) % 3
    if step == 0:
        raise _fail(HoTTError, "circle generator doubled to zero", step=step)
    return 1


def main() -> int:
    """Print the circle-step certificate."""
    try:
        print(circle_step_witness())
    except HoTTError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
