
from witnessed_difference.native_functionals import representative_mass
from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product

import pytest
import witnessed_difference.simplicial as simplicial
from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    DiagnosticClass,
    d0_adjoint,
    d0_matrix,
    d1_matrix,
    obstruction_signature,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.simplicial import (
    RP2_FACETS,
    OrientedSimplicialComplex,
    bianchi_identity,
    cycle_pairing_gauge_invariant,
    divergence_total,
    from_facets,
    gauss_law_solvable,
    make_simplicial_complex,
    rank_mod_p,
    rank_rational,
    rp2_six_vertex,
    rp2_torsion_witness,
    tetrahedron,
)


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def filled_triangle() -> OrientedSimplicialComplex:
    return accepted(from_facets((0, 1, 2), ((0, 1, 2),)))


@pytest.mark.parametrize(
    ("vertices", "simplices", "code"),
    [
        ((0, 0), ((0,),), RefusalCode.INVALID_INPUT),
        ([0, 1], ((0,), (1,)), RefusalCode.INVALID_INPUT),
        ((0, 1), ((0,), (1,), (0, 2)), RefusalCode.OUTSIDE_CARRIER),
        ((0, 1), ((0,), (1,), (0, 1, 1)), RefusalCode.INVALID_INPUT),
        ((0, 1, 2), ((0,), (1,), (2,), (0, 1, 2)), RefusalCode.INVALID_INPUT),
        ((0, 1), ((0,), (1,), (0, 1), (1, 0)), RefusalCode.INVALID_INPUT),
        ((0, 1), ((0,), (0, 1)), RefusalCode.INVALID_INPUT),
        ((0, 1), ((0,), (1,), ()), RefusalCode.INVALID_INPUT),
    ],
)
def test_simplicial_complex_refusals(vertices, simplices, code) -> None:
    refused(make_simplicial_complex(vertices, simplices), code)


@pytest.mark.parametrize(
    ("vertices", "simplices", "message"),
    [
        ((0, 1), ((0,), (1,), (1, 0)), "vertex order"),
        ((0, 1), ((0,), (1,), (0, 0)), "degenerate"),
        ((0, 1), [(0,), (1,)], "immutable"),
        ((0, 1, 2), ((0,), (1,), (2,), (0, 1), (0, 1, 2)), "downward closed"),
        ((0, 1), ((0,), (1,), (0, 1), (0, 1)), "repeat"),
        ((0, 0), ((0,),), "unique"),
    ],
)
def test_direct_construction_validates_the_same_invariants(vertices, simplices, message) -> None:
    with pytest.raises(ValueError, match=message):
        OrientedSimplicialComplex(vertices, simplices)


def test_facet_closure_refusals_and_sorting() -> None:
    refused(from_facets((0, 1), ((0, 0),)), RefusalCode.INVALID_INPUT, "degenerate")
    refused(from_facets((0, 1), ((0, 9),)), RefusalCode.OUTSIDE_CARRIER)
    complex_ = accepted(make_simplicial_complex(("b", "a"), (("b",), ("a",), ("a", "b"))))
    assert ("b", "a") in complex_.simplices and complex_.dimension == 1


def test_coboundary_convention_matches_the_degree_one_window() -> None:
    oriented = filled_triangle()
    window = FiniteComplex((0, 1, 2), oriented.k_simplices(1), oriented.k_simplices(2))
    assert oriented.coboundary_matrix(0) == d0_matrix(window)
    assert oriented.coboundary_matrix(1) == d1_matrix(window)
    assert oriented.coboundary_matrix(2) == ()
    with pytest.raises(ValueError):
        oriented.coboundary_matrix(-1)


def test_nilpotence_in_every_degree() -> None:
    assert accepted(tetrahedron().verify_nilpotence()) == 2
    assert accepted(rp2_six_vertex().verify_nilpotence()) == 1
    assert accepted(accepted(make_simplicial_complex((0,), ((0,),))).verify_nilpotence()) == 0
    product_ = simplicial.matrix_product(
        tetrahedron().coboundary_matrix(2), tetrahedron().coboundary_matrix(1), 6
    )
    assert product_ == ((Fraction(0),) * 6,)


