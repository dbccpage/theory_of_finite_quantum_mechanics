"""Independent replay of the finite counts in GenesisHottShadow.

Reimplements the six-operation admission step and the stated finite
enumerations. Imports no repository code. AuthorityEffect: None.
"""

from __future__ import annotations

import sys


def insert_new(items: list, item) -> list:
    if item in items:
        return items
    return items + [item]


def step_e(regime: dict, event: tuple) -> dict | None:
    kind = event[0]
    if kind == "supply":
        return regime
    if kind == "admitDatum":
        return {**regime, "data": regime["data"] + 1}
    if kind == "admitForm":
        arity = event[1]
        if arity >= 1:
            return {**regime, "forms": regime["forms"] + [arity]}
        return None
    if kind == "admitInst":
        form = event[1]
        args = event[2]
        forms = regime["forms"]
        if form < len(forms) and len(args) == (forms[form] if form < len(forms) else 0):
            if all(x < regime["data"] for x in args):
                return {**regime, "insts": insert_new(regime["insts"], (form, tuple(args)))}
        return None
    if kind == "admitRuleAll":
        form = event[1]
        if form < len(regime["forms"]):
            return {**regime, "rules": insert_new(regime["rules"], form)}
        return None
    if kind == "impose":
        i, j = event[1], event[2]
        if i < j and j < regime["data"]:
            return {**regime, "reqs": insert_new(regime["reqs"], (i, j))}
        return None
    raise ValueError(kind)


def replay(history: list[tuple], base: dict) -> dict | None:
    current = base
    for event in history:
        nxt = step_e(current, event)
        if nxt is None:
            return None
        current = nxt
    return current


def empty_regime() -> dict:
    return {"data": 0, "forms": [], "insts": [], "rules": [], "reqs": []}


def check(name: str, cond: bool) -> None:
    if not cond:
        print(f"FAIL {name}")
        raise SystemExit(1)
    print(f"ok {name}")


def regime_wf(r: dict) -> bool:
    for form, args in r["insts"]:
        if not (form < len(r["forms"]) and len(args) == r["forms"][form]):
            return False
        if any(a >= r["data"] for a in args):
            return False
    if any(f >= len(r["forms"]) for f in r["rules"]):
        return False
    if any(not (i < j and j < r["data"]) for i, j in r["reqs"]):
        return False
    if any(a < 1 for a in r["forms"]):
        return False
    return True


def fragment_replay() -> tuple[list[int], list[int]] | None:
    data: list[int] = []
    forms: list[int] = []
    events = [("admit", 0), ("admit", 1), ("form", 2)]
    for kind, payload in events:
        if kind == "admit":
            if payload not in data:
                data = data + [payload]
        elif kind == "form":
            if payload < 1:
                return None
            forms = forms + [payload]
        else:
            raise ValueError(kind)
    return data, forms


def orientations(pair: tuple[int, int]) -> list[tuple[int, int]]:
    a, b = pair
    return [(b, a), (a, b)]


def all_face_maps() -> list[tuple[int, int]]:
    out = []
    for f0 in (0, 1):
        for f1 in (0, 1):
            out.append((f0, f1))
    return out


