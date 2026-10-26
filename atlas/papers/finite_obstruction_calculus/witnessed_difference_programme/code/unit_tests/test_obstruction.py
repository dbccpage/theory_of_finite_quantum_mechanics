
from witnessed_difference.native_functionals import representative_mass, dual_bound
from dataclasses import replace
from fractions import Fraction
from itertools import product

import pytest
import witnessed_difference.obstruction as obstruction
from witnessed_difference.cochains import FiniteComplex, is_closed, solve_potential
from witnessed_difference.obstruction import (
    ROUTING_TERMINALS,
    DiagnosticClass,
    MatrixQuotientCertificate,
    ObstructionSignature,
    QuotientCertificate,
    classify_signature,
    d0_adjoint,
    d0_matrix,
    d1_matrix,
    d1_operator_norm_1to1,
    degree_one_window,
    edge_weights,
    evaluation_preorder,
    exact_quotient_l1,
    matrix_quotient_l1,
    obstruction_signature,
    promote_diagnostic,
    solve_standard_lp,
    verify_matrix_certificate,
    verify_quotient_certificate,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused

TRIANGLE_EDGES = ((0, 1), (1, 2), (0, 2))
SQUARE_EDGES = ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2))
C1 = (1, 1, 0, 0, -1)
C2 = (0, 0, 1, -1, 1)


def triangle(filled: bool = True) -> FiniteComplex:
    return FiniteComplex((0, 1, 2), TRIANGLE_EDGES, ((0, 1, 2),) if filled else ())


def square(faces: tuple[tuple[int, int, int], ...] = ()) -> FiniteComplex:
    return FiniteComplex((0, 1, 2, 3), SQUARE_EDGES, faces)


def cochain(complex_: FiniteComplex, values) -> dict:
    return dict(zip(complex_.edges, values))


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def assert_exact(*values) -> None:
    for value in values:
        items = value if isinstance(value, tuple) else (value,)
        assert all(type(item) is Fraction for item in items), value


def test_evaluation_preorder_is_the_reflexive_transitive_closure() -> None:
    carrier = ("a", "b", "c", "d")
    closure = accepted(evaluation_preorder(carrier, (("a", "b"), ("b", "c"), ("c", "b"))))
    assert {(state, state) for state in carrier} <= closure
    assert {("a", "c"), ("b", "c"), ("c", "b")} <= closure
    assert ("c", "a") not in closure and ("a", "d") not in closure
    for (x, y), (u, v) in product(closure, repeat=2):
        if y == u:
            assert (x, v) in closure
    assert accepted(evaluation_preorder((), ())) == frozenset()


@pytest.mark.parametrize(
    ("carrier", "relation", "code"),
    [
        (("a", "a"), (), RefusalCode.INVALID_INPUT),
        (("a", "b"), (("a", "z"),), RefusalCode.OUTSIDE_CARRIER),
        (("a", "b"), (["a", "b"],), RefusalCode.INVALID_INPUT),
        (("a", "b"), (("a", "b", "a"),), RefusalCode.INVALID_INPUT),
    ],
)
def test_evaluation_preorder_refuses_malformed_relations(carrier, relation, code) -> None:
    refused(evaluation_preorder(carrier, relation), code)


def test_degree_one_window_carries_a_zero_composite_certificate() -> None:
    window = accepted(degree_one_window(square(((0, 1, 2), (0, 2, 3)))))
    assert len(window.d0) == 5 and len(window.d1) == 2
    assert window.composite == ((Fraction(0),) * 4, (Fraction(0),) * 4)
    assert window.d1[0] == (1, 1, 0, 0, -1)
    assert accepted(degree_one_window(triangle(False))).composite == ()
    refused(degree_one_window("triangle"), RefusalCode.INVALID_INPUT)


