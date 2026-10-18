from __future__ import annotations

from dataclasses import replace

import pytest

from omega_engine_operations.domain.rop.result import Err, Ok
from omega_engine.kernel.presentation_difference import (
    DemandV1,
    ExtensionEffect,
    PresentationV1,
    QuestionV1,
    active_obstruction,
    derived_question,
    evaluate_extension,
    presentation_replays,
    question_is_derived_from_parent,
)


def _parent() -> PresentationV1:
    return PresentationV1(
        points=("a", "b", "c"),
        questions=(QuestionV1("q:root", ("0", "0", "1")),),
    )


def _demand(**changes: object) -> DemandV1:
    base = DemandV1("a", "b", retained=True, protected=True)
    return replace(base, **changes)


def test_profile_equality_is_the_zero_relation() -> None:
    parent = _parent()
    assert parent.zero_related("a", "b")
    assert not parent.zero_related("a", "c")
    assert parent.partition() == (("a", "b"), ("c",))


@pytest.mark.parametrize(
    ("retained", "protected"),
    ((False, False), (False, True), (True, False)),
)
def test_retention_and_protection_are_independent(
    retained: bool, protected: bool
) -> None:
    assert active_obstruction(
        _parent(), _demand(retained=retained, protected=protected)
    ) is None


def test_retained_protected_missed_pair_is_active() -> None:
    obstruction = active_obstruction(_parent(), _demand())
    assert obstruction is not None
    assert obstruction.pair == ("a", "b")
    assert obstruction.shared_profile == ("0",)
    assert obstruction.authority_effect == "None"


def test_derived_replay_question_cannot_split_old_class() -> None:
    parent = _parent()
    replay = derived_question(
        parent,
        "q:replay",
        ((("0",), "digest-0"), (("1",), "digest-1")),
    )
    assert question_is_derived_from_parent(parent, replay)
    child = PresentationV1(parent.points, parent.questions + (replay,))
    result = evaluate_extension(parent, child, _demand())
    assert isinstance(result, Ok)
    assert result.value.effect is ExtensionEffect.INEFFECTIVE
    assert not result.value.accepted
    assert result.value.derived_new_question_ids == ("q:replay",)


def test_genuine_separator_is_a_strict_structural_split() -> None:
    parent = _parent()
    separator = QuestionV1("q:separator", ("left", "right", "right"))
    assert not question_is_derived_from_parent(parent, separator)
    child = PresentationV1(parent.points, parent.questions + (separator,))
    result = evaluate_extension(parent, child, _demand())
    assert isinstance(result, Ok)
    assert result.value.accepted
    assert result.value.effect is ExtensionEffect.RESOLVED
    assert result.value.class_count_before == 2
    assert result.value.class_count_after == 3


def test_equal_cost_nonunique_separators_are_both_preserved() -> None:
    parent = _parent()
    left = PresentationV1(
        parent.points,
        parent.questions + (QuestionV1("q:left", ("1", "0", "0")),),
    )
    right = PresentationV1(
        parent.points,
        parent.questions + (QuestionV1("q:right", ("0", "1", "0")),),
    )
    left_result = evaluate_extension(parent, left, _demand())
    right_result = evaluate_extension(parent, right, _demand())
    assert isinstance(left_result, Ok) and left_result.value.accepted
    assert isinstance(right_result, Ok) and right_result.value.accepted
    assert left.presentation_id != right.presentation_id


def test_reordered_old_questions_are_not_preserved() -> None:
    parent = PresentationV1(
        ("a", "b", "c"),
        (
            QuestionV1("q:one", ("0", "0", "1")),
            QuestionV1("q:two", ("x", "x", "y")),
        ),
    )
    child = PresentationV1(
        parent.points,
        (
            parent.questions[1],
            parent.questions[0],
            QuestionV1("q:separator", ("0", "1", "1")),
        ),
    )
    result = evaluate_extension(parent, child, _demand())
    assert isinstance(result, Ok)
    assert not result.value.old_questions_preserved
    assert not result.value.accepted


def test_carrier_change_is_a_typed_refusal() -> None:
    parent = _parent()
    child = PresentationV1(
        ("a", "b", "c", "d"),
        (QuestionV1("q:root", ("0", "0", "1", "1")),),
    )
    result = evaluate_extension(parent, child, _demand())
    assert isinstance(result, Err)
    assert result.error.code == "CARRIER_CHANGE_UNLICENSED"


def test_nonactive_demand_is_a_typed_refusal() -> None:
    parent = _parent()
    child = PresentationV1(
        parent.points,
        parent.questions + (QuestionV1("q:separator", ("0", "1", "1")),),
    )
    result = evaluate_extension(parent, child, _demand(protected=False))
    assert isinstance(result, Err)
    assert result.error.code == "NO_ACTIVE_OBSTRUCTION"


def test_mutated_nested_container_fails_closed() -> None:
    parent = _parent()
    object.__setattr__(parent.questions[0], "answers", ["0", "0", "1"])
    assert not presentation_replays(parent)
    result = evaluate_extension(parent, parent, _demand())
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_PRESENTATION"


def test_authority_cannot_be_minted_by_normal_construction() -> None:
    with pytest.raises(ValueError, match="AuthorityEffect"):
        PresentationV1(("a",), (), authority_effect="Minted")
    with pytest.raises(ValueError, match="AuthorityEffect"):
        DemandV1("a", "b", True, True, authority_effect="Minted")


def test_question_shape_and_domain_are_checked() -> None:
    with pytest.raises(ValueError, match="answer every carrier point"):
        PresentationV1(("a", "b"), (QuestionV1("q:short", ("0",)),))
    with pytest.raises(ValueError, match="unique"):
        PresentationV1(("a", "a"), ())


def test_timestamp_free_content_ids_are_stable() -> None:
    first = _parent()
    second = _parent()
    assert first.presentation_id == second.presentation_id
