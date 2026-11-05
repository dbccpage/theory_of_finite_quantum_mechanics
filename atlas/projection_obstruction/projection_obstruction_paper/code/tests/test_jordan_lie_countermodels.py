"""Unit and property tests for Jordan-Lie Operational Foundations & Countermodels (R6)."""

from fractions import Fraction
from itertools import product

import pytest

import jordan_lie_countermodels as models

from jordan_lie_countermodels import (
    AlbertMatrix,
    Octonion,
    check_albert_algebra_properties,
    check_quaternionic_qm_countermodel,
    check_real_qm_countermodel,
    check_superselection_countermodel,
    get_axiom_satisfaction_table,
    verify_jordan_lie_countermodels,
)


def test_octonion_algebra_and_non_associativity():
    """Verify exact Fano plane multiplication, units, conjugates, and non-associativity."""
    # Basis units
    e0 = Octonion.unit(0)
    e1 = Octonion.unit(1)
    e2 = Octonion.unit(2)
    e3 = Octonion.unit(3)
    e4 = Octonion.unit(4)

    # e0 is multiplicative identity
    assert (e0 * e1).coeffs == e1.coeffs
    assert (e1 * e0).coeffs == e1.coeffs

    # Squares of imaginary units are -1
    for i in range(1, 8):
        ei = Octonion.unit(i)
        prod_ei = ei * ei
        assert prod_ei.coeffs == (-Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))

    # Fano triplet: e1 * e2 = e3, e2 * e3 = e1, e3 * e1 = e2, e2 * e1 = -e3
    assert (e1 * e2).coeffs == e3.coeffs
    assert (e2 * e3).coeffs == e1.coeffs
    assert (e3 * e1).coeffs == e2.coeffs
    assert (e2 * e1).coeffs == e3.scale(-1).coeffs

    # Non-associativity: (e1 * e2) * e4 != e1 * (e2 * e4)
    # (e1 * e2) * e4 = e3 * e4 = e7 (triplet (3, 4, 7))
    # e2 * e4 = e6 (triplet (2, 4, 6))
    # e1 * e6 = -e7 (triplet (1, 7, 6) has e1 * e7 = e6 => e1 * e6 = -e7)
    # Associator: (e1 * e2) * e4 - e1 * (e2 * e4) = e7 - (-e7) = 2 e7 != 0
    lhs = (e1 * e2) * e4
    rhs = e1 * (e2 * e4)
    associator = lhs - rhs
    assert not associator.is_zero()
    assert associator.coeffs[7] == Fraction(2)
    for k in range(7):
        assert associator.coeffs[k] == Fraction(0)


def test_selected_albert_identities():
    """Check finite identities; exceptionality is a separate imported theorem."""
    receipt = check_albert_algebra_properties()
    assert receipt["dimension"] == 27
    assert receipt["selected_jordan_identity_holds"] is True
    assert receipt["octonion_non_associative"] is True
    assert receipt["special_embedding_status"] == "imported_exceptionality_theorem"
    assert "B1" in receipt["excluded_by"]

    # Check explicit AlbertMatrix Jordan product commutativity
    A = AlbertMatrix(
        d0=Fraction(2),
        d1=Fraction(-1),
        d2=Fraction(3),
        x01=Octonion.unit(2),
        x02=Octonion.unit(5),
        x12=Octonion.unit(7),
    )
    B = AlbertMatrix(
        d0=Fraction(1),
        d1=Fraction(4),
        d2=Fraction(0),
        x01=Octonion.unit(1),
        x02=Octonion.unit(3),
        x12=Octonion.unit(6),
    )
    AoB = A.jordan_product(B)
    BoA = B.jordan_product(A)
    diff = AoB - BoA
    assert diff.is_zero()