def test_degree_one_window_refuses_a_broken_closure_matrix(monkeypatch) -> None:
    def flipped(complex_):
        return tuple(tuple(-entry if index == 2 else entry for index, entry in enumerate(row)) for row in d1_matrix(complex_))

    monkeypatch.setattr(obstruction, "d1_matrix", flipped)
    refused(degree_one_window(triangle()), RefusalCode.CERTIFICATE_MISMATCH, "d1 o d0")


def test_reversed_edge_orientation_changes_signs_not_the_signature() -> None:
    reversed_ = FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (2, 0)), ((0, 1, 2),))
    assert d1_matrix(reversed_) == ((1, 1, 1),)
    values = {(0, 1): 1, (1, 2): 1, (2, 0): 0}
    signature = accepted(obstruction_signature(reversed_, values, closure_declared=True))
    standard = accepted(obstruction_signature(triangle(), cochain(triangle(), (1, 1, 0)), closure_declared=True))
    assert (signature.phi1, signature.gamma2, signature.closure_ratio) == (standard.phi1, standard.gamma2, 1)
    assert accepted(degree_one_window(reversed_)).composite == ((0, 0, 0),)


def test_worked_filled_triangle_signature_and_certificate() -> None:
    complex_ = triangle()
    signature = accepted(obstruction_signature(complex_, cochain(complex_, (1, 1, 0)), closure_declared=True))
    assert (signature.phi1, signature.gamma2) == (2, 2)
    assert signature.closure_ratio == 1 == signature.d1_opnorm
    assert signature.diagnostic_class is DiagnosticClass.ACTIVE_CLOSURE_FAILURE
    assert_exact(signature.phi1, signature.gamma2, signature.closure_ratio, signature.certificate.dual)
    worked = QuotientCertificate(
        complex_,
        (Fraction(1), Fraction(1), Fraction(0)),
        (Fraction(1),) * 3,
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(2), Fraction(0)),
        Fraction(2),
        (Fraction(1), Fraction(1), Fraction(-1)),
    )
    assert accepted(verify_quotient_certificate(worked)) == worked


def test_no_integer_potential_in_a_box_beats_the_certified_quotient_norm() -> None:
    complex_ = triangle()
    phi = accepted(exact_quotient_l1(complex_, cochain(complex_, (1, 1, 0)))).value
    masses = []
    for f in product(range(-3, 4), repeat=3):
        residual = (1 - (f[1] - f[0]), 1 - (f[2] - f[1]), 0 - (f[2] - f[0]))
        masses.append(representative_mass(tuple(Fraction(value) for value in residual)))
    assert min(masses) == phi == 2
    assert all(mass >= phi for mass in masses)


def test_fractional_class_is_certified_where_integer_potentials_fail() -> None:
    complex_ = triangle()
    certificate = accepted(exact_quotient_l1(complex_, cochain(complex_, ("1/2", "1/2", "1/2"))))
    assert certificate.value == Fraction(1, 2)
    integer_best = min(
        representative_mass(tuple(Fraction(1, 2) - step for step in (f[1] - f[0], f[2] - f[1], f[2] - f[0])))
        for f in product(range(-5, 6), repeat=3)
    )
    assert integer_best == Fraction(3, 2)


def test_weak_duality_for_every_admissible_circulation_on_a_grid() -> None:
    complex_ = square()
    for values in ((1, 0, 0, 0, 0), (1, 0, 1, 0, 0), (2, -1, 1, 3, 0), ("1/3", 0, 0, "-1/2", 1)):
        phi = accepted(exact_quotient_l1(complex_, cochain(complex_, values))).value
        delta = tuple(Fraction(value) for value in values)
        steps = tuple(Fraction(k, 4) for k in range(-4, 5))
        for a, b in product(steps, repeat=2):
            y = tuple(a * p + b * q for p, q in zip(C1, C2))
            assert all(value == 0 for value in d0_adjoint(complex_, cochain(complex_, y)).values())
            if all(abs(value) <= 1 for value in y):
                assert dual_bound(d0_matrix(complex_), len(complex_.vertices), delta, (Fraction(1),)*len(delta), y) <= phi


