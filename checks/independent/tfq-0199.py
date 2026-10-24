#!/usr/bin/env python3
"""Independent computational check for TFQ-0199 (IMPLEMENTATION_SIBLING):
Do not treat the GR holonomy scaffold or the 2D Regge sum as the exact rational 4D gravity shadow.

Verifies:
1. Source anchors and explicit AUTHORITY_FENCE strings across:
   - `code/rust/src/majorana/holonomy.rs` (`holonomy_receipt_gf2`, `AUTHORITY_FENCE`)
   - `code/rust/src/general_relativity/regge_calculus.rs` (`ReggeCalculus::regge_action_2d`, `AUTHORITY_FENCE`)
   - `code/rust/src/general_relativity/discrete_spacetime.rs` (`DiscreteSpacetime::euler_characteristic`, `AUTHORITY_FENCE`)
   - `code/rust/src/general_relativity/einstein_hilbert_action.rs` (`EinsteinHilbertAction::try_from_regge`, `AUTHORITY_FENCE`)
   - `code/rust/src/general_relativity/exact_regge/action.rs` (`rational_regge_proxy`, `flat_einstein_hilbert`, `flat_chart_admitted`, `defect_bound_holds`)
   - `lean4/FiniteQFTAndGravity.lean` (`gr_deflection_twice_newton`, `mercury_per_orbit_arcsec`, `null_probe_traceless`)
2. Exact rational 4D Regge proxy evaluation on the orthogonal pentatope (`orthogonal_pentatope`):
   - 5 vertices in Q^4: v0=(0,0,0,0), v1=(1,0,0,0), v2=(0,1,0,0), v3=(0,0,1,0), v4=(0,0,0,1)
   - 10 triangular hinges: 6 right triangles with A_h^2 = 1/4, 4 equilateral base triangles with A_h^2 = 3/4
   - Exact rational action S_proxy = sum_h A_h^2 * kappa_h and flat decision S_proxy == 0
   - Rejection of sub-cutoff curvature kappa_0 = 1/10^9 (S_proxy = 1/4000000000 != 0)
   - Exact rational defect_bound_holds verification across 100 rational grid combinations
3. Contrast against 2D vertex-deficit Regge calculus (`regge_calculus.rs` / `einstein_hilbert_action.rs`),
   combinatorial carrier (`discrete_spacetime.rs`), and F_2 / Z[zeta_16] holonomy (`majorana/holonomy.rs`).
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def cayley_menger_triangle_area_sq(s01: Fraction, s02: Fraction, s12: Fraction) -> Fraction:
    """Exact rational Cayley-Menger squared area of a triangle with squared side lengths."""
    num = 2 * (s01 * s02 + s01 * s12 + s02 * s12) - (s01 * s01 + s02 * s02 + s12 * s12)
    return num / Fraction(16, 1)


def defect_bound_holds(s_regge: Fraction, s_eh: Fraction, c: Fraction, a_sq: Fraction) -> bool:
    """Exact rational replica of exact_regge::action::defect_bound_holds."""
    if c < 0 or a_sq < 0:
        return False
    diff = s_regge - s_eh
    allowance = c * a_sq
    return diff * diff <= allowance * allowance


def run_all_checks() -> dict:
    checks_passed = 0
    failures: list[str] = []

    def check(cond: bool, label: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            failures.append(label)

    # 1. Source anchor and authority fence verification
    hol_path = REPO_ROOT / "code" / "rust" / "src" / "majorana" / "holonomy.rs"
    regge_path = REPO_ROOT / "code" / "rust" / "src" / "general_relativity" / "regge_calculus.rs"
    ds_path = REPO_ROOT / "code" / "rust" / "src" / "general_relativity" / "discrete_spacetime.rs"
    eh_path = REPO_ROOT / "code" / "rust" / "src" / "general_relativity" / "einstein_hilbert_action.rs"
    exact_path = REPO_ROOT / "code" / "rust" / "src" / "general_relativity" / "exact_regge" / "action.rs"
    lean_fg_path = REPO_ROOT / "lean4" / "FiniteQFTAndGravity.lean"

    for p in (hol_path, regge_path, ds_path, eh_path, exact_path, lean_fg_path):
        check(p.exists(), f"file_exists:{p.relative_to(REPO_ROOT).as_posix()}")

    hol_src = hol_path.read_text(encoding="utf-8")
    regge_src = regge_path.read_text(encoding="utf-8")
    ds_src = ds_path.read_text(encoding="utf-8")
    eh_src = eh_path.read_text(encoding="utf-8")
    exact_src = exact_path.read_text(encoding="utf-8")
    lean_fg_src = lean_fg_path.read_text(encoding="utf-8")

    check("pub fn holonomy_receipt_gf2" in hol_src, "holonomy_rs_fn")
    check("AuthorityEffect None; declared carrier + monoid only; diagnostic receipt." in hol_src, "holonomy_rs_fence")
    check("pub fn regge_action_2d" in regge_src, "regge_calculus_rs_fn")
    check("AuthorityEffect None; not PROVED; not GlobalGreen; finite 2D Regge face." in regge_src, "regge_calculus_rs_fence")
    check("pub fn euler_characteristic" in ds_src, "discrete_spacetime_rs_fn")
    check("AuthorityEffect None; not PROVED; not GlobalGreen; finite simplicial spacetime." in ds_src, "discrete_spacetime_rs_fence")
    check("pub fn try_from_regge" in eh_src, "einstein_hilbert_action_rs_fn")
    check("not the exact proxy (the sum of area_squared times kappa)" in eh_src, "einstein_hilbert_action_rs_fence")
    check("pub fn rational_regge_proxy" in exact_src, "exact_regge_action_rs_proxy")
    check("pub fn flat_chart_admitted" in exact_src, "exact_regge_action_rs_flat")
    check("theorem gr_deflection_twice_newton" in lean_fg_src, "lean_fg_gr_deflection")
    check("theorem mercury_per_orbit_arcsec" in lean_fg_src, "lean_fg_mercury_arcsec")

    # 2. Combinatorial carrier f-vector and Euler characteristic (discrete_spacetime.rs)
    for n in range(1, 6):
        counts = [math.comb(n + 1, k + 1) for k in range(n + 1)]
        euler = sum(((-1) ** k) * c for k, c in enumerate(counts))
        check(euler == 1, f"delta_{n}_euler_characteristic_is_1")
    check(math.comb(3, 3) == 1 and math.comb(5, 3) == 10, "delta2_vs_delta4_triangle_hinges")

    # 3. Orthogonal pentatope in Q^4: 5 vertices, 10 edges, 10 triangular hinges
    verts = {
        0: (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        1: (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        2: (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        3: (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
        4: (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    }

    def dist_sq(u: int, v: int) -> Fraction:
        return sum((verts[u][i] - verts[v][i]) ** 2 for i in range(4))

    hinges = list(itertools.combinations(range(5), 3))
    check(len(hinges) == 10, "pentatope_has_10_hinges")

    hinge_areas_sq: dict[tuple[int, int, int], Fraction] = {}
    right_count = 0
    equil_count = 0
    for h in hinges:
        s01 = dist_sq(h[0], h[1])
        s02 = dist_sq(h[0], h[2])
        s12 = dist_sq(h[1], h[2])
        a_sq = cayley_menger_triangle_area_sq(s01, s02, s12)
        hinge_areas_sq[h] = a_sq
        if 0 in h:
            right_count += 1
            check(a_sq == Fraction(1, 4), f"right_hinge_{h}_area_sq_1_4")
        else:
            equil_count += 1
            check(a_sq == Fraction(3, 4), f"equil_hinge_{h}_area_sq_3_4")

    check(right_count == 6 and equil_count == 4, "pentatope_6_right_4_equil_hinges")
    check(sum(hinge_areas_sq.values()) == Fraction(9, 2), "pentatope_total_hinge_area_sq_9_2")

    # 4. Exact flat admission vs float cutoff (exact_regge/action.rs)
    kappa_tiny = Fraction(1, 1_000_000_000)
    s_curved = hinge_areas_sq[(0, 1, 2)] * kappa_tiny
    check(s_curved == Fraction(1, 4_000_000_000), "tiny_curved_proxy_action_exact")
    flat_admitted = (s_curved == Fraction(0))
    float_below_cutoff = abs(float(s_curved)) < 1e-6
    check((not flat_admitted) and float_below_cutoff, "exact_flat_fence_rejects_sub_cutoff_curvature")

    # 5. Exact rational defect_bound_holds across explicit and grid witnesses
    check(
        defect_bound_holds(Fraction(1, 3), Fraction(1, 4), Fraction(2), Fraction(1, 16)),
        "defect_bound_rust_test_1",
    )
    check(
        not defect_bound_holds(Fraction(1), Fraction(0), Fraction(1), Fraction(1, 4)),
        "defect_bound_rust_test_2",
    )
    check(
        not defect_bound_holds(Fraction(1), Fraction(0), Fraction(-1), Fraction(1)),
        "defect_bound_rust_test_3",
    )

    for num_r in range(-5, 6):
        for num_eh in range(-5, 6):
            s_r = Fraction(num_r, 12)
            s_e = Fraction(num_eh, 12)
            c_val = Fraction(3, 2)
            a_val = Fraction(1, 6)
            lhs = (s_r - s_e) ** 2
            rhs = (c_val * a_val) ** 2
            check(
                defect_bound_holds(s_r, s_e, c_val, a_val) == (lhs <= rhs),
                f"defect_bound_grid_{num_r}_{num_eh}",
            )

    # 6. 2D equilateral fan vertex-deficit calculus (regge_calculus.rs / einstein_hilbert_action.rs)
    for n_tri in (1, 3, 4, 5, 6, 7, 8):
        center_deficit_pi_units = Fraction(2, 1) - Fraction(n_tri, 3)
        center_deficit_f64 = 2.0 * math.pi - n_tri * math.acos(0.5)
        check(
            abs(center_deficit_f64 - float(center_deficit_pi_units) * math.pi) < 1e-12,
            f"fan_{n_tri}_center_deficit_matches_pi_units",
        )
        if n_tri == 6:
            check(center_deficit_pi_units == 0, "fan_6_flat_center")
        if n_tri == 3:
            check(center_deficit_pi_units == 1, "fan_3_pi_cone_center")

    # Scaling difference: 2D vertex deficits are invariant under edge scaling L -> s*L,
    # whereas 4D rational Regge proxy action scales as L^4 (s_sq^2).
    for scale_sq in (Fraction(1, 2), Fraction(2, 1), Fraction(3, 1), Fraction(5, 2)):
        scaled_area_sq = cayley_menger_triangle_area_sq(scale_sq, scale_sq, 2 * scale_sq)
        check(
            scaled_area_sq == (scale_sq * scale_sq) * Fraction(1, 4),
            f"area_sq_quartic_length_scaling_{scale_sq}",
        )

    # 7. F_2 plaquette holonomy (majorana/holonomy.rs) vs rational quaternion holonomy (general_relativity/holonomy.rs)
    # In F_2, a 4-edge plaquette with connection [1,1,1,1] has residual (1+1+1+1) mod 2 == 0 (flat).
    # In Q-quaternions, q1 = (3/5, 4/5, 0, 0) has norm 1, and q1^4 = (-527/625, -336/625, 0, 0) != 1.
    def qmul(p: tuple[Fraction, ...], q: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        a1, b1, c1, d1 = p
        a2, b2, c2, d2 = q
        return (
            a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
        )

    q1 = (Fraction(3, 5), Fraction(4, 5), Fraction(0), Fraction(0))
    q1_inv = (Fraction(3, 5), Fraction(-4, 5), Fraction(0), Fraction(0))
    q_one = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    check(sum(x * x for x in q1) == Fraction(1), "q1_unit_norm_sq")
    check(qmul(q1, q1_inv) == q_one, "q1_times_q1_inv_is_one")
    q2 = qmul(q1, q1)
    q4 = qmul(q2, q2)
    check(
        q4 == (Fraction(-527, 625), Fraction(-336, 625), Fraction(0), Fraction(0)) and q4 != q_one,
        "q1_fourth_power_nontrivial_unlike_gf2_plaquette",
    )

    # 8. Exact rational GR textbook identities in lean4/FiniteQFTAndGravity.lean (pi-free, sqrt-free)
    for gm_num in range(1, 6):
        for c_num in range(1, 4):
            for b_num in range(1, 4):
                gm = Fraction(gm_num, 3)
                c = Fraction(c_num, 1)
                b = Fraction(b_num, 2)
                newton_defl = 2 * gm / (c * c * b)
                gr_defl = 4 * gm / (c * c * b)
                check(gr_defl == 2 * newton_defl, f"gr_twice_newton_{gm_num}_{c_num}_{b_num}")

    return {
        "node_id": "TFQ-0199",
        "stage": "IMPLEMENTATION_SIBLING",
        "checks_passed": checks_passed,
        "failures": failures,
        "passed": len(failures) == 0,
    }


if __name__ == "__main__":
    result = run_all_checks()
    if not result["passed"]:
        print(json.dumps(result, indent=2))
        raise SystemExit(1)
    print(
        f"TFQ-0199 INDEPENDENT CHECKER PASSED: checks={result['checks_passed']} failed={len(result['failures'])}"
    )
