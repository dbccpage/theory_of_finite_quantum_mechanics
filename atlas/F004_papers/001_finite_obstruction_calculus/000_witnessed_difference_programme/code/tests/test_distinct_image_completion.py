"""Checker-driven tests for distinct realization and repair images."""

import sys
import pytest
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from observer_completion.distinct_image import (  # noqa: E402
    M,
    analyze,
    annihilator_status,
    check_completion,
    check_shelf,
    inclusion_examples,
    produce_completion,
    produce_shelf,
    quotient_holds,
    raw_holds,
    suite_is_sufficient,
)
from observer_completion.distinct_replay import (  # noqa: E402
    positive_and_negative,
    rejection_suite,
)
from observer_completion.observer_completion import hc, null, vc  # noqa: E402


def _column(*entries):
    return M([[entry] for entry in entries], 1)


def test_three_inclusions_and_joint_gap():
    examples = inclusion_examples()
    proper = examples["R_subset_B"]
    assert proper["R_in_B"] and not proper["B_in_R"]
    assert proper["raw_minimum"] == 1
    assert proper["quotient_minimum"] == 0
    reverse = examples["B_subset_R"]
    assert reverse["B_in_R"] and not reverse["R_in_B"]
    assert reverse["joint_minimum"] == 2
    assert reverse["separate_sum"] == 3
    assert reverse["joint_minimum"] != reverse["separate_sum"]
    neither = examples["neither_inclusion"]
    assert not neither["R_in_B"] and not neither["B_in_R"]
    assert neither["joint_minimum"] < neither["separate_sum"]


def test_checker_replays_raw_quotient_and_joint_criteria():
    source = hc(_column(1, 0, 0), _column(0, 1, 0))
    repair = _column(1, 0, 0)
    observer = M([[0, 0, 1]], 3)
    facts = analyze(source, repair, observer)
    both = produce_completion(source, repair, observer, "both")
    accepted = check_completion(source, repair, observer, both)
    rows = M.decode(both["E"])
    kernel = null(vc(observer, rows))
    hidden = analyze(source, repair, vc(observer, rows))
    assert hidden["RK"].c == 0
    assert raw_holds(source, observer, rows)
    assert quotient_holds(repair, observer, rows)
    assert kernel.c == 0 or rank_inside_repair(repair, kernel)
    assert accepted["minimum"] == facts["joint_minimum"]
    assert facts["joint_minimum"] != facts["separate_sum"]
    quotient = produce_completion(source, repair, observer, "quotient")
    check_completion(source, repair, observer, quotient)
    assert quotient_holds(repair, observer, M.decode(quotient["E"]))
    assert not raw_holds(source, observer, M.decode(quotient["E"]))


def rank_inside_repair(repair, kernel):
    from observer_completion.observer_completion import rank
    from observer_completion.distinct_image import image_basis
    algebraic = image_basis(repair)
    return kernel.c == 0 or rank(hc(algebraic, kernel)) == algebraic.c


def test_lower_certificate_must_be_an_obstruction_basis():
    source = hc(_column(1, 0, 0), _column(0, 1, 0))
    repair = _column(1, 0, 0)
    observer = M([[0, 0, 1]], 3)
    both = produce_completion(source, repair, observer, "both")
    assert check_completion(source, repair, observer, both)["accepted"] is True
    forged = dict(both)
    forged["lower_columns"] = hc(_column(0, 1, 0), _column(0, 0, 1)).encode()
    try:
        check_completion(source, repair, observer, forged)
    except ValueError as error:
        assert str(error) == "lower certificate"
    else:
        raise AssertionError("columns outside ker Q were accepted")
    quotient_only = produce_completion(
        _column(1, 0, 0),
        hc(_column(1, 0, 0), _column(0, 1, 0)),
        observer,
        "quotient",
    )
    assert quotient_only["minimum"] == 0
    assert check_completion(
        _column(1, 0, 0),
        hc(_column(1, 0, 0), _column(0, 1, 0)),
        observer,
        quotient_only,
    )["accepted"] is True


def test_full_repair_space_needs_an_admissible_operation():
    source = _column(1, 0)
    repair = hc(_column(1, 0), _column(0, 1))
    observer = M([[1, 0]], 2)
    witness = produce_completion(source, repair, observer, "quotient")
    witness["solves_original"] = True
    try:
        check_completion(source, repair, observer, witness)
    except ValueError as error:
        assert str(error) == "observation_completion_does_not_certify_repairs"
    else:
        raise AssertionError("B=V was accepted without an operation")
    witness["admissible_operation"] = {
        "map": source.encode(),
        "preimage": M([[1]], 1).encode(),
        "repair": _column(1, 0).encode(),
        "defect": _column(1, 0).encode(),
    }
    with pytest.raises(ValueError, match="observation_completion_does_not_certify_repairs"):
        check_completion(source, repair, observer, witness)


