"""Targeted Unit Verification Suite for Genesis Primitives and Composed Types.

Checks selected computational behavior and declared algebraic invariants.
General source fidelity and primitive completeness require separate evidence.

Uses dynamic module loading to load from the '2_genesis/primitives' directory
without violating Python identifier syntax on digit-prefixed paths.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
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


# ===========================================================================
# 1. Tests for Category 1: Seed & Regime
# ===========================================================================


def test_seed_and_regime_step_determinism():
    """Verify that Supply is a no-op, AdmitDatum internalizes tokens, and forms/instances type-check."""
    r0 = gp.EMPTY
    assert r0.n_data() == 0
    assert r0.n_forms() == 0

    # Supply does not mutate state
    r1 = gp.step(r0, gp.Supply("<>"))
    assert r1 == r0

    # AdmitDatum adds token
    r2 = gp.step(r1, gp.AdmitDatum("<>"))
    assert r2.n_data() == 1
    assert r2.data == ("<>",)

    # Dedup on re-admission
    r2_dedup = gp.step(r2, gp.AdmitDatum("<>"))
    assert r2_dedup == r2

    # Admit second datum
    r3 = gp.step(r2, gp.AdmitDatum("<a>"))
    assert r3.n_data() == 2

    # Admit binary form
    r4 = gp.step(r3, gp.AdmitForm(2))
    assert r4.n_forms() == 1
    assert r4.forms == (2,)

    # Admit instance (form 0, args (0, 1))
    r5 = gp.step(r4, gp.AdmitInst(0, (0, 1)))
    assert len(r5.insts) == 1
    assert (0, (0, 1)) in r5.insts

    # Impose separation requirement on (0, 1)
    r6 = gp.step(r5, gp.Impose(0, 1))
    assert (0, 1) in r6.reqs

    # Replay equals sequential step
    history = [
        gp.Supply("<>"),
        gp.AdmitDatum("<>"),
        gp.AdmitDatum("<a>"),
        gp.AdmitForm(2),
        gp.AdmitInst(0, (0, 1)),
        gp.Impose(0, 1),
    ]
    assert gp.replay(history) == r6


def test_seed_and_regime_errors():
    """Verify proper AdmissionError raises on invalid admissions."""
    with pytest.raises(gp.AdmissionError):
        gp.step(gp.EMPTY, gp.AdmitForm(0))

    with pytest.raises(gp.AdmissionError):
        gp.step(gp.EMPTY, gp.AdmitInst(0, (0,)))

    with pytest.raises(gp.AdmissionError):
        gp.step(gp.EMPTY, gp.Impose(1, 0))


def test_delta_and_cost_measures():
    """Verify canonical item sorting and cost measures mu1, mu2."""
    d = (gp.NewInst(0, (0, 1)), gp.NewForm(2), gp.NewDatum())
    canon = gp.canonical_delta(d)
    assert isinstance(canon[0], gp.NewDatum)
    assert isinstance(canon[1], gp.NewForm)
    assert isinstance(canon[2], gp.NewInst)
    assert gp.mu1(canon) == 3
    assert gp.mu2(canon) == (3, 2)


# ===========================================================================
# 2. Tests for Category 2: Primitive Difference
# ===========================================================================


def test_primitive_difference_relations():
    """Verify irreflexivity, symmetry, transpose, and cotransitivity."""
    rel_irrefl = frozenset({(0, 1), (1, 2)})
    rel_refl = frozenset({(0, 0), (0, 1)})
    assert gp.irreflexive(rel_irrefl) is True
    assert gp.irreflexive(rel_refl) is False

    assert gp.symmetric(frozenset({(0, 1), (1, 0)})) is True
    assert gp.symmetric(frozenset({(0, 1)})) is False

    assert gp.transpose(frozenset({(0, 1)})) == frozenset({(1, 0)})
    assert gp.cotransitive(frozenset({(0, 1)}), 2) is True


def test_primitive_difference_candidates():
    """Verify 9-candidate readings on concrete settings."""
    s_a = gp.Setting(
        n=2,
        r=frozenset({(0, 1)}),
        a=0,
        b=1,
        ret=frozenset(),
        prot=frozenset(),
        ops=frozenset(),
    )
    assert gp.W(s_a) is True
    assert gp.A(s_a) is True
    assert gp.D(s_a) is True  # a != b
    assert gp.Bs(s_a) is False  # not symmetric
    assert gp.C(s_a) is False  # not in prot
    assert gp.F(s_a) is False  # not in ret/prot

    s_w = gp.Setting(
        n=1,
        r=frozenset({(0, 0)}),
        a=0,
        b=0,
        ret=frozenset(),
        prot=frozenset(),
        ops=frozenset(),
    )
    assert gp.W(s_w) is True
    assert gp.A(s_w) is False  # fails irreflexivity
    assert gp.D(s_w) is False  # a == b (fails separation)

    # Minimal carriers
    assert gp.D2.n == 2 and gp.D2.rel == frozenset({(0, 1)})
    assert gp.S2.n == 2 and gp.S2.rel == frozenset({(0, 1), (1, 0)})


def test_category_ptd_rel():
    """Verify pointed relations and morphisms in PtdRel."""
    p_src = gp.PtdRel(2, frozenset({(0, 1)}), 0, 1)
    p_tgt = gp.PtdRel(3, frozenset({(1, 2)}), 1, 2)
    # Morphism mapping 0 -> 1, 1 -> 2
    h = gp.Hom(p_src, p_tgt, (1, 2))
    assert h.is_valid() is True


# ===========================================================================
# 3. Tests for Category 3: Primitive Passage
# ===========================================================================


def test_passage_active_obstruction_four_gates():
    """Verify 4-gate decomposition of active obstruction."""
    s0 = gp.GENESIS_P
    assert gp.declared_p(s0) is False

    # Admit 2 occurrences
    s1 = gp.pstep(s0, ("admitOcc", 0))
    s2 = gp.pstep(s1, ("admitOcc", 1))

    # Assert witness (0, 1)
    s3 = gp.pstep(s2, ("assertWit", 0, 1))

    # Retain witness (0, 1) -> Gate 1 passes
    s4 = gp.pstep(s3, ("admitWit", 0, 1))
    assert gp.retained_p(s4, 0, 1) is True
    assert gp.protected_p(s4, 0, 1) is False
    assert gp.obst_p(s4, 0, 1) is False  # protected gate false

    # Protect (0, 1) -> Gate 2 passes
    s5 = gp.pstep(s4, ("protect", 0, 1))
    assert gp.protected_p(s5, 0, 1) is True
    assert gp.declared_p(s5) is False
    assert gp.obst_p(s5, 0, 1) is False  # declared gate false

    # Declare observation (empty columns initially) -> Gate 3 passes
    s6 = gp.pstep(s5, ("declareObs",))
    assert gp.declared_p(s6) is True
    assert gp.zero_p_gate(s6, 0, 1) is True  # empty observer cannot separate
    # All 4 gates now pass -> Active Obstruction holds!
    assert gp.obst_p(s6, 0, 1) is True

    # Now add separating column with license and budget
    s7 = gp.pstep(s6, ("setBudget", 5))
    s8 = gp.pstep(s7, ("addCol", (0,)))
    assert gp.declared_p(s8) is True
    assert gp.zero_p_gate(s8, 0, 1) is False  # column (0,) separates 0 and 1
    # Obstruction resolves!
    assert gp.obst_p(s8, 0, 1) is False


def test_diff_obs_equivalence():
    """Verify DiffObs certifies reflexivity, symmetry, and transitivity."""
    obs = gp.DiffObs(2, frozenset({(0, 0), (1, 1)}))
    assert obs.is_reflexive() is True
    assert obs.is_symmetric() is True
    assert obs.is_transitive() is True


# ===========================================================================
# 4. Tests for Category 4: Refusal & Boundary
# ===========================================================================


def test_refusal_disciplines():
    """Verify refusal re-admission disciplines."""
    s0 = gp.EMPTY_RST
    s1 = gp.readmit_fact(s0, "token_a")
    assert s1.refusals == 1

    s2 = gp.readmit_reify_tagged(s0, "token_b")
    assert len(s2.data) == 1
    assert 0 in s2.tags


def test_world_and_constitution_desc():
    """Verify World representation and Desc index roundtrip."""
    w = gp.GENESIS_WORLD
    assert gp.quiescent(w) is True

    # Desc 64-toggle roundtrip
    for idx in range(64):
        d = gp.Desc.from_index(idx)
        assert d.to_index() == idx
    assert gp.KERNEL_DESC.to_index() == 63


# ===========================================================================
# 5. Tests for Category 5: Simplicial Complex
# ===========================================================================


def test_simplicial_complex_and_boundary_cancellation():
    """Verify simplicial complex creation and d^2 = 0 boundary cancellation."""
    cx = gp.EMPTY_COMPLEX
    cx = gp.cstep(cx, ("addV", 0))
    cx = gp.cstep(cx, ("addV", 1))
    assert gp.shell1(cx, 0, 1) is True
    cx = gp.cstep(cx, ("addE", 0, 1))
    assert cx.c1 == ((0, 1),)

    # Test boundary of 2-simplex [0, 1, 2]
    tri = (0, 1, 2)
    b = gp.boundary(tri)
    assert b == [(1, (1, 2)), (-1, (0, 2)), (1, (0, 1))]

    # d^2 vanishes on triangle
    assert gp.d2_vanishes(tri) is True

    # d^2 vanishes on tetrahedron [0, 1, 2, 3]
    tet = (0, 1, 2, 3)
    assert gp.d2_vanishes(tet) is True


def test_regge_calculus_curvature_bounds_and_cech_gluing_obstruction():
    """Verify Regge calculus simplicial complex curvature bounds and Čech gluing obstructions.

    Tests:
    1. 2D Regge Triangulations & Deficit Angles:
       - Flat hexagon: eps(0) == 0.0, Cech obstruction gamma(0) == 0.0, global gluing holds.
       - Curved icosahedral cap: eps(0) == pi/3, Cech obstruction gamma(0) == pi/3, global gluing obstructed.
       - Hyperbolic saddle: eps(0) == -pi/3, Cech obstruction gamma(0) == pi/3, global gluing obstructed.
    2. Discrete Gauss-Bonnet Index Invariant:
       - Closed 2-sphere boundary of tetrahedron (chi = 2): sum_v eps(v) = 4*pi = 2*pi*chi(K).
    3. 3D Higher-Dimensional Simplicial Complexes:
       - 4-tetrahedron flat cluster around edge (0, 1): dihedral angles == pi/2, eps == 0.0, gamma == 0.0.
       - 5-tetrahedron curved star around edge (0, 1): dihedral angles == arccos(1/3), eps == 2*pi - 5*arccos(1/3) approx 0.1284 rad, gamma > 0.
    4. Discrete Deficit Angle Curvature Bounds:
       - Local curvature bound max |eps(h)| <= Delta strictly bounds the maximum Čech gluing obstruction.
       - Boundary certification against positive/negative tolerances.
    5. Sheaf-Theoretic Čech Presheaf Projection:
       - Projects 2D and 3D Regge hinge stars to Category 12 ObserverPresheaf.
       - Verifies exact Čech 0-cycle compatibility (No-Signaling) across all shared facet intersections.
       - Asserts that Čech gluing obstruction vanishes iff the Regge deficit angle vanishes.
    """
    import math

    # 1. 2D Regge Triangulations
    # 1a. Flat Hexagon (6 equilateral triangles around vertex 0)
    rc_hex = gp.flat_2d_hexagon_regge_fixture()
    assert rc_hex.is_internal_hinge(0) is True
    eps_hex = rc_hex.deficit_angle(0)
    assert eps_hex == pytest.approx(0.0, abs=1e-12)
    gamma_hex = rc_hex.cech_gluing_obstruction(0)
    assert gamma_hex == pytest.approx(0.0, abs=1e-12)
    assert rc_hex.has_global_gluing(0) is True

    # 1b. Positively Curved Icosahedral Cap (5 equilateral triangles around vertex 0)
    rc_ico = gp.curved_2d_icosahedral_cap_regge_fixture()
    assert rc_ico.is_internal_hinge(0) is True
    eps_ico = rc_ico.deficit_angle(0)
    assert eps_ico == pytest.approx(math.pi / 3.0, abs=1e-12)
    gamma_ico = rc_ico.cech_gluing_obstruction(0)
    assert gamma_ico == pytest.approx(math.pi / 3.0, abs=1e-12)
    assert rc_ico.has_global_gluing(0) is False  # Obstructed by positive curvature

    # 1c. Negatively Curved Hyperbolic Saddle (7 equilateral triangles around vertex 0)
    rc_sad = gp.saddle_2d_hyperbolic_regge_fixture()
    assert rc_sad.is_internal_hinge(0) is True
    eps_sad = rc_sad.deficit_angle(0)
    assert eps_sad == pytest.approx(-math.pi / 3.0, abs=1e-12)
    gamma_sad = rc_sad.cech_gluing_obstruction(0)
    assert gamma_sad == pytest.approx(math.pi / 3.0, abs=1e-12)
    assert rc_sad.has_global_gluing(0) is False  # Obstructed by negative curvature

    # 2. Discrete Gauss-Bonnet Theorem on Closed 2-Sphere
    rc_tet = gp.closed_2d_tetrahedron_surface_regge_fixture()
    assert rc_tet.euler_characteristic() == 2
    # Each of the 4 vertices has deficit angle pi
    for v in rc_tet.complex.c0:
        assert rc_tet.deficit_angle(v) == pytest.approx(math.pi, abs=1e-12)
    # Total deficit angle is 4*pi == 2*pi*chi
    gb_discrepancy = rc_tet.discrete_gauss_bonnet_discrepancy()
    assert gb_discrepancy == pytest.approx(0.0, abs=1e-12)

    # 3. 3D Higher-Dimensional Simplicial Complexes & Dihedral Angles
    # 3a. Flat 3D tetrahedral cluster (4 tetrahedra meeting along edge (0, 1))
    rc_3df = gp.flat_3d_tetrahedral_cluster_regge_fixture()
    assert rc_3df.is_internal_hinge((0, 1)) is True
    # Dihedral angle of each tetrahedron at hinge edge (0, 1) is pi/2
    for q in rc_3df.incident_top_simplices((0, 1)):
        dih = rc_3df.tetrahedron_dihedral_angle(q, (0, 1))
        assert dih == pytest.approx(math.pi / 2.0, abs=1e-12)
    eps_3df = rc_3df.deficit_angle((0, 1))
    assert eps_3df == pytest.approx(0.0, abs=1e-12)
    gamma_3df = rc_3df.cech_gluing_obstruction((0, 1))
    assert gamma_3df == pytest.approx(0.0, abs=1e-12)
    assert rc_3df.has_global_gluing((0, 1)) is True

    # 3b. Curved 3D 5-tetrahedron star (5 regular tetrahedra meeting along edge (0, 1))
    rc_3dc = gp.curved_3d_5_tetrahedra_star_regge_fixture()
    assert rc_3dc.is_internal_hinge((0, 1)) is True
    # Dihedral angle of each regular tetrahedron is arccos(1/3)
    dih_reg = math.acos(1.0 / 3.0)
    for q in rc_3dc.incident_top_simplices((0, 1)):
        dih = rc_3dc.tetrahedron_dihedral_angle(q, (0, 1))
        assert dih == pytest.approx(dih_reg, abs=1e-12)
    expected_eps_3d = 2.0 * math.pi - 5.0 * dih_reg  # approx 0.128388 rad
    eps_3dc = rc_3dc.deficit_angle((0, 1))
    assert eps_3dc == pytest.approx(expected_eps_3d, abs=1e-12)
    gamma_3dc = rc_3dc.cech_gluing_obstruction((0, 1))
    assert gamma_3dc == pytest.approx(expected_eps_3d, abs=1e-12)
    assert rc_3dc.has_global_gluing((0, 1)) is False

    # 4. Discrete Deficit Angle Curvature Bounds
    # rc_3dc satisfies bound 0.2 rad on internal hinges, but violates bound 0.1 rad
    bounded_20, max_curv_20, _ = rc_3dc.check_curvature_bound(0.2, internal_only=True)
    assert bounded_20 is True
    assert max_curv_20 == pytest.approx(expected_eps_3d, abs=1e-12)
    bounded_10, _, _ = rc_3dc.check_curvature_bound(0.1, internal_only=True)
    assert bounded_10 is False

    # Closed tetrahedron surface satisfies bound pi on all vertices
    bounded_tet, max_curv_tet, _ = rc_tet.check_curvature_bound(math.pi + 1e-6)
    assert bounded_tet is True
    assert max_curv_tet == pytest.approx(math.pi, abs=1e-12)

    # 5. Sheaf-Theoretic Čech Presheaf Projection (Category 5 -> Category 12)
    # 5a. 2D Hexagon Presheaf
    ps_hex = rc_hex.to_observer_presheaf(0)
    assert len(ps_hex.contexts) == 6
    compat_hex, disc_hex = ps_hex.check_cech_0_cycle_compatibility()
    assert compat_hex is True, (
        f"Hexagon presheaf must satisfy Čech 0-cycle (No-Signaling): {disc_hex}"
    )
    assert len(disc_hex) == 0

    # 5b. 3D Flat Presheaf
    ps_3df = rc_3df.to_observer_presheaf((0, 1))
    assert len(ps_3df.contexts) == 4
    compat_3df, disc_3df = ps_3df.check_cech_0_cycle_compatibility()
    assert compat_3df is True, (
        f"3D flat presheaf must satisfy Čech 0-cycle (No-Signaling): {disc_3df}"
    )
    assert len(disc_3df) == 0

    # 5c. 3D Curved Presheaf
    ps_3dc = rc_3dc.to_observer_presheaf((0, 1))
    assert len(ps_3dc.contexts) == 5
    compat_3dc, disc_3dc = ps_3dc.check_cech_0_cycle_compatibility()
    assert compat_3dc is True, (
        f"3D curved presheaf must satisfy Čech 0-cycle (No-Signaling): {disc_3dc}"
    )
    assert len(disc_3dc) == 0


# ===========================================================================
# 6. Tests for Category 6: Transition & Trace
# ===========================================================================


def test_transition_profile_and_trecord():
    """Verify transition alphabet, profile construction, and TRecord."""
    assert len(gp.DDC_ALPHABET) == 8
    s0 = gp.GENESIS_P
    ev = ("admitOcc", 0)
    assert gp.guard_holds(s0, ev) is True
    assert gp.accepted(s0, ev) is True

    prof = gp.profile_of(s0, ev)
    assert prof[6] is True  # accepted

    rec = gp.make_record(s0, ev)
    assert isinstance(rec, gp.TRecord)
    assert rec.is_well_formed() is True


# ===========================================================================
# 7. Tests for Category 7: Derivation Engine
# ===========================================================================


def test_derivation_engine_primitives():
    """Verify Reading L & F, Tree, Node, Edge, and ProposalRecord."""
    assert len(gp.READINGS) == 2
    assert gp.READING_L.name == "L" and gp.READING_L.target == (0, 1)
    assert gp.READING_F.name == "F" and gp.READING_F.target == (1, 2)

    prop = gp.ProposalRecord(
        block="Block0",
        embed=(0, 1),
        retract=(0, 0),
        new_pair=(0, 1),
        parent_pos=0,
        fresh_pos=1,
        cost=2,
    )
    assert prop.cost == 2

    tree = gp.Tree(
        reading="L",
        measure="mu1",
        bounds=gp.Bounds(),
        max_rounds=5,
        pre_expansion_node_guard=10,
        supply=True,
    )
    stats = tree.stats()
    assert stats["reading"] == "L"
    assert stats["nodes"] == 0


# ===========================================================================
# 8. Tests for Category 8: Apartness & Indistinguishability
# ===========================================================================


def test_apartness_and_indistinguishability():
    """Verify positive constructive apartness, equivalence theorem, and countermodels."""
    n = 3
    apart_rel = frozenset((i, j) for i in range(n) for j in range(n) if i != j)
    assert gp.is_apart(n, apart_rel) is True
    assert gp.indist_is_equivalence(n, apart_rel) is True

    empty_rel = frozenset()
    assert gp.is_apart(2, empty_rel) is True
    assert gp.indist_is_equivalence(2, empty_rel) is True

    assert gp.equivalence_theorem_exhaustive(max_n=2) is True

    cm = gp.insufficiency_countermodels()
    assert cm["bare_breaks_refl"] is True
    assert cm["irrefl_alone_breaks_symm"] is True
    assert cm["symm_without_cotrans_breaks_trans"] is True


# ===========================================================================
# 9. Tests for Category 9: Primitive Contact
# ===========================================================================


def test_primitive_contact_and_witnessed_diff():
    """Verify WitnessedDiff kernel and pre-topological ContactKernel."""
    k = gp.bool_kernel()
    assert k.is_diag_zero(False) is True
    assert k.is_diag_zero(True) is True
    assert k.is_witness_nonzero() is True
    assert k.kernel_apart(False, True) is True
    assert k.kernel_apart(True, False) is False

    ck = gp.ContactKernel(
        size=3,
        contacts=frozenset({(frozenset({0}), frozenset({1}))}),
    )
    assert ck.touches({0, 1}, {1, 2}) is True
    assert ck.touches({0}, {1}) is True
    assert ck.touches({1}, {0}) is True
    assert ck.touches({0}, {2}) is False
    assert ck.separated({0}, {2}) is True


# ===========================================================================
# 10. Tests for Category 10: Attachment Ladder
# ===========================================================================


def test_attachment_ladder_and_lawful_policies():
    """Verify lawful policy certification, UpFamily blocks, and checked attachment."""

    def lawful_pi(k: int) -> int:
        return 0

    assert gp.lawful_to(lawful_pi, 5) is True

    def unlawful_pi(k: int) -> int:
        return k + 1

    assert gp.lawful_to(unlawful_pi, 3) is False

    s0 = gp.pstep(gp.GENESIS_P, ("admitOcc", 100))
    block = gp.up_block(s0, 0)
    assert len(block) == 4
    assert block[0] == ("admitOcc", 101)

    fam = gp.up_family(s0)
    assert len(fam) == 1

    res_ok = gp.attach_checked(s0, 0)
    assert res_ok["outcome"] == "attached"
    assert res_ok["occ_len"] == 2

    res_refused = gp.attach_checked(s0, 99)
    assert res_refused["outcome"] == "refusedParent"

    assert gp.shell_guard(2, (0, 1, 2)) is True
    assert gp.shell_guard(2, (0, 2, 1)) is False
    assert gp.shell_guard(2, (0, 1)) is False


# ===========================================================================
# 11. Tests for Category 11: Renaming Structure
# ===========================================================================


def test_renaming_structures_and_automorphisms():
    """Verify permutation actions, relational isomorphism, and gauge invariants."""
    perms = gp.all_permutations(3)
    assert len(perms) == 6

    r_cycle1 = frozenset({(0, 1), (1, 2), (2, 0)})
    r_cycle2 = frozenset({(1, 2), (2, 0), (0, 1)})
    assert gp.are_isomorphic_relations(3, r_cycle1, r_cycle2) is True

    r_path = frozenset({(0, 1), (1, 2)})
    assert gp.are_isomorphic_relations(3, r_cycle1, r_path) is False

    r_empty = frozenset()
    assert len(gp.automorphism_group(3, r_empty)) == 6

    p_swap = (1, 0, 2)
    r_swapped = gp.apply_perm_rel(p_swap, r_path)
    assert gp.iso_canon_key(3, r_path) == gp.iso_canon_key(3, r_swapped)


# ===========================================================================
# 12. Tests for Category 12: Observer Inventory
# ===========================================================================


def test_observer_inventory_and_profiles():
    """Verify nine-slot observer inventory, probing contexts, and profile separation."""
    assert len(gp.OBSERVER_SLOTS) == 9
    assert "carrier" in gp.OBSERVER_SLOTS
    assert "local_state" in gp.OBSERVER_SLOTS

    r0 = gp.EMPTY
    r1 = gp.step(r0, gp.AdmitDatum("A"))
    r2 = gp.step(r1, gp.AdmitDatum("B"))
    r3 = gp.step(r2, gp.AdmitForm(1))
    r4 = gp.step(r3, gp.AdmitInst(0, (0,)))

    ctxs = gp.contexts(r4)
    assert len(ctxs) > 0

    prof_A = gp.profile(r4, 0)
    prof_B = gp.profile(r4, 1)
    assert prof_A != prof_B
    assert gp.separable(r4, 0, 1) is True
    assert (0, 1) not in gp.collapsed_pairs(r4)


def test_observer_presheaf_cech_compatibility_and_gluing_obstruction():
    """Verify presheaf restriction, Čech 0-cycle (No-Signaling), and Čech gluing obstruction."""
    # 1. Classical Local Hidden Variable fixture (Factorizable, non-contextual)
    lhv = gp.classical_local_hidden_variable_fixture()
    compat, disc = lhv.check_cech_0_cycle_compatibility()
    assert compat is True, f"LHV must satisfy Čech 0-cycle compatibility (No-Signaling): {disc}"
    assert len(disc) == 0
    s_lhv = lhv.compute_chsh_correlator()
    assert s_lhv == pytest.approx(2.0)
    gamma_lhv = lhv.cech_gluing_obstruction()
    assert gamma_lhv == pytest.approx(0.0)
    assert lhv.has_global_gluing() is True

    # 2. Rational Pythagorean Bell fixture (Quantum contextual, exact 14/5 = 2.8)
    bell = gp.rational_pythagorean_bell_fixture()
    compat_bell, disc_bell = bell.check_cech_0_cycle_compatibility()
    assert compat_bell is True, (
        f"Pythagorean Bell must satisfy Čech 0-cycle compatibility (No-Signaling): {disc_bell}"
    )
    assert len(disc_bell) == 0
    s_bell = bell.compute_chsh_correlator()
    assert s_bell == pytest.approx(2.8)  # 14/5 = 2.8
    gamma_bell = bell.cech_gluing_obstruction()
    assert gamma_bell == pytest.approx(0.8)  # 4/5 = 0.8
    assert bell.has_global_gluing() is False  # Global gluing obstructed by contextuality

    # 3. Popescu-Rohrlich superquantum box fixture (Algebraic contextuality bound S = 4.0)
    pr = gp.pr_box_fixture()
    compat_pr, disc_pr = pr.check_cech_0_cycle_compatibility()
    assert compat_pr is True, f"PR box must satisfy Čech 0-cycle compatibility: {disc_pr}"
    s_pr = pr.compute_chsh_correlator()
    assert s_pr == pytest.approx(4.0)
    gamma_pr = pr.cech_gluing_obstruction()
    assert gamma_pr == pytest.approx(2.0)
    assert pr.has_global_gluing() is False

    # 4. Signalling / Incompatible presheaf detection
    # Perturb one context marginal so it violates Čech 0-cycle compatibility across (A1, B1) and (A1, B2)
    ctx_a1b1 = gp.MeasurementContext(("A1", "B1"))
    signaling_section = gp.LocalSection(
        context=ctx_a1b1,
        distribution={(1, 1): 0.9, (1, -1): 0.0, (-1, 1): 0.0, (-1, -1): 0.1},
    )
    signaling_sections = dict(bell.sections)
    signaling_sections[ctx_a1b1] = signaling_section
    signaling_presheaf = gp.ObserverPresheaf(contexts=bell.contexts, sections=signaling_sections)

    compat_sig, disc_sig = signaling_presheaf.check_cech_0_cycle_compatibility()
    assert compat_sig is False, "Signaling presheaf must fail Čech 0-cycle compatibility"
    assert len(disc_sig) > 0


# ===========================================================================
# 13. Tests for Category 13: Presentation Relativity
# ===========================================================================


def test_presentation_relativity_and_gauge():
    """Verify presentation frames and gauge-invariant relational observables."""
    f1 = gp.PresentationFrame(
        frame_id="frame_A",
        carrier_size=2,
        local_relations=frozenset({(0, 1)}),
    )
    t = gp.FrameTransformation(
        source_frame="frame_A",
        target_frame="frame_B",
        mapping={0: 1, 1: 0},
    )
    r_transformed = t.transform_rel(f1.local_relations)
    assert r_transformed == frozenset({(1, 0)})

    def edge_count(r: frozenset[tuple[int, int]]) -> int:
        return len(r)

    assert gp.is_gauge_invariant_observable(edge_count, f1.local_relations, [t]) is True


# ===========================================================================
# 14. Tests for Category 14: Controller Category
# ===========================================================================


def test_controller_category_and_orbits():
    """Verify 1024-member event-grammar controller family and controlled execution."""
    assert len(gp.KIND_NAMES) == 10
    kinds = gp.all_kinds()
    assert len(kinds) == 1024

    assert gp.response_live(gp.FULL_K) is True

    k_no_budget = gp.full_without("setBudget")
    assert gp.response_live(k_no_budget) is False

    s0 = gp.GENESIS_P
    ev_occ = ("admitOcc", 10)
    s_full = gp.interp_k(gp.FULL_K, s0, ev_occ)
    assert len(s_full.occ) == 1

    k_no_occ = gp.full_without("admitOcc")
    s_blocked = gp.interp_k(k_no_occ, s0, ev_occ)
    assert len(s_blocked.occ) == 0


# ===========================================================================
# 15. Tests for Category 15: Trace Algebra
# ===========================================================================


def test_trace_algebra_and_commutation():
    """Verify independent event commutation and trace consistency."""
    ev1 = ("assertWit", 0, 1)
    ev2 = ("setBudget", 50)
    assert gp.are_independent_events(ev1, ev2) is True

    s0 = gp.GENESIS_P
    assert gp.trace_commutes(s0, ev1, ev2) is True


# ===========================================================================
# 16. Tests for Category 16: Stable Content
# ===========================================================================


def test_stable_content_and_inertia():
    """Verify protected separation, quiescence, and relational inertia."""
    s = replace(
        gp.GENESIS_P,
        prot=((0, 1),),
        obs=((0,), (1,)),
    )
    assert gp.prot_sep(s, 0, 1) is True
    assert gp.prot_sep(s, 1, 0) is False

    s_next = replace(s, budget=100)
    assert gp.has_relational_inertia(s, 0, 1, [s_next]) is True


# ===========================================================================
# 17. Tests for Category 17: Weight Profile
# ===========================================================================


def test_weight_profiles_and_ray_equivalence():
    """Verify discrete weight profiles and exact integer cross-multiplication."""
    carrier = [0, 1, 2]
    w = {0: 2, 1: 4, 2: 6}
    assert gp.total(carrier, w) == 12

    v = {0: 4, 1: 8, 2: 12}
    assert gp.same_profile(carrier, w, v) is True
    assert gp.same_ray(carrier, w, v) is True

    u = {0: 2, 1: 5, 2: 6}
    assert gp.same_profile(carrier, w, u) is False

    mapping = {0: 1, 1: 1, 2: 2}
    w_trans = gp.transport_weights(mapping, w)
    assert w_trans[1] == 6
    assert w_trans[2] == 6


# ===========================================================================
# 18. Tests for Category 18: Represented Progress
# ===========================================================================


def test_represented_progress_and_retractions():
    """Verify World requirement satisfaction, quiescence, and retraction maps."""
    w0 = gp.RepresentedWorld(
        data=(0, 1, 2),
        views=((0,), (1, 2)),
        reqs=((0, 1),),
        budget=10,
    )
    assert gp.represented_sat(w0, (0, 1)) is True
    assert gp.represented_viol(w0, (0, 1)) is False
    assert gp.represented_quiescent(w0) is True

    w1 = replace(w0, reqs=((1, 2),))
    assert gp.represented_sat(w1, (1, 2)) is False
    assert gp.represented_viol(w1, (1, 2)) is True
    assert gp.represented_quiescent(w1) is False

    prop = gp.RepresentedProposalRecord(
        name="Prop1",
        target_pair=(1, 2),
        down_map={0: 0, 1: 1, 2: 2, 3: 0},
        cost=1,
    )
    assert prop.is_valid_retraction([0, 1, 2]) is True

    prop_invalid = gp.RepresentedProposalRecord(
        name="BadProp",
        target_pair=(1, 2),
        down_map={0: 1, 1: 1, 2: 2, 3: 0},
        cost=1,
    )
    assert prop_invalid.is_valid_retraction([0, 1, 2]) is False


# ===========================================================================
# 19. Tests for Category 19: Endogenous Fidelity & No-Outside Invariant
# ===========================================================================


def test_endogenous_fidelity_and_no_outside():
    """Verify Effectual-Outside Dichotomy check and represented support extraction."""
    w1 = gp.RepresentedWorld(
        data=(0, 1),
        views=((0,), (1,)),
        reqs=((0, 1),),
        refusals=(),
        budget=5,
        aug_licensed=True,
        notes=(123,),
    )
    w2 = gp.RepresentedWorld(
        data=(0, 1),
        views=((0,), (1,)),
        reqs=((0, 1),),
        refusals=(),
        budget=5,
        aug_licensed=True,
        notes=(999,),
    )
    assert gp.extract_support(w1) == gp.extract_support(w2)

    def operational_eval(w: gp.RepresentedWorld) -> bool:
        return gp.represented_quiescent(w)

    assert gp.effectual_outside_dichotomy_check(w1, w2, operational_eval) is True

    wit = gp.SymmetryBreakingWitness(
        symmetry_name="Z2_parity",
        broken_pair=(0, 1),
        distinguishing_relation="directed_wit",
    )
    assert wit.symmetry_name == "Z2_parity"
    assert wit.broken_pair == (0, 1)


# ===========================================================================
# 20. Automated Lake Elaboration and Axiom Purity Gate
# ===========================================================================


def test_lean4_lake_elaboration_and_axiom_audit():
    """Verify that all 19 Lean 4 primitive modules and AxiomAudit elaborate cleanly under Lake.

    Invariants:
    1. 'lake build' in lean4/ exits with returncode 0.
    2. Zero unproved 'sorry' or 'admit' keywords exist in any *.lean file.
    3. All theorems in AxiomAudit depend on zero custom axioms.
    """
    import re
    import shutil
    import subprocess

    lean4_dir = PRIMITIVES_DIR.parent / "lean4"
    assert lean4_dir.is_dir(), f"Missing lean4 directory: {lean4_dir}"

    # 1. Zero sorry / admit scan (excluding block and line comments)
    sorry_re = re.compile(r"\b(sorry|admit)\b")
    for lean_file in lean4_dir.glob("*.lean"):
        text = lean_file.read_text(encoding="utf-8")
        clean_text = re.sub(r"/-[\s\S]*?-/", "", text)
        for idx, l in enumerate(clean_text.splitlines(), 1):
            code_line = l.split("--")[0].strip()
            assert not sorry_re.search(code_line), (
                f"Forbidden sorry/admit found in {lean_file.name}:{idx}: {code_line}"
            )

    # 2. Lake build execution if lake binary is present
    lake_bin = shutil.which("lake")
    if not lake_bin:
        pytest.skip("Lake executable unavailable; the pinned Lean build was not run")
    pinned_version = (
        (lean4_dir / "lean-toolchain").read_text(encoding="utf-8").strip().split(":v")[-1]
    )
    version = subprocess.run(
        [lake_bin, "env", "lean", "--version"], cwd=str(lean4_dir), capture_output=True, text=True
    )
    if version.returncode or not re.search(
        rf"Lean \(version {re.escape(pinned_version)}(?:,|\))", version.stdout
    ):
        pytest.skip(
            f"Declared Lean {pinned_version} is unavailable; compatibility checks are separate"
        )
    res = subprocess.run([lake_bin, "build"], cwd=str(lean4_dir), capture_output=True, text=True)
    assert res.returncode == 0, f"Lake build failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
    # Re-emit reports even when Lake reused an already-built audit module.
    audit = subprocess.run(
        [lake_bin, "env", "lean", "AxiomAudit.lean"],
        cwd=str(lean4_dir),
        capture_output=True,
        text=True,
    )
    assert audit.returncode == 0, audit.stdout + audit.stderr
    audit_path = lean4_dir.parent / "scripts/verify_lean.py"
    spec = importlib.util.spec_from_file_location("genesis_complete_axiom_audit", audit_path)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    sources = {
        p.name: p.read_text(encoding="utf-8")
        for p in lean4_dir.glob("*.lean")
        if p.name != "lakefile.lean"
    }
    expected = verifier.scan({"education": sources})["education"]
    reports = verifier.reports(audit.stdout + audit.stderr)
    assert sorted(reports) == expected
    assert len(expected) == 9
    assert all(set(axioms) <= {"propext", "Quot.sound"} for axioms in reports.values())