def test_nilpotence_failure_is_refused(monkeypatch) -> None:
    original = OrientedSimplicialComplex.coboundary_matrix

    def breaking(degree):
        def broken(self, k):
            matrix = original(self, k)
            return tuple(tuple(abs(entry) for entry in row) for row in matrix) if k == degree else matrix

        return broken

    monkeypatch.setattr(OrientedSimplicialComplex, "coboundary_matrix", breaking(2))
    refused(tetrahedron().verify_nilpotence(), RefusalCode.CERTIFICATE_MISMATCH, "delta^2 delta^1")
    monkeypatch.setattr(OrientedSimplicialComplex, "coboundary_matrix", breaking(1))
    refused(rp2_torsion_witness(), RefusalCode.CERTIFICATE_MISMATCH, "delta^1 delta^0")


def test_betti_numbers_over_q_and_finite_fields() -> None:
    rp2 = rp2_six_vertex()
    assert accepted(rp2.betti_numbers("Q")) == (1, 0, 0)
    assert accepted(rp2.betti_numbers(2)) == (1, 1, 1)
    assert accepted(rp2.betti_numbers(3)) == (1, 0, 0)
    assert accepted(tetrahedron().betti_numbers(2)) == (1, 0, 0, 0)
    circle = accepted(from_facets((0, 1, 2), ((0, 1), (1, 2), (0, 2))))
    assert accepted(circle.betti_numbers()) == (1, 1)
    for field in ("R", 4, 1, True, 2.0):
        refused(rp2.betti_numbers(field), RefusalCode.INVALID_INPUT)


def test_exact_ranks_over_q_and_f_p() -> None:
    assert rank_rational([]) == 0 and rank_mod_p([], 2) == 0
    assert rank_rational([[1, 2], [2, 4]]) == 1
    assert rank_rational([[2]]) == 1 and rank_mod_p([[2]], 2) == 0
    assert rank_rational([["1/2", 0], [0, 3]]) == 2
    assert rank_mod_p([["1/3", 0], [0, 3]], 2) == 2
    assert rank_mod_p([[1, 1], [1, -1]], 2) == 1 and rank_mod_p([[1, 1], [1, -1]], 3) == 2
    assert rank_rational([[0, 0], [0, 1]]) == 1
    with pytest.raises(TypeError):
        rank_rational([[1.0]])
    with pytest.raises(ValueError, match="equal length"):
        rank_rational([[1], [1, 2]])
    with pytest.raises(ValueError, match="p-integral"):
        rank_mod_p([["1/2"]], 2)
    for p in (4, 1, True, "2"):
        with pytest.raises(ValueError, match="prime"):
            rank_mod_p([[1]], p)


def test_rp2_is_a_closed_ten_triangle_surface() -> None:
    rp2 = rp2_six_vertex()
    assert len(RP2_FACETS) == 10
    for edge in rp2.k_simplices(1):
        assert sum(set(edge) <= set(face) for face in RP2_FACETS) == 2
    assert rp2.k_simplices(1) == tuple(combinations(range(6), 2))


def test_rp2_torsion_witness_separates_rational_and_mod_two_cohomology() -> None:
    record = accepted(rp2_torsion_witness())
    assert record.face_counts == (6, 15, 10) and record.euler_characteristic == 1
    assert (record.rank_delta0_q, record.rank_delta1_q) == (5, 10)
    assert (record.rank_delta0_f2, record.rank_delta1_f2) == (5, 9)
    assert (record.h2_q, record.h2_f2, record.h1_f2) == (0, 1, 1)
    assert record.bockstein_nonzero and record.rational_solver_misses_torsion
    assert record.triangle_class_rationally_exact and record.triangle_class_nonzero_mod2
    assert all(value % 2 == 0 for value in record.integral_coboundary) and any(record.integral_coboundary)
    assert sum(record.torsion_cocycle) == 5


def test_rational_quotient_solver_reports_the_mod_two_class_as_exact() -> None:
    rp2 = rp2_six_vertex()
    faces = rp2.k_simplices(2)
    triangle = {face: int(index == 0) for index, face in enumerate(faces)}
    signature = accepted(rp2.degree_k_signature(2, triangle))
    assert signature.phi == 0 and signature.diagnostic_class is DiagnosticClass.EXACT_CLASS
    assert signature.gamma == 0 and signature.closure_ratio is None and signature.opnorm == 0
    assert any(value.denominator != 1 for value in signature.certificate.potential)
    delta1 = rp2.coboundary_matrix(1)
    column = tuple(row + (Fraction(triangle[face]),) for row, face in zip(delta1, faces))
    assert rank_mod_p(column, 2) == rank_mod_p(delta1, 2) + 1
    even = tuple(row + (Fraction(1),) for row in delta1)
    assert rank_mod_p(even, 2) == rank_mod_p(delta1, 2)


