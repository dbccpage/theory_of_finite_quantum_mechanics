"""Exact examples for Appendix E, not a general reconstruction verifier."""

from itertools import product

import pytest

from jordan_lie_countermodels import central_weight_bounds

sp = pytest.importorskip("sympy")

ONE = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
BASIS = (ONE, X, Y, Z)


def jordan(a, b):
    return (a * b + b * a) / 2


def bracket(a, b):
    return (a * b - b * a) / (2 * sp.I)


def star(a, b):
    return jordan(a, b) + sp.I * bracket(a, b)


def coefficients(a):
    return sp.Matrix([sp.trace(b * a) / 2 for b in BASIS])


def operator_matrix(action):
    return sp.Matrix.hstack(*(coefficients(action(b)) for b in BASIS))


def marginal_a(rho, dim_a, dim_b):
    return sp.Matrix(dim_a, dim_a, lambda i, j: sum(
        rho[i * dim_b + k, j * dim_b + k] for k in range(dim_b)
    ))


def test_jacobi_derivation_and_associator_on_all_pauli_basis_triples():
    for a, b, c in product(BASIS, repeat=3):
        assert bracket(a, bracket(b, c)) + bracket(b, bracket(c, a)) + bracket(c, bracket(a, b)) == sp.zeros(2)
        assert bracket(a, jordan(b, c)) == jordan(bracket(a, b), c) + jordan(b, bracket(a, c))
        assert jordan(jordan(a, b), c) - jordan(a, jordan(b, c)) == bracket(b, bracket(c, a))
        assert star(star(a, b), c) == star(a, star(b, c)) == a * b * c


def test_wrong_associator_sign_and_zero_bracket_are_detected():
    associator = jordan(jordan(X, Z), Z) - jordan(X, jordan(Z, Z))
    assert associator == -X
    assert associator != -bracket(Z, bracket(Z, X))
    assert associator != sp.zeros(2)


def test_positive_trace_form_and_skew_bracket_generate_hermitian_left_action():
    for a in BASIS:
        left = operator_matrix(lambda b: jordan(a, b))
        derivation = operator_matrix(lambda b: bracket(a, b))
        assert left.H == left
        assert derivation.H == -derivation
        matrix = left + sp.I * derivation
        assert matrix.H == matrix
        assert matrix * coefficients(ONE) == coefficients(a)
    for a, b in product(BASIS, repeat=2):
        ma = operator_matrix(lambda c: star(a, c))
        mb = operator_matrix(lambda c: star(b, c))
        mab = operator_matrix(lambda c: star(star(a, b), c))
        assert ma * mb == mab


def test_canonical_multiplication_trace_constructs_the_compatible_form():
    def tau(a):
        return sp.trace(operator_matrix(lambda b: jordan(a, b)))

    gram = sp.Matrix(4, 4, lambda i, j: tau(jordan(BASIS[i], BASIS[j])))
    assert gram == 4 * sp.eye(4)
    assert gram.is_positive_definite
    for a in BASIS:
        left = operator_matrix(lambda b: jordan(a, b))
        derivation = operator_matrix(lambda b: bracket(a, b))
        assert left.T * gram == gram * left
        assert derivation.T * gram == -gram * derivation
        assert tau(a) == 2 * sp.trace(a)

    e = (ONE + Z) / 2
    left = operator_matrix(lambda b: jordan(e, b))
    p, q = 2 * left**2 - left, 4 * (left - left**2)
    assert 2 * left**3 - 3 * left**2 + left == sp.zeros(4)
    assert p * p == p
    assert q * q == q
    assert 2 * left == 2 * p + q
    assert sp.trace(left) == p.rank() + sp.Rational(1, 2) * q.rank() == 2


def test_real_spectral_premise_cannot_be_dropped_from_trace_positivity():
    # Multiplication by i on C regarded as a real algebra.
    left_i = sp.Matrix([[0, -1], [1, 0]])
    left_i_squared = -sp.eye(2)
    assert left_i * left_i == left_i_squared
    assert sp.trace(left_i_squared) == -2


