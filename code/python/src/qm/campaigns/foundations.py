# AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)
"""Foundational walk, discrete walk engines, and simplicial complex quantum mechanics.

This module serves as the primary backwards-compatible public facade for the
finite quantum mechanics application suite. The underlying monolithic implementation
has been decomposed into focused domain submodules:
  - primitives.py: Core Pauli matrices, Schatten norms, partial traces, and operators
  - rungs.py: Foundational walk Rungs 1 through 8 (CochainPacket, Born rule, POVM, Gleason)
  - discrete_walk_engines.py: Phase 1 separating experiment and Phase 2 direct walk packets
  - simplicial_complex_qm.py: Simplicial 3-complex evolution, MUB frame polytopes, and graph states
  - stabilizer_codes.py: Bit-flip, CSS [[4, 2, 2]], and Steane [[7, 1, 3]] error-correcting codes
  - quantum_protocols.py: Bell-CHSH, Pell-Tsirelson, Clifford/T, Wigner negativity, teleportation, superdense coding
  - born_normalization.py: Born normalization and conditional Hilbert lift
  - interference.py: Non-L1 interference cross-terms and superposition fibers
  - contextuality_f2.py: Mermin-Peres square and F2 parity obstructions
  - quantum_correlation.py: Bipartite correlation defect and escape rate certificates
  - primitive_difference.py: Typed primitive differences and cocycle checks
  - finite_qm_engine.py: 6-rung ladder engine and typed evaluation dataclasses

AuthorityEffect: None.
"""

from __future__ import annotations

# 2. Canonical Math Crates
from ..domain.primitive_difference import PrimitiveDifference

# 1. Primitives and Operator Constants
from ..domain.primitives import (
    HADAMARD_2,
    I2,
    PHASE_S,
    SIGMA_I,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    commutator,
    dagger,
    is_density_matrix,
    ket00,
    kron_all,
    marginals,
    mutual_information,
    operator_norm,
    partial_trace_a,
    partial_trace_b,
    pure_state,
    purity,
    trace_norm,
    von_neumann_entropy,
)

# 8. Advanced Targets (Loops 4, 5, 13-22)
from .advanced_targets import (
    D3_STATE_BUILDERS,
    D4_STATE_BUILDERS,
    build_cayley_graph_s3,
    build_cayley_graph_s4,
    build_cayley_graph_sn,
    build_d3_mub_projectors,
    build_d4_mub_projectors,
    build_prime_p_phase_point_operators,
    build_shor_nine_qubit_code,
    build_sp2_f2_generators_and_elements,
    build_sp4_f2_generators_and_elements,
    build_toric_code_2x2,
    compute_richardson_weights,
    compute_symplectic_group_order,
    decode_and_recover_shor,
    discrete_grover_step,
    discrete_phase_estimation,
    discrete_qft,
    evaluate_anyon_defect_algebra,
    evaluate_ballistic_propagation,
    evaluate_d4_clifton_kent_deficit,
    evaluate_discrete_weyl_commutation,
    evaluate_eastin_knill_obstruction,
    evaluate_finite_commutator_trace_obstruction,
    evaluate_prime_p_discrete_wigner,
    extract_shor_syndrome,
    grover_exact_trigonometric_orbit,
    reconstruct_d3_state_from_mub_probabilities,
    reconstruct_d4_state_from_mub_probabilities,
    reconstruct_state_from_mub_probabilities,
    richardson_zero_noise_extrapolate,
    simulate_anyon_braiding_phase,
    simulate_d4_mub_tomography,
    simulate_discrete_quantum_walk_cayley,
    simulate_mitigated_quantum_expectation,
    simulate_mub_tomography,
    simulate_shor_error_recovery,
    stone_von_neumann_finite_cyclic_report,
    verify_all_single_qubit_errors_recovery,
    verify_clifford_symplectic_isomorphism_n1,
    verify_cyclotomic_dyadic_projection,
    verify_gross_stabilizer_covariance,
    verify_grover_n4_exact_one_step,
    verify_mub_inversion_all_tested_states,
    verify_mub_inversion_completeness,
    verify_target4_rational_cayley_so8,
    verify_target5_pentagon_identity_q5,
    verify_toric_homology_and_degeneracy,
)
from .born_normalization import (
    PaperEvaluator,
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)
from .contextuality_f2 import (
    context_products,
    contextuality_report,
    enumerate_all_assignments,
    f2_rank,
    f2_system,
    parity_obstruction,
    peres_mermin_square,
)