@pytest.mark.parametrize(
    ("faces", "norm", "classes"),
    [
        (((0, 1, 2),), 1, set(DiagnosticClass)),
        (((0, 1, 2), (0, 2, 3)), 2, {DiagnosticClass.EXACT_CLASS, DiagnosticClass.ACTIVE_CLOSURE_FAILURE}),
        ((), 0, {DiagnosticClass.EXACT_CLASS, DiagnosticClass.CLOSED_RESIDUAL}),
    ],
)
def test_theorem_e_and_class_partition_exhaustively(faces, norm, classes) -> None:
    complex_ = square(faces)
    seen = set()
    for values in product((-1, 0, 1), repeat=5):
        h = cochain(complex_, values)
        signature = accepted(obstruction_signature(complex_, h, closure_declared=True))
        phi, gamma = signature.phi1, signature.gamma2
        assert_exact(phi, gamma, signature.d1_opnorm)
        assert phi >= 0 and gamma >= 0 and signature.d1_opnorm == norm
        assert (phi == 0) == isinstance(solve_potential(complex_, h), Accepted)
        assert (gamma == 0) == is_closed(complex_, h)
        assert gamma <= norm * phi
        assert (signature.closure_ratio is None) == (phi == 0)
        if signature.closure_ratio is not None:
            assert 0 <= signature.closure_ratio <= norm
        memberships = (phi == 0, phi > 0 and gamma == 0, gamma > 0)
        assert sum(memberships) == 1
        assert signature.diagnostic_class is classify_signature(phi, gamma)
        seen.add(signature.diagnostic_class)
    assert seen == classes


def test_no_positive_lower_closure_bound_when_first_cohomology_is_nonzero() -> None:
    complex_ = triangle(False)
    signature = accepted(obstruction_signature(complex_, cochain(complex_, (1, 0, 0)), closure_declared=True))
    assert (signature.phi1, signature.gamma2, signature.d1_opnorm) == (1, 0, 0)
    assert signature.diagnostic_class is DiagnosticClass.CLOSED_RESIDUAL
    assert signature.closure_ratio == 0
    for c in (Fraction(1), Fraction(1, 2), Fraction(1, 1000)):
        assert not signature.gamma2 >= c * signature.phi1


@pytest.mark.parametrize("declared", [False, None, 1, "yes", Fraction(1)])
def test_undeclared_closure_data_is_refused_not_classified(declared) -> None:
    complex_ = triangle()
    refused(
        obstruction_signature(complex_, cochain(complex_, (1, 1, 0)), closure_declared=declared),
        RefusalCode.NO_RULE,
    )


def test_classifier_boundaries() -> None:
    assert classify_signature(Fraction(0), Fraction(0)) is DiagnosticClass.EXACT_CLASS
    assert classify_signature(Fraction(1), Fraction(0)) is DiagnosticClass.CLOSED_RESIDUAL
    assert classify_signature(Fraction(1), Fraction(1)) is DiagnosticClass.ACTIVE_CLOSURE_FAILURE


@pytest.mark.parametrize(
    ("values", "weights"),
    [
        ({(0, 1): 1, (1, 2): 1}, None),
        ({(0, 1): 1.0, (1, 2): 1, (0, 2): 0}, None),
        ({(0, 1): 1, (1, 2): 1, (0, 2): 0}, {(0, 1): 1, (1, 2): 0, (0, 2): 1}),
        ({(0, 1): 1, (1, 2): 1, (0, 2): 0}, {(0, 1): 1, (1, 2): -2, (0, 2): 1}),
        ({(0, 1): 1, (1, 2): 1, (0, 2): 0}, {(0, 1): 0.5, (1, 2): 1, (0, 2): 1}),
        ({(0, 1): 1, (1, 2): 1, (0, 2): 0}, {(0, 1): 1, (1, 2): 1}),
    ],
)
def test_quotient_and_signature_refuse_invalid_data(values, weights) -> None:
    refused(exact_quotient_l1(triangle(), values, weights), RefusalCode.INVALID_INPUT)
    refused(obstruction_signature(triangle(), values, closure_declared=True, weights=weights), RefusalCode.INVALID_INPUT)