def test_degree_one_signature_agrees_with_the_graph_window() -> None:
    oriented = filled_triangle()
    values = {(0, 1): 1, (1, 2): 1, (0, 2): 0}
    signature = accepted(oriented.degree_k_signature(1, values))
    window = FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)), ((0, 1, 2),))
    graph = accepted(obstruction_signature(window, values, closure_declared=True))
    assert (signature.phi, signature.gamma, signature.opnorm) == (graph.phi1, graph.gamma2, graph.d1_opnorm)
    assert signature.diagnostic_class is graph.diagnostic_class is DiagnosticClass.ACTIVE_CLOSURE_FAILURE
    assert type(signature.phi) is Fraction and type(signature.gamma) is Fraction


@pytest.mark.parametrize(("degree", "norm"), [(0, 3), (1, 2), (2, 1), (3, 0)])
def test_degree_k_theorem_e_on_the_tetrahedron(degree, norm) -> None:
    complex_ = tetrahedron()
    simplices = complex_.k_simplices(degree)
    for values in product((0, 1, -1), repeat=len(simplices)) if len(simplices) <= 4 else product((0, 1), repeat=6):
        signature = accepted(complex_.degree_k_signature(degree, dict(zip(simplices, values))))
        assert signature.opnorm == norm
        assert signature.gamma <= norm * signature.phi
        if signature.closure_ratio is not None:
            assert 0 <= signature.closure_ratio <= norm
        if degree == 0:
            assert signature.phi == representative_mass(values)


def test_degree_k_signature_refusals(monkeypatch) -> None:
    complex_ = tetrahedron()
    edges = complex_.k_simplices(1)
    refused(complex_.degree_k_signature(4, {}), RefusalCode.OUTSIDE_CARRIER)
    refused(complex_.degree_k_signature("1", {}), RefusalCode.OUTSIDE_CARRIER)
    refused(complex_.degree_k_signature(1, {edges[0]: 1}), RefusalCode.INVALID_INPUT)
    refused(complex_.degree_k_signature(1, [1] * 6), RefusalCode.INVALID_INPUT)
    refused(complex_.degree_k_signature(1, {edge: 1.0 for edge in edges}), RefusalCode.INVALID_INPUT)
    honest = accepted(complex_.degree_k_signature(1, {edge: 1 for edge in edges})).certificate

    def lying(*args, **kwargs):
        return Accepted(replace(honest, value=Fraction(0)))

    monkeypatch.setattr(simplicial, "matrix_quotient_l1", lying)
    refused(
        complex_.degree_k_signature(1, {edge: 1 for edge in edges}),
        RefusalCode.CERTIFICATE_MISMATCH,
        "Gamma_{k+1}",
    )


def test_divergence_total_vanishes_on_every_finite_oriented_graph() -> None:
    graphs = (
        FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)), ((0, 1, 2),)),
        FiniteComplex((0, 1, 2), ((0, 1), (1, 2))),
        FiniteComplex(("source", "sink", "isolated"), (("source", "sink"),)),
        FiniteComplex((0, 1, 2, 3), ((0, 1), (2, 3), (1, 2))),
    )
    for graph in graphs:
        for values in product((-2, 0, 1, "1/3"), repeat=len(graph.edges)):
            flux = dict(zip(graph.edges, values))
            assert divergence_total(graph, flux) == 0
            assert type(divergence_total(graph, flux)) is Fraction


def test_gauss_law_is_solved_exactly_when_each_component_is_neutral() -> None:
    path = FiniteComplex((0, 1, 2, 3), ((0, 1), (2, 1), (2, 3)))
    rho = {0: 1, 1: "-5/2", 2: 0, 3: "3/2"}
    flow = accepted(gauss_law_solvable(path, rho))
    assert d0_adjoint(path, flow) == {vertex: Fraction(value) for vertex, value in rho.items()}
    split = FiniteComplex((0, 1, 2, 3), ((0, 1), (2, 3)))
    assert d0_adjoint(split, accepted(gauss_law_solvable(split, {0: 1, 1: -1, 2: 3, 3: -3})))[3] == -3


