"""Exact cochain helpers: construction guards, Phi1, Gamma2, classes, Hodge split."""

from fractions import Fraction as F
from itertools import product

import cochain
import pytest
from cochain import CochainError, Complex


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


TRIANGLE = Complex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("c", "a")), (((0, 1), (1, 1), (2, 1)),))
SQUARE = Complex(("a", "b", "c", "d"), (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")))
THETA = Complex(
    ("a", "b", "c", "d"),
    (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("a", "c")),
)


@pytest.mark.parametrize(
    "vertices,edges,faces,weights,code",
    [
        (("a", "a"), (), (), None, "DUPLICATE_VERTEX"),
        (("a",), (("a", "b"),), (), None, "UNKNOWN_VERTEX"),
        (("a",), (("a", "a"),), (), None, "SELF_LOOP"),
        (("a", "b"), (("a", "b"),), (((1, 1),),), None, "MALFORMED_FACE"),
        (("a", "b"), (("a", "b"),), (((0, 2),),), None, "MALFORMED_FACE"),
        (
            ("a", "b", "c"),
            (("a", "b"), ("b", "c"), ("c", "a")),
            (((0, True), (1, 1), (2, 1)),),
            None,
            "MALFORMED_FACE",
        ),
        (("a", "b"), (("a", "b"),), (), (F(1), F(1)), "WEIGHT_LENGTH"),
        (("a", "b"), (("a", "b"),), (), (F(0),), "NONPOSITIVE_WEIGHT"),
        (("a", "b"), (("a", "b"),), (((0, 1),),), None, "CHAIN_LAW_VIOLATED"),
    ],
)
def test_malformed_complexes_are_refused(vertices, edges, faces, weights, code):
    with pytest.raises(CochainError) as err:
        Complex(vertices, edges, faces, weights)
    assert err.value.code == code


@pytest.mark.parametrize("value,code", [(0.5, "FLOAT_FORBIDDEN"), (True, "BOOL_FORBIDDEN"), ("1", "NOT_EXACT")])
def test_only_exact_rationals_are_admitted(value, code):
    with pytest.raises(CochainError) as err:
        cochain.exact(value)
    assert err.value.code == code


def test_d0_requires_a_total_potential_and_cochain_length_is_checked():
    with pytest.raises(CochainError) as err:
        TRIANGLE.d0({"a": F(0)})
    assert err.value.code == "POTENTIAL_NOT_TOTAL"
    with pytest.raises(CochainError) as err:
        TRIANGLE.d1((1, 2))
    assert err.value.code == "COCHAIN_LENGTH"


def test_matrices_agree_with_the_operators():
    phi = {"a": F(0), "b": F(2), "c": F(5)}
    x = (F(1), F(-2), F(4))
    assert cochain.matvec(TRIANGLE.d0_matrix(), (F(0), F(2), F(5))) == TRIANGLE.d0(phi)
    assert cochain.matvec(TRIANGLE.d1_matrix(), x) == TRIANGLE.d1(x)
    assert all(v == 0 for row in cochain.matmul(TRIANGLE.d1_matrix(), TRIANGLE.d0_matrix()) for v in row)


def test_exactness_gamma2_and_classes_on_a_filled_triangle():
    assert cochain.exact_potential(TRIANGLE, (1, 2, -3)) is not None
    assert cochain.classify(TRIANGLE, (1, 2, -3)) == cochain.EXACT_REPAIR
    assert cochain.gamma2(TRIANGLE, (1, 1, 1)) == 3
    assert cochain.classify(TRIANGLE, (1, 1, 1)) == cochain.ACTIVE_CLOSURE_FAILURE
    assert cochain.phi1(TRIANGLE, (1, 1, 1)) == 3


def test_a_hollow_cycle_carries_a_closed_residual():
    x = (1, 0, 0, 0)
    assert cochain.gamma2(SQUARE, x) == 0
    assert cochain.classify(SQUARE, x) == cochain.CLOSED_RESIDUAL
    assert cochain.phi1(SQUARE, x) == 1
    assert cochain.cycle_coordinates(SQUARE, x) == (F(1),)
    assert cochain.phi1(SQUARE, (3, 0, 0, 0)) == 3
    assert cochain.phi1(SQUARE, (1, 1, 1, 1)) == 4


def test_weighted_phi1_uses_the_cheapest_edge():
    weighted = Complex(SQUARE.vertices, SQUARE.edges, (), (F(5), F(1), F(5), F(5)))
    assert cochain.phi1(weighted, (4, 0, 0, 0)) == 4


def test_phi1_is_gauge_invariant_and_matches_brute_force_on_small_grids():
    # Brute force over integer potentials in a box: the l1 optimum of an integer
    # cochain on this graph is attained at an integer potential.
    values = range(-2, 3)
    for x in product(range(-1, 2), repeat=5):
        best = min(
            sum(abs(xe - de) for xe, de in zip(x, THETA.d0({"a": 0, "b": b, "c": c, "d": d})))
            for b, c, d in product(values, repeat=3)
        )
        assert cochain.phi1(THETA, x) == best
        shifted = tuple(xe + de for xe, de in zip(x, THETA.d0({"a": 0, "b": 1, "c": -1, "d": 2})))
        assert cochain.phi1(THETA, shifted) == cochain.phi1(THETA, x)
        assert len(cochain.cycle_coordinates(THETA, x)) == THETA.first_betti_of_graph() == 2


def test_phi1_refuses_when_the_forest_enumeration_is_over_budget(monkeypatch):
    monkeypatch.setattr(cochain, "PHI1_SUBSET_BUDGET", 1)
    with pytest.raises(CochainError) as err:
        cochain.phi1(SQUARE, (1, 0, 0, 0))
    assert err.value.code == "BUDGET_UNKNOWN"


def test_disconnected_complexes_fix_one_gauge_per_component():
    two = Complex(("a", "b", "c", "d"), (("a", "b"), ("c", "d")))
    assert len(two.components()) == 2
    potential = cochain.exact_potential(two, (3, -4))
    assert potential is not None and two.d0(potential) == (F(3), F(-4))
    assert cochain.phi1(two, (3, -4)) == 0


def test_hodge_split_is_orthogonal_and_matches_the_classes():
    cases = [(TRIANGLE, (1, 2, -3)), (TRIANGLE, (1, 1, 1)), (SQUARE, (1, 0, 0, 0)), (THETA, (1, -1, 2, 0, 1))]
    for cx, x in cases:
        exact_part, coexact, harmonic = cochain.hodge_split(cx, x)
        assert tuple(a + b + c for a, b, c in zip(exact_part, coexact, harmonic)) == cochain.exact_vector(x)
        assert dot(exact_part, coexact) == dot(exact_part, harmonic) == dot(coexact, harmonic) == 0
        assert all(v == 0 for v in cx.d1(harmonic))
        assert all(v == 0 for v in cochain.matvec(cochain.transpose(cx.d0_matrix()), harmonic))
        assert cochain.exact_potential(cx, exact_part) is not None
        # FOC classes read off the Hodge support: Gamma2 > 0 iff co-exact part is non-zero,
        # Phi1 = 0 iff both co-exact and harmonic parts vanish.
        klass = cochain.classify(cx, x)
        assert (klass == cochain.ACTIVE_CLOSURE_FAILURE) == any(coexact)
        assert (klass == cochain.EXACT_REPAIR) == (not any(coexact) and not any(harmonic))


def test_hodge_split_without_edges_and_solver_refusal():
    empty = Complex(("a",), ())
    assert cochain.hodge_split(empty, ()) == ((), (), ())
    with pytest.raises(CochainError) as err:
        cochain.solve_consistent(((F(0),),), (F(1),))
    assert err.value.code == "INCONSISTENT_SYSTEM"
    assert cochain.transpose(()) == ()
    assert cochain.matmul((), ((F(1),),)) == ()


def test_maurer_cartan_obstruction_detects_unlawful_deformations():
    d0 = TRIANGLE.d0_matrix()
    d1 = TRIANGLE.d1_matrix()
    zero0 = tuple(tuple(F(0) for _ in row) for row in d0)
    zero1 = tuple(tuple(F(0) for _ in row) for row in d1)
    assert all(v == 0 for row in cochain.deformation_obstruction(d0, d1, zero0, zero1) for v in row)
    bump = tuple(tuple(F(1) if (i, j) == (0, 0) else F(0) for j in range(len(row))) for i, row in enumerate(d0))
    assert any(v != 0 for row in cochain.deformation_obstruction(d0, d1, bump, zero1) for v in row)
    short = ((F(1),),)
    with pytest.raises(CochainError) as err:
        cochain.deformation_obstruction(d0, d1, short, zero1)
    assert err.value.code == "SHAPE"
    narrow = ((F(1), F(0)),)
    with pytest.raises(CochainError) as err:
        cochain.deformation_obstruction(d0, narrow, zero0, narrow)
    assert err.value.code == "SHAPE"


def test_phi1_certificates_close_the_duality_gap_exactly():
    """Primal potential and dual flow agree on every small case (Gate 4 dual witness)."""
    for x in product(range(-1, 2), repeat=5):
        cert = cochain.phi1_certificate(THETA, x)
        assert cert.value == cochain.phi1(THETA, x)
        assert cochain.check_certificate(THETA, x, cert)
    weighted = Complex(SQUARE.vertices, SQUARE.edges, (), (F(5), F(1), F(5), F(5)))
    cert = cochain.phi1_certificate(weighted, (4, 0, 0, 0))
    assert cert.value == 4 and cochain.check_certificate(weighted, (4, 0, 0, 0), cert)
    for cx, x in ((TRIANGLE, (1, 1, 1)), (SQUARE, (1, 0, 0, 0)), (TRIANGLE, (1, 2, -3))):
        cert = cochain.phi1_certificate(cx, x)
        assert cochain.check_certificate(cx, x, cert)


def test_a_wrong_certificate_is_rejected():
    cert = cochain.phi1_certificate(SQUARE, (1, 0, 0, 0))
    too_big = cochain.Phi1Certificate(cert.value, cert.potential, tuple(2 * y for y in cert.dual))
    assert not cochain.check_certificate(SQUARE, (1, 0, 0, 0), too_big)
    wrong_value = cochain.Phi1Certificate(cert.value + 1, cert.potential, cert.dual)
    assert not cochain.check_certificate(SQUARE, (1, 0, 0, 0), wrong_value)
    short = cochain.Phi1Certificate(cert.value, cert.potential, cert.dual[:-1])
    assert not cochain.check_certificate(SQUARE, (1, 0, 0, 0), short)


def test_certificate_budget_refusal(monkeypatch):
    monkeypatch.setattr(cochain, "PHI1_SUBSET_BUDGET", 1)
    with pytest.raises(CochainError) as err:
        cochain.phi1_certificate(SQUARE, (1, 0, 0, 0))
    assert err.value.code == "BUDGET_UNKNOWN"


def test_a_duality_gap_is_refused_not_hidden(monkeypatch):
    monkeypatch.setattr(cochain, "check_certificate", lambda *args: False)
    with pytest.raises(CochainError) as err:
        cochain.phi1_certificate(SQUARE, (1, 0, 0, 0))
    assert err.value.code == "DUALITY_GAP"