def test_quotient_refuses_a_non_complex_and_an_exhausted_budget() -> None:
    refused(exact_quotient_l1("triangle", {}), RefusalCode.INVALID_INPUT)
    complex_ = triangle()
    refused(exact_quotient_l1(complex_, cochain(complex_, (1, 1, 0)), max_pivots=0), RefusalCode.BUDGET_EXHAUSTED)


def test_weighted_quotient_and_reverse_oriented_weight_keys() -> None:
    complex_ = triangle(False)
    weights = {(1, 0): 1, (2, 1): 3, (0, 2): "2"}
    assert accepted(edge_weights(complex_, weights)) == (1, 3, 2)
    assert accepted(edge_weights(complex_, None)) == (1, 1, 1)
    certificate = accepted(exact_quotient_l1(complex_, cochain(complex_, (1, 1, 0)), weights))
    assert certificate.value == 2
    assert certificate.dual == (1, 1, -1)
    signature = accepted(
        obstruction_signature(complex_, cochain(complex_, (1, 1, 0)), closure_declared=True, weights=weights)
    )
    assert signature.phi1 == 2 and signature.diagnostic_class is DiagnosticClass.CLOSED_RESIDUAL


def test_theorem_e_bound_violation_is_refused(monkeypatch) -> None:
    monkeypatch.setattr(obstruction, "d1_operator_norm_1to1", lambda complex_: Fraction(0))
    complex_ = triangle()
    refused(
        obstruction_signature(complex_, cochain(complex_, (1, 1, 0)), closure_declared=True),
        RefusalCode.CERTIFICATE_MISMATCH,
        "Gamma_2",
    )


def _square_certificate() -> QuotientCertificate:
    complex_ = square()
    return accepted(exact_quotient_l1(complex_, cochain(complex_, (1, 0, 0, 0, 0))))


def _fractions(values) -> tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in values)


@pytest.mark.parametrize(
    ("field", "value", "fragment"),
    [
        ("residual", _fractions((0, 0, 0, 0, 1)), "residual"),
        ("cochain", _fractions((2, 0, 0, 0, 0)), "residual"),
        ("potential", _fractions((0, 0, 0, 5)), "residual"),
        ("value", Fraction(3), "weighted primal residual norm"),
        ("weights", _fractions((2, 2, 2, 2, 2)), "weighted primal residual norm"),
        ("weights", _fractions((1, 1, 0, 1, 1)), "positive"),
        ("dual", tuple(p + 5 * q for p, q in zip(_fractions(C1), _fractions(C2))), "weighted dual bound"),
        ("dual", _fractions((1, 0, 0, 0, 0)), "annihilate im(d0)"),
        ("dual", _fractions((0, 0, 0, 0, 0)), "dual pairing"),
        ("dual", _fractions((1, 1, 0, 0)), "aligned"),
        ("potential", _fractions((0, 0, 0)), "aligned"),
        ("value", 1.0, "exact Fractions"),
        ("value", True, "exact Fractions"),
        ("potential", (0, 0, 0, 0), "exact Fractions"),
        ("dual", [Fraction(1)] * 5, "exact Fractions"),
    ],
    ids=[
        "residual",
        "cochain",
        "potential-shift",
        "value",
        "weights-scaled",
        "weights-zero",
        "dual-oversized",
        "dual-divergent",
        "dual-zero",
        "dual-short",
        "potential-short",
        "value-float",
        "value-bool",
        "potential-int",
        "dual-list",
    ],
)
def test_every_graph_certificate_field_is_recomputed(field, value, fragment) -> None:
    pristine = _square_certificate()
    assert accepted(verify_quotient_certificate(pristine)) == pristine
    refused(verify_quotient_certificate(replace(pristine, **{field: value})), RefusalCode.CERTIFICATE_MISMATCH, fragment)


