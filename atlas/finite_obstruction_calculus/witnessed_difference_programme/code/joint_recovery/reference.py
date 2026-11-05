"""Joint report admission and finite cost witnesses for affine segments.

Every segment uses one latent parameter across all coordinates. The supplied
union of segments is the model, not an inferred calibration or distribution.
Cost arithmetic and certificate checking belong to the existing finite reference
solver; this module constructs its input and checks report compatibility.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations

from calibrated_recovery import bridge as calibrated
from finite_observation import solver


@dataclass(frozen=True)
class Channel:
    name: str
    raw_unit: str
    unit: str
    raw_gain: Fraction
    raw_offset: Fraction
    price: Fraction


@dataclass(frozen=True)
class Segment:
    state: str
    visible: str
    answer: str
    parameter_unit: str
    lower: Fraction
    upper: Fraction
    slopes: tuple[Fraction, ...]
    offsets: tuple[Fraction, ...]


@dataclass(frozen=True)
class Model:
    channels: tuple[Channel, ...]
    segments: tuple[Segment, ...]
    cost_unit: str = "query_cost"


World = tuple[str, tuple[Fraction, ...]]


def validate(model: Model) -> None:
    if type(model) is not Model:
        raise TypeError("expected joint Model")
    if type(model.cost_unit) is not str or not model.cost_unit:
        raise TypeError("one nonempty common cost-unit label required")
    if type(model.channels) is not tuple or len(model.channels) > solver.MAX_INSTRUMENTS:
        raise ValueError("immutable channel shelf exceeds the reference cap")
    if type(model.segments) is not tuple or not 1 <= len(model.segments) <= solver.MAX_STATES:
        raise ValueError("between one and ten immutable segments required")
    names = []
    for channel in model.channels:
        if type(channel) is not Channel:
            raise TypeError("expected Channel")
        for label in (channel.name, channel.raw_unit, channel.unit):
            if type(label) is not str or not label:
                raise TypeError("nonempty channel and unit labels required")
        names.append(channel.name)
        for value in (channel.raw_gain, channel.raw_offset, channel.price):
            calibrated._fraction(value)
        if channel.raw_gain == 0 or channel.price <= 0:
            raise ValueError("nonzero raw conversion and positive price required")
    if len(set(names)) != len(names):
        raise ValueError("duplicate channel")
    metadata = {}
    for segment in model.segments:
        if type(segment) is not Segment:
            raise TypeError("expected Segment")
        for label in (segment.state, segment.visible, segment.answer, segment.parameter_unit):
            if type(label) is not str:
                raise TypeError("state, report, answer and parameter-unit labels must be strings")
        if not segment.state or not segment.parameter_unit:
            raise ValueError("nonempty state and parameter-unit labels required")
        entry = (segment.visible, segment.answer)
        if segment.state in metadata and metadata[segment.state] != entry:
            raise ValueError("one state has conflicting free reports or answers")
        metadata[segment.state] = entry
        for value in (segment.lower, segment.upper):
            calibrated._fraction(value)
        if segment.lower > segment.upper:
            raise ValueError("reversed parameter interval")
        for row in (segment.slopes, segment.offsets):
            if type(row) is not tuple or len(row) != len(model.channels):
                raise TypeError("immutable affine rows must match the channel count")
            for value in row:
                calibrated._fraction(value)
        if any(slope == 0 for slope in segment.slopes):
            raise ValueError("finite reduction requires every segment slope to be nonzero")


def model_hash(model: Model) -> str:
    validate(model)
    encoded = json.dumps(
        asdict(model), default=calibrated._json_fraction, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(encoded.encode()).hexdigest()


def _readings(model: Model, report: object) -> tuple[str, tuple[tuple[int, Fraction], ...]]:
    if type(report) is not dict or set(report) != {"model_sha256", "visible", "readings"}:
        raise ValueError("report schema mismatch")
    if (
        type(report["model_sha256"]) is not str
        or report["model_sha256"] != model_hash(model)
        or type(report["visible"]) is not str
    ):
        raise ValueError("report model or visible label mismatch")
    rows = report["readings"]
    if type(rows) is not list or len(rows) > len(model.channels):
        raise ValueError("invalid reading list")
    names = {channel.name: i for i, channel in enumerate(model.channels)}
    seen = set()
    parsed = []
    for row in rows:
        if type(row) is not dict or set(row) != {"channel", "raw_unit", "value"}:
            raise ValueError("reading schema mismatch")
        name = row["channel"]
        if type(name) is not str or name not in names or name in seen:
            raise ValueError("unknown or repeated channel")
        seen.add(name)
        i = names[name]
        channel = model.channels[i]
        if type(row["raw_unit"]) is not str or row["raw_unit"] != channel.raw_unit:
            raise ValueError("raw unit mismatch")
        value = channel.raw_gain * calibrated._parse_fraction(row["value"]) + channel.raw_offset
        parsed.append((i, value))
    return report["visible"], tuple(parsed)


def _matches(segment: Segment, readings: tuple[tuple[int, Fraction], ...]) -> bool:
    if not readings:
        return True
    i, value = readings[0]
    parameter = (value - segment.offsets[i]) / segment.slopes[i]
    return segment.lower <= parameter <= segment.upper and all(
        segment.slopes[j] * parameter + segment.offsets[j] == observed for j, observed in readings
    )


def evaluate(model: Model, report: object, proposed_answer: object) -> calibrated.Evaluation:
    """Check an answer using a common latent parameter; return no action authority."""
    validate(model)
    try:
        visible, readings = _readings(model, report)
    except (ValueError, TypeError):
        return calibrated.Evaluation("INVALID_REPORT")
    compatible = {
        segment.state: segment.answer
        for segment in model.segments
        if segment.visible == visible and _matches(segment, readings)
    }
    if not compatible:
        return calibrated.Evaluation("INCONSISTENT")
    labels = tuple(compatible)
    answers = set(compatible.values())
    if len(answers) != 1:
        return calibrated.Evaluation("ABSTAIN", labels)
    if type(proposed_answer) is not str or proposed_answer not in answers:
        return calibrated.Evaluation("INVALID_PROPOSAL", labels)
    return calibrated.Evaluation("VERIFIED", labels)


def _world(segment: Segment, parameter: Fraction) -> World:
    return segment.state, tuple(a * parameter + b for a, b in zip(segment.slopes, segment.offsets))


def _fiber(segments: tuple[Segment, ...], i: int, value: Fraction) -> tuple[World, ...]:
    worlds = {}
    for segment in segments:
        parameter = (value - segment.offsets[i]) / segment.slopes[i]
        if segment.lower <= parameter <= segment.upper:
            worlds[_world(segment, parameter)] = None
    return tuple(worlds)


def _image(segment: Segment, i: int) -> tuple[Fraction, Fraction]:
    values = (
        segment.slopes[i] * segment.lower + segment.offsets[i],
        segment.slopes[i] * segment.upper + segment.offsets[i],
    )
    return min(values), max(values)


def _prediction(segment: Segment, i: int, j: int) -> tuple[Fraction, Fraction]:
    slope = segment.slopes[j] / segment.slopes[i]
    return slope, segment.offsets[j] - slope * segment.offsets[i]


def _collision(model: Model) -> tuple[World, World] | None:
    for left, right in combinations(model.segments, 2):
        if left.visible != right.visible or left.answer == right.answer:
            continue
        if not model.channels:
            return _world(left, left.lower), _world(right, right.lower)
        l0, l1 = _image(left, 0)
        r0, r1 = _image(right, 0)
        low, high = max(l0, r0), min(l1, r1)
        if low > high:
            continue
        root = None
        compatible = True
        for j in range(len(model.channels)):
            a, b = _prediction(left, 0, j)
            c, d = _prediction(right, 0, j)
            if a == c:
                if b != d:
                    compatible = False
                    break
            else:
                value = (d - b) / (a - c)
                if root is not None and root != value:
                    compatible = False
                    break
                root = value
        value = low if root is None else root
        if compatible and low <= value <= high:
            worlds = _fiber((left, right), 0, value)
            assert len(worlds) == 2 and worlds[0][1] == worlds[1][1]
            return worlds[0], worlds[1]
    return None


def _critical_values(segments: tuple[Segment, ...], i: int, width: int) -> tuple[Fraction, ...]:
    points = {value for segment in segments for value in _image(segment, i)}
    for left, right in combinations(segments, 2):
        l0, l1 = _image(left, i)
        r0, r1 = _image(right, i)
        low, high = max(l0, r0), min(l1, r1)
        if low > high:
            continue
        for j in range(width):
            a, b = _prediction(left, i, j)
            c, d = _prediction(right, i, j)
            if a != c:
                root = (d - b) / (a - c)
                if low <= root <= high:
                    points.add(root)
    return tuple(sorted(points))


def _instance(
    model: Model, worlds: tuple[World, ...], remaining: tuple[int, ...]
) -> solver.Instance:
    metadata = {segment.state: (segment.visible, segment.answer) for segment in model.segments}
    instance = solver.Instance(
        tuple(str(i) for i in range(len(worlds))),
        tuple(metadata[state][0] for state, _ in worlds),
        tuple(metadata[state][1] for state, _ in worlds),
        tuple(
            solver.Instrument(
                model.channels[j].name,
                tuple(str(values[j]) for _, values in worlds),
                model.channels[j].price,
            )
            for j in remaining
        ),
    )
    solver.validate_instance(instance)
    return instance


def conditional_instance(model: Model, i: int, value: Fraction, visible: str) -> solver.Instance:
    """Exact remaining problem; apply the report cap before raw calibration."""
    validate(model)
    if type(i) is not int or not 0 <= i < len(model.channels) or type(visible) is not str:
        raise ValueError("invalid channel index or free report")
    if type(value) is not Fraction:
        raise TypeError("exact Fraction required")
    channel = model.channels[i]
    # Calibration can enlarge a valid raw rational beyond 256 bits. Check
    # the same input domain as _readings, not the derived coordinate size.
    calibrated._fraction((value - channel.raw_offset) / channel.raw_gain)
    segments = tuple(segment for segment in model.segments if segment.visible == visible)
    worlds = _fiber(segments, i, value)
    if not worlds:
        raise ValueError("inconsistent history")
    return _instance(model, worlds, tuple(j for j in range(len(model.channels)) if j != i))


def sample_worlds(model: Model) -> tuple[World, ...]:
    """Construct the complete critical-cell cost witness; never silently truncate it."""
    validate(model)
    collision = _collision(model)
    if collision is not None:
        return collision
    worlds: dict[World, None] = {}

    def admit(world: World) -> None:
        if world not in worlds:
            if len(worlds) == solver.MAX_STATES:
                raise ValueError("joint witness exceeds the existing finite solver state cap")
            worlds[world] = None

    for segment in model.segments:
        admit(_world(segment, segment.lower))
    metadata = {segment.state: segment.answer for segment in model.segments}
    for visible in sorted({segment.visible for segment in model.segments}):
        segments = tuple(segment for segment in model.segments if segment.visible == visible)
        if len({segment.answer for segment in segments}) == 1:
            continue
        for i in range(len(model.channels)):
            endpoints = _critical_values(segments, i, len(model.channels))
            representatives = sorted(
                set(endpoints) | {(a + b) / 2 for a, b in zip(endpoints, endpoints[1:])}
            )
            for value in representatives:
                fiber = _fiber(segments, i, value)
                if len({metadata[state] for state, _ in fiber}) > 1:
                    for world in fiber:
                        admit(world)
    return tuple(worlds)


def finite_instance(model: Model) -> solver.Instance:
    return _instance(model, sample_worlds(model), tuple(range(len(model.channels))))


def propose_cost(model: Model) -> dict:
    return {
        "model_sha256": model_hash(model),
        "finite_certificate": solver.solve(finite_instance(model)),
    }


def verify_cost(model: Model, certificate: object) -> solver.Verification:
    """Reconstruct the critical witness and replay the submitted finite certificate."""
    validate(model)
    if (
        type(certificate) is not dict
        or set(certificate) != {"model_sha256", "finite_certificate"}
        or type(certificate["model_sha256"]) is not str
        or certificate["model_sha256"] != model_hash(model)
    ):
        return solver.Verification(False, "MODEL_MISMATCH", "wrong joint-support model")
    return solver.verify(finite_instance(model), certificate["finite_certificate"])
