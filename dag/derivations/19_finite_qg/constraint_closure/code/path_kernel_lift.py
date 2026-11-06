"""FOC-012 path kernels and PO-011 χ=1 product, on the GR-002 walk.

AuthorityEffect: None. Stdlib only.

Unique-path G1: one geodesic per shell, remaining 2d capacity 1/n,
slice w(n)=1/(n(n+1)), sum 1 at L1. That is obstruction removal, not
a path-integral.

Many-path: |Ω|>1, evaluated path kernel
Z = Σ_γ E(γ) exp(-β A[γ]). Composition is a product over a declared
cut only under G1–G3. FOC-012 refuses Born, phase, and interference;
the Hilbert/Born reading is a named lift, not a theorem of that paper.

χ=1: product state, no inter-site bond. PO-011 Lemma 5.3: one-local
gates stay in the product tangent (n_e=0). A supplied two-site
interaction with n_e ≠ 0 forces χ>1. Mapping the triangle face or any
particle to that interaction is additional data and is not proved here.

Local k=6, ε=0 is green. Composing those greens into “the wall is α”
is red. Δ_E = E_g − E_1 E_2 = −1. Defining E_g as the local product
is the FOC-012 false-green collapse; we do not.
"""

from __future__ import annotations

import math
from typing import Any

from regge_alpha_wall import (
    _hex_norm,
    hex_vertices,
    hex_wall_deficit_units,
    l1_unity,
    triangles_at,
    w_obstruction_removal,
)



def delta_eval(e1: int, e2: int, eg: int) -> int:
    """Δ_E = E_g − E_1 E_2. Restricted to {-1,0,1} for binary evaluators."""
    if e1 not in (0, 1) or e2 not in (0, 1) or eg not in (0, 1):
        raise ValueError("binary evaluators")
    return eg - e1 * e2


def path_kernel(n_accepted: int, action: float, beta: float) -> float:
    """Z for n_accepted equal-cost paths. β=0 ⇒ Z is a count."""
    if n_accepted < 0:
        raise ValueError("n_accepted")
    return n_accepted * math.exp(-beta * action)


def compose_under_g1g2g3(z_cb: float, z_ba: float) -> float:
    """Kernel composition when G1–G3 hold: Z(c|a) = Z(c|b) Z(b|a)."""
    return z_cb * z_ba


def unique_path_l1(n_max: int = 2000) -> dict[str, Any]:
    """G1 with |Ω(0,n)|=1: capacity slices, not a kernel sum."""
    s = 0.0
    weights: list[float] = []
    for n in range(1, n_max + 1):
        w = w_obstruction_removal(n)
        weights.append(w)
        s += w
    u = l1_unity(n_max)
    return {
        "g1_unique_decomposition": True,
        "n_paths_per_shell": 1,
        "sum_w": s,
        "sum_w_limit": 1.0,
        "w_1": weights[0],
        "w_2": weights[1],
        "kernel_is_a_sum": False,
        "born_requires_additional_structure": True,
        "born_derived_here": False,
        "sum_born_limit": u["sum_born_limit"],
        "is_qed": False,
        "foc012_refuses_born": True,
    }


def many_path_kernel(
    n_paths: int, action: float, beta: float = 0.0
) -> dict[str, Any]:
    """|Ω|>1: Z is a sum. G1 can still hold through a declared cut."""
    if n_paths < 1:
        raise ValueError("n_paths")
    z_many = path_kernel(n_paths, action, beta)
    z_unique = path_kernel(1, action, beta)
    return {
        "g1_unique_decomposition_per_path": True,
        "n_paths": n_paths,
        "kernel_is_a_sum": True,
        "z_many": z_many,
        "z_unique": z_unique,
        "ratio": z_many / z_unique if z_unique != 0.0 else None,
        "born_derived_here": False,
        "foc012_refuses_born": True,
    }


