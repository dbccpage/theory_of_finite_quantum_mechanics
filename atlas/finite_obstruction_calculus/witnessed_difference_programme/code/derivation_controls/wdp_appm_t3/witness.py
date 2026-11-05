"""Exact witness for the 3D winding, linking, and character-orthogonality carrier in derivation.md."""

from __future__ import annotations

from fractions import Fraction

Point3 = tuple[int, int, int]
Edge3 = tuple[Point3, Point3]


def _edge(a: Point3, b: Point3) -> Edge3:
    return (a, b) if a <= b else (b, a)


def plaquettes_3d() -> list[frozenset[Edge3]]:
    out: list[frozenset[Edge3]] = []
    for x in range(4):
        for y in range(4):
            for z in range(4):
                xp, yp, zp = (x + 1) % 4, (y + 1) % 4, (z + 1) % 4
                out.append(
                    frozenset(
                        (
                            _edge((x, y, z), (xp, y, z)),
                            _edge((xp, y, z), (xp, yp, z)),
                            _edge((xp, yp, z), (x, yp, z)),
                            _edge((x, yp, z), (x, y, z)),
                        )
                    )
                )
                out.append(
                    frozenset(
                        (
                            _edge((x, y, z), (x, yp, z)),
                            _edge((x, yp, z), (x, yp, zp)),
                            _edge((x, yp, zp), (x, y, zp)),
                            _edge((x, y, zp), (x, y, z)),
                        )
                    )
                )
                out.append(
                    frozenset(
                        (
                            _edge((x, y, z), (x, y, zp)),
                            _edge((x, y, zp), (xp, y, zp)),
                            _edge((xp, y, zp), (xp, y, z)),
                            _edge((xp, y, z), (x, y, z)),
                        )
                    )
                )
    return out


def generators_3d() -> list[frozenset[Edge3]]:
    out: list[frozenset[Edge3]] = []
    for a in range(4):
        for b in range(4):
            out.append(
                frozenset(_edge((i, a, b), ((i + 1) % 4, a, b)) for i in range(4))
            )
            out.append(
                frozenset(_edge((a, i, b), (a, (i + 1) % 4, b)) for i in range(4))
            )
            out.append(
                frozenset(_edge((a, b, i), (a, b, (i + 1) % 4)) for i in range(4))
            )
    return out


def hopf_loop(shift_x: int = 0, reverse: bool = False) -> list[tuple[Point3, Point3]]:
    pts = [
        (1 + shift_x, 1, -1),
        (1 + shift_x, 1, 0),
        (1 + shift_x, 1, 1),
        (3 + shift_x, 1, 1),
        (3 + shift_x, 1, 0),
        (3 + shift_x, 1, -1),
    ]
    edges: list[tuple[Point3, Point3]] = []
    for i in range(len(pts)):
        u, v = pts[i], pts[(i + 1) % len(pts)]
        edges.append((v, u) if reverse else (u, v))
    return edges


def linking_with_square_patch(directed_edges: list[tuple[Point3, Point3]]) -> int:
    total = 0
    for u, v in directed_edges:
        for p in (u, v):
            if p[2] == 0 and 0 <= p[0] <= 2 and 0 <= p[1] <= 2:
                if p[0] in (0, 2) or p[1] in (0, 2):
                    raise ValueError("loop intersects boundary C1 of spanning square")
        if u[0] == v[0] == 1 and u[1] == v[1] == 1:
            if u[2] == 0 and v[2] == 1:
                total += 1
            elif u[2] == 1 and v[2] == 0:
                total -= 1
    return total


def parity_character_sum(kx: int, ky: int, kz: int) -> int:
    total = 0
    for x in range(4):
        for y in range(4):
            for z in range(4):
                total += 1 if ((kx * x + ky * y + kz * z) % 2 == 0) else -1
    return total


def witness() -> dict[str, int | Fraction]:
    plaq = plaquettes_3d()
    gen = generators_3d()
    cycles = plaq + gen
    if len(set(cycles)) != len(cycles):
        raise RuntimeError("3D 4-cycle edge sets are not distinct")
    z = len(plaq) * 2
    n = len(gen) * 2
    orientations = 2 * len(cycles)
    nontrivial = [
        abs(parity_character_sum(kx, ky, kz))
        for kx in (0, 1)
        for ky in (0, 1)
        for kz in (0, 1)
        if (kx, ky, kz) != (0, 0, 0)
    ]
    return {
        "sites": 64,
        "cycles": len(cycles),
        "plaquettes": len(plaq),
        "generators": len(gen),
        "orientations": orientations,
        "Z": z,
        "N": n,
        "average_sign": Fraction(z, orientations),
        "expectation": Fraction(n, z),
        "hopf_linking": linking_with_square_patch(hopf_loop(0, False)),
        "reversed_linking": linking_with_square_patch(hopf_loop(0, True)),
        "shifted_linking": linking_with_square_patch(hopf_loop(2, False)),
        "trivial_character_sum": parity_character_sum(0, 0, 0),
        "max_nontrivial_character_residual": max(nontrivial),
    }


def reject_pinned_t3_string_only_claim(claim: str) -> None:
    if "10^-25" in claim or "Dirac functional determinant" in claim:
        raise ValueError("pinned string labels and 10^-25 residual are not derived from this 3D carrier")
