"""Certified Adaptive Quantum Dynamics (CAQD) solver.

Dynamically allocates variational degrees of freedom by cluster merging
based on local projection residuals nu_e(t),
using a heuristic target tolerance; sampled residuals do not certify the trajectory error.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple
import numpy as np
import scipy.linalg

from caqd.dynamics import SimulationResult
from caqd.residuals import compute_edge_residual
from caqd.spin_chains import (
    SpinChainModel,
    operator_norm,
    partial_trace,
    validate_times,
    validate_density_matrix,
)


class QuantumCluster:
    """Represents a coherent subsystem of sites in the partitioned quantum lattice."""
    def __init__(self, sites: Sequence[int], rho: np.ndarray):
        raw_sites = list(sites)
        if (not raw_sites or len(set(raw_sites)) != len(raw_sites)
                or any(not isinstance(s, (int, np.integer)) or isinstance(s, bool) or s < 0 for s in raw_sites)):
            raise ValueError("cluster sites must be distinct nonnegative integer indices")
        self.sites = sorted(raw_sites)
        self.dim = 2 ** len(self.sites)
        self.rho = validate_density_matrix(rho, self.dim)
        if raw_sites != self.sites:
            k = len(raw_sites)
            perm = [raw_sites.index(site) for site in self.sites]
            self.rho = self.rho.reshape([2] * (2*k)).transpose(perm + [i+k for i in perm]).reshape((self.dim, self.dim))

    def contains_site(self, site: int) -> bool:
        return site in self.sites

    def local_index(self, site: int) -> int:
        return self.sites.index(site)

    def single_site_marginal(self, site: int) -> np.ndarray:
        """Extract 2x2 density matrix for a specific qubit site within this cluster."""
        idx = self.local_index(site)
        return partial_trace(self.rho, [idx], len(self.sites))


def _merge_clusters(c1: QuantumCluster, c2: QuantumCluster) -> QuantumCluster:
    """Merge two clusters into a single joint cluster with tensor product state."""
    if set(c1.sites) & set(c2.sites):
        raise ValueError("cannot merge overlapping clusters")
    # To keep canonical site ordering, determine permutation if necessary
    all_sites = sorted(c1.sites + c2.sites)
    
    # Form raw kron rho_c1 (x) rho_c2
    raw_rho = np.kron(c1.rho, c2.rho)
    
    # Re-order qubits if c1.sites and c2.sites are interleaved
    raw_sites = c1.sites + c2.sites
    if raw_sites != all_sites:
        k = len(all_sites)
        perm = [raw_sites.index(s) for s in all_sites]
        # Reshape to (2, 2, ..., 2, 2, ...) and transpose
        tensor = raw_rho.reshape([2] * (2 * k))
        # permute rows and cols
        transpose_axes = perm + [p + k for p in perm]
        tensor = np.transpose(tensor, axes=transpose_axes)
        raw_rho = tensor.reshape((2**k, 2**k))
        
    return QuantumCluster(all_sites, raw_rho)


def _build_cluster_effective_h(
    cluster: QuantumCluster,
    clusters: List[QuantumCluster],
    model: SpinChainModel,
) -> np.ndarray:
    """Build effective Hamiltonian for cluster including internal interactions and mean fields."""
    k = len(cluster.sites)
    dim = 2 ** k
    h_eff = np.zeros((dim, dim), dtype=complex)
    
    # 1. 1-local terms inside cluster
    for site in cluster.sites:
        for t1 in model.get_terms_for_site(site):
            loc_idx = cluster.local_index(site)
            h_eff += _embed_single_site_op(t1.matrix, loc_idx, k)
            
    # 2. 2-local terms
    for edge in model.edges:
        s1, s2 = edge
        in1 = cluster.contains_site(s1)
        in2 = cluster.contains_site(s2)
        
        terms = model.get_terms_for_edge(edge)
        if not terms:
            continue
        h_edge = sum((t.matrix for t in terms), np.zeros((4, 4), dtype=complex))
        
        if in1 and in2:
            # Fully internal to this cluster: exact 2-body interaction
            loc1 = cluster.local_index(s1)
            loc2 = cluster.local_index(s2)
            h_eff += _embed_two_site_op(h_edge, loc1, loc2, k)
        elif in1 and not in2:
            # Boundary interaction: contract with marginal of s2 from its containing cluster
            c_other = next(c for c in clusters if c.contains_site(s2))
            rho_s2 = c_other.single_site_marginal(s2)
            # Contract second site of h_edge
            t_tensor = h_edge.reshape((2, 2, 2, 2))
            m_s1 = np.einsum("abcd,db->ac", t_tensor, rho_s2)
            loc1 = cluster.local_index(s1)
            h_eff += _embed_single_site_op(m_s1, loc1, k)
        elif in2 and not in1:
            # Boundary interaction: contract with marginal of s1
            c_other = next(c for c in clusters if c.contains_site(s1))
            rho_s1 = c_other.single_site_marginal(s1)
            t_tensor = h_edge.reshape((2, 2, 2, 2))
            m_s2 = np.einsum("abcd,ca->bd", t_tensor, rho_s1)
            loc2 = cluster.local_index(s2)
            h_eff += _embed_single_site_op(m_s2, loc2, k)
            
    return h_eff


def _embed_single_site_op(op: np.ndarray, loc_idx: int, k: int) -> np.ndarray:
    """Embed 2x2 operator at loc_idx in a k-qubit cluster."""
    I2 = np.eye(2, dtype=complex)
    res = np.array([[1.0]], dtype=complex)
    for i in range(k):
        curr = op if i == loc_idx else I2
        res = np.kron(res, curr)
    return res


def _embed_two_site_op(op4: np.ndarray, loc1: int, loc2: int, k: int) -> np.ndarray:
    """Embed 4x4 two-site operator acting on (loc1, loc2) in a k-qubit cluster."""
    I2 = np.eye(2, dtype=complex)
    if loc1 > loc2:
        loc1, loc2 = loc2, loc1
        # Swap sites in 4x4 matrix
        tensor = op4.reshape((2, 2, 2, 2))
        tensor = np.transpose(tensor, (1, 0, 3, 2))
        op4 = tensor.reshape((4, 4))
        
    # Full embedding via Kronecker product with canonical transposition
    full = np.zeros((2**k, 2**k), dtype=complex)
    # Decompose op4 into sum of tensor products of single-qubit matrices
    paulis = [np.eye(2, dtype=complex),
              np.array([[0, 1], [1, 0]], dtype=complex),
              np.array([[0, -1j], [1j, 0]], dtype=complex),
              np.array([[1, 0], [0, -1]], dtype=complex)]
    for p1 in paulis:
        for p2 in paulis:
            basis_op = np.kron(p1, p2)
            coeff = 0.25 * np.trace(basis_op.conj().T @ op4)
            if coeff != 0:
                term = np.array([[1.0]], dtype=complex)
                for i in range(k):
                    if i == loc1:
                        term = np.kron(term, p1)
                    elif i == loc2:
                        term = np.kron(term, p2)
                    else:
                        term = np.kron(term, I2)
                full += coeff * term
    return full


def _cluster_residual_rates(model: SpinChainModel, clusters: List[QuantumCluster]) -> Dict[Tuple[int, int], float]:
    """Sample boundary normal residuals on full cluster factors, not site marginals.

    Internally correlated clusters can have maximally mixed boundary marginals
    while their full boundary commutator is nonzero. Use the same bipartite
    retraction on the cluster density matrices and the embedded edge operator.
    """
    rates = {}
    for edge in model.edges:
        a, b = edge
        c_a = next(c for c in clusters if c.contains_site(a))
        c_b = next(c for c in clusters if c.contains_site(b))
        terms = model.get_terms_for_edge(edge)
        if c_a is c_b or not terms:
            rates[edge] = 0.0
            continue
        h_ab = sum((t.matrix for t in terms), np.zeros((4, 4), dtype=complex))
        size_a, size_b = len(c_a.sites), len(c_b.sites)
        h_cluster = _embed_two_site_op(h_ab, c_a.local_index(a),
                                      size_a + c_b.local_index(b), size_a + size_b)
        _, rate = compute_edge_residual(c_a.rho, c_b.rho, h_cluster, c_a.dim, c_b.dim)
        rates[edge] = rate
    return rates


def compute_edge_hop_distance(
    model: SpinChainModel,
    edge: Tuple[int, int],
    source_sites: Sequence[int],
) -> int:
    """Compute minimum graph hop distance from edge vertices to declared source sites."""
    if not source_sites:
        return 0
    N = model.num_sites
    adj: Dict[int, List[int]] = {i: [] for i in range(N)}
    for u, v in model.edges:
        adj[u].append(v)
        adj[v].append(u)

    distances: Dict[int, int] = {}
    queue = [int(s) for s in source_sites]
    for s in queue:
        distances[s] = 0

    head = 0
    while head < len(queue):
        curr = queue[head]
        head += 1
        d_curr = distances[curr]
        for neighbor in adj.get(curr, []):
            if neighbor not in distances:
                distances[neighbor] = d_curr + 1
                queue.append(neighbor)

    u, v = edge
    return min(distances.get(u, N), distances.get(v, N))


def is_edge_in_causal_cone(
    model: SpinChainModel,
    edge: Tuple[int, int],
    source_sites: Sequence[int],
    current_time: float,
    v_lr: float,
    causal_margin: float = 0.0,
) -> bool:
    """Determine whether edge lies within the forward causal light cone r <= v_LR * t + margin."""
    if isinstance(v_lr, bool) or not isinstance(v_lr, (int, float, np.number)) or not np.isfinite(v_lr) or v_lr <= 0.0:
        raise ValueError("v_lr must be a positive finite real")
    if isinstance(current_time, bool) or not isinstance(current_time, (int, float, np.number)) or not np.isfinite(current_time) or current_time < 0.0:
        raise ValueError("current_time must be a nonnegative finite real")
    if isinstance(causal_margin, bool) or not isinstance(causal_margin, (int, float, np.number)) or not np.isfinite(causal_margin) or causal_margin < 0.0:
        raise ValueError("causal_margin must be a nonnegative finite real")
    if not source_sites:
        return True
    dist = compute_edge_hop_distance(model, edge, source_sites)
    r_light = float(v_lr) * float(current_time) + float(causal_margin)
    return bool(dist <= r_light)


def evaluate_causal_envelope_metrics(
    result: SimulationResult,
    model: SpinChainModel,
    source_sites: Sequence[int],
    v_lr: float,
    causal_margin: float = 0.0,
) -> Dict[str, float | int | bool]:
    """Audit adaptive trajectory to verify absence of acausal merges outside the light cone."""
    if isinstance(v_lr, bool) or not isinstance(v_lr, (int, float, np.number)) or not np.isfinite(v_lr) or v_lr <= 0.0:
        raise ValueError("v_lr must be a positive finite real")
    if isinstance(causal_margin, bool) or not isinstance(causal_margin, (int, float, np.number)) or not np.isfinite(causal_margin) or causal_margin < 0.0:
        raise ValueError("causal_margin must be a nonnegative finite real")
    spacelike_merges = 0
    max_spacelike_res = 0.0

    cluster_hist = result.metadata.get("cluster_history", [])
    times = result.times

    for step_idx, t in enumerate(times):
        r_cone = float(v_lr) * float(t) + float(causal_margin)
        clusters_at_t = cluster_hist[step_idx] if step_idx < len(cluster_hist) else []
        for edge in model.edges:
            dist = compute_edge_hop_distance(model, edge, source_sites)
            if dist > r_cone:
                res_val = float(result.residuals[edge][step_idx])
                if res_val > max_spacelike_res:
                    max_spacelike_res = res_val
                for c in clusters_at_t:
                    if edge[0] in c and edge[1] in c:
                        spacelike_merges += 1
                        break

    return {
        "spacelike_merges_count": spacelike_merges,
        "max_spacelike_residual": max_spacelike_res,
        "causal_purity_verified": bool(spacelike_merges == 0),
    }


def evolve_adaptive(
    model: SpinChainModel,
    rho0: np.ndarray | Sequence[np.ndarray],
    obs_dict: Dict[str, np.ndarray] | Sequence[np.ndarray] | None = None,
    t_span: Sequence[float] = (0.0, 0.1, 0.2, 0.5, 1.0),
    tol: float = 0.2,
    max_bond: int = 4,
    refine_threshold: float = 0.05,
    v_lr: float | None = None,
    source_sites: Sequence[int] | None = None,
    causal_margin: float = 0.0,
) -> SimulationResult:
    """Execute Certified Adaptive Quantum Dynamics (CAQD) simulation.
    
    Dynamically identifies bottleneck entanglement cuts where local defect rate
    nu_e = ||n_e||_1 is large, and adaptively refines the variational manifold
    by merging clusters across those edges. The target is heuristic; this finite
    implementation does not certify B_O(t) <= tol or integration error.
    
    Args:
        model: SpinChainModel instance.
        rho0: Initial state (full density matrix or single-site marginals).
        obs_dict: Dictionary or sequence of physical observables.
        t_span: Evaluation time sequence.
        tol: Target observable error tolerance epsilon.
        max_bond: Maximum allowed cluster size (in number of qubits) during adaptation.
        refine_threshold: Local rate threshold triggering proactive bond expansion.
        v_lr: Optional Lieb-Robinson velocity enforcing causal cone refinement.
        source_sites: Optional sequence of perturbation/source site indices.
        causal_margin: Optional distance buffer added to the causal light-cone radius.
        
    Returns:
        SimulationResult containing adaptive trajectory, observables, and error bounds.
    """
    times = validate_times(t_span)
    N = model.num_sites
    if not isinstance(max_bond, (int, np.integer)) or isinstance(max_bond, bool) or max_bond < 1:
        raise ValueError("max_bond must be a positive integer cluster-size ceiling")
    if not np.isfinite(tol) or tol < 0 or not np.isfinite(refine_threshold) or refine_threshold < 0:
        raise ValueError("tol and refine_threshold must be finite and nonnegative")
    if v_lr is not None:
        if isinstance(v_lr, bool) or not isinstance(v_lr, (int, float, np.number)) or not np.isfinite(v_lr) or v_lr <= 0.0:
            raise ValueError("v_lr must be a positive finite real")
        v_lr = float(v_lr)
    if source_sites is not None:
        raw_sources = list(source_sites)
        if any(isinstance(s, bool) or not isinstance(s, (int, np.integer)) or not (0 <= s < N) for s in raw_sources):
            raise ValueError("source_sites must be integers in range [0, N-1]")
        source_sites = sorted(set(raw_sources))
    if isinstance(causal_margin, bool) or not isinstance(causal_margin, (int, float, np.number)) or not np.isfinite(causal_margin) or causal_margin < 0:
        raise ValueError("causal_margin must be a nonnegative finite real")
    causal_margin = float(causal_margin)
    
    # Format observables
    if obs_dict is None:
        obs_map: Dict[str, np.ndarray] = {}
    elif isinstance(obs_dict, (list, tuple)):
        obs_map = {f"obs_{i}": np.array(o, dtype=complex) for i, o in enumerate(obs_dict)}
    else:
        obs_map = {k: np.array(v, dtype=complex) for k, v in obs_dict.items()}
        
    max_obs_norm = max([operator_norm(o) for o in obs_map.values()], default=1.0)
    
    # Initialize clusters: initially each site is an independent cluster (chi=1)
    if isinstance(rho0, np.ndarray) and rho0.shape == (2**N, 2**N):
        rho0 = validate_density_matrix(rho0, model.dim)
        init_marginals = [partial_trace(rho0, [i], N) for i in range(N)]
        product = np.array([[1.0]], dtype=complex)
        for marginal in init_marginals:
            product = np.kron(product, marginal)
        if not np.allclose(rho0, product, atol=1e-10, rtol=1e-10):
            raise ValueError("Product-state initialization required; correlated rho0 would introduce unaccounted initial error.")
    elif isinstance(rho0, (list, tuple)) and len(rho0) == N:
        init_marginals = [np.array(m, dtype=complex) for m in rho0]
    else:
        raise ValueError("rho0 must be full state (2^N, 2^N) or list of N single-site density matrices.")
        
    clusters: List[QuantumCluster] = [QuantumCluster([i], init_marginals[i]) for i in range(N)]
    
    states: List[np.ndarray] = []
    obs_trajs: Dict[str, List[float]] = {name: [] for name in obs_map}
    residual_history: Dict[Tuple[int, int], List[float]] = {e: [] for e in model.edges}
    total_rates_list: List[float] = []
    cluster_history: List[List[List[int]]] = []
    
    current_time = times[0]
    cumulative_integral = 0.0
    integral_history: List[float] = []
    incoming_rate_history: List[float] = []
    prev_outgoing_rate = 0.0

    for target_time in times:
        dt = target_time - current_time

        # Advance the previous partition first. All effective Hamiltonians use
        # the same pre-substep state so arbitrary cluster order cannot bias it.
        if dt > 0:
            # Avoid an extra substep caused solely by translating a time grid
            # (e.g. 2.1 - 2.0 is slightly larger than 0.1 in binary arithmetic).
            n_substeps = max(2, int(np.ceil(dt / 0.005 - 1e-12)))
            sub_dt = dt / n_substeps
            for _ in range(n_substeps):
                effective_h = [_build_cluster_effective_h(c, clusters, model) for c in clusters]
                for c, h_eff in zip(clusters, effective_h):
                    u = scipy.linalg.expm(-1.0j * h_eff * sub_dt)
                    c.rho = u @ c.rho @ u.conj().T
                    c.rho = 0.5 * (c.rho + c.rho.conj().T)
                    c.rho /= np.real(np.trace(c.rho))
        current_time = target_time

        # Incoming rate belongs to this time and the partition used over the
        # preceding interval. A merge must not erase its accumulated estimate.
        edge_rates = _cluster_residual_rates(model, clusters)
        incoming_rate = float(sum(edge_rates.values()))
        if dt > 0:
            cumulative_integral += 0.5 * (prev_outgoing_rate + incoming_rate) * dt
        incoming_rate_history.append(incoming_rate)
        integral_history.append(cumulative_integral)

        horizon_remaining = times[-1] - target_time
        predicted = max_obs_norm * (cumulative_integral + incoming_rate * horizon_remaining)
        if predicted > tol or max(edge_rates.values(), default=0.0) > refine_threshold:
            # A blocked strongest edge must not hide a feasible weaker merge.
            feasible = []
            for edge, rate in edge_rates.items():
                if v_lr is not None and source_sites is not None:
                    if not is_edge_in_causal_cone(model, edge, source_sites, target_time, v_lr, causal_margin):
                        continue
                c1 = next(c for c in clusters if c.contains_site(edge[0]))
                c2 = next(c for c in clusters if c.contains_site(edge[1]))
                if c1 is not c2 and len(c1.sites) + len(c2.sites) <= max_bond and rate > 1e-12:
                    feasible.append((rate, edge, c1, c2))
            if feasible:
                _, _, c1, c2 = max(feasible, key=lambda candidate: candidate[0])
                merged = _merge_clusters(c1, c2)
                clusters.remove(c1)
                clusters.remove(c2)
                clusters.append(merged)
                # Recompute every edge for the new partition, including other
                # edges that have become internal and changed boundary factors.
                edge_rates = _cluster_residual_rates(model, clusters)
        tot_rate = float(sum(edge_rates.values()))
        prev_outgoing_rate = tot_rate

        # Reconstruct full state representation for metrics & observables
        # Sort clusters by minimum site index
        sorted_clusters = sorted(clusters, key=lambda c: c.sites[0])
        full_rho = np.array([[1.0]], dtype=complex)
        for c in sorted_clusters:
            full_rho = np.kron(full_rho, c.rho)
            
        # Periodic/nonadjacent merges can interleave cluster site indices.
        raw_sites = [site for cluster in sorted_clusters for site in cluster.sites]
        if raw_sites != list(range(N)):
            order = [raw_sites.index(site) for site in range(N)]
            full_rho = full_rho.reshape([2] * (2 * N)).transpose(order + [i + N for i in order]).reshape((2**N, 2**N))
        states.append(full_rho)
        cluster_history.append([list(c.sites) for c in clusters])
        
        for name, O in obs_map.items():
            exp_val = float(np.real(np.trace(O @ full_rho)))
            obs_trajs[name].append(exp_val)
            
        for e in model.edges:
            residual_history[e].append(edge_rates.get(e, 0.0))
        total_rates_list.append(tot_rate)
        
    return SimulationResult(
        times=times,
        states=states,
        observables={k: np.array(v) for k, v in obs_trajs.items()},
        residuals={k: np.array(v) for k, v in residual_history.items()},
        total_rates=np.array(total_rates_list),
        method="adaptive",
        metadata={
            "cluster_history": cluster_history,
            "final_clusters": [c.sites for c in clusters],
            "max_bond": max_bond,
            "target_tolerance": tol,
            "certificate_status": "HEURISTIC_UNCERTIFIED",
            "residual_scope": "full cluster factors; sampled ideal tangent residual",
            "cumulative_residual_estimates": np.array(integral_history),
            "pre_refinement_total_rates": np.array(incoming_rate_history),
            "estimated_target_met": bool(max_obs_norm * cumulative_integral <= tol),
            "v_lr": v_lr,
            "source_sites": list(source_sites) if source_sites is not None else None,
            "causal_filtering_active": bool(v_lr is not None and source_sites is not None),
        },
    )