# 4. Phase 1 Separating Experiment & Phase 2 Discrete Walk Engines
from .discrete_walk import (
    CABELLO_9_BASES,
    CABELLO_18_VECTORS,
    build_glued_simplex_packet,
    build_mzi_packet,
    build_sorkin_3slit_packet,
    cabello_interface_from_packet,
    cayley_evolution_from_packet,
    evaluate_quadratic_frame_sum_rational,
    evaluate_quartic_frame_sum_rational,
    monotone_admission_from_packet,
    quartic_homogeneous_polynomial_reduction,
    sorkin_3slit_amplitudes_from_cochain,
    sorkin_3slit_phases_from_cochain,
    verify_quartic_frame_additivity_failure_exact,
)
from .finite_qm_engine import (
    FiniteQMEngine,
    Rung1BornRedundancy,
    Rung2DensityPurity,
    Rung3CPTPShadow,
    Rung4PathSum,
    Rung5SuperpositionFiber,
    Rung6InterferenceCrossTerm,
    evaluate_6rung_ladder,
)
from .interference import (
    cross_term,
    diagonal_data,
    interfered_weight,
    phase_sweep,
    theorem_a1_separation,
    two_path_cross_term,
)
from .quantum_correlation import (
    EscapeRateCertificate,
    InteractionResidualEngine,
    correlation_defect,
    partial_trace_left,
    partial_trace_right,
)

# 6. Quantum Information Protocols & Nonlocality (Loops 4-7, 11-12)
from .quantum_protocols import (
    build_qutrit_phase_point_operators,
    derive_bell_singlet_correlation,
    evaluate_clifford_pauli_conjugations,
    evaluate_discrete_pythagorean_bell_chsh,
    evaluate_pell_pythagorean_tsirelson_convergence,
    evaluate_qutrit_discrete_wigner,
    evaluate_t_gate_orbit_departure,
    simulate_discrete_quantum_teleportation,
    simulate_discrete_superdense_coding,
)

# 3. Rungs 1-8 Domain Implementation
from .rungs import (
    BoundaryDefense,
    CochainPacket,
    amplitudes_to_probabilities,
    bell_state,
    bipartite_linear_entropy,
    bipartite_von_neumann_entropy,
    born_normalization,
    build_triangle_packet,
    check_difference_antisymmetry,
    check_difference_cocycle,
    compute_cycle_holonomy,
    continuous_generator_branch_count,
    density_matrix_frame_function,
    discrete_gleason_triads_d3,
    discrete_unitary_step,
    evaluate_frame_function,
    get_boundary_defense,
    gleason_dimension_2_counterexample,
    is_entangled_pure_state,
    is_orthonormal_frame,
    is_same,
    is_unitary,
    is_valid_povm,
    non_selective_measurement_decoherence,
    partial_trace,
    povm_probabilities,
    primitive_difference,
    rational_pythagorean_frames_d2,
    schmidt_decomposition,
    sorkin_3slit_parameter,
    superposition_interference_test,
    superposition_quotient_fiber,
    two_path_interference,
    verify_born_normalization_redundancy,
    verify_cptp_contractivity,
    verify_gleason_frame_additivity,
    verify_mermin_peres_contextuality,
    verify_non_signaling,
    verify_ray_invariance,
    weights_to_born_density,
    weights_to_probabilities,
)

