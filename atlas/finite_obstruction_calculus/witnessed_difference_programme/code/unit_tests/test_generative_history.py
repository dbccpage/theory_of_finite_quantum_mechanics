from __future__ import annotations

import copy

import pytest

from generative_history.model import (
    Edge,
    History,
    HistoryError,
    Question,
    Signature,
    bounded_context_counterexample,
    compose,
    edge_counts,
    enumerate_histories,
    expected_endpoint_boundary,
    vertex_boundary,
)
from generative_history.replay import check, produce, reference_problem


def signature() -> Signature:
    return Signature(
        ("x", "y", "z"),
        (
            Edge("xy", "x", "y"),
            Edge("yz", "y", "z"),
            Edge("xz", "x", "z"),
            Edge("loop-a", "z", "z"),
            Edge("loop-b", "z", "z"),
        ),
    )


def test_typed_history_and_composition() -> None:
    sig = signature()
    xy = History("x", "y", ("xy",))
    yz = History("y", "z", ("yz",))
    assert compose(sig, xy, yz) == History("x", "z", ("xy", "yz"))
    with pytest.raises(HistoryError, match="do not compose"):
        compose(sig, yz, xy)
    with pytest.raises(HistoryError, match="expected"):
        History("x", "z", ("yz",)).validate(sig)


def test_context_exposes_equal_current_answers() -> None:
    sig = Signature(
        ("o",),
        (Edge("a", "o", "o"), Edge("b", "o", "o")),
    )
    left = History("o", "o", ())
    right = History("o", "o", ("a",))
    question = Question("exact-b", "o", "o", "exact_word", ("b",))
    assert question.evaluate(left) is False
    assert question.evaluate(right) is False
    witness = bounded_context_counterexample(sig, left, right, (question,), 1)
    assert witness == {
        "question": "exact-b",
        "prefix": [],
        "suffix": ["b"],
        "left_answer": True,
        "right_answer": False,
    }


def test_bounded_search_labels_its_bound() -> None:
    sig = signature()
    histories = enumerate_histories(sig, "x", "z", 2)
    assert History("x", "z", ("xz",)) in histories
    assert History("x", "z", ("xy", "yz")) in histories
    assert all(len(history.edges) <= 2 for history in histories)
    with pytest.raises(HistoryError, match="nonnegative"):
        enumerate_histories(sig, "x", "z", -1)


def test_boundary_telescopes_for_every_small_history() -> None:
    sig = signature()
    for source in sig.objects:
        for target in sig.objects:
            for history in enumerate_histories(sig, source, target, 4):
                assert vertex_boundary(sig, history) == expected_endpoint_boundary(sig, history)


def test_abelianization_forgets_order() -> None:
    left = History("z", "z", ("loop-a", "loop-b"))
    right = History("z", "z", ("loop-b", "loop-a"))
    assert edge_counts(left) == edge_counts(right)
    assert left != right
    exact_left = Question("left-word", "z", "z", "exact_word", left.edges)
    assert exact_left.evaluate(left) is True
    assert exact_left.evaluate(right) is False


def test_replay_binds_and_rechecks_the_problem() -> None:
    problem = reference_problem()
    receipt = produce(problem)
    check(problem, receipt)

    forged = copy.deepcopy(receipt)
    forged["context_counterexample"]["right_answer"] = True
    with pytest.raises(ValueError, match="does not replay"):
        check(problem, forged)

    changed = copy.deepcopy(problem)
    changed["max_context_length"] = 0
    with pytest.raises(ValueError, match="does not replay"):
        check(changed, receipt)


def test_exact_bounds_reject_bool_and_truncated_numbers() -> None:
    history = History("z", "z", ("loop-a",))
    for bad in (True, 1.5, "2"):
        with pytest.raises(HistoryError, match="positive integer"):
            Question("mod", "z", "z", "length_mod", bad).evaluate(history)
    with pytest.raises(HistoryError, match="nonnegative integer"):
        enumerate_histories(signature(), "x", "z", True)  # type: ignore[arg-type]
    problem = reference_problem()
    for bad in (True, 1.5, -1):
        changed = copy.deepcopy(problem)
        changed["max_context_length"] = bad
        with pytest.raises(ValueError, match="nonnegative integer"):
            produce(changed)
