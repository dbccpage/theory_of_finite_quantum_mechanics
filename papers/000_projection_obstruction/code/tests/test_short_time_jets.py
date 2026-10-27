"""Exact controls for the short-time Taylor extension; numerical checks are scoped."""

import sys
from math import factorial
from pathlib import Path

import numpy as np
import pytest
sp = pytest.importorskip("sympy", reason="install the optional jets extra for exact Taylor checks")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from short_time_jets import (
    I2, PLUS, X, Y, Z, ZERO, defect_jets, derivative_factor,
    normal_rate, partial_trace, remainder_bound, state_jets, tensor,
)


def trace_norm_exact(matrix):
    assert matrix == matrix.conjugate().T
    return sp.simplify(sum(abs(value) * multiplicity for value, multiplicity in matrix.eigenvals().items()))


def amplitude_jets(hamiltonian, state, order):
    """Independent pure-state series, using powers of H instead of commutators."""
    t = sp.Symbol("t", real=True)
    psi = sum(
        ((-sp.I * t) ** k / factorial(k) * hamiltonian ** k * state for k in range(order + 1)),
        sp.zeros(state.rows, 1),
    )
    rho = psi * psi.conjugate().T
    left = sp.Matrix(2, 2, lambda a, b: sum(rho[2*a+c, 2*b+c] for c in range(2)))
    right = sp.Matrix(2, 2, lambda a, b: sum(rho[2*c+a, 2*c+b] for c in range(2)))
    residual = rho - tensor(left, right)
    return [
        residual.applyfunc(lambda entry: sp.expand(entry).coeff(t, k) * factorial(k))
        for k in range(order + 1)
    ]


def test_ising_zero_is_cubic_not_quadratic():
    j, h = sp.symbols("J h", real=True)
    hamiltonian = -j * tensor(Z, Z) - h * (tensor(X, I2) + tensor(I2, X))
    actual = defect_jets(hamiltonian, tensor(ZERO, ZERO), (2, 2), (0, 1), 3)
    expected = sp.zeros(4)
    expected[0, 3], expected[3, 0] = 8*sp.I*j*h**2, -8*sp.I*j*h**2
    assert actual[:3] == [sp.zeros(4)] * 3
    assert actual[3] == expected
    assert trace_norm_exact(expected) == 16*abs(j)*h**2
    assert actual == amplitude_jets(hamiltonian, sp.Matrix([1, 0, 0, 0]), 3)


def test_local_fields_cannot_create_correlation():
    hamiltonian = tensor(X, I2) + 2*tensor(I2, X)
    assert defect_jets(hamiltonian, tensor(ZERO, ZERO), (2, 2), (0, 1), 5) == [sp.zeros(4)] * 6


def test_omitted_terms_cancel_the_proposed_curvature():
    hamiltonian = -tensor(Z, Z) - tensor(X, I2) - tensor(I2, X)
    derivatives = state_jets(hamiltonian, tensor(ZERO, ZERO), 2)
    da = partial_trace(derivatives[1], (2, 2), (0,))
    db = partial_trace(derivatives[1], (2, 2), (1,))
    isolated = -2*tensor(da, db)
    assert isolated == -2*tensor(Y, Y)
    assert trace_norm_exact(isolated) == 8
    assert defect_jets(hamiltonian, tensor(ZERO, ZERO), (2, 2), (0, 1), 2)[2] == sp.zeros(4)


def test_actual_quadratic_onset():
    hamiltonian = tensor(Z, Z) + tensor(X, I2)
    jets = defect_jets(hamiltonian, tensor(ZERO, PLUS), (2, 2), (0, 1), 2)
    assert jets[1] == sp.zeros(4)
    assert trace_norm_exact(jets[2]) == 4
    state = sp.Matrix([1, 1, 0, 0]) / sp.sqrt(2)
    assert jets == amplitude_jets(hamiltonian, state, 2)


def test_plus_state_first_order_rate():
    j = sp.Symbol("J", real=True)
    assert trace_norm_exact(normal_rate(-j*tensor(Z, Z), PLUS, PLUS)) == 2*abs(j)


def test_raw_commutator_is_not_the_normal_rate():
    pair = tensor(ZERO, PLUS)
    raw = -sp.I*(tensor(Z, Z)*pair - pair*tensor(Z, Z))
    assert trace_norm_exact(raw) == 2
    assert normal_rate(tensor(Z, Z), ZERO, PLUS) == sp.zeros(4)


def test_centered_interaction_for_mixed_product():
    a = (I2 + X/sp.Integer(3) + Y/sp.Integer(4) + Z/sp.Integer(5))/2
    b = (I2 - X/sp.Integer(5) + Y/sp.Integer(3) - Z/sp.Integer(4))/2
    ac = Z - sp.trace(Z*a)*I2
    bc = Z - sp.trace(Z*b)*I2
    centered = tensor(ac, bc)
    pair = tensor(a, b)
    assert normal_rate(tensor(Z, Z), a, b) == (-sp.I*(centered*pair-pair*centered)).applyfunc(sp.simplify)


