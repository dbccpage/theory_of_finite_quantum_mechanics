import numpy as np
import pytest

from omega_engine.crates.quantum_physics.quantum_carriers import (
    QuotientWitness,
    cochain_to_connection,
    connection_laplacian,
    covariant_difference,
    covariant_matrix,
    gauge_transform,
    gell_mann,
    incidence_matrix,
    mass_phase_amplitudes,
    path_holonomy,
    primitive_difference,
    solve_l1_quotient,
    structure_constants,
)
from omega_engine.crates.homology_theory.finite_graph import FiniteGraph


def triangle() -> FiniteGraph:
    return FiniteGraph(3, ((0, 1), (1, 2), (2, 0)))


def test_primitive_difference_and_edgeless_graph() -> None:
    graph = FiniteGraph(2, ((0, 1),))
    assert primitive_difference(graph, [2, 5]).tolist() == [3]
    empty = FiniteGraph(3, ())
    witness = solve_l1_quotient(empty, [], [])
    assert witness.value == 0
    assert witness.residual.size == 0


def test_raw_l1_and_quotient_are_distinct() -> None:
    graph = triangle()
    omega = np.array([2.0, -1.0, 4.0])
    witness = solve_l1_quotient(graph, omega, [1, 1, 1])
    assert witness.value == pytest.approx(abs(omega.sum()))
    assert witness.value != pytest.approx(np.abs(omega).sum())
    assert witness.duality_gap < 1e-8
    assert witness.authority_effect == "None"


def test_gauge_covariance_and_closed_holonomy() -> None:
    graph = triangle()
    connection = np.exp(1j * np.array([0.2, -0.4, 0.7]))
    field = np.array([1 + 2j, -0.5j, 3 - 1j])
    gauge = np.exp(1j * np.array([0.3, -0.8, 1.1]))
    transformed = gauge_transform(graph, connection, gauge)
    lhs = covariant_difference(graph, transformed, gauge * field)
    edge_gauge = np.array([gauge[head] for _, head in graph.edges])
    rhs = edge_gauge * covariant_difference(graph, connection, field)
    assert np.allclose(lhs, rhs)
    loop = [(0, 1), (1, 1), (2, 1)]
    assert path_holonomy(graph, transformed, loop, require_closed=True) == pytest.approx(
        path_holonomy(graph, connection, loop, require_closed=True)
    )
    assert path_holonomy(
        graph, connection, [(0, 1), (0, -1)], require_closed=True
    ) == pytest.approx(1)


def test_connection_laplacian_is_psd_and_gauge_equivalent() -> None:
    graph = triangle()
    connection = np.exp(1j * np.array([0.2, -0.4, 0.7]))
    gauge = np.exp(1j * np.array([0.3, -0.8, 1.1]))
    transformed = gauge_transform(graph, connection, gauge)
    laplacian = connection_laplacian(graph, connection, [1, 2, 3])
    transformed_laplacian = connection_laplacian(graph, transformed, [1, 2, 3])
    gauge_matrix = np.diag(gauge)
    assert np.allclose(laplacian, laplacian.conj().T)
    assert np.linalg.eigvalsh(laplacian).min() >= -1e-10
    assert np.allclose(transformed_laplacian, gauge_matrix @ laplacian @ gauge_matrix.conj().T)
    assert np.linalg.eigvalsh(connection_laplacian(graph, connection)).min() >= -1e-10


