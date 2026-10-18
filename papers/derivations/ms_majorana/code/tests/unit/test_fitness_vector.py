"""Fitness as an observation with separate dimensions, not a score.

`EPIC-OE-PROMPT-CIV-001` section 6 lists what a `FitnessVectorV1` must not do.
Two of those prohibitions are the substance of this suite, because both are easy
to violate by accident and invisible afterwards:

> [it must not] collapse inconclusive results into failures or passes; or hide
> dimension tradeoffs behind a single undocumented scalar.

**Inconclusive is a third value.** A dimension that could not be evaluated did
not fail. Folding them together loses the difference between "this candidate is
worse" and "we did not find out", and the loss is invisible downstream because
both arrive as a number that is not a pass.

**A scalar needs its formula frozen first.** "If a scalar is needed for a
preregistered experiment, its formula, units, weights, tie rule, and sensitivity
analysis are frozen before outcomes are observed."

The strongest test here is one that asserts an *absence*: there is no
`pass_rate()` method. A ratio must decide what to do with `INCONCLUSIVE` and
`MISSING`, and whatever it decides is the collapse the epic forbids -- silently,
because the caller sees only a number. The API therefore does not offer one.
"""

from __future__ import annotations

import pytest

from omega_engine.crates.prompt_civilization.domain.fitness_vector_v1 import (
    COMPARISON_BINDINGS,
    DIMENSION_OUTCOMES,
    PREREGISTRATION_PARTS,
    FitnessDimensionV1,
    FitnessError,
    FitnessVectorV1,
    ScalarPreregistrationV1,
)


def digest(character: str) -> str:
    return "sha256:" + character * 64


def dimension(name: str = "task_success", outcome: str = "PASS", **overrides):
    fields = {
        "name": name,
        "outcome": outcome,
        "observed": 8,
        "total": 10,
        "uncertainty": "wilson 95% [0.49, 0.94]",
    }
    if outcome == "MISSING":
        fields["observed"] = None
        fields["total"] = None
    fields.update(overrides)
    return FitnessDimensionV1(**fields)


def make_preregistration(**overrides) -> ScalarPreregistrationV1:
    fields = {
        "formula": "w1*success + w2*novelty",
        "units": "dimensionless",
        "weights": (("task_success", "0.7"), ("novelty", "0.3")),
        "tie_rule": "lower candidate digest wins",
        "sensitivity": "+/-0.05 on w1 does not reorder the top three",
    }
    fields.update(overrides)
    return ScalarPreregistrationV1(**fields)


def make_vector(**overrides) -> FitnessVectorV1:
    fields = {
        "manifest_digest": digest("a"),
        "candidate_digest": digest("b"),
        "checker_id": "checker_one",
        "holdout_digest": digest("c"),
        "dimensions": (dimension(),),
    }
    fields.update(overrides)
    return FitnessVectorV1(**fields)




def test_the_outcome_vocabulary_is_four_valued():
    assert DIMENSION_OUTCOMES == {"PASS", "FAIL", "INCONCLUSIVE", "MISSING"}


def test_there_is_no_pass_rate_method():
    """The strongest assertion in this suite, and it asserts an absence.

    Any ratio has to choose how to treat `INCONCLUSIVE` and `MISSING`, and
    whatever it chooses is the collapse the epic forbids -- invisibly, because
    the caller sees a number and not the choice.
    """
    vector = make_vector()
    assert not hasattr(vector, "pass_rate")
    assert not hasattr(vector, "score")
    assert not hasattr(vector, "ratio")


def test_every_outcome_is_tallied_separately():
    vector = make_vector(
        dimensions=(
            dimension("task_success", "PASS"),
            dimension("specificity", "FAIL"),
            dimension("novelty", "INCONCLUSIVE"),
            dimension("budget", "MISSING"),
        )
    )
    assert vector.outcome_tally() == {
        "PASS": 1,
        "FAIL": 1,
        "INCONCLUSIVE": 1,
        "MISSING": 1,
    }


def test_an_inconclusive_dimension_is_not_counted_as_a_failure():
    vector = make_vector(
        dimensions=(dimension("task_success", "PASS"), dimension("novelty", "INCONCLUSIVE"))
    )
    tally = vector.outcome_tally()
    assert tally["FAIL"] == 0
    assert tally["INCONCLUSIVE"] == 1


def test_a_missing_dimension_is_not_counted_as_a_failure():
    vector = make_vector(
        dimensions=(dimension("task_success", "PASS"), dimension("budget", "MISSING"))
    )
    tally = vector.outcome_tally()
    assert tally["FAIL"] == 0
    assert tally["MISSING"] == 1


def test_conclusiveness_is_reported_not_assumed():
    decided = make_vector(
        dimensions=(dimension("a", "PASS"), dimension("b", "FAIL"))
    )
    assert decided.is_conclusive() is True
    undecided = make_vector(
        dimensions=(dimension("a", "PASS"), dimension("b", "INCONCLUSIVE"))
    )
    assert undecided.is_conclusive() is False


def test_undecided_dimensions_are_named_not_counted():
    vector = make_vector(
        dimensions=(
            dimension("a", "PASS"),
            dimension("b", "INCONCLUSIVE"),
            dimension("c", "MISSING"),
        )
    )
    assert vector.undecided_dimensions() == ("b", "c")


def test_a_missing_dimension_may_not_carry_counts():
    """Counts on a MISSING dimension describe an evaluation that did not happen."""
    with pytest.raises(FitnessError) as excinfo:
        FitnessDimensionV1(
            name="budget", outcome="MISSING", observed=3, total=10, uncertainty="u"
        )
    assert excinfo.value.code == "MISSING_WITH_COUNTS"