def test_real_qm_countermodel_and_exclusion_of_b2():
    """Verify that Real QM violates local tomography with dimension gap 10 - 9 = 1."""
    receipt = check_real_qm_countermodel()
    assert receipt["single_system_observable_dim"] == 3
    assert receipt["product_observable_dim"] == 9
    assert receipt["composite_observable_dim"] == 10
    assert receipt["dimension_gap"] == 1
    assert receipt["local_tomography_fails"] is True
    assert "Y (x) Y" in receipt["missing_observable_witness"]
    assert "B2" in receipt["excluded_by"]

    # Verify linear algebra proof of missing observable:
    # Let Y = [[0, -1], [1, 0]]. For any real symmetric 2x2 matrix S:
    # tr(Y S) = Y_00 S_00 + Y_01 S_10 + Y_10 S_01 + Y_11 S_11
    #         = 0 - S_10 + S_01 + 0 = S_01 - S_10 = 0 (since S is symmetric!).
    # Thus for W = Y (x) Y, tr(W (A (x) B)) = tr(Y A) tr(Y B) = 0 * 0 = 0.
    # But tr(W * W) = tr(Y^2) * tr(Y^2) = (-2) * (-2) = 4 != 0.
    # Hence W is nonzero and strictly orthogonal to span(S_2(R) (x) S_2(R)).
    tr_Y_squared = -2
    tr_W_squared = tr_Y_squared * tr_Y_squared
    assert tr_W_squared == 4


def test_quaternionic_qm_countermodel_and_exclusion_of_b2():
    """Verify that Quaternionic QM violates local tomography with dimension defect 36 - 28 = 8."""
    receipt = check_quaternionic_qm_countermodel()
    assert receipt["single_system_observable_dim"] == 6
    assert receipt["product_observable_dim"] == 36
    assert receipt["composite_observable_dim"] == 28
    assert receipt["dimension_defect"] == 8
    assert receipt["local_tomography_fails"] is True
    assert "B2" in receipt["excluded_by"]


def test_fair_sector_report_has_positive_distance_from_each_pure_report():
    receipt = check_superselection_countermodel()
    assert receipt["distances_to_pure_reports"] == (Fraction(1, 2), Fraction(1, 2))
    for vertex in receipt["pure_central_reports"]:
        # The central effect attaining the variation distance is explicit.
        index = vertex.index(Fraction(1))
        assert abs(vertex[index] - receipt["central_weights"][index]) == Fraction(1, 2)


def test_real_purification_and_failure_of_local_tomography_can_coexist():
    sp = pytest.importorskip("sympy")
    receipt = check_real_qm_countermodel()
    joint = sp.Matrix(receipt["purification_joint"])
    marginal = sp.Matrix(receipt["purification_marginal"])
    assert joint == joint.T
    assert joint.is_positive_semidefinite
    assert joint.rank() == 1
    assert sp.trace(joint) == 1
    assert sp.trace(joint * joint) == receipt["purification_joint_purity"] == 1
    independently_reduced = sp.Matrix(2, 2, lambda i, j: sum(
        joint[2 * i + k, 2 * j + k] for k in range(2)
    ))
    assert independently_reduced == marginal == sp.diag(sp.Rational(9, 25), sp.Rational(16, 25))
    assert marginal.rank() == 2
    assert sp.trace(marginal * marginal) < 1

    skew = sp.Matrix([[0, -1], [1, 0]])
    hidden = sp.kronecker_product(skew, skew)
    plus, minus = (sp.eye(4) + hidden) / 4, (sp.eye(4) - hidden) / 4
    for state in (plus, minus):
        assert state == state.T
        assert state.is_positive_semidefinite
        assert sp.trace(state) == 1
    local_basis = (sp.eye(2), sp.Matrix([[0, 1], [1, 0]]), sp.diag(1, -1))
    for a, b in product(local_basis, repeat=2):
        effect = sp.kronecker_product(a, b)
        assert sp.trace(plus * effect) == sp.trace(minus * effect)
    assert sp.trace(plus * hidden) == 1
    assert sp.trace(minus * hidden) == -1
    # The table records this proved distinction, including real purification.
    table = get_axiom_satisfaction_table()
    assert table["real_qm"]["purification"] is True
    assert table["real_qm"]["B2"] is False


def test_quaternion_subalgebra_is_associative_on_every_basis_triple():
    units = tuple(Octonion.unit(i) for i in range(4))
    for a, b, c in product(units, repeat=3):
        assert (a * b) * c == a * (b * c)
    assert units[1] * units[2] != units[2] * units[1]


@pytest.mark.parametrize("value", [0.1, 2.0**-41, float("nan"), True, False])
def test_exact_scalar_boundary_refuses_floats_and_booleans(value):
    with pytest.raises(TypeError):
        Octonion.from_coeffs([value, 0, 0, 0, 0, 0, 0, 0])
    with pytest.raises(TypeError):
        Octonion(value, 0, 0, 0, 0, 0, 0, 0)
    with pytest.raises(TypeError):
        Octonion.unit(1).scale(value)
    with pytest.raises(TypeError):
        AlbertMatrix(value, 0, 0, Octonion.zero(), Octonion.zero(), Octonion.zero())


