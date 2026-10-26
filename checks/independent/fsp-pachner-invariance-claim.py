"""Independent exact 4D Pachner audit: enumerate edge labels, not vertex potentials.

AuthorityEffect: None. No repository module or Lean result is imported.
Declared scope: untwisted flat-connection counting for C1, C2, C3, C4, C5 and S3.
The universal finite-group theorem is in Lean; these finite checks are controls.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
import json


class CheckFailure(RuntimeError):
    """A finite identity, enumeration or negative control failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


@dataclass(frozen=True)
class GroupTable:
    name: str
    mul: tuple[tuple[int, ...], ...]
    inv: tuple[int, ...]
    unit: int

    @property
    def order(self) -> int:
        return len(self.mul)

    def validate(self) -> None:
        values = range(self.order)
        require(all(len(row) == self.order for row in self.mul), "square group table")
        require(all(type(x) is int and x in values for row in self.mul for x in row), "closed group table")
        require(len(self.inv) == self.order and self.unit in values, "group metadata")
        for a in values:
            require(self.inv[a] in values, "inverse in carrier")
            require(self.mul[self.unit][a] == a == self.mul[a][self.unit], "two-sided unit")
            require(self.mul[a][self.inv[a]] == self.unit == self.mul[self.inv[a]][a], "two-sided inverse")
        for a, b, c in product(values, repeat=3):
            require(self.mul[self.mul[a][b]][c] == self.mul[a][self.mul[b][c]], "associativity")


def cyclic(order: int) -> GroupTable:
    return GroupTable(f"C{order}", tuple(tuple((a + b) % order for b in range(order))
                      for a in range(order)), tuple((-a) % order for a in range(order)), 0)


def symmetric_three() -> GroupTable:
    elements = tuple(permutations(range(3)))
    position = {p: i for i, p in enumerate(elements)}
    table = tuple(tuple(position[tuple(p[q[i]] for i in range(3))] for q in elements) for p in elements)
    unit = position[(0, 1, 2)]
    inverses = tuple(next(b for b in range(6) if table[a][b] == unit) for a in range(6))
    return GroupTable("S3", table, inverses, unit)


VERTICES = frozenset(range(6))


def complex_faces(p: int, left: bool) -> set[frozenset[int]]:
    omitted = range(p) if left else range(p, 6)
    facets = [VERTICES - {v} for v in omitted]
    return {frozenset(s) for f in facets for size in range(6) for s in combinations(sorted(f), size)}


def skeleton(faces: set[frozenset[int]], size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(tuple(sorted(s)) for s in faces if len(s) == size))


def flat_assignments(group: GroupTable, edges: tuple, triangles: tuple) -> list[tuple[int, ...]]:
    """Backtrack over independent edge labels; propagate each triangle equation.

    For i<j<k, g_ij*g_jk=g_ik. Every assigned edge is independently checked
    against every triangle. The fixed six-vertex/group-order envelope bounds
    this audit; it is not an efficient sampler or general group-solving API.
    """
    require(group.order <= 6 and len(edges) <= 15, "declared audit envelope")
    index = {edge: i for i, edge in enumerate(edges)}
    constraints = [(index[i, j], index[j, k], index[i, k]) for i, j, k in triangles]
    results = []
    visits = 0

    def search(values: list[int | None]) -> None:
        nonlocal visits
        visits += 1
        require(visits <= 100_000, "enumeration visit budget")
        changed = True
        while changed:
            changed = False
            for ab, bc, ac in constraints:
                a, b, c = values[ab], values[bc], values[ac]
                missing = (a is None) + (b is None) + (c is None)
                if missing == 0:
                    if group.mul[a][b] != c:
                        return
                elif missing == 1:
                    if a is None:
                        values[ab] = group.mul[c][group.inv[b]]
                    elif b is None:
                        values[bc] = group.mul[group.inv[a]][c]
                    else:
                        values[ac] = group.mul[a][b]
                    changed = True
        if None not in values:
            results.append(tuple(values))
            return
        edge = values.index(None)
        for value in range(group.order):
            extension = values.copy()
            extension[edge] = value
            search(extension)

    search([None] * len(edges))
    require(len(results) == len(set(results)), "duplicate enumerated configuration")
    return results


def brute_force(group: GroupTable, edges: tuple, triangles: tuple) -> set[tuple[int, ...]]:
    """Second enumeration route for C2: inspect all 2^E raw assignments."""
    require(group.order == 2, "brute-force control limited to C2")
    index = {edge: i for i, edge in enumerate(edges)}
    return {values for values in product(range(2), repeat=len(edges))
            if all(group.mul[values[index[i, j]]][values[index[j, k]]] == values[index[i, k]]
                   for i, j, k in triangles)}


def boundary_counts(states: list[tuple], edges: tuple, boundary: tuple) -> Counter:
    positions = [edges.index(e) for e in boundary]
    return Counter(tuple(state[i] for i in positions) for state in states)


