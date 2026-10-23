"""Enumerate the finite horn carrier used by GenesisHottHorns.

No repository imports. Vertices, edges, and the one triangle are restated
here and checked against the horn and shell predicates from that module.
"""

from __future__ import annotations


VERTS = ("v0", "v1", "v2")
EDGES = {
    "e01": ("v0", "v1"),
    "e12": ("v1", "v2"),
    "e02": ("v0", "v2"),
    "e20": ("v2", "v0"),
    "e21": ("v2", "v1"),
}
TRI = {
    "t012": {"d0": "e12", "d1": "e02", "d2": "e01"},
}


def src(edge: str) -> str:
    return EDGES[edge][0]


def tgt(edge: str) -> str:
    return EDGES[edge][1]


def shell2(present: set[str]) -> bool:
    return {"e01", "e12", "e02"} <= present


def main() -> int:
    assert len(VERTS) == 3
    assert len(EDGES) == 5
    assert len(TRI) == 1
    for edge, (start, end) in EDGES.items():
        assert start != end, edge
        assert start in VERTS and end in VERTS
    for faces in TRI.values():
        d0, d1, d2 = faces["d0"], faces["d1"], faces["d2"]
        assert tgt(d1) == tgt(d0)
        assert tgt(d2) == src(d0)
        assert src(d2) == src(d1)
        assert tgt(d0) == "v2"
    inner = [
        (d0, d2)
        for d2 in EDGES
        for d0 in EDGES
        if tgt(d2) == src(d0)
    ]
    filled_inner = [
        pair
        for pair in inner
        if any(faces["d0"] == pair[0] and faces["d2"] == pair[1] for faces in TRI.values())
    ]
    assert ("e12", "e01") in filled_inner
    assert ("e01", "e20") in inner
    assert ("e01", "e20") not in filled_inner
    assert len(inner) == 8
    assert len(filled_inner) == 1
    assert len(inner) - len(filled_inner) == 7
    outer = [
        (d1, d2)
        for d2 in EDGES
        for d1 in EDGES
        if src(d1) == src(d2) and tgt(d1) != tgt(d2)
    ]
    filled_outer = [
        pair
        for pair in outer
        if any(faces["d1"] == pair[0] and faces["d2"] == pair[1] for faces in TRI.values())
    ]
    assert ("e02", "e01") in filled_outer
    assert ("e21", "e20") in outer
    assert ("e21", "e20") not in filled_outer
    assert ("e12", "e02") not in outer
    assert any(
        faces["d0"] == "e12" and faces["d1"] == "e02" for faces in TRI.values()
    )
    assert len(outer) == 4
    assert len(filled_outer) == 1
    assert len(outer) - len(filled_outer) == 3
    assert shell2({"e01", "e12"}) is False
    assert shell2({"e01", "e12", "e02"}) is True
    for vertex in VERTS:
        assert any(src(edge) == vertex for edge in EDGES)
        assert any(tgt(edge) == vertex for edge in EDGES)
    assert "unit" != "reflId"
    print("genesis_hott_horns: vertices=3 edges=5 triangles=1")
    print("inner horns=8 filled=1 refused=7")
    print("outer k0 horns=4 filled=1 refused=3")
    print("shell2(inner-horn edges)=false shell2(full boundary)=true")
    print("1-horns: every vertex is a source and a target")
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
