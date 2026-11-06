"""Finite replay and independent exact-arithmetic boundary regressions."""
from dataclasses import replace

import pytest
from finite_obstruction import (
    Diagnostic,
    ExactnessCertificate,
    FiniteObstructionPacket,
    FiniteRepairMove,
    FiniteRepairRegistry,
    LinearRepairProblem,
    QuotientDistanceCertificate,
    RepairDisposition,
    TerminalRoute,
    _exact_matrix,
    _exact_vector,
    as_rational,
    diagnose,
    exact_equal,
    terminal_route,
    transport_residuals,
    weighted_l1_operator_norm,
)
from sympy import Float, Matrix, Rational, sqrt


def packet():
    return FiniteObstructionPacket.create([[1], [0]], [[0, 0]], Matrix.zeros(1, 0), [1, 1], [1])


def test_replay_binds_concrete_corrections_and_every_receipt_field():
    registry = FiniteRepairRegistry(packet(), (0, 1), "scope", (FiniteRepairMove("m", (1, 0)),))
    result, evidence = registry.replay(2)
    assert terminal_route(result, evidence, registry=registry) is TerminalRoute.STABILIZED_SURVIVOR
    for change in (
        {"completeness_receipt_digest": "a" * 64}, {"bindings_digest": "b" * 64},
        {"evaluator_id": "unknown"}, {"registry_scope": "other"}, {"budget_spent": 0},
        {"budget_limit": True}, {"budget_spent": True}, {"budget_limit": 0},
        {"registry_entries": ("m", "m")},
        {"checks": (replace(evidence.checks[0], witness_digest="c" * 64),)},
        {"checks": evidence.checks * 2},
    ):
        assert not replace(evidence, **change).valid_for(result, registry)
    changed_registry = replace(registry, moves=(FiniteRepairMove("m", (0, -1)),))
    assert not evidence.valid_for(result, changed_registry)
    _, repair = changed_registry.replay(2)
    assert repair.checks[0].disposition is RepairDisposition.REPAIR_AVAILABLE
    assert terminal_route(result, repair, registry=changed_registry) is TerminalRoute.OPEN_OBSTRUCTION
    forged = replace(result, phi1=replace(result.phi1, value=Rational(99)))
    assert not evidence.valid_for(forged, registry)


@pytest.mark.parametrize("budget", [0, -1, True, "1"])
def test_replay_requires_sufficient_integer_budget(budget):
    registry = FiniteRepairRegistry(packet(), (0, 1), "scope", (FiniteRepairMove("m", (0, 0)),))
    with pytest.raises(ValueError, match="budget"):
        registry.replay(budget)


def test_finite_registry_shape_identity_and_exactness():
    from types import SimpleNamespace

    with pytest.raises(TypeError, match="immutable"):
        FiniteRepairRegistry(packet(), (0, 1), "s", (SimpleNamespace(move_id="m", correction=[0, 0]),))
    with pytest.raises(TypeError, match="immutable"):
        FiniteRepairRegistry(SimpleNamespace(), (0, 1), "s", ())
    with pytest.raises(ValueError, match="move_id"):
        FiniteRepairMove("", (0,))
    with pytest.raises(TypeError):
        FiniteRepairMove("float", (0.1,))
    move = FiniteRepairMove("m", (0, 0))
    for scope, moves, defect in [("", (move,), (0, 1)), ("s", (), (0, 1)),
                                 ("s", (move, move), (0, 1)), ("s", (move,), (0,))]:
        with pytest.raises(ValueError):
            FiniteRepairRegistry(packet(), defect, scope, moves)
    with pytest.raises(ValueError, match="inhabit"):
        FiniteRepairRegistry(packet(), (0, 1), "s", (FiniteRepairMove("m", (0,)),))
    original = Matrix([[1], [0]])
    p = FiniteObstructionPacket.create(original, [[0, 0]], Matrix.zeros(1, 0), [1, 1], [1])
    original[0] = 7
    assert p.d0[0] == 1
    with pytest.raises(TypeError):
        p.d0[0] = 7


