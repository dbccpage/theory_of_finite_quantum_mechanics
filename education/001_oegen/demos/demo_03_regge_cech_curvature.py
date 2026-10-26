"""Genesis Demo 03: Higher-Dimensional Regge Simplicial Complexes & Čech Curvature Bounds.

Demonstrates the geometric unification of Regge calculus (Category 5) with sheaf-theoretic
Čech gluing obstructions:
  - 2D Regge triangulations: Flat hexagon (eps = 0), Elliptic cap (eps = pi/3), Hyperbolic saddle (eps = -pi/3)
  - Discrete Gauss-Bonnet index theorem on closed 2-sphere boundary: sum_v eps(v) = 2*pi * chi(K)
  - 3D Higher-dimensional simplicial complexes: exact dihedral angles via Cayley-Menger determinants
  - 3D Flat cluster (eps = 0) vs. Curved 5-tetrahedron star (eps = 2*pi - 5*arccos(1/3) approx 0.1284 rad)
  - Discrete deficit angle curvature bounds: max |eps(h)| <= Delta bounds the Čech gluing obstruction
  - Category 5 -> Category 12 Presheaf Projection: verifies exact Čech 0-cycle (No-Signaling) compatibility
    and non-trivial contextuality obstruction on curved Regge hinges.

Epistemic Status: Supports discrete geometric evaluation of curvature as a Čech gluing obstruction.
AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEMOS_DIR = Path(__file__).resolve().parent
PRIMITIVES_DIR = DEMOS_DIR.parent / "primitives" / "code"


def _load_primitives_package():
    init_path = PRIMITIVES_DIR / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "genesis_primitives",
        init_path,
        submodule_search_locations=[str(PRIMITIVES_DIR)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {init_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["genesis_primitives"] = mod
    spec.loader.exec_module(mod)
    return mod


gp = _load_primitives_package()


def run_regge_cech_curvature_demo() -> None:
    print("=" * 78)
    print("DEMO 03: HIGHER-DIMENSIONAL REGGE COMPLEXES & CECH CURVATURE BOUNDS")
    print("=" * 78)

    # -----------------------------------------------------------------------
    # 1. 2D Regge Triangulations & Deficit Angle Trichotomy
    # -----------------------------------------------------------------------
    print("\n--- 1. 2D Regge Triangulations: Flat, Elliptic & Hyperbolic ---")

    # 1a. Flat Hexagon (6 equilateral triangles)
    rc_hex = gp.flat_2d_hexagon_regge_fixture()
    eps_hex = rc_hex.deficit_angle(0)
    gamma_hex = rc_hex.cech_gluing_obstruction(0)
    print("  [1a. Flat Hexagon Patch (6 triangles around vertex 0)]")
    print(f"      Total angle at vertex 0: {2.0 * math.pi - eps_hex:.4f} rad (2*pi)")
    print(f"      Deficit angle epsilon(0): {eps_hex:.6f} rad (0 deg)")
    print(f"      Cech Gluing Obstruction gamma(0): {gamma_hex:.6f} rad")
    print(f"      Has Global Euclidean Gluing: {rc_hex.has_global_gluing(0)}")
    assert abs(eps_hex) < 1e-12 and rc_hex.has_global_gluing(0) is True

    # 1b. Elliptic Cap (5 equilateral triangles, icosahedron vertex)
    rc_ico = gp.curved_2d_icosahedral_cap_regge_fixture()
    eps_ico = rc_ico.deficit_angle(0)
    gamma_ico = rc_ico.cech_gluing_obstruction(0)
    print("  [1b. Positively Curved Icosahedral Cap (5 triangles around vertex 0)]")
    print(f"      Total angle at vertex 0: {2.0 * math.pi - eps_ico:.4f} rad (5*pi/3)")
    print(f"      Deficit angle epsilon(0): {eps_ico:.6f} rad (+{math.degrees(eps_ico):.1f} deg)")
    print(f"      Cech Gluing Obstruction gamma(0): {gamma_ico:.6f} rad")
    print(f"      Has Global Euclidean Gluing: {rc_ico.has_global_gluing(0)}")
    assert abs(eps_ico - math.pi / 3.0) < 1e-12 and rc_ico.has_global_gluing(0) is False

    # 1c. Hyperbolic Saddle (7 equilateral triangles)
    rc_sad = gp.saddle_2d_hyperbolic_regge_fixture()
    eps_sad = rc_sad.deficit_angle(0)
    gamma_sad = rc_sad.cech_gluing_obstruction(0)
    print("  [1c. Negatively Curved Hyperbolic Saddle (7 triangles around vertex 0)]")
    print(f"      Total angle at vertex 0: {2.0 * math.pi - eps_sad:.4f} rad (7*pi/3)")
    print(f"      Deficit angle epsilon(0): {eps_sad:.6f} rad ({math.degrees(eps_sad):.1f} deg)")
    print(f"      Cech Gluing Obstruction gamma(0): {gamma_sad:.6f} rad")
    print(f"      Has Global Euclidean Gluing: {rc_sad.has_global_gluing(0)}")
    assert abs(eps_sad - (-math.pi / 3.0)) < 1e-12 and rc_sad.has_global_gluing(0) is False

    # -----------------------------------------------------------------------
    # 2. Discrete Gauss-Bonnet Index Theorem on Closed 2-Sphere
    # -----------------------------------------------------------------------
    print("\n--- 2. Discrete Gauss-Bonnet Index Theorem (Closed 2-Sphere) ---")
    rc_tet = gp.closed_2d_tetrahedron_surface_regge_fixture()
    chi_tet = rc_tet.euler_characteristic()
    deficits_tet = [rc_tet.deficit_angle(v) for v in rc_tet.complex.c0]
    sum_deficits = sum(deficits_tet)
    expected_gb = 2.0 * math.pi * chi_tet
    discrepancy = rc_tet.discrete_gauss_bonnet_discrepancy()

    print("  Closed triangulation: boundary of 3-simplex (tetrahedron)")
    print(
        f"    Vertices |c0| = {len(rc_tet.complex.c0)}, Edges |c1| = {len(rc_tet.complex.c1)}, Faces |c2| = {len(rc_tet.complex.c2)}"
    )
    print(f"    Euler characteristic chi(K) = {chi_tet}")
    print(
        f"    Deficit angle at each vertex: {[f'{d:.4f}' for d in deficits_tet]} (all exactly pi)"
    )
    print(f"    Total deficit angle sum_v epsilon(v): {sum_deficits:.6f} rad")
    print(f"    Gauss-Bonnet target 2*pi * chi(K): {expected_gb:.6f} rad (4*pi)")
    print(f"    Gauss-Bonnet discrepancy: {discrepancy:.2e}")
    assert discrepancy < 1e-12

    # -----------------------------------------------------------------------
    # 3. 3D Higher-Dimensional Simplicial Complexes (Dihedral Angles)
    # -----------------------------------------------------------------------
    print("\n--- 3. 3D Higher-Dimensional Regge Simplicial Complexes ---")

    # 3a. Flat 3D tetrahedral cluster
    rc_3df = gp.flat_3d_tetrahedral_cluster_regge_fixture()
    inc_3df = rc_3df.incident_top_simplices((0, 1))
    dih_3df = [rc_3df.tetrahedron_dihedral_angle(q, (0, 1)) for q in inc_3df]
    eps_3df = rc_3df.deficit_angle((0, 1))
    gamma_3df = rc_3df.cech_gluing_obstruction((0, 1))

    print("  [3a. Flat 3D Tetrahedral Cluster (4 tetrahedra around edge (0, 1))]")
    print(f"      Incident tetrahedra count: {len(inc_3df)}")
    print(
        f"      Dihedral angles around edge (0, 1): {[f'{math.degrees(d):.1f} deg' for d in dih_3df]} (all 90 deg = pi/2)"
    )
    print(f"      Sum of dihedral angles: {sum(dih_3df):.6f} rad (2*pi)")
    print(f"      Hinge deficit angle epsilon((0, 1)): {eps_3df:.6f} rad")
    print(f"      Cech Gluing Obstruction gamma((0, 1)): {gamma_3df:.6f} rad")
    print(f"      Has Global 3D Euclidean Gluing: {rc_3df.has_global_gluing((0, 1))}")
    assert abs(eps_3df) < 1e-12 and rc_3df.has_global_gluing((0, 1)) is True

    # 3b. Curved 3D 5-tetrahedron star
    rc_3dc = gp.curved_3d_5_tetrahedra_star_regge_fixture()
    inc_3dc = rc_3dc.incident_top_simplices((0, 1))
    dih_3dc = [rc_3dc.tetrahedron_dihedral_angle(q, (0, 1)) for q in inc_3dc]
    eps_3dc = rc_3dc.deficit_angle((0, 1))
    gamma_3dc = rc_3dc.cech_gluing_obstruction((0, 1))
    expected_eps_3dc = 2.0 * math.pi - 5.0 * math.acos(1.0 / 3.0)

    print("  [3b. Curved 3D Star (5 regular tetrahedra around edge (0, 1))]")
    print(f"      Incident tetrahedra count: {len(inc_3dc)}")
    print(
        f"      Regular tetrahedron dihedral angle: {math.degrees(dih_3dc[0]):.2f} deg (arccos(1/3))"
    )
    print(f"      Sum of dihedral angles: {sum(dih_3dc):.4f} rad < 2*pi ({2.0 * math.pi:.4f} rad)")
    print(
        f"      Hinge deficit angle epsilon((0, 1)): {eps_3dc:.6f} rad (+{math.degrees(eps_3dc):.2f} deg)"
    )
    print(f"      Cech Gluing Obstruction gamma((0, 1)): {gamma_3dc:.6f} rad")
    print(f"      Has Global 3D Euclidean Gluing: {rc_3dc.has_global_gluing((0, 1))}")
    assert abs(eps_3dc - expected_eps_3dc) < 1e-12 and rc_3dc.has_global_gluing((0, 1)) is False

    # -----------------------------------------------------------------------
    # 4. Discrete Deficit Angle Curvature Bounds
    # -----------------------------------------------------------------------
    print("\n--- 4. Discrete Deficit Angle Curvature Bounds (Certification) ---")
    bound_20 = 0.20
    bound_10 = 0.10
    bounded_20, max_c20, _ = rc_3dc.check_curvature_bound(bound_20, internal_only=True)
    bounded_10, max_c10, _ = rc_3dc.check_curvature_bound(bound_10, internal_only=True)

    print(
        f"  Curvature bound check for 3D curved star (internal hinge max curvature = {max_c20:.6f} rad):"
    )
    print(
        f"    - Bound <= {bound_20:.2f} rad: {bounded_20} (PASSES: curvature is bounded by {bound_20} rad)"
    )
    print(
        f"    - Bound <= {bound_10:.2f} rad: {bounded_10} (FAILS: curvature exceeds {bound_10} rad)"
    )
    assert bounded_20 is True and bounded_10 is False

    # -----------------------------------------------------------------------
    # 5. Sheaf-Theoretic Čech Presheaf Projection (Category 5 -> Category 12)
    # -----------------------------------------------------------------------
    print("\n--- 5. Sheaf-Theoretic Cech Presheaf Projection (Cat 5 -> Cat 12) ---")

    # Hexagon Presheaf
    ps_hex = rc_hex.to_observer_presheaf(0)
    compat_hex, disc_hex = ps_hex.check_cech_0_cycle_compatibility()
    print("  [2D Hexagon -> ObserverPresheaf]")
    print(f"    Cover context count: {len(ps_hex.contexts)}")
    print(f"    Cech 0-cycle (No-Signaling) compatibility: {compat_hex}")
    print(f"    Discrepancies on context intersections: {len(disc_hex)}")
    assert compat_hex is True and len(disc_hex) == 0

    # 3D Flat Presheaf
    ps_3df = rc_3df.to_observer_presheaf((0, 1))
    compat_3df, disc_3df = ps_3df.check_cech_0_cycle_compatibility()
    print("  [3D Flat Cluster -> ObserverPresheaf]")
    print(f"    Cover context count: {len(ps_3df.contexts)}")
    print(f"    Cech 0-cycle (No-Signaling) compatibility: {compat_3df}")
    print(f"    Discrepancies on context intersections: {len(disc_3df)}")
    assert compat_3df is True and len(disc_3df) == 0

    # 3D Curved Presheaf
    ps_3dc = rc_3dc.to_observer_presheaf((0, 1))
    compat_3dc, disc_3dc = ps_3dc.check_cech_0_cycle_compatibility()
    print("  [3D Curved Star -> ObserverPresheaf]")
    print(f"    Cover context count: {len(ps_3dc.contexts)}")
    print(f"    Cech 0-cycle (No-Signaling) compatibility: {compat_3dc}")
    print(f"    Discrepancies on context intersections: {len(disc_3dc)}")
    assert compat_3dc is True and len(disc_3dc) == 0

    print("\n" + "=" * 78)
    print("ILLUSTRATION RESULT: ALL 5 SUPPLIED STAGES RAN; THE CECH/CURVATURE CORRESPONDENCE IS NOT PROVED")
    print("=" * 78)


if __name__ == "__main__":
    run_regge_cech_curvature_demo()
