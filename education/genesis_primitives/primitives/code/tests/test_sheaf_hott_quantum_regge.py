"""Targeted Unit Verification Suite for Sheaf Theory (SH-01 to SH-25),
Homotopy Type Theory (HoTT-01 to HoTT-05), and Quantum Regge Calculus (RQ-01 to RQ-10).

AuthorityEffect: None.
Tests all 40 advanced foundational targets reachable from Genesis and WDP.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

# Dynamic module loading for digit-prefixed directory 2_genesis
PRIMITIVES_DIR = Path(__file__).resolve().parent.parent


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


# ==============================================================================
# Part 1: Tests for 25 Sheaf Theory Targets (SH-01 to SH-25)
# ==============================================================================


@pytest.fixture
def sample_poset_topology():
    """Face poset topology of a triangle (3 vertices v0, v1, v2; 3 edges e01, e12, e02; 1 face t)."""
    base = frozenset({"v0", "v1", "v2", "e01", "e12", "e02", "t"})
    # Poset relation: x <= y iff y is in the star of x
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
    return gp.PosetTopology(base_elements=base, le_relation=le)


def test_sh_01_poset_open_set_category(sample_poset_topology):
    """SH-01: Poset Open Set Category & Alexandrov Topology."""
    topo = sample_poset_topology
    # Star of v0: {v0, e01, e02, t}
    u_v0 = topo.minimal_open_neighborhood("v0")
    assert u_v0.elements == frozenset({"v0", "e01", "e02", "t"})
    assert topo.is_open(u_v0)

    # Subset that is not an up-set
    not_open = gp.OpenSet(frozenset({"v0"}))
    assert not topo.is_open(not_open)

    # Union and intersection of open sets are open
    u_v1 = topo.minimal_open_neighborhood("v1")
    u_union = u_v0.union(u_v1)
    u_inter = u_v0.intersection(u_v1)
    assert topo.is_open(u_union)
    assert topo.is_open(u_inter)
    assert u_inter.elements == frozenset({"e01", "t"})


def test_sh_02_presheaf_functoriality(sample_poset_topology):
    """SH-02: Presheaf Functor and composition law."""
    topo = sample_poset_topology
    u = topo.minimal_open_neighborhood("v0")
    v = gp.OpenSet(frozenset({"e01", "t"}))
    w = gp.OpenSet(frozenset({"t"}))

    def res_op(u_set, v_set, s):
        # Section is a dict mapping element to scalar
        return {k: val for k, val in s.items() if k in v_set.elements}

    sec_u = {k: 42 for k in u.elements}
    presh = gp.Presheaf(
        name="TestPresh",
        topology=topo,
        sections_map={u: [sec_u]},
        restriction_op=res_op,
    )

    assert presh.check_functoriality(u, v, w, sec_u)


def test_sh_03_stalk_at_simplex(sample_poset_topology):
    """SH-03: Stalk computation in finite poset topology."""
    topo = sample_poset_topology
    u_v0 = topo.minimal_open_neighborhood("v0")
    sec = {"v0": 1, "e01": 2, "e02": 3, "t": 4}
    presh = gp.Presheaf(
        name="StalkPresh",
        topology=topo,
        sections_map={u_v0: [sec]},
        restriction_op=lambda u, v, s: s,
    )

    stalk = gp.compute_stalk(presh, "v0")
    assert len(stalk) == 1
    assert stalk[0].point == "v0"
    assert stalk[0].section == sec


def test_sh_04_presheaf_morphisms(sample_poset_topology):
    """SH-04: Presheaf Morphisms commuting with restrictions."""
    topo = sample_poset_topology
    u = topo.minimal_open_neighborhood("v0")
    v = gp.OpenSet(frozenset({"e01", "t"}))

    presh_f = gp.Presheaf(
        name="F",
        topology=topo,
        sections_map={u: [10], v: [10]},
        restriction_op=lambda u_s, v_s, s: s,
    )
    presh_g = gp.Presheaf(
        name="G",
        topology=topo,
        sections_map={u: [20], v: [20]},
        restriction_op=lambda u_s, v_s, s: s,
    )

    morph = gp.PresheafMorphism(
        source=presh_f,
        target=presh_g,
        component_map=lambda u_s, s: s * 2,
    )

    assert morph.check_naturality(u, v, 10)


def test_sh_05_presheaf_kernel(sample_poset_topology):
    """SH-05: Presheaf Kernel construction."""
    topo = sample_poset_topology
    u = topo.minimal_open_neighborhood("v0")
    zero = (Fraction(0),)

    presh_f = gp.Presheaf(
        name="F",
        topology=topo,
        sections_map={u: [(Fraction(1),), (Fraction(0),)]},
        restriction_op=lambda u_s, v_s, s: s,
    )
    presh_g = gp.Presheaf(
        name="G",
        topology=topo,
        sections_map={u: [(Fraction(2),), (Fraction(0),)]},
        restriction_op=lambda u_s, v_s, s: s,
    )

    morph = gp.PresheafMorphism(
        source=presh_f,
        target=presh_g,
        component_map=lambda u_s, s: (s[0] * 2,),
    )

    ker = gp.presheaf_kernel(morph, zero)
    assert ker.sections(u) == [(Fraction(0),)]


def test_sh_06_separated_presheaf(sample_poset_topology):
    """SH-06: Separated Presheaf (Locality Axiom S1)."""
    topo = sample_poset_topology
    u = topo.minimal_open_neighborhood("v0")
    cover = [gp.OpenSet(frozenset({"v0", "e01"})), gp.OpenSet(frozenset({"v0", "e02"}))]

    # Distinct sections that restrict to same on cover violates S1
    presh = gp.Presheaf(
        name="TestSep",
        topology=topo,
        sections_map={u: ["s1", "s2"]},
        restriction_op=lambda u_s, v_s, s: "same",
    )
    is_sep, viol = gp.check_separated(presh, u, cover)
    assert not is_sep
    assert viol == ("s1", "s2")


def test_sh_07_sheaf_condition_gluing(sample_poset_topology):
    """SH-07: Sheaf Condition (S1 + S2 Gluing)."""
    topo = sample_poset_topology
    u1 = gp.OpenSet(frozenset({"a"}))
    u2 = gp.OpenSet(frozenset({"b"}))
    u = u1.union(u2)
    cover = [u1, u2]

    # Matching family ("val_a", "val_b") has no global section if F(U) is empty
    presh = gp.Presheaf(
        name="NoGluing",
        topology=topo,
        sections_map={u1: ["val_a"], u2: ["val_b"], u: []},
        restriction_op=lambda u_s, v_s, s: s,
    )
    res = gp.check_sheaf_condition(presh, u, cover)
    assert not res.is_sheaf
    assert res.is_separated


def test_sh_08_equalizer_diagram(sample_poset_topology):
    """SH-08: Equalizer Diagram computation."""
    topo = sample_poset_topology
    u1 = gp.OpenSet(frozenset({"v0", "e01"}))
    u2 = gp.OpenSet(frozenset({"v1", "e01"}))
    u = u1.union(u2)
    cover = [u1, u2]

    # Section is a dict mapping elements to value
    s1 = {"v0": 1, "e01": 2}
    s2 = {"v1": 3, "e01": 2}
    presh = gp.Presheaf(
        name="EqPresh",
        topology=topo,
        sections_map={u1: [s1], u2: [s2], u: []},
        restriction_op=lambda u_s, v_s, s: {k: s[k] for k in s if k in v_s.elements},
    )
    eq = gp.compute_equalizer_kernel(presh, u, cover)
    assert len(eq) == 1
    assert eq[0] == (s1, s2)


def test_sh_09_plus_construction(sample_poset_topology):
    """SH-09: Grothendieck Plus Construction F^+."""
    topo = sample_poset_topology
    cp = gp.make_constant_presheaf(topo, "val")
    f_plus = gp.plus_construction(cp)
    assert f_plus.name == "ConstantPresheaf^+"


def test_sh_10_sheafification_functor(sample_poset_topology):
    """SH-10: Sheafification Functor F^#."""
    topo = sample_poset_topology
    cp = gp.make_constant_presheaf(topo, "val")
    f_sharp = gp.sheafify(cp)
    assert f_sharp.name == "ConstantPresheaf^#"


