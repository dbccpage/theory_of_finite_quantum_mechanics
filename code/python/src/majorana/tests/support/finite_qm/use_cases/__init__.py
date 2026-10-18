"""Finite-QM use_cases.

AuthorityEffect: None.
"""

from importlib import import_module as _import_module

__all__ = ['advanced_targets', 'audit_map', 'born_normalization', 'branch_finegraining', 'busch_effects', 'cancellation_certificates', 'cochain', 'composition_tensor_mub', 'contextuality_f2', 'contextuality_thresholds', 'continuous_time_locality_limit', 'continuum_lift', 'cptp_channel', 'cptp_channels_stinespring', 'density_matrix', 'discrete_dynamics', 'discrete_walk_engines', 'dynamics_dichotomy', 'embedding_relativity', 'everett_tree', 'finite_operational_closure_contract', 'finite_qm_engine', 'foundations', 'gleason_cyclotomic', 'growth_refinement', 'heisenberg_representation_uniqueness', 'higher_dim_entanglement', 'interference', 'lattice_gauge_manybody_benchmark', 'mermin_peres', 'norm_approximation_frontier', 'operational_axiom_selection', 'quantum_correlation', 'quantum_protocols', 'refinement_subsystem_tower', 'rungs', 'simplicial_complex_qm', 'stabilizer_codes', 'tensor_commuting_correlation_frontier', 'terminal_price_list', 'tower_topological_completion', 'weyl_ccr_residual']

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    value = _import_module(f"{__name__}.{name}")
    globals()[name] = value
    return value

def __dir__():
    return sorted(set(globals()) | set(__all__))