# 5. Simplicial Complex Quantum Mechanics (Loops 1-3)
from .simplicial_qm import (
    arbitrary_degree_polynomial_reduction,
    build_octahedral_mub_polytope,
    build_octahedron_graph_state_stabilizers,
    build_octahedron_packet,
    build_tetrahedron_packet,
    cayley_evolution_on_simplicial_3complex,
    evaluate_octahedral_clifton_kent,
    evaluate_octahedral_depolarizing_noise_threshold,
    evaluate_octahedral_graph_state_entanglement,
    polynomial_reduce_mod_circle,
    solve_frame_additive_homogeneous_polynomial,
    tetrahedron_3cell_boundary,
)

# 7. Stabilizer and Topological Codes (Loops 8-10)
from .stabilizer_codes import (
    build_four_qubit_css_surface_code,
    build_steane_seven_qubit_code,
    build_three_qubit_bitflip_code,
)

__all__ = [
    # Constants
    "I2",
    "SIGMA_I",
    "SIGMA_X",
    "SIGMA_Y",
    "SIGMA_Z",
    "HADAMARD_2",
    "PHASE_S",
    "kron_all",
    "trace_norm",
    "operator_norm",
    "partial_trace_a",
    "partial_trace_b",
    "commutator",
    "dagger",
    "is_density_matrix",
    "purity",
    "von_neumann_entropy",
    "mutual_information",
    "marginals",
    "pure_state",
    "ket00",
    # Crates
    "PrimitiveDifference",
    "l1_to_l2_amplitude_lift",
    "verify_born_normalization",
    "PaperEvaluator",
    "diagonal_data",
    "interfered_weight",
    "cross_term",
    "two_path_cross_term",
    "phase_sweep",
    "theorem_a1_separation",
    "peres_mermin_square",
    "context_products",
    "f2_system",
    "f2_rank",
    "parity_obstruction",
    "enumerate_all_assignments",
    "contextuality_report",
    "partial_trace_left",
    "partial_trace_right",
    "correlation_defect",
    "EscapeRateCertificate",
    "InteractionResidualEngine",
    "FiniteQMEngine",
    "Rung1BornRedundancy",
    "Rung2DensityPurity",
    "Rung3CPTPShadow",
    "Rung4PathSum",
    "Rung5SuperpositionFiber",
    "Rung6InterferenceCrossTerm",
    "evaluate_6rung_ladder",
    # Rungs 1-8
    "primitive_difference",
    "is_same",
    "check_difference_cocycle",
    "check_difference_antisymmetry",
    "CochainPacket",
    "build_triangle_packet",
    "weights_to_probabilities",
    "verify_ray_invariance",
    "amplitudes_to_probabilities",
    "born_normalization",
    "verify_born_normalization_redundancy",
    "weights_to_born_density",
    "compute_cycle_holonomy",
    "two_path_interference",
    "sorkin_3slit_parameter",
    "superposition_quotient_fiber",
    "superposition_interference_test",
    "schmidt_decomposition",
    "is_entangled_pure_state",
    "verify_mermin_peres_contextuality",
    "partial_trace",
    "bipartite_linear_entropy",
    "bipartite_von_neumann_entropy",
    "bell_state",
    "verify_non_signaling",
    "is_unitary",
    "discrete_unitary_step",
    "continuous_generator_branch_count",
    "is_valid_povm",
    "povm_probabilities",
    "non_selective_measurement_decoherence",
    "verify_cptp_contractivity",
    "BoundaryDefense",
    "get_boundary_defense",
    "is_orthonormal_frame",
    "evaluate_frame_function",
    "density_matrix_frame_function",
    "verify_gleason_frame_additivity",
    "gleason_dimension_2_counterexample",
    "discrete_gleason_triads_d3",
    "rational_pythagorean_frames_d2",
    # Discrete walk engines
    "CABELLO_18_VECTORS",
    "CABELLO_9_BASES",
    "evaluate_quartic_frame_sum_rational",
    "evaluate_quadratic_frame_sum_rational",
    "verify_quartic_frame_additivity_failure_exact",
    "quartic_homogeneous_polynomial_reduction",
    "build_mzi_packet",
    "build_sorkin_3slit_packet",
    "sorkin_3slit_phases_from_cochain",
    "sorkin_3slit_amplitudes_from_cochain",
    "cayley_evolution_from_packet",
    "build_glued_simplex_packet",
    "cabello_interface_from_packet",
    "monotone_admission_from_packet",
    # Simplicial complex QM
    "arbitrary_degree_polynomial_reduction",
    "polynomial_reduce_mod_circle",
    "solve_frame_additive_homogeneous_polynomial",
    "tetrahedron_3cell_boundary",
    "build_tetrahedron_packet",
    "build_octahedron_packet",
    "cayley_evolution_on_simplicial_3complex",
    "build_octahedral_mub_polytope",
    "evaluate_octahedral_clifton_kent",
    "build_octahedron_graph_state_stabilizers",
    "evaluate_octahedral_depolarizing_noise_threshold",
    "evaluate_octahedral_graph_state_entanglement",
    # Quantum protocols
    "evaluate_discrete_pythagorean_bell_chsh",
    "derive_bell_singlet_correlation",
    "evaluate_pell_pythagorean_tsirelson_convergence",
    "evaluate_clifford_pauli_conjugations",
    "evaluate_t_gate_orbit_departure",
    "build_qutrit_phase_point_operators",
    "evaluate_qutrit_discrete_wigner",
    "simulate_discrete_quantum_teleportation",
    "simulate_discrete_superdense_coding",
    # Stabilizer codes
    "build_three_qubit_bitflip_code",
    "build_four_qubit_css_surface_code",
    "build_steane_seven_qubit_code",
    # Advanced Targets (Loops 4, 5, 13-22)
    "verify_target4_rational_cayley_so8", "verify_target5_pentagon_identity_q5",
    "build_prime_p_phase_point_operators", "evaluate_prime_p_discrete_wigner", "verify_gross_stabilizer_covariance",
    "build_shor_nine_qubit_code", "extract_shor_syndrome", "decode_and_recover_shor", "simulate_shor_error_recovery", "verify_all_single_qubit_errors_recovery",
    "discrete_qft", "discrete_phase_estimation", "verify_cyclotomic_dyadic_projection",
    "build_toric_code_2x2", "verify_toric_homology_and_degeneracy", "evaluate_anyon_defect_algebra", "simulate_anyon_braiding_phase",
    "discrete_grover_step", "grover_exact_trigonometric_orbit", "verify_grover_n4_exact_one_step",
    "compute_symplectic_group_order", "build_sp2_f2_generators_and_elements", "build_sp4_f2_generators_and_elements", "verify_clifford_symplectic_isomorphism_n1", "evaluate_eastin_knill_obstruction",
    "evaluate_finite_commutator_trace_obstruction", "evaluate_discrete_weyl_commutation", "stone_von_neumann_finite_cyclic_report",
    "compute_richardson_weights", "richardson_zero_noise_extrapolate", "simulate_mitigated_quantum_expectation",
    "build_cayley_graph_sn", "build_cayley_graph_s3", "build_cayley_graph_s4", "simulate_discrete_quantum_walk_cayley", "evaluate_ballistic_propagation",
    "build_d3_mub_projectors", "reconstruct_state_from_mub_probabilities", "reconstruct_d3_state_from_mub_probabilities", "simulate_mub_tomography", "verify_mub_inversion_all_tested_states", "verify_mub_inversion_completeness", "D3_STATE_BUILDERS",
    "build_d4_mub_projectors", "reconstruct_d4_state_from_mub_probabilities", "simulate_d4_mub_tomography", "evaluate_d4_clifton_kent_deficit", "D4_STATE_BUILDERS",
]


def foundations_frame_norm():
    """Sum of squared norms of the exported rational Pythagorean frames. Each vector contributes 1."""
    from fractions import Fraction

    total = Fraction(0)
    for frame in rational_pythagorean_frames_d2():
        dot = frame[0][0] * frame[1][0] + frame[0][1] * frame[1][1]
        if dot != 0:
            raise ValueError(f"exported frame is not orthogonal: dot {dot}")
        for vector in frame:
            norm = vector[0] * vector[0] + vector[1] * vector[1]
            if norm != 1:
                raise ValueError(f"exported frame vector has norm {norm}")
            total += norm
    return total