def diamond_composition(beta: float = 0.0) -> dict[str, Any]:
    """Two routes A→{B1,B2}→C. Cut B={B1,B2} restores G1.

    Each leg has action 1. Accepted E=1. Then Z(C|A)=2 and
    Z(C|B1)Z(B1|A)+Z(C|B2)Z(B2|A)=2 under G1–G3.
    """
    z_b1_a = path_kernel(1, 1.0, beta)
    z_c_b1 = path_kernel(1, 1.0, beta)
    z_b2_a = path_kernel(1, 1.0, beta)
    z_c_b2 = path_kernel(1, 1.0, beta)
    composed = compose_under_g1g2g3(z_c_b1, z_b1_a) + compose_under_g1g2g3(
        z_c_b2, z_b2_a
    )
    direct = path_kernel(2, 2.0, beta)
    return {
        "z_composed_cut": composed,
        "z_direct_two_paths": direct,
        "g1g2g3_holds_on_cut": abs(composed - direct) < 1e-12,
        "n_paths": 2,
    }


def g3_fail_local_green_global_red() -> dict[str, Any]:
    """Canonical FOC-012 counterexample: E1=E2=1, Eg=0, Δ_E=−1."""
    e1, e2, eg = 1, 1, 0
    d = delta_eval(e1, e2, eg)
    return {
        "E1": e1,
        "E2": e2,
        "Eg": eg,
        "delta_eval": d,
        "local_green_global_red": d == -1,
        "g3_holds": False,
        "false_green_if_eg_defined_as_product": delta_eval(1, 1, 1) == 0,
    }




def hex_shortest_path_count(q: int, r: int) -> int:
    """Shortest hex paths from the origin to (q,r).

    Cube coords (q, −q−r, r). Distance n is the max abs cube coord.
    Shortest paths interleave the two smaller axes: C(n, i).
    Axial cells (one cube coord zero) have count 1.
    """
    x, z = q, r
    y = -q - r
    ax, ay, az = abs(x), abs(y), abs(z)
    n = max(ax, ay, az)
    if n == 0:
        return 1
    others = sorted((ax, ay, az))
    return math.comb(n, others[0])


def hex_shell_paths(radius: int) -> dict[str, Any]:
    """Radius-n hex ring: 6 axial unique geodesics, rest many-path."""
    if radius < 0:
        raise ValueError("radius")
    if radius == 0:
        return {
            "radius": 0,
            "n_cells": 1,
            "n_axial": 1,
            "n_off_axis": 0,
            "unique_path_cells": 1,
            "total_geodesics": 1,
        }
    axial = 0
    off = 0
    total = 0
    cells = 0
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            if _hex_norm(q, r) != radius:
                continue
            cells += 1
            n = hex_shortest_path_count(q, r)
            total += n
            if n == 1:
                axial += 1
            else:
                off += 1
    return {
        "radius": radius,
        "n_cells": cells,
        "n_axial": axial,
        "n_off_axis": off,
        "unique_path_cells": axial,
        "total_geodesics": total,
        "kernel_is_a_sum": total > cells,
    }




def one_local_stays_chi1() -> dict[str, Any]:
    """PO-011 / PO-000 Lemma 5.3: one-local motion stays in the product tangent."""
    return {
        "chi": 1,
        "n_e": 0,
        "forces_chi_gt_1": False,
        "one_local": True,
        "product_state": True,
    }


def two_site_forces_chi(nu_e: float) -> dict[str, Any]:
    """A supplied nonzero normal rate rules out χ=1.

    The certificate gives only the lower bound χ≥2; it does not compute
    an exact bond dimension.
    """
    if nu_e < 0:
        raise ValueError("nu_e")
    forced = nu_e > 0
    return {
        "chi_lower_bound": 2 if forced else 1,
        "chi_exact": None if forced else 1,
        "n_e": nu_e,
        "forces_chi_gt_1": forced,
        "one_local": False,
        "product_state": not forced,
    }


def bond_growth_lower(nu_e: float, g: float, t: float) -> float:
    """PO-011 Theorem 3.1 / PO-000 Theorem 5.1: D_e(t) ≥ ν t − 24 g² t².

    Lieb–Robinson-free. Valid as a lower bound only for
    0 ≤ t ≤ ν/(48 g²) when ν>0 and g>0; outside that window the
    quadratic can go negative and is not used as a certificate.
    """
    return nu_e * t - 24.0 * g * g * t * t


def bond_growth_window(nu_e: float, g: float) -> float:
    if nu_e <= 0 or g <= 0:
        return 0.0
    return nu_e / (48.0 * g * g)


