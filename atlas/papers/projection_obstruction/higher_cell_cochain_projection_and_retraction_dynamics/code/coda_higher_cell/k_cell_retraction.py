"""Product retractions and two distinct correlation projectors.

k counts subsystems, not simplicial dimension. NumPy uses floating-point
arithmetic, not exact rational certification. AuthorityEffect: None.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from ._validation import density, dimensions, indices, matrix, nonnegative, reference


def partial_trace_keep_subset(
    matrix_: np.ndarray, dims: Sequence[int], keep_indices: Sequence[int]
) -> np.ndarray:
    """Partial trace with output factors in the requested order.

    Empty keep indices return the total trace as a 1-by-1 matrix.
    """
    ds = dimensions(dims)
    keep = indices(keep_indices, len(ds))
    size = math.prod(ds)
    tensor = matrix(matrix_, "operator", (size, size)).reshape(ds + ds)
    remaining = list(range(len(ds)))
    for i in reversed(range(len(ds))):
        if i not in keep:
            pos = remaining.index(i)
            tensor = np.trace(tensor, axis1=pos, axis2=pos + len(remaining))
            remaining.remove(i)
    order = [remaining.index(i) for i in keep]
    if keep:
        tensor = tensor.transpose(order + [i + len(keep) for i in order])
    out_size = math.prod(ds[i] for i in keep)
    return tensor.reshape(out_size, out_size)


def partial_trace_keep_single(
    matrix_: np.ndarray, dims: Sequence[int], keep_idx: int
) -> np.ndarray:
    """Trace out every subsystem except keep_idx."""
    return partial_trace_keep_subset(matrix_, dims, [keep_idx])


partial_trace_k = partial_trace_keep_single


def tensor_product_list(operators: Sequence[np.ndarray]) -> np.ndarray:
    """Kronecker product of a nonempty list of finite matrices."""
    if not operators:
        raise ValueError("operators must be nonempty")
    result = matrix(operators[0], "operator")
    for op in operators[1:]:
        result = np.kron(result, matrix(op, "operator"))
    return result


def k_cell_product_retraction(rho_state: np.ndarray, dims: Sequence[int]) -> np.ndarray:
    """Pi(rho) is the tensor product of its single-site marginals."""
    ds = dimensions(dims)
    rho = density(rho_state, math.prod(ds))
    return tensor_product_list([partial_trace_keep_single(rho, ds, j) for j in range(len(ds))])


def k_cell_tangent_projector(
    perturbation: np.ndarray, marginals: Sequence[np.ndarray], dims: Sequence[int]
) -> np.ndarray:
    """D Pi on trace-zero directions; D of the homogeneous extension otherwise.

    R(S) = tr(S)^(1-k) tensor_j tr_not_j(S).
    D R(Z) = sum_j iota_j(tau_j Z) - (k-1) tr(Z) rho.
    The full-space image also contains the radial direction rho.
    """
    ds, rhos = reference(marginals, dims)
    size = math.prod(ds)
    z = matrix(perturbation, "perturbation", (size, size))
    result = np.zeros_like(z)
    for j in range(len(ds)):
        ops = list(rhos)
        ops[j] = partial_trace_keep_single(z, ds, j)
        result += tensor_product_list(ops)
    # No threshold: thresholding the trace correction makes the map nonlinear.
    return result - (len(ds) - 1) * np.trace(z) * tensor_product_list(rhos)


def k_cell_normal_projector(
    perturbation: np.ndarray, marginals: Sequence[np.ndarray], dims: Sequence[int]
) -> np.ndarray:
    """Q = I-P: all departure from the fully factorized tangent model."""
    p_z = k_cell_tangent_projector(perturbation, marginals, dims)
    return np.asarray(perturbation) - p_z


def _replacement(
    z: np.ndarray, rhos: Sequence[np.ndarray], ds: Sequence[int], site: int
) -> np.ndarray:
    """E_j Z replaces site j by rho_j while retaining its complement."""
    complement = [i for i in range(len(ds)) if i != site]
    reduced = partial_trace_keep_subset(z, ds, complement)
    order = complement + [site]
    ordered_dims = [ds[i] for i in order]
    tensor = np.kron(reduced, rhos[site]).reshape(ordered_dims + ordered_dims)
    inverse = [order.index(i) for i in range(len(ds))]
    return tensor.transpose(inverse + [i + len(ds) for i in inverse]).reshape(z.shape)


def highest_order_correlation_projector(
    perturbation: np.ndarray, marginals: Sequence[np.ndarray], dims: Sequence[int]
) -> np.ndarray:
    """R_k = product_j (I-E_j), a distinct full-support component projector.

    It annihilates Z_X tensor rho_complement for every proper subset X.
    This algebraic component is not an entanglement certificate.
    """
    ds, rhos = reference(marginals, dims)
    size = math.prod(ds)
    result = matrix(perturbation, "perturbation", (size, size)).copy()
    for j in range(len(ds)):
        result -= _replacement(result, rhos, ds, j)
    return result


def k_cell_boundary_face_projector(
    perturbation: np.ndarray,
    dims: Sequence[int],
    sub_indices_list: Sequence[Sequence[int]],
    marginals: Sequence[np.ndarray] | None = None,
) -> np.ndarray:
    """I-R_k for the complete codimension-one boundary face family.

    Reference marginals are required. A partial face family is rejected.
    """
    ds = dimensions(dims)
    if marginals is None:
        raise ValueError("explicit reference marginals are required")
    faces = [frozenset(indices(face, len(ds))) for face in sub_indices_list]
    expected = {frozenset(set(range(len(ds))) - {j}) for j in range(len(ds))}
    if len(faces) != len(expected) or set(faces) != expected:
        raise ValueError("the complete codimension-one boundary is required")
    return np.asarray(perturbation) - highest_order_correlation_projector(
        perturbation, marginals, ds
    )


def verify_marginal_preservation(
    perturbation: np.ndarray,
    marginals: Sequence[np.ndarray],
    dims: Sequence[int],
    tol: float = 1e-12,
) -> bool:
    """Numerical marginal check using only the absolute tolerance."""
    tol = nonnegative(tol, "tol")
    p_z = k_cell_tangent_projector(perturbation, marginals, dims)
    return all(
        np.allclose(
            partial_trace_keep_single(p_z, dims, j),
            partial_trace_keep_single(perturbation, dims, j),
            atol=tol,
            rtol=0,
        )
        for j in range(len(dims))
    )


def embed_local_operator(
    local_op: np.ndarray, target_indices: Sequence[int], dims: Sequence[int]
) -> np.ndarray:
    """Embed an operator whose tensor factors follow target_indices order."""
    ds = dimensions(dims)
    target = indices(target_indices, len(ds))
    size = math.prod(ds[i] for i in target)
    local = matrix(local_op, "local operator", (size, size))
    rest = [i for i in range(len(ds)) if i not in target]
    order = list(target) + rest
    ordered_dims = [ds[i] for i in order]
    full = np.kron(local, np.eye(math.prod(ds[i] for i in rest))).reshape(
        ordered_dims + ordered_dims
    )
    inverse = [order.index(i) for i in range(len(ds))]
    return full.transpose(inverse + [i + len(ds) for i in inverse]).reshape(
        math.prod(ds), math.prod(ds)
    )


def verify_generalized_tangent_isolation(
    h_sub: np.ndarray,
    sub_indices: Sequence[int],
    marginals: Sequence[np.ndarray],
    dims: Sequence[int],
    tol: float = 1e-12,
) -> bool:
    """Test the actual Q commutator; multi-site proper supports can return False.

    This compatibility name no longer substitutes an untouched-site marginal
    check for tangent isolation.
    """
    tol = nonnegative(tol, "tol")
    ds, rhos = reference(marginals, dims)
    support = indices(sub_indices, len(ds))
    if len(support) >= len(ds):
        raise ValueError("sub_indices must be a proper subset")
    h = embed_local_operator(h_sub, support, ds)
    if not np.allclose(h, h.conj().T, atol=tol, rtol=0):
        raise ValueError("Hamiltonian must be Hermitian")
    rho = tensor_product_list(rhos)
    z = -1j * (h @ rho - rho @ h)
    return bool(np.linalg.norm(k_cell_normal_projector(z, rhos, ds), ord="fro") <= tol)


def verify_1local_tangent_isolation(
    h_single: np.ndarray,
    site_idx: int,
    marginals: Sequence[np.ndarray],
    dims: Sequence[int],
    tol: float = 1e-12,
) -> bool:
    """Numerical test of the valid one-site isolation theorem."""
    return verify_generalized_tangent_isolation(h_single, [site_idx], marginals, dims, tol)
