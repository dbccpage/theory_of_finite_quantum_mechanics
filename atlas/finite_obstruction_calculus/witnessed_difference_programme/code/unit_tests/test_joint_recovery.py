"""Exact controls for correlated reports and the finite cost reduction."""

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
from itertools import product

import pytest
from calibrated_recovery import bridge as calibrated
from calibrated_recovery.examples import correlated_enclosure
from finite_observation import solver
from joint_recovery import reference
from joint_recovery.examples import (
    isolated_collision,
    isolated_cost_peak,
    parity_points,
    shared_error,
)
from joint_recovery.reference import Channel, Model, Segment
from joint_recovery.replay import propose_bundle, verify_bundle


def report(model, readings, visible="*"):
    return {
        "model_sha256": reference.model_hash(model),
        "visible": visible,
        "readings": [
            {
                "channel": model.channels[i].name,
                "raw_unit": model.channels[i].raw_unit,
                "value": str(z),
            }
            for i, z in readings
        ],
    }


def costs(model):
    certificate = reference.propose_cost(model)
    assert reference.verify_cost(model, certificate).accepted
    return tuple(certificate["finite_certificate"][kind]["value"] for kind in ("fixed", "adaptive"))


def test_shared_error_recovers_where_the_marginal_enclosure_abstains():
    model = shared_error()
    assert costs(model) == ("2", "2")
    assert len(reference.sample_worlds(model)) == 10
    assert reference.evaluate(model, report(model, [(0, F(0))]), "0").status == "ABSTAIN"
    data = report(model, [(0, F(0)), (1, F(0))])
    assert reference.evaluate(model, data, "0").status == "VERIFIED"
    assert reference.evaluate(model, data, "1").status == "INVALID_PROPOSAL"
    outer = correlated_enclosure()
    outer_report = dict(data, model_sha256=calibrated.model_hash(outer))
    outer_report["readings"] = [
        dict(row, channel=name) for row, name in zip(data["readings"], ("plus", "minus"))
    ]
    assert calibrated.evaluate(outer, outer_report, "0").status == "ABSTAIN"
    outer_cost = calibrated.propose_cost(outer)
    assert outer_cost["finite_certificate"]["adaptive"]["value"] is None


def test_all_readings_need_one_common_parameter_and_one_component():
    model = shared_error()
    assert (
        reference.evaluate(model, report(model, [(0, F(0)), (1, F(1))]), "0").status
        == "INCONSISTENT"
    )
    assert (
        reference.evaluate(model, report(model, [(0, F(0)), (1, F(-2))]), "1").status == "VERIFIED"
    )
    parity = parity_points()
    assert costs(parity) == ("2", "2")
    assert (
        reference.evaluate(parity, report(parity, [(0, F(0)), (1, F(1))]), "1").status == "VERIFIED"
    )
    assert (
        reference.evaluate(parity, report(parity, [(0, F(0)), (1, F(1))]), "0").status
        == "INVALID_PROPOSAL"
    )


def test_identical_candidate_sets_can_have_different_remaining_costs():
    model = isolated_collision()
    for value in (F(0), F(1, 3)):
        result = reference.evaluate(model, report(model, [(0, value)]), "0")
        assert result.status == "ABSTAIN" and result.compatible == ("0", "1")
    ordinary = solver.solve(reference.conditional_instance(model, 0, F(0), "*"))
    singular = solver.solve(reference.conditional_instance(model, 0, F(1, 3), "*"))
    assert ordinary["adaptive"]["value"] == "1"
    assert singular["adaptive"]["value"] is None


@pytest.mark.parametrize("gain,raw", [
    (F(2**256 - 1), F(2)),
    (F(-(2**256 - 1)), F(2)),
    (F(1, 2**256 - 1), F(1, 2)),
    (F(-1, 2**256 - 1), F(1, 2)),
])
def test_calibrated_continuation_preserves_the_raw_report_domain(gain, raw):
    offset = F(1, 2**255 - 19)
    model = Model(
        (Channel("A", "raw", "cal", gain, offset, F(1)),
         Channel("B", "raw", "cal", F(1), F(0), F(1))),
        tuple(Segment(str(x), "*", str(x), "u", raw, raw,
                      (gain, F(1)), (offset, F(x))) for x in (0, 1)),
    )
    value = gain * raw + offset
    assert max(value.numerator.bit_length(), value.denominator.bit_length()) > 256
    assert reference.evaluate(model, report(model, [(0, raw)]), "0").status == "ABSTAIN"
    instance = reference.conditional_instance(model, 0, value, "*")
    certificate = solver.solve(instance)
    assert solver.verify(instance, certificate).accepted
    assert certificate["adaptive"]["value"] == "1"
    for x in (0, 1):
        assert reference.evaluate(
            model, report(model, [(0, raw), (1, raw + x)]), str(x)
        ).status == "VERIFIED"