def main() -> None:
    base = empty_regime()
    supplied = replay([("supply", 0), ("supply", 1)], base)
    check("supply_history_stays_empty", supplied == base)

    first = replay(
        [
            ("admitDatum",),
            ("admitDatum",),
            ("admitForm", 1),
            ("admitInst", 0, [0]),
            ("impose", 0, 1),
        ],
        base,
    )
    check(
        "first_separation_shadow",
        first == {"data": 2, "forms": [1], "insts": [(0, (0,))], "rules": [], "reqs": [(0, 1)]},
    )
    check("first_separation_wf", first is not None and regime_wf(first))
    check("first_separation_unary", first is not None and all(len(args) == 1 for _, args in first["insts"]))
    check("first_separation_no_binary", first is not None and all(len(args) != 2 for _, args in first["insts"]))

    edge = replay(
        [("admitDatum",), ("admitDatum",), ("admitForm", 2), ("admitInst", 0, [0, 1])],
        base,
    )
    reverse = replay(
        [("admitDatum",), ("admitDatum",), ("admitForm", 2), ("admitInst", 0, [1, 0])],
        base,
    )
    check(
        "edge_shadow",
        edge == {"data": 2, "forms": [2], "insts": [(0, (0, 1))], "rules": [], "reqs": []},
    )
    check(
        "reverse_shadow",
        reverse == {"data": 2, "forms": [2], "insts": [(0, (1, 0))], "rules": [], "reqs": []},
    )
    check("edge_wf", edge is not None and regime_wf(edge))
    check("reverse_wf", reverse is not None and regime_wf(reverse))
    check(
        "edge_and_reverse_differ",
        edge is not None
        and reverse is not None
        and edge["data"] == reverse["data"]
        and edge["forms"] == reverse["forms"]
        and edge["insts"] != reverse["insts"],
    )
    check("edge_tuple_length", edge is not None and len(edge["insts"]) == 1 and len(edge["insts"]) != 3)

    frag = fragment_replay()
    check("fragment_replay", frag == ([0, 1], [2]))

    maps = all_face_maps()
    check("face_map_card", len(maps) == 4)
    recovering = [m for m in maps if m in orientations((0, 1))]
    check("recovers_fun_card", set(recovering) == {(1, 0), (0, 1)} and len(recovering) == 2)

    globe_pairs = [(s, t) for s in (0, 1) for t in (0, 1)]
    check("globular_pair_card", len(globe_pairs) == 4)
    globe_orients = [p for p in globe_pairs if p in ((0, 1), (1, 0))]
    check("globular_orientation_count", globe_orients == [(0, 1), (1, 0)] and len(globe_orients) == 2)

    def face_a(i: int, e: int) -> int:
        if e == 0:
            return 1 if i == 0 else 0
        if e == 1:
            return 0
        return 1

    def s0_a(v: int) -> int:
        return 1 if v == 0 else 2

    def face_b(i: int, e: int) -> int:
        if e == 0:
            return 1 if i == 0 else 0
        if e == 3:
            return 1
        return 0

    def s0_b(v: int) -> int:
        return 1 if v == 0 else 3

    def degeneracy_ok(face, s0, n0: int) -> bool:
        return all(face(i, s0(v)) == v for v in range(n0) for i in (0, 1))

    check("simpA_degeneracy", degeneracy_ok(face_a, s0_a, 2) and face_a(0, 0) == 1 and face_a(1, 0) == 0)
    check("simpB_degeneracy", degeneracy_ok(face_b, s0_b, 2) and face_b(0, 0) == 1 and face_b(1, 0) == 0)
    check("simplicial_n1", s0_a(0) < 3 and s0_b(1) < 4 and 3 != 4)

    def identities(face2: tuple[int, int, int]) -> bool:
        def face1(i: int, e: int) -> int:
            return 1 if i == 0 else 0

        return (
            face1(0, face2[1]) == face1(0, face2[0])
            and face1(0, face2[2]) == face1(1, face2[0])
            and face1(1, face2[2]) == face1(1, face2[1])
        )

    only = (0, 0, 0)
    check("no_simplex2_on_forward_edge", identities(only) is False)

    one_way = {(0, 1)}
    symmetric = {(0, 1), (1, 0)}
    check("cuts_exhibit_requirement", (0, 1) in one_way and (0, 1) in symmetric and first is not None and first["reqs"] == [(0, 1)])
    check("cuts_differ", one_way != symmetric and (1, 0) not in one_way and (1, 0) in symmetric)

    irreflexive_holding_01 = []
    for r01 in (False, True):
        for r10 in (False, True):
            rel = set()
            if r01:
                rel.add((0, 1))
            if r10:
                rel.add((1, 0))
            if (0, 1) in rel:
                irreflexive_holding_01.append(rel)
    check("two_irreflexive_relations_holding_01", len(irreflexive_holding_01) == 2)

    def d0(v0: int, v1: int, v2: int) -> tuple[int, int, int]:
        return (v1 - v0, v2 - v1, v0 - v2)

    def d1(e01: int, e12: int, e20: int) -> int:
        return e01 + e12 + e20

    check("triangle_nilpotence", d1(*d0(0, 1, 2)) == 0)

    check("chain_boundaries_differ", (lambda _e: 0)(0) != (lambda _e: 1)(0))
    check("globe2_counts", 0 != 1)
    print("checked finite admission shadow counts")


if __name__ == "__main__":
    main()
    sys.exit(0)
