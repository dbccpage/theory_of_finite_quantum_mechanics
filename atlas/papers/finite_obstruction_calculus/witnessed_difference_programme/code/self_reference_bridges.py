"""Explicit CH14 finite R1/R2/R3 bridges and accepted self-witness replay.

Generation/comparison tables are declared semantics, not physical truth.
Partiality, richer accessible state, and reflexive provenance are explicit.
"""

from dataclasses import dataclass, fields, replace

from witnessed_difference.observation import AcceptedObservation, classify_observation
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.witness import payload_digest, verify_witness


@dataclass(frozen=True)
class ProvenanceLink:
    source_observer: int
    target_observer: int
    captured_accessible: int
    reaccessed_accessible: int
    reported_value: int


@dataclass(frozen=True)
class BridgeSignature:
    report_total: bool
    linkage_provided: bool
    linkage_verified: bool
    report_stable: bool
    comparison_available: bool
    comparison_success: bool

    def __post_init__(self):
        if any(type(getattr(self, field.name)) is not bool for field in fields(self)):
            raise TypeError("bridge predicates require Boolean values")

    def realizable(self):
        if not self.report_total:
            return not any((self.linkage_provided, self.linkage_verified, self.report_stable, self.comparison_available, self.comparison_success))
        return (not self.linkage_verified or self.linkage_provided) and (not self.comparison_success or self.comparison_available)


def _factor(keys, values):
    result = {}
    for key, value in zip(keys, values):
        if key in result and result[key] != value:
            return None
        result[key] = value
    return result


@dataclass(frozen=True)
class SelfReferenceModel:
    observer_id: int
    observer_count: int
    accessible_count: int
    report_count: int
    sigma: tuple[int, ...]
    presentation: tuple[int, ...]
    reports: tuple[int | None, ...]
    provenance: tuple[ProvenanceLink | None, ...]
    context: tuple[int, ...]
    later: tuple[int, ...]
    target: tuple[int | None, ...]
    generation: frozenset[tuple[int, int]]
    comparison_domain: frozenset[tuple[int, int]] | None

    def __post_init__(self):
        n = len(self.sigma)
        for value in (self.observer_count, self.accessible_count, self.report_count):
            if type(value) is not int or value <= 0:
                raise ValueError("finite bridge carriers must have positive integer sizes")
        if type(self.observer_id) is not int or not 0 <= self.observer_id < self.observer_count or n == 0:
            raise ValueError("observer identity/carrier is invalid")
        for row, size in ((self.sigma, self.accessible_count), (self.presentation, None), (self.context, n), (self.later, n)):
            if not isinstance(row, tuple) or any(type(x) is not int or x < 0 or (size is not None and x >= size) for x in row):
                raise ValueError("finite bridge map leaves its declared carrier")
        if len(self.presentation) != self.accessible_count or any(not isinstance(row, tuple) or len(row) != n for row in (self.reports, self.provenance, self.context, self.later, self.target)):
            raise ValueError("bridge maps require every declared row")
        for row in (self.reports, self.target):
            if any(value is not None and (type(value) is not int or not 0 <= value < self.report_count) for value in row):
                raise ValueError("partial report/target leaves its carrier")
        for candidate in self.provenance:
            if candidate is None:
                continue
            if not isinstance(candidate, ProvenanceLink):
                raise TypeError("provenance candidates must be typed links")
            for value, size in ((candidate.source_observer, self.observer_count), (candidate.target_observer, self.observer_count), (candidate.captured_accessible, self.accessible_count), (candidate.reaccessed_accessible, self.accessible_count), (candidate.reported_value, self.report_count)):
                if type(value) is not int or not 0 <= value < size:
                    raise ValueError("provenance candidate leaves its declared carrier")
        for relation, first_size in ((self.generation, self.accessible_count), (self.comparison_domain, self.report_count)):
            if relation is None:
                continue
            if not isinstance(relation, frozenset) or any(not isinstance(pair, tuple) or len(pair) != 2 or type(pair[0]) is not int or type(pair[1]) is not int or not 0 <= pair[0] < first_size or not 0 <= pair[1] < self.report_count for pair in relation):
                raise ValueError("generation/protocol requires an exact finite relation")
        if self.generation is None:
            raise ValueError("the generation relation must be declared, even if empty")

    def point(self, x: int):
        if type(x) is not int or not 0 <= x < len(self.sigma):
            raise ValueError("audit point leaves its carrier")
        report, link = self.reports[x], self.provenance[x]
        supplied = report is not None and link is not None
        verified = supplied and link.source_observer == self.observer_id and link.target_observer == self.observer_id and link.captured_accessible == self.sigma[x] and link.reaccessed_accessible == self.sigma[x] and link.reported_value == report and (self.sigma[x], report) in self.generation
        transported = self.reports[self.context[x]]
        stable_available = report is not None and transported is not None
        target = self.target[self.later[x]]
        compare_available = report is not None and target is not None and self.comparison_domain is not None and (report, target) in self.comparison_domain
        return (report is not None, supplied, bool(verified), stable_available, stable_available and report == transported, compare_available, compare_available and report == target)

    def signature(self):
        points = tuple(self.point(x) for x in range(len(self.sigma)))
        flags = tuple(all(point[index] for point in points) for index in (0, 1, 2, 4, 5, 6))
        return BridgeSignature(*flags)

    def report_events_preserved(self):
        return all(report is None or report == self.reports[self.context[x]] for x, report in enumerate(self.reports))

    def successful_linked_report_plan(self, require_context_stability=False):
        reports = tuple(self.target[x] for x in self.later)
        if self.comparison_domain is None or any(r is None or (self.sigma[x], r) not in self.generation or (r, r) not in self.comparison_domain for x, r in enumerate(reports)):
            return None
        if require_context_stability and any(r != reports[self.context[x]] for x, r in enumerate(reports)):
            return None
        provenance = tuple(ProvenanceLink(self.observer_id, self.observer_id, self.sigma[x], self.sigma[x], r) for x, r in enumerate(reports))
        return replace(self, reports=reports, provenance=provenance)

    def generation_is_functional(self):
        return _factor(tuple(a for a, _ in sorted(self.generation)), tuple(r for _, r in sorted(self.generation))) is not None

    def report_factor_accessible(self):
        return _factor(self.sigma, self.reports)

    def report_factor_presentation(self):
        return _factor(tuple(self.presentation[a] for a in self.sigma), self.reports)

    def later_target_factor_accessible(self):
        return _factor(self.sigma, tuple(self.target[x] for x in self.later))

    def prescribed_target_factor_later(self, values: tuple[int | None, ...]):
        if not isinstance(values, tuple) or len(values) != len(self.sigma) or any(value is not None and (type(value) is not int or not 0 <= value < self.report_count) for value in values):
            raise ValueError("prescribed target must be a partial table on the whole carrier")
        return _factor(self.later, values)


