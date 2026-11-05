"""Small exhaustive countermodels for decision descent and occurrence replay."""

from dataclasses import replace
from itertools import product

import pytest
from witnessed_difference.finite_observer_adapter_completeness import DescentError
from witnessed_difference.proposal_admission_bridge import (
    DecisionTable,
    DeclaredTransitions,
    decision_decoder,
    joint_commit_table,
    replay,
    verify_replay,
)


def test_exhaustive_decoder_iff_fiber_constancy():
    for n in range(4):
        for reports in product(range(2), repeat=n):
            for decisions in product((None, False, True), repeat=n):
                table = DecisionTable(reports, decisions)
                collisions = [
                    (i, j)
                    for i in range(n)
                    for j in range(i + 1, n)
                    if reports[i] == reports[j] and decisions[i] != decisions[j]
                ]
                if collisions:
                    with pytest.raises(DescentError) as caught:
                        decision_decoder(table)
                    i, j = caught.value.left, caught.value.right
                    assert reports[i] == reports[j] and decisions[i] != decisions[j]
                else:
                    decoder = decision_decoder(table)
                    assert tuple(decoder.decode(r) for r in reports) == decisions
                    with pytest.raises(ValueError):
                        decoder.decode(2)


def test_exhaustive_joint_commit_and_evaluation_only_failure():
    values = (None, False, True)
    for evaluation in product(values, repeat=2):
        for permission in product(values, repeat=2):
            table = joint_commit_table(evaluation, permission)
            decoder = decision_decoder(table)
            assert tuple(decoder.decode(r) for r in table.reports) == table.decisions
    assert joint_commit_table((True, True), (False, True)).decisions == (False, True)
    with pytest.raises(DescentError):
        decision_decoder(DecisionTable((7, 7), (False, True)))
    # Same permission cannot reconstruct evaluation either.
    with pytest.raises(DescentError):
        decision_decoder(DecisionTable((0, 0), (False, True)))


def test_role_labels_and_process_count_do_not_determine_permission():
    for labels in ((0, 0), (1, 1)):  # fixed role label or fixed physical process count
        with pytest.raises(DescentError):
            decision_decoder(DecisionTable(labels, (False, True)))


def test_order_and_occurrence_count_are_independent_of_final_state():
    d = DeclaredTransitions(2, 2, "set-bit", "declared-domain", (0, 1, 0, 1))
    left, right = replay(d, 0, (0, 1)), replay(d, 0, (1, 0))
    assert sorted(left.events) == sorted(right.events) and left.final != right.final
    with pytest.raises(DescentError):
        verify_replay(d, 0, right.events, left)
    with pytest.raises(DescentError):
        verify_replay(d, 1, left.events, left)
    with pytest.raises(DescentError):
        verify_replay(replace(d, table=(1, 0, 1, 0)), 0, left.events, left)
    with pytest.raises(ValueError):
        replace(left, final=True)
    empty, repeated = replay(d, 0, ()), replay(d, 0, (0, 0))
    assert empty.final == repeated.final and len(empty.occurrences) != len(repeated.occurrences)


def test_exhaustive_replay_and_forgery_rejection():
    for table in product(range(2), repeat=4):
        d = DeclaredTransitions(2, 2, "rule", "scope", table)
        for initial in range(2):
            for n in range(4):
                for events in product(range(2), repeat=n):
                    receipt = replay(d, initial, events)
                    verify_replay(d, initial, events, receipt)
                    false = replace(receipt, final=1 - receipt.final)
                    # A freshly recomputed hash of false has no bearing on verification.
                    hash(false)
                    with pytest.raises(DescentError):
                        verify_replay(d, initial, events, false)
                    for changed in (replace(d, rule="other"), replace(d, scope="other")):
                        with pytest.raises(DescentError):
                            verify_replay(changed, initial, events, receipt)
                    if receipt.occurrences:
                        bad = replace(receipt, occurrences=())
                        with pytest.raises(DescentError):
                            verify_replay(d, initial, events, bad)


def test_validation_preserves_false_and_undefined():
    assert decision_decoder(DecisionTable((0, 1), (False, None))).decisions == (False, None)
    with pytest.raises(ValueError):
        DecisionTable((0,), (0,))
    with pytest.raises(ValueError):
        DecisionTable((True,), (False,))
    with pytest.raises(ValueError):
        joint_commit_table((1,), (True,))
    with pytest.raises(ValueError):
        DeclaredTransitions(2, 1, "r", "s", (False, 0))
    d = DeclaredTransitions(2, 1, "r", "s", (None, 0))
    with pytest.raises(ValueError):
        replay(d, 0, (0,))
    with pytest.raises(ValueError):
        replay(d, 0, (True,))


def test_always_equal_object_cannot_impersonate_receipt():
    class AlwaysEqual:
        def __eq__(self, other):
            return True

        def __ne__(self, other):
            return False

    declaration = DeclaredTransitions(2, 1, "r", "s", (0, 1))
    with pytest.raises(ValueError, match="invalid receipt"):
        verify_replay(declaration, 0, (0,), AlwaysEqual())
    with pytest.raises(ValueError, match="invalid declaration"):
        replay(AlwaysEqual(), 0, ())


def test_frozen_bypass_is_revalidated_including_nested_records():
    declaration = DeclaredTransitions(2, 1, "r", "s", (0, 1))
    for attribute, value in (("initial", False), ("events", (False,)), ("final", False)):
        receipt = replay(declaration, 0, (0,))
        object.__setattr__(receipt, attribute, value)
        with pytest.raises(ValueError):
            verify_replay(declaration, 0, (0,), receipt)
    receipt = replay(declaration, 0, (0,))
    object.__setattr__(receipt.occurrences[0], "event", False)
    with pytest.raises(ValueError, match="invalid occurrence"):
        verify_replay(declaration, 0, (0,), receipt)
    nested = DeclaredTransitions(2, 1, "r", "s", (0, 1))
    receipt = replay(nested, 0, (0,))
    object.__setattr__(nested, "table", (False, 1))
    with pytest.raises(ValueError, match="invalid target state"):
        verify_replay(declaration, 0, (0,), receipt)
    with pytest.raises(ValueError, match="invalid target state"):
        replay(nested, 0, ())
    table = DecisionTable((0,), (False,))
    object.__setattr__(table, "decisions", (0,))
    with pytest.raises(ValueError, match="decisions must be bool"):
        decision_decoder(table)