def check_move(group: GroupTable, p: int) -> dict:
    left, right = complex_faces(p, True), complex_faces(p, False)
    boundary = left & right
    le, re, be = (skeleton(c, 2) for c in (left, right, boundary))
    lt, rt, bt = (skeleton(c, 3) for c in (left, right, boundary))
    lv, rv, bv = (set(skeleton(c, 1)) for c in (left, right, boundary))
    interior = (len(lv - bv), len(rv - bv))
    require((len(skeleton(left, 5)), len(skeleton(right, 5))) == (p, 6 - p), "actual Pachner facets")
    require(len(skeleton(boundary, 4)) == p * (6 - p), "common boundary tetrahedra")
    require(interior == ((0, 1) if p == 1 else (0, 0)), "interior vertex difference")
    ls, rs = flat_assignments(group, le, lt), flat_assignments(group, re, rt)
    lc, rc = boundary_counts(ls, le, be), boundary_counts(rs, re, be)
    bs = set(flat_assignments(group, be, bt))
    require(set(lc) == bs == set(rc), "all and only flat boundary data extend on both sides")
    require(set(lc.values()) == {1}, "left fixed-boundary count")
    require(set(rc.values()) == ({group.order} if p == 1 else {1}), "right fixed-boundary count")
    for b in bs:
        require(Fraction(lc[b], group.order ** interior[0]) ==
                Fraction(rc[b], group.order ** interior[1]), "normalized local amplitude")
    # Nonconstant exterior multiplicities, plus the zero/empty exterior case.
    weighted_left = weighted_right = 0
    for index, b in enumerate(sorted(bs)):
        multiplicity = index % 4
        weighted_left += multiplicity * lc[b]
        weighted_right += multiplicity * rc[b]
    outside_vertices = len(bv) + 2
    require(Fraction(weighted_left, group.order ** (outside_vertices + interior[0])) ==
            Fraction(weighted_right, group.order ** (outside_vertices + interior[1])), "glued normalized sum")
    require(Fraction(0, group.order ** outside_vertices) == 0, "empty exterior")
    if group.name == "C2":
        require(set(ls) == brute_force(group, le, lt), "left exhaustive Cartesian control")
        require(set(rs) == brute_force(group, re, rt), "right exhaustive Cartesian control")
    if group.order > 1:
        bad = [group.unit] * len(be)
        bad[0] = next(x for x in range(group.order) if x != group.unit)
        require(tuple(bad) not in bs and lc[tuple(bad)] == rc[tuple(bad)] == 0, "nonflat boundary refused")
        if p == 1:
            require(sum(lc.values()) != sum(rc.values()), "omitting vertex normalization must fail")
        if p == 2:
            position = re.index((0, 1))
            forced = boundary_counts([s for s in rs if s[position] == group.unit], re, be)
            require(any(forced[b] != lc[b] for b in bs), "forcing the new edge to identity must fail")
    return {"move": f"{p}-{6-p}", "facets": [p, 6-p], "vertices": [len(lv), len(rv)],
            "edges": [len(le), len(re)], "triangles": [len(lt), len(rt)],
            "boundary_tetrahedra": len(skeleton(boundary, 4)), "interior_vertices": list(interior),
            "flat_boundaries": len(bs), "flat_colorings": [len(ls), len(rs)],
            "fixed_boundary_fillings": [sorted(set(lc.values())), sorted(set(rc.values()))],
            "normalized_local_amplitude": "1", "weighted_exterior_total": str(Fraction(weighted_left, group.order ** outside_vertices))}


def negative_flatness_control() -> dict:
    group = cyclic(2)
    left, right = complex_faces(1, True), complex_faces(1, False)
    edges = skeleton(right, 2)
    # Keep the correct boundary and all five new edges, but omit interior flatness.
    damaged = flat_assignments(group, edges, skeleton(left, 3))
    counts = boundary_counts(damaged, edges, skeleton(left & right, 2))
    require(set(counts.values()) == {32}, "damaged model control count")
    require(Fraction(next(iter(counts.values())), group.order) == 16, "damaged model violates amplitude one")
    return {"group": "C2", "omitted_interior_flatness": {"fillings_per_boundary": 32, "normalized_amplitude": "16"}}


def main() -> None:
    results = []
    for group in [cyclic(n) for n in range(1, 6)] + [symmetric_three()]:
        group.validate()
        moves = [check_move(group, p) for p in (1, 2, 3)]
        results.append({"group": group.name, "order": group.order, "moves": moves})
    s3 = symmetric_three()
    require(any(s3.mul[a][b] != s3.mul[b][a] for a, b in product(range(6), repeat=2)), "nonabelian control really is nonabelian")
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "method": "edge-CSP enumeration plus independent full Cartesian C2 enumeration",
                      "groups": results, "negative_flatness_control": negative_flatness_control(),
                      "scope": "Finite test groups only; the universal theorem is kernel checked separately."}, indent=2))


if __name__ == "__main__":
    main()
