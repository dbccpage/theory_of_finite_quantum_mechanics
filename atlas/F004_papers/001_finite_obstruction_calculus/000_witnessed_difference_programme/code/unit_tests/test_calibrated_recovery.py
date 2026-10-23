"""Controls for support loss, forged reports, units, and conditional cost transfer."""

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F

import pytest
from calibrated_recovery import bridge
from calibrated_recovery.bridge import (
    alphabet,
    evaluate,
    finite_lift,
    model_hash,
    propose_cost,
    verify_cost,
)
from calibrated_recovery.examples import correlated_enclosure, separated, touching
from calibrated_recovery.replay import propose_bundle, verify_bundle
from finite_observation import solver


@pytest.mark.parametrize(
    "text", ["1e1000000000", "1e-1000000000", "1.0", " 1", "1\n", "1_0", "１２", "1" * 161]
)
def test_invalid_report_syntax_never_reaches_fraction_construction(monkeypatch, text):
    monkeypatch.setattr(
        bridge, "Fraction", lambda *_: pytest.fail("arithmetic before syntax admission")
    )
    with pytest.raises(ValueError, match="canonical"):
        bridge._parse_fraction(text)


def report(model, values, visible="*"):
    return {
        "model_sha256": model_hash(model),
        "visible": visible,
        "readings": [
            {
                "channel": model.channels[i].name,
                "raw_unit": model.channels[i].raw_unit,
                "value": str(value),
            }
            for i, value in values
        ],
    }


def test_positive_noise_preserves_the_exact_adaptive_cost_gap():
    for radius in (F(0), F(1), F(499, 100)):
        model = separated(radius)
        certificate = propose_cost(model)
        assert verify_cost(model, certificate).accepted
        assert certificate["finite_certificate"]["fixed"]["value"] == "7"
        assert certificate["finite_certificate"]["adaptive"]["value"] == "4"
        assert len(finite_lift(model).states) == 4


def test_ideal_cost_does_not_certify_bounded_raw_api_feasibility():
    model = bridge.Model(
        ("low", "high"), ("*", "*"), ("low", "high"),
        (bridge.Channel("M", "raw", "cal", F(1, 2**255), F(0),
                        ((F(0), F(0)), (F(2**255), F(2**255))), F(1)),),
    )
    bridge.validate(model)
    certificate = propose_cost(model)
    assert certificate["cost_domain"] == "ideal_calibrated_interval_product"
    assert verify_cost(model, certificate).accepted
    assert certificate["finite_certificate"]["fixed"]["value"] == "1"
    assert certificate["finite_certificate"]["adaptive"]["value"] == "1"
    raw_high = F(2**510)
    assert model.channels[0].gain * raw_high == 2**255
    assert raw_high.numerator.bit_length() == 511
    assert len(str(raw_high)) <= 160  # Bit refusal, not the separate text cap.
    assert evaluate(model, report(model, [(0, raw_high)]), "high").status == "INVALID_REPORT"
    assert evaluate(model, report(model, [(0, F(0))]), "low").status == "VERIFIED"
    assert evaluate(model, report(model, [(0, F(0))]), "high").status == "INVALID_PROPOSAL"


@pytest.mark.parametrize("scope", [None, "bounded_raw_api", True])
def test_cost_scope_cannot_be_omitted_or_promoted(scope):
    model = separated()
    certificate = propose_cost(model)
    if scope is None:
        certificate.pop("cost_domain")
    else:
        certificate["cost_domain"] = scope
    assert not verify_cost(model, certificate).accepted


def test_answer_requires_nonempty_unanimous_candidates_and_correct_proposal():
    model = separated()
    partial = report(model, [(0, F(-1, 2))])
    assert evaluate(model, partial, "00").status == "ABSTAIN"
    complete = report(model, [(0, F(-1, 2)), (1, F(-1, 2))])
    assert evaluate(model, complete, "00").status == "VERIFIED"
    assert evaluate(model, complete, "11").status == "INVALID_PROPOSAL"
    assert evaluate(model, complete, False).status == "INVALID_PROPOSAL"
    assert evaluate(model, report(model, [(0, F(100))]), "00").status == "INCONSISTENT"
    assert evaluate(model, report(model, [], "absent"), "00").status == "INCONSISTENT"


def test_singleton_endpoints_cannot_be_discarded():
    model = touching()
    assert alphabet(model.channels[0]) == ((0,), (0, 1), (1,))
    assert evaluate(model, report(model, [(0, F(1))]), "a").status == "ABSTAIN"
    certificate = propose_cost(model)
    assert verify_cost(model, certificate).accepted
    assert certificate["finite_certificate"]["fixed"]["value"] is None
    assert certificate["finite_certificate"]["adaptive"]["value"] is None
    collision = separated(F(5))
    assert (
        evaluate(collision, report(collision, [(i, F(2)) for i in range(3)]), "00").status
        == "ABSTAIN"
    )


def test_degenerate_point_intervals_and_empty_instrument_shelf():
    model = touching()
    point = replace(
        model, channels=(replace(model.channels[0], intervals=((F(0), F(0)), (F(1), F(1)))),)
    )
    certificate = propose_cost(point)
    assert verify_cost(point, certificate).accepted
    assert certificate["finite_certificate"]["adaptive"]["value"] == "1"
    free = replace(model, visible=("a", "b"), channels=())
    assert propose_cost(free)["finite_certificate"]["adaptive"]["value"] == "0"
    assert evaluate(free, report(free, [], "a"), "a").status == "VERIFIED"