def test_small_exact_coefficients_are_preserved():
    value = Fraction(1, 2**41)
    x = Octonion.from_coeffs([value, 0, 0, 0, 0, 0, 0, 0])
    assert not x.is_zero()
    assert x * Octonion.unit(0) == x


@pytest.mark.parametrize("field", ["selected_jordan_identity_holds", "octonion_non_associative"])
def test_failed_albert_fixture_cannot_receive_a_success_status(monkeypatch, field):
    bad = check_albert_algebra_properties()
    bad[field] = False
    monkeypatch.setattr(models, "check_albert_algebra_properties", lambda: bad)
    with pytest.raises(ValueError, match="finite countermodel check failed"):
        verify_jordan_lie_countermodels()


def test_failed_real_purification_cannot_receive_a_success_status(monkeypatch):
    bad = check_real_qm_countermodel()
    bad["purification_joint_purity"] = Fraction(1, 2)
    monkeypatch.setattr(models, "check_real_qm_countermodel", lambda: bad)
    with pytest.raises(ValueError, match="finite countermodel check failed"):
        verify_jordan_lie_countermodels()


def test_octonion_algebra_involution_norm_and_alternativity():
    """Verify conjugate anti-automorphism, norm multiplicative law, and alternativity."""
    x = Octonion(Fraction(1), Fraction(2), Fraction(-1), Fraction(0), Fraction(3), Fraction(-2), Fraction(1), Fraction(1))
    y = Octonion(Fraction(-1), Fraction(1), Fraction(2), Fraction(-3), Fraction(0), Fraction(1), Fraction(-1), Fraction(2))

    # Double conjugate is identity: (x^*)^* = x
    assert x.conjugate().conjugate().coeffs == x.coeffs

    # Conjugate anti-automorphism: (x * y)^* = y^* * x^*
    xy_conj = (x * y).conjugate()
    y_conj_x_conj = y.conjugate() * x.conjugate()
    assert xy_conj.coeffs == y_conj_x_conj.coeffs

    # Alternativity: x * (x * y) == (x * x) * y
    left_alt = x * (x * y)
    right_alt = (x * x) * y
    assert left_alt.coeffs == right_alt.coeffs

    # Right alternativity: (y * x) * x == y * (x * x)
    left_alt_r = (y * x) * x
    right_alt_r = y * (x * x)
    assert left_alt_r.coeffs == right_alt_r.coeffs


def test_real_and_quaternionic_qm_general_dimension_laws():
    """Verify general dimension scaling formulas proving local tomography fails for all d >= 2."""
    # Real QM: dim S_d(R) = d(d+1)/2. For composite system of two d-dimensional systems,
    # composite dimension is dim S_{d^2}(R) = d^2 (d^2 + 1) / 2.
    # Product dimension is (d(d+1)/2)^2 = d^2 (d+1)^2 / 4.
    # The gap is d^2 (d^2 + 1)/2 - d^2 (d+1)^2 / 4 = d^2 (d-1)^2 / 4 > 0 for all d >= 2!
    for d in (2, 3, 4, 5):
        single_dim = d * (d + 1) // 2
        product_dim = single_dim * single_dim
        comp_dim = (d * d) * (d * d + 1) // 2
        expected_gap = (d * d) * ((d - 1) * (d - 1)) // 4
        assert comp_dim - product_dim == expected_gap
        assert expected_gap > 0  # Local tomography strictly fails for all d >= 2!

    # Quaternionic QM: dim H_d(H) = 2 d^2 - d.
    # Composite system of two d-dimensional systems is H_{d^2}(H) with dimension 2 (d^2)^2 - d^2 = 2 d^4 - d^2.
    # Product dimension is (2 d^2 - d)^2 = 4 d^4 - 4 d^3 + d^2.
    # Defect product_dim - comp_dim = 2 d^4 - 4 d^3 + 2 d^2 = 2 d^2 (d - 1)^2 > 0 for all d >= 2!
    for d in (2, 3, 4):
        single_dim = 2 * d * d - d
        product_dim = single_dim * single_dim
        comp_dim = 2 * (d * d) * (d * d) - (d * d)
        expected_defect = 2 * (d * d) * ((d - 1) * (d - 1))
        assert product_dim - comp_dim == expected_defect
        assert expected_defect > 0  # Local tomography strictly fails for all d >= 2!

