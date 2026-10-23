"""Certified Adaptive Quantum Dynamics from Projection Residuals (CAQD).

Finite cluster-product research prototype with sampled residual estimates.
The implemented numerical trajectory is HEURISTIC_UNCERTIFIED.

AuthorityEffect: None.
"""

from caqd.spin_chains import (
    SpinChainModel,
    TFIMChain,
    XXZChain,
    pauli_matrices,
    operator_norm,
    trace_norm,
    hilbert_schmidt_norm,
    partial_trace,
    pauli_on_site,
    two_body_op,
    staggered_magnetization,
    center_correlation,
    transverse_magnetization,
    neel_state,
    polarized_x_state,
    all_up_state,
)

from caqd.residuals import (
    retraction_tangent_projector,
    normal_projector,
    compute_edge_residual,
    compute_local_residuals,
    dual_witness_schatten1,
    verify_lemma_5_3_tangent_isolation,
)

from caqd.dynamics import (
    SimulationResult,
    evolve_exact,
    evolve_mean_field,
)

from caqd.bounds import (
    evaluate_bound,
    compute_cumulative_bounds,
    verify_bound_honesty,
    ObservableVerification,
    CertificateTracker,
)

from caqd.adaptive import (
    evolve_adaptive,
    QuantumCluster,
    compute_edge_hop_distance,
    is_edge_in_causal_cone,
    evaluate_causal_envelope_metrics,
)

__version__ = "1.0.1"

__all__ = [
    # Models & Pauli algebra
    "SpinChainModel",
    "TFIMChain",
    "XXZChain",
    "pauli_matrices",
    "operator_norm",
    "trace_norm",
    "hilbert_schmidt_norm",
    "partial_trace",
    "pauli_on_site",
    "two_body_op",
    "staggered_magnetization",
    "center_correlation",
    "transverse_magnetization",
    "neel_state",
    "polarized_x_state",
    "all_up_state",
    # Residuals & Projections
    "retraction_tangent_projector",
    "normal_projector",
    "compute_edge_residual",
    "compute_local_residuals",
    "dual_witness_schatten1",
    "verify_lemma_5_3_tangent_isolation",
    # Dynamics
    "SimulationResult",
    "evolve_exact",
    "evolve_mean_field",
    # Bounds & Certificates
    "evaluate_bound",
    "compute_cumulative_bounds",
    "verify_bound_honesty",
    "ObservableVerification",
    "CertificateTracker",
    # Adaptive Refinement
    "evolve_adaptive",
    "QuantumCluster",
    "compute_edge_hop_distance",
    "is_edge_in_causal_cone",
    "evaluate_causal_envelope_metrics",
    "__version__",
]

