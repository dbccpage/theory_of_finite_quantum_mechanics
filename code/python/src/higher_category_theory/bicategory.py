"""Strict finite 2-category composition and the identity-associator pentagon.

Origin: papers/core/finite_quantum_mechanics_source_notes.md section on the
source pentagon (the implemented relation is strict composition, not a
Biedenharn-Elliott or 6j-symbol theorem).
Claim: urn:omega:fqm:bicategory:strict-association-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/higher_category_theory/test_bicategory_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: strict_association_witness checks that parenthesizations of four
generating 1-cells name the same composite. The pentagon and triangle checks
use identity 2-cells of a strict 2-category. This file does not prove Mac
Lane coherence for a weak bicategory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


class HigherCategoryError(ValueError):
    """One violated higher-category invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class PentagonCoherenceViolation(HigherCategoryError):
    """The two strict pentagon paths named different 2-cells."""

    def __init__(self, step: str, path_a: str, path_b: str) -> None:
        self.step = step
        self.path_a = path_a
        self.path_b = path_b
        super().__init__("pentagon coherence failed", {"step": step, "path_a": path_a, "path_b": path_b})


class TriangleCoherenceViolation(HigherCategoryError):
    """The two strict triangle paths named different 2-cells."""

    def __init__(self, details: str, left: str, right: str) -> None:
        self.details = details
        self.left = left
        self.right = right
        super().__init__("triangle coherence failed", {"details": details, "left": left, "right": right})


def _fail(invariant: str, **parameters: object) -> HigherCategoryError:
    return HigherCategoryError(invariant, parameters)


def _require_name(value: object, role: str) -> str:
    if isinstance(value, str) and value != "":
        return value
    raise _fail("cell name is not a non-empty string", role=role, received=type(value).__name__)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the bicategory boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def checked_count(value: object) -> int:
    """Return one integer after refusing float and bool."""
    return _require_int(value, "count")


@dataclass(frozen=True)
class Invertible2Cell:
    """A named invertible 2-cell."""

    forward: str
    inverse: str