def test_sh_11_constant_sheaf_vs_presheaf(sample_poset_topology):
    """SH-11: Constant Sheaf vs Constant Presheaf distinction."""
    topo = sample_poset_topology
    cp = gp.make_constant_presheaf(topo, "val")
    cs = gp.make_constant_sheaf(topo, "val")
    assert cp.name == "ConstantPresheaf"
    assert cs.name == "ConstantPresheaf^+"


def test_sh_12_skyscraper_sheaf(sample_poset_topology):
    """SH-12: Skyscraper Sheaf exact localization."""
    topo = sample_poset_topology
    sky = gp.make_skyscraper_sheaf(topo, "v0", "MASS_V0")
    u_v0 = topo.minimal_open_neighborhood("v0")
    u_v1 = topo.minimal_open_neighborhood("v1")

    assert sky.sections(u_v0) == ["MASS_V0"]
    assert sky.sections(u_v1) == ["0"]


def test_sh_13_direct_image_sheaf(sample_poset_topology):
    """SH-13: Direct Image Sheaf (Pushforward f_*)."""
    topo = sample_poset_topology
    sky = gp.make_skyscraper_sheaf(topo, "v0", "VAL")
    # Identity projection
    push = gp.pushforward_sheaf(lambda x: x, sky, topo)
    assert push.sections(topo.minimal_open_neighborhood("v0")) == ["VAL"]