def test_gauss_law_refusals() -> None:
    triangle = FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)))
    refused(gauss_law_solvable(triangle, {0: 1, 1: 2, 2: -2}), RefusalCode.INFEASIBLE, "sum_v (d0* x)(v) = 0")
    split = FiniteComplex((0, 1, 2, 3), ((0, 1), (2, 3)))
    refused(gauss_law_solvable(split, {0: 1, 1: -2, 2: 0, 3: 1}), RefusalCode.INFEASIBLE, "component")
    refused(gauss_law_solvable(triangle, {0: 1, 1: -1}), RefusalCode.INVALID_INPUT)
    refused(gauss_law_solvable(triangle, [0, 0, 0]), RefusalCode.INVALID_INPUT)
    refused(gauss_law_solvable(triangle, {0: 0.5, 1: -0.5, 2: 0}), RefusalCode.INVALID_INPUT)


def test_cycle_pairings_are_gauge_invariant() -> None:
    square = FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2)))
    connection = dict(zip(square.edges, (1, "2/3", -4, 5, 7)))
    cycle = {(0, 1): 1, (1, 2): 1, (2, 3): 2, (0, 3): -2, (0, 2): 1}
    for gauge in product((-1, 0, "1/2"), repeat=4):
        record = accepted(cycle_pairing_gauge_invariant(square, connection, cycle, dict(zip(range(4), gauge))))
        assert record.invariant and record.before == record.after == Fraction(-28, 3)
    refused(
        cycle_pairing_gauge_invariant(square, connection, dict(zip(square.edges, (1, 0, 0, 0, 0))), dict.fromkeys(range(4), 0)),
        RefusalCode.NOT_CLOSED,
    )
    for bad in (
        ({**connection, (0, 1): 1.0}, cycle, dict.fromkeys(range(4), 0)),
        (connection, {(0, 1): 1}, dict.fromkeys(range(4), 0)),
        (connection, cycle, {0: 1}),
    ):
        refused(cycle_pairing_gauge_invariant(square, *bad), RefusalCode.INVALID_INPUT)


def test_bianchi_identity_on_the_tetrahedron_exhaustively() -> None:
    complex_ = tetrahedron()
    edges = complex_.k_simplices(1)
    for values in product((-1, 0, 1), repeat=6):
        record = accepted(bianchi_identity(complex_, dict(zip(edges, values))))
        assert record.curvature_coboundary == (Fraction(0),)
    record = accepted(bianchi_identity(filled_triangle(), {(0, 1): 1, (0, 2): 0, (1, 2): 1}))
    assert record.curvature == (Fraction(2),) and record.curvature_coboundary == ()
    refused(bianchi_identity(accepted(from_facets((0, 1), ((0, 1),))), {(0, 1): 1}), RefusalCode.INVALID_INPUT)
    refused(bianchi_identity("K", {}), RefusalCode.INVALID_INPUT)
    refused(bianchi_identity(complex_, {edges[0]: 1}), RefusalCode.INVALID_INPUT)
    refused(bianchi_identity(complex_, dict.fromkeys(edges, 0.5)), RefusalCode.INVALID_INPUT)


def test_strings_are_not_sequences_of_vertices_or_digits() -> None:
    from witnessed_difference.simplicial import from_facets, make_simplicial_complex, rank_rational

    with pytest.raises(TypeError, match="not a string"):
        rank_rational(["12", "24"])
    with pytest.raises(TypeError, match="not a string"):
        rank_rational("1224")
    assert rank_rational([[1, 2], [2, 4]]) == 1
    refused(make_simplicial_complex(("a", "b"), ("a", "b", "ab")), RefusalCode.INVALID_INPUT, "sequence of vertices")
    refused(from_facets(("a", "b"), ("ab",)), RefusalCode.INVALID_INPUT, "sequence of vertices")
    assert isinstance(from_facets(("a", "b"), (("a", "b"),)), Accepted)


# Executable finite evidence; AuthorityEffect: None.