@pytest.mark.parametrize("scale,shift", [(F(100), F(7)), (F(-3, 2), F(11))])
def test_affine_unit_change_transports_intervals_reports_and_costs(scale, shift):
    model = separated()
    converted = replace(
        model,
        channels=tuple(
            replace(
                c,
                unit="converted",
                gain=scale * c.gain,
                offset=scale * c.offset + shift,
                intervals=tuple(
                    tuple(sorted((scale * a + shift, scale * b + shift))) for a, b in c.intervals
                ),
            )
            for c in model.channels
        ),
    )
    raw = [(0, F(-1, 2)), (1, F(-1, 2))]
    assert evaluate(model, report(model, raw), "00") == evaluate(
        converted, report(converted, raw), "00"
    )
    before, after = propose_cost(model), propose_cost(converted)
    assert verify_cost(converted, after).accepted
    assert before["finite_certificate"] == after["finite_certificate"]
    assert not verify_cost(converted, before).accepted


@pytest.mark.parametrize(
    "mutation", ["digest", "unit", "duplicate", "unknown", "bool", "float", "fraction", "extra"]
)
def test_report_parser_rejects_unbound_or_ambiguous_inputs(mutation):
    model = separated()
    data = report(model, [(0, F(-1, 2))])
    match mutation:
        case "digest":
            data["model_sha256"] = "forged"
        case "unit":
            data["readings"][0]["raw_unit"] = "cm"
        case "duplicate":
            data["readings"].append(data["readings"][0].copy())
        case "unknown":
            data["readings"][0]["channel"] = "unknown"
        case "bool":
            data["readings"][0]["value"] = True
        case "float":
            data["readings"][0]["value"] = -0.5
        case "fraction":
            data["readings"][0]["value"] = "-2/4"
        case "extra":
            data["trusted"] = True
    assert evaluate(model, data, "00").status == "INVALID_REPORT"


def test_cost_checker_does_not_replace_tampered_certificates(monkeypatch):
    model = separated()
    certificate = propose_cost(model)
    monkeypatch.setattr(solver, "solve", lambda *_: pytest.fail("verifier called proposal solver"))
    assert verify_cost(model, certificate).accepted
    changed = deepcopy(certificate)
    changed["finite_certificate"]["adaptive"]["value"] = "3"
    assert not verify_cost(model, changed).accepted
    changed = deepcopy(certificate)
    changed["finite_certificate"]["adaptive"]["table"].pop()
    assert not verify_cost(model, changed).accepted
    new_price = replace(
        model, channels=(replace(model.channels[0], price=F(2)),) + model.channels[1:]
    )
    assert not verify_cost(new_price, certificate).accepted


def test_correlated_noise_is_strictly_easier_than_its_rectangular_enclosure():
    model = correlated_enclosure()
    certificate = propose_cost(model)
    assert verify_cost(model, certificate).accepted
    assert certificate["finite_certificate"]["adaptive"]["value"] is None
    assert evaluate(model, report(model, [(0, F(0)), (1, F(0))]), "0").status == "ABSTAIN"
    for x in (F(0), F(1)):
        for noise in (F(-1), F(-1, 3), F(0), F(1)):
            plus, minus = x + noise, -x + noise
            assert (plus - minus) / 2 == x
    # These finite points accompany the written all-noise cancellation proof.


def test_caps_and_invalid_models_refuse_without_claiming_infeasibility():
    with pytest.raises(ValueError, match="state cap"):
        finite_lift(separated(F(5)))
    model = touching()
    with pytest.raises(TypeError, match="Fraction"):
        propose_cost(replace(model, channels=(replace(model.channels[0], price=True),)))
    with pytest.raises(ValueError, match="reversed"):
        propose_cost(
            replace(
                model,
                channels=(replace(model.channels[0], intervals=((F(1), F(0)), (F(1), F(2)))),),
            )
        )
    with pytest.raises(ValueError, match="nonzero"):
        propose_cost(replace(model, channels=(replace(model.channels[0], gain=F(0)),)))


def test_bundle_requires_every_named_case_and_replays_without_proposal(monkeypatch):
    bundle = propose_bundle()
    monkeypatch.setattr(solver, "solve", lambda *_: pytest.fail("replay called proposal solver"))
    assert verify_bundle(bundle)["separated"] == {"fixed": "7", "adaptive": "4"}
    bundle.pop("touching")
    with pytest.raises(ValueError, match="inventory"):
        verify_bundle(bundle)


def test_failure_to_scale_the_error_bound_loses_an_admitted_reading():
    model = touching()
    c = model.channels[0]
    converted = replace(
        model,
        channels=(
            replace(c, gain=F(100), unit="cm", intervals=((F(0), F(100)), (F(100), F(200)))),
        ),
    )
    wrong = replace(
        converted,
        channels=(replace(converted.channels[0], intervals=((F(49), F(51)), (F(149), F(151)))),),
    )
    raw = [(0, F(1, 4))]
    assert evaluate(converted, report(converted, raw), "a").status == "VERIFIED"
    assert evaluate(wrong, report(wrong, raw), "a").status == "INCONSISTENT"