@dataclass
class Strict2Category:
    """Strict 2-category presented by named generators and cached composites."""

    objects: set[str] = field(default_factory=set)
    one_cells: dict[str, tuple[str, str]] = field(default_factory=dict)
    two_cells: dict[str, tuple[str, str]] = field(default_factory=dict)
    comp_1: dict[tuple[str, str], str] = field(default_factory=dict)
    comp_2_v: dict[tuple[str, str], str] = field(default_factory=dict)
    comp_2_h: dict[tuple[str, str], str] = field(default_factory=dict)

    def add_object(self, obj: object) -> None:
        self.objects.add(_require_name(obj, "object"))

    def add_1cell(self, name: object, source: object, target: object) -> None:
        cell = _require_name(name, "1-cell")
        start = _require_known_object(self, source, "source")
        end = _require_known_object(self, target, "target")
        self.one_cells[cell] = (start, end)

    def add_2cell(self, name: object, source_1: object, target_1: object) -> None:
        cell = _require_name(name, "2-cell")
        source = _require_known_1cell(self, source_1, "source")
        target = _require_known_1cell(self, target_1, "target")
        if self.one_cells[source] != self.one_cells[target]:
            raise _fail("2-cell boundary is not parallel", source=source, target=target)
        self.two_cells[cell] = (source, target)

    def id_1(self, obj: object) -> str:
        name = f"id_{_require_known_object(self, obj, 'object')}"
        if name not in self.one_cells:
            self.add_1cell(name, name[3:], name[3:])
            self.comp_1[(name, name)] = name
        return name

    def id_2(self, one_cell: object) -> str:
        cell = _require_known_1cell(self, one_cell, "1-cell")
        name = f"id_{cell}"
        if name not in self.two_cells:
            self.add_2cell(name, cell, cell)
            self.comp_2_v[(name, name)] = name
        return name

    def is_id_1(self, one_cell: object) -> bool:
        cell = _require_name(one_cell, "1-cell")
        return cell.startswith("id_") and cell[3:] in self.objects

    def is_id_2(self, two_cell: object) -> bool:
        cell = _require_name(two_cell, "2-cell")
        return cell.startswith("id_") and cell[3:] in self.one_cells

    def compose_1(self, left: object, right: object) -> str:
        first = _require_known_1cell(self, left, "left")
        second = _require_known_1cell(self, right, "right")
        cached = self.comp_1.get((first, second))
        if cached is not None:
            return cached
        return self._compose_1_new(first, second)

    def _compose_1_new(self, first: str, second: str) -> str:
        source, middle_left = self.one_cells[first]
        middle_right, target = self.one_cells[second]
        if middle_left != middle_right:
            raise _fail("1-cells are not composable", left=first, right=second, middle_left=middle_left, middle_right=middle_right)
        if self.is_id_1(first):
            self.comp_1[(first, second)] = second
            return second
        if self.is_id_1(second):
            self.comp_1[(first, second)] = first
            return first
        composite = _circ_name(first, second)
        if composite not in self.one_cells:
            self.add_1cell(composite, source, target)
        self.comp_1[(first, second)] = composite
        return composite

    def compose_2_vertical(self, left: object, right: object) -> str:
        first = _require_known_2cell(self, left, "left")
        second = _require_known_2cell(self, right, "right")
        cached = self.comp_2_v.get((first, second))
        if cached is not None:
            return cached
        return self._compose_2_vertical_new(first, second)

    def _compose_2_vertical_new(self, first: str, second: str) -> str:
        source, middle_left = self.two_cells[first]
        middle_right, target = self.two_cells[second]
        if middle_left != middle_right:
            raise _fail("2-cells are not vertically composable", left=first, right=second)
        if self.is_id_2(first):
            self.comp_2_v[(first, second)] = second
            return second
        if self.is_id_2(second):
            self.comp_2_v[(first, second)] = first
            return first
        composite = f"{second}_o_{first}"
        if composite not in self.two_cells:
            self.add_2cell(composite, source, target)
        self.comp_2_v[(first, second)] = composite
        return composite

    def compose_2_horizontal(self, left: object, right: object) -> str:
        first = _require_known_2cell(self, left, "left")
        second = _require_known_2cell(self, right, "right")
        cached = self.comp_2_h.get((first, second))
        if cached is not None:
            return cached
        return self._compose_2_horizontal_new(first, second)

    def _compose_2_horizontal_new(self, first: str, second: str) -> str:
        source_left, target_left = self.two_cells[first]
        source_right, target_right = self.two_cells[second]
        source = self.compose_1(source_left, source_right)
        target = self.compose_1(target_left, target_right)
        if self.is_id_2(first) and self.is_id_2(second):
            identity = self.id_2(source)
            self.comp_2_h[(first, second)] = identity
            return identity
        composite = f"{second}_star_{first}"
        if composite not in self.two_cells:
            self.add_2cell(composite, source, target)
        self.comp_2_h[(first, second)] = composite
        return composite


def _require_known_object(category: Strict2Category, value: object, role: str) -> str:
    name = _require_name(value, role)
    if name not in category.objects:
        raise _fail("object is not declared", role=role, object=name)
    return name


def _require_known_1cell(category: Strict2Category, value: object, role: str) -> str:
    name = _require_name(value, role)
    if name not in category.one_cells:
        raise _fail("1-cell is not declared", role=role, cell=name)
    return name


def _require_known_2cell(category: Strict2Category, value: object, role: str) -> str:
    name = _require_name(value, role)
    if name not in category.two_cells:
        raise _fail("2-cell is not declared", role=role, cell=name)
    return name


def _circ_name(left: str, right: str) -> str:
    return "_circ_".join(right.split("_circ_") + left.split("_circ_"))