def test_norm_two_transport_can_double_the_leftover():
    p = packet()
    assert transport_residuals(p, p, [[2]], Matrix.eye(2)*2, [[2]], Matrix.zeros(0, 0)) == (0, 0, 0)
    bound = weighted_l1_operator_norm(Matrix.eye(2)*2, [1, 1], [1, 1])
    assert bound == 2
    assert diagnose(p, [0, 2]).phi1.value == bound * diagnose(p, [0, 1]).phi1.value == 2


@pytest.mark.parametrize("bad", [True, 0.1, Float("0.1"), sqrt(2), object()])
def test_exact_scalar_api_rejects_inexact_or_uninterpreted_inputs(bad):
    with pytest.raises(TypeError):
        as_rational(bad)


def test_exact_membership_and_separator_replay():
    assert as_rational("3/7") == Rational(3, 7)
    assert not exact_equal(Matrix([1]), Matrix([1, 2]))
    problem = LinearRepairProblem(Matrix([[1], [0]]))
    repair = problem.exactness_certificate(Matrix([3, 0]))
    assert repair.verify()
    assert not replace(repair, witness=None).verify()
    obstruction = problem.exactness_certificate(Matrix([0, 2]))
    assert obstruction.verify()
    assert not replace(obstruction, separating_pairing=None).verify()
    assert not replace(obstruction, separating_pairing=Rational(0)).verify()
    with pytest.raises(ValueError, match="shape"):
        problem.exactness_certificate(Matrix([1]))
    with pytest.raises(ValueError, match="shape"):
        problem.quotient_l1_distance(Matrix([1]))
    empty = LinearRepairProblem(Matrix.zeros(0, 0)).quotient_l1_distance(Matrix.zeros(0, 1))
    assert empty.verify() and empty.distance == 0


def test_rank_selection_skips_dependent_columns_and_refuses_false_rank():
    from finite_obstruction import _independent_column_indices

    assert _independent_column_indices(Matrix([[0, 1]]), 1) == (1,)
    with pytest.raises(ArithmeticError, match="independent-column"):
        _independent_column_indices(Matrix.zeros(1, 1), 1)


def test_verifier_rejects_floating_point_counterexample():
    # Peer review finding P1:
    # A = (1, 1)^T, x = (2^60, 2^60 + 1)^T. Exact quotient distance is 1.
    # In float arithmetic, Float(2^60, 15) erases the coordinate difference.
    A = Matrix([[1], [1]])
    x = Matrix([[2**60], [2**60 + 1]])
    w_float = Matrix([Float(2**60, 15)])

    # Constructing certificates with floats is rejected at boundaries
    with pytest.raises(TypeError, match="Floating-point"):
        ExactnessCertificate(
            is_exact_coboundary=True,
            cochain=x,
            repair_map=A,
            witness=w_float,
            separating_left_kernel_vector=None,
            separating_pairing=None,
        )

    with pytest.raises(TypeError, match="Floating-point"):
        QuotientDistanceCertificate(
            distance=Rational(0),
            repair_witness=w_float,
            residual=Matrix.zeros(2, 1),
            cochain=x,
            dual_witness=Matrix.zeros(2, 1),
            dual_pairing=Rational(0),
            repair_map=A,
        )

    # Even if an unvalidated certificate contains floats, verify() rejects it before arithmetic
    cert_raw = object.__new__(ExactnessCertificate)
    object.__setattr__(cert_raw, "is_exact_coboundary", True)
    object.__setattr__(cert_raw, "cochain", x)
    object.__setattr__(cert_raw, "repair_map", A)
    object.__setattr__(cert_raw, "witness", w_float)
    object.__setattr__(cert_raw, "separating_left_kernel_vector", None)
    object.__setattr__(cert_raw, "separating_pairing", None)

    with pytest.raises(TypeError, match="Floating-point"):
        cert_raw.verify()

    # Exact rational problem correctly finds distance == 1
    problem = LinearRepairProblem(A)
    qd_cert = problem.quotient_l1_distance(x)
    assert qd_cert.distance == 1
    assert qd_cert.verify()