def test_an_evaluated_dimension_must_carry_counts():
    with pytest.raises(FitnessError, match="BAD_COUNTS"):
        FitnessDimensionV1(
            name="task", outcome="PASS", observed=None, total=None, uncertainty="u"
        )


def test_every_dimension_states_uncertainty_including_undecided_ones():
    """"We could not evaluate this" is itself a stated uncertainty."""
    with pytest.raises(FitnessError) as excinfo:
        FitnessDimensionV1(
            name="novelty",
            outcome="INCONCLUSIVE",
            observed=3,
            total=10,
            uncertainty="   ",
        )
    assert excinfo.value.code == "UNCERTAINTY_ABSENT"


def test_an_outcome_outside_the_vocabulary_is_refused():
    with pytest.raises(FitnessError, match="BAD_OUTCOME"):
        dimension(outcome="PROBABLY_FINE")


def test_observed_may_not_exceed_total():
    with pytest.raises(FitnessError, match="BAD_COUNTS"):
        dimension(observed=11, total=10)




def test_a_scalar_without_a_preregistration_is_refused():
    """The epic's second prohibition, directly."""
    with pytest.raises(FitnessError) as excinfo:
        make_vector(scalar="0.72")
    assert excinfo.value.code == "SCALAR_NOT_PREREGISTERED"
    assert "hides dimension tradeoffs" in str(excinfo.value)


def test_a_scalar_with_a_preregistration_is_admitted():
    """The permitted case. Without it the refusal above proves nothing."""
    prereg = make_preregistration()
    vector = make_vector(
        scalar="0.72", preregistration_digest=prereg.preregistration_digest
    )
    assert vector.scalar == "0.72"


def test_a_vector_without_a_scalar_needs_no_preregistration():
    """The common case must stay cheap; most vectors carry no scalar at all."""
    assert make_vector().scalar is None


@pytest.mark.parametrize("part", ["formula", "units", "tie_rule", "sensitivity"])
def test_a_preregistration_missing_any_part_is_refused(part):
    with pytest.raises(FitnessError) as excinfo:
        make_preregistration(**{part: "   "})
    assert excinfo.value.code == "PREREGISTRATION_INCOMPLETE"


def test_a_preregistration_needs_weights():
    with pytest.raises(FitnessError, match="PREREGISTRATION_INCOMPLETE"):
        make_preregistration(weights=())


def test_a_dimension_weighted_twice_is_refused():
    with pytest.raises(FitnessError, match="weighted twice"):
        make_preregistration(weights=(("a", "0.5"), ("a", "0.5")))


def test_the_preregistration_parts_are_the_five_the_epic_names():
    assert PREREGISTRATION_PARTS == (
        "formula",
        "units",
        "weights",
        "tie_rule",
        "sensitivity",
    )


def test_a_preregistration_is_content_addressed():
    a = make_preregistration()
    b = make_preregistration()
    assert a.preregistration_digest == b.preregistration_digest
    c = make_preregistration(tie_rule="higher digest wins")
    assert c.preregistration_digest != a.preregistration_digest


def test_a_tampered_preregistration_digest_is_refused():
    with pytest.raises(FitnessError, match="does not match canonical content"):
        make_preregistration(preregistration_digest=digest("f"))




def test_two_vectors_measured_the_same_way_are_comparable():
    assert make_vector().comparable_with(make_vector()) is True


@pytest.mark.parametrize("binding", ["checker_id", "holdout_digest"])
def test_changing_a_comparison_binding_makes_vectors_incomparable(binding):
    """"Changing a fitness formula, weight, seed, checker, holdout ..."."""
    other = {"checker_id": "checker_two", "holdout_digest": digest("e")}[binding]
    assert make_vector().comparable_with(make_vector(**{binding: other})) is False


def test_changing_the_preregistration_makes_vectors_incomparable():
    a = make_preregistration()
    b = make_preregistration(formula="different formula")
    left = make_vector(scalar="0.7", preregistration_digest=a.preregistration_digest)
    right = make_vector(scalar="0.7", preregistration_digest=b.preregistration_digest)
    assert left.comparable_with(right) is False


def test_the_comparison_bindings_are_declared():
    assert COMPARISON_BINDINGS == (
        "preregistration_digest",
        "checker_id",
        "holdout_digest",
    )


def test_comparing_with_a_non_vector_is_refused():
    with pytest.raises(FitnessError, match="BAD_COMPARISON"):
        make_vector().comparable_with("not a vector")




def test_a_fitness_vector_has_no_status_field():
    """"Fitness changes review ordering only and cannot change lifecycle status."

    Enforced by absence: there is nowhere to put one.
    """
    vector = make_vector()
    assert not hasattr(vector, "status")
    assert not hasattr(vector, "population_status")
    assert "status" not in vector.to_dict()


def test_authority_effect_is_none_and_anything_else_is_refused():
    assert make_vector().authority_effect == "None"
    with pytest.raises(FitnessError, match="authority_effect"):
        make_vector(authority_effect="ACTION_LICENSE")


def test_a_vector_with_no_dimensions_is_refused():
    with pytest.raises(FitnessError, match="NO_DIMENSIONS"):
        make_vector(dimensions=())


def test_a_duplicate_dimension_name_is_refused():
    with pytest.raises(FitnessError, match="appears twice"):
        make_vector(dimensions=(dimension("a"), dimension("a")))


def test_vectors_are_content_addressed():
    assert make_vector().vector_id == make_vector().vector_id
    assert make_vector().vector_id != make_vector(checker_id="other").vector_id
