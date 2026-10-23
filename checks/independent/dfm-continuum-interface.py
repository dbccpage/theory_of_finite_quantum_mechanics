#!/usr/bin/env python3
"""Independent check for DFM-CONTINUUM-INTERFACE.

Recomputes the supplied rooted-tree dressing of one chord without importing
repository code. Group multiplication is later-on-the-left, matching
FiniteGraphDressing.transport of an appended walk.

Exits 0 on success.
"""

from __future__ import annotations

from collections.abc import Sequence
import sympy as sp  # type: ignore[import-untyped]  # SymPy does not ship typing metadata.


VERTICES = ("root", "p", "a", "b")
EDGES: dict[str, tuple[str, str]] = {
    "eRP": ("root", "p"),
    "ePA": ("p", "a"),
    "eRB": ("root", "b"),
    "eAB": ("a", "b"),
}
TREE_PATH: dict[str, tuple[str, ...]] = {
    "root": (),
    "p": ("eRP",),
    "a": ("eRP", "ePA"),
    "b": ("eRB",),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mat(rows: Sequence[Sequence[int]]) -> sp.Matrix:
    if len(rows) != 2 or any(len(row) != 2 for row in rows):
        raise ValueError("SL(2,Z) matrices require two rows and two columns")
    if any(type(value) is not int for row in rows for value in row):
        raise ValueError("exact integer entries required; bool and float are refused")
    result = sp.Matrix(rows)
    if result.det() != 1:
        raise ValueError("matrix must have determinant one")
    return result


def eye() -> sp.Matrix:
    return sp.eye(2)


def transport(labels: dict[str, sp.Matrix], path: tuple[str, ...]) -> sp.Matrix:
    value = eye()
    for edge in path:
        value = labels[edge] * value
    return value


def dress(labels: dict[str, sp.Matrix], edge: str) -> sp.Matrix:
    src, dst = EDGES[edge]
    u_src = transport(labels, TREE_PATH[src]).inv()
    u_dst = transport(labels, TREE_PATH[dst]).inv()
    return sp.simplify(u_dst * labels[edge] * u_src.inv())


def formula(labels: dict[str, sp.Matrix]) -> sp.Matrix:
    return sp.simplify(
        labels["eRB"].inv() * labels["eAB"] * labels["ePA"] * labels["eRP"]
    )


def incident(edge: str) -> bool:
    src, dst = EDGES[edge]
    return src in ("a", "b") or dst in ("a", "b")


def additive_dress(x_rp: int, x_pa: int, x_rb: int, x_ab: int) -> int:
    """Integers under addition. Later-on-the-left is ordinary sum."""
    t_a = x_pa + x_rp
    t_b = x_rb
    return (-t_b) + x_ab + t_a


def check_additive() -> None:
    print("[1/4] Additive witness: outer labels 2 and 5, other labels 0.")
    d2 = additive_dress(2, 0, 0, 0)
    d5 = additive_dress(5, 0, 0, 0)
    require(d2 == 2, 'independent check failed at original line 75')
    require(d5 == 5, 'independent check failed at original line 76')
    require(d2 != d5, 'independent check failed at original line 77')
    print(f"  dressed chords: {d2} and {d5}")


def check_identity_matrices() -> None:
    print("[2/4] Matrix witness with trivial star labels.")
    x = mat([[1, 1], [0, 1]])
    xp = mat([[1, 2], [0, 1]])
    labels = {"eRP": x, "ePA": eye(), "eRB": eye(), "eAB": eye()}
    labelsp = {"eRP": xp, "ePA": eye(), "eRB": eye(), "eAB": eye()}
    dressed = dress(labels, "eAB")
    dressedp = dress(labelsp, "eAB")
    require(dressed == x, 'independent check failed at original line 89')
    require(dressedp == xp, 'independent check failed at original line 90')
    require(dressed != dressedp, 'independent check failed at original line 91')
    for edge in EDGES:
        if incident(edge):
            require(labels[edge] == labelsp[edge], 'independent check failed at original line 94')
        else:
            require(edge == "eRP", 'independent check failed at original line 96')
            require(labels[edge] != labelsp[edge], 'independent check failed at original line 97')
    require(not incident("eRP"), 'independent check failed at original line 98')
    print(f"  dressed eAB: {dressed.tolist()} and {dressedp.tolist()}")
    print("  incident edges ePA, eRB, eAB agree; eRP does not meet {a, b}")


def check_noncommutative_order() -> None:
    print("[3/4] Noncommutative path product, later factor on the left.")
    labels = {
        "eRP": mat([[1, 1], [0, 1]]),
        "ePA": mat([[1, 0], [1, 1]]),
        "eRB": mat([[1, 3], [0, 1]]),
        "eAB": mat([[0, -1], [1, 0]]),
    }
    dressed = dress(labels, "eAB")
    expected = formula(labels)
    reversed_product = sp.simplify(
        labels["eRP"] * labels["ePA"] * labels["eAB"] * labels["eRB"].inv()
    )
    require(dressed == expected, 'independent check failed at original line 116')
    require(dressed != reversed_product, 'independent check failed at original line 117')
    require(dressed == mat([[-4, -5], [1, 1]]), 'independent check failed at original line 118')
    labelsp = dict(labels)
    labelsp["eRP"] = mat([[1, 2], [0, 1]])
    dressedp = dress(labelsp, "eAB")
    require(dressedp == formula(labelsp), 'independent check failed at original line 122')
    require(dressedp == mat([[-4, -9], [1, 2]]), 'independent check failed at original line 123')
    require(dressed != dressedp, 'independent check failed at original line 124')
    for edge in ("ePA", "eRB", "eAB"):
        require(labels[edge] == labelsp[edge], 'independent check failed at original line 126')
    print(f"  dressed eAB: {dressed.tolist()}")
    print(f"  after changing only eRP: {dressedp.tolist()}")
    print(f"  reversed product, not the dressing: {reversed_product.tolist()}")


def check_star_enumeration() -> None:
    print("[4/4] Closed star of a→b is {ePA, eRB, eAB}.")
    star = tuple(edge for edge in EDGES if incident(edge))
    require(star == ("ePA", "eRB", "eAB"), 'independent check failed at original line 135')
    require(EDGES["eRP"] == ("root", "p"), 'independent check failed at original line 136')
    print(f"  star: {star}")


def main() -> int:
    check_additive()
    check_identity_matrices()
    check_noncommutative_order()
    check_star_enumeration()
    print("checked: dressed chords 2 and 5; matrices [[1,1],[0,1]] vs [[1,2],[0,1]];")
    print("checked: noncommutative dressed [[-4,-5],[1,1]] vs [[-4,-9],[1,2]];")
    print("checked: eRP lies outside the closed star of a→b.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