def declared_face_two_site_fixture() -> dict[str, Any]:
    """Apply the χ bound after explicitly admitting a face/two-site map.

    No Hamiltonian or normal projector is constructed from the triangle,
    so ``nu_e=1`` is fixture data.  Historical particle names are retained
    only as analogy labels.
    """
    hollow = one_local_stays_chi1()
    filled = two_site_forces_chi(1.0)
    return {
        "hollow_chi": hollow["chi"],
        "filled_chi_lower_bound": filled["chi_lower_bound"],
        "filled_chi_exact": filled["chi_exact"],
        "hollow_n_e": hollow["n_e"],
        "filled_n_e": filled["n_e"],
        "face_two_site_mapping_admitted": True,
        "face_two_site_mapping_derived": False,
        "physical_identifications_proved": False,
        "analogy_labels": {
            "face": "Higgs",
            "edges": ("W+", "W-", "Z"),
            "deficit_phase": "photon",
        },
        "po011_lemma_53": True,
    }




def local_green_global_red_hex(radius: int) -> dict[str, Any]:
    """Interior k=6, ε=0 is green. 'Is the wall α?' is red.

    Empty-interior (radius 0) is the FOC-012 trivial-slice collapse:
    the product of no locals is 1 by convention. Named, not used as α.
    """
    if radius < 0:
        raise ValueError("radius")
    wall = hex_vertices(radius)
    interior_green = 0
    interior_red = 0
    for q, r in wall:
        if _hex_norm(q, r) >= radius:
            continue
        k = triangles_at(q, r, wall)
        if k == 6:
            interior_green += 1
        else:
            interior_red += 1
    n_interior = interior_green + interior_red
    e_local_product = 1 if interior_red == 0 else 0
    e_g_alpha = 0
    d = delta_eval(e_local_product, 1, e_g_alpha)
    units = hex_wall_deficit_units(radius)
    return {
        "radius": radius,
        "n_interior": n_interior,
        "interior_k6_green": interior_green,
        "interior_not_k6": interior_red,
        "E_local_product": e_local_product,
        "E_g_is_alpha": e_g_alpha,
        "global_evaluator_declared": True,
        "qed_observable_constructed": False,
        "delta_eval": d,
        "local_green_global_red": d == -1 and e_local_product == 1,
        "trivial_interior": n_interior == 0,
        "deficit_units": units,
        "false_green_if_eg_is_local_product": False,
        "detector": "E_g asks whether the wall sum is alpha, not whether k=6",
        "is_qed": False,
    }


def join_report() -> dict[str, Any]:
    """One receipt: unique-path L1, many-path kernel, χ, hex Δ_E."""
    u = unique_path_l1(2000)
    many = many_path_kernel(2, 2.0, beta=0.0)
    dia = diamond_composition(0.0)
    g3 = g3_fail_local_green_global_red()
    face = declared_face_two_site_fixture()
    hex2 = local_green_global_red_hex(2)
    shell2 = hex_shell_paths(2)
    t = 0.01
    nu, g = 1.0, 1.0
    return {
        "unique_path_sum_w": u["sum_w"],
        "unique_path_limit": 1.0,
        "many_path_ratio": many["ratio"],
        "diamond_g1g2g3": dia["g1g2g3_holds_on_cut"],
        "delta_eval_counterexample": g3["delta_eval"],
        "hollow_chi": face["hollow_chi"],
        "filled_chi_lower_bound": face["filled_chi_lower_bound"],
        "face_two_site_mapping_derived": face["face_two_site_mapping_derived"],
        "hex_R2_local_green_global_red": hex2["local_green_global_red"],
        "hex_R2_interior_k6": hex2["interior_k6_green"],
        "hex_R2_geodesics": shell2["total_geodesics"],
        "hex_R2_axial_unique": shell2["n_axial"],
        "bond_growth_lower_at_t": bond_growth_lower(nu, g, t),
        "bond_growth_window": bond_growth_window(nu, g),
        "foc012_refuses_born": True,
        "po011_chi1_is_product": True,
        "is_qed": False,
        "born_requires_additional_structure": True,
        "born_derived_here": False,
    }
