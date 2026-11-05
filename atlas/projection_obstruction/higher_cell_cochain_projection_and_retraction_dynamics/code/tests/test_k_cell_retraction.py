"""Projector regressions, support counterexamples, and tensor ordering."""

import numpy as np
import pytest
from coda_higher_cell.k_cell_retraction import (
    embed_local_operator,
    highest_order_correlation_projector,
    k_cell_boundary_face_projector,
    k_cell_normal_projector,
    k_cell_product_retraction,
    k_cell_tangent_projector,
    partial_trace_keep_single,
    partial_trace_keep_subset,
    tensor_product_list,
    verify_generalized_tangent_isolation,
    verify_marginal_preservation,
)

X = np.array([[0, 1], [1, 0]], dtype=complex)
RHO0 = np.diag([1.0, 0.0])


def random_density(d, rng):
    a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = a @ a.conj().T
    return rho / np.trace(rho)


@pytest.mark.parametrize("dims", [[2, 2], [2, 3, 2], [2, 2, 2, 2]])
def test_tangent_projector_idempotence_and_marginals(dims):
    rng = np.random.default_rng(11)
    rhos = [random_density(d, rng) for d in dims]
    size = int(np.prod(dims))
    a = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    z = a + a.conj().T
    z -= np.trace(z) * np.eye(size) / size
    pz = k_cell_tangent_projector(z, rhos, dims)
    assert np.allclose(k_cell_tangent_projector(pz, rhos, dims), pz, atol=1e-11, rtol=0)
    assert verify_marginal_preservation(z, rhos, dims)
    qz = k_cell_normal_projector(z, rhos, dims)
    for j in range(len(dims)):
        assert np.allclose(partial_trace_keep_single(qz, dims, j), 0, atol=1e-11, rtol=0)
    rz = highest_order_correlation_projector(z, rhos, dims)
    assert np.allclose(highest_order_correlation_projector(rz, rhos, dims), rz, atol=1e-11, rtol=0)


def test_full_space_extension_derivative_and_tiny_trace_linearity():
    dims, rhos = [2, 2], [np.diag([0.7, 0.3]), np.diag([0.4, 0.6])]
    rho = tensor_product_list(rhos)
    z = np.diag([0.2, -0.3, 0.4, 0.8])

    def extension(s):
        return tensor_product_list(
            [partial_trace_keep_single(s, dims, j) for j in range(2)]
        ) / np.trace(s)

    step = 1e-5
    finite_diff = (extension(rho + step * z) - extension(rho - step * z)) / (2 * step)
    assert np.allclose(k_cell_tangent_projector(z, rhos, dims), finite_diff, atol=1e-9, rtol=0)
    tiny = 1e-16 * rho
    assert np.allclose(k_cell_tangent_projector(tiny, rhos, dims), tiny, atol=0, rtol=1e-12)
    assert verify_marginal_preservation(z, rhos, dims)


def test_product_retraction_and_classical_correlation():
    rho = np.diag([0.5, 0, 0, 0.5])
    assert np.allclose(k_cell_product_retraction(rho, [2, 2]), np.eye(4) / 4)
    product = np.kron(np.diag([0.3, 0.7]), RHO0)
    assert np.allclose(k_cell_product_retraction(product, [2, 2]), product)


@pytest.mark.parametrize("site", range(3))
def test_one_site_tangent_isolation(site):
    assert verify_generalized_tangent_isolation(X, [site], [RHO0] * 3, [2] * 3)


@pytest.mark.parametrize("support", [[0, 1], [0, 2], [2, 1]])
def test_two_body_counterexample_and_highest_order_isolation(support):
    rhos, dims = [RHO0] * 3, [2] * 3
    h = embed_local_operator(np.kron(X, X), support, dims)
    rho = tensor_product_list(rhos)
    velocity = -1j * (h @ rho - rho @ h)
    assert not verify_generalized_tangent_isolation(np.kron(X, X), support, rhos, dims)
    assert np.allclose(k_cell_tangent_projector(velocity, rhos, dims), 0)
    assert np.linalg.svd(
        k_cell_normal_projector(velocity, rhos, dims), compute_uv=False
    ).sum() == pytest.approx(2)
    assert np.allclose(highest_order_correlation_projector(velocity, rhos, dims), 0)


def test_full_support_can_commute():
    z = np.diag([1, -1])
    rho = tensor_product_list([RHO0] * 3)
    h = tensor_product_list([z] * 3)
    assert np.array_equal(h @ rho - rho @ h, np.zeros((8, 8)))


def test_highest_order_not_identity_and_boundary_projector():
    rhos, dims = [RHO0] * 3, [2] * 3
    z = tensor_product_list([np.diag([1, -1])] * 3)
    assert np.array_equal(highest_order_correlation_projector(z, rhos, dims), z)
    assert np.array_equal(
        k_cell_boundary_face_projector(z, dims, [[0, 1], [0, 2], [1, 2]], rhos), np.zeros_like(z)
    )
    with pytest.raises(ValueError):
        k_cell_boundary_face_projector(z, dims, [[0, 1]], rhos)
    with pytest.raises(ValueError):
        k_cell_boundary_face_projector(z, dims, [[0, 1], [0, 2], [1, 2]])


def test_partial_trace_reversed_order_and_empty_keep():
    ops = [np.diag([1, 2]), np.diag([2, 3, 4]), np.diag([5, 6])]
    full = tensor_product_list(ops)
    assert np.array_equal(
        partial_trace_keep_subset(full, [2, 3, 2], [2, 0]), 9 * np.kron(ops[2], ops[0])
    )
    assert partial_trace_keep_subset(full, [2, 3, 2], [])[0, 0] == np.trace(full)
    local = np.kron(ops[2], ops[0])
    embedded = embed_local_operator(local, [2, 0], [2, 3, 2])
    assert np.array_equal(embedded, tensor_product_list([ops[0], np.eye(3), ops[2]]))


@pytest.mark.parametrize("dims", [[], [0, 2], [2.5, 2], [True, 2], [-1, 2]])
def test_invalid_dimensions(dims):
    with pytest.raises(ValueError):
        partial_trace_keep_subset(np.eye(4), dims, [0])


@pytest.mark.parametrize("keep", [[0, 0], [-1], [2], [True]])
def test_invalid_indices(keep):
    with pytest.raises(ValueError):
        partial_trace_keep_subset(np.eye(4), [2, 2], keep)


@pytest.mark.parametrize(
    "rho",
    [np.diag([1, 1]), np.diag([1.1, -0.1]), np.array([[1, 1], [0, 0]]), np.full((2, 2), np.nan)],
)
def test_invalid_reference_densities(rho):
    with pytest.raises(ValueError):
        k_cell_tangent_projector(np.eye(4), [rho, RHO0], [2, 2])


def test_invalid_shapes_and_empty_products():
    with pytest.raises(ValueError):
        partial_trace_keep_single(np.eye(3), [2, 2], 0)
    with pytest.raises(ValueError):
        k_cell_tangent_projector(np.eye(4), [RHO0], [2, 2])
    with pytest.raises(ValueError):
        tensor_product_list([])
    with pytest.raises(ValueError):
        embed_local_operator(np.eye(2), [0, 1], [2, 2])
    with pytest.raises(ValueError):
        verify_generalized_tangent_isolation(np.eye(4), [0, 1], [RHO0] * 2, [2] * 2)
    with pytest.raises(ValueError):
        verify_generalized_tangent_isolation(np.array([[0, 1], [0, 0]]), [0], [RHO0] * 2, [2] * 2)
