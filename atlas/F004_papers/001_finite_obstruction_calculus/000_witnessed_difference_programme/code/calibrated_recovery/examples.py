"""Small exact instances for Appendix X; these are deterministic examples."""

from fractions import Fraction as F

from .bridge import Channel, Model


def separated(radius: F = F(1)) -> Model:
    values = ((0, 0, 10, 10), (0, 10, 0, 0), (0, 0, 0, 10))
    return Model(
        ("00", "01", "10", "11"),
        ("*",) * 4,
        ("00", "01", "10", "11"),
        tuple(
            Channel(
                name,
                "raw",
                "m",
                F(2),
                F(1),
                tuple((F(v) - radius, F(v) + radius) for v in row),
                F(price),
            )
            for name, row, price in zip(("A", "B", "C"), values, (1, 3, 3))
        ),
    )


def touching() -> Model:
    return Model(
        ("a", "b"),
        ("*", "*"),
        ("a", "b"),
        (Channel("M", "raw", "m", F(1), F(0), ((F(0), F(1)), (F(1), F(2))), F(1)),),
    )


def correlated_enclosure() -> Model:
    return Model(
        ("0", "1"),
        ("*", "*"),
        ("0", "1"),
        tuple(
            Channel(name, "raw", "m", F(1), F(0), bounds, F(1))
            for name, bounds in (
                ("plus", ((F(-1), F(1)), (F(0), F(2)))),
                ("minus", ((F(-1), F(1)), (F(-2), F(0)))),
            )
        ),
    )
