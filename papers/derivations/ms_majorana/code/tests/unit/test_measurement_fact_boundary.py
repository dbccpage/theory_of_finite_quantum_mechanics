"""Raw evidence remains usable; an absent checker cannot manufacture facts.

These are admission and explicit-unavailability tests, not source authentication,
method/tolerance validation, complete hash binding, or certificate verification.
"""

import importlib
import json
from dataclasses import FrozenInstanceError, asdict, replace

import pytest
from pydantic import TypeAdapter, ValidationError

from omega_engine.crates.kernel.higher_operad.result import Err
from omega_engine.crates.measurement.measurement import (
    MeasurementEnvelope,
    MeasurementKernel,
    MeasurementValue,
    MeasurementValueKind,
    verify_measurement_contract,
)


def raw_envelope():
    return MeasurementKernel().create_envelope(
        measurement_id="measurement:claimed",
        source_ref="source:claimed",
        method_ref="method:claimed",
        value=MeasurementValue(MeasurementValueKind.EXACT_RATIONAL, "1/2", "count"),
        tolerance_ref="tolerance:claimed",
        witness_refs=["witness:claimed"],
        certificate_refs=["certificate:claimed"],
        replay_refs=["replay:claimed"],
    )


def assert_checker_unavailable(result):
    assert type(result) is Err
    assert result.error.to_dict() == {
        "code": "MEASUREMENT_CHECKER_UNAVAILABLE",
        "message": "The trusted measurement checker boundary is not implemented.",
        "locus": "MeasurementKernel.verify_measurement",
        "details": {"authority_effect": "None", "checks_performed": "none"},
    }


def test_raw_creation_and_json_preserve_submitted_evidence_without_facts():
    original = raw_envelope()
    assert original.measurement_id == "measurement:claimed"
    assert original.source_ref == "source:claimed"
    assert original.method_ref == "method:claimed"
    assert original.value == MeasurementValue(
        MeasurementValueKind.EXACT_RATIONAL, "1/2", "count"
    )
    assert original.tolerance_ref == "tolerance:claimed"
    assert original.witness_refs == ["witness:claimed"]
    assert original.certificate_refs == ["certificate:claimed"]
    assert original.replay_refs == ["replay:claimed"]
    assert original.authority_effect == "EvidenceOnly"
    assert original.measurement_hash == original.compute_hash()
    assert len(original.measurement_hash) == 64

    adapter = TypeAdapter(MeasurementEnvelope)
    encoded = adapter.dump_json(original)
    assert json.loads(encoded)["authority_effect"] == "EvidenceOnly"
    restored = adapter.validate_json(encoded)
    assert restored == original
    assert_checker_unavailable(MeasurementKernel().verify_measurement(restored))


@pytest.mark.parametrize(
    "label", ["FactOnly", "fact_only", "Certified", "StateTransition", "None", "", None]
)
def test_raw_constructor_rejects_stronger_and_unknown_authority_labels(label):
    fields = asdict(raw_envelope())
    fields["authority_effect"] = label
    with pytest.raises(ValidationError) as caught:
        MeasurementEnvelope(**fields)
    assert [(e["loc"], e["type"]) for e in caught.value.errors()] == [
        (("authority_effect",), "literal_error")
    ]


@pytest.mark.parametrize(
    "label", ["FactOnly", "fact_only", "Certified", "StateTransition", "None", "", None]
)
def test_raw_json_rejects_stronger_and_unknown_authority_labels(label):
    adapter = TypeAdapter(MeasurementEnvelope)
    fields = json.loads(adapter.dump_json(raw_envelope()))
    fields["authority_effect"] = label
    with pytest.raises(ValidationError) as caught:
        adapter.validate_json(json.dumps(fields))
    assert [(e["loc"], e["type"]) for e in caught.value.errors()] == [
        (("authority_effect",), "literal_error")
    ]


def test_raw_field_assignment_cannot_upgrade_evidence():
    envelope = raw_envelope()
    with pytest.raises(FrozenInstanceError):
        envelope.authority_effect = "FactOnly"
    assert envelope.authority_effect == "EvidenceOnly"


@pytest.mark.parametrize(
    "case", ["raw", "corrupt_hash", "rehashed", "unit_changed", "empty_refs"]
)
def test_raw_and_altered_evidence_never_substitutes_for_the_missing_checker(case):
    envelope = raw_envelope()
    if case == "corrupt_hash":
        envelope = replace(envelope, measurement_hash="0" * 64)
    elif case == "rehashed":
        envelope = replace(
            envelope, value=MeasurementValue(MeasurementValueKind.INTEGER, 13, "count")
        )
        envelope = replace(envelope, measurement_hash=envelope.compute_hash())
    elif case == "unit_changed":
        envelope = replace(envelope, value=replace(envelope.value, unit="kg"))
    elif case == "empty_refs":
        envelope = replace(
            envelope, witness_refs=[], certificate_refs=[], replay_refs=[]
        )
    assert_checker_unavailable(
        MeasurementKernel().verify_measurement(envelope, "claimed-checker")
    )


def test_checker_unavailability_precedes_untrusted_input_or_checker_name_access():
    class Trap:
        def __getattribute__(self, name):
            raise AssertionError("UNTRUSTED_ATTRIBUTE_READ")

        def __str__(self):
            raise AssertionError("UNTRUSTED_STRINGIFICATION")

        def __repr__(self):
            raise AssertionError("UNTRUSTED_REPRESENTATION")

    assert_checker_unavailable(MeasurementKernel().verify_measurement(Trap(), Trap()))


@pytest.mark.parametrize(
    "module_name",
    ["omega_engine.crates.measurement", "omega_engine.crates.measurement.measurement"],
)
def test_public_checked_measurement_constructor_is_retired(module_name):
    module = importlib.import_module(module_name)
    assert module.MeasurementEnvelope is MeasurementEnvelope
    assert module.MeasurementKernel is MeasurementKernel
    assert "MeasurementEnvelope" in module.__all__
    assert "CheckedMeasurement" not in module.__all__
    with pytest.raises(AttributeError, match="CheckedMeasurement"):
        _ = module.CheckedMeasurement


def test_api_shape_probe_does_not_discharge_the_missing_checker():
    kernel = MeasurementKernel()
    assert verify_measurement_contract(kernel) is True
    assert verify_measurement_contract(object()) is False
    assert_checker_unavailable(kernel.verify_measurement(raw_envelope()))
