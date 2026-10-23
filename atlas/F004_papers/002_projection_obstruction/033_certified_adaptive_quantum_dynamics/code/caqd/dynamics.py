"""Quantum dynamical solvers: exact unitary evolution and product-state mean field.

Provides exact matrix-exponential evolution and variational product-state
mean-field dynamics for numerical reference comparisons of residual estimates.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple
import numpy as np
import scipy.linalg

from caqd.residuals import compute_local_residuals
from caqd.spin_chains import (
    SpinChainModel,
    operator_norm,
    partial_trace,
    trace_norm,
    validate_times,
    validate_density_matrix,
)


@dataclass
class SimulationResult:
    """Stores trajectory data from a quantum dynamics simulation."""
    times: np.ndarray
    states: List[np.ndarray]
    observables: Dict[str, np.ndarray]
    residuals: Dict[Tuple[int, int], np.ndarray]
    total_rates: np.ndarray
    method: str
    metadata: Dict[str, object] = field(default_factory=dict)

    def expectation(self, name: str) -> np.ndarray:
        """Retrieve expectation array for a named observable."""
        if name not in self.observables:
            raise KeyError(f"Observable {name} not found in results: {list(self.observables.keys())}")
        return self.observables[name]


def evolve_exact(
    model: SpinChainModel,
    rho0: np.ndarray,
    t_span: Sequence[float],
    obs_dict: Dict[str, np.ndarray] | None = None,
) -> SimulationResult:
    """Compute dense unitary reference evolution from rho0 at t_span[0].

    rho(t) = exp(-i H (t-t_0)) rho0 exp(i H (t-t_0)); floating-point
    diagonalization is a numerical reference, not interval-certified arithmetic.
    
    Args:
        model: SpinChainModel containing system Hamiltonian H and edges.
        rho0: Initial density matrix (2^N x 2^N).
        t_span: Monotonically increasing sequence of evaluation times [t_0, t_1, ...].
        obs_dict: Optional dictionary of observable matrices {"O_name": O_matrix}.
        
    Returns:
        SimulationResult containing exact trajectory, observables, and local residuals.
    """
    times = validate_times(t_span)
    rho0 = validate_density_matrix(rho0, model.dim)
        
    H = model.H
    # Spectral decomposition of Hermitian Hamiltonian for efficient unitary exponentiation
    evals, evecs = scipy.linalg.eigh(H)
    evecs_adj = evecs.conj().T
    
    # Pre-transform rho0 into eigenbasis
    rho0_diag = evecs_adj @ rho0 @ evecs
    
    if obs_dict is None:
        obs_dict = {}
        
    states: List[np.ndarray] = []
    obs_trajs: Dict[str, List[float]] = {name: [] for name in obs_dict}
    residual_history: Dict[Tuple[int, int], List[float]] = {e: [] for e in model.edges}
    total_rates_list: List[float] = []
    
    for t in times:
        # rho0 is the state at the first sampling time, consistently with the
        # mean-field and adaptive solvers (including translated time grids).
        phase = np.exp(-1.0j * evals * (t - times[0]))
        rho_t_diag = phase[:, None] * rho0_diag * phase[None, :].conj()
        rho_t = evecs @ rho_t_diag @ evecs_adj
        
        # Enforce exact Hermiticity
        rho_t = 0.5 * (rho_t + rho_t.conj().T)
        states.append(rho_t)
        
        # Evaluate observables
        for name, O in obs_dict.items():
            exp_val = float(np.real(np.trace(O @ rho_t)))
            obs_trajs[name].append(exp_val)
            
        # Compute instantaneous local residuals across edges
        rates = compute_local_residuals(model, rho_t)
        tot_rate = 0.0
        for e in model.edges:
            r = rates.get(e, 0.0)
            residual_history[e].append(r)
            tot_rate += r
        total_rates_list.append(tot_rate)
        
    return SimulationResult(
        times=times,
        states=states,
        observables={k: np.array(v) for k, v in obs_trajs.items()},
        residuals={k: np.array(v) for k, v in residual_history.items()},
        total_rates=np.array(total_rates_list),
        method="exact",
    )


def _mean_field_derivatives(
    marginals: List[np.ndarray],
    model: SpinChainModel,
) -> List[np.ndarray]:
    """Compute variational equations of motion d(rho_i)/dt for product state.
    
    Derivation from Tangent Projection P_e:
        d(rho_i)/dt = -i [h_i^eff, rho_i]
    where:
        h_i^eff = h_i^(1-local) + sum_{j in N(i)} Tr_j( h_ij (I (x) rho_j) )
    """
    N = model.num_sites
    derivs: List[np.ndarray] = []
    
    for i in range(N):
        # 1-local contribution
        h_eff = np.zeros((2, 2), dtype=complex)
        for t1 in model.get_terms_for_site(i):
            h_eff += t1.matrix
            
        # 2-local mean-field contractions
        for edge in model.edges:
            if i not in edge:
                continue
            j = edge[1] if edge[0] == i else edge[0]
            rho_j = marginals[j]
            
            terms = model.get_terms_for_edge(edge)
            h_ij = sum((t.matrix for t in terms), np.zeros((4, 4), dtype=complex))
            
            # h_ij acts on C^2 (x) C^2 with site order (edge[0], edge[1])
            # We contract site j with rho_j
            if edge[0] == i:
                # i is first site: contract second site
                # h_ij shape (2_i, 2_j, 2_i, 2_j)
                t_tensor = h_ij.reshape((2, 2, 2, 2))
                # contract index 1 and 3 with rho_j
                h_eff += np.einsum("abcd,db->ac", t_tensor, rho_j)
            else:
                # i is second site: contract first site
                t_tensor = h_ij.reshape((2, 2, 2, 2))
                h_eff += np.einsum("abcd,ca->bd", t_tensor, rho_j)
                
        # Commutator -i [h_eff, rho_i]
        d_rho_i = -1.0j * (h_eff @ marginals[i] - marginals[i] @ h_eff)
        # Symmetrize derivative to maintain Hermiticity
        d_rho_i = 0.5 * (d_rho_i + d_rho_i.conj().T)
        derivs.append(d_rho_i)
        
    return derivs


def evolve_mean_field(
    model: SpinChainModel,
    rho0: np.ndarray | Sequence[np.ndarray],
    t_span: Sequence[float],
    obs_dict: Dict[str, np.ndarray] | None = None,
) -> SimulationResult:
    """Propagate product-state mean field dynamics (chi=1 tangent projection).
    
    Integrates the self-consistent single-site von Neumann equations via 4th-order
    Runge-Kutta, strictly maintaining trace-preservation and Hermiticity.
    
    Args:
        model: SpinChainModel instance.
        rho0: Initial state (full density matrix or list of N single-site density matrices).
        t_span: Monotonically increasing evaluation times.
        obs_dict: Optional dictionary of target observables.
        
    Returns:
        SimulationResult containing mean-field trajectory and observable expectations.
    """
    times = validate_times(t_span)
    N = model.num_sites
    
    # Initialize single-site marginals
    if isinstance(rho0, np.ndarray) and rho0.shape == (2**N, 2**N):
        rho0 = validate_density_matrix(rho0, model.dim)
        curr_marginals = [partial_trace(rho0, [i], N) for i in range(N)]
        product = np.array([[1.0]], dtype=complex)
        for marginal in curr_marginals:
            product = np.kron(product, marginal)
        if not np.allclose(rho0, product, atol=1e-10, rtol=1e-10):
            raise ValueError("Product-state initialization required; correlated rho0 would introduce unaccounted initial error.")
    elif isinstance(rho0, (list, tuple)) and len(rho0) == N:
        curr_marginals = [np.array(m, dtype=complex) for m in rho0]
    else:
        raise ValueError("rho0 must be full state (2^N, 2^N) or list of N single-site density matrices.")
        
    # Ensure pure / physical initial marginals
    curr_marginals = [validate_density_matrix(m, 2) for m in curr_marginals]
    
    if obs_dict is None:
        obs_dict = {}
        
    states: List[np.ndarray] = []
    obs_trajs: Dict[str, List[float]] = {name: [] for name in obs_dict}
    residual_history: Dict[Tuple[int, int], List[float]] = {e: [] for e in model.edges}
    total_rates_list: List[float] = []
    
    current_time = times[0]
    
    for idx, target_time in enumerate(times):
        dt = target_time - current_time
        if dt > 0:
            # Sub-step RK4 if dt is large for numerical stability
            n_substeps = max(1, int(np.ceil(dt / 0.01 - 1e-12)))
            sub_dt = dt / n_substeps
            
            for _ in range(n_substeps):
                # RK4 integration step for list of matrices
                k1 = _mean_field_derivatives(curr_marginals, model)
                
                m_k2 = [curr_marginals[i] + 0.5 * sub_dt * k1[i] for i in range(N)]
                k2 = _mean_field_derivatives(m_k2, model)
                
                m_k3 = [curr_marginals[i] + 0.5 * sub_dt * k2[i] for i in range(N)]
                k3 = _mean_field_derivatives(m_k3, model)
                
                m_k4 = [curr_marginals[i] + sub_dt * k3[i] for i in range(N)]
                k4 = _mean_field_derivatives(m_k4, model)
                
                new_marginals = []
                for i in range(N):
                    step_i = (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
                    m_new = curr_marginals[i] + sub_dt * step_i
                    # Re-symmetrize and re-normalize trace
                    m_new = 0.5 * (m_new + m_new.conj().T)
                    tr = np.real(np.trace(m_new))
                    if tr > 1e-14:
                        m_new = m_new / tr
                    new_marginals.append(m_new)
                curr_marginals = new_marginals
                
            current_time = target_time
            
        # Reconstruct full product state rho = rho_0 (x) ... (x) rho_{N-1}
        full_rho = np.array([[1.0]], dtype=complex)
        for m in curr_marginals:
            full_rho = np.kron(full_rho, m)
        states.append(full_rho)
        
        # Evaluate observables
        for name, O in obs_dict.items():
            exp_val = float(np.real(np.trace(O @ full_rho)))
            obs_trajs[name].append(exp_val)
            
        # Compute local residuals
        rates = compute_local_residuals(model, curr_marginals)
        tot_rate = 0.0
        for e in model.edges:
            r = rates.get(e, 0.0)
            residual_history[e].append(r)
            tot_rate += r
        total_rates_list.append(tot_rate)
        
    return SimulationResult(
        times=times,
        states=states,
        observables={k: np.array(v) for k, v in obs_trajs.items()},
        residuals={k: np.array(v) for k, v in residual_history.items()},
        total_rates=np.array(total_rates_list),
        method="mean_field",
    )