def test_continuation_rejects_readings_outside_the_raw_report_cap():
    gain = F(1, 2**256 - 1)
    model = Model(
        (Channel("A", "raw", "cal", gain, F(0), F(1)),),
        (Segment("x", "*", "x", "u", F(0), F(0), (F(1),), (F(2),)),),
    )
    assert reference.evaluate(model, report(model, [(0, F(2) / gain)]), "x").status == "INVALID_REPORT"
    with pytest.raises(ValueError, match="rational bit cap"):
        reference.conditional_instance(model, 0, F(2), "*")


@pytest.mark.parametrize("value", [True, 0, 0.0, "0"])
def test_continuation_requires_an_exact_calibrated_fraction(value):
    with pytest.raises(TypeError, match="exact Fraction"):
        reference.conditional_instance(shared_error(), 0, value, "*")


def test_isolated_joint_collision_is_retained_exactly():
    model = isolated_collision()
    assert costs(model) == (None, None)
    worlds = reference.sample_worlds(model)
    assert {x for x, _ in worlds} == {"0", "1"}
    assert all(z == (F(1, 3), F(1, 3)) for _, z in worlds)


def test_free_report_separates_identical_joint_supports_without_queries():
    model = Model(
        (shared_error().channels[0],),
        tuple(Segment(str(x), str(x), str(x), "m", F(0), F(0), (F(1),), (F(0),)) for x in (0, 1)),
    )
    assert costs(model) == ("0", "0")
    for x in ("0", "1"):
        assert reference.evaluate(model, report(model, [], x), x).status == "VERIFIED"
    shared_free_report = replace(
        model, segments=tuple(replace(s, visible="*") for s in model.segments)
    )
    assert costs(shared_free_report) == (None, None)
    empty_shelf = replace(
        model,
        channels=(),
        segments=tuple(replace(s, slopes=(), offsets=()) for s in model.segments),
    )
    assert costs(empty_shelf) == ("0", "0")


def test_critical_point_prevents_a_false_cost_from_endpoint_sampling():
    model = isolated_cost_peak()
    assert costs(model) == ("3", "3")
    # This four-world baseline samples only the two parameter endpoints.
    endpoint_only = solver.Instance(
        ("a", "b", "c", "d"),
        ("*",) * 4,
        ("0", "0", "1", "1"),
        (
            solver.Instrument("A", ("-1", "1", "-1", "1"), F(1)),
            solver.Instrument("B", ("-1", "1", "1", "-1"), F(1)),
            solver.Instrument("C", ("-1", "1", "9", "11"), F(3)),
        ),
    )
    sample_certificate = solver.solve(endpoint_only)
    assert sample_certificate["fixed"]["value"] == "2"
    assert sample_certificate["adaptive"]["value"] == "2"
    ambiguous = reference.evaluate(model, report(model, [(0, F(0)), (1, F(0))]), "0")
    assert ambiguous.status == "ABSTAIN"


def test_free_observation_answer_coarsening_and_empty_shelf():
    model = shared_error()
    free = replace(model, segments=tuple(replace(s, visible=s.answer) for s in model.segments))
    assert costs(free) == ("0", "0")
    assert reference.evaluate(free, report(free, [], "0"), "0").status == "VERIFIED"
    same = replace(model, segments=tuple(replace(s, answer="same") for s in model.segments))
    assert costs(same) == ("0", "0")
    empty = replace(
        model,
        channels=(),
        segments=tuple(replace(s, slopes=(), offsets=()) for s in model.segments),
    )
    assert costs(empty) == (None, None)


@pytest.mark.parametrize("scale,shift", [(F(100), F(7)), (F(-3, 2), F(-4))])
def test_affine_coordinate_change_preserves_joint_answers_and_costs(scale, shift):
    model = shared_error()
    changed = Model(
        tuple(
            replace(
                c,
                raw_gain=scale * c.raw_gain,
                raw_offset=scale * c.raw_offset + shift,
                unit="converted",
            )
            for c in model.channels
        ),
        tuple(
            replace(
                s,
                slopes=tuple(scale * a for a in s.slopes),
                offsets=tuple(scale * b + shift for b in s.offsets),
            )
            for s in model.segments
        ),
    )
    assert costs(changed) == costs(model)
    raw = [(0, F(0)), (1, F(-2))]
    assert reference.evaluate(changed, report(changed, raw), "1") == reference.evaluate(
        model, report(model, raw), "1"
    )
    assert not reference.verify_cost(changed, reference.propose_cost(model)).accepted


def test_cost_unit_is_required_and_bound_to_the_certificate():
    model = shared_error()
    changed = replace(model, cost_unit="seconds")
    assert not reference.verify_cost(changed, reference.propose_cost(model)).accepted
    with pytest.raises(TypeError, match="cost-unit"):
        reference.validate(replace(model, cost_unit=""))


def test_overlapping_duplicate_segments_do_not_create_information():
    model = shared_error()
    repeated = replace(model, segments=model.segments + (model.segments[0],))
    assert reference.sample_worlds(repeated) == reference.sample_worlds(model)
    assert costs(repeated) == costs(model)


