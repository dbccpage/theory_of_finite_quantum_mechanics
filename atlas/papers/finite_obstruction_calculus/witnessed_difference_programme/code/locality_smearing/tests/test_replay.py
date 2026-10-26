import json
from copy import deepcopy
from fractions import Fraction as Q

import pytest
import sympy as sp
from locality_smearing.car import operators, response
from locality_smearing.finite import (
    exponential_envelope,
    positive_threshold,
    time_consistency_constant,
)
from locality_smearing.locality import check_locality, fixture, marginal, trace_product
from locality_smearing.replay import RECEIPT, check
from trotter_characteristic_polynomials import compute_exact_response_matrix


@pytest.fixture(scope="module")
def retained():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_replay_submitted_finite_certificates(retained):
    assert check(retained)["accepted"]


@pytest.mark.parametrize(
    "change", ["source", "matrix", "diagonal", "basis", "inertia", "parameter"]
)
def test_replay_rejects_mutations(retained, change):
    bad = deepcopy(retained)
    if change == "source":
        key = next(iter(bad["source_hashes"]))
        bad["source_hashes"][key] = "0" * 64
    elif change == "matrix":
        bad["car"][0]["matrix"][0][0] = "7"
    elif change == "diagonal":
        bad["car"][0]["congruence"]["diagonal"][0] = "7"
    elif change == "basis":
        bad["car"][0]["congruence"]["basis"][0] = ["0"] * 8
    elif change == "inertia":
        bad["car"][0]["inertia"] = [3, 1, 4]
    else:
        bad["car"][0]["theta"] = "1/192"
    with pytest.raises(ValueError):
        check(bad)


def test_joint_marginal_tail_bound_is_sharp_and_false_trace_rejected(retained):
    p = fixture()
    c = retained["locality"]["certificate"]
    assert check_locality(p, c)
    assert marginal(p["rho"]) == marginal(p["sigma"])
    assert Q(c["readout_difference"]) == 2 * Q(p["beta"])
    wrong = deepcopy(c)
    wrong["readout_difference"] = "0"
    assert not check_locality(p, wrong)
    # Tr([rho,O]) is zero while the difference of two state readouts is not.
    assert trace_product(p["rho"], p["operator"]) == trace_product(p["operator"], p["rho"])


def test_symbolic_m1_and_the_declared_small_disk():
    r = sp.Symbol("r")
    symbolic = response(1, r)["eigenvalue"]
    assert sp.factor(symbolic + r**4 / (4 * (r + 2) * (r**2 + 4 * r + 8))) == 0
    assert symbolic.subs(r, sp.Rational(1, 192)) == -sp.Rational(1, 87426958080)


def test_actual_constant_profile_margin_binding():
    identity, a, bonds = operators()
    h = sum(bonds, sp.zeros(16))
    total = sum(a, sp.zeros(16))
    u = sp.zeros(16)
    for s in range(16):
        occupied = [(x + 1) % 4 for x in range(4) if s & (1 << x)]
        inversions = sum(x > y for i, x in enumerate(occupied) for y in occupied[i + 1 :])
        t = sum(1 << x for x in occupied)
        u[t, s] = (-1) ** inversions
    assert u.T * u == identity and u * h * u.T == h and u * total * u.T == -total
    assert (total * total).trace() == 16
    assert all(p * p == p and p.T == p for p in bonds)
    theta = Q(1, 10)
    a_bound = time_consistency_constant(theta, 4, 1, 0)
    margin = 1 / (4 * exponential_envelope(theta, 4))
    m0 = positive_threshold(a_bound, margin)
    assert m0 * margin > a_bound
    assert (m0 - 1) * margin <= a_bound


def test_low_pass_is_not_quotient_and_nonclosed_coexact_survives():
    # On a four-cycle this zero-period k=+-1 mode is exact but kept by that low pass.
    low = sp.Matrix([1, -1, -1, 1])
    n = 4
    project = sp.Matrix(n, n, lambda j, k: sum(sp.I ** (p * (j - k)) for p in (1, 3)) / n)
    assert project * low == low and sum(low) == 0
    # Filled triangle: the quotient C1/im d0 includes a nonzero coexact direction.
    d0 = sp.Matrix([[-1, 1, 0], [0, -1, 1], [1, 0, -1]])
    d1 = sp.Matrix([[1, 1, 1]])
    assert d1 * d0 == sp.zeros(1, 3)
    assert 3 - d0.rank() == 1 and 3 - d0.rank() - d1.rank() == 0
    assert d1 * sp.ones(3, 1) != sp.zeros(1, 1)


@pytest.mark.parametrize("m", [1, 2])
def test_independent_existing_car_construction_matches_entire_matrix(m):
    reference = compute_exact_response_matrix(m, sp.Rational(1, 10))
    assert reference["matrix"] == response(m)["matrix"]
