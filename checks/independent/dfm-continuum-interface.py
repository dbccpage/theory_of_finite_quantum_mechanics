"""Bounded finite SL(2,Z) transport and rooted-tree dressing controls.

AuthorityEffect: None. Later factors stand on the left. No topology, smooth
field, refinement limit, continuum patching or continuum dynamics is built.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path as _Path
import sys as _sys
from types import MappingProxyType
import sympy as sp

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate, require
from checker_support.cases import Cases
from checker_support.domains import integer, rational, sequence
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix

VERTICES = ("root", "p", "a", "b")
EDGES: Mapping[str, tuple[str, str]] = MappingProxyType({
    "eRP": ("root", "p"), "ePA": ("p", "a"), "eRB": ("root", "b"), "eAB": ("a", "b")})
TREE_PATH: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "root": (), "p": ("eRP",), "a": ("eRP", "ePA"), "b": ("eRB",)})
SignedPath = tuple[tuple[str, int], ...]


def _name(value: object) -> str:
    if type(value) is not str or not value.strip():
        raise Violation("input", "edge name must be nonempty text")
    integer(len(value), "edge-name characters", 1, 64)
    return value


def _graph_edge(value: object) -> str:
    name = _name(value)
    if name not in EDGES:
        raise Violation("input", "unknown fixed-graph edge")
    return name


def _det_one(matrix: RationalMatrix) -> RationalMatrix:
    matrix.require_shape(2, 2)
    if matrix.det2() != 1:
        raise Violation("input", "SL(2,Z) requires determinant one")
    return matrix


def _export(matrix: RationalMatrix) -> sp.Matrix:
    return sp.ImmutableMatrix(matrix.integer_rows())


def mat(rows: object) -> sp.Matrix:
    snapshot = tuple(sequence(row, "SL(2,Z) row", 2) for row in sequence(rows, "SL(2,Z) rows", 2))
    return _export(_det_one(RationalMatrix.from_integers(snapshot)))


def _sl2(value: object) -> RationalMatrix:
    if not isinstance(value, sp.MatrixBase) or value.shape != (2, 2):
        raise Violation("input", "label must be an exact2x2 SymPy matrix")
    if any(entry.is_Integer is not True for entry in value):
        raise Violation("input", "SL(2,Z) entries must be exact integers")
    rows = tuple(tuple(int(entry) for entry in row) for row in value.tolist())
    return _det_one(RationalMatrix.from_integers(rows))


def eye() -> sp.Matrix:
    return _export(RationalMatrix.eye(2))


def _signed_path(path: object) -> SignedPath:
    steps: list[tuple[str, int]] = []
    for step in sequence(path, "signed loop word"):
        edge, sign = sequence(step, "signed edge", 2)
        name = _name(edge)
        if type(sign) is not int or sign not in (-1, 1):
            raise Violation("input", "orientation must be integer+1 or-1")
        steps.append((name, sign))
    return tuple(steps)


def footprint(path: object) -> set[str]:
    return {edge for edge, _ in _signed_path(path)}


@dataclass(frozen=True, slots=True, init=False)
class SL2Connection:
    """Aggregate owning bounded immutable labels, with exact transport outcomes."""
    labels: Mapping[str, RationalMatrix]

    def __init__(self, labels: object) -> None:
        if type(labels) is not dict:
            raise Violation("input", "connection labels must be a dict")
        integer(len(labels), "connection edge count", 0, 4096)
        owned = {_name(name): _sl2(matrix) for name, matrix in labels.items()}
        object.__setattr__(self, "labels", MappingProxyType(owned))

    def _path(self, path: object) -> RationalMatrix:
        steps = _signed_path(path)
        if any(edge not in self.labels for edge, _ in steps):
            raise Violation("input", "loop word contains an unlabelled edge")
        result = RationalMatrix.eye(2)
        for edge, sign in steps:
            factor = self.labels[edge] if sign == 1 else self.labels[edge].inverse2()
            result = factor.mul(result)
        return result

    def path(self, path: object) -> Outcome[RationalMatrix]:
        return evaluate(self._path, path)

    def _tree(self, path: object) -> RationalMatrix:
        edges = tuple(_graph_edge(edge) for edge in sequence(path, "fixed-graph walk"))
        previous: str | None = None
        for edge in edges:
            if edge not in self.labels:
                raise Violation("input", "fixed-graph walk contains an unlabelled edge")
            src, dst = EDGES[edge]
            if previous is not None and src != previous:
                raise Violation("input", "fixed-graph walk endpoints do not compose")
            previous = dst
        return self._path(tuple((edge, 1) for edge in edges))

    def tree(self, path: object) -> Outcome[RationalMatrix]:
        return evaluate(self._tree, path)

    def _complete_graph(self) -> None:
        if any(edge not in self.labels for edge in EDGES):
            raise Violation("input", "dressing requires every fixed-graph label")

    def _dress(self, edge: object) -> RationalMatrix:
        name = _graph_edge(edge)
        self._complete_graph()
        src, dst = EDGES[name]
        target_inverse = self._tree(TREE_PATH[dst]).inverse2()
        return target_inverse.mul(self.labels[name]).mul(self._tree(TREE_PATH[src]))

    def dress(self, edge: object) -> Outcome[RationalMatrix]:
        return evaluate(self._dress, edge)


def validated_labels(labels: object) -> dict[str, sp.Matrix]:
    return {name: _export(matrix) for name, matrix in SL2Connection(labels).labels.items()}


def transport(labels: object, path: object) -> sp.Matrix:
    return _export(SL2Connection(labels)._tree(path))


def path_transport(labels: object, path: object) -> sp.Matrix:
    return _export(SL2Connection(labels)._path(path))


def dress(labels: object, edge: object) -> sp.Matrix:
    return _export(SL2Connection(labels)._dress(edge))


def formula(labels: object) -> sp.Matrix:
    connection = SL2Connection(labels)
    connection._complete_graph()
    owned = connection.labels
    result = owned["eRB"].inverse2().mul(owned["eAB"]).mul(owned["ePA"]).mul(owned["eRP"])
    return _export(result)


def incident(edge: object) -> bool:
    src, dst = EDGES[_graph_edge(edge)]
    return src in ("a", "b") or dst in ("a", "b")


def _bounded_integer(value: object) -> int:
    return rational(integer(value, "additive label"), "additive label").numerator


def additive_dress(x_rp: object, x_pa: object, x_rb: object, x_ab: object) -> int:
    rp, pa, rb, ab = (_bounded_integer(value) for value in (x_rp, x_pa, x_rb, x_ab))
    return _bounded_integer(-rb + ab + pa + rp)


def _cases(cases: Cases | None) -> Cases:
    if cases is None:
        return Cases()
    if type(cases) is not Cases:
        raise Violation("input", "a Cases recorder is required")
    return cases


def check_additive(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    print('[1/4] Additive witness: outer labels 2 and 5, other labels 0.')
    d2 = additive_dress(2, 0, 0, 0)
    d5 = additive_dress(5, 0, 0, 0)
    cases.require(d2 == 2, 'dressed additive chord for outer label 2 is 2')
    cases.require(d5 == 5, 'dressed additive chord for outer label 5 is 5')
    cases.require(d2 != d5, 'equal closed-star labels with outer labels 2 and 5 dress unequal chords')
    print(f'  dressed chords: {d2} and {d5}')


def check_identity_matrices(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    print('[2/4] Matrix witness with trivial star labels.')
    x = mat([[1, 1], [0, 1]])
    xp = mat([[1, 2], [0, 1]])
    labels = {'eRP': x, 'ePA': eye(), 'eRB': eye(), 'eAB': eye()}
    labelsp = {'eRP': xp, 'ePA': eye(), 'eRB': eye(), 'eAB': eye()}
    dressed = dress(labels, 'eAB')
    dressedp = dress(labelsp, 'eAB')
    cases.require(dressed == x, 'identity-matrix dressed chord equals the outer matrix')
    cases.require(dressedp == xp, 'dressed chord after changing only eRP equals the new outer matrix')
    cases.require(dressed != dressedp, 'the two identity-matrix dressings differ')
    for edge in EDGES:
        if incident(edge):
            cases.require(labels[edge] == labelsp[edge], f'incident edge {edge} agrees across the two labelings')
        else:
            cases.require(edge == 'eRP', f'{edge} is outside the closed star and must be eRP')
            cases.require(labels[edge] != labelsp[edge], 'eRP is the only edge whose label changes')
    cases.require(not incident('eRP'), 'eRP does not meet the closed star of a to b')
    print(f'  dressed eAB: {dressed.tolist()} and {dressedp.tolist()}')
    print('  incident edges ePA, eRB, eAB agree; eRP does not meet {a, b}')


def check_noncommutative_order(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    print('[3/4] Noncommutative path product, later factor on the left.')
    labels = {'eRP': mat([[1, 1], [0, 1]]), 'ePA': mat([[1, 0], [1, 1]]), 'eRB': mat([[1, 3], [0, 1]]), 'eAB': mat([[0, -1], [1, 0]])}
    dressed = dress(labels, 'eAB')
    expected = formula(labels)
    reversed_product = sp.simplify(labels['eRP'] * labels['ePA'] * labels['eAB'] * labels['eRB'].inv())
    cases.require(dressed == expected, 'dressed chord equals the later-on-the-left formula')
    cases.require(dressed != reversed_product, 'dressed chord is not the reversed product')
    cases.require(dressed == mat([[-4, -5], [1, 1]]), 'dressed chord is [[-4, -5], [1, 1]]')
    labelsp = dict(labels)
    labelsp['eRP'] = mat([[1, 2], [0, 1]])
    dressedp = dress(labelsp, 'eAB')
    cases.require(dressedp == formula(labelsp), 'dressed chord after changing eRP still matches the formula')
    cases.require(dressedp == mat([[-4, -9], [1, 2]]), 'dressed chord after changing eRP is [[-4, -9], [1, 2]]')
    cases.require(dressed != dressedp, 'changing only the outer edge changes the dressed chord')
    for edge in ('ePA', 'eRB', 'eAB'):
        cases.require(labels[edge] == labelsp[edge], f'incident edge {edge} is unchanged when only eRP changes')
    print(f'  dressed eAB: {dressed.tolist()}')
    print(f'  after changing only eRP: {dressedp.tolist()}')
    print(f'  reversed product, not the dressing: {reversed_product.tolist()}')


def check_star_enumeration(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    print('[4/4] Closed star of a→b is {ePA, eRB, eAB}.')
    star = tuple((edge for edge in EDGES if incident(edge)))
    cases.require(star == ('ePA', 'eRB', 'eAB'), 'closed star of a to b is ePA, eRB, eAB')
    cases.require(EDGES['eRP'] == ('root', 'p'), 'eRP runs from root to p')
    print(f'  star: {star}')


def check_path_laws(path: object, labels: object, cases: Cases | None = None) -> None:
    """Fixture verification on x/y loops; outside is explicitly excluded from the word."""
    cases = _cases(cases)
    steps = _signed_path(path)
    sequence(steps, "fixture prefix", maximum=4095)
    checked = validated_labels(labels)
    if any(name not in checked for name in ("x", "y", "outside")) or not footprint(steps) <= {"x", "y"}:
        raise Violation("input", "path-law fixture requires x/y/outside labels and an x/y word")
    result = path_transport(checked, steps)
    rev = tuple((edge, -sign) for edge, sign in reversed(steps))
    cases.require(path_transport(checked, rev) == result.inv(), "reverse transport")
    changed = dict(checked)
    changed["outside"] = mat([[1, 7], [0, 1]])
    cases.require(path_transport(changed, steps) == result, "outside footprint stability")
    changed["x"] = mat([[1, 2], [0, 1]])
    other = path_transport(changed, steps)
    if result != other:
        cases.require(any(checked[edge] != changed[edge] for edge in footprint(steps)), "changed-label certificate")
    for tail in ((), (("x", 1),), (("y", -1),)):
        cases.require(path_transport(checked, steps+tail) == path_transport(checked, tail)*result, "append transport order")


def check_general_dependencies(cases: Cases | None = None) -> None:
    cases = _cases(cases)
    labels = {"x": mat([[1, 1], [0, 1]]), "y": mat([[1, 0], [1, 1]]), "outside": eye()}
    letters = (("x", 1), ("x", -1), ("y", 1), ("y", -1))
    paths = [tuple(word) for size in range(4) for word in product(letters, repeat=size)]
    for path in paths:
        check_path_laws(path, labels, cases)
    for invalid in ((("x", 0),), (("x", True),), (("missing", 1),)):
        result = evaluate(path_transport, labels, invalid)
        cases.require(result.error is not None and result.error.kind == "input", "invalid signed path refused")
    print(f"dependency API: {len(paths)} loop words, {3*len(paths)} append cases; 3 invalid paths refused")


def main() -> int:
    cases = Cases()
    for check in (check_general_dependencies, check_additive, check_identity_matrices,
                  check_noncommutative_order, check_star_enumeration):
        check(cases)
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "checks": cases.checks,
                      "scope": "Supplied finite paths and rooted-tree dressing; no continuum construction."}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
