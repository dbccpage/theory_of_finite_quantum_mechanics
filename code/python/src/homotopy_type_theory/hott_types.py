"""Homotopy Type Theory core spine types and Higher Inductive Types (HIT).

Synonym-level path records, contractible types (isContr), and HIT generators.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class HoTTError(Exception):
    """Base error for HoTT shape validation."""
    pass


class MissingReferenceError(HoTTError):
    pass


class InvalidHITError(HoTTError):
    pass


@dataclass(frozen=True)
class Path:
    """Synonym-level path record: path_ref witnesses source = target in type_id."""
    type_id: str
    source: str
    target: str
    path_ref: str

    def validate(self) -> None:
        if not self.type_id or not self.source or not self.target or not self.path_ref:
            raise MissingReferenceError("Path requires non-empty type_id, source, target, and path_ref")


@dataclass(frozen=True)
class ContractibleType:
    """Shape record for isContr(A): center point + contraction family reference."""
    type_ref: str
    center_ref: str
    contraction_ref: str

    def validate(self) -> None:
        if not self.type_ref or not self.center_ref or not self.contraction_ref:
            raise MissingReferenceError("ContractibleType requires non-empty type_ref, center_ref, and contraction_ref")


@dataclass(frozen=True)
class PointConstructor:
    """Point constructor (0-cell generator)."""
    name: str
    doc: str = ""


@dataclass(frozen=True)
class PathConstructor:
    """Path constructor (1-cell or higher generator equality between points/paths)."""
    name: str
    source_point: str
    target_point: str
    dimension: int = 1


@dataclass
class HigherInductiveType:
    """Higher Inductive Type specification."""
    type_name: str
    points: List[PointConstructor] = field(default_factory=list)
    paths: List[PathConstructor] = field(default_factory=list)

    def validate(self) -> None:
        if not self.type_name:
            raise InvalidHITError("HigherInductiveType must have a name")
        point_names = {p.name for p in self.points}
        for path in self.paths:
            if path.source_point not in point_names:
                raise InvalidHITError(f"Path {path.name} source {path.source_point} not in declared points")
            if path.target_point not in point_names:
                raise InvalidHITError(f"Path {path.name} target {path.target_point} not in declared points")
            if path.dimension < 1:
                raise InvalidHITError(f"Path {path.name} must have dimension >= 1")

    @classmethod
    def circle_s1(cls) -> HigherInductiveType:
        """Construct circle S^1: base point + loop path."""
        hit = cls(
            type_name="S^1",
            points=[PointConstructor("base", "Base point of S1")],
            paths=[PathConstructor("loop", "base", "base", dimension=1)],
        )
        hit.validate()
        return hit

    @classmethod
    def interval_i(cls) -> HigherInductiveType:
        """Construct Interval I: zero + one + seg path."""
        hit = cls(
            type_name="Interval",
            points=[
                PointConstructor("zero", "Left endpoint 0"),
                PointConstructor("one", "Right endpoint 1"),
            ],
            paths=[PathConstructor("seg", "zero", "one", dimension=1)],
        )
        hit.validate()
        return hit

    @classmethod
    def torus_t2(cls) -> HigherInductiveType:
        """Construct Torus T^2: base point + 2 1-loops (p, q)."""
        hit = cls(
            type_name="T^2",
            points=[PointConstructor("base", "Base point of T2")],
            paths=[
                PathConstructor("p_loop", "base", "base", dimension=1),
                PathConstructor("q_loop", "base", "base", dimension=1),
            ],
        )
        hit.validate()
        return hit
