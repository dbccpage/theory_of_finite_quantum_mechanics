"""Exact certificates and counterexamples for §§5.11–5.13 and 7.5–7.6."""

from itertools import combinations, product

import pytest

sp = pytest.importorskip("sympy")

from derivation_replays import (
    cycle_five_state,
    finite_sign_fiber,
    hermitian_trace_norm,
    mixed_certificate,
    phase_envelope,
)
from short_time_jets import I2, ZERO, X, Y, Z, normal_rate, partial_trace, state_jets, tensor


@pytest.mark.parametrize("value", [0.1, sp.Float("0.1")])
def test_exact_metric_and_phase_replays_reject_float_inputs(value):
    for operation in (
        lambda: mixed_certificate(value, sp.Rational(3, 4)),
        lambda: hermitian_trace_norm(sp.diag(value, -value)),
        lambda: phase_envelope((value, 1)),
        lambda: finite_sign_fiber((value, 1), (1, 1)),
        lambda: finite_sign_fiber((1, 1), (1, value)),
    ):
        with pytest.raises(TypeError, match="exact scalar"):
            operation()


@pytest.mark.parametrize("value", [sp.nan, sp.oo, -sp.oo, sp.zoo])
def test_phase_replay_rejects_nonfinite_inputs(value):
    with pytest.raises(ValueError, match="finite exact scalar"):
        phase_envelope((value, 1))


def test_exact_algebraic_lengths_remain_supported():
    envelope = phase_envelope((sp.sqrt(2), sp.sqrt(2)))
    assert envelope['minimum'] == 0 and envelope['maximum'] == 8


@pytest.mark.parametrize("p,q", [(sp.Rational(3, 4), sp.Rational(3, 4)),
                                (sp.Rational(1, 4), sp.Rational(1, 5)),
                                (sp.Rational(2, 3), sp.Rational(1, 2)),
                                (sp.Rational(1, 2), sp.Rational(2, 3))])
def test_mixed_primal_dual_certificates(p, q):
    c = mixed_certificate(p, q)
    rho = tensor(c['r'], c['s'])
    velocity = state_jets(tensor(X, Z), rho, 1)[1]
    assert velocity == c['derivative']
    assert normal_rate(tensor(X, Z), c['r'], c['s']) == c['normal']
    assert c['normal'] + c['projected'] == velocity
    for pauli in (X, Y, Z):
        assert sp.trace(c['witness'] * tensor(pauli, c['s'])) == 0
        assert sp.trace(c['witness'] * tensor(c['r'], pauli)) == 0
    assert max(abs(v) for v in c['witness'].eigenvals()) <= 1
    assert hermitian_trace_norm(velocity - c['tangent']) == c['mu']
    assert sp.trace(c['witness'] * velocity) == c['mu']
    assert hermitian_trace_norm(c['normal']) == c['nu']
    if p != sp.Rational(1, 2):
        assert c['nu'] / c['mu'] == 2 * max(q, 1 - q)


def test_triangle_orthogonal_sectors_and_direction_information():
    u = sp.eye(8)[:, 0]
    interactions = (tensor(X, X, I2), 2 * tensor(X, I2, X), 3 * tensor(I2, X, X))
    sectors = [h * u for h in interactions]
    gram = sp.Matrix(3, 3, lambda i, j: (sectors[i].H * sectors[j])[0])
    assert gram == sp.diag(1, 4, 9)  # all three pairs overlap at vertices
    chi = sum(sectors, sp.zeros(8, 1))
    n = -sp.I * (chi * u.H - u * chi.H)
    assert sp.simplify(hermitian_trace_norm(n)**2) == 56
    masses = list(gram.diagonal())
    assert [mass / sum(masses) for mass in masses] == [sp.Rational(1, 14), sp.Rational(2, 7), sp.Rational(9, 14)]
    changed = -sectors[0] + sectors[1] + sectors[2]
    changed_n = -sp.I * (changed * u.H - u * changed.H)
    assert hermitian_trace_norm(n - changed_n) == 4
    assert sp.simplify(hermitian_trace_norm(changed_n)**2) == 56
    # Terms on the SAME edge must be summed before taking masses.
    assert normal_rate(tensor(X, X) - tensor(X, X), ZERO, ZERO) == sp.zeros(4)
    assert hermitian_trace_norm(normal_rate(tensor(X, X), ZERO, ZERO)) == 2