def test_terminal_route_rejects_forged_exact_repair():
    # Peer review finding P1:
    # Starting with a genuine coherent residual (phi1.value > 0), forging the diagnostic
    # to EXACT_REPAIR, value to 0, and residual to 0 must route to OPEN_OBSTRUCTION.
    # Terminal routing requires problem-bound verification before accepting EXACT_REPAIR.
    p = packet()
    coherent_result = diagnose(p, [0, 1])
    assert coherent_result.diagnostic is Diagnostic.COHERENT_RESIDUAL
    assert coherent_result.phi1.value == 1

    forged = replace(coherent_result, diagnostic=Diagnostic.EXACT_REPAIR)
    assert terminal_route(forged, None) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(forged, None, packet=p, defect=[0, 1]) is TerminalRoute.OPEN_OBSTRUCTION

    # Forged zero-value and zero-residual coherent residual
    forged_zeroed = replace(
        coherent_result,
        diagnostic=Diagnostic.EXACT_REPAIR,
        phi1=replace(
            coherent_result.phi1,
            value=Rational(0),
            residual=Matrix.zeros(2, 1),
            duality_gap=Rational(0),
        ),
    )
    assert terminal_route(forged_zeroed, None) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(forged_zeroed, None, packet=p, defect=[0, 1]) is TerminalRoute.OPEN_OBSTRUCTION

    # Exact result without problem-bound verification routes to OPEN_OBSTRUCTION
    exact_result = diagnose(p, [1, 0])
    assert exact_result.diagnostic is Diagnostic.EXACT_REPAIR
    assert terminal_route(exact_result, None) is TerminalRoute.OPEN_OBSTRUCTION
    # With problem-bound verification, it routes to EXACT_REPAIR
    assert terminal_route(exact_result, None, packet=p, defect=[1, 0]) is TerminalRoute.EXACT_REPAIR
    exact_reg = FiniteRepairRegistry(p, (1, 0), "exact-scope", (FiniteRepairMove("m1", (0, 0)),))
    assert terminal_route(exact_result, None, registry=exact_reg) is TerminalRoute.EXACT_REPAIR

    forged_exact = replace(
        exact_result,
        phi1=replace(exact_result.phi1, residual=Matrix([1, 0])),
    )
    assert terminal_route(forged_exact, None, packet=p, defect=[1, 0]) is TerminalRoute.OPEN_OBSTRUCTION


def test_returned_certificate_matrices_are_immutable():
    # Peer review finding P2:
    # Returned certificate matrices must be ImmutableMatrix to prevent mutation.
    p = packet()
    result = diagnose(p, [0, 1])
    with pytest.raises(TypeError):
        result.phi1.residual[1] = 999
    with pytest.raises(TypeError):
        result.phi1.repair[0] = 999
    with pytest.raises(TypeError):
        result.phi1.annihilator[0] = 999