def realize_bridge(signature: BridgeSignature):
    if not signature.realizable():
        raise ValueError("impossible finite bridge signature")
    reports = (0, 1) if signature.report_total else (0, None)
    provenance = tuple(ProvenanceLink(0 if signature.linkage_verified else 1, 0, x, x, x) for x in range(2)) if signature.linkage_provided else (None, None)
    return SelfReferenceModel(
        0, 2, 2, 2, (0, 1), (0, 1), reports, provenance,
        (0, 1) if signature.report_stable else (1, 0),
        (1, 0), (1, 0) if signature.comparison_success else (0, 1),
        frozenset({(0, 0), (1, 1)}),
        frozenset({(0, 0), (0, 1), (1, 0), (1, 1)}) if signature.comparison_available else None,
    )


def self_witness_payload(model: SelfReferenceModel, x: int):
    if not model.point(x)[2]:
        raise ValueError("self-witnessing needs a verified reflexive report link")
    return {"observer_id": model.observer_id, "state_index": x, "target_component": "accessible_self_state", "self_state": model.sigma[x], "report": model.reports[x]}


def verify_self_witness_event(model: SelfReferenceModel, x: int, observation: AcceptedObservation, reaccessed_mark: object):
    """Check an actual accepted E-observation targeting the same observer state.

    This explicitly adds the accepted-observation and independent re-access
    prerequisites of CH14-D01. Structural self-model linkage alone is insufficient.
    """
    if not isinstance(model, SelfReferenceModel):
        return Refused(RefusalCode.INVALID_INPUT, "self-witness model has the wrong type")
    if not isinstance(observation, AcceptedObservation):
        return Refused(RefusalCode.MISSING_OBSERVATION, "self-witnessing requires an accepted E-observation")
    checked = classify_observation(observation.receipt)
    if isinstance(checked, Refused):
        return checked
    try:
        expected = self_witness_payload(model, x)
        expected_digest = payload_digest(expected)
        mark_digest = payload_digest(observation.registration.mark)
    except (TypeError, ValueError):
        return Refused(RefusalCode.INVALID_INPUT, "self-witness target/provenance is unavailable")
    if observation.registration.carrier_id != f"self:{model.observer_id}" or mark_digest != expected_digest:
        return Refused(RefusalCode.DIGEST_MISMATCH, "accepted observation does not target this reflexive state/report")
    replay = verify_witness(observation.witness, reaccessed_mark)
    if isinstance(replay, Refused):
        return replay
    return Accepted(True)
