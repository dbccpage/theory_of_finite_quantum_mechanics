"""Finite four-point order and exact two-site operator controls.

AuthorityEffect: None. Shared matrix operations are infrastructure, not an
independent second implementation. These supplied finite matrices do not
construct a continuum local net or verify the Haag-Kastler axioms.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.cases import Cases
from checker_support.domains import integer
from checker_support.rational_matrix import Flat2, RationalMatrix

FlatInput = tuple[int | Fraction, int | Fraction, int | Fraction, int | Fraction]


def rel(i: int, j: int) -> bool:
    left, right = integer(i, "carrier point", 0, 3), integer(j, "carrier point", 0, 3)
    return (left, right) in {(0, 2), (1, 2), (1, 3)}


def spacelike(i: int, j: int) -> bool:
    left, right = integer(i, "carrier point", 0, 3), integer(j, "carrier point", 0, 3)
    return left != right and not rel(left, right) and not rel(right, left)


def mm(x: FlatInput, y: FlatInput) -> Flat2:
    return RationalMatrix.from_flat2(x).mul(RationalMatrix.from_flat2(y)).flat2()


def add2(x: FlatInput, y: FlatInput) -> Flat2:
    return RationalMatrix.from_flat2(x).add(RationalMatrix.from_flat2(y)).flat2()


def trp(x: FlatInput) -> Flat2:
    return RationalMatrix.from_flat2(x).transpose().flat2()


def det2(x: FlatInput) -> Fraction:
    return RationalMatrix.from_flat2(x).det2()


def mm4(p: list[list[int]], q: list[list[int]]) -> list[list[int]]:
    left = RationalMatrix.from_integers(p).require_shape(4, 4)
    right = RationalMatrix.from_integers(q).require_shape(4, 4)
    return [list(row) for row in left.mul(right).integer_rows()]


def flat(value: list[list[int]]) -> tuple[int, ...]:
    rows = RationalMatrix.from_integers(value).require_shape(4, 4).integer_rows()
    return tuple(x for row in rows for x in row)


def kron_blocks(p: FlatInput, q: FlatInput) -> list[list[int]]:
    """Integer tensor embedding; reject nonintegral inputs even if products cancel."""
    left, right = RationalMatrix.from_flat2(p), RationalMatrix.from_flat2(q)
    left.integer_rows()
    right.integer_rows()
    return [list(row) for row in left.kron(right).integer_rows()]


def check_four_point_order(cases: Cases) -> None:
    points = range(4)
    for point in points:
        cases.append((f"order.irreflexive.{point}", not rel(point, point)))
    for x in points:
        for y in points:
            for z in points:
                cases.append((f"order.transitive.{x}.{y}.{z}", not (rel(x, y) and rel(y, z)) or rel(x, z)))
    relations = [(i, j) for i in points for j in points if rel(i, j)]
    unordered = [(i, j) for i in points for j in points if i < j and spacelike(i, j)]
    cases.append(("order.relations", relations == [(0, 2), (1, 2), (1, 3)]))
    cases.append(("order.spacelike", unordered == [(0, 1), (0, 3), (2, 3)]))
    cases.append(("order.flags", spacelike(1, 0) and not spacelike(1, 3)))


def check_single_site_algebra(cases: Cases) -> None:
    ident: FlatInput = (1, 0, 0, 1)
    xmat: FlatInput = (0, 1, 1, 0)
    zmat: FlatInput = (1, 0, 0, -1)
    amat: FlatInput = (1, 2, 3, 4)
    bmat: FlatInput = (5, 6, 7, 8)
    for index, matrix in enumerate((amat, bmat, xmat, zmat)):
        cases.append((f"single.unit.{index}", mm(ident, matrix) == matrix and mm(matrix, ident) == matrix))
    xz, zx = mm(xmat, zmat), mm(zmat, xmat)
    cases.append(("single.pauli", xz == tuple(Fraction(n) for n in (0, -1, 1, 0))
                  and zx == tuple(Fraction(n) for n in (0, 1, -1, 0))))
    cases.append(("single.anticommutator", add2(xz, zx) == (Fraction(0),)*4 and xz != zx))
    cases.append(("single.transpose", trp(trp(amat)) == amat and trp(mm(amat, bmat)) == mm(trp(bmat), trp(amat))))
    cases.append(("single.determinants", tuple(det2(m) for m in (amat, bmat, xmat, zmat))
                  == tuple(Fraction(n) for n in (-2, -2, -1, -1))))


def check_two_site_products(cases: Cases) -> None:
    ident: FlatInput = (1, 0, 0, 1)
    amat: FlatInput = (1, 2, 3, 4)
    bmat: FlatInput = (5, 6, 7, 8)
    xmat: FlatInput = (0, 1, 1, 0)
    zmat: FlatInput = (1, 0, 0, -1)
    left, right, both = kron_blocks(amat, ident), kron_blocks(ident, bmat), kron_blocks(amat, bmat)
    cases.append(("two.disjoint", mm4(left, right) == both and mm4(right, left) == both))
    cases.append(("two.sum", sum(sum(row) for row in both) == 260))
    same_l = mm4(kron_blocks(xmat, ident), kron_blocks(zmat, ident))
    same_r = mm4(kron_blocks(zmat, ident), kron_blocks(xmat, ident))
    cases.append(("two.same_site", same_l != same_r and same_l[0][2] == -1 and same_r[0][2] == 1))
    cases.append(("two.corners", flat(both)[0] == 5 and flat(both)[-1] == 32))
    eye = [list(row) for row in RationalMatrix.eye(4).integer_rows()]
    cases.append(("two.identity", mm4(eye, both) == both and mm4(both, eye) == both))


def run_checks() -> dict[str, object]:
    cases = Cases()
    for operation in (check_four_point_order, check_single_site_algebra, check_two_site_products):
        operation(cases)
    failures = [name for name, passed in cases if not passed]
    return {"scope": "finite four-point order and two-site matrices", "authority_effect": "None",
            "total_checks": len(cases), "failed_checks": len(failures), "failures": failures, "all_passed": not failures}


def main() -> int:
    result = run_checks()
    print(json.dumps(result, indent=2))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))
