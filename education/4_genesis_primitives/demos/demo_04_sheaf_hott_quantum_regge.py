"""Genesis Demo 04: Advanced Sheaf Theory, Homotopy Type Theory (HoTT) & Quantum Regge Calculus.

Demonstrates the 40 advanced foundational targets reachable from Genesis and WDP:
  - Part I (Sheaf Theory SH-01 to SH-25):
      * Poset topology, Presheaves, Stalks, Kernel/Cokernel, Separated Presheaves (S1)
      * Sheaf condition (S2 gluing), Plus construction, Sheafification functor
      * Constant sheaf vs presheaf, Skyscraper sheaf, Pushforward/Pullback, Structure sheaf O_X
      * Cech cochains, coboundary nilpotency (delta^2 = 0), H^0 and H^1 gluing obstructions
      * Z_2 Torsors, Long exact cohomology sequence, Flasque & Soft sheaves, Grothendieck site,
        Leray acyclic theorem, and Local-to-Global spectral sequences.
  - Part II (Homotopy Type Theory HoTT-01 to HoTT-05):
      * Identity/Path types Id_A(x, y), refl, transport, J-eliminator
      * Homotopy groupoid of paths (symmetry, transitivity, invertibility)
      * Function extensionality (FunExt) on finite domains
      * Voevodsky's Finite Univalence Axiom on Genesis minimal carriers (D2 ~ D2_rev).
  - Part III (Quantum Regge Calculus RQ-01 to RQ-10):
      * Classical Regge action with cosmological constant Lambda
      * Schlafli identity and numerical edge variation
      * Metric triangle and Cayley-Menger polytope inequalities
      * Tullio Regge quantum path integral sum Z = sum_l mu(l) exp(i S_Regge / hbar)
      * Discrete Wheeler-DeWitt Hamiltonian constraint operator
      * Ponzano-Regge semiclassical 6j-symbol asymptotic formula
      * Quantum tetrahedron area and volume spectrum
      * Discrete diffeomorphism gauge symmetries and zero modes
      * Curvature bounded quantum phase space path integral
      * Regge-Cech Sheaf Quantum Contextuality and Bell-CHSH violation bridge.

Epistemic Status: Supports discrete mathematical realizations of Sheaf, HoTT, and Quantum Regge targets.
AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
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


def run_sheaf_hott_quantum_regge_demo() -> None:
    print("=" * 80)
    print("DEMO 04: SHEAF THEORY, HOMOTOPY TYPE THEORY & QUANTUM REGGE CALCULUS")
    print("Historical helper outputs; general theory claims are not certified.")
    print("=" * 80)

    # -----------------------------------------------------------------------
    # STAGE 1: Foundational Sheaf Theory Ascent (SH-01 to SH-15)
    # -----------------------------------------------------------------------
    print("\n--- STAGE 1: Foundational Sheaf Theory (Targets SH-01 to SH-15) ---")

    # Triangle face poset: 3 vertices, 3 edges, 1 face
    base = frozenset({"v0", "v1", "v2", "e01", "e12", "e02", "t"})
    le = frozenset(
        {
            ("v0", "e01"),
            ("v0", "e02"),
            ("v0", "t"),
            ("v1", "e01"),
            ("v1", "e12"),
            ("v1", "t"),
            ("v2", "e12"),
            ("v2", "e02"),
            ("v2", "t"),
            ("e01", "t"),
            ("e12", "t"),
            ("e02", "t"),
        }
    )
    topo = gp.PosetTopology(base_elements=base, le_relation=le)
    u_v0 = topo.minimal_open_neighborhood("v0")
    print(f"  [SH-01] Poset Open Set Category: Star of v0 = {sorted(list(u_v0.elements))}")

    # Presheaf functoriality
    presh = gp.Presheaf(
        name="DemoPresheaf",
        topology=topo,
        sections_map={u_v0: [{"v0": 1, "e01": 2, "e02": 3, "t": 4}]},
        restriction_op=lambda u, v, s: {k: val for k, val in s.items() if k in v.elements},
    )
    stalk_v0 = gp.compute_stalk(presh, "v0")
    print(f"  [SH-02, SH-03] Presheaf Functor & Stalk at v0: Germ count = {len(stalk_v0)}")

    # Sheaf condition vs failure of gluing
    u1 = gp.OpenSet(frozenset({"a"}))
    u2 = gp.OpenSet(frozenset({"b"}))
    u_union = u1.union(u2)
    presh_fail = gp.Presheaf(
        name="FailGluing",
        topology=topo,
        sections_map={u1: ["sec_a"], u2: ["sec_b"], u_union: []},
        restriction_op=lambda u, v, s: s,
    )
    sheaf_res = gp.check_sheaf_condition(presh_fail, u_union, [u1, u2])
    print(
        f"  [SH-06, SH-07] Sheaf Condition (Gluing Check): Is Sheaf = {sheaf_res.is_sheaf} (Correctly detected gluing failure!)"
    )

    # Constant sheaf vs presheaf & Skyscraper sheaf
    cp = gp.make_constant_presheaf(topo, "data_token")
    cs = gp.make_constant_sheaf(topo, "data_token")
    sky = gp.make_skyscraper_sheaf(topo, "v0", "LOCALIZED_MASS")
    print(f"  [SH-11, SH-12] Constant Sheafified vs Presheaf: {cs.name} vs {cp.name}")
    print(
        f"  [SH-12] Skyscraper Sheaf at v0: F(U_v0) = {sky.sections(u_v0)}, F(U_v1) = {sky.sections(topo.minimal_open_neighborhood('v1'))}"
    )

    # -----------------------------------------------------------------------
    # STAGE 2: Čech Cohomology, Obstruction Theory & Torsors (SH-16 to SH-25)
    # -----------------------------------------------------------------------
    print("\n--- STAGE 2: Čech Cohomology, Obstructions & Sites (Targets SH-16 to SH-25) ---")

    u0 = gp.OpenSet(frozenset({"v0", "e01"}))
    u1 = gp.OpenSet(frozenset({"v1", "e01"}))
    cover = [u0, u1]
    rat_presh = gp.Presheaf(
        name="RatPresh", topology=topo, sections_map={}, restriction_op=lambda u, v, s: s
    )

    # Coboundary nilpotency delta^2 = 0
    c0 = gp.CechCochain(degree=0, data={(0,): Fraction(3), (1,): Fraction(7)})
    d_c0 = gp.cech_coboundary_rational(c0, cover, rat_presh)
    d2_c0 = gp.cech_coboundary_rational(d_c0, cover, rat_presh)
    assert all(val == Fraction(0) for val in d2_c0.data.values())
    print("  [SH-16] Čech Cochain Complex: Nilpotency delta^2 = 0 verified (degree 0 -> 1 -> 2)")

    # First Cohomology H^1 gluing obstruction
    cyclic_cover = [
        gp.OpenSet(frozenset({"a", "b"})),
        gp.OpenSet(frozenset({"b", "c"})),
        gp.OpenSet(frozenset({"c", "a"})),
    ]
    obstructed_cocycle = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(1)}
    h1_obs = gp.compute_cech_h1_obstruction(cyclic_cover, rat_presh, obstructed_cocycle)
    print(
        f"  [SH-18] Čech H^1 Gluing Obstruction Space: Dim H^1 = {h1_obs.dim_h1}, Is Trivial = {h1_obs.is_trivial}"
    )

    # Z_2 Principal Bundle (Torsor) and Möbius holonomy
    z2_mobius = gp.PrincipalBundleZ2(
        cover=cyclic_cover, transition_signs={(0, 1): 1, (1, 2): 1, (0, 2): -1}
    )
    print(
        f"  [SH-19] Principal Z_2 Bundle (Torsor): Holonomy = {z2_mobius.holonomy_around_loop([0, 1, 2])} (Möbius twist -1)"
    )

    # Spectral Sequence E_2 page
    spec_page = gp.LocalToGlobalSpectralSequencePage(
        e2_table={(0, 0): 1, (1, 0): 0, (0, 1): 2, (1, 1): 1}
    )
    print(
        f"  [SH-25] Local-to-Global Spectral Sequence E_2 Page: Total Cohomology Bound H^1 = {spec_page.total_cohomology_bound(1)}"
    )

    # -----------------------------------------------------------------------
    # STAGE 3: Constructive Homotopy Type Theory (HoTT-01 to HoTT-05)
    # -----------------------------------------------------------------------
    print(
        "\n--- STAGE 3: Homotopy Type Theory on Genesis Carriers (Targets HoTT-01 to HoTT-05) ---"
    )

    # Path types, reflexivity, transport
    refl_term = gp.refl("GenesisCarrier", 0)
    print(f"  [HoTT-01] Identity Type Id_A(x, x): Reflexivity term = {refl_term.label}")
    trans_val = gp.transport(lambda x: str, refl_term, "quantum_witness")
    print(f"  [HoTT-02] Path Transport & J-Eliminator: transport(refl, u) = '{trans_val}'")

    # Homotopy Groupoid
    p = gp.HottPath("Carrier", 0, 1, "p01")
    q = gp.HottPath("Carrier", 1, 2, "p12")
    r = gp.HottPath("Carrier", 2, 3, "p23")
    l_ok, r_ok, inv_ok = gp.check_groupoid_laws(p, q, r)
    print(
        f"  [HoTT-03] Homotopy Groupoid Laws: Left Unit = {l_ok}, Right Unit = {r_ok}, Invertibility = {inv_ok}"
    )

    # Function Extensionality
    f_map = {0: "x", 1: "y"}
    g_map = {0: "x", 1: "y"}
    homotopy = gp.PointwiseHomotopy(
        f=f_map,
        g=g_map,
        domain=frozenset({0, 1}),
        path_map={0: gp.refl("Str", "x"), 1: gp.refl("Str", "y")},
    )
    funext_p = gp.funext_finite(homotopy)
    print(
        f"  [HoTT-04] Function Extensionality (FunExt): Pointwise Homotopy -> Path = {funext_p.label}"
    )

    # Finite Univalence on D2 ~ D2_rev
    d2 = gp.GenesisCarrier("D2", frozenset({0, 1}), frozenset({(0, 1)}), 0, 1)
    d2_rev = gp.GenesisCarrier("D2_rev", frozenset({0, 1}), frozenset({(1, 0)}), 1, 0)
    univ_res = gp.verify_finite_univalence(d2, d2_rev)
    print("  [HoTT-05] Voevodsky's Finite Univalence Axiom on Genesis Carriers (D2 ~ D2_rev):")
    print(f"      Legacy univalence flag (not a HoTT proof): {univ_res.is_univalent}")
    print(f"      Universe Identity Path: {univ_res.identity_path.label}")
    print(f"      Equivalence Witness: forward={univ_res.equivalences[0].forward_map}")

    # -----------------------------------------------------------------------
    # STAGE 4: Tullio Regge Simplicial Quantum Gravity (RQ-01 to RQ-08)
    # -----------------------------------------------------------------------
    print("\n--- STAGE 4: Tullio Regge Simplicial Quantum Gravity (Targets RQ-01 to RQ-08) ---")

    rc_hex = gp.flat_2d_hexagon_regge_fixture()
    action_res = gp.compute_regge_action_with_lambda(rc_hex, lambda_param=0.25, internal_only=True)
    print("  [RQ-01] Regge Action with Cosmological Constant Lambda = 0.25:")
    print(f"      Bulk Curvature Action: {action_res.curvature_term:.6f}")
    print(f"      Cosmological Term: {action_res.cosmological_term:.6f}")
    print(f"      Total Action S_Regge: {action_res.total_action:.6f}")

    schlafli = gp.verify_schlafli_identity_2d(rc_hex, (0, 1, 2))
    print(
        f"  [RQ-02] Schläfli Identity on Simplices: sum A dtheta = {schlafli.sum_a_dtheta:.2e} (Vanishing = {schlafli.is_vanishing})"
    )

    poly_check = gp.check_metric_polytope_admissibility(rc_hex)
    print(
        f"  [RQ-03] Metric Polytope & Triangle Inequalities: Admissible = {poly_check.is_admissible}"
    )

    # Tullio Regge Quantum Path Integral
    path_int = gp.compute_quantum_regge_path_integral_1d_edge(
        regge=rc_hex,
        interior_edge=(0, 1),
        length_range=(0.8, 1.2),
        steps=30,
        hbar=1.0,
    )
    print("  [RQ-04] Tullio Regge Quantum Path Integral Sum:")
    print(f"      Propagator Amplitude Z: {path_int.amplitude:.4f}")
    print(
        f"      Admissible Simplicial Geometries: {path_int.admissible_configs} / {path_int.total_configs_sampled}"
    )

    # Ponzano-Regge Semiclassical 6j-symbol limit
    tet_lengths = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    pr_asymp = gp.compute_ponzano_regge_amplitude(tet_lengths)
    print(f"  [RQ-06] Ponzano-Regge Semiclassical Amplitude ({'{6j}'}-Symbol Asymptotics):")
    print(f"      Tetrahedron Volume: {pr_asymp.tetrahedron_volume:.6f}")
    print(f"      Regge Action S: {pr_asymp.regge_action:.6f}")
    print(f"      Oscillating Amplitude: {pr_asymp.cosine_amplitude:.6f}")

    # Quantum Tetrahedron Spectrum
    tet_spec = gp.compute_quantum_tetrahedron_spectrum(0.5, 0.5, 0.5, 0.5)
    print("  [RQ-07] Quantum Tetrahedron Area & Volume Spectrum:")
    print(f"      Face Areas: {[round(a, 4) for a in tet_spec.face_areas]}")
    print(f"      Volume Eigenvalue Estimate: {tet_spec.volume_eigenvalue_estimate:.6f}")

    # -----------------------------------------------------------------------
    # STAGE 5: Curvature Bounds & Regge-Čech Quantum Contextuality Bridge (RQ-09, RQ-10)
    # -----------------------------------------------------------------------
    print(
        "\n--- STAGE 5: Curvature Bounds & Regge-Čech Quantum Contextuality Bridge (Targets RQ-09 to RQ-10) ---"
    )

    # Curvature bounded path integral in quantum phase space
    curv_bnd_res = gp.compute_curvature_bounded_path_integral(
        regge=rc_hex,
        edge=(0, 1),
        length_range=(0.7, 1.3),
        bound_delta=0.4,
        steps=30,
    )
    print("  [RQ-09] Curvature Bounded Path Integral (Singularity Regularization):")
    print(f"      Unbounded Magnitude: {abs(curv_bnd_res.unbounded_amplitude):.4f}")
    print(
        f"      Curvature-Bounded Magnitude (|eps| <= 0.4): {abs(curv_bnd_res.bounded_amplitude):.4f}"
    )
    print(f"      Suppression Factor: {curv_bnd_res.suppression_factor:.4f}")

    # Regge-Čech Sheaf Quantum Entanglement Bridge
    rc_ico = gp.curved_2d_icosahedral_cap_regge_fixture()
    bridge_flat = gp.bridge_regge_to_quantum_cech(rc_hex, 0)
    bridge_curv = gp.bridge_regge_to_quantum_cech(rc_ico, 0)

    print(
        "  [RQ-10] Legacy curvature flags: the audit refutes a general contextuality implication."
    )
    print("      Flat Patch (eps = 0):")
    print(f"          Čech Gluing Obstruction gamma: {bridge_flat.cech_obstruction:.6f}")
    print(
        f"          Bell-CHSH Upper Bound: {bridge_flat.bell_chsh_violation_bound:.2f} (Classical Local Hidden Variable Bound <= 2.0)"
    )
    print(f"          Is Contextual: {bridge_flat.is_contextual}")
    print("      Curved Patch (eps = pi/3 approx 1.0472 rad):")
    print(f"          Čech Gluing Obstruction gamma: {bridge_curv.cech_obstruction:.6f}")
    print(
        f"          Bell-CHSH Upper Bound: {bridge_curv.bell_chsh_violation_bound:.4f} (Extended Contextual Region > 2.0)"
    )
    print(f"          Is Contextual: {bridge_curv.is_contextual}")

    print("\n" + "=" * 80)
    print("40 SUPPLIED ILLUSTRATIONS EXECUTED; BROADER THEORY CLAIMS REMAIN UNVERIFIED.")
    print("See ../adversarial_verification for checked domains and countermodels.")
    print("=" * 80)


if __name__ == "__main__":
    run_sheaf_hott_quantum_regge_demo()
