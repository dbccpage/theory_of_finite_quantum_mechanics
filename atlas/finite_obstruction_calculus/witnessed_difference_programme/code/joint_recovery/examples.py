"""Declared joint supports; none is a measured noise distribution."""

from fractions import Fraction as F

from .reference import Channel, Model, Segment


def channels():
    return tuple(Channel(name, "raw", "m", F(1), F(0), F(1)) for name in ("A", "B"))


def shared_error() -> Model:
    return Model(
        channels(),
        tuple(
            Segment(str(x), "*", str(x), "m", F(-1), F(1), (F(1), F(1)), (F(x), F(-x)))
            for x in (0, 1)
        ),
    )


def isolated_collision() -> Model:
    return Model(
        channels(),
        (
            Segment("0", "*", "0", "m", F(0), F(1), (F(1), F(1)), (F(0), F(0))),
            Segment("1", "*", "1", "m", F(0), F(1), (F(1), F(2)), (F(0), F(-1, 3))),
        ),
    )


def parity_points() -> Model:
    return Model(
        channels(),
        tuple(
            Segment(str(x ^ y), "*", str(x ^ y), "m", F(0), F(0), (F(1), F(1)), (F(x), F(y)))
            for x in (0, 1)
            for y in (0, 1)
        ),
    )


def isolated_cost_peak() -> Model:
    return Model(
        channels() + (Channel("C", "raw", "m", F(1), F(0), F(3)),),
        (
            Segment("0", "*", "0", "m", F(-1), F(1), (F(1), F(1), F(1)), (F(0), F(0), F(0))),
            Segment("1", "*", "1", "m", F(-1), F(1), (F(1), F(-1), F(1)), (F(0), F(0), F(10))),
        ),
    )
