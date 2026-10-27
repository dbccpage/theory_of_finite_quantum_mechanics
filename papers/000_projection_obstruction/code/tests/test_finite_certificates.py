"""Independent finite evidence replay and hostile record controls."""

from copy import deepcopy
from dataclasses import replace

import pytest

sp = pytest.importorskip("sympy")

from ffi import NativeMeasurementUnavailable, measurement_call
from finite_certificates import build_finite_certificates
from finite_inputs import local_zero_models, measurement_requests
from local_persistent_zero import LocalTerm, decode_certificate, verify_local_zero
from verify_finite_certificates import verify_finite_records


@pytest.fixture(scope="module")
def records():
    return build_finite_certificates()


def require_native(records):
    refused = {name: records[name] for name in measurement_requests() if records[name]["status"] == "refused"}
    if refused:
        pytest.skip(f"native measurement capability unavailable: {refused}")


def test_complete_records_replay_with_explicit_capability_refusals(records):
    assert verify_finite_records(records) == []
    assert records["commuting_boundary"]["status"] == "verified"
    assert records["rotating_polynomial"]["status"] == "verified"


@pytest.mark.native_integration
def test_native_measurement_examples(records):
    require_native(records)
    for name in measurement_requests():
        assert records[name]["status"] == "verified", records[name]
    assert records["separable_correlated"]["certificate"]["quotient"] == "1"
    assert records["separable_correlated"]["certificate"]["product_distance_lower_bound"] == "3/10"
    assert records["three_factor"]["certificate"]["product_distance_lower_bound"] == "7/240"
    assert records["ising_five_cycle"]["certificate"]["quotient"] == "1"
    assert records["ising_five_cycle"]["certificate"]["product_distance_lower_bound"] == "13/60"


@pytest.mark.parametrize("path,value", [
    (("contract", "arity"), 2),
    (("contract", "reading_error"), "0"),
    (("contract", "observables", 0, "factors", 0, "axis"), "Z"),
    (("repair_potential", 0), "8"),
])
@pytest.mark.native_integration
def test_changed_measurement_input_rejected_even_if_certificate_reissued(records, path, value):
    require_native(records)
    changed = deepcopy(measurement_requests()["three_factor"])
    cursor = changed
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    try:
        forged = measurement_call("measurement_evaluate", changed)
    except NativeMeasurementUnavailable:
        return  # Malformed arity/repair is refused by the producer as well.
    mutation = deepcopy(records)
    mutation["three_factor"]["certificate"] = forged
    assert verify_finite_records(mutation)


@pytest.mark.parametrize("field,value", [("corrected_moments", ["0"] * 3),
    ("quotient", "0"), ("product_distance_lower_bound", "1"),
    ("laboratory_coverage", "verified"), ("authority_effect", "Authorized")])
@pytest.mark.native_integration
def test_forged_measurement_consequences_are_rejected(records, field, value):
    require_native(records)
    mutation = deepcopy(records)
    mutation["separable_correlated"]["certificate"][field] = value
    assert verify_finite_records(mutation)


@pytest.mark.native_integration
def test_valid_changed_support_is_bound_even_after_full_reissue(records):
    require_native(records)
    changed = deepcopy(measurement_requests()["ising_five_cycle"])
    changed["contract"]["observables"][0]["factors"][2]["site"] = 3
    cert = measurement_call("measurement_evaluate", changed)
    mutation = deepcopy(records)
    mutation["ising_five_cycle"]["certificate"] = cert
    assert verify_finite_records(mutation)


def test_changed_boundary_fails_after_a_valid_record(records):
    cert = decode_certificate(records["commuting_boundary"]["certificate"])
    model = local_zero_models()["commuting_boundary"]
    x = sp.Matrix([[0, 1], [1, 0]])
    changed = replace(model, terms=(LocalTerm((0, 1), sp.kronecker_product(x, x)),))
    assert not verify_local_zero(changed, cert)


@pytest.mark.parametrize("field,value", [("annihilator", ["1", "1"]),
    ("derivatives", [["1"]]), ("first_onset", 0),
    ("model_digest", "0" * 64), ("authority_effect", "Authorized")])
def test_forged_local_zero_records_are_rejected(records, field, value):
    mutation = deepcopy(records)
    mutation["commuting_boundary"]["certificate"][field] = value
    assert verify_finite_records(mutation)


def test_missing_and_unknown_records_cannot_silently_shrink_coverage(records):
    mutation = deepcopy(records)
    del mutation["three_factor"]
    assert verify_finite_records(mutation)
    mutation["invented"] = {"status": "verified", "certificate": {}}
    assert verify_finite_records(mutation)


def test_zero_denominator_and_inexact_local_entries_are_refused(records):
    for value in ("1/0", "0.0", 0.0, True):
        mutation = deepcopy(records)
        mutation["commuting_boundary"]["certificate"]["annihilator"][0] = value
        assert verify_finite_records(mutation)