def test_sh_14_inverse_image_sheaf(sample_poset_topology):
    """SH-14: Inverse Image Sheaf (Pullback f^*)."""
    topo = sample_poset_topology
    sky = gp.make_skyscraper_sheaf(topo, "v0", "VAL")
    pull = gp.pullback_presheaf(lambda x: x, topo, sky)
    assert pull.sections(topo.minimal_open_neighborhood("v0")) == ["VAL"]


def test_sh_15_structure_sheaf_rings(sample_poset_topology):
    """SH-15: Structure Sheaf O_X of rational piecewise affine rings."""
    topo = sample_poset_topology
    ox = gp.StructureSheaf(topo)
    u_v0 = topo.minimal_open_neighborhood("v0")
    secs = ox.sections(u_v0)
    # 4 elements in u_v0: zero vector + 4 basis vectors = 5 sections
    assert len(secs) == 5
    assert secs[0] == (Fraction(0), Fraction(0), Fraction(0), Fraction(0))


def test_sh_16_cech_cochain_coboundary(sample_poset_topology):
    """SH-16: Čech Cochain Complex and coboundary nilpotency delta^2 = 0."""
    topo = sample_poset_topology
    u0 = gp.OpenSet(frozenset({"v0", "e01"}))
    u1 = gp.OpenSet(frozenset({"v1", "e01"}))
    u2 = gp.OpenSet(frozenset({"v2", "e01"}))
    cover = [u0, u1, u2]

    presh = gp.Presheaf(
        name="RatPresh",
        topology=topo,
        sections_map={},
        restriction_op=lambda u, v, s: s,
    )

    c0 = gp.CechCochain(degree=0, data={(0,): Fraction(1), (1,): Fraction(2), (2,): Fraction(3)})
    d_c0 = gp.cech_coboundary_rational(c0, cover, presh)
    assert d_c0.degree == 1

    d2_c0 = gp.cech_coboundary_rational(d_c0, cover, presh)
    assert d2_c0.degree == 2
    # delta^2 == 0 identically!
    assert all(val == Fraction(0) for val in d2_c0.data.values())


def test_sh_17_cech_zeroth_cohomology(sample_poset_topology):
    """SH-17: Čech Zeroth Cohomology H^0(U, F)."""
    topo = sample_poset_topology
    u0 = gp.OpenSet(frozenset({"v0", "e01"}))
    u1 = gp.OpenSet(frozenset({"v1", "e01"}))
    cover = [u0, u1]

    presh = gp.Presheaf(name="P", topology=topo, sections_map={}, restriction_op=lambda u, v, s: s)
    h0 = gp.compute_cech_h0(cover, presh)
    assert len(h0) == 1
    assert h0[0].data[(0,)] == Fraction(1)


def test_sh_18_cech_first_cohomology_obstruction(sample_poset_topology):
    """SH-18: Čech First Cohomology H^1(U, F) as Gluing Obstruction Space."""
    topo = sample_poset_topology
    u0 = gp.OpenSet(frozenset({"a", "b"}))
    u1 = gp.OpenSet(frozenset({"b", "c"}))
    u2 = gp.OpenSet(frozenset({"c", "a"}))
    cover = [u0, u1, u2]
    presh = gp.Presheaf(name="P", topology=topo, sections_map={}, restriction_op=lambda u, v, s: s)

    # Trivial cocycle (sum around cycle is 0)
    triv_cocycle = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(2)}
    res_triv = gp.compute_cech_h1_obstruction(cover, presh, triv_cocycle)
    assert res_triv.is_trivial
    assert res_triv.dim_h1 == 0

    # Non-trivial cocycle (sum around cycle is non-zero => gluing obstruction!)
    obstructed = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(1)}
    res_obs = gp.compute_cech_h1_obstruction(cover, presh, obstructed)
    assert not res_obs.is_trivial
    assert res_obs.dim_h1 == 1