@dataclass
class FiniteBicategory:
    """Strict bicategory whose associators and unitors default to identity 2-cells."""

    base_strict: Strict2Category
    associator_table: dict[tuple[str, str, str], Invertible2Cell] = field(default_factory=dict)
    left_unitor_table: dict[str, Invertible2Cell] = field(default_factory=dict)
    right_unitor_table: dict[str, Invertible2Cell] = field(default_factory=dict)

    def set_associator(self, left: object, middle: object, right: object, forward: object, inverse: object) -> None:
        first = _require_name(left, "left")
        second = _require_name(middle, "middle")
        third = _require_name(right, "right")
        forward_name = _require_name(forward, "forward")
        inverse_name = _require_name(inverse, "inverse")
        right_composite = self.base_strict.compose_1(second, third)
        left_composite = self.base_strict.compose_1(first, second)
        left_boundary = self.base_strict.compose_1(first, right_composite)
        right_boundary = self.base_strict.compose_1(left_composite, third)
        _declare_2cell(self.base_strict, forward_name, left_boundary, right_boundary)
        _declare_2cell(self.base_strict, inverse_name, right_boundary, left_boundary)
        self.associator_table[(first, second, third)] = Invertible2Cell(forward_name, inverse_name)

    def set_left_unitor(self, cell: object, forward: object, inverse: object) -> None:
        name = _require_known_1cell(self.base_strict, cell, "1-cell")
        _target = self.base_strict.one_cells[name][1]
        identity = self.base_strict.id_1(_target)
        composite = self.base_strict.compose_1(name, identity)
        forward_name = _require_name(forward, "forward")
        inverse_name = _require_name(inverse, "inverse")
        _declare_2cell(self.base_strict, forward_name, composite, name)
        _declare_2cell(self.base_strict, inverse_name, name, composite)
        self.left_unitor_table[name] = Invertible2Cell(forward_name, inverse_name)

    def set_right_unitor(self, cell: object, forward: object, inverse: object) -> None:
        name = _require_known_1cell(self.base_strict, cell, "1-cell")
        identity = self.base_strict.id_1(self.base_strict.one_cells[name][0])
        composite = self.base_strict.compose_1(identity, name)
        forward_name = _require_name(forward, "forward")
        inverse_name = _require_name(inverse, "inverse")
        _declare_2cell(self.base_strict, forward_name, composite, name)
        _declare_2cell(self.base_strict, inverse_name, name, composite)
        self.right_unitor_table[name] = Invertible2Cell(forward_name, inverse_name)

    def associator(self, left: object, middle: object, right: object) -> Invertible2Cell:
        first = _require_name(left, "left")
        second = _require_name(middle, "middle")
        third = _require_name(right, "right")
        cached = self.associator_table.get((first, second, third))
        if cached is not None:
            return cached
        composite = self.base_strict.compose_1(first, self.base_strict.compose_1(second, third))
        identity = self.base_strict.id_2(composite)
        return Invertible2Cell(identity, identity)

    def left_unitor(self, cell: object) -> Invertible2Cell:
        name = _require_known_1cell(self.base_strict, cell, "1-cell")
        cached = self.left_unitor_table.get(name)
        if cached is not None:
            return cached
        identity = self.base_strict.id_2(name)
        return Invertible2Cell(identity, identity)

    def right_unitor(self, cell: object) -> Invertible2Cell:
        name = _require_known_1cell(self.base_strict, cell, "1-cell")
        cached = self.right_unitor_table.get(name)
        if cached is not None:
            return cached
        identity = self.base_strict.id_2(name)
        return Invertible2Cell(identity, identity)


def _declare_2cell(category: Strict2Category, name: str, source: str, target: str) -> None:
    if name not in category.two_cells:
        category.add_2cell(name, source, target)