def test_certificate_verifier_refuses_non_certificates() -> None:
    refused(verify_quotient_certificate("certificate"), RefusalCode.INVALID_INPUT)
    refused(verify_quotient_certificate(replace(_square_certificate(), complex_="K")), RefusalCode.INVALID_INPUT)
    refused(verify_matrix_certificate("certificate"), RefusalCode.INVALID_INPUT)


def _matrix_certificate() -> MatrixQuotientCertificate:
    return accepted(matrix_quotient_l1(d0_matrix(square()), (1, 0, 0, 0, 0), (1, 1, 1, 1, 1)))


@pytest.mark.parametrize(
    ("field", "value", "fragment"),
    [
        ("residual", _fractions((0, 0, 0, 0, 1)), "residual"),
        ("value", Fraction(5), "weighted primal residual norm"),
        ("weights", _fractions((1, -1, 1, 1, 1)), "positive"),
        ("dual", tuple(p + 5 * q for p, q in zip(_fractions(C1), _fractions(C2))), "weighted dual bound"),
        ("dual", _fractions((1, 0, 0, 0, 0)), "annihilate im(d0)"),
        ("dual", _fractions((0, 0, 0, 0, 0)), "dual pairing"),
        ("columns", 3, "shapes"),
        ("delta", _fractions((1, 0, 0)), "shapes"),
        ("matrix", ((1, 0, 0, 0),), "exact Fractions"),
        ("columns", "4", ""),
    ],
)
def test_every_matrix_certificate_field_is_recomputed(field, value, fragment) -> None:
    pristine = _matrix_certificate()
    assert accepted(verify_matrix_certificate(pristine)) == pristine
    outcome = verify_matrix_certificate(replace(pristine, **{field: value}))
    assert isinstance(outcome, Refused) and fragment in outcome.detail


def test_matrix_quotient_edge_shapes_and_refusals() -> None:
    no_rows = accepted(matrix_quotient_l1((), (), columns=2))
    assert (no_rows.value, no_rows.potential) == (0, (0, 0))
    no_columns = accepted(matrix_quotient_l1(((), ()), (3, "-1/2")))
    assert no_columns.value == Fraction(7, 2) and no_columns.dual == (1, -1)
    weighted = accepted(matrix_quotient_l1(((1,), (1,)), (0, 4), (1, 3)))
    assert weighted.value == 4 and weighted.potential == (4,)
    for arguments, keywords in (
        (((1.0,),), {}),
        (((1, 0), (1,)), {}),
        (((1,),), {"columns": 2}),
        (((1,),), {"columns": -1}),
        (((1,),), {"columns": True}),
    ):
        refused(matrix_quotient_l1(arguments, (1,) * len(arguments), **keywords), RefusalCode.INVALID_INPUT)
    refused(matrix_quotient_l1(((1,),), (1, 2)), RefusalCode.INVALID_INPUT)
    refused(matrix_quotient_l1(((1,),), "1"), RefusalCode.INVALID_INPUT)
    refused(matrix_quotient_l1("matrix", (1,)), RefusalCode.INVALID_INPUT)
    refused(matrix_quotient_l1(((1,),), (1,), (0,)), RefusalCode.INVALID_INPUT)
    refused(matrix_quotient_l1(((1,),), (1,), (1, 1)), RefusalCode.INVALID_INPUT)
    refused(matrix_quotient_l1(((1,),), (1,), max_pivots=0), RefusalCode.BUDGET_EXHAUSTED)


