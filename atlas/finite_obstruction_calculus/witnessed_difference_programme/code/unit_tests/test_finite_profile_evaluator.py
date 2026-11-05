"""Finite CH20 model checks; no semantic adequacy claim."""

from itertools import product

import pytest
from finite_profile_evaluator import (
    Evidence,
    Profile,
    ProfileTransport,
    Status,
    evaluate,
    status_guards,
    verify_evidence,
)


def test_exhaustive_guards_with_forged_and_conflicting_evidence():
    for truth, admitted, refused, budget in product((False, True), (False, True), (False, True), range(3)):
        if refused and not admitted:
            continue
        profile = Profile((("q", truth),), frozenset({"q"} if admitted else ()),
                          frozenset({"q"} if refused else ()), budget)
        for values in ((), (False,), (True,), (False, True), (True, False)):
            candidates = tuple(Evidence("q", value) for value in values)
            guards = status_guards(profile, "q", candidates)
            assert sum(guards) == 1
            result = evaluate(profile, "q", candidates)
            if result is Status.PROVED:
                assert truth is True
            if result is Status.REFUTED:
                assert truth is False
            assert verify_evidence(profile, Evidence("q", not truth)) is False


def test_evidence_replay_budget_and_query_binding():
    profile = Profile((("q", True), ("r", True)), frozenset({"q", "r"}), budget=1)
    assert evaluate(profile, "q", (Evidence("r", True), Evidence("q", True))) is Status.UNDETERMINED
    assert evaluate(profile, "q", (Evidence("q", True),)) is Status.PROVED
    with pytest.raises(ValueError):
        evaluate(profile, "untyped")
    with pytest.raises(TypeError):
        evaluate(profile, "q", [Evidence("q", True)])


def test_transport_replays_evidence_but_does_not_promote_policy_status():
    source = Profile((("q", True),), frozenset({"q"}))
    target = Profile((("encoded", True),), frozenset({"encoded"}), frozenset({"encoded"}))
    adapter = ProfileTransport(source, target, (("q", "encoded"),))
    transported = adapter.transport_evidence(Evidence("q", True))
    assert verify_evidence(target, transported)
    assert evaluate(source, "q", (Evidence("q", True),)) is Status.PROVED
    assert evaluate(target, "encoded", (transported,)) is Status.REFUSED
    with pytest.raises(ValueError):
        adapter.transport_evidence(Evidence("q", False))
    with pytest.raises(ValueError):
        ProfileTransport(source, Profile((("encoded", False),), frozenset()), (("q", "encoded"),))
    with pytest.raises(ValueError):
        ProfileTransport(source, target, ())


def test_transport_rejects_lossy_and_duplicate_encodings():
    source = Profile((("q", True), ("r", True)), frozenset({"q", "r"}))
    target = Profile((("s", True),), frozenset({"s"}))
    with pytest.raises(ValueError):
        ProfileTransport(source, target, (("q", "s"), ("r", "s")))
    with pytest.raises(ValueError):
        ProfileTransport(source, target, (("q", "s"), ("q", "s")))


def test_strict_boolean_tables_and_defensive_freezing():
    with pytest.raises(TypeError):
        Evidence("q", 1)
    with pytest.raises(TypeError):
        Profile((("q", 1),), frozenset({"q"}))
    with pytest.raises(ValueError):
        Profile((("q", True), ("q", False)), frozenset())
    with pytest.raises(ValueError):
        Profile((("q", True),), frozenset({"unknown"}))
    with pytest.raises(ValueError):
        Profile((("q", True),), frozenset(), frozenset({"q"}))
    with pytest.raises(ValueError):
        Profile((("q", True),), frozenset(), budget=True)
    rows = [["q", True]]
    profile = Profile(rows, {"q"})
    rows[0][1] = False
    assert verify_evidence(profile, Evidence("q", True))
