from dataclasses import replace
from itertools import product

import pytest
from self_reference_bridges import (
    BridgeSignature,
    ProvenanceLink,
    realize_bridge,
    self_witness_payload,
    verify_self_witness_event,
)
from witnessed_difference.observation import (
    EvaluatorResult,
    EvaluatorStanding,
    EvaluatorStatus,
    Interaction,
    ObservationReceipt,
    classify_observation,
)
from witnessed_difference.outcomes import Accepted, Refused
from witnessed_difference.witness import Registration, make_witness


def full():
    return realize_bridge(BridgeSignature(True, True, True, True, True, True))


def observation(payload):
    registration = Registration("self:0", payload, 0)
    witnessed = make_witness(registration, dict(payload), "E")
    assert isinstance(witnessed, Accepted)
    observed = classify_observation(ObservationReceipt(
        Interaction(("self:0", "probe"), "self:0"), registration, witnessed.value,
        EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
    ))
    assert isinstance(observed, Accepted)
    return observed.value


def test_complete_aggregate_classification_and_universal_implications():
    count = 0
    for flags in product((False, True), repeat=6):
        signature = BridgeSignature(*flags)
        if signature.realizable():
            model = realize_bridge(signature)
            assert model.signature() == signature
            assert all(model.point(x)[3] for x in range(2)) == signature.report_total
            count += 1
        else:
            with pytest.raises(ValueError):
                realize_bridge(signature)
    assert count == 19


def test_exhaustive_partial_reports_contexts_later_targets_and_protocols():
    base = full()
    for reports, target in product(product((None, 0, 1), repeat=2), repeat=2):
        for context, later in product(product(range(2), repeat=2), repeat=2):
            for domain in (None, frozenset(), frozenset(product(range(2), repeat=2))):
                provenance = tuple(None if r is None else ProvenanceLink(0, 0, x, x, r) for x, r in enumerate(reports))
                model = replace(base, reports=reports, target=target, context=context, later=later, provenance=provenance, generation=frozenset(product(range(2), repeat=2)), comparison_domain=domain)
                signature = model.signature()
                assert signature.realizable()
                for x in range(2):
                    point = model.point(x)
                    available = reports[x] is not None and target[later[x]] is not None and domain is not None and (reports[x], target[later[x]]) in domain
                    assert point[5] == available
                    assert point[6] == (available and reports[x] == target[later[x]])


def test_actual_accepted_self_witness_targets_reflexive_accessible_state():
    model = full()
    payload = self_witness_payload(model, 0)
    observed = observation(payload)
    checked = verify_self_witness_event(model, 0, observed, dict(payload))
    assert isinstance(checked, Accepted) and checked.value
    changed_reaccess = dict(payload, report=1)
    assert isinstance(verify_self_witness_event(model, 0, observed, changed_reaccess), Refused)
    foreign_target = dict(payload, observer_id=1)
    assert isinstance(verify_self_witness_event(model, 0, observation(foreign_target), foreign_target), Refused)
    # Correctly hashed but wrong finite-type target is still rejected.
    bool_target = dict(payload, state_index=False)
    assert isinstance(verify_self_witness_event(model, 0, observation(bool_target), bool_target), Refused)
    assert isinstance(verify_self_witness_event(model, 0, None, payload), Refused)
    assert isinstance(verify_self_witness_event(None, 0, observed, payload), Refused)


def test_later_factorization_and_generator_regularities_are_checked():
    base = full()
    sigma_collision = replace(base, sigma=(0, 0))
    assert sigma_collision.later_target_factor_accessible() is None
    later_collision = replace(base, later=(0, 0))
    assert later_collision.prescribed_target_factor_later((0, 1)) is None
    assert later_collision.prescribed_target_factor_later((0, None)) is None
    assert later_collision.prescribed_target_factor_later((1, 1)) == {0: 1}
    richer = replace(base, presentation=(0, 0))
    assert richer.signature().linkage_verified
    assert richer.report_factor_accessible() == {0: 0, 1: 1}
    assert richer.report_factor_presentation() is None
    nondeterministic = replace(base, sigma=(0, 0), provenance=(ProvenanceLink(0, 0, 0, 0, 0), ProvenanceLink(0, 0, 0, 0, 1)), generation=frozenset({(0, 0), (0, 1)}))
    assert nondeterministic.signature().linkage_verified
    assert not nondeterministic.generation_is_functional()
    assert nondeterministic.report_factor_accessible() is None
    assert base.generation_is_functional()


def test_stale_or_unbound_provenance_does_not_create_r1():
    base = full()
    for link in (ProvenanceLink(1, 0, 0, 0, 0), ProvenanceLink(0, 1, 0, 0, 0), ProvenanceLink(0, 0, 0, 1, 0), ProvenanceLink(0, 0, 0, 0, 1)):
        model = replace(base, provenance=(link, base.provenance[1]))
        assert model.point(0)[1] and not model.point(0)[2]
        with pytest.raises(ValueError):
            self_witness_payload(model, 0)
    model = replace(base, generation=frozenset())
    assert model.signature().linkage_provided and not model.signature().linkage_verified


def test_partial_and_noncanonical_model_boundaries_refuse():
    base = full()
    for changes in ({"context": (0,)}, {"later": (2, 0)}, {"target": (False, 1)}, {"sigma": (0, True)}, {"generation": frozenset({(0, 2)})}, {"report_count": 0}, {"comparison_domain": frozenset({(0, 2)})}, {"provenance": (object(), None)}, {"generation": None}):
        with pytest.raises((TypeError, ValueError)):
            replace(base, **changes)
    with pytest.raises(TypeError):
        BridgeSignature(1, True, True, True, True, True)
    with pytest.raises(ValueError):
        base.point(True)
    with pytest.raises(ValueError):
        base.prescribed_target_factor_later((0,))


def test_exact_fixed_bridge_plans_and_partial_report_event_stability():
    base = full()
    planned = base.successful_linked_report_plan(True)
    assert planned is not None
    assert planned.signature().linkage_verified and planned.signature().comparison_success and planned.signature().report_stable
    unstable = replace(base, context=(1, 0))
    assert unstable.successful_linked_report_plan(True) is None
    assert unstable.successful_linked_report_plan(False) is not None
    for missing in (replace(base, target=(1, None)), replace(base, generation=frozenset()), replace(base, comparison_domain=None), replace(base, comparison_domain=frozenset())):
        assert missing.successful_linked_report_plan(False) is None
    partial = replace(base, reports=(0, None))
    assert partial.report_events_preserved()
    assert not partial.signature().report_total and not partial.signature().report_stable
    assert not replace(partial, context=(1, 0)).report_events_preserved()
