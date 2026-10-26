"""Exact report checking and finite reduction; no physical calibration inference.

The caller supplies the trusted model separately from a report and an answer
proposal. Interval supports are outer bounds; cost certificates describe their
full ideal Cartesian product, without the raw parser's resource bounds. They
describe physical optimality only when that product is realizable. Model admission
does not guarantee that every ideal reading has an admitted raw encoding. Cost
proposal and verification reuse finite_observation unchanged.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import product

from finite_observation import solver

COST_DOMAIN = "ideal_calibrated_interval_product"


@dataclass(frozen=True)
class Channel:
    name: str
    raw_unit: str
    unit: str
    gain: Fraction
    offset: Fraction
    intervals: tuple[tuple[Fraction, Fraction], ...]
    price: Fraction


@dataclass(frozen=True)
class Model:
    states: tuple[str, ...]
    visible: tuple[str, ...]
    answers: tuple[str, ...]
    channels: tuple[Channel, ...]


@dataclass(frozen=True)
class Evaluation:
    status: str
    compatible: tuple[str, ...] = ()


def _fraction(value: object) -> None:
    if type(value) is not Fraction:
        raise TypeError("exact Fraction required")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > 256:
        raise ValueError("rational bit cap exceeded")


def validate(model: Model) -> None:
    if type(model) is not Model:
        raise TypeError("expected Model")
    if type(model.states) is not tuple or not 1 <= len(model.states) <= 10:
        raise ValueError("candidate count must be between 1 and 10")
    n = len(model.states)
    for labels in (model.states, model.visible, model.answers):
        if type(labels) is not tuple or len(labels) != n or any(type(s) is not str for s in labels):
            raise TypeError("aligned immutable string tables required")
    if len(set(model.states)) != n:
        raise ValueError("duplicate state")
    if type(model.channels) is not tuple or len(model.channels) > 12:
        raise ValueError("immutable channel shelf of at most 12 required")
    names = []
    for channel in model.channels:
        if type(channel) is not Channel:
            raise TypeError("expected Channel")
        for label in (channel.name, channel.raw_unit, channel.unit):
            if type(label) is not str or not label:
                raise TypeError("nonempty channel and unit labels required")
        names.append(channel.name)
        for value in (channel.gain, channel.offset, channel.price):
            _fraction(value)
        if channel.gain == 0 or channel.price <= 0:
            raise ValueError("nonzero gain and positive price required")
        if type(channel.intervals) is not tuple or len(channel.intervals) != n:
            raise TypeError("aligned immutable interval table required")
        for interval in channel.intervals:
            if type(interval) is not tuple or len(interval) != 2:
                raise TypeError("immutable endpoint pair required")
            for value in interval:
                _fraction(value)
            if interval[0] > interval[1]:
                raise ValueError("reversed interval")
    if len(set(names)) != len(names):
        raise ValueError("duplicate channel")


def _json_fraction(value: object) -> str:
    if type(value) is not Fraction:
        raise TypeError("model digest admits Fraction only")
    return str(value)


def model_hash(model: Model) -> str:
    validate(model)
    data = json.dumps(asdict(model), default=_json_fraction, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def _parse_fraction(value: object) -> Fraction:
    if (
        type(value) is not str
        or len(value) > 160
        or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is None
    ):
        raise ValueError("canonical rational string required")
    result = Fraction(value)
    _fraction(result)
    if str(result) != value:
        raise ValueError("noncanonical rational")
    return result


def _support(channel: Channel, value: Fraction) -> tuple[int, ...]:
    return tuple(x for x, (low, high) in enumerate(channel.intervals) if low <= value <= high)


def _compatible(model: Model, report: object) -> tuple[int, ...]:
    if type(report) is not dict or set(report) != {"model_sha256", "visible", "readings"}:
        raise ValueError("report schema mismatch")
    if (
        type(report["model_sha256"]) is not str
        or report["model_sha256"] != model_hash(model)
        or type(report["visible"]) is not str
    ):
        raise ValueError("report model or visible label mismatch")
    readings = report["readings"]
    if type(readings) is not list or len(readings) > len(model.channels):
        raise ValueError("invalid reading list")
    channels = {channel.name: channel for channel in model.channels}
    candidates = {x for x, p in enumerate(model.visible) if p == report["visible"]}
    seen = set()
    for row in readings:
        if type(row) is not dict or set(row) != {"channel", "raw_unit", "value"}:
            raise ValueError("reading schema mismatch")
        name = row["channel"]
        if type(name) is not str or name not in channels or name in seen:
            raise ValueError("unknown or repeated channel")
        seen.add(name)
        channel = channels[name]
        if type(row["raw_unit"]) is not str or row["raw_unit"] != channel.raw_unit:
            raise ValueError("raw unit mismatch")
        value = channel.gain * _parse_fraction(row["value"]) + channel.offset
        candidates.intersection_update(_support(channel, value))
    return tuple(sorted(candidates))


def evaluate(model: Model, report: object, proposed_answer: object) -> Evaluation:
    """Check one bounded raw report; INVALID_REPORT includes encoding-cap refusal.

    A refused report says nothing about ideal-product recovery costs. This returns
    no permission to act on the answer.
    """
    validate(model)
    try:
        candidates = _compatible(model, report)
    except (ValueError, TypeError):
        return Evaluation("INVALID_REPORT")
    labels = tuple(model.states[x] for x in candidates)
    if not candidates:
        return Evaluation("INCONSISTENT")
    answers = {model.answers[x] for x in candidates}
    if len(answers) != 1:
        return Evaluation("ABSTAIN", labels)
    if type(proposed_answer) is not str or proposed_answer not in answers:
        return Evaluation("INVALID_PROPOSAL", labels)
    return Evaluation("VERIFIED", labels)


def alphabet(channel: Channel) -> tuple[tuple[int, ...], ...]:
    """All nonempty membership signatures, including singleton endpoint cells."""
    endpoints = sorted({p for interval in channel.intervals for p in interval})
    representatives = endpoints + [(a + b) / 2 for a, b in zip(endpoints, endpoints[1:])]
    return tuple(sorted({s for value in representatives if (s := _support(channel, value))}))


def finite_lift(model: Model) -> solver.Instance:
    """Encode the full rectangular report model; refuse before exceeding the solver cap."""
    validate(model)
    alphabets = tuple(alphabet(channel) for channel in model.channels)
    worlds = []
    for x in range(len(model.states)):
        options = tuple(tuple(s for s in symbols if x in s) for symbols in alphabets)
        count = 1
        for values in options:
            count *= len(values)
        if len(worlds) + count > solver.MAX_STATES:
            raise ValueError("finite lift exceeds the reference solver state cap")
        worlds.extend((x, reports) for reports in product(*options))
    instance = solver.Instance(
        states=tuple(str(j) for j in range(len(worlds))),
        visible=tuple(model.visible[x] for x, _ in worlds),
        query=tuple(model.answers[x] for x, _ in worlds),
        instruments=tuple(
            solver.Instrument(
                channel.name, tuple(str(reports[i]) for _, reports in worlds), channel.price
            )
            for i, channel in enumerate(model.channels)
        ),
    )
    solver.validate_instance(instance)
    return instance


def propose_cost(model: Model) -> dict:
    """Certify ideal-product costs, not feasibility through the bounded raw API."""
    return {
        "model_sha256": model_hash(model),
        "cost_domain": COST_DOMAIN,
        "finite_certificate": solver.solve(finite_lift(model)),
    }


def verify_cost(model: Model, certificate: object) -> solver.Verification:
    """Replay a model-bound ideal-product certificate, including its scope tag."""
    validate(model)
    if (
        type(certificate) is not dict
        or set(certificate) != {"model_sha256", "cost_domain", "finite_certificate"}
        or type(certificate["model_sha256"]) is not str
        or certificate["model_sha256"] != model_hash(model)
    ):
        return solver.Verification(False, "MODEL_MISMATCH", "wrong calibrated model")
    if type(certificate["cost_domain"]) is not str or certificate["cost_domain"] != COST_DOMAIN:
        return solver.Verification(False, "COST_DOMAIN_MISMATCH", "ideal product required")
    return solver.verify(finite_lift(model), certificate["finite_certificate"])