def test_sh_19_torsors_and_principal_sheaves():
    """SH-19: Z_2 Torsors and holonomy classification."""
    cover = [gp.OpenSet(frozenset({str(i)})) for i in range(3)]
    # Trivial bundle: all transitions +1
    b_triv = gp.PrincipalBundleZ2(cover=cover, transition_signs={(0, 1): 1, (1, 2): 1, (0, 2): 1})
    assert b_triv.is_trivial_bundle
    assert b_triv.holonomy_around_loop([0, 1, 2]) == 1

    # Non-trivial Möbius Z_2 bundle: one transition -1
    b_mobius = gp.PrincipalBundleZ2(
        cover=cover, transition_signs={(0, 1): 1, (1, 2): 1, (0, 2): -1}
    )
    assert not b_mobius.is_trivial_bundle
    assert b_mobius.holonomy_around_loop([0, 1, 2]) == -1


def test_sh_20_long_exact_cohomology_sequence():
    """SH-20: Long exact cohomology sequence connecting homomorphism delta*."""
    res = gp.connecting_homomorphism_delta_star(
        section_h=Fraction(5),
        lift_to_g=Fraction(5),
        overlap_difference=Fraction(0),
    )
    assert res.is_exact_at_boundary
    assert res.connecting_coboundary_h1 == Fraction(0)


def test_sh_21_flasque_sheaf(sample_poset_topology):
    """SH-21: Flasque Sheaf restriction surjectivity."""
    topo = sample_poset_topology
    u = topo.minimal_open_neighborhood("v0")
    v = gp.OpenSet(frozenset({"e01", "t"}))

    # Surjective presheaf
    flasque_presh = gp.Presheaf(
        name="Flasque",
        topology=topo,
        sections_map={u: ["s1", "s2"], v: ["s1"]},
        restriction_op=lambda u_s, v_s, s: "s1",
    )
    assert gp.is_flasque_sheaf(flasque_presh, [(u, v)])


def test_sh_22_soft_sheaf_partition_of_unity():
    """SH-22: Soft / Fine Sheaf and Partition of Unity."""
    u1 = gp.OpenSet(frozenset({"x", "y"}))
    u2 = gp.OpenSet(frozenset({"y", "z"}))
    pou = gp.PartitionOfUnity(
        cover=[u1, u2],
        weights={
            (0, "x"): Fraction(1),
            (1, "x"): Fraction(0),
            (0, "y"): Fraction(1, 2),
            (1, "y"): Fraction(1, 2),
            (0, "z"): Fraction(0),
            (1, "z"): Fraction(1),
        },
    )
    assert pou.verify_sum_to_one(frozenset({"x", "y", "z"}))


def test_sh_23_grothendieck_site(sample_poset_topology):
    """SH-23: Grothendieck Pretopology and covering sieves."""
    topo = sample_poset_topology
    site = gp.GrothendieckSite(topo)
    u_v0 = topo.minimal_open_neighborhood("v0")
    family = [gp.OpenSet(frozenset({"v0", "e01"})), gp.OpenSet(frozenset({"e02", "t"}))]
    assert site.is_covering_sieve(u_v0, family)


def test_sh_24_leray_acyclic_cover_theorem():
    """SH-24: Leray Acyclic Cover Condition."""
    u0 = gp.OpenSet(frozenset({"0", "1"}))
    u1 = gp.OpenSet(frozenset({"1", "2"}))
    # All open sets have H^1 = 0
    ok = gp.check_leray_acyclic_condition([u0, u1], lambda u: True)
    assert ok


def test_sh_25_local_to_global_spectral_sequence():
    """SH-25: Local-to-Global Spectral Sequence E_2 page."""
    e2 = gp.LocalToGlobalSpectralSequencePage(e2_table={(0, 0): 1, (1, 0): 0, (0, 1): 2, (1, 1): 1})
    # Total cohomology bound at degree 1: dim E_2^{1,0} + dim E_2^{0,1} = 0 + 2 = 2
    assert e2.total_cohomology_bound(1) == 2


# ==============================================================================
# Part 2: Tests for 5 Homotopy Type Theory Targets (HoTT-01 to HoTT-05)
# ==============================================================================


