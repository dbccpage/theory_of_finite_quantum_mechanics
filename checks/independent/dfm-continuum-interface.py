#!/usr/bin/env python3
"""Independent check for DFM-CONTINUUM-INTERFACE.

Recomputes the supplied rooted-tree dressing of one chord without importing
repository code. Group multiplication is later-on-the-left, matching
FiniteGraphDressing.transport of an appended walk.

Exits 0 on success.
"""

from __future__ import annotations

import sympy as sp


VERTICES = ("root", "p", "a", "b")
EDGES = {
    "eRP": ("root", "p"),
    "ePA": ("p", "a"),
    "eRB": ("root", "b"),
    "eAB": ("a", "b"),
}
TREE_PATH = {
    "root": (),
    "p": ("eRP",),
    "a": ("eRP", "ePA"),
    "b": ("eRB",),
}


def mat(rows):
    return sp.Matrix(rows)


def eye():
    return sp.eye(2)


def transport(labels, path):
    value = eye()
    for edge in path:
        value = labels[edge] * value
    return value


def dress(labels, edge):
    src, dst = EDGES[edge]
    u_src = transport(labels, TREE_PATH[src]).inv()
    u_dst = transport(labels, TREE_PATH[dst]).inv()
    return sp.simplify(u_dst * labels[edge] * u_src.inv())


def formula(labels):
    return sp.simplify(
        labels["eRB"].inv() * labels["eAB"] * labels["ePA"] * labels["eRP"]
    )


def incident(edge):
    src, dst = EDGES[edge]
    return src in ("a", "b") or dst in ("a", "b")


def additive_dress(x_rp, x_pa, x_rb, x_ab):
    """Integers under addition. Later-on-the-left is ordinary sum."""
    t_a = x_pa + x_rp
    t_b = x_rb
    return (-t_b) + x_ab + t_a


def check_additive():
    print("[1/4] Additive witness: outer labels 2 and 5, other labels 0.")
    d2 = additive_dress(2, 0, 0, 0)
    d5 = additive_dress(5, 0, 0, 0)
    assert d2 == 2, d2
    assert d5 == 5, d5
    assert d2 != d5
    print(f"  dressed chords: {d2} and {d5}")


def check_identity_matrices():
    print("[2/4] Matrix witness with trivial star labels.")
    x = mat([[1, 1], [0, 1]])
    xp = mat([[1, 2], [0, 1]])
    labels = {"eRP": x, "ePA": eye(), "eRB": eye(), "eAB": eye()}
    labelsp = {"eRP": xp, "ePA": eye(), "eRB": eye(), "eAB": eye()}
    dressed = dress(labels, "eAB")
    dressedp = dress(labelsp, "eAB")
    assert dressed == x
    assert dressedp == xp
    assert dressed != dressedp
    for edge in EDGES:
        if incident(edge):
            assert labels[edge] == labelsp[edge]
        else:
            assert edge == "eRP"
            assert labels[edge] != labelsp[edge]
    assert not incident("eRP")
    print(f"  dressed eAB: {dressed.tolist()} and {dressedp.tolist()}")
    print("  incident edges ePA, eRB, eAB agree; eRP does not meet {a, b}")


def check_noncommutative_order():
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
    assert dressed == expected
    assert dressed != reversed_product
    assert dressed == mat([[-4, -5], [1, 1]])
    labelsp = dict(labels)
    labelsp["eRP"] = mat([[1, 2], [0, 1]])
    dressedp = dress(labelsp, "eAB")
    assert dressedp == formula(labelsp)
    assert dressedp == mat([[-4, -9], [1, 2]])
    assert dressed != dressedp
    for edge in ("ePA", "eRB", "eAB"):
        assert labels[edge] == labelsp[edge]
    print(f"  dressed eAB: {dressed.tolist()}")
    print(f"  after changing only eRP: {dressedp.tolist()}")
    print(f"  reversed product, not the dressing: {reversed_product.tolist()}")


def check_star_enumeration():
    print("[4/4] Closed star of a→b is {ePA, eRB, eAB}.")
    star = tuple(edge for edge in EDGES if incident(edge))
    assert star == ("ePA", "eRB", "eAB")
    assert EDGES["eRP"] == ("root", "p")
    print(f"  star: {star}")


def main():
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
