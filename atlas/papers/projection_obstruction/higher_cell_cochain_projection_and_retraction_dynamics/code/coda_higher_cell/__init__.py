"""coda_higher_cell: Finite product retractions, scalar cochains, and numerical examples.

AuthorityEffect: None.
"""

from .bicomplex_ddc import (
    DoubleBicomplex,
    bicomplex_curvature_tensor,
    ddc_trace_sequence_evaluation,
    semigroup_defect_tensor,
)
from .cochain_holonomy_bridge import (
    DefectVelocityResult,
    DiscreteContinuumMembrane,
    HolonomyAccumulationReport,
    QuotientStickinessResult,
    build_3simplex_cell_complex,
    compute_boundary_face_holonomies,
    compute_quotient_stickiness_lp,
    evaluate_cochain_holonomy_bridge,
    evaluate_discrete_continuum_membrane,
    evaluate_hamiltonian_defect_velocity,
    map_edge_interactions_to_cochain,
)
from .defect_bounds import (
    duhamel_observable_certificate,
    evaluate_k_party_trace_defect,
    schatten1_dual_witness,
    short_time_k_party_defect_lower_bound,
)
from .k_cell_retraction import (
    highest_order_correlation_projector,
    k_cell_normal_projector,
    k_cell_product_retraction,
    k_cell_tangent_projector,
    partial_trace_k,
    verify_generalized_tangent_isolation,
    verify_marginal_preservation,
)
from .prime_triad_bridge import (
    PrimeTriadCarrier,
    adapter_loss_ledger,
    can_continue_predicate,
    prime_triad_carrier_declaration,
)
from .simplicial_complex import (
    SimplicialComplex,
    hodge_decomposition,
    simplicial_boundary_matrix,
    simplicial_coboundary_matrix,
    simplicial_laplacian,
)

__all__ = [
    "highest_order_correlation_projector",
    "k_cell_tangent_projector",
    "k_cell_normal_projector",
    "k_cell_product_retraction",
    "partial_trace_k",
    "verify_marginal_preservation",
    "verify_generalized_tangent_isolation",
    "SimplicialComplex",
    "simplicial_boundary_matrix",
    "simplicial_coboundary_matrix",
    "simplicial_laplacian",
    "hodge_decomposition",
    "evaluate_k_party_trace_defect",
    "short_time_k_party_defect_lower_bound",
    "schatten1_dual_witness",
    "duhamel_observable_certificate",
    "DoubleBicomplex",
    "bicomplex_curvature_tensor",
    "semigroup_defect_tensor",
    "ddc_trace_sequence_evaluation",
    "PrimeTriadCarrier",
    "prime_triad_carrier_declaration",
    "adapter_loss_ledger",
    "can_continue_predicate",
    "DefectVelocityResult",
    "QuotientStickinessResult",
    "HolonomyAccumulationReport",
    "DiscreteContinuumMembrane",
    "evaluate_hamiltonian_defect_velocity",
    "build_3simplex_cell_complex",
    "map_edge_interactions_to_cochain",
    "compute_boundary_face_holonomies",
    "compute_quotient_stickiness_lp",
    "evaluate_cochain_holonomy_bridge",
    "evaluate_discrete_continuum_membrane",
]

