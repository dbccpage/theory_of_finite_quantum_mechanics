"""Conditional remainder on the three-node carrier of Appendix M.4.

L=(4,6,8), x=1/L^2, Z at repetitions=2 and q=3. The degree-at-most-2
Lagrange weights at 0 are rational. Declared bounds b_i are external.
H vanishes on the nodes and H(0)=-1/36864, so the samples do not
determine those bounds. No continuum limit is stated.
"""

from __future__ import annotations

from fractions import Fraction

L_VALUES: tuple[int, int, int] = (4, 6, 8)
Z_VALUES: tuple[int, int, int] = (912, 33012, 973824)
REPETITIONS: int = 2
Q: int = 3

# External rationals. They instantiate the conditional law only.
_F = Fraction(1)
_C1 = Fraction(2, 3)
_C2 = Fraction(-4, 5)
_B = (Fraction(1, 5), Fraction(1, 7), Fraction(1, 11))


def nodes() -> tuple[Fraction, Fraction, Fraction]:
    return (Fraction(1, 16), Fraction(1, 36), Fraction(1, 64))


def lagrange_weights(xs: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    found: list[Fraction] = []
    for index, left in enumerate(xs):
        weight = Fraction(1)
        for other, right in enumerate(xs):
            if index == other:
                continue
            weight *= right / (left - right)
        found.append(weight)
    return (found[0], found[1], found[2])


def separable(value: Fraction, xs: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    image = Fraction(1)
    for node in xs:
        image *= value - node
    return image


def _fraction(value: int | Fraction, label: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"{label} is not an exact integer or rational")
    return Fraction(value)


def _triple(
    values: tuple[int | Fraction, int | Fraction, int | Fraction],
    label: str,
) -> tuple[Fraction, Fraction, Fraction]:
    if len(values) != 3:
        raise ValueError(f"three {label} values are required")
    return (
        _fraction(values[0], label),
        _fraction(values[1], label),
        _fraction(values[2], label),
    )


def carrier() -> tuple[
    tuple[Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction],
]:
    xs = nodes()
    if tuple(Fraction(1, length * length) for length in L_VALUES) != xs:
        raise RuntimeError("nodes are not 1/L^2")
    ws = lagrange_weights(xs)
    if ws != (Fraction(4, 15), Fraction(-81, 35), Fraction(64, 21)):
        raise RuntimeError("weights left (4/15, -81/35, 64/21)")
    return xs, ws


def projection_gap(
    level: int | Fraction,
    slope: int | Fraction,
    curvature: int | Fraction,
    remainders: tuple[int | Fraction, int | Fraction, int | Fraction],
) -> tuple[Fraction, Fraction]:
    """Return (hat f - f, sum w_i r_i). Moments (1,0,0) make them equal."""
    xs, ws = carrier()
    f = _fraction(level, "f")
    c1 = _fraction(slope, "c1")
    c2 = _fraction(curvature, "c2")
    rs = _triple(remainders, "r")
    images = tuple(f + c1 * x + c2 * x * x + r for x, r in zip(xs, rs, strict=True))
    hat = sum((w * g for w, g in zip(ws, images, strict=True)), Fraction(0))
    carried = sum((w * r for w, r in zip(ws, rs, strict=True)), Fraction(0))
    if hat - f != carried:
        raise RuntimeError("quadratic terms did not cancel")
    return hat - f, carried


def model_radius(
    bounds: tuple[int | Fraction, int | Fraction, int | Fraction],
) -> Fraction:
    """B = sum |w_i| b_i. Each b_i is an external nonnegative rational."""
    _, ws = carrier()
    total = Fraction(0)
    for weight, bound in zip(ws, _triple(bounds, "b"), strict=True):
        if bound < 0:
            raise ValueError("a declared bound is negative")
        total += abs(weight) * bound
    return total


def sharp_remainders(
    bounds: tuple[int | Fraction, int | Fraction, int | Fraction],
) -> tuple[Fraction, Fraction, Fraction]:
    """r_i = sign(w_i) b_i. Then sum w_i r_i equals the triangle radius."""
    _, ws = carrier()
    signed: list[Fraction] = []
    for weight, bound in zip(ws, _triple(bounds, "b"), strict=True):
        if bound < 0:
            raise ValueError("a declared bound is negative")
        if weight == 0:
            raise RuntimeError("a weight vanished")
        signed.append((Fraction(1) if weight > 0 else Fraction(-1)) * bound)
    return (signed[0], signed[1], signed[2])


def refuse_scaling_remainder(traces: object) -> None:
    """The occupation traces do not determine (b_4, b_6, b_8)."""
    del traces
    raise ValueError(
        "verification record carries no independently justified scaling remainder"
    )


def refuse_higher_dimensional_sum(dimension: int, term: int) -> None:
    if isinstance(dimension, bool) or not isinstance(dimension, int):
        raise ValueError("dimension is not an integer")
    if isinstance(term, bool) or not isinstance(term, int):
        raise ValueError("term is not an integer")
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term not in Z_VALUES:
        raise ValueError("term is not a labelled one-dimensional trace")


def witness() -> dict[str, int | Fraction | tuple[int, int, int] | tuple[Fraction, Fraction, Fraction]]:
    xs, ws = carrier()
    moment_0 = sum(ws, Fraction(0))
    moment_1 = sum((w * x for w, x in zip(ws, xs, strict=True)), Fraction(0))
    moment_2 = sum((w * x * x for w, x in zip(ws, xs, strict=True)), Fraction(0))
    if (moment_0, moment_1, moment_2) != (Fraction(1), Fraction(0), Fraction(0)):
        raise RuntimeError("moments are not (1, 0, 0)")
    origin = separable(Fraction(0), xs)
    if origin != Fraction(-1, 36864):
        raise RuntimeError("H(0) is not -1/36864")
    on_nodes = tuple(separable(x, xs) for x in xs)
    if on_nodes != (Fraction(0), Fraction(0), Fraction(0)):
        raise RuntimeError("H did not vanish on the sample nodes")
    lengths = _triple(L_VALUES, "L")
    weight_over_length = sum(
        (abs(w) / length for w, length in zip(ws, lengths, strict=True)),
        Fraction(0),
    )
    if weight_over_length != Fraction(5, 6):
        raise RuntimeError("sum |w_i|/L_i is not 5/6")
    direct_l8 = Fraction(1, 8)
    if weight_over_length / direct_l8 != Fraction(20, 3):
        raise RuntimeError("unlicensed radius is not 20/3 times the L=8 term")
    remainders = sharp_remainders(_B)
    gap, carried = projection_gap(_F, _C1, _C2, remainders)
    radius = model_radius(_B)
    if gap != carried or gap != radius:
        raise RuntimeError("sharp triangle bound was not attained")
    if any(abs(r) > b for r, b in zip(remainders, _B, strict=True)):
        raise RuntimeError("sharp remainder left its declared bound")
    dimensions = tuple(1 << length for length in L_VALUES)
    if dimensions != (16, 64, 256):
        raise RuntimeError("full Fock dimensions left (16, 64, 256)")
    unit_triangle = model_radius((1, 1, 1))
    if unit_triangle != Fraction(197, 35):
        raise RuntimeError("unit triangle factor is not 197/35")
    return {
        "repetitions": REPETITIONS,
        "q": Q,
        "L": L_VALUES,
        "Z": Z_VALUES,
        "fock": dimensions,
        "x": xs,
        "w": ws,
        "moment_0": moment_0,
        "moment_1": moment_1,
        "moment_2": moment_2,
        "H0": origin,
        "H_nodes": on_nodes,
        "unit_triangle": unit_triangle,
        "external_f": _F,
        "external_c1": _C1,
        "external_c2": _C2,
        "external_b": _B,
        "external_r": remainders,
        "gap": gap,
        "carried": carried,
        "radius": radius,
        "weight_over_length": weight_over_length,
        "unlicensed_over_direct_l8": weight_over_length / direct_l8,
        "unlicensed_adopted": 0,
        "bounds_from_samples": 0,
    }
