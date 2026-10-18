"""Production-seam parity tests for the Rust/Python Q obstruction solver."""

import math

import pytest

from omega_engine.crates.linear_algebra_theory.basis import BasisDescriptor, BasisError, BasisId
from omega_engine.crates.operator.lambda_op.lamb_network_simplex_basis import Basis
from omega_engine.crates.solver.solv_q_obstruction import (
    Q_AUTHORITY_EFFECT,
    Q_SPECTRAL_RECEIPT_SCHEMA,
    QObstructionInput,
    QObstructionInputDegree1,
    QObstructionSolver,
    WeightedCarrier,
    gauge_transform_input,
    imaginary_time_excited_ratio,
    orthogonal_gauge,
    parity_shadow_check,
    s2_rayleigh_scan,
    solve_degree1,
    symmetrize,
    weighted_to_unit_input,
)
from omega_engine.crates.type.solver_evidence import CertificateKind, SolverError
from omega_engine.crates.solver.solv_hodge_primal_dual import solve_spectral_hodge, spectral_hodge_laplacian


def _edge_input():
    return QObstructionInput.from_rows([[1.0, -1.0]], [[0.0, 0.0], [0.0, 0.0]])


def test_q_solver_known_spectrum_receipt_and_certificate():
    result = QObstructionSolver().solve(_edge_input())
    receipt = result.value
    assert receipt.schema == Q_SPECTRAL_RECEIPT_SCHEMA
    assert receipt.eigenvalues == pytest.approx((0.0, 2.0), abs=1e-12)
    assert receipt.ground_energy == pytest.approx(0.0, abs=1e-12)
    assert receipt.spectral_gap == pytest.approx(2.0, abs=1e-12)
    assert receipt.residual_inf_norm <= 1e-12
    assert result.diagnostics.converged is True
    assert result.diagnostics.certificates[0].kind is CertificateKind.Eigenpair
    assert Q_AUTHORITY_EFFECT == "None"


def test_q_solver_is_deterministic_and_hash_bound():
    solver = QObstructionSolver()
    first = solver.solve(_edge_input())
    second = solver.solve(_edge_input())
    assert first == second
    assert first.value.evidence_sha256 == second.value.evidence_sha256
    assert len(first.value.evidence_sha256) == 64


def test_q_solver_uses_rust_parity_diagnostics_constructor_and_rejects_bool():
    result = QObstructionSolver().solve(_edge_input())
    assert type(result).new_with_diagnostics(result.value, result.diagnostics) == result
    assert type(result).new_certified(result.value, result.diagnostics) == result

    with pytest.raises(SolverError) as error:
        QObstructionInput.from_rows([[True, -1.0]], [[0.0, 0.0], [0.0, 0.0]])
    assert error.value.kind == SolverError.INFEASIBLE


@pytest.mark.parametrize(
    "input_data, expected_kind",
    [
        (
            QObstructionInput.from_rows(
                [[float("nan"), 0.0]], [[0.0, 0.0], [0.0, 0.0]]
            ),
            SolverError.NON_FINITE_INPUT,
        ),
        (
            QObstructionInput.from_rows([[1.0, -1.0]], [[0.0, 1.0], [0.0, 0.0]]),
            SolverError.INFEASIBLE,
        ),
    ],
)
def test_q_solver_refuses_invalid_numeric_domain(input_data, expected_kind):
    with pytest.raises(SolverError) as error:
        QObstructionSolver().solve(input_data)
    assert error.value.kind == expected_kind


def test_symmetrize_discloses_discarded_asymmetry():
    symmetric, residual = symmetrize([[1.0, 2.0], [0.0, 1.0]])
    assert symmetric == ((1.0, 1.0), (1.0, 1.0))
    assert residual == 1.0


def test_orthogonal_gauge_preserves_spectrum_and_discloses_roundoff():
    gauge = orthogonal_gauge([[0.0, -0.25], [0.25, 0.0]])
    identity_00 = sum(gauge[k][0] * gauge[k][0] for k in range(2))
    identity_01 = sum(gauge[k][0] * gauge[k][1] for k in range(2))
    assert identity_00 == pytest.approx(1.0, abs=1e-14)
    assert identity_01 == pytest.approx(0.0, abs=1e-14)

    transformed, residual = gauge_transform_input(_edge_input(), gauge)
    original_receipt = QObstructionSolver().solve(_edge_input()).value
    transformed_receipt = QObstructionSolver().solve(transformed).value
    assert transformed_receipt.eigenvalues == pytest.approx(
        original_receipt.eigenvalues, abs=1e-12
    )
    assert residual <= 1e-15


def test_degree1_hodge_lives_behind_topology_facade():
    problem = QObstructionInputDegree1.from_rows(
        d0=[[-1.0, 1.0], [1.0, -1.0]],
        d1=None,
        defect_potential=[[0.0, 0.0], [0.0, 0.0]],
    )
    assert spectral_hodge_laplacian(problem) == ((2.0, -2.0), (-2.0, 2.0))
    direct = solve_degree1(QObstructionSolver(), problem)
    topological = solve_spectral_hodge(problem)
    assert topological == direct
    assert topological.value.eigenvalues == pytest.approx((0.0, 4.0), abs=1e-12)


def test_parity_shadow_is_exact_and_orientation_free_mod_two():
    d0 = [[-1, 1, 0], [0, -1, 1], [-1, 0, 1]]
    d1 = [[1, 1, -1]]
    receipt = parity_shadow_check(d0, d1, [[1, -1, 0], [0, 1, -1], [1, 0, -1]])
    assert receipt.delta1_delta0_zero is True
    assert receipt.max_composite_entry == 0
    assert receipt.shadow_orientation_free is True

    bad = parity_shadow_check(d0, [[1, 1, 1]], d0)
    assert bad.delta1_delta0_zero is False
    assert bad.max_composite_entry > 0


def test_weighted_carrier_transform_and_rayleigh_scan():
    carrier = WeightedCarrier.from_rows(
        d0=[[1.0, -1.0]],
        w0=[4.0, 1.0],
        w1=[9.0],
        defect_potential=[[0.0, 0.0], [0.0, 0.0]],
    )
    transformed = weighted_to_unit_input(carrier)
    assert transformed.coboundary[0] == pytest.approx((1.5, -3.0))
    result = QObstructionSolver().solve(transformed)
    violation, ground_error = s2_rayleigh_scan(
        transformed,
        result.value,
        ([1.0, 0.0], [0.0, 1.0]),
    )
    assert violation <= 1e-12
    assert ground_error <= 1e-12


def test_imaginary_time_excited_ratio_follows_spectral_gap():
    receipt = QObstructionSolver().solve(_edge_input()).value
    psi = tuple(a + b for a, b in zip(receipt.ground_state, receipt.eigenvectors[1]))
    ratio = imaginary_time_excited_ratio(receipt, psi, 0.5)
    assert ratio == pytest.approx(math.exp(-receipt.spectral_gap * 0.5), abs=1e-12)


def test_network_tree_basis_binds_canonical_coordinate_descriptor():
    basis = Basis(4)
    descriptor = basis.descriptor()
    assert descriptor == BasisDescriptor(BasisId("network-simplex-node-coordinates"), 4)
    assert descriptor.dimension == len(basis.parent)
    with pytest.raises(BasisError):
        BasisId("   ")