def test_input_conversion_shapes_and_empty_carriers():
    # Peer review finding P2:
    # 1. 2D array cannot be silently flattened into a vector
    import numpy as np

    with pytest.raises(ValueError, match="expected vector"):
        _exact_vector(np.eye(2, dtype=int))

    # 2. Empty-row matrix preserves its declared domain (0, 2)
    m02 = _exact_matrix(np.zeros((0, 2), dtype=int))
    assert m02.shape == (0, 2)

    # 3. Empty weights [] normalize to (0, 1), supporting 0-dimensional carriers
    assert _exact_vector([]).shape == (0, 1)
    assert _exact_vector(np.zeros(0, dtype=int)).shape == (0, 1)

    # 4. Empty SymPy matrices with zero columns and >1 rows must raise ValueError
    with pytest.raises(ValueError, match="expected vector"):
        _exact_vector(Matrix.zeros(2, 0))
    with pytest.raises(ValueError, match="expected vector"):
        _exact_vector(Matrix.zeros(0, 2))
    with pytest.raises(ValueError, match="expected vector"):
        _exact_vector(np.zeros((2, 0), dtype=int))
    with pytest.raises(ValueError, match="expected vector"):
        diagnose(packet(), Matrix.zeros(2, 0))

    p0 = FiniteObstructionPacket.create(
        Matrix.zeros(0, 0), Matrix.zeros(0, 0), Matrix.zeros(0, 0), [], []
    )
    assert p0.w1.shape == (0, 1)
    assert p0.w2.shape == (0, 1)
    res0 = diagnose(p0, [])
    assert res0.diagnostic is Diagnostic.EXACT_REPAIR
    assert res0.phi1.value == 0
    assert terminal_route(res0, None) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(res0, None, packet=p0, defect=[]) is TerminalRoute.EXACT_REPAIR


def test_survivor_routing_rejects_conflicting_problem_data():
    # Peer review finding P2:
    # Genuine survivor evidence for (0, 1) with registry must reject conflicting explicit arguments:
    # 1. Supplying defect=[1, 0] (which contradicts registry.defect) must route to OPEN_OBSTRUCTION.
    # 2. Supplying a conflicting packet must route to OPEN_OBSTRUCTION.
    # 3. Supplying consistent explicit arguments must route to STABILIZED_SURVIVOR.
    p = packet()
    registry = FiniteRepairRegistry(p, (0, 1), "scope", (FiniteRepairMove("m", (1, 0)),))
    result, evidence = registry.replay(2)
    assert result.diagnostic is Diagnostic.COHERENT_RESIDUAL
    assert terminal_route(result, evidence, registry=registry) is TerminalRoute.STABILIZED_SURVIVOR

    # Conflicting defect
    assert (
        terminal_route(result, evidence, registry=registry, defect=[1, 0])
        is TerminalRoute.OPEN_OBSTRUCTION
    )
    assert (
        terminal_route(result, evidence, registry=registry, defect=iter([1, 0]))
        is TerminalRoute.OPEN_OBSTRUCTION
    )

    # Conflicting packet
    conflicting_packet = FiniteObstructionPacket.create(
        [[2], [0]], [[0, 0]], Matrix.zeros(1, 0), [1, 1], [1]
    )
    assert (
        terminal_route(result, evidence, registry=registry, packet=conflicting_packet)
        is TerminalRoute.OPEN_OBSTRUCTION
    )

    # Consistent explicit arguments succeed
    assert (
        terminal_route(result, evidence, registry=registry, packet=p, defect=[0, 1])
        is TerminalRoute.STABILIZED_SURVIVOR
    )
    assert (
        terminal_route(result, evidence, registry=registry, packet=p, defect=iter([0, 1]))
        is TerminalRoute.STABILIZED_SURVIVOR
    )


def test_exact_routing_accepts_iterator_defect_inputs():
    # Peer review finding P2:
    # Exact routing must not consume iterator defect inputs twice.
    # Iterator or generator passed as defect must route to EXACT_REPAIR, matching list input.
    p = packet()
    exact_result = diagnose(p, [1, 0])
    assert exact_result.diagnostic is Diagnostic.EXACT_REPAIR

    # List defect routes to EXACT_REPAIR
    assert terminal_route(exact_result, None, packet=p, defect=[1, 0]) is TerminalRoute.EXACT_REPAIR

    # Iterator defect must route to EXACT_REPAIR (not OPEN_OBSTRUCTION from exhausted iterator)
    assert (
        terminal_route(exact_result, None, packet=p, defect=iter([1, 0]))
        is TerminalRoute.EXACT_REPAIR
    )

    # Generator defect must also route to EXACT_REPAIR
    assert (
        terminal_route(exact_result, None, packet=p, defect=(v for v in [1, 0]))
        is TerminalRoute.EXACT_REPAIR
    )