def test_annihilator_menu_can_be_impossible():
    examples_source = _column(1, 0, 0)
    repair = hc(_column(1, 0, 0), _column(0, 1, 0))
    observer = M([[0, 0, 1]], 3)
    blocked = annihilator_status(examples_source, repair, observer, "both")
    assert blocked["feasible"] is False
    assert blocked["reason"] == "annihilator_menu_impossible"


def test_shelf_matches_independent_enumeration_and_rejects_costlier():
    source = hc(_column(1, 0, 0), _column(0, 1, 0))
    repair = _column(1, 0, 0)
    observer = M([[0, 0, 1]], 3)
    shelf = (
        M([[1, 0, 0]], 3),
        M([[0, 1, 0]], 3),
        M([[1, 1, 0]], 3),
        M([[0, 0, 1]], 3),
    )
    costs = (F(3), F(4), F(5), F(1))
    produced = produce_shelf(source, repair, observer, shelf, costs, "both")
    assert produced["feasible"] is True

    def independent_min():
        best = None
        for size in range(len(shelf) + 1):
            for chosen in combinations(range(len(shelf)), size):
                rows = vc(*[shelf[index] for index in chosen]) if chosen else M([], 3)
                if suite_is_sufficient(source, repair, observer, rows, "both"):
                    cost = sum((costs[index] for index in chosen), F(0))
                    if best is None or cost < best:
                        best = cost
        return best

    assert produced["cost"] == independent_min()
    assert check_shelf(
        source, repair, observer, shelf, costs, "both", produced
    )["accepted"] is True
    costlier = dict(produced)
    # Rows 0 and 2 separate the joint defect, at a strictly higher cost than the optimum.
    costlier["indices"] = (0, 2)
    costlier["cost"] = costs[0] + costs[2]
    costlier["E"] = vc(shelf[0], shelf[2]).encode()
    try:
        check_shelf(source, repair, observer, shelf, costs, "both", costlier)
    except ValueError as error:
        assert "not minimum" in str(error) or "insufficient" in str(error)
    else:
        raise AssertionError("costlier suite accepted")


def test_shelf_refuses_bool_float_and_missing_feasible():
    source = hc(_column(1, 0, 0), _column(0, 1, 0))
    repair = _column(1, 0, 0)
    observer = M([[0, 0, 1]], 3)
    shelf = (M([[1, 0, 0]], 3),)
    try:
        produce_shelf(source, repair, observer, shelf, (True,), "both")
    except ValueError as error:
        assert str(error) == "positive costs"
    else:
        raise AssertionError("boolean cost accepted")
    try:
        produce_shelf(source, repair, observer, shelf, (1.5,), "both")
    except ValueError as error:
        assert str(error) == "positive costs"
    else:
        raise AssertionError("float cost accepted")
    costs = (F(3), F(4), F(5), F(1))
    full_shelf = (
        M([[1, 0, 0]], 3),
        M([[0, 1, 0]], 3),
        M([[1, 1, 0]], 3),
        M([[0, 0, 1]], 3),
    )
    produced = produce_shelf(source, repair, observer, full_shelf, costs, "both")
    missing = dict(produced)
    del missing["feasible"]
    try:
        check_shelf(source, repair, observer, full_shelf, costs, "both", missing)
    except ValueError as error:
        assert str(error) == "feasible flag"
    else:
        raise AssertionError("missing feasible flag accepted")


def test_rejection_replay_reasons_are_stable():
    first = [(item["name"], item["reason"]) for item in rejection_suite()]
    second = [(item["name"], item["reason"]) for item in rejection_suite()]
    assert first == second
    assert all(name == reason for name, reason in first)
    # Numbered obligation 3 asks for quotient-without-raw and the converse, so
    # those two directions are separate witnesses inside the fourteen obligations.
    required = {
        "r_and_b_conflated",
        "blind_realizable_defect",
        "quotient_without_raw",
        "raw_without_quotient",
        "optima_incorrectly_added",
        "observation_completion_does_not_certify_repairs",
        "wrong_coefficient_field",
        "toric_kernel_identified_with_s",
        "rank_defect_as_low_weight_collision",
        "t0_requires_full_detector_basis",
        "current_answer_loses_future_operation",
        "false_adaptive_lower_bound",
        "finite_m_promoted_to_all_m",
        "lr_upper_bound_as_error_floor",
        "wrong_task_or_stale_witness",
    }
    assert {name for name, _reason in first} == required
    certificates = positive_and_negative()
    assert certificates["positive"]["accepted"] is True
    assert certificates["negative_reason"] != "accepted"
