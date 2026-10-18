"""End-to-end tests for QM-214: Second Symanzik 2-forest polynomial F_G(alpha; q, m^2),
DFM spanning-tree momentum routing, and Zimmermann BPHZ forest renormalization.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.symanzik_two_forest_bphz_control import (
    DivergentSubgraph,
    bphz_two_loop_nested_sector_integrand,
    bubble_graph,
    dfm_loop_eliminated_f0,
    diamond_graph,
    enumerate_spanning_trees,
    enumerate_spanning_two_forests,
    enumerate_zimmermann_forests,
    evaluate_symanzik_two_forest_bphz_control,
    kirchhoff_schur_symanzik_f0,
    symanzik_f0_polynomial,
    symanzik_f_polynomial,
    symanzik_u_polynomial,
    tree_routed_edge_momenta,
    triangle_graph,
    vertex_divergence_of_edge_flow,
)

Q = Fraction


def test_part_a_bubble_and_triangle_symanzik_f_and_kirchhoff_duality() -> None:
    bub = bubble_graph()
    alpha_bub = [Q(2), Q(3)]
    q_bub = [(Q(5), Q(-2)), (Q(-5), Q(2))]  # ||P||^2 = 25 + 4 = 29
    m2_bub = [Q(7), Q(11)]
    assert symanzik_u_polynomial(bub, alpha_bub) == Q(5)
    assert symanzik_f0_polynomial(bub, alpha_bub, q_bub) == Q(2 * 3 * 29)  # 174
    assert kirchhoff_schur_symanzik_f0(bub, alpha_bub, q_bub) == Q(174)
    # F_G = 174 + 5 * (2*7 + 3*11) = 174 + 5 * 47 = 409
    assert symanzik_f_polynomial(bub, alpha_bub, q_bub, m2_bub) == Q(409)

    tri = triangle_graph()
    alpha_tri = [Q(2), Q(3), Q(5)]
    q_tri = [(Q(1), Q(2)), (Q(3), Q(-1)), (Q(-4), Q(-1))]
    assert symanzik_u_polynomial(tri, alpha_tri) == Q(10)
    # ||q_0||^2 = 5, ||q_1||^2 = 10, ||q_2||^2 = 17
    # Cut edges omitting single tree edge:
    # F={e0=(0,1)} isolates v2: prod = a1*a2 = 15, ||q_2||^2 = 17 -> 255
    # F={e1=(1,2)} isolates v0: prod = a0*a2 = 10, ||q_0||^2 = 5  -> 50
    # F={e2=(0,2)} isolates v1: prod = a0*a1 = 6,  ||q_1||^2 = 10 -> 60
    # Total F_0 = 255 + 50 + 60 = 365
    assert symanzik_f0_polynomial(tri, alpha_tri, q_tri) == Q(365)
    assert kirchhoff_schur_symanzik_f0(tri, alpha_tri, q_tri) == Q(365)


def test_part_a_diamond_two_loop_two_forests_match_kirchhoff_schur() -> None:
    dia = diamond_graph()
    assert len(enumerate_spanning_trees(dia)) == 8
    assert len(enumerate_spanning_two_forests(dia)) == 10

    alpha_dia = [Q(2), Q(3), Q(5), Q(7), Q(11)]
    q_dia = [(Q(2), Q(1)), (Q(-1), Q(3)), (Q(4), Q(-2)), (Q(-5), Q(-2))]
    f0_comb = symanzik_f0_polynomial(dia, alpha_dia, q_dia)
    f0_kirch = kirchhoff_schur_symanzik_f0(dia, alpha_dia, q_dia)
    assert f0_comb == f0_kirch
    assert f0_comb > Q(0)


def test_part_a_rejects_nonconserved_external_momenta() -> None:
    bub = bubble_graph()
    with pytest.raises(ValueError, match="External momenta must satisfy conservation"):
        symanzik_f0_polynomial(bub, [Q(1), Q(1)], [(Q(1), Q(0)), (Q(1), Q(0))])


def test_part_b_dfm_spanning_tree_momentum_routing_and_tree_invariance() -> None:
    dia = diamond_graph()
    alpha_dia = [Q(2), Q(3), Q(5), Q(7), Q(11)]
    q_dia = [(Q(2), Q(1)), (Q(-1), Q(3)), (Q(4), Q(-2)), (Q(-5), Q(-2))]
    u_expected = symanzik_u_polynomial(dia, alpha_dia)
    f0_expected = symanzik_f0_polynomial(dia, alpha_dia, q_dia)

    trees = enumerate_spanning_trees(dia)
    for tree in trees:
        p_t = tree_routed_edge_momenta(dia, tree, q_dia)
        assert vertex_divergence_of_edge_flow(dia, p_t) == q_dia
        for e_idx in range(dia.edge_count):
            if e_idx not in tree:
                assert p_t[e_idx] == (Q(0), Q(0))
        u_dfm, f0_dfm = dfm_loop_eliminated_f0(dia, tree, alpha_dia, q_dia)
        assert u_dfm == u_expected
        assert f0_dfm == f0_expected


def test_part_c_zimmermann_forests_and_uv_pole_cancellation() -> None:
    overlapping_subs = [
        DivergentSubgraph("gamma_L", frozenset({0, 1, 2}), 0),
        DivergentSubgraph("gamma_R", frozenset({2, 3, 4}), 0),
        DivergentSubgraph("G_all", frozenset({0, 1, 2, 3, 4}), 0),
    ]
    forests = enumerate_zimmermann_forests(overlapping_subs)
    assert len(forests) == 6
    for f in forests:
        names = {g.name for g in f}
        assert not ("gamma_L" in names and "gamma_R" in names)

    # Check exact UV pole cancellation across arbitrarily small sector variables
    for lam1 in [Q(1, 5), Q(1, 100), Q(1, 1000000)]:
        for lam2 in [Q(1, 7), Q(1, 200), Q(1, 1000000)]:
            res = bphz_two_loop_nested_sector_integrand(lam1, lam2, Q(3, 5))
            assert res["r_sum"] == res["r_analytic_regular"]


def test_full_qm214_receipt() -> None:
    receipt = evaluate_symanzik_two_forest_bphz_control()
    assert receipt["all_graphs_f0_match_kirchhoff_schur"] is True
    assert receipt["dfm_all_eight_trees_conserve_momentum"] is True
    assert receipt["dfm_all_eight_trees_match_f0_and_u"] is True
    assert receipt["dfm_tree_change_is_cycle_cocycle"] is True
    assert receipt["bphz_nested_2loop_forest_count"] == 4
    assert receipt["bphz_overlapping_subgraph_forest_count"] == 6
    assert receipt["bphz_uv_boundary_poles_cancel_identically"] is True
    assert receipt["bphz_uv_boundary_regular_value_at_zero"] == Q(9, 25)