def test_pure_normal_rate_covariance_identity():
    a = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5)])
    b = sp.Matrix([sp.Rational(5, 13), 12*sp.I/sp.Integer(13)])
    pa, pb = a*a.conjugate().T, b*b.conjugate().T
    interaction = tensor(X, Z) + 2*tensor(Y, X) + tensor(Z, Y)
    u = tensor(a, b)
    chi = tensor(I2-pa, I2-pb)*interaction*u
    n = normal_rate(interaction, pa, pb)
    assert n == (-sp.I*(chi*u.conjugate().T-u*chi.conjugate().T)).applyfunc(sp.simplify)
    # Trace(n^2)/2 = ||chi||^2; nonzero eigenvalues are +/- ||chi||.
    assert sp.simplify(sp.trace(n*n)/2 - (chi.conjugate().T*chi)[0]) == 0
    assert sp.simplify(n*n*n - (chi.conjugate().T*chi)[0]*n) == sp.zeros(4)


@pytest.mark.parametrize("order", range(1, 9))
def test_factorial_normalization(order):
    assert remainder_bound(order, 1, 1) == sp.Rational(derivative_factor(order+1), factorial(order+1))
    assert sum(sp.binomial(order, m)*factorial(m)*factorial(order-m) for m in range(order+1)) == factorial(order+1)


@pytest.mark.parametrize("coupling,field", [(1, 0), (1, 1), (-1, 2), (sp.Rational(1, 7), 1)])
def test_numerical_polynomial_envelopes(coupling, field):
    hamiltonian = -coupling*tensor(Z, Z)-field*(tensor(X, I2)+tensor(I2, X))
    rho = tensor(ZERO, ZERO)
    jets = defect_jets(hamiltonian, rho, (2, 2), (0, 1), 3)
    hn = np.array(hamiltonian).astype(complex)
    rn = np.array(rho).astype(complex)
    eigenvalues, eigenvectors = np.linalg.eigh(hn)
    g = abs(coupling)+abs(field)
    for t in (0.002, 0.01, 0.1, 0.3):
        evolution = (eigenvectors*np.exp(-1j*t*eigenvalues))@eigenvectors.conjugate().T
        state = evolution@rn@evolution.conjugate().T
        tensor_state = state.reshape(2, 2, 2, 2)
        a = np.einsum("ijkj->ik", tensor_state)
        b = np.einsum("ijil->jl", tensor_state)
        residual = state-np.kron(a, b)
        for order in (1, 2, 3):
            polynomial = sum(
                (np.array(jets[k]).astype(complex)*t**k/factorial(k) for k in range(1, order+1)),
                np.zeros((4, 4), complex),
            )
            for norm_order in (1, 2, np.inf):
                norm = lambda matrix: np.linalg.norm(np.linalg.svd(matrix, compute_uv=False), ord=norm_order)
                assert abs(norm(residual)-norm(polynomial)) <= float(remainder_bound(order, g, t))+1e-12


def test_dissipation_can_reduce_the_initial_normal_rate():
    interaction, rho = tensor(X, X), tensor(ZERO, ZERO)
    jump = 2*sp.eye(4)+sp.I*interaction/2
    unitary = -sp.I*(interaction*rho-rho*interaction)
    dissipative = jump*rho*jump.conjugate().T-(jump.conjugate().T*jump*rho+rho*jump.conjugate().T*jump)/2
    total = unitary+dissipative
    normal = total-tensor(partial_trace(total, (2, 2), (0,)), ZERO)-tensor(ZERO, partial_trace(total, (2, 2), (1,)))
    assert trace_norm_exact(unitary) == 2
    assert trace_norm_exact(normal) == 1


def test_first_two_jets_ignore_the_distance_two_term():
    # Edge (0,1); site 3 is two graph steps from it.
    h01 = tensor(X, X, I2, I2)
    h12 = tensor(I2, Z, Z, I2)
    h23 = tensor(I2, I2, X, X)
    rho = tensor(ZERO, ZERO, (I2+Y)/2, PLUS)
    nearby = defect_jets(h01+h12, rho, (2, 2, 2, 2), (0, 1), 3)
    extended = defect_jets(h01+h12+h23, rho, (2, 2, 2, 2), (0, 1), 3)
    assert nearby[:3] == extended[:3]
    assert nearby[3] != extended[3]


@pytest.mark.parametrize("dimensions,keep", [((2, 3), (1,)), ((2, 2, 2), (0, 2)), ((2, 2), ())])
def test_partial_trace_identity(dimensions, keep):
    size = int(np.prod(dimensions))
    retained = int(np.prod([dimensions[i] for i in keep]))
    assert partial_trace(sp.eye(size), dimensions, keep) == (size//retained)*sp.eye(retained)


@pytest.mark.parametrize("dimensions,keep", [((2, 2), (1, 0)), ((2, 2), (0, 0)), ((2, 2), (2,)), ((2, 3), (0,))])
def test_partial_trace_refuses_invalid_input(dimensions, keep):
    with pytest.raises(ValueError):
        partial_trace(sp.eye(4), dimensions, keep)