@pytest.mark.parametrize("values", list(product((0, 1), repeat=4)))
def test_degenerate_supports_agree_with_direct_finite_checker(values):
    model = Model(
        shared_error().channels,
        tuple(
            Segment(
                str(x),
                "*",
                str(x),
                "m",
                F(0),
                F(0),
                (F(1), F(1)),
                (F(values[2 * x]), F(values[2 * x + 1])),
            )
            for x in (0, 1)
        ),
    )
    direct = solver.Instance(
        ("0", "1"),
        ("*", "*"),
        ("0", "1"),
        tuple(
            solver.Instrument(name, (str(values[j]), str(values[2 + j])), F(1))
            for j, name in enumerate(("A", "B"))
        ),
    )
    expected = solver.solve(direct)
    assert costs(model) == (expected["fixed"]["value"], expected["adaptive"]["value"])


def test_degenerate_support_preserves_the_existing_adaptive_gap():
    values = ((0, 0, 0), (0, 10, 0), (10, 0, 0), (10, 0, 10))
    model = Model(
        tuple(
            Channel(name, "raw", "m", F(1), F(0), F(price))
            for name, price in zip(("A", "B", "C"), (1, 3, 3))
        ),
        tuple(
            Segment(str(i), "*", str(i), "m", F(0), F(0), (F(1),) * 3, tuple(map(F, row)))
            for i, row in enumerate(values)
        ),
    )
    assert costs(model) == ("7", "4")


@pytest.mark.parametrize(
    "mutation",
    ["digest", "unit", "repeat", "unknown", "bool", "float", "fraction", "exponent", "extra"],
)
def test_report_rejects_unbound_or_noncanonical_data(mutation):
    model = shared_error()
    data = report(model, [(0, F(0))])
    match mutation:
        case "digest":
            data["model_sha256"] = "forged"
        case "unit":
            data["readings"][0]["raw_unit"] = "wrong"
        case "repeat":
            data["readings"].append(dict(data["readings"][0]))
        case "unknown":
            data["readings"][0]["channel"] = "missing"
        case "bool":
            data["readings"][0]["value"] = False
        case "float":
            data["readings"][0]["value"] = 0.0
        case "fraction":
            data["readings"][0]["value"] = "0/2"
        case "exponent":
            data["readings"][0]["value"] = "1e1000000000"
        case "extra":
            data["permission"] = True
    assert reference.evaluate(model, data, "0").status == "INVALID_REPORT"


def test_cost_verification_reconstructs_witness_without_proposal_fallback(monkeypatch):
    model = shared_error()
    certificate = reference.propose_cost(model)
    monkeypatch.setattr(
        solver, "solve", lambda *_: pytest.fail("verification called proposal solver")
    )
    assert reference.verify_cost(model, certificate).accepted
    wrong = deepcopy(certificate)
    wrong["finite_certificate"]["adaptive"]["value"] = "1"
    assert not reference.verify_cost(model, wrong).accepted
    wrong = deepcopy(certificate)
    wrong["finite_certificate"]["adaptive"]["table"].pop()
    assert not reference.verify_cost(model, wrong).accepted
    substituted = replace(
        model, segments=(replace(model.segments[0], upper=F(2)), model.segments[1])
    )
    assert not reference.verify_cost(substituted, certificate).accepted


def test_resource_refusal_and_invalid_models_are_not_infeasibility():
    model = shared_error()
    large = replace(
        model,
        segments=model.segments
        + (replace(model.segments[1], state="2", answer="2", offsets=(F(2), F(-2))),),
    )
    with pytest.raises(ValueError, match="state cap"):
        reference.propose_cost(large)
    invalid = [
        replace(model, segments=()),
        replace(model, segments=(replace(model.segments[0], lower=F(2)),)),
        replace(model, segments=(replace(model.segments[0], slopes=(F(0), F(1))),)),
        replace(model, segments=(replace(model.segments[0], slopes=(F(1),)),)),
        replace(model, segments=(replace(model.segments[0], lower=False),)),
        replace(model, segments=(model.segments[0], replace(model.segments[1], state="0"))),
        replace(model, channels=(replace(model.channels[0], raw_gain=F(0)), model.channels[1])),
        replace(model, channels=(replace(model.channels[0], price=F(0)), model.channels[1])),
    ]
    for bad in invalid:
        with pytest.raises((ValueError, TypeError)):
            reference.propose_cost(bad)
    with pytest.raises(ValueError, match="inconsistent"):
        reference.conditional_instance(model, 0, F(100), "*")


def test_bundle_inventory_and_replay_are_strict(monkeypatch):
    bundle = propose_bundle()
    monkeypatch.setattr(solver, "solve", lambda *_: pytest.fail("replay called proposal solver"))
    assert verify_bundle(bundle)["shared_error"] == {"fixed": "2", "adaptive": "2"}
    bundle.pop("parity_points")
    with pytest.raises(ValueError, match="inventory"):
        verify_bundle(bundle)
