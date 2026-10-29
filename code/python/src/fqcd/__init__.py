"""FQCD Strong-Coupling Area Law package (Record TFQ-1052).

Governing DAG target node: FQCD-STRONG-COUPLING-AREA-LAW
AuthorityEffect: None
"""

from .strong_coupling_area_law import (
    CONST_K,
    CONST_SIGMA_0,
    area_law_decay_bound,
    area_law_decay_bound_rational,
    cluster_series_geometric_sum,
    cluster_series_geometric_sum_rational,
    collar_tube_contraction,
    collar_tube_contraction_rational,
    coordination_number_delta,
    geometric_cluster_series_bound_satisfied,
    loop_perimeter,
    minimal_spanning_area,
    q8_center_parity_protection,
    q8_cubic_character_invariant,
    q8_cubic_character_invariant_rational,
    s3_cubic_character_invariant,
    s3_cubic_character_invariant_rational,
    single_plaquette_character_activity_zn,
    strong_coupling_threshold_beta0,
    strong_coupling_threshold_beta0_rational,
    strong_coupling_threshold_beta0_rational_bounds,
    twod_character_decimation_area_law,
    twod_character_decimation_area_law_rational,
    verify_fqcd_strong_coupling_area_law_witness,
)

__all__ = [
    "CONST_K",
    "CONST_SIGMA_0",
    "area_law_decay_bound",
    "area_law_decay_bound_rational",
    "cluster_series_geometric_sum",
    "cluster_series_geometric_sum_rational",
    "collar_tube_contraction",
    "collar_tube_contraction_rational",
    "coordination_number_delta",
    "geometric_cluster_series_bound_satisfied",
    "loop_perimeter",
    "minimal_spanning_area",
    "q8_center_parity_protection",
    "q8_cubic_character_invariant",
    "q8_cubic_character_invariant_rational",
    "s3_cubic_character_invariant",
    "s3_cubic_character_invariant_rational",
    "single_plaquette_character_activity_zn",
    "strong_coupling_threshold_beta0",
    "strong_coupling_threshold_beta0_rational",
    "strong_coupling_threshold_beta0_rational_bounds",
    "twod_character_decimation_area_law",
    "twod_character_decimation_area_law_rational",
    "verify_fqcd_strong_coupling_area_law_witness",
]
