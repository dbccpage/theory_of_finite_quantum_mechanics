from fractions import Fraction

import pytest
from witnessed_difference.cochains import (
    FiniteComplex,
    cochain_l1,
    d0,
    d1,
    finite_quotient_l1,
    is_closed,
    solve_potential,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused


def triangle() -> FiniteComplex:
    return FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")), (("a", "b", "c"),))


@pytest.mark.parametrize(
    "args",
    [
        (("a", "a"), (), ()),
        (("a",), (("a", "a"),), ()),
        (("a",), (("a", "b"),), ()),
        (("a", "b"), (("a", "b"), ("b", "a")), ()),
        (("a", "b", "c"), (("a", "b"),), (("a", "a", "b"),)),
        (("a", "b", "c"), (("a", "b"),), (("a", "b", "d"),)),
        (("a", "b", "c"), (("a", "b"), ("b", "c")), (("a", "b", "c"),)),
    ],
)
def test_complex_validation(args) -> None:
    with pytest.raises(ValueError):
        FiniteComplex(*args)


def test_d0_d1_and_reverse_orientation() -> None:
    complex_ = triangle()
    gradient = d0(complex_, {"a": 0, "b": "2", "c": Fraction(5, 2)})
    assert gradient == {
        ("a", "b"): Fraction(2),
        ("b", "c"): Fraction(1, 2),
        ("a", "c"): Fraction(5, 2),
    }
    assert d1(complex_, gradient) == {("a", "b", "c"): 0}
    reversed_values = {(b, a): -value for (a, b), value in gradient.items()}
    assert d1(complex_, reversed_values) == {("a", "b", "c"): 0}
    assert is_closed(complex_, gradient)
    assert cochain_l1(complex_, gradient) == 5


def test_d0_and_cochain_domain_validation() -> None:
    complex_ = triangle()
    with pytest.raises(ValueError, match="every vertex"):
        d0(complex_, {"a": 0})
    with pytest.raises(ValueError, match="every admitted edge"):
        d1(complex_, {("a", "b"): 1})
    with pytest.raises(ValueError, match="every admitted edge"):
        d1(complex_, {("a", "b"): 1, ("b", "c"): 1, ("x", "y"): 1})
    with pytest.raises(ValueError, match="one orientation"):
        d1(complex_, {("a", "b"): 1, ("b", "a"): 999, ("b", "c"): 1})


def test_solve_potential_on_tree_and_disconnected_carrier() -> None:
    complex_ = FiniteComplex(("a", "b", "isolated"), (("a", "b"),))
    result = solve_potential(complex_, {("a", "b"): 3})
    assert isinstance(result, Accepted)
    assert result.value == {"a": 0, "b": 3, "isolated": 0}


def test_cycle_counter_witness_refuses_nonexact_cochain() -> None:
    complex_ = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")))
    result = solve_potential(complex_, {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 3})
    assert isinstance(result, Refused)
    assert result.code is RefusalCode.NOT_EXACT
    assert "cycle inconsistency" in result.detail


def test_finite_quotient_l1_requires_explicit_candidates_and_tie_breaks() -> None:
    complex_ = FiniteComplex(("a", "b"), (("a", "b"),))
    empty = finite_quotient_l1(complex_, {("a", "b"): 2}, ())
    assert isinstance(empty, Refused)
    assert empty.code is RefusalCode.BUDGET_REQUIRED
    candidates = (
        {"a": 0, "b": 0},
        {"a": 0, "b": 2},
        {"a": 1, "b": 3},
    )
    result = finite_quotient_l1(complex_, {("a", "b"): 2}, candidates)
    assert isinstance(result, Accepted)
    assert result.value == (0, {"a": Fraction(0), "b": Fraction(2)})


def test_nonclosed_triangle_is_detected() -> None:
    assert not is_closed(triangle(), {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 0})
# Executable finite evidence; AuthorityEffect: None.