def test_hott_01_identity_path_type():
    """HoTT-01: Identity Type Id_A(x, y) and reflexivity."""
    p_refl = gp.refl("GenesisCarrier", 0)
    assert p_refl.is_reflexive
    assert p_refl.start == 0 and p_refl.end == 0

    id_type = gp.IdentityType(type_name="GenesisCarrier", x=0, y=0, witness=p_refl)
    assert id_type.is_inhabited


def test_hott_02_path_transport_and_induction():
    """HoTT-02: Path transport and J-eliminator."""
    p_refl = gp.refl("Carrier", 42)
    val = "evidence_datum"
    # transport^P(refl_x, u) == u
    trans_val = gp.transport(lambda x: str, p_refl, val)
    assert trans_val == val

    # J-eliminator
    j_res = gp.j_eliminator(p_refl, lambda x: f"proved({x})")
    assert j_res == "proved(42)"


def test_hott_03_homotopy_groupoid_laws():
    """HoTT-03: Homotopy Groupoid of paths (symmetry, transitivity, invertibility)."""
    p = gp.HottPath("Carrier", 0, 1, "p01")
    q = gp.HottPath("Carrier", 1, 2, "p12")
    r = gp.HottPath("Carrier", 2, 3, "p23")

    p_inv = gp.path_inverse(p)
    assert p_inv.start == 1 and p_inv.end == 0

    pq = gp.path_concat(p, q)
    assert pq.start == 0 and pq.end == 2

    left_u, right_u, inv_ok = gp.check_groupoid_laws(p, q, r)
    assert left_u
    assert right_u
    assert inv_ok


def test_hott_04_function_extensionality_finite():
    """HoTT-04: Function Extensionality (FunExt) on finite domains."""
    f = {0: "a", 1: "b"}
    g = {0: "a", 1: "b"}
    domain = frozenset({0, 1})
    path_map = {
        0: gp.refl("TargetType", "a"),
        1: gp.refl("TargetType", "b"),
    }
    homotopy = gp.PointwiseHomotopy(f=f, g=g, domain=domain, path_map=path_map)
    assert homotopy.is_valid_homotopy

    p_ext = gp.funext_finite(homotopy)
    assert p_ext.start == f
    assert p_ext.end == g


def test_hott_05_finite_univalence_genesis_carriers():
    """HoTT-05: Finite Univalence on Genesis Minimal Carriers (D2 ~ D2_rev)."""
    d2 = gp.GenesisCarrier(
        name="D2",
        elements=frozenset({0, 1}),
        relation=frozenset({(0, 1)}),
        src=0,
        tgt=1,
    )
    d2_rev = gp.GenesisCarrier(
        name="D2_rev",
        elements=frozenset({0, 1}),
        relation=frozenset({(1, 0)}),
        src=1,
        tgt=0,
    )

    res = gp.verify_finite_univalence(d2, d2_rev)
    assert res.is_univalent
    assert len(res.equivalences) == 1
    assert res.equivalences[0].is_relational_isomorphism
    assert res.identity_path.start == d2
    assert res.identity_path.end == d2_rev


# ==============================================================================
# Part 3: Tests for 10 Quantum Regge Calculus Targets (RQ-01 to RQ-10)
# ==============================================================================


def test_rq_01_classical_regge_action_with_lambda():
    """RQ-01: Regge action with cosmological constant."""
    # 2D flat hexagon fixture
    regge = gp.flat_2d_hexagon_regge_fixture()
    # Internal curvature only (bulk action)
    res_int = gp.compute_regge_action_with_lambda(regge, lambda_param=0.5, internal_only=True)
    # Hexagon curvature term: 0.0 at center vertex
    assert abs(res_int.curvature_term) < 1e-12
    # Area of 6 equilateral triangles with side 1: 6 * (sqrt(3)/4) ~ 2.598
    assert res_int.cosmological_term > 0.0
    assert abs(res_int.total_action - (-res_int.cosmological_term)) < 1e-12

    # Full curvature (bulk + boundary Gauss-Bonnet sum = 2*pi*chi)
    res_full = gp.compute_regge_action_with_lambda(regge, lambda_param=0.5, internal_only=False)
    assert abs(res_full.curvature_term - 2.0 * math.pi) < 1e-12


