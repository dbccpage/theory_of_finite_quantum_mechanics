"""Independent check for PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT.

Recomputes the one-triangle slot swap, face column, 02 sign, vertex cycle,
and the identity triD1 of triD0 = 0. Does not import repository code.
"""

from __future__ import annotations

import re
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2] / "lean4" / "CampaignPgwWdpIncidenceOrientationTransport.lean"
THEOREMS = [
    "pgwInc_swap_involutive",
    "pgwInc_face_swapped",
    "pgwInc_row",
    "pgwInc_face_is_row",
    "pgwInc_face_cyclic",
    "pgwInc_transported_cycle",
    "pgwInc_dot_matches_order",
    "pgwInc_swapped_coord_is_tri",
    "pgwInc_face_tri",
    "pgwInc_int_d1_d0",
    "pgwInc_rat_telescope",
    "pgwInc_d1_d0",
]


def swap23(a, b, c):
    return (a, c, b)


def reverse02(a01, a12, a02):
    return (a01, a12, -a02)


def d2(w):
    return (w, -w, w)


def vertex_boundary(a01, a12, a02):
    return (-a01 - a02, a01 - a12, a12 + a02)


def tri_d1(a01, a12, a02):
    return a01 + a12 - a02


def tri_d0(f0, f1, f2):
    return (f1 - f0, f2 - f1, f2 - f0)


def main() -> int:
    failures = 0
    claims = 0

    def check(ok: bool, label: str) -> None:
        nonlocal failures, claims
        claims += 1
        if not ok:
            failures += 1
            print("FAIL", label)

    face = d2(1)
    check(face == (1, -1, 1), "face column (1, -1, 1)")
    swapped = swap23(*face)
    check(swapped == (1, 1, -1), "swapped face (1, 1, -1)")
    check(swap23(*swapped) == face, "swap is an involution on the face")
    check(swap23(4, 5, 6) == (4, 6, 5) and swap23(4, 6, 5) == (4, 5, 6), "swap involution on 4, 5, 6")
    check(swapped == (1, 1, -1), "matches triD1Row (1, 1, -1)")
    cyclic = reverse02(*swapped)
    check(cyclic == (1, 1, 1), "02 reversal sends the row to (1, 1, 1)")
    check(vertex_boundary(*swapped) == (0, 0, 0), "vertex boundary is 0, 0, 0")
    check(tri_d1(*swapped) == 3, "triD1 of the swapped face row is 3")
    check(tri_d1(*swapped) != 0, "triD1 of the row is not the vertex cycle")
    for a01, a02, a12 in ((1, -1, 1), (2, 3, 5), (-4, 7, 0)):
        dot = a01 * 1 + a02 * (-1) + a12 * 1
        check(dot == a01 + a12 - a02, f"dot matches order for {a01}, {a02}, {a12}")
        check(tri_d1(a01, a12, a02) == a01 + a12 - a02, f"triD1 after swap for {a01}, {a12}, {a02}")
    for f0, f1, f2 in ((0, 0, 0), (1, 2, 3), (-5, 4, 1), (8, -2, 6)):
        a01, a12, a02 = tri_d0(f0, f1, f2)
        check(tri_d1(a01, a12, a02) == 0, f"triD1 triD0 is 0 for {f0}, {f1}, {f2}")
        check((f1 - f0) + (f2 - f1) - (f2 - f0) == 0, f"integer telescope for {f0}, {f1}, {f2}")
    # Algebraic cancellation, exact integers standing for the three coordinates.
    f0, f1, f2 = 11, 13, 17
    check((f1 - f0) + (f2 - f1) - (f2 - f0) == 0, "telescope on 11, 13, 17")
    text = LEAN.read_text(encoding="utf-8")
    lines = text.splitlines()
    check("\r" not in text, "lean file has no CR")
    for name in THEOREMS:
        check(any(line.startswith(f"theorem {name}") or line.startswith(f"def {name}") for line in lines), f"decl {name}")
        prints = [line for line in lines if line == f"#print axioms {name}"]
        check(len(prints) == 1, f"print {name}")
    for index, line in enumerate(lines, 1):
        code = line.split("--", 1)[0]
        if code.strip().startswith("#print"):
            continue
        for token in ("sorry", "admit", "axiom", "native_decide", "unsafe"):
            if re.search(rf"(?<![\w.']){token}(?![\w'])", code):
                check(False, f"forbidden {token} on line {index}")
    print(f"checked {claims} claims, failures {failures}")
    print("swapped", swapped, "cyclic", cyclic, "boundary", vertex_boundary(*swapped), "row_tri", tri_d1(*swapped))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
