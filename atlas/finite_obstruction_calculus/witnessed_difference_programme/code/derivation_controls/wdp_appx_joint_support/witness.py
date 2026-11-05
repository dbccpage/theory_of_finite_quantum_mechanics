"""Shared-noise joint reports on the declared two-segment scope.

Candidates are {0, 1}, the free report is *, and A and B each cost 1.
Costs are exact Fractions. The ten-world list is one carrier. The marginal
interval product is another. Neither result is a continuum limit.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

PRICE = Fraction(1)
OFFSETS = {0: (Fraction(0), Fraction(0)), 1: (Fraction(1), Fraction(-1))}
PLUS = ((Fraction(-1), Fraction(1)), (Fraction(0), Fraction(2)))
MINUS = ((Fraction(-1), Fraction(1)), (Fraction(-2), Fraction(0)))


def _vector(answer: int, parameter: Fraction) -> tuple[Fraction, Fraction]:
    if type(answer) is not int or type(parameter) is not Fraction:
        raise TypeError("exact int answer and Fraction parameter required")
    if answer not in OFFSETS or parameter < -1 or parameter > 1:
        raise ValueError("outside the declared segment")
    return (parameter + answer, parameter - answer)


def _difference_form(answer: int) -> tuple[Fraction, Fraction]:
    if type(answer) is not int or answer not in OFFSETS:
        raise TypeError("exact candidate required")
    slope = Fraction(1) - Fraction(1)
    constant = Fraction(answer) - Fraction(-answer)
    return slope, constant


def _on_segment(answer: int, point: tuple[Fraction, Fraction]) -> bool:
    left, right = point
    if type(left) is not Fraction or type(right) is not Fraction:
        raise TypeError("exact Fraction coordinates required")
    slope, constant = _difference_form(answer)
    if slope != 0 or left - right != constant or constant != Fraction(2) * answer:
        return False
    parameter = right + answer
    return Fraction(-1) <= parameter <= Fraction(1) and left == parameter + answer


def _admitted(readings: dict[str, Fraction]) -> tuple[int, ...]:
    if any(name not in ("A", "B") for name in readings):
        raise ValueError("unknown instrument")
    for value in readings.values():
        if type(value) is not Fraction:
            raise TypeError("exact Fraction readings required")
    found = []
    for answer in (0, 1):
        if not readings:
            found.append(answer)
            continue
        first = next(name for name in ("A", "B") if name in readings)
        index = 0 if first == "A" else 1
        parameter = readings[first] - OFFSETS[answer][index]
        if parameter < -1 or parameter > 1:
            continue
        predicted = _vector(answer, parameter)
        named = {"A": predicted[0], "B": predicted[1]}
        if all(readings[name] == named[name] for name in readings):
            found.append(answer)
    return tuple(found)


def _status(answers: tuple[int, ...], proposed: int) -> str:
    if not answers:
        return "INCONSISTENT"
    if len(answers) != 1:
        return "ABSTAIN"
    if proposed != answers[0]:
        return "INVALID_PROPOSAL"
    return "VERIFIED"


def _intervals_admit(point: tuple[Fraction, Fraction]) -> tuple[int, ...]:
    left, right = point
    if type(left) is not Fraction or type(right) is not Fraction:
        raise TypeError("exact Fraction coordinates required")
    found = []
    for answer in (0, 1):
        low_a, high_a = PLUS[answer]
        low_b, high_b = MINUS[answer]
        if low_a <= left <= high_a and low_b <= right <= high_b:
            found.append(answer)
    return tuple(found)


def _enclosure_status(point: tuple[Fraction, Fraction], proposed: int) -> str:
    return _status(_intervals_admit(point), proposed)


def _image(answer: int, index: int) -> tuple[Fraction, Fraction]:
    ends = (_vector(answer, Fraction(-1))[index], _vector(answer, Fraction(1))[index])
    return min(ends), max(ends)


def _prediction(answer: int, source: int, target: int) -> tuple[Fraction, Fraction]:
    offsets = OFFSETS[answer]
    slope = Fraction(1)
    return slope, offsets[target] - slope * offsets[source]


def _critical(index: int) -> tuple[Fraction, ...]:
    points = set()
    for answer in (0, 1):
        low, high = _image(answer, index)
        points.add(low)
        points.add(high)
    low_0, high_0 = _image(0, index)
    low_1, high_1 = _image(1, index)
    low, high = max(low_0, low_1), min(high_0, high_1)
    if low <= high:
        for other in (0, 1):
            left_slope, left_intercept = _prediction(0, index, other)
            right_slope, right_intercept = _prediction(1, index, other)
            if left_slope != right_slope:
                root = (right_intercept - left_intercept) / (left_slope - right_slope)
                if low <= root <= high:
                    points.add(root)
    return tuple(sorted(points))


def _fiber(index: int, value: Fraction) -> tuple[tuple[int, tuple[Fraction, Fraction]], ...]:
    found = []
    for answer in (0, 1):
        parameter = value - OFFSETS[answer][index]
        if Fraction(-1) <= parameter <= Fraction(1):
            world = (answer, _vector(answer, parameter))
            if world not in found:
                found.append(world)
    return tuple(found)


def _carrier() -> tuple[tuple[int, tuple[Fraction, Fraction]], ...]:
    worlds: list[tuple[int, tuple[Fraction, Fraction]]] = []

    def admit(world: tuple[int, tuple[Fraction, Fraction]]) -> None:
        if world in worlds:
            return
        if len(worlds) == 10:
            raise RuntimeError("joint witness exceeds the ten-world carrier")
        worlds.append(world)

    for answer in (0, 1):
        admit((answer, _vector(answer, Fraction(-1))))
    for index in (0, 1):
        endpoints = _critical(index)
        mids = [(left + right) / 2 for left, right in zip(endpoints, endpoints[1:])]
        for value in sorted(set(endpoints) | set(mids)):
            fiber = _fiber(index, value)
            if len({answer for answer, _ in fiber}) > 1:
                for world in fiber:
                    admit(world)
    if len(worlds) != 10 or len({vector for _, vector in worlds}) != 10:
        raise RuntimeError("sampler did not return ten distinct worlds")
    for answer, vector in worlds:
        if not _on_segment(answer, vector) or _on_segment(1 - answer, vector):
            raise RuntimeError("carrier world is not on exactly one segment")
    return tuple(worlds)


def _robust(
    records: tuple[tuple[int, tuple], ...], prices: tuple[Fraction, ...]
) -> tuple[Fraction | None, Fraction | None, tuple[tuple[int, Fraction, bool], ...]]:
    if any(type(price) is not Fraction or price <= 0 for price in prices):
        raise TypeError("positive Fraction prices required")
    width = len(prices)
    pairs = tuple(
        (i, j)
        for i, j in combinations(range(len(records)), 2)
        if records[i][0] != records[j][0]
    )
    table = []
    best: tuple[Fraction, int] | None = None
    for mask in range(1 << width):
        cost = sum((prices[k] for k in range(width) if mask & (1 << k)), Fraction(0))
        sufficient = all(
            any(mask & (1 << k) and records[i][1][k] != records[j][1][k] for k in range(width))
            for i, j in pairs
        )
        table.append((mask, cost, sufficient))
        if sufficient and (best is None or (cost, mask) < (best[0], best[1])):
            best = (cost, mask)
    values: list[Fraction | None] = []
    size = len(records)
    for mask in range(1 << size):
        members = [i for i in range(size) if mask & (1 << i)]
        if len({records[i][0] for i in members}) <= 1:
            values.append(Fraction(0))
            continue
        options = []
        for k, price in enumerate(prices):
            groups: dict[object, int] = {}
            for i in members:
                groups[records[i][1][k]] = groups.get(records[i][1][k], 0) | (1 << i)
            if len(groups) < 2:
                continue
            children = [values[child] for child in groups.values()]
            if all(child is not None for child in children):
                options.append(price + max(children))
        values.append(min(options) if options else None)
    fixed = None if best is None else best[0]
    adaptive = values[(1 << size) - 1]
    if fixed is not None and (adaptive is None or adaptive > fixed):
        raise RuntimeError("adaptive value exceeds the separating suite")
    if fixed is None and adaptive is not None:
        raise RuntimeError("adaptive optimum cannot undercut an infeasible fixed problem")
    return fixed, adaptive, tuple(table)


def _support(intervals: tuple[tuple[Fraction, Fraction], ...], value: Fraction) -> tuple[int, ...]:
    return tuple(i for i, (low, high) in enumerate(intervals) if low <= value <= high)


def _alphabet(intervals: tuple[tuple[Fraction, Fraction], ...]) -> tuple[tuple[int, ...], ...]:
    endpoints = sorted({bound for interval in intervals for bound in interval})
    representatives = endpoints + [(left + right) / 2 for left, right in zip(endpoints, endpoints[1:])]
    return tuple(sorted({sig for value in representatives if (sig := _support(intervals, value))}))


def _product_worlds() -> tuple[tuple[int, tuple[tuple[int, ...], tuple[int, ...]]], ...]:
    alphabets = (_alphabet(PLUS), _alphabet(MINUS))
    worlds = []
    for answer in (0, 1):
        options = tuple(tuple(sig for sig in symbols if answer in sig) for symbols in alphabets)
        worlds.extend((answer, reports) for reports in product(*options))
    if len(worlds) > 10:
        raise RuntimeError("interval product exceeds the ten-world solver carrier")
    return tuple(worlds)


def _segment_optima() -> tuple[Fraction, Fraction]:
    forms = tuple(_difference_form(answer) for answer in (0, 1))
    if any(slope != 0 or constant != Fraction(2) * answer for answer, (slope, constant) in zip((0, 1), forms)):
        raise RuntimeError("pointwise difference is not 2x on these segments")
    if forms[0][1] == forms[1][1]:
        raise RuntimeError("complete reports do not separate the two segments")
    collisions = (
        (_vector(0, Fraction(0)), _vector(1, Fraction(-1)), 0),
        (_vector(0, Fraction(-1)), _vector(1, Fraction(0)), 1),
    )
    for left, right, index in collisions:
        if left[index] != right[index] or left[1 - index] == right[1 - index]:
            raise RuntimeError("exhibited reading does not leave both answers")
        if _admitted({"A": left[0], "B": left[1]}) != (0,) or _admitted({"A": right[0], "B": right[1]}) != (1,):
            raise RuntimeError("collision points are not jointly feasible")
    if _admitted({"A": Fraction(0)}) != (0, 1) or _admitted({"B": Fraction(-1)}) != (0, 1):
        raise RuntimeError("single-instrument collision missing")
    # Both instruments determine (z_A - z_B) / 2. Each one-instrument collision
    # still costs the other instrument. Empty and singleton suites fail.
    return PRICE + PRICE, PRICE + PRICE


def witness() -> dict[str, object]:
    worlds = _carrier()
    present = {vector: answer for answer, vector in worlds}
    for answer, vector in (
        (0, (Fraction(0), Fraction(0))),
        (1, (Fraction(0), Fraction(-2))),
        (0, (Fraction(-1), Fraction(-1))),
        (1, (Fraction(1), Fraction(-1))),
    ):
        if present.get(vector) != answer:
            raise RuntimeError("shared-noise control point missing from the carrier")
    carrier_fixed, carrier_adaptive, carrier_table = _robust(worlds, (PRICE, PRICE))
    segment_fixed, segment_adaptive = _segment_optima()
    # Same integers on this scope only: enumeration on the carrier, identity on the segments.
    if (carrier_fixed, carrier_adaptive) != (segment_fixed, segment_adaptive):
        raise RuntimeError("carrier enumeration and segment identity disagree")
    instrument_fixed = tuple(row[1] if row[2] else None for row in carrier_table if row[0] in (1, 2))
    product_worlds = _product_worlds()
    product_fixed, product_adaptive, product_table = _robust(product_worlds, (PRICE, PRICE))
    if carrier_table[3][2] is not True or product_table[3][2] is not False:
        raise RuntimeError("joint suite and product suite were not distinguished")
    sound_upper_bound = carrier_table[3][1]
    point_00 = (Fraction(0), Fraction(0))
    point_01 = (Fraction(0), Fraction(1))
    point_0_m2 = (Fraction(0), Fraction(-2))
    joint_00 = _admitted({"A": point_00[0], "B": point_00[1]})
    joint_01 = _admitted({"A": point_01[0], "B": point_01[1]})
    joint_0_m2 = _admitted({"A": point_0_m2[0], "B": point_0_m2[1]})
    joint_a0 = _admitted({"A": Fraction(0)})
    return {
        "worlds": worlds,
        "carrier_fixed": carrier_fixed,
        "carrier_adaptive": carrier_adaptive,
        "carrier_fixed_table": carrier_table,
        "segment_fixed": segment_fixed,
        "segment_adaptive": segment_adaptive,
        "identity_slope": _difference_form(0)[0],
        "identity_constants": (_difference_form(0)[1], _difference_form(1)[1]),
        "instrument_fixed": instrument_fixed,
        "joint_admits_A0": joint_a0,
        "joint_admits_00": joint_00,
        "joint_admits_0_m2": joint_0_m2,
        "joint_admits_01": joint_01,
        "joint_status_A0": _status(joint_a0, 0),
        "joint_status_00_answer_0": _status(joint_00, 0),
        "joint_status_00_answer_1": _status(joint_00, 1),
        "joint_status_0_m2_answer_1": _status(joint_0_m2, 1),
        "joint_status_01": _status(joint_01, 0),
        "product_world_count": len(product_worlds),
        "product_fixed": product_fixed,
        "product_adaptive": product_adaptive,
        "product_fixed_table": product_table,
        "product_admits_00": _intervals_admit(point_00),
        "product_status_00": _enclosure_status(point_00, 0),
        "product_admits_01": _intervals_admit(point_01),
        "product_status_01_answer_0": _enclosure_status(point_01, 0),
        "sound_upper_bound": sound_upper_bound,
        "upper_bound_equals_carrier_optima": carrier_fixed == sound_upper_bound and carrier_adaptive == sound_upper_bound,
        "product_price_is_optimum": product_fixed == product_table[3][1],
    }


def refuse_coordinate_enclosure(point: tuple[object, object], proposed: object) -> str:
    """Refuse a marginal certificate the declared segments do not admit."""
    if any(type(coord) is float for coord in point) or type(proposed) is float:
        raise TypeError("float tolerance is not a claim")
    if type(point) is not tuple or len(point) != 2 or any(type(coord) is not Fraction for coord in point):
        raise TypeError("exact Fraction coordinates required")
    if type(proposed) is not int:
        raise TypeError("exact int answer required")
    typed = (point[0], point[1])
    joint = _admitted({"A": typed[0], "B": typed[1]})
    outer = _intervals_admit(typed)
    if proposed in outer and proposed not in joint:
        raise ValueError("coordinate enclosure is not a realizable joint report")
    return _status(joint, proposed)