def assert_lp_certificate(costs, matrix, rhs, solution) -> None:
    c = _fractions(costs)
    b = _fractions(rhs)
    a = tuple(_fractions(row) for row in matrix)
    x, y = solution.primal, solution.dual
    assert_exact(x, y, solution.value)
    assert all(value >= 0 for value in x)
    assert all(sum(p * q for p, q in zip(row, x)) == target for row, target in zip(a, b))
    for j, cost in enumerate(c):
        assert sum(row[j] * yi for row, yi in zip(a, y)) <= cost
    assert sum(p * q for p, q in zip(c, x)) == solution.value == sum(p * q for p, q in zip(b, y))


@pytest.mark.parametrize(
    ("costs", "matrix", "rhs", "value"),
    [
        ((2, 1, 0), ((1, 1, -1),), (2,), 2),
        ((2,), ((-1,),), (-3,), 6),
        ((1, 1), ((1, -1), (-1, 1)), (0, 0), 0),
        ((1, 2), (), (), 0),
        ((), ((), ()), (0, 0), 0),
        (("1/3", 1, "1/2"), ((1, 1, 0), (0, 1, 1), (1, 2, 1)), (1, 1, 2), Fraction(5, 6)),
    ],
)
def test_two_phase_simplex_returns_a_complementary_certificate(costs, matrix, rhs, value) -> None:
    solution = accepted(solve_standard_lp(costs, matrix, rhs))
    assert solution.value == value
    assert_lp_certificate(costs, matrix, rhs, solution)


@pytest.mark.parametrize(
    ("costs", "matrix", "rhs", "keywords", "code"),
    [
        ((1,), ((1,), (1,)), (1, 2), {}, RefusalCode.INFEASIBLE),
        ((), ((),), (1,), {}, RefusalCode.INFEASIBLE),
        ((-1, -1), ((1, -1),), (1,), {}, RefusalCode.UNBOUNDED),
        ((-1,), (), (), {}, RefusalCode.UNBOUNDED),
        ((1.0,), ((1,),), (1,), {}, RefusalCode.INVALID_INPUT),
        ((1,), ((1, 1),), (1,), {}, RefusalCode.INVALID_INPUT),
        ((1,), ((1,),), (1, 1), {}, RefusalCode.INVALID_INPUT),
        ((1,), ((1,),), (True,), {}, RefusalCode.INVALID_INPUT),
        ((1,), ((1,),), (1,), {"max_pivots": -1}, RefusalCode.INVALID_INPUT),
        ((1,), ((1,),), (1,), {"max_pivots": True}, RefusalCode.INVALID_INPUT),
        ((1,), ((1,),), (1,), {"max_pivots": 0}, RefusalCode.BUDGET_EXHAUSTED),
        ((0, -1), ((1, 1),), (1,), {"max_pivots": 1}, RefusalCode.BUDGET_EXHAUSTED),
    ],
)
def test_two_phase_simplex_typed_refusals(costs, matrix, rhs, keywords, code) -> None:
    refused(solve_standard_lp(costs, matrix, rhs, **keywords), code)


BEALE_COSTS = (0, 0, 0, Fraction(-3, 4), 20, Fraction(-1, 2), 6)
BEALE_MATRIX = (
    (1, 0, 0, Fraction(1, 4), -8, -1, 9),
    (0, 1, 0, Fraction(1, 2), -12, Fraction(-1, 2), 3),
    (0, 0, 1, 0, 0, 1, 0),
)
BEALE_RHS = (0, 0, 1)


def _beale_tableau() -> list[list[Fraction]]:
    top = [Fraction(value) for value in BEALE_COSTS] + [Fraction(0)]
    return [top] + [[Fraction(v) for v in row] + [Fraction(b)] for row, b in zip(BEALE_MATRIX, BEALE_RHS)]


def _largest_coefficient_rule(tableau, basis, budget) -> str:
    """Negative control: Dantzig entering plus least-index ties cycles on Beale's LP."""

    for _ in range(budget):
        entering = min(range(7), key=lambda j: (tableau[0][j], j))
        if tableau[0][entering] >= 0:
            return "optimal"
        ratios = [(row[-1] / row[entering], basis[i], i + 1) for i, row in enumerate(tableau[1:]) if row[entering] > 0]
        leaving = min(ratios)[2]
        obstruction._pivot(tableau, leaving, entering)
        basis[leaving - 1] = entering
    return "budget"


