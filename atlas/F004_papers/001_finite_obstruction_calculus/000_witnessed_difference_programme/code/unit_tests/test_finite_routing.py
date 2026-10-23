from fractions import Fraction as Q

from witnessed_difference.finite_routing import (
    Lift,
    Packet,
    Refusal,
    check_lift,
    guarded_edit,
    terminalize,
)
from witnessed_difference.obstruction import MatrixQuotientCertificate
from witnessed_difference.native_functionals import representative_mass


def packet(values, closure):
    values = tuple(map(Q, values))
    return Packet(MatrixQuotientCertificate(tuple((Q(0),) for _ in values), 1, values,
                  tuple(Q(1) for _ in values), (Q(0),), values, representative_mass(values),
                  tuple(Q((v > 0) - (v < 0)) for v in values)), tuple(tuple(map(Q, row)) for row in closure))


def test_lift_actual_squares_transport_and_inclusion():
    a, b = packet([2], [[0]]), packet([4], [[0]])
    lift = Lift((((Q(1),),), ((Q(2),),), ((Q(1),),)))
    assert check_lift(a, b, lift) is None
    assert check_lift(a, a, lift) == Refusal.INVALID_CONTRACT
    assert check_lift(a, b, Lift(lift.maps, True)) == Refusal.INVALID_CONTRACT
    assert check_lift(a, b, None) == Refusal.MISSING_CONTRACT


def test_gamma_damage_and_phi_descent_are_independent():
    a, b = packet([3, 0], [[0, 1]]), packet([1, 1], [[0, 1]])
    assert guarded_edit(a, b, Q(0)) == Refusal.DAMAGE
    assert guarded_edit(a, b, Q(1)) == b
    assert guarded_edit(a, a, Q(1)) == Refusal.NO_DESCENT


def test_fixedpoint_needs_actual_total_declared_transition():
    p = packet([2], [[0]])
    policy = ("ExactCertified", "StabilizedSurvivor", "ActiveCertified")
    assert terminalize(p, None) == Refusal.MISSING_POLICY
    assert terminalize(p, policy) == Refusal.MISSING_STABILITY
    assert terminalize(p, policy, ((p, p), (1, 0)), 0) == Refusal.INVALID_STABILITY
    assert terminalize(p, policy, ((p, p), (0, 0)), 0) == "StabilizedSurvivor"