def test_rq_02_regge_field_equations_schlafli():
    """RQ-02: Schläfli identity and Regge gradient."""
    regge = gp.flat_2d_hexagon_regge_fixture()
    check = gp.verify_schlafli_identity_2d(regge, (0, 1, 2))
    assert check.is_vanishing

    # Gradient of flat action with respect to interior edge
    grad = gp.compute_regge_edge_gradient(regge, (0, 1))
    assert isinstance(grad, float)


def test_rq_03_metric_polytope_inequalities():
    """RQ-03: Simplicial metric triangle and Cayley-Menger inequalities."""
    regge = gp.flat_2d_hexagon_regge_fixture()
    check = gp.check_metric_polytope_admissibility(regge)
    assert check.is_admissible
    assert len(check.triangle_inequality_violations) == 0


def test_rq_04_quantum_regge_path_integral():
    """RQ-04: Tullio Regge quantum path integral sum over edge length."""
    regge = gp.flat_2d_hexagon_regge_fixture()
    res = gp.compute_quantum_regge_path_integral_1d_edge(
        regge=regge,
        interior_edge=(0, 1),
        length_range=(0.8, 1.2),
        steps=20,
        hbar=1.0,
    )
    assert res.admissible_configs > 0
    assert abs(res.amplitude) > 0.0


def test_rq_05_wheeler_dewitt_simplicial_constraint():
    """RQ-05: Discrete Wheeler-DeWitt Hamiltonian constraint operator."""
    regge = gp.curved_3d_5_tetrahedra_star_regge_fixture()
    res = gp.evaluate_simplicial_wheeler_dewitt(regge, vertex=0, psi_val=1.0, psi_hessian_trace=0.0)
    assert res.vertex == 0
    assert abs(res.potential_term) > 0.0


def test_rq_06_ponzano_regge_amplitude():
    """RQ-06: Ponzano-Regge semiclassical 6j-symbol correspondence."""
    # Regular tetrahedron of edge length 1.0
    lengths = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    res = gp.compute_ponzano_regge_amplitude(lengths)
    # Volume of regular tetrahedron with unit edges is 1/(6*sqrt(2)) ~ 0.11785
    assert abs(res.tetrahedron_volume - 1.0 / (6.0 * math.sqrt(2.0))) < 1e-6
    assert isinstance(res.cosine_amplitude, float)


def test_rq_07_quantum_tetrahedron_spectrum():
    """RQ-07: Quantum tetrahedron area and volume spectrum."""
    spec = gp.compute_quantum_tetrahedron_spectrum(j1=0.5, j2=0.5, j3=0.5, j4=0.5)
    assert len(spec.face_areas) == 4
    # All face areas equal for equal spins
    assert abs(spec.face_areas[0] - spec.face_areas[1]) < 1e-12
    assert spec.volume_eigenvalue_estimate > 0.0


def test_rq_08_zero_modes_diffeomorphism():
    """RQ-08: Discrete diffeomorphism zero modes in flat triangulations."""
    regge = gp.flat_2d_hexagon_regge_fixture()
    interior_edges = [(0, 1), (0, 2), (0, 3)]
    res = gp.analyze_flat_triangulation_zero_modes(regge, interior_edges)
    assert len(res.eigenvalues) == 3


def test_rq_09_curvature_bounded_path_integral():
    """RQ-09: Curvature bounded path integral in quantum phase space."""
    regge = gp.flat_2d_hexagon_regge_fixture()
    res = gp.compute_curvature_bounded_path_integral(
        regge=regge,
        edge=(0, 1),
        length_range=(0.8, 1.2),
        bound_delta=0.5,
        steps=20,
    )
    assert 0.0 <= res.suppression_factor <= 1.0


def test_rq_10_regge_cech_quantum_bridge():
    """RQ-10: Regge-Čech Sheaf Quantum Entanglement & Contextuality Bridge."""
    # Flat fixture: non-contextual, gamma = 0
    flat_regge = gp.flat_2d_hexagon_regge_fixture()
    bridge_flat = gp.bridge_regge_to_quantum_cech(flat_regge, 0)
    assert not bridge_flat.is_contextual
    assert bridge_flat.cech_obstruction == 0.0
    assert bridge_flat.bell_chsh_violation_bound == 2.0

    # Curved fixture: contextual, gamma > 0, Bell bound expanded
    curved_regge = gp.curved_2d_icosahedral_cap_regge_fixture()
    bridge_curv = gp.bridge_regge_to_quantum_cech(curved_regge, 0)
    assert bridge_curv.is_contextual
    assert bridge_curv.cech_obstruction > 0.0
    assert bridge_curv.bell_chsh_violation_bound > 2.0
