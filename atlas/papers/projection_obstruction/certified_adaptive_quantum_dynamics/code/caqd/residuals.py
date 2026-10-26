"""Projection residuals, tangent retractors, and Schatten-1 dual witness certification.

Implements the retraction differential P_e, normal projector Q_e, local normal
residual n_e = Q_e L_e, and defect rate nu_e = ||n_e||_1, along with the Schatten-1
dual witness matrix W in subgradient partial ||.||_1(Q).

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple
import numpy as np
import scipy.linalg

from caqd.spin_chains import (
    SpinChainModel,
    operator_norm,
    partial_trace,
    trace_norm,
)


def retraction_tangent_projector(
    rho_a: np.ndarray,
    rho_b: np.ndarray,
    Z_ab: np.ndarray,
    da: int = 2,
    db: int = 2,
) -> np.ndarray:
    """Evaluate retraction differential P_e(Z_ab) at product point rho_a (x) rho_b.
    
    Formula:
        P_e(Z_ab) = (Tr_B Z_ab) (x) rho_b + rho_a (x) (Tr_A Z_ab) - Tr(Z_ab) (rho_a (x) rho_b)
        
    Properties:
        1. P_e^2 = P_e when rho_a and rho_b have unit trace.
        2. Tr_B(P_e Z_ab) = Tr_B(Z_ab), Tr_A(P_e Z_ab) = Tr_A(Z_ab) (marginal preservation).
        3. For traceless Z_ab (Tr(Z_ab)=0), the third term vanishes.

    This is the differential of (Tr_B sigma (x) Tr_A sigma) / Tr(sigma).
    Its restriction to traceless Hermitian inputs gives the algebraic product
    tangent space; at full-rank factors this is the normalized density manifold
    tangent. On the full ambient space its range also includes the scaling
    direction rho_a (x) rho_b.
    """
    tensor = Z_ab.reshape((da, db, da, db))
    tr_B = np.trace(tensor, axis1=1, axis2=3) # shape (da, da)
    tr_A = np.trace(tensor, axis1=0, axis2=2) # shape (db, db)
    tr_total = np.trace(Z_ab)
    
    res = np.kron(tr_B, rho_b) + np.kron(rho_a, tr_A)
    res -= tr_total * np.kron(rho_a, rho_b)
    return res


def normal_projector(
    rho_a: np.ndarray,
    rho_b: np.ndarray,
    Z_ab: np.ndarray,
    da: int = 2,
    db: int = 2,
) -> np.ndarray:
    """Evaluate normal projector Q_e(Z_ab) = (I - P_e)(Z_ab)."""
    return Z_ab - retraction_tangent_projector(rho_a, rho_b, Z_ab, da, db)


def compute_edge_residual(
    rho_a: np.ndarray,
    rho_b: np.ndarray,
    h_ab: np.ndarray,
    da: int = 2,
    db: int = 2,
) -> Tuple[np.ndarray, float]:
    """Compute local normal residual operator n_e and defect rate nu_e for a bipartite edge.
    
    Args:
        rho_a: Density matrix of subsystem A (da x da).
        rho_b: Density matrix of subsystem B (db x db).
        h_ab: Interaction Hamiltonian term across edge (da*db x da*db).
        
    Returns:
        n_e: Normal residual matrix (da*db x da*db).
        nu_e: Schatten-1 norm ||n_e||_1.
    """
    rho_prod = np.kron(rho_a, rho_b)
    comm = -1.0j * (h_ab @ rho_prod - rho_prod @ h_ab)
    n_e = normal_projector(rho_a, rho_b, comm, da, db)
    nu_e = trace_norm(n_e)
    return n_e, float(nu_e)


def compute_local_residuals(
    model: SpinChainModel,
    rho_state: np.ndarray | Sequence[np.ndarray],
) -> Dict[Tuple[int, int], float]:
    """Compute product-of-site-marginals residual rates for all model edges.

    For a correlated input this is a diagnostic of its product marginals, not
    the global trajectory defect. Adaptive cluster boundaries require the full
    cluster factors instead (see adaptive._cluster_residual_rates).
    
    Args:
        model: SpinChainModel instance with lattice edges and local terms.
        rho_state: Either the full N-qubit density matrix, or a sequence of single-site
                   reduced density matrices [rho_0, rho_1, ..., rho_{N-1}].
                   
    Returns:
        Dictionary mapping edge (a, b) to local rate nu_e.
    """
    rates: Dict[Tuple[int, int], float] = {}
    N = model.num_sites
    
    if isinstance(rho_state, np.ndarray) and rho_state.shape == (2**N, 2**N):
        marginals = [partial_trace(rho_state, [i], N) for i in range(N)]
    elif isinstance(rho_state, (list, tuple)) and len(rho_state) == N:
        marginals = list(rho_state)
    else:
        raise ValueError("rho_state must be full state (2^N, 2^N) or list of N single-site density matrices.")
        
    for edge in model.edges:
        a, b = edge
        terms = model.get_terms_for_edge(edge)
        if not terms:
            rates[edge] = 0.0
            continue
        h_ab = sum((t.matrix for t in terms), np.zeros((4, 4), dtype=complex))
        _, nu_e = compute_edge_residual(marginals[a], marginals[b], h_ab, da=2, db=2)
        rates[edge] = nu_e
        
    return rates


def dual_witness_schatten1(Q: np.ndarray, tol: float = 1e-12) -> Tuple[np.ndarray, float]:
    """Construct and certify the Schatten-1 dual witness matrix W in partial ||.||_1(Q).
    
    By Schatten norm duality:
        ||W||_inf <= 1,
        Re(Tr(W^dagger Q)) = ||Q||_1.
        
    Constructed via SVD polar decomposition:
        Q = U Sigma V^dagger  =>  W = U V^dagger.
        
    Returns:
        W: The dual witness matrix.
        gap: Absolute duality gap |Re(Tr(W^dagger Q)) - ||Q||_1|.

    This certifies the norm of Q, not optimality of a trace-norm projection onto
    a tangent space. That separate statement needs tangent annihilation.
    """
    U, s, Vh = scipy.linalg.svd(Q, full_matrices=False)
    W = U @ Vh
    
    w_norm = operator_norm(W)
    if w_norm > 1.0 + 1e-7:
        raise RuntimeError(f"Dual witness violates unit ball condition: ||W||_inf = {w_norm}")
        
    trace_val = float(np.real(np.trace(W.conj().T @ Q)))
    true_norm = float(np.sum(s))
    gap = abs(trace_val - true_norm)
    return W, gap


def verify_lemma_5_3_tangent_isolation(
    rho_a: np.ndarray,
    rho_b: np.ndarray,
    h_a: np.ndarray,
) -> float:
    """Verify PO-000 Lemma 5.3: one-local terms generate motion strictly inside the tangent space.
    
    For single-site generator -i [h_a (x) I, rho_a (x) rho_b], the normal residual
    Q_e(-i [h_a (x) I, rho_a (x) rho_b]) is identically zero.
    
    Returns:
        The trace norm of the normal residual (must be approx 0.0).
    """
    I_b = np.eye(rho_b.shape[0], dtype=complex)
    h_embedded = np.kron(h_a, I_b)
    rho_prod = np.kron(rho_a, rho_b)
    comm = -1.0j * (h_embedded @ rho_prod - rho_prod @ h_embedded)
    n_normal = normal_projector(rho_a, rho_b, comm, da=rho_a.shape[0], db=rho_b.shape[0])
    return trace_norm(n_normal)
