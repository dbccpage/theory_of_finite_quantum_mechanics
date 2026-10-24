"""Independent check for the TFQ-0031 strong-coupling boundary.

Recomputes the lattice counts, the Creutz exponent identities, and the
cleared beta numerators. Reads the finite-map note and checks that the
named shelf file is absent. Imports no repository code.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "dag" / "research" / "qcd_beta0_wilson_confinement_finite_map.md"
SHELF = (
    ROOT
    / "omega_engine_atlas"
    / "coda_atlas"
    / "F002_continuum"
    / "S001_continuum_finite_shadow_bridge"
    / "shelf.yaml"
)

FAILURES: list[str] = []
CHECKED = 0


def check(name: str, ok: bool) -> None:
    global CHECKED
    CHECKED += 1
    if not ok:
        FAILURES.append(name)


def beta0_num(n: int) -> int:
    return 33 - 2 * n


def beta1_num(n: int) -> int:
    return 306 - 38 * n


def area_ok(r: int, t: int) -> bool:
    return (r + 1) * (t + 1) + r * t == (r + 1) * t + r * (t + 1) + 1


def perim_ok(r: int, t: int) -> bool:
    return 2 * ((r + 1) + (t + 1)) + 2 * (r + t) == 2 * ((r + 1) + t) + 2 * (
        r + (t + 1)
    )


def main() -> None:
    check("vertices", 3 * 3 == 9)
    check("edges", 3 * 2 + 3 * 2 == 12)
    check("tree", 9 - 1 == 8)
    check("betti", 12 - 9 + 1 == 4)
    check("beta_tilde_den", 2 * (3 * 3) == 18)
    check("beta_tilde_reduced", 2 == 1 * 2 and 2 * (3 * 3) == 9 * 2)
    check("gluon_numerator", 11 * 3 == 33)
    check("quark_fraction", 4 * 3 == 2 * 6)
    for r in range(0, 9):
        for t in range(0, 9):
            check(f"area_{r}_{t}", area_ok(r, t))
            check(f"perim_{r}_{t}", perim_ok(r, t))
    for (side_r, side_t, area_lhs, perim_lhs) in (
        (2, 2, 5, 12),
        (2, 3, 8, 16),
        (3, 2, 8, 16),
        (3, 3, 13, 20),
    ):
        r, t = side_r - 1, side_t - 1
        check(f"pair_area_{side_r}{side_t}", area_ok(r, t) and (r + 1) * (t + 1) + r * t == area_lhs)
        check(
            f"pair_perim_{side_r}{side_t}",
            perim_ok(r, t)
            and 2 * ((r + 1) + (t + 1)) + 2 * (r + t) == perim_lhs,
        )
    samples = {0: 33, 3: 27, 5: 23, 6: 21, 16: 1, 17: -1}
    for n, expected in samples.items():
        check(f"beta0_{n}", beta0_num(n) == expected)
    window = [beta0_num(n) for n in range(17)]
    check(
        "beta0_window",
        window == [33, 31, 29, 27, 25, 23, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3, 1],
    )
    check("beta0_window_positive", all(value > 0 for value in window))
    check("beta0_ratios", 33 == 11 * 3 and 27 == 9 * 3 and 21 == 7 * 3 and 1 * 3 == 3 and (-1) * 3 == -3)
    check("beta1_16", beta1_num(16) == -302)
    check("banks_zaks", -beta0_num(16) * 302 == beta1_num(16) == -302)
    text = MAP.read_text(encoding="utf-8")
    start = text.find("Does not support a continuum")
    window_text = text[start : start + 240] if start >= 0 else ""
    check("withhold_present", start >= 0)
    check("withhold_mass_gap", "mass-gap existence proof" in window_text)
    check("withhold_limit", "non-perturbative confinement in the continuum limit" in window_text)
    check("withhold_weak", "at weak coupling" in window_text)
    check("withhold_spacing", "$a \\to 0$" in window_text)
    check("map_vertices", "|V| = 9" in text and "|E| = 12" in text)
    check("map_tree", "|E_T| = |V| - 1 = 8" in text)
    check("map_betti", "b_1(G) = |E| - |V| + 1 = 4" in text)
    check("map_one_ninth", "= 1/9" in text)
    check("map_beta0_16", "\\beta_0(3, 16) = 1/3" in text)
    check("map_beta1", "\\beta_1 = -302/3" in text)
    check("map_banks", "= 1/302" in text)
    check("shelf_absent", not SHELF.exists())
    named = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name not in {".git", ".lake", "__pycache__"}]
        if "named_adjoining.yaml" in filenames:
            named.append(str(Path(dirpath) / "named_adjoining.yaml"))
    check("named_adjoining_absent", named == [])
    print(f"checked {CHECKED} claims, failures {len(FAILURES)}")
    if FAILURES:
        for name in FAILURES:
            print("FAIL", name)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