def test_central_purity_ceiling_and_distance_bound_are_attained():
    weights = (sp.Rational(3, 5), sp.Rational(2, 5))
    bounds = central_weight_bounds(("3/5", "2/5"))
    vectors = (sp.Matrix([sp.Rational(3, 5), 0, 0, sp.Rational(4, 5)]), sp.eye(4)[:, 0])
    pure_blocks = tuple(v * v.H for v in vectors)
    extension = sp.diag(*(p * block for p, block in zip(weights, pure_blocks, strict=True)))
    marginals = tuple(marginal_a(block, 2, 2) for block in pure_blocks)
    rho = sp.diag(*(p * block for p, block in zip(weights, marginals, strict=True)))
    assert extension.is_positive_semidefinite
    assert sp.trace(extension) == 1
    assert sp.trace(extension**2) == bounds["maximum_extension_purity"] == sp.Rational(13, 25)
    assert sp.diag(*(marginal_a(p * block, 2, 2)
                     for p, block in zip(weights, pure_blocks, strict=True))) == rho
    nearest = sp.diag(marginals[0], sp.zeros(2))
    difference = rho - nearest
    distance = sum(abs(value) * multiplicity for value, multiplicity in difference.eigenvals().items()) / 2
    assert distance == bounds["minimum_pure_marginal_distance"] == sp.Rational(2, 5)


def test_sector_swap_channel_can_change_sector_probabilities():
    # A reversible *-automorphism exists although no continuous pure-state
    # path can join the two connected components of the classical state space.
    swap = sp.Matrix([[0, 1], [1, 0]])
    rho = sp.diag(sp.Rational(3, 5), sp.Rational(2, 5))
    assert swap.H * swap == sp.eye(2)
    assert swap * rho * swap.H == sp.diag(sp.Rational(2, 5), sp.Rational(3, 5))
    assert swap * rho * swap.H != rho


@pytest.mark.parametrize("weights", [(), ("-1/2", "3/2"), ("1/3", "1/3"), (0, 0)])
def test_central_bounds_refuse_invalid_probability_reports(weights):
    with pytest.raises(ValueError, match="sum exactly to one"):
        central_weight_bounds(weights)


def test_classical_diagonals_satisfy_the_same_base_with_zero_bracket():
    basis = (sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1))
    for a, b, c in product(basis, repeat=3):
        assert bracket(a, b) == sp.zeros(3)
        assert jordan(jordan(a, b), c) == jordan(a, jordan(b, c))
    fair_bit = sp.diag(sp.Rational(1, 2), sp.Rational(1, 2))
    for ancillary_size in range(1, 6):
        for index in range(2 * ancillary_size):
            vector = sp.eye(2 * ancillary_size)[:, index]
            reduced = marginal_a(vector * vector.H, 2, ancillary_size)
            assert reduced != fair_bit
            assert reduced[0, 0] in (0, 1)


def test_local_brackets_commute_and_product_is_standard_tensor():
    for a, b in product(BASIS, repeat=2):
        alpha = sp.kronecker_product(a, ONE)
        beta = sp.kronecker_product(ONE, b)
        assert bracket(alpha, beta) == sp.zeros(4)
        assert star(alpha, beta) == sp.kronecker_product(a, b)
    # Local tomography here is an exact independence check on 16 products.
    products = [sp.kronecker_product(a, b).reshape(16, 1) for a, b in product(BASIS, repeat=2)]
    assert sp.Matrix.hstack(*products).rank() == 16


def test_jordan_compression_equals_matrix_corner():
    p = sp.diag(1, 0, 1)
    a = sp.Matrix([[1, 2 + sp.I, 3], [2 - sp.I, 4, 5], [3, 5, 6]])
    assert 2 * jordan(p, jordan(p, a)) - jordan(p, a) == p * a * p
    # Arbitrary block tuple (1, 2, 3) is a corner of C^3 tensor M_3.
    projections = (sp.diag(1, 0, 0), sp.diag(1, 1, 0), sp.eye(3))
    corner = sp.diag(*projections)
    assert corner * corner == corner
    assert [block.rank() for block in projections] == [1, 2, 3]