def test_cycle_five_exact_global_counterexample():
    rho = cycle_five_state()
    assert sp.trace(rho) == 1 and rho.H == rho and rho * rho == rho
    for site in range(5):
        assert partial_trace(rho, (2,) * 5, (site,)) == I2 / 2
    for pair in combinations(range(5), 2):
        assert partial_trace(rho, (2,) * 5, pair) == sp.eye(4) / 4
    assert hermitian_trace_norm(rho - sp.eye(32) / 32) == sp.Rational(31, 16)
    # Check the claimed Hamiltonian orbit without transcendental numerics.
    # Each agreeing ZZ edge contributes exp(-i*pi/4); each disagreeing edge
    # multiplies the common phase by i. Disagreements on a cycle are even.
    signs = rho[:, 0] * 32
    for index, bits in enumerate(product((0, 1), repeat=5)):
        disagreements = sum(bits[j] != bits[(j + 1) % 5] for j in range(5))
        assert signs[index] == sp.I**disagreements


@pytest.mark.parametrize("lengths,expected", [((0, 0), (0, 0)), ((0, 2), (4, 4)),
                                             ((3, 1), (4, 16)), ((4, 1, 1), (4, 36)),
                                             ((1, 1, 1), (0, 9))])
def test_full_phase_endpoints(lengths, expected):
    result = phase_envelope(lengths)
    assert (result['minimum'], result['maximum']) == expected
    assert result['mean'] <= result['midpoint']
    assert (result['mean'] == result['midpoint']) == (sum(v > 0 for v in lengths) <= 2)


def test_restricted_host_and_reconstructed_fraction_fixture():
    fixture = finite_sign_fiber((2, 1, 1), (sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 8)))
    assert fixture['values'] == tuple(sp.Rational(n, 384) for n in (25, 49, 81, 121))
    assert fixture['mean'] == sp.Rational(23, 128)
    assert fixture['midpoint'] == sp.Rational(73, 384)
    assert fixture['radius'] == sp.Rational(1, 8)
    assert max(abs(value - fixture['mean']) for value in fixture['values']) == sp.Rational(13, 96)
    signs = finite_sign_fiber((1, 1, 1), (1 / sp.sqrt(3),) * 3)
    assert signs['values'] == (sp.Rational(1, 9), sp.S.One)
    assert phase_envelope((sp.Rational(1, 3),) * 3)['minimum'] == 0
    with pytest.raises(ValueError, match="positive total mass"):
        finite_sign_fiber((0, 0), (1, 1))


def test_imaginary_effect_is_invisible_to_real_signs_but_visible_to_phases():
    effect = (I2 + Y) / 2
    for signs in product((-1, 1), repeat=2):
        z = sp.Matrix(signs)
        assert (z.H * effect * z)[0] / 2 == sp.Rational(1, 2)
    for phase, expected in ((sp.I, 1), (-sp.I, 0)):
        z = sp.Matrix([1, phase])
        assert (z.H * effect * z)[0] / 2 == expected


def test_dephasing_is_not_operator_norm_optimal_and_blocks_differ():
    effect = sp.ones(3) / 3
    assert max(abs(e) for e in (effect - sp.eye(3) / 3).eigenvals()) == sp.Rational(2, 3)
    assert max(abs(e) for e in (effect - sp.eye(3) / 2).eigenvals()) == sp.Rational(1, 2)
    block = sp.diag(1, 1, 0)
    readout = sp.diag(1, 0, 0)
    first, second = sp.diag(1, 0, 0), sp.diag(0, 1, 0)
    assert sp.trace(block * first) == sp.trace(block * second) == 1
    assert sp.trace(readout * first) == 1 and sp.trace(readout * second) == 0


def test_zero_population_can_have_second_order_phase_ambiguity():
    h = sp.Matrix([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    derivatives = []
    for sign in (1, -1):
        z = sp.Matrix([0, 1, sign])
        jets = state_jets(h, z * z.T / 2, 2)
        assert jets[0][0, 0] == jets[1][0, 0] == 0
        derivatives.append(jets[2][0, 0])
    assert derivatives == [4, 0]
    # Z under H=X requires Y for closure; those observables are not commuting.
    assert sp.I * (X * Z - Z * X) == 2 * Y
    assert sp.I * (X * Y - Y * X) == -2 * Z
    assert Y * Z != Z * Y


def test_scalar_midpoints_need_not_be_a_probability_vector():
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    fourier = sp.Matrix(3, 3, lambda i, j: omega**(i * j) / sp.sqrt(3))
    assert (fourier * fourier.H).applyfunc(sp.simplify) == sp.eye(3)
    midpoints = []
    for i in range(3):
        lengths = tuple(sp.simplify(sp.Abs(fourier[i, j]) / sp.sqrt(3)) for j in range(3))
        midpoints.append(phase_envelope(lengths)['midpoint'])
        # The inverse image of each output vertex has the same input weights.
        lift = fourier.H[:, i]
        assert [sp.simplify(sp.Abs(x)**2) for x in lift] == [sp.Rational(1, 3)] * 3
    assert sum(midpoints) == sp.Rational(3, 2)
