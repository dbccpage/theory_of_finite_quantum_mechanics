"""Independent exact Wilson-slab diagnostic; imports no repository modules.

AuthorityEffect: None. This tests a fixed-basis chiral truncation and a lifted
level-one cup-product candidate, not a regulated Callan-Harvey determinant.
Arithmetic: Q(i) matrices and Q[z]/(z**16+1), named Q(zeta_32), for CS phases.
Bounded CLI: open 2 x 2 x nz boxes, nz in {3, 4}, and a 3 x 3 x 3 box.
Dense elimination uses polynomially many exact field operations.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
import json
from typing import Any, Callable

import sympy as sp  # type: ignore[import-untyped]

Vertex = tuple[int, int, int]
Edge = tuple[Vertex, Vertex]
Tet = tuple[Vertex, Vertex, Vertex, Vertex]
Scalar = Any  # SymPy exact expressions, checked at the construction boundary.
Matrix = Any  # SymPy matrices, never converted to numerical arrays.
Q = sp.Rational


class DomainError(ValueError):
    """Input is outside this deliberately bounded exact model."""


class CheckFailure(RuntimeError):
    """An independently recomputed identity or witness did not match."""


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CheckFailure(message)


def equal(actual: Scalar, expected: Scalar, message: str) -> None:
    if isinstance(actual, sp.MatrixBase):
        require(actual.shape == expected.shape, message + ": shape")
        require(all(sp.cancel(x) == 0 for x in actual - expected), message)
    else:
        require(sp.cancel(actual - expected) == 0, message)


@dataclass(frozen=True)
class Slab:
    """Open boundaries in every direction; the end surfaces are z=0,nz-1."""

    nz: int
    width: int = 2

    def __post_init__(self) -> None:
        if type(self.nz) is not int or self.nz not in (3, 4):
            raise DomainError("nz must be the integer 3 or 4")
        if type(self.width) is not int or (self.width, self.nz) not in ((2, 3), (2, 4), (3, 3)):
            raise DomainError("only 2x2x3, 2x2x4 and 3x3x3 slabs are admitted")

    @property
    def vertices(self) -> tuple[Vertex, ...]:
        return tuple(product(range(self.width), range(self.width), range(self.nz)))

    @property
    def edges(self) -> tuple[Edge, ...]:
        return tuple((v, w) for v in self.vertices for w in self.vertices
                     if v < w and sum(abs(w[j] - v[j]) for j in range(3)) == 1)

    @property
    def tetrahedra(self) -> tuple[tuple[int, Tet], ...]:
        result: list[tuple[int, Tet]] = []
        for x, y, z, order in product(range(self.width - 1), range(self.width - 1),
                                      range(self.nz - 1), permutations(range(3))):
            path: list[Vertex] = [(x, y, z)]
            for axis in order:
                dest = list(path[-1])
                dest[axis] += 1
                path.append((dest[0], dest[1], dest[2]))
            inversions = sum(order[i] > order[j] for i in range(3) for j in range(i + 1, 3))
            result.append(((-1) ** inversions, (path[0], path[1], path[2], path[3])))
        return tuple(result)


@dataclass(frozen=True)
class Field:
    """Immutable integer quarter-turn link lifts and vertex gauge lifts."""

    slab: Slab
    turns: tuple[int, ...]
    gauge: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.slab) is not Slab:
            raise DomainError("slab must be a Slab")
        for data, size in ((self.turns, len(self.slab.edges)), (self.gauge, len(self.slab.vertices))):
            if type(data) is not tuple or len(data) != size:
                raise DomainError("field data must be a tuple with the declared length")
            if any(type(x) is not int or abs(x) > 8 for x in data):
                raise DomainError("quarter turns must be bounded integers, excluding bool")

    def transformed(self) -> Field:
        alpha = dict(zip(self.slab.vertices, self.gauge))
        turns = tuple(a + alpha[w] - alpha[v] for (v, w), a in zip(self.slab.edges, self.turns))
        return Field(self.slab, turns, self.gauge)

    def lift(self, v: Vertex, w: Vertex) -> Scalar:
        """Extend axial links along the monotone x-then-y-then-z path."""
        links = dict(zip(self.slab.edges, self.turns))
        total = 0
        for axis in range(3):
            while v[axis] < w[axis]:
                dest = list(v)
                dest[axis] += 1
                nxt = (dest[0], dest[1], dest[2])
                total += links[v, nxt]
                v = nxt
        if v != w:
            raise DomainError("lift requires componentwise ordered slab vertices")
        return Q(total, 4)


def fixture(nz: int, width: int = 2) -> Field:
    slab = Slab(nz, width)
    active = ((0, 0, 1), (0, 1, 1)) if width == 2 else ((1, 1, 0), (1, 2, 0))
    gauge_site = (0, 0, 0) if width == 2 else (1, 1, 0)
    return Field(slab, tuple(int(e == active) for e in slab.edges),
                 tuple(int(v == gauge_site) for v in slab.vertices))


def wilson(field: Field, reverse_conjugate: bool = True) -> Matrix:
    """a=r=1, m(z)=-1 if 2*z<nz else +1; omitted exterior hops are zero."""
    vertices = field.slab.vertices
    index = {v: i for i, v in enumerate(vertices)}
    identity = sp.eye(2)
    sigma = (sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]),
             sp.diag(1, -1))
    result = sp.zeros(2 * len(vertices))
    for v, i in index.items():
        mass = -1 if 2 * v[2] < field.slab.nz else 1
        result[2*i:2*i+2, 2*i:2*i+2] = (mass + 3) * identity
    for (v, w), turns in zip(field.slab.edges, field.turns):
        axis = next(j for j in range(3) if v[j] != w[j])
        i, j = index[v], index[w]
        u = sp.I ** turns
        result[2*i:2*i+2, 2*j:2*j+2] += -Q(1, 2) * (identity - sigma[axis]) * u
        inverse = sp.conjugate(u) if reverse_conjugate else u
        result[2*j:2*j+2, 2*i:2*i+2] += -Q(1, 2) * (identity + sigma[axis]) * inverse
    require(all(x in sp.QQ_I for x in result), "matrix escaped Q(i)")
    return result


def determinant(matrix: Matrix) -> Scalar:
    return sp.cancel(matrix.det(method="domain-ge"))


def effective(matrix: Matrix, boundary: list[int], interior: list[int]) -> tuple[Matrix, Matrix]:
    bulk = matrix.extract(interior, interior)
    if determinant(bulk) == 0:
        raise DomainError("singular interior block: boundary Schur complement undefined")
    inverse = bulk.inv(method="DM")
    equal(bulk * inverse, sp.eye(len(interior)), "right inverse")
    equal(inverse * bulk, sp.eye(len(interior)), "left inverse")
    schur = matrix.extract(boundary, boundary) - matrix.extract(boundary, interior) * inverse * matrix.extract(interior, boundary)
    return bulk, schur.applyfunc(sp.cancel)


def curvature(field: Field, x: Vertex, y: Vertex, z: Vertex) -> Scalar:
    return field.lift(y, z) - field.lift(x, z) + field.lift(x, y)


def cs_action(field: Field) -> Scalar:
    return sum((Q(sign, 2) * field.lift(a, b) * curvature(field, b, c, d)
                for sign, (a, b, c, d) in field.slab.tetrahedra), Q(0))


def boundary_variation(field: Field) -> tuple[Scalar, int]:
    """Build the boundary chain explicitly, canceling internal triangular faces."""
    faces: dict[tuple[Vertex, ...], int] = {}
    for sign, tet in field.slab.tetrahedra:
        for j in range(4):
            face = tet[:j] + tet[j+1:]
            faces[face] = faces.get(face, 0) + sign * (-1)**j
    alpha = dict(zip(field.slab.vertices, field.gauge))
    result = sum((Q(sign, 2) * Q(alpha[t[0]], 4) * curvature(field, t[0], t[1], t[2])
                  for t, sign in faces.items()), Q(0))
    return result, sum(sign != 0 for sign in faces.values())


def matrix_witness(field: Field) -> dict[str, object]:
    vertices = field.slab.vertices
    boundary_sites = [i for i, v in enumerate(vertices) if v[2] in (0, field.slab.nz - 1)]
    boundary = [2*i+s for i in boundary_sites for s in range(2)]
    interior = [j for j in range(2*len(vertices)) if j not in boundary]
    original, changed = wilson(field), wilson(field.transformed())
    g = sp.diag(*(sp.I**a for a in field.gauge for _ in range(2)))
    equal(changed, g.inv() * original * g, "Wilson gauge covariance")
    bulk, schur = effective(original, boundary, interior)
    bulk_t, schur_t = effective(changed, boundary, interior)
    gb, gi = g.extract(boundary, boundary), g.extract(interior, interior)
    equal(bulk_t, gi.inv() * bulk * gi, "bulk covariance")
    equal(schur_t, gb.inv() * schur * gb, "Schur covariance")
    chirality = sp.diag(*(1 if j % 2 == 0 else -1 for j in range(schur.rows)))
    require(chirality * schur + schur * chirality != sp.zeros(schur.rows),
            "unexpected exact boundary chiral symmetry")
    # Opposite sigma_z chirality at the two end surfaces; fixed bases, one mode/site.
    cols = [2*k + int(vertices[i][2] != 0) for k, i in enumerate(boundary_sites)]
    rows = [j ^ 1 for j in cols]
    chiral, chiral_t = schur.extract(rows, cols), schur_t.extract(rows, cols)
    gch = gb.extract(cols, cols)
    equal(chiral_t, gch.inv() * chiral * gch, "fixed chiral block covariance")
    dets = tuple(determinant(m) for m in (original, bulk, schur, chiral))
    changed_dets = tuple(determinant(m) for m in (changed, bulk_t, schur_t, chiral_t))
    require(all(d != 0 for d in dets), "fixture has a zero determinant")
    for a, b in zip(dets, changed_dets):
        equal(a, b, "gauge determinant invariance")
    equal(dets[0], dets[1] * dets[2], "Schur determinant factorization")
    return {"matrix_size": original.rows, "bulk_size": bulk.rows, "boundary_size": schur.rows,
            "chiral_size": chiral.rows, "determinants": list(map(str, dets)),
            "transformed_determinants": list(map(str, changed_dets)),
            "ratios_full_bulk_schur_chiral": ["1"] * len(dets)}


def witness(nz: int, width: int = 2) -> dict[str, object]:
    field = fixture(nz, width)
    transformed = field.transformed()
    before, after = cs_action(field), cs_action(transformed)
    boundary, faces = boundary_variation(field)
    equal(before, Q(0), "initial CS action")
    equal(after, Q(1, 32), "transformed CS action")
    equal(after - before, boundary, "explicit discrete Stokes")
    integer_gauge = Field(field.slab, field.turns, tuple(4*a for a in field.gauge))
    equal(wilson(integer_gauge.transformed()), wilson(field), "integer lift has unchanged U(1) links")
    equal(cs_action(integer_gauge.transformed()) - before, Q(1, 8), "compact lift obstruction")
    alpha = dict(zip(field.slab.vertices, field.gauge))
    if width == 3:
        require(all(alpha[v] == 0 for v in field.slab.vertices
                    if v[0] in (0, 2) or v[1] in (0, 2)), "side boundary gauge support")
    for _, tet in field.slab.tetrahedra:
        a, b, c, d = tet
        equal(curvature(field, b, c, d), curvature(transformed, b, c, d), "curvature invariance")
        equal(transformed.lift(a, b), field.lift(a, b) + Q(alpha[b] - alpha[a], 4), "path extension covariance")
    z = sp.Symbol("z")
    modulus = sp.Poly(sp.cyclotomic_poly(32, z), z, domain=sp.QQ)
    equal(modulus.as_expr(), z**16 + 1, "cyclotomic field")
    exponent = 32 * (after - before)
    require(exponent.is_Integer is True, "phase outside Q(zeta_32)")
    residual = sp.rem(sp.Poly(z**int(exponent) - 1, z, domain=sp.QQ), modulus)
    require(not residual.is_zero, "unexpected cancellation")
    return {"geometry": [width, width, nz], "sites": len(field.slab.vertices),
            "edges": len(field.slab.edges), "tetrahedra": len(field.slab.tetrahedra),
            "boundary_triangles_including_sides": faces, **matrix_witness(field),
            "cs_before": str(before), "cs_after": str(after), "delta_cs": str(boundary),
            "bulk_cs_phase_ratio": "zeta_32", "combined_phase_ratio": "zeta_32",
            "integer_lift_delta_cs_same_links": "1/8",
            "nonzero_phase_residual": str(residual.as_expr())}


def rejection(operation: Callable[[], object]) -> None:
    try:
        operation()
    except DomainError:
        return
    raise CheckFailure("expected DomainError")


def challenges() -> dict[str, object]:
    field = fixture(3)
    rejection(lambda: Slab(True))
    rejection(lambda: Slab(2))
    rejection(lambda: Slab(4, 3))
    rejection(lambda: Field(field.slab, (), field.gauge))
    rejection(lambda: Field(field.slab, (True,) * len(field.turns), field.gauge))
    rejection(lambda: Field(field.slab, (9,) * len(field.turns), field.gauge))
    rejection(lambda: effective(sp.zeros(2), [0], [1]))
    rejection(lambda: field.lift((1, 0, 0), (0, 0, 0)))
    g = sp.diag(*(sp.I**a for a in field.gauge for _ in range(2)))
    mutated = wilson(field.transformed(), reverse_conjugate=False)
    require(mutated != g.inv() * wilson(field, reverse_conjugate=False) * g,
            "wrong reverse-link mutation survived")
    require(cs_action(field.transformed()) - cs_action(field) != -boundary_variation(field)[0],
            "boundary orientation mutation survived")
    require(cs_action(field.transformed()) - cs_action(field) != Q(0),
            "zero CS variation mutation survived")
    # Independent symbolic identities; no fixture constants or repository imports.
    a01, a02, a03, a12, a13, a23 = sp.symbols("a01 a02 a03 a12 a13 a23")
    f0, f1, f2, f3 = sp.symbols("f0 f1 f2 f3")
    flux = a23 - a13 + a12
    boundary = f1*flux - f0*(a23-a03+a02) + f0*(a13-a03+a01) - f0*(a12-a02+a01)
    equal(boundary, (f1-f0)*flux, "symbolic cochain Stokes")
    equal((a23+f3-f2)-(a13+f3-f1)+(a12+f2-f1), flux, "symbolic curvature")
    equal(sp.eye(0).det(), 1, "empty determinant")
    return {"domain_rejections": 8, "mutations": {"killed": 3, "survived": 0,
            "demonstrably_equivalent": 0, "invalid": 0, "inconclusive": 0, "unrun": 0},
            "symbolic_cochain_identities": "passed"}


def main() -> None:
    result = {"node": "FSP-LATTICE-ANOMALY-INFLOW", "authority_effect": "None",
              "sympy_version": sp.__version__, "checks": challenges(),
              "witnesses": [witness(3), witness(4), witness(3, 3)],
              "outcome": "fixed-basis Wilson boundary plus lifted CS candidate fails; full target OPEN"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
