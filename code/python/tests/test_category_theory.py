"""Tests for finite categories and report-query factorization."""

from src.category_theory.finite_category import (
    FiniteCategory,
    verify_report_query_factorization,
)


def test_finite_arrow_category_axioms() -> None:
    cat = FiniteCategory(
        objects=frozenset({"A", "B"}),
        morphisms={"id_A": ("A", "A"), "id_B": ("B", "B"), "f": ("A", "B")},
        identities={"A": "id_A", "B": "id_B"},
        composition={
            ("id_A", "id_A"): "id_A",
            ("id_B", "id_B"): "id_B",
            ("f", "id_A"): "f",
            ("id_B", "f"): "f",
        },
    )
    assert cat.verify_axioms() is True


def test_report_query_factorization_and_collision_obstruction() -> None:
    report = {0: 10, 1: 10, 2: 20}
    compatible_query = {0: 1, 1: 1, 2: 0}
    obstructed_query = {0: 1, 1: 0, 2: 0}

    ok, dec = verify_report_query_factorization(report, compatible_query)
    assert ok is True
    assert dec == {10: 1, 20: 0}

    ok_bad, _ = verify_report_query_factorization(report, obstructed_query)
    assert ok_bad is False
