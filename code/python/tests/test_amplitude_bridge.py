"""Tests for Gaussian rational amplitude bridge, holonomy, and gauge invariance."""

from fractions import Fraction
from src.wdp.amplitude_bridge import (
    GaussianRational,
    U_PHASE,
    u_pow,
    u_power_is_never_one,
    OrientedGraph,
    readout_quadratic,
    readout_quartic,
    AUTHORITY_FENCE,
)


def test_unit_phase_modulus():
    assert U_PHASE.norm_sq() == Fraction(1)
    # u = 3/5 + 4/5 i
    assert U_PHASE.re == Fraction(3, 5)
    assert U_PHASE.im == Fraction(4, 5)

    # u^2 = (9 - 16)/25 + 24/25 i = -7/25 + 24/25 i
    u2 = u_pow(2)
    assert u2.re == Fraction(-7, 25)
    assert u2.im == Fraction(24, 25)
    assert u2.norm_sq() == Fraction(1)


def test_u_power_never_one():
    assert u_power_is_never_one(1) is True
    assert u_power_is_never_one(100) is True
    # u^n != 1 for small n
    for n in range(1, 10):
        un = u_pow(n)
        assert not (un.re == Fraction(1) and un.im == Fraction(0))


def test_cycle_holonomy_and_gauge_invariance():
    # Triangle graph A -> B -> C -> A
    g = OrientedGraph()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.add_edge("C", "A", -1)

    triangle_cycle = [("A", "B"), ("B", "C"), ("C", "A")]
    hol_orig = g.cycle_holonomy(triangle_cycle)

    # Total winding = 1 + 2 - 1 = 2
    assert hol_orig == u_pow(2)

    # Gauge transformation by f: A=3, B=-2, C=5
    f = {"A": 3, "B": -2, "C": 5}
    g_gauged = g.gauge_transform(f)

    # Cycle holonomy must be strictly invariant under gauge transformation!
    hol_gauged = g_gauged.cycle_holonomy(triangle_cycle)
    assert hol_gauged == hol_orig


def test_readouts():
    z1 = GaussianRational.from_integers(1, 0)
    z2 = GaussianRational.from_integers(0, 1)

    # z1 + z2 = 1 + i, |z1+z2|^2 = 2
    quad = readout_quadratic(z1, z2)
    assert quad == Fraction(2)

    # quartic = 4
    quart = readout_quartic(z1, z2)
    assert quart == Fraction(4)