def test_mixed_quantum_state_has_pure_quantum_purification():
    plus = sp.Matrix([1, 1]) / sp.sqrt(2)
    minus = sp.Matrix([1, -1]) / sp.sqrt(2)
    e0, e1 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
    vector = sp.sqrt(sp.Rational(2, 3)) * sp.kronecker_product(plus, e0) + sp.sqrt(sp.Rational(1, 3)) * sp.kronecker_product(minus, e1)
    joint = sp.simplify(vector * vector.H)
    rho = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 6)], [sp.Rational(1, 6), sp.Rational(1, 2)]])
    assert joint.rank() == 1
    assert sp.trace(joint) == 1
    assert marginal_a(joint, 2, 2) == rho
    changed = sp.kronecker_product(ONE, X) * joint * sp.kronecker_product(ONE, X)
    assert changed != joint
    assert marginal_a(changed, 2, 2) == rho


def test_superselection_cannot_be_removed_by_cross_sector_coherence():
    # (C direct-sum M_2) tensor M_2 has blocks of dimensions 2 and 4.
    central = sp.diag(1, 1, 0, 0, 0, 0)
    vector = (sp.eye(6)[:, 0] + sp.eye(6)[:, 2]) / sp.sqrt(2)
    attempted = vector * vector.H
    assert sp.trace(central * attempted) == sp.Rational(1, 2)
    assert attempted[:2, 2:] != sp.zeros(2, 4)  # Not in the observable/state algebra.
    complement = sp.eye(6) - central
    allowed = central * attempted * central + complement * attempted * complement
    assert allowed[:2, 2:] == sp.zeros(2, 4)
    assert allowed.rank() == 2  # Dephasing restores the algebra but loses purity.


def test_born_pairing_and_continuous_pure_state_motion():
    t = sp.symbols("t", real=True)
    unitary = sp.Matrix([[sp.cos(t), -sp.sin(t)], [sp.sin(t), sp.cos(t)]])
    assert sp.simplify(unitary.H * unitary) == ONE
    assert unitary.subs(t, 0) == ONE
    e0, e1 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
    assert unitary.subs(t, sp.pi / 2) * e0 == e1
    phi = sp.Matrix([3, 4]) / 5
    psi = sp.Matrix([1, sp.I]) / sp.sqrt(2)
    amplitude = (phi.H * psi)[0]
    assert sp.trace(psi * psi.H * phi * phi.H) == sp.simplify(amplitude * sp.conjugate(amplitude))


def test_transposition_fails_the_ancilla_condition():
    matrix_units = [sp.eye(2)[:, j] * sp.eye(2)[:, k].T for j, k in product(range(2), repeat=2)]
    choi = sum((sp.kronecker_product(e, e.T) for e in matrix_units), sp.zeros(4))
    singlet = sp.Matrix([0, 1, -1, 0]) / sp.sqrt(2)
    assert (singlet.H * choi * singlet)[0] == -1
    rho = sp.Matrix([[sp.Rational(1, 2), sp.I / 6], [-sp.I / 6, sp.Rational(1, 2)]])
    assert all(value >= 0 for value in rho.T.eigenvals())


def test_amplitude_damping_kraus_and_choi_forms_agree():
    operators = (sp.diag(1, sp.Rational(3, 5)), sp.Matrix([[0, sp.Rational(4, 5)], [0, 0]]))
    assert sum((k.H * k for k in operators), sp.zeros(2)) == ONE

    def channel(a):
        return sum((k * a * k.H for k in operators), sp.zeros(2))

    choi = sp.zeros(4)
    for j, k in product(range(2), repeat=2):
        unit = sp.eye(2)[:, j] * sp.eye(2)[:, k].T
        choi += sp.kronecker_product(unit, channel(unit))
    vectors = [sp.Matrix.vstack(k[:, 0], k[:, 1]) for k in operators]
    assert choi == sum((v * v.H for v in vectors), sp.zeros(4))
    assert all(value >= 0 for value in choi.eigenvals())
    assert choi.rank() == 2