def test_blands_rule_terminates_on_beales_cycling_programme() -> None:
    solution = accepted(solve_standard_lp(BEALE_COSTS, BEALE_MATRIX, BEALE_RHS))
    assert solution.value == Fraction(-5, 4)
    assert solution.primal == _fractions(("3/4", 0, 0, 1, 0, 1, 0))
    assert_lp_certificate(BEALE_COSTS, BEALE_MATRIX, BEALE_RHS, solution)
    tableau = _beale_tableau()
    status, pivots = obstruction._simplex(tableau, [0, 1, 2], 7, 100)
    assert status == "optimal" and pivots <= 10
    assert -tableau[0][-1] == Fraction(-5, 4)
    assert _largest_coefficient_rule(_beale_tableau(), [0, 1, 2], 60) == "budget"


def test_d0_adjoint_divergence_and_operator_norms() -> None:
    complex_ = triangle()
    assert d0_adjoint(complex_, cochain(complex_, (1, 1, -1))) == {0: 0, 1: 0, 2: 0}
    assert d0_adjoint(complex_, {(1, 0): 1, (1, 2): 0, (0, 2): 0}) == {0: 1, 1: -1, 2: 0}
    with pytest.raises(ValueError):
        d0_adjoint(complex_, {(0, 1): 1})
    assert d1_operator_norm_1to1(complex_) == 1
    assert d1_operator_norm_1to1(square(((0, 1, 2), (0, 2, 3)))) == 2
    assert d1_operator_norm_1to1(triangle(False)) == 0
    assert_exact(d1_operator_norm_1to1(complex_), d1_operator_norm_1to1(triangle(False)))


PROMOTION_TARGETS = tuple(sorted(ROUTING_TERMINALS)) + (
    "authority",
    "standing",
    "VerifiedPromotion",
    "repair_action",
    "stabilization_receipt",
    "",
    ["unhashable"],
)


PROMOTION_IDS = [target if isinstance(target, str) and target else f"target{index}" for index, target in enumerate(PROMOTION_TARGETS)]


@pytest.mark.parametrize("target", PROMOTION_TARGETS, ids=PROMOTION_IDS)
def test_diagnostic_evidence_is_never_promoted(target) -> None:
    complex_ = triangle()
    signature = accepted(obstruction_signature(complex_, cochain(complex_, (1, 1, 0)), closure_declared=True))
    for evidence in (signature, signature.certificate, _matrix_certificate()):
        refusal = refused(promote_diagnostic(evidence, target), RefusalCode.SCOPE_VIOLATION, "diagnostic evidence")
        assert refusal.authority_effect is AuthorityEffect.NONE
    kind = "routing terminal" if isinstance(target, str) and target in ROUTING_TERMINALS else "authority"
    assert kind in promote_diagnostic(signature, target).detail


def test_promotion_firewall_input_and_signature_authority_guard() -> None:
    refused(promote_diagnostic("signature", "ExactRepair"), RefusalCode.INVALID_INPUT)
    complex_ = triangle()
    signature = accepted(obstruction_signature(complex_, cochain(complex_, (1, 1, 0)), closure_declared=True))
    assert signature.authority_effect is AuthorityEffect.NONE
    assert not any(hasattr(signature, name) for name in ("route", "terminal", "authority", "standing", "repair"))
    with pytest.raises(ValueError, match="authority"):
        ObstructionSignature(
            signature.phi1,
            signature.gamma2,
            signature.closure_ratio,
            signature.d1_opnorm,
            signature.diagnostic_class,
            signature.certificate,
            "Operational",
        )
# Executable finite evidence; AuthorityEffect: None.