def test_exact_cochain_repair_becomes_gauge_transform() -> None:
    graph = triangle()
    alpha = 0.73
    omega = np.array([0.2, -0.7, 1.4])
    potential = np.array([0.4, -1.2, 0.6])
    repaired = omega + incidence_matrix(graph) @ potential
    connection = cochain_to_connection(omega, alpha)
    repaired_connection = cochain_to_connection(repaired, alpha)
    gauge = np.exp(1j * alpha * potential)
    assert np.allclose(repaired_connection, gauge_transform(graph, connection, gauge))


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_gell_mann_basis_identities(n: int) -> None:
    basis = gell_mann(n)
    assert len(basis) == n * n - 1
    gram = np.array([[np.trace(a @ b) for b in basis] for a in basis])
    assert np.allclose(gram, 2 * np.eye(n * n - 1))
    assert all(np.allclose(matrix, matrix.conj().T) for matrix in basis)
    assert all(np.trace(matrix) == pytest.approx(0) for matrix in basis)


def test_structure_constants_reconstruct_su2_commutator() -> None:
    basis = gell_mann(2)
    constants = structure_constants(2)
    for a in range(3):
        for b in range(3):
            lhs = basis[a] @ basis[b] - basis[b] @ basis[a]
            rhs = 2j * sum(constants[a, b, c] * basis[c] for c in range(3))
            assert np.allclose(lhs, rhs)


def test_declared_mass_phase_embedding() -> None:
    amplitude = mass_phase_amplitudes([1, 3], [0.2, -0.7])
    assert np.linalg.norm(amplitude) == pytest.approx(1)
    changed = mass_phase_amplitudes([1, 3], [0.2, 0.9])
    assert np.allclose(np.abs(amplitude), np.abs(changed))
    assert not np.allclose(amplitude, changed)


def test_invalid_inputs_are_refused() -> None:
    with pytest.raises(ValueError, match="at least one"):
        FiniteGraph(0, ())
    with pytest.raises(ValueError, match="outside"):
        FiniteGraph(2, ((0, 2),))
    with pytest.raises(ValueError, match="loops"):
        FiniteGraph(1, ((0, 0),))
    with pytest.raises(ValueError, match="dimension mismatch"):
        primitive_difference(FiniteGraph(2, ()), [1])
    with pytest.raises(ValueError, match="strictly positive"):
        solve_l1_quotient(FiniteGraph(2, ((0, 1),)), [1], [0])
    with pytest.raises(ValueError, match=r"U\(1\)"):
        gauge_transform(FiniteGraph(2, ((0, 1),)), [2], [1, 1])
    with pytest.raises(ValueError, match="dimension mismatch"):
        gauge_transform(FiniteGraph(2, ((0, 1),)), [1, 1], [1, 1])
    with pytest.raises(ValueError, match="field dimension"):
        covariant_difference(FiniteGraph(2, ((0, 1),)), [1], [1])
    with pytest.raises(ValueError, match="path"):
        path_holonomy(FiniteGraph(2, ((0, 1),)), [1], [(2, 1)])
    with pytest.raises(ValueError, match=r"U\(1\)"):
        path_holonomy(FiniteGraph(2, ((0, 1),)), [2], [(0, 1)])
    with pytest.raises(ValueError, match="at least one"):
        path_holonomy(FiniteGraph(2, ((0, 1),)), [1], [])
    with pytest.raises(ValueError, match="continuous"):
        path_holonomy(triangle(), [1, 1, 1], [(0, 1), (2, 1)])
    with pytest.raises(ValueError, match="not closed"):
        path_holonomy(
            FiniteGraph(2, ((0, 1),)), [1], [(0, 1)], require_closed=True
        )
    with pytest.raises(ValueError, match="positive"):
        connection_laplacian(FiniteGraph(2, ((0, 1),)), [1], [0])
    with pytest.raises(ValueError, match="N>=2"):
        gell_mann(1)
    with pytest.raises(ValueError, match="finite"):
        cochain_to_connection([float("nan")], 1)
    with pytest.raises(ValueError, match="not all zero"):
        mass_phase_amplitudes([0, 0], [0, 1])
    with pytest.raises(ValueError, match="equal size"):
        mass_phase_amplitudes([1], [0, 1])
    with pytest.raises(ValueError, match="finite"):
        mass_phase_amplitudes([1], [float("inf")])