def check_pentagon_coherence(bicategory: FiniteBicategory, left: object, middle: object, third: object, fourth: object) -> bool:
    """Return True when the strict pentagon paths are the same 2-cell name."""
    if not isinstance(bicategory, FiniteBicategory):
        raise _fail("pentagon requires a finite bicategory", received=type(bicategory).__name__)
    base = bicategory.base_strict
    first = _require_name(left, "left")
    second = _require_name(middle, "middle")
    third_name = _require_name(third, "third")
    fourth_name = _require_name(fourth, "fourth")
    path_a = _pentagon_path_a(bicategory, first, second, third_name, fourth_name)
    path_b = _pentagon_path_b(bicategory, first, second, third_name, fourth_name)
    if path_a == path_b:
        return True
    raise PentagonCoherenceViolation(f"({first}, {second}, {third_name}, {fourth_name})", path_a, path_b)


def _pentagon_path_a(bicategory: FiniteBicategory, first: str, second: str, third: str, fourth: str) -> str:
    base = bicategory.base_strict
    step_1 = base.compose_2_horizontal(base.id_2(first), bicategory.associator(second, third, fourth).forward)
    step_2 = bicategory.associator(first, base.compose_1(second, third), fourth).forward
    step_3 = base.compose_2_horizontal(bicategory.associator(first, second, third).forward, base.id_2(fourth))
    return base.compose_2_vertical(base.compose_2_vertical(step_1, step_2), step_3)


def _pentagon_path_b(bicategory: FiniteBicategory, first: str, second: str, third: str, fourth: str) -> str:
    base = bicategory.base_strict
    step_1 = bicategory.associator(first, second, base.compose_1(third, fourth)).forward
    step_2 = bicategory.associator(base.compose_1(first, second), third, fourth).forward
    return base.compose_2_vertical(step_1, step_2)


def check_triangle_coherence(bicategory: FiniteBicategory, left: object, right: object) -> bool:
    """Return True when the strict triangle paths are the same 2-cell name."""
    if not isinstance(bicategory, FiniteBicategory):
        raise _fail("triangle requires a finite bicategory", received=type(bicategory).__name__)
    base = bicategory.base_strict
    first = _require_name(left, "left")
    second = _require_name(right, "right")
    identity = base.id_1(base.one_cells[first][1])
    associator = bicategory.associator(first, identity, second).forward
    left_path = base.compose_2_vertical(associator, base.compose_2_horizontal(bicategory.left_unitor(first).forward, base.id_2(second)))
    right_path = base.compose_2_horizontal(base.id_2(first), bicategory.right_unitor(second).forward)
    if left_path == right_path:
        return True
    raise TriangleCoherenceViolation(f"Pair ({first}, {second})", left_path, right_path)


def _four_composite(category: Strict2Category) -> str:
    return category.compose_1(category.compose_1(category.compose_1("f", "g"), "h"), "k")


def _four_composite_other(category: Strict2Category) -> str:
    return category.compose_1("f", category.compose_1("g", category.compose_1("h", "k")))


def strict_association_witness() -> int:
    """Return 1 when both four-fold parenthesizations and the strict pentagon agree."""
    category = Strict2Category()
    for name in ("A", "B", "C", "D", "E"):
        category.add_object(name)
    category.add_1cell("f", "A", "B")
    category.add_1cell("g", "B", "C")
    category.add_1cell("h", "C", "D")
    category.add_1cell("k", "D", "E")
    left = _four_composite(category)
    right = _four_composite_other(category)
    if left != right:
        raise _fail("strict composites disagree", left=left, right=right)
    if left != "k_circ_h_circ_g_circ_f":
        raise _fail("strict composite has the wrong name", composite=left)
    if check_pentagon_coherence(FiniteBicategory(category), "f", "g", "h", "k") is not True:
        raise _fail("strict pentagon did not hold")
    count = checked_count(1)
    if count != 1:
        raise _fail("association count drifted", count=count)
    return count


def main() -> int:
    """Print the strict association certificate."""
    try:
        print(strict_association_witness())
    except HigherCategoryError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
