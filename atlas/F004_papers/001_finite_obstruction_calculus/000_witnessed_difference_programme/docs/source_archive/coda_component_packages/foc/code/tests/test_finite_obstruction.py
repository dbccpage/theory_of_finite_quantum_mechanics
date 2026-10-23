"""Exact rational test suite for CODA-FOC.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e).
Verifies: FOC-D1, FOC-T1, FOC-T2, FOC-C1, FOC-D2, FOC-T3, FOC-P1, FOC-T4, FOC-T5, FOC-NC1.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace

import numpy as np
import pytest
from finite_obstruction import (
    Diagnostic,
    FiniteObstructionPacket,
    FiniteRepairMove,
    FiniteRepairRegistry,
    RepairCheck,
    RepairDisposition,
    StabilizationEvidence,
    TerminalRoute,
    diagnose,
    direct_sum,
    is_full_subspace_annihilator,
    quotient_certificate,
    terminal_route,
    transport_residuals,
    weighted_l1_operator_norm,
)
from sympy import Matrix, Rational


def coherent_packet() -> FiniteObstructionPacket:
    return FiniteObstructionPacket.create(
        d0=[[1], [0]],
        d1=[[0, 0]],
        a2=Matrix.zeros(1, 0),
        w1=[1, 1],
        w2=[1],
    )


def nonclosed_packet() -> FiniteObstructionPacket:
    return FiniteObstructionPacket.create(
        d0=[[1], [0]],
        d1=[[0, 1]],
        a2=Matrix.zeros(1, 0),
        w1=[1, 1],
        w2=[2],
    )


@pytest.mark.parametrize(
    ("packet", "defect", "expected"),
    [
        (coherent_packet(), [3, 0], Diagnostic.EXACT_REPAIR),
        (coherent_packet(), [0, 4], Diagnostic.COHERENT_RESIDUAL),
        (nonclosed_packet(), [0, 4], Diagnostic.NONCLOSED_DEFECT),
    ],
)
def test_total_trichotomy(packet, defect, expected) -> None:
    result = diagnose(packet, defect)
    assert result.diagnostic is expected
    assert result.authority_effect == "None"
    assert result.phi1.authority_effect == "None"
    assert len(result.phi1.input_digest) == 64
    assert len(result.input_digest) == 64
    assert result.phi1.duality_gap == 0
    assert result.gamma2.duality_gap == 0


def test_l1_l2_counterexample() -> None:
    # A = (1, 1, 1)^T, x = (0, 0, 10), w = (1, 1, 1)
    # L1 quotient distance is 10, whereas L2 projection would predict 40/3 in L1 norm.
    certificate = quotient_certificate(
        Matrix([[1], [1], [1]]), [0, 0, 10], [1, 1, 1]
    )
    assert certificate.value == Rational(10)
    assert certificate.value != Rational(40, 3)
    assert certificate.duality_gap == Rational(0)
    assert is_full_subspace_annihilator(Matrix([[1], [1], [1]]), certificate.annihilator)


def test_zero_and_negative_weight_is_refused() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        quotient_certificate(Matrix.zeros(2, 0), [0, 1], [1, 0])
    with pytest.raises(ValueError, match="strictly positive"):
        quotient_certificate(Matrix.zeros(2, 0), [0, 1], [1, -1])


def test_generator_closure_counterexample() -> None:
    generator_only = Matrix([[1], [0]])
    full_repair_subspace = Matrix.eye(2)
    functional = [0, 1]
    assert is_full_subspace_annihilator(generator_only, functional)
    assert not is_full_subspace_annihilator(full_repair_subspace, functional)


def test_direct_sum_additivity() -> None:
    left = coherent_packet()
    right = nonclosed_packet()
    combined = direct_sum(left, right)
    left_result = diagnose(left, [0, 2])
    right_result = diagnose(right, [0, 3])
    combined_result = diagnose(combined, [0, 2, 0, 3])
    assert combined_result.phi1.value == left_result.phi1.value + right_result.phi1.value
    assert combined_result.gamma2.value == left_result.gamma2.value + right_result.gamma2.value


def test_identity_transport_and_norm() -> None:
    packet = nonclosed_packet()
    t0 = Matrix.eye(1)
    t1 = Matrix.eye(2)
    t2 = Matrix.eye(1)
    s2 = Matrix.zeros(0, 0)
    assert transport_residuals(packet, packet, t0, t1, t2, s2) == (Rational(0), Rational(0), Rational(0))
    assert weighted_l1_operator_norm(t1, packet.w1, packet.w1) == Rational(1)


def test_transport_reports_broken_square() -> None:
    packet = nonclosed_packet()
    residuals = transport_residuals(
        packet, packet, Matrix.eye(1), 2 * Matrix.eye(2), Matrix.eye(1), Matrix.zeros(0, 0)
    )
    assert residuals[0] > 0 or residuals[1] > 0


def test_terminal_firewall() -> None:
    exact = diagnose(coherent_packet(), [1, 0])
    coherent = diagnose(coherent_packet(), [0, 1])
    nonclosed = diagnose(nonclosed_packet(), [0, 1])
    fabricated = StabilizationEvidence.create(
        coherent,
        registry_scope="finite-demo-scope",
        registry_entries=("move-A",),
        completeness_receipt_digest="a" * 64,
        evaluator_id="demo-evaluator-v1",
        budget_limit=1,
        budget_spent=1,
        checks=(
            RepairCheck(
                "move-A", RepairDisposition.NO_ADMISSIBLE_REPAIR, "b" * 64
            ),
        ),
        bindings_digest="c" * 64,
    )
    registry = FiniteRepairRegistry(
        coherent_packet(), (0, 1), "finite-demo-scope",
        (FiniteRepairMove("move-A", (1, 0)),),
    )
    replayed, complete = registry.replay(1)
    assert replayed == coherent
    assert terminal_route(coherent, fabricated, registry=registry) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(coherent, complete) is TerminalRoute.OPEN_OBSTRUCTION
    partial = replace(complete, bindings_digest="not-a-digest")
    available = replace(
        complete,
        checks=(
            RepairCheck("move-A", RepairDisposition.REPAIR_AVAILABLE, "b" * 64),
        ),
    )
    mismatched = replace(complete, input_digest="d" * 64)
    invalid_evidence = (
        replace(complete, authority_effect="Grant"),
        replace(complete, observer_digest="d" * 64),
        replace(complete, registry_scope=""),
        replace(complete, budget_spent=2),
        replace(complete, registry_entries=()),
        replace(complete, registry_digest="d" * 64),
        replace(complete, checks=()),
    )
    assert terminal_route(exact, None) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(exact, None, packet=coherent_packet(), defect=[1, 0]) is TerminalRoute.EXACT_REPAIR
    assert terminal_route(coherent, None) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(coherent, partial, registry=registry) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(coherent, available, registry=registry) is TerminalRoute.OPEN_OBSTRUCTION
    assert terminal_route(coherent, mismatched, registry=registry) is TerminalRoute.OPEN_OBSTRUCTION
    assert all(
        terminal_route(coherent, item, registry=registry) is TerminalRoute.OPEN_OBSTRUCTION
        for item in invalid_evidence
    )
    assert terminal_route(coherent, complete, registry=registry) is TerminalRoute.STABILIZED_SURVIVOR
    assert terminal_route(nonclosed, complete) is TerminalRoute.OPEN_OBSTRUCTION


def test_float_rejection_negative_paths() -> None:
    # Python binary floats are strictly rejected
    with pytest.raises(TypeError, match="Floating-point"):
        FiniteObstructionPacket.create([[1.0]], [[0]], Matrix.zeros(1, 0), [1], [1])
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(Matrix([[1]]), [1.0], [1])
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(Matrix([[1]]), [1], [1.0])
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate([[1.0]], [1], [1])
    with pytest.raises(TypeError, match="Floating-point"):
        diagnose(coherent_packet(), [0.0, 1.0])
    with pytest.raises(TypeError, match="Floating-point"):
        weighted_l1_operator_norm([[1.0]], [1], [1])
    with pytest.raises(TypeError, match="Floating-point"):
        is_full_subspace_annihilator([[1.0]], [1])

    # Numpy floating types are strictly rejected
    with pytest.raises(TypeError, match="Floating-point"):
        FiniteObstructionPacket.create(np.array([[1.0]]), [[0]], Matrix.zeros(1, 0), [1], [1])
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(Matrix([[1]]), np.array([1.0]), [1])

    # Booleans masquerading as numbers are strictly rejected
    with pytest.raises(TypeError, match="rejects bool"):
        quotient_certificate(Matrix([[1]]), [True], [1])


def test_fractions_and_rationals_accepted() -> None:
    # Exact fractions.Fraction and sympy.Rational are accepted
    packet = FiniteObstructionPacket.create(
        d0=[[Fraction(1, 2)], [0]],
        d1=[[0, 0]],
        a2=Matrix.zeros(1, 0),
        w1=[Fraction(1, 3), Rational(2, 3)],
        w2=[Rational(1)],
    )
    result = diagnose(packet, [Fraction(1, 4), Rational(0)])
    assert result.diagnostic is Diagnostic.EXACT_REPAIR
    assert result.phi1.value == Rational(0)


def test_invalid_packets_and_dimensions_are_refused() -> None:
    with pytest.raises(ValueError, match="matrices"):
        FiniteObstructionPacket.create([1], [[0]], Matrix.zeros(1, 0), [1], [1])
    with pytest.raises(ValueError, match="compose"):
        FiniteObstructionPacket.create([[1]], [[0, 0]], Matrix.zeros(1, 0), [1], [1])
    with pytest.raises(ValueError, match="weight dimensions"):
        FiniteObstructionPacket.create([[1]], [[0]], Matrix.zeros(1, 0), [1, 1], [1])
    with pytest.raises(ValueError, match="cochain"):
        FiniteObstructionPacket.create([[1]], [[1]], Matrix.zeros(1, 0), [1], [1])
    with pytest.raises(ValueError, match="strictly positive"):
        FiniteObstructionPacket.create([[1]], [[0]], Matrix.zeros(1, 0), [0], [1])
    with pytest.raises(ValueError, match="does not inhabit"):
        diagnose(coherent_packet(), [1])
    with pytest.raises(ValueError, match="dimensions"):
        is_full_subspace_annihilator(Matrix.eye(2), [1])
    with pytest.raises(ValueError, match="transport dimensions"):
        weighted_l1_operator_norm(Matrix.eye(2), [1], [1])
    with pytest.raises(ValueError, match="strictly positive"):
        weighted_l1_operator_norm(Matrix.eye(1), [0], [1])
    with pytest.raises(ValueError, match="quotient dimensions"):
        quotient_certificate(Matrix.eye(2), [1], [1, 1])


def test_edge_cases_and_type_guards() -> None:
    # m == 0 quotient certificate
    cert_empty = quotient_certificate(Matrix.zeros(0, 0), [], [])
    assert cert_empty.value == Rational(0)
    assert cert_empty.duality_gap == Rational(0)

    # 0-column transport operator norm
    norm_0col = weighted_l1_operator_norm(Matrix.zeros(2, 0), [], [1, 1])
    assert norm_0col == Rational(0)

    # Vector conversions: Matrix 1xN, numpy 1D int array
    cert_row = quotient_certificate(Matrix.eye(1), Matrix([[2]]), [1])
    assert cert_row.value == Rational(0)

    cert_np = quotient_certificate(Matrix.eye(1), np.array([2]), np.array([1]))
    assert cert_np.value == Rational(0)

    # Float tolerance rejection
    with pytest.raises(TypeError, match="Floating-point tolerance"):
        FiniteObstructionPacket.create([[1]], [[0]], Matrix.zeros(1, 0), [1], [1], tolerance=1e-5)
    with pytest.raises(TypeError, match="Floating-point tolerance"):
        coherent_packet().validate(tolerance=1e-5)
    with pytest.raises(TypeError, match="Floating-point tolerance"):
        quotient_certificate(Matrix.eye(1), [1], [1], tolerance=1e-5)
    with pytest.raises(TypeError, match="Floating-point tolerance"):
        diagnose(coherent_packet(), [1, 0], tolerance=1e-5)
    with pytest.raises(TypeError, match="Floating-point tolerance"):
        is_full_subspace_annihilator(Matrix.eye(1), [1], tolerance=1e-5)

    # Ragged matrix rows
    with pytest.raises(ValueError, match="equal length"):
        FiniteObstructionPacket.create([[1, 2], [3]], [[0]], Matrix.zeros(1, 0), [1, 1], [1])

    # Unsupported types
    with pytest.raises(TypeError, match="unsupported matrix type"):
        FiniteObstructionPacket.create(123, [[0]], Matrix.zeros(1, 0), [1], [1])
    with pytest.raises(TypeError, match="unsupported vector type"):
        FiniteObstructionPacket.create([[1]], [[0]], Matrix.zeros(1, 0), 123, [1])

    # MatrixBase with float
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(Matrix([[1.0]]), [1], [1])
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(Matrix.eye(1), Matrix([1.0]), [1])
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(Matrix.eye(1), Matrix([[1.0]]), [1])

    # 2D numpy float array
    with pytest.raises(TypeError, match="Floating-point"):
        quotient_certificate(np.array([[1.0]]), [1], [1])

    # 1D numpy non-2D matrix
    with pytest.raises(ValueError, match="matrices"):
        FiniteObstructionPacket.create(np.array([1]), [[0]], Matrix.zeros(1, 0), [1], [1])

    # 1xN row vector MatrixBase
    cert_row_vec = quotient_certificate(Matrix.eye(2), Matrix([[0, 0]]), [1, 1])
    assert cert_row_vec.value == Rational(0)

    # Generator vector
    cert_gen = quotient_certificate(Matrix.eye(2), (x for x in [0, 0]), [1, 1])
    assert cert_gen.value == Rational(0)

    # Scalar in digest
    from finite_obstruction import _digest_exact
    d_scalar = _digest_exact("test", Rational(1, 2), "string")
    assert len(d_scalar) == 64


def test_numpy_integer_matrix_empty_list_and_nonvector() -> None:
    # Invariant: 2-D integer ndarrays and empty nested lists are exact matrices.
    cert_np = quotient_certificate(np.array([[1]], dtype=int), [1], [1])
    assert cert_np.value == Rational(0)
    packet = FiniteObstructionPacket.create(
        np.array([[1], [0]], dtype=int),
        np.array([[0, 0]], dtype=int),
        Matrix.zeros(1, 0),
        [1, 1],
        [1],
    )
    result = diagnose(packet, [1, 0])
    assert result.diagnostic is Diagnostic.EXACT_REPAIR
    cert_empty = quotient_certificate([], [], [])
    assert cert_empty.value == Rational(0)
    with pytest.raises(ValueError, match="expected vector"):
        quotient_certificate(Matrix.eye(2), Matrix.eye(2), [1, 1])


def test_numpy_scalar_floats_are_rejected() -> None:
    # np.float64 subclasses Python float and is caught earlier; float32 does not.
    with pytest.raises(TypeError, match="Floating-point numpy"):
        quotient_certificate(Matrix([[1]]), [np.float32(1)], [1])
    with pytest.raises(TypeError, match="Floating-point numpy"):
        quotient_certificate(Matrix([[1]]), [np.complex64(1)], [1])


def test_validate_rejects_negative_column_count() -> None:
    class NegativeMap:
        cols = -1
        rows = 1

    with pytest.raises(TypeError, match="unsupported matrix type"):
        FiniteObstructionPacket(
            d0=NegativeMap(), d1=NegativeMap(), a2=NegativeMap(),
            w1=Matrix([1]), w2=Matrix([1]),
        )



def test_quotient_certificate_refuses_inconsistent_duals(monkeypatch) -> None:
    # Invariant: a dual witness that fails gap, subspace, or capacity is refused.
    def install(*, distance, dual_witness, repair_cols: int) -> None:
        class FakeProblem:
            def __init__(self, matrix) -> None:
                self.matrix = matrix

            def quotient_l1_distance(
                self,
                weighted_vector,
                _distance=distance,
                _dual=dual_witness,
                _cols=repair_cols,
            ):
                return SimpleNamespace(
                    repair_witness=Matrix.zeros(_cols, 1),
                    residual=weighted_vector,
                    dual_witness=_dual,
                    distance=_distance,
                )

        monkeypatch.setattr("finite_obstruction.LinearRepairProblem", FakeProblem)

    install(distance=Rational(1), dual_witness=Matrix([[0]]), repair_cols=1)
    with pytest.raises(RuntimeError, match="duality gap nonzero"):
        quotient_certificate([[1]], [1], [1])

    install(distance=Rational(1), dual_witness=Matrix([[1]]), repair_cols=1)
    with pytest.raises(RuntimeError, match="does not vanish"):
        quotient_certificate([[1]], [1], [1])

    install(distance=Rational(2), dual_witness=Matrix([[2]]), repair_cols=0)
    with pytest.raises(RuntimeError, match="exceeds observer capacity"):
        quotient_certificate(Matrix.zeros(1, 0), [1], [1])


