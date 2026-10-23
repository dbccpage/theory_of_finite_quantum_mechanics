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
    require(d2 == 2, 'dressed additive chord for outer label 2 is 2')
    require(d5 == 5, 'dressed additive chord for outer label 5 is 5')
    require(d2 != d5, 'equal closed-star labels with outer labels 2 and 5 dress unequal chords')
    print(f"  dressed chords: {d2} and {d5}")


def check_identity_matrices() -> None:
    print("[2/4] Matrix witness with trivial star labels.")
    x = mat([[1, 1], [0, 1]])
    xp = mat([[1, 2], [0, 1]])
    labels = {"eRP": x, "ePA": eye(), "eRB": eye(), "eAB": eye()}
    labelsp = {"eRP": xp, "ePA": eye(), "eRB": eye(), "eAB": eye()}
    dressed = dress(labels, "eAB")
    dressedp = dress(labelsp, "eAB")
    require(dressed == x, 'identity-matrix dressed chord equals the outer matrix')
    require(dressedp == xp, 'dressed chord after changing only eRP equals the new outer matrix')
    require(dressed != dressedp, 'the two identity-matrix dressings differ')
    for edge in EDGES:
        if incident(edge):
            require(labels[edge] == labelsp[edge], f'incident edge {edge} agrees across the two labelings')
        else:
            require(edge == "eRP", f'{edge} is outside the closed star and must be eRP')
            require(labels[edge] != labelsp[edge], 'eRP is the only edge whose label changes')
    require(not incident("eRP"), 'eRP does not meet the closed star of a to b')
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
    require(dressed == expected, 'dressed chord equals the later-on-the-left formula')
    require(dressed != reversed_product, 'dressed chord is not the reversed product')
    require(dressed == mat([[-4, -5], [1, 1]]), 'dressed chord is [[-4, -5], [1, 1]]')
    labelsp = dict(labels)
    labelsp["eRP"] = mat([[1, 2], [0, 1]])
    dressedp = dress(labelsp, "eAB")
    require(dressedp == formula(labelsp), 'dressed chord after changing eRP still matches the formula')
    require(dressedp == mat([[-4, -9], [1, 2]]), 'dressed chord after changing eRP is [[-4, -9], [1, 2]]')
    require(dressed != dressedp, 'changing only the outer edge changes the dressed chord')
    for edge in ("ePA", "eRB", "eAB"):
        require(labels[edge] == labelsp[edge], f'incident edge {edge} is unchanged when only eRP changes')
    print(f"  dressed eAB: {dressed.tolist()}")
    print(f"  after changing only eRP: {dressedp.tolist()}")
    print(f"  reversed product, not the dressing: {reversed_product.tolist()}")


def check_star_enumeration() -> None:
    print("[4/4] Closed star of a→b is {ePA, eRB, eAB}.")
    star = tuple(edge for edge in EDGES if incident(edge))
    require(star == ("ePA", "eRB", "eAB"), 'closed star of a to b is ePA, eRB, eAB')
    require(EDGES["eRP"] == ("root", "p"), 'eRP runs from root to p')
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
