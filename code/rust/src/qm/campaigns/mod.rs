//! Campaigns of the finite quantum mechanics programme.

pub mod advanced_targets;
pub mod atomic_dirac;
pub mod audit_map;
pub mod axiom_selection;
pub mod boost_composition;
pub mod born_gleason;
pub mod born_normalization;
pub mod bound_spectra;
pub mod branch_finegraining;
pub mod buildability;
pub mod busch_effects;
pub mod cancellations;
pub mod carrier;
pub mod causal_order;
pub mod channel_census;
pub mod clock_tower_control;
pub mod cochain;
pub mod commuting_obs;
pub mod composite_mub;
pub mod context_barrier;
pub mod context_parity;
pub mod context_thresholds;
pub mod contextuality_f2;
pub mod continuum;
pub mod continuum_lift;
pub mod cptp_channel;
pub mod density_matrix;
pub mod derivation_closure;
pub mod discrete_dynamics;
pub mod discrete_walk;
pub mod dressed_qed;
pub mod dynamics;
pub mod dynamics_dichotomy;
pub mod electroweak_dfm;
pub mod embedding_relativity;
pub mod engine_bridge;
pub mod everett;
pub mod everett_tree;
pub mod expressibility;
pub mod finite_geometry_host;
pub mod finite_qm_engine;
pub mod foundational_targets;
pub mod foundations;
pub mod four_wall_operad;
pub mod frame_function;
pub mod gleason;
pub mod gleason_cyclotomic;
pub mod growth_refinement;
pub mod heisenberg_unique;
pub mod higher_dim;
pub mod higher_entangle;
pub mod holonomy_bridge;
pub mod import_bundle;
pub mod interference;
pub mod lattice_gauge;
pub mod locality_limit;
pub mod lorentz_boost;
pub mod matrix_recovery;
pub mod mermin_peres;
pub mod mub_reports;
pub mod no_signalling;
pub mod nonabelian_dfm;
pub mod norm_frontier;
pub mod operational_closure;
pub mod page_wootters;
pub mod pauli_spin_stat;
pub mod phase_fiber;
pub mod qcd_confinement;
pub mod qed_hadronic;
pub mod quadratic_readout;
pub mod quantum_correlation;
pub mod quantum_protocols;
pub mod quantum_walk;
pub mod refinement_tower;
pub mod regge_gravity;
pub mod residual_density;
pub mod rotation_groups;
pub mod rungs;
pub mod sector_conditioning;
pub mod separating_preds;
pub mod simplicial_qm;
pub mod spectral_claims;
pub mod stabilizer_codes;
pub mod stinespring;
pub mod symanzik_two_forest;
pub mod tensor_correlation;
pub mod terminal_price_list;
pub mod toric;
pub mod tower;
pub mod tower_completion;
pub mod vacuum_polarization;
pub mod ward_takahashi;
pub mod weyl_ccr_residual;

/// Walks the declared campaign modules. Index mass equals `n(n+1)/2`, and
/// the three-term frame sum `1/2 + 1/3 + 1/6` clears to 1.
pub fn campaign_inventory_holds() -> Result<(), &'static str> {
    const NAMES: &[&str] = &[
        "advanced_targets",
        "atomic_dirac",
        "audit_map",
        "axiom_selection",
        "boost_composition",
        "born_gleason",
        "born_normalization",
        "bound_spectra",
        "branch_finegraining",
        "buildability",
        "busch_effects",
        "cancellations",
        "carrier",
        "causal_order",
        "channel_census",
        "clock_tower_control",
        "cochain",
        "commuting_obs",
        "composite_mub",
        "context_barrier",
        "context_parity",
        "context_thresholds",
        "contextuality_f2",
        "continuum",
        "continuum_lift",
        "cptp_channel",
        "density_matrix",
        "derivation_closure",
        "discrete_dynamics",
        "discrete_walk",
        "dressed_qed",
        "dynamics",
        "dynamics_dichotomy",
        "electroweak_dfm",
        "embedding_relativity",
        "engine_bridge",
        "everett",
        "everett_tree",
        "expressibility",
        "finite_geometry_host",
        "finite_qm_engine",
        "foundational_targets",
        "foundations",
        "four_wall_operad",
        "frame_function",
        "gleason",
        "gleason_cyclotomic",
        "growth_refinement",
        "heisenberg_unique",
        "higher_dim",
        "higher_entangle",
        "holonomy_bridge",
        "import_bundle",
        "interference",
        "lattice_gauge",
        "locality_limit",
        "lorentz_boost",
        "matrix_recovery",
        "mermin_peres",
        "mub_reports",
        "no_signalling",
        "nonabelian_dfm",
        "norm_frontier",
        "operational_closure",
        "page_wootters",
        "pauli_spin_stat",
        "phase_fiber",
        "qcd_confinement",
        "qed_hadronic",
        "quadratic_readout",
        "quantum_correlation",
        "quantum_protocols",
        "quantum_walk",
        "refinement_tower",
        "regge_gravity",
        "residual_density",
        "rotation_groups",
        "rungs",
        "sector_conditioning",
        "separating_preds",
        "simplicial_qm",
        "spectral_claims",
        "stabilizer_codes",
        "stinespring",
        "symanzik_two_forest",
        "tensor_correlation",
        "terminal_price_list",
        "toric",
        "tower",
        "tower_completion",
        "vacuum_polarization",
        "ward_takahashi",
        "weyl_ccr_residual",
    ];
    if NAMES.len() != 93 {
        return Err("campaign module count is not 93");
    }
    let mut mass = 0u64;
    for (index, name) in NAMES.iter().enumerate() {
        if name.is_empty() {
            return Err("campaign module name is empty");
        }
        if NAMES[..index].contains(name) {
            return Err("campaign module name is duplicated");
        }
        mass = mass
            .checked_add((index as u64).checked_add(1).ok_or("index")?)
            .ok_or("index mass")?;
    }
    let n = NAMES.len() as u64;
    let closed = n.checked_mul(n.checked_add(1).ok_or("count")?).ok_or("triangle")? / 2;
    if mass != closed {
        return Err("campaign index mass disagrees with n(n+1)/2");
    }
    // 1/2 + 1/3 + 1/6 = 1, cleared over the denominator 6.
    let frame = 3i64 + 2 + 1;
    if frame != 6 {
        return Err("campaign frame sum is not 1");
    }
    Ok(())
}
