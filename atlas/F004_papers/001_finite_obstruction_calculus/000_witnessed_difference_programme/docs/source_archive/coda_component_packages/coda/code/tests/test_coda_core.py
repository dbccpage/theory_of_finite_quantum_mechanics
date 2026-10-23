"""Independent counterexamples, exact certificates, and bounded exhaustions."""

from dataclasses import replace
from fractions import Fraction
from itertools import product

import pytest
from audit_legacy_embedding import audit
from coda_core import (
    Collision,
    affine_quadrature,
    coordinate_packet,
    evaluate_menu,
    factor_or_collision,
    parity_sections,
    rational,
    sample_collision,
    standing,
    verify_coordinate_certificate,
)


def test_factorization_against_all_boolean_fibers():
    states = tuple(range(4))
    for obs in product(range(2), repeat=4):
        for query in product(range(2), repeat=4):
            result = factor_or_collision(states, obs.__getitem__, query.__getitem__)
            collisions = [
                (a, b)
                for a in states
                for b in states
                if obs[a] == obs[b] and query[a] != query[b]
            ]
            if collisions:
                assert isinstance(result, Collision)
                assert (result.left, result.right) in collisions
            else:
                assert not isinstance(result, Collision)
                assert set(result) == set(obs)
                assert all(result[obs[x]] == query[x] for x in states)


def test_empty_image_and_off_image_values():
    assert factor_or_collision([], lambda x: x, lambda x: x) == {}
    assert factor_or_collision([1, 2], lambda _: "realized", lambda _: 7) == {
        "realized": 7
    }


def test_coarsening_retains_collision_and_augmentation_can_remove_it():
    states = tuple(product((0, 1), repeat=2))
    assert isinstance(
        factor_or_collision(states, lambda _: 0, lambda x: x[1]), Collision
    )
    assert factor_or_collision(states, lambda x: x, lambda x: x[1]) == dict(
        (x, x[1]) for x in states
    )


def test_incomplete_search_never_claims_exhaustion_or_minimality():
    menu = {"fails": 0, "expensive": 8, "cheap": 1}
    def works(x):
        return x != "fails"
    for budget in (0, 1, 2):
        result = evaluate_menu(menu, works, budget)
        assert result.status == "BudgetUnknown"
        assert result.minima == ()
    assert evaluate_menu(menu, works).minima == ("cheap",)
    assert evaluate_menu({"fails": 0}, works).status == "ExhaustedDeclaredMenu"


def test_ties_and_vacuous_empty_menu_are_scoped():
    assert evaluate_menu(
        {"a": Fraction(1, 2), "b": Fraction(1, 2)}, lambda _: True
    ).minima == ("a", "b")
    empty = evaluate_menu({}, lambda _: True)
    assert empty.status == "ExhaustedDeclaredMenu" and empty.declared == 0


@pytest.mark.parametrize("bad", [0.1, float("nan"), float("inf"), True, "1/3"])
def test_exact_boundary_rejects_approximate_or_untyped_inputs(bad):
    with pytest.raises(TypeError):
        rational(bad)
    with pytest.raises(TypeError):
        coordinate_packet((0, bad, 0))


@pytest.mark.parametrize("values", list(product((-2, 0, 3), repeat=3)))
def test_linear_certificate_and_independent_repair_bounds(values):
    certificate = coordinate_packet(values)
    assert verify_coordinate_certificate(certificate)
    a, b, c = values
    # Independent finite probes support, but do not replace, the dual bound.
    for repair in (Fraction(n, 2) for n in range(-9, 10)):
        assert certificate.phi <= abs(a + repair) + abs(b) + abs(c)
    assert certificate.gamma == abs(c)


def test_forged_dual_primal_value_and_grade_are_rejected():
    good = coordinate_packet((2, 3, 5))
    for bad in (
        replace(good, repair=0),
        replace(good, dual=(1, 1, 1)),
        replace(good, dual=(0, 2, 1)),
        replace(good, phi=0),
        replace(good, gamma=0),
        replace(good, grade="ExactRepair"),
        replace(good, residual=(0, 3, 4)),
        replace(good, phi=8.0),
    ):
        assert not verify_coordinate_certificate(bad)


def test_triangle_local_sections_do_not_glue():
    edges = ((0, 1, 0), (1, 2, 0), (2, 0, 1))
    assert all(len(parity_sections(3, [edge])) == 4 for edge in edges)
    assert parity_sections(3, edges) == ()
    assert len(parity_sections(3, [(0, 1, 0), (1, 2, 0), (2, 0, 0)])) == 2


@pytest.mark.parametrize("n", [1, 2, 3, 10, 37, 100])
def test_quadrature_against_closed_form(n):
    result = affine_quadrature(n)
    assert result["left"] == 50 - Fraction(50, n)
    assert result["right"] == 50 + Fraction(50, n)
    assert result["trapezoid"] == result["integral"] == 50


def test_sample_collision_has_exact_positive_area_difference():
    collision = sample_collision()
    assert collision["perturbation_at_nodes"] == (0, 0, 0)
    assert collision["area_difference"] == Fraction(1, 84)
    assert collision["perturbed_integral"] == Fraction(4201, 84)


def test_evidence_without_grant_and_actual_legacy_counterexample():
    assert standing(True, False) is False
    assert standing(True, True) is True
    result = audit()
    assert result["identical_span_data"] is True
    assert result["legacy_checker_reports_faithful"] is True


@pytest.mark.parametrize("n", [0, -1, True, 1.5])
def test_invalid_panel_counts(n):
    with pytest.raises(ValueError):
        affine_quadrature(n)


def test_invalid_declared_inputs():
    with pytest.raises(ValueError):
        evaluate_menu({"a": -1}, lambda _: True)
    with pytest.raises(ValueError):
        evaluate_menu({}, lambda _: True, -1)
    with pytest.raises(TypeError):
        evaluate_menu({"a": 1}, lambda _: "yes")
    with pytest.raises(ValueError):
        coordinate_packet((1, 2))
    with pytest.raises(ValueError):
        parity_sections(3, [(0, 3, 0)])
    with pytest.raises(TypeError):
        standing(1, True)
