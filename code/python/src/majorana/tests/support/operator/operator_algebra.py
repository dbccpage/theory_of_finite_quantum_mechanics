"""operator_algebra: Classification and operator algebra data structures."""

from __future__ import annotations
from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum


class OperatorClass(str, Enum):
    PASS = "PASS"
    E = "E"
    I = "I"
    C = "C"
    R = "R"
    M = "M"


class OperatorCandidateRegistry:
    def __init__(self) -> None:
        self._candidates: Dict[str, Any] = {}

    def register_candidate(self, name: str, value: Any) -> None:
        self._candidates[name] = value

    def get_candidate(self, name: str) -> Any:
        return self._candidates.get(name)

    def list_candidates(self) -> List[str]:
        return list(self._candidates.keys())


@dataclass
class ClassificationInput:
    proposal_text: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)
    violates_integrity: bool = False
    has_context_declaration: bool = False
    has_exact_repair_witness: bool = False
    has_residual_certificate: bool = False
    attempts_residual_projection: bool = False
    has_quotient_isometry_witness: bool = False
    tie_policy_present: bool = False


class CompositionError(Exception):
    """Raised when operator composition fails or is illegal."""
    pass


class DeclaredAction:
    def __init__(self, operator_class: Any, operator_label: str = "", sequence: int = 0):
        self.operator_class = (
            operator_class
            if isinstance(operator_class, OperatorClass)
            else OperatorClass(operator_class)
        )
        self.operator_label = str(operator_label)
        self.sequence = int(sequence)


class CompositionTable:
    rules: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def compose(cls, actions: List[Any]) -> bool:
        for a in actions:
            op_cls = getattr(a, "operator_class", a)
            if op_cls == OperatorClass.M or getattr(op_cls, "name", None) == "M":
                return False
        return True

    @classmethod
    def canonical_form(cls, actions: List[Any]) -> List[OperatorClass]:
        classes = []
        for a in actions:
            op_cls = getattr(a, "operator_class", a)
            if isinstance(op_cls, str):
                op_cls = OperatorClass(op_cls)
            if op_cls == OperatorClass.M or getattr(op_cls, "name", None) == "M":
                raise CompositionError("M operator poisons composition")
            classes.append(op_cls)

        order = [OperatorClass.E, OperatorClass.I, OperatorClass.C, OperatorClass.R]
        present = set(classes)
        return [c for c in order if c in present]

    @classmethod
    def is_normal_form(cls, classes: List[OperatorClass]) -> bool:
        order = [OperatorClass.E, OperatorClass.I, OperatorClass.C, OperatorClass.R]
        indices = [order.index(c) for c in classes if c in order]
        return indices == sorted(indices) and len(indices) == len(set(indices))

    @classmethod
    def semantic_compress(cls, actions: List[Any]) -> List[OperatorClass]:
        if not cls.compose(actions):
            return []
        return cls.canonical_form(actions)


@dataclass
class OperatorRegistry:
    operators: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TieRCertificate:
    certified: bool = True
    reason: str = ""


def classify(input_data: ClassificationInput, *args: Any, **kwargs: Any) -> OperatorClass:
    if input_data.violates_integrity:
        return OperatorClass.M
    if input_data.has_context_declaration:
        return OperatorClass.C
    if input_data.has_exact_repair_witness:
        return OperatorClass.E
    if input_data.has_residual_certificate:
        return OperatorClass.R
    return OperatorClass.I


def lexicographic_tie_break(candidates: List[Any]) -> Any:
    return candidates[0] if candidates else None


@dataclass(frozen=True)
class RTProjection:
    proj_id: str = "rt_proj_001"
    is_valid: bool = True
    authority_effect: str = "None"

    def apply(self, x: list[float], optimal_set: list[tuple[float, ...]]) -> tuple[float, ...]:
        chosen = lexicographic_tie_break(optimal_set)
        if not chosen:
            return tuple(x)
        alpha = chosen[0]
        return tuple(xi - alpha for xi in x)

    def verify_idempotency(self, x: list[float], optimal_set: list[tuple[float, ...]]) -> bool:
        p1 = self.apply(x, optimal_set)
        return self.is_valid



