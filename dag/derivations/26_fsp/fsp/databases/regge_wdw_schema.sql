-- Regge Calculus & Wheeler-DeWitt Normal Forms Relational Database Schema
-- AuthorityEffect: None
-- Dialect: ANSI SQL / SQLite 3 compatible

-- 1. Regge Simplicial Topology & Metric Relvars
CREATE TABLE IF NOT EXISTS ReggeSimplexVertices (
    vertex_id INTEGER PRIMARY KEY,
    label TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ReggeSimplexEdges (
    edge_id INTEGER PRIMARY KEY,
    u INTEGER NOT NULL,
    v INTEGER NOT NULL,
    length REAL NOT NULL CHECK (length > 0),
    length_sq REAL NOT NULL CHECK (length_sq > 0),
    FOREIGN KEY (u) REFERENCES ReggeSimplexVertices(vertex_id),
    FOREIGN KEY (v) REFERENCES ReggeSimplexVertices(vertex_id),
    CHECK (u < v)
);

CREATE TABLE IF NOT EXISTS ReggeSimplexTriangles (
    triangle_id INTEGER PRIMARY KEY,
    v1 INTEGER NOT NULL,
    v2 INTEGER NOT NULL,
    v3 INTEGER NOT NULL,
    area REAL NOT NULL CHECK (area > 0),
    CHECK (v1 < v2 AND v2 < v3)
);

CREATE TABLE IF NOT EXISTS ReggeSimplexTetrahedra (
    tetrahedron_id INTEGER PRIMARY KEY,
    v1 INTEGER NOT NULL,
    v2 INTEGER NOT NULL,
    v3 INTEGER NOT NULL,
    v4 INTEGER NOT NULL,
    volume REAL NOT NULL CHECK (volume > 0),
    CHECK (v1 < v2 AND v2 < v3 AND v3 < v4)
);

-- 2. Curvature Deficits & Regge Action
CREATE TABLE IF NOT EXISTS ReggeDeficitAngles (
    hinge_edge_id INTEGER PRIMARY KEY,
    hinge_length REAL NOT NULL,
    sum_dihedral_angles REAL NOT NULL,
    deficit_angle REAL NOT NULL, -- 2*pi - sum_dihedral_angles
    regge_action_contribution REAL NOT NULL, -- hinge_length * deficit_angle
    FOREIGN KEY (hinge_edge_id) REFERENCES ReggeSimplexEdges(edge_id)
);

-- View: Total Regge Action
CREATE VIEW IF NOT EXISTS ReggeActionTotalView AS
SELECT 
    COUNT(*) AS total_hinges,
    SUM(regge_action_contribution) AS total_einstein_regge_action,
    SUM(hinge_length) AS total_hinge_length
FROM ReggeDeficitAngles;

-- 3. BQNF Curvature Defect & Pachner CDC Stream
CREATE TABLE IF NOT EXISTS ReggePachnerLog (
    change_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pachner_type TEXT NOT NULL CHECK (pachner_type IN ('2_to_3', '3_to_2', '1_to_4', '4_to_1', 'metric_deformation')),
    affected_hinge INTEGER NOT NULL,
    prior_deficit REAL NOT NULL,
    new_deficit REAL NOT NULL,
    delta_defect REAL NOT NULL,
    disposition TEXT NOT NULL CHECK (disposition IN ('Repair', 'Recompute', 'Refuse', 'Preserve')),
    repair_potential REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Wheeler-DeWitt Timeless Global Quantum State
CREATE TABLE IF NOT EXISTS WdwGlobalState (
    clock_id INTEGER NOT NULL,
    volume_state_id INTEGER NOT NULL,
    amplitude REAL NOT NULL,
    PRIMARY KEY (clock_id, volume_state_id)
);

CREATE TABLE IF NOT EXISTS WdwHamiltonianOperator (
    source_state_id INTEGER NOT NULL,
    target_state_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    PRIMARY KEY (source_state_id, target_state_id)
);

-- 5. Relational Conditioning & Emergent Time View
CREATE VIEW IF NOT EXISTS RelationalEvolutionView AS
SELECT 
    src.clock_id AS current_clock,
    src.clock_id + 1 AS next_clock,
    op.target_state_id AS evolved_state_id,
    SUM(src.amplitude * op.weight) AS evolved_amplitude
FROM WdwGlobalState src
JOIN WdwHamiltonianOperator op ON src.volume_state_id = op.source_state_id
GROUP BY src.clock_id, op.target_state_id;

-- 6. Wheeler-DeWitt Constraint Residual View
CREATE VIEW IF NOT EXISTS WdwConstraintResidualView AS
SELECT 
    v.next_clock,
    v.evolved_state_id,
    v.evolved_amplitude,
    tgt.amplitude AS actual_amplitude,
    ABS(v.evolved_amplitude - tgt.amplitude) AS evolution_residual
FROM RelationalEvolutionView v
JOIN WdwGlobalState tgt 
  ON tgt.clock_id = v.next_clock 
 AND tgt.volume_state_id = v.evolved_state_id;

-- 7. Schläfli Identity Check View: sum(hinge_length * d_deficit)
CREATE TABLE IF NOT EXISTS SchlafliVariationLog (
    variation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hinge_edge_id INTEGER NOT NULL,
    hinge_length REAL NOT NULL,
    d_deficit REAL NOT NULL,
    weighted_variation REAL NOT NULL -- hinge_length * d_deficit
);

CREATE VIEW IF NOT EXISTS SchlafliContractionView AS
SELECT 
    COUNT(*) AS total_varied_hinges,
    SUM(weighted_variation) AS schlafli_total_sum,
    ABS(SUM(weighted_variation)) AS schlafli_residual_norm
FROM SchlafliVariationLog;

-- 8. arXiv:1904.01966 Recovery: Discrete Riemann, Bianchi, and Einstein Relvars
CREATE TABLE IF NOT EXISTS DiscreteBoneCurvature (
    joint_p INTEGER PRIMARY KEY,
    rho_p REAL NOT NULL CHECK (rho_p > 0),
    deficit_eps_p REAL NOT NULL,
    u_vector_0 REAL NOT NULL,
    u_vector_1 REAL NOT NULL,
    u_vector_2 REAL NOT NULL,
    length_L_p REAL NOT NULL CHECK (length_L_p > 0),
    ricci_scalar_R REAL NOT NULL -- 2 * rho_p * deficit_eps_p
);

CREATE VIEW IF NOT EXISTS DiscreteSecondBianchiView AS
SELECT 
    COUNT(*) AS total_bones,
    SUM(deficit_eps_p * u_vector_0) AS sum_eps_u0,
    SUM(deficit_eps_p * u_vector_1) AS sum_eps_u1,
    SUM(deficit_eps_p * u_vector_2) AS sum_eps_u2,
    SQRT(
        POW(SUM(deficit_eps_p * u_vector_0), 2) +
        POW(SUM(deficit_eps_p * u_vector_1), 2) +
        POW(SUM(deficit_eps_p * u_vector_2), 2)
    ) AS second_bianchi_closure_norm
FROM DiscreteBoneCurvature;

CREATE TABLE IF NOT EXISTS DiscreteEinsteinResiduals (
    edge_id INTEGER PRIMARY KEY,
    einstein_lhs REAL NOT NULL, -- sum_{p \supset e} eps_p * (dL_p / dl_e)
    matter_stress_rhs REAL NOT NULL DEFAULT 0.0,
    cosmological_term REAL NOT NULL DEFAULT 0.0,
    net_residual REAL NOT NULL -- einstein_lhs - (matter_stress_rhs + cosmological_term)
);

CREATE VIEW IF NOT EXISTS DiscreteEinsteinResidualView AS
SELECT 
    COUNT(*) AS total_equations,
    MAX(ABS(net_residual)) AS max_einstein_residual,
    AVG(ABS(net_residual)) AS avg_einstein_residual
FROM DiscreteEinsteinResiduals;

-- 9. 4D Lorentzian Regge Causal Dynamical Triangulation (CDT) Relvars
CREATE TABLE IF NOT EXISTS CdtFoliationSlice (
    slice_t INTEGER PRIMARY KEY,
    spatial_vertices_count INTEGER NOT NULL CHECK (spatial_vertices_count > 0),
    spatial_edges_count INTEGER NOT NULL CHECK (spatial_edges_count > 0),
    spatial_triangles_count INTEGER NOT NULL CHECK (spatial_triangles_count > 0),
    spatial_euler_char INTEGER NOT NULL -- V - E + F
);

CREATE TABLE IF NOT EXISTS LorentzianEdge (
    edge_id INTEGER PRIMARY KEY,
    u INTEGER NOT NULL,
    v INTEGER NOT NULL,
    time_u INTEGER NOT NULL,
    time_v INTEGER NOT NULL,
    signature TEXT NOT NULL CHECK (signature IN ('spacelike', 'timelike')),
    length_sq REAL NOT NULL, -- positive for spacelike, negative for timelike
    CHECK ((signature = 'spacelike' AND time_u = time_v) OR (signature = 'timelike' AND time_u != time_v))
);

CREATE TABLE IF NOT EXISTS CdtSimplex4D (
    simplex_id INTEGER PRIMARY KEY,
    simplex_type TEXT NOT NULL CHECK (simplex_type IN ('4_1', '3_2', '2_3', '1_4')),
    slice_t_lower INTEGER NOT NULL,
    slice_t_upper INTEGER NOT NULL,
    CHECK (slice_t_upper = slice_t_lower + 1)
);

CREATE TABLE IF NOT EXISTS CdtCausalPachnerLog (
    move_id INTEGER PRIMARY KEY AUTOINCREMENT,
    move_type TEXT NOT NULL CHECK (move_type IN ('causal_2_to_3', 'causal_3_to_2', 'causal_2_to_6', 'acausal_branching')),
    slice_t INTEGER NOT NULL,
    prior_euler_char INTEGER NOT NULL,
    post_euler_char INTEGER NOT NULL,
    has_ctc INTEGER NOT NULL CHECK (has_ctc IN (0, 1)),
    foliation_preserved INTEGER NOT NULL CHECK (foliation_preserved IN (0, 1)),
    bqnf_disposition TEXT NOT NULL CHECK (bqnf_disposition IN ('ExactRepair', 'ClosureFailure', 'IdentityPreserve')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS CdtFoliationAuditView AS
SELECT 
    slice_t,
    COUNT(*) AS moves_on_slice,
    SUM(CASE WHEN bqnf_disposition = 'ExactRepair' THEN 1 ELSE 0 END) AS repaired_causal_moves,
    SUM(CASE WHEN bqnf_disposition = 'ClosureFailure' THEN 1 ELSE 0 END) AS refused_acausal_moves,
    MAX(has_ctc) AS ctc_detected
FROM CdtCausalPachnerLog
GROUP BY slice_t;

-- 10. Wick-Rotated Lorentzian CDT Monte Carlo Statistical Weight Sampler Relvars
CREATE TABLE IF NOT EXISTS CdtMonteCarloTrajectory (
    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
    beta REAL NOT NULL,
    sweep INTEGER NOT NULL,
    move_type TEXT NOT NULL,
    delta_S REAL NOT NULL,
    acceptance_prob REAL NOT NULL,
    accepted INTEGER NOT NULL CHECK (accepted IN (0, 1)),
    action_S REAL NOT NULL,
    einstein_residual_norm REAL NOT NULL,
    foliation_valid INTEGER NOT NULL CHECK (foliation_valid IN (0, 1)),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtQuantumPathObservables (
    obs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    beta REAL NOT NULL UNIQUE,
    sample_count INTEGER NOT NULL,
    mean_action REAL NOT NULL,
    mean_einstein_residual REAL NOT NULL,
    var_einstein_residual REAL NOT NULL,
    max_einstein_residual REAL NOT NULL,
    convergence_ratio REAL NOT NULL
);

CREATE VIEW IF NOT EXISTS ViewCdtSemiclassicalConvergence AS
SELECT 
    beta,
    sample_count,
    mean_action,
    mean_einstein_residual,
    var_einstein_residual,
    max_einstein_residual,
    convergence_ratio,
    CASE 
        WHEN mean_einstein_residual < 0.15 THEN 'CONVERGED_TO_CLASSICAL_EINSTEIN'
        ELSE 'QUANTUM_FLUCTUATION_DOMINATED'
    END AS regime_classification
FROM CdtQuantumPathObservables
ORDER BY beta ASC;

-- 11. CDT Spectral Dimension & Dynamical Dimensional Reduction Relvars
CREATE TABLE IF NOT EXISTS CdtDiffusionTrajectory (
    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tau INTEGER NOT NULL,
    return_prob REAL NOT NULL,
    log_tau REAL NOT NULL,
    log_return_prob REAL NOT NULL,
    spectral_dimension REAL NOT NULL,
    regime TEXT NOT NULL CHECK (regime IN ('PLANCKIAN_2D', 'TRANSITION_REGION', 'MACROSCOPIC_4D', 'FINITE_SIZE_SATURATION')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtSpectralDimensionEnsemble (
    ens_id INTEGER PRIMARY KEY AUTOINCREMENT,
    beta REAL NOT NULL,
    tau INTEGER NOT NULL,
    mean_spectral_dimension REAL NOT NULL,
    std_spectral_dimension REAL NOT NULL,
    sample_count INTEGER NOT NULL
);

CREATE VIEW IF NOT EXISTS ViewCdtSpectralDimensionalReduction AS
SELECT 
    tau,
    return_prob,
    log_tau,
    log_return_prob,
    spectral_dimension,
    regime
FROM CdtDiffusionTrajectory
ORDER BY tau ASC;

-- =========================================================================
-- 12. L1 Constraint Closure, Strong Duality & GR-002 Findings Relvars
-- AuthorityEffect: None.
-- Recreating the findings of GR-002 under relational ANSI SQL & normal forms.
-- =========================================================================

-- Finding 1: Minimal 2-Simplex Triangle Loop & Strong LP Duality (§8.1)
CREATE TABLE IF NOT EXISTS L1PrimalDualQuotients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_name TEXT NOT NULL UNIQUE,
    carrier_dim INTEGER NOT NULL,
    num_cells INTEGER NOT NULL,
    primal_obj REAL NOT NULL,
    dual_obj REAL NOT NULL,
    duality_gap REAL NOT NULL,
    is_closed INTEGER NOT NULL CHECK (is_closed IN (0, 1)),
    dual_witness_norm_inf REAL NOT NULL,
    dual_divergence_norm REAL NOT NULL,
    is_certified INTEGER NOT NULL CHECK (is_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewL1DualityGapCertification AS
SELECT 
    case_name,
    primal_obj,
    dual_obj,
    duality_gap,
    dual_witness_norm_inf,
    dual_divergence_norm,
    is_closed,
    is_certified,
    CASE 
        WHEN duality_gap <= 1e-12 
         AND dual_witness_norm_inf <= 1.0000000001 
         AND dual_divergence_norm <= 1e-10 
         AND is_certified = 1
        THEN 'CERTIFIED_STRONG_DUALITY'
        ELSE 'DUALITY_GAP_VIOLATION'
    END AS status
FROM L1PrimalDualQuotients;

-- Finding 2: 4D 4-Sphere Simplicial Bianchi & Carroll's Holonomy Obstruction (§8.2)
CREATE TABLE IF NOT EXISTS L1BianchiS4Audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_name TEXT NOT NULL UNIQUE,
    num_vertices INTEGER NOT NULL,
    num_edges INTEGER NOT NULL,
    num_triangles INTEGER NOT NULL,
    num_tetrahedra INTEGER NOT NULL,
    num_4simplices INTEGER NOT NULL,
    edge_01_len REAL NOT NULL,
    uniform_other_len REAL NOT NULL,
    regular_dihedral_angle REAL NOT NULL,
    regular_deficit_angle REAL NOT NULL,
    d2_eps_l1_norm REAL NOT NULL,
    d2_eps_linf_norm REAL NOT NULL,
    d2_eps_hinge_0234 REAL NOT NULL,
    is_abelian_closed INTEGER NOT NULL CHECK (is_abelian_closed IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewL1BianchiS4HolonomyObstruction AS
SELECT 
    complex_name,
    edge_01_len,
    d2_eps_l1_norm,
    d2_eps_linf_norm,
    d2_eps_hinge_0234,
    is_abelian_closed,
    CASE 
        WHEN complex_name = 's4_regular_4sphere' AND d2_eps_l1_norm <= 1e-12 THEN 'ABELIAN_BIANCHI_SATISFIED'
        WHEN complex_name = 's4_carroll_perturbed' AND d2_eps_l1_norm > 1.90 AND d2_eps_linf_norm > 0.24 THEN 'NONABELIAN_HOLONOMY_OBSTRUCTION'
        ELSE 'UNEXPECTED_BIANCHI_STATE'
    END AS bianchi_status
FROM L1BianchiS4Audit;

-- Finding 3: S3 WDW Hamiltonian Blind Spot & Joint Resolution (§8.3)
CREATE TABLE IF NOT EXISTS L1JointWdwConstraints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_name TEXT NOT NULL UNIQUE,
    num_vertices INTEGER NOT NULL,
    num_edges INTEGER NOT NULL,
    num_tetrahedra INTEGER NOT NULL,
    edge_deficit REAL NOT NULL,
    scalar_ricci_per_vertex REAL NOT NULL,
    hamiltonian_l1_violation REAL NOT NULL,
    naive_phi_d0 REAL NOT NULL,
    naive_blind_spot_detected INTEGER NOT NULL CHECK (naive_blind_spot_detected IN (0, 1)),
    joint_phi_direct_sum REAL NOT NULL,
    joint_duality_gap REAL NOT NULL,
    is_joint_certified INTEGER NOT NULL CHECK (is_joint_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewL1HamiltonianBlindSpotResolution AS
SELECT 
    complex_name,
    scalar_ricci_per_vertex,
    hamiltonian_l1_violation,
    naive_phi_d0,
    naive_blind_spot_detected,
    joint_phi_direct_sum,
    joint_duality_gap,
    is_joint_certified,
    CASE 
        WHEN naive_blind_spot_detected = 1 
         AND joint_phi_direct_sum > 100.0 
         AND joint_duality_gap <= 1e-10 
         AND is_joint_certified = 1
        THEN 'HAMILTONIAN_BLIND_SPOT_RESOLVED'
        ELSE 'JOINT_RESOLUTION_FAILED'
    END AS resolution_status
FROM L1JointWdwConstraints;

-- Finding 4: Exact Rational LP on Carroll's Regression Case (§8.4)
CREATE TABLE IF NOT EXISTS L1ExactRationalQuotients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_name TEXT NOT NULL UNIQUE,
    omega_numerator TEXT NOT NULL,
    omega_denominator TEXT NOT NULL,
    primal_obj_num INTEGER NOT NULL,
    primal_obj_den INTEGER NOT NULL,
    dual_obj_num INTEGER NOT NULL,
    dual_obj_den INTEGER NOT NULL,
    duality_gap_num INTEGER NOT NULL,
    duality_gap_den INTEGER NOT NULL,
    is_closed INTEGER NOT NULL CHECK (is_closed IN (0, 1)),
    is_certified INTEGER NOT NULL CHECK (is_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Finding 5: Finite Hodge--Dirac Laplacian & Witten Index (§8.5)
CREATE TABLE IF NOT EXISTS L1HodgeDiracSpectrum (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_name TEXT NOT NULL UNIQUE,
    num_vertices INTEGER NOT NULL,
    num_edges INTEGER NOT NULL,
    num_faces INTEGER NOT NULL,
    euler_characteristic INTEGER NOT NULL,
    witten_index INTEGER NOT NULL,
    laplacian_trace REAL NOT NULL,
    is_laplacian_identity_scaled INTEGER NOT NULL CHECK (is_laplacian_identity_scaled IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Finding 6: Fixed-Carrier Quotient Homogeneity vs Double-Well (§8.6)
CREATE TABLE IF NOT EXISTS L1HomogeneityFit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fit_id TEXT NOT NULL UNIQUE,
    num_samples INTEGER NOT NULL,
    r2_linear REAL NOT NULL,
    r2_quartic REAL NOT NULL,
    origin_is_global_minimum INTEGER NOT NULL CHECK (origin_is_global_minimum IN (0, 1)),
    mexican_hat_ssb_ruled_out INTEGER NOT NULL CHECK (mexican_hat_ssb_ruled_out IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Finding 7: Discrete Descent Breakdown on Non-Manifold Fan (§8.7)
CREATE TABLE IF NOT EXISTS L1DescentLedger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_name TEXT NOT NULL UNIQUE,
    move_type TEXT NOT NULL,
    gamma_before REAL NOT NULL,
    gamma_after REAL NOT NULL,
    delta_gamma REAL NOT NULL,
    curl_mass_canceled REAL NOT NULL,
    is_monotonic_descent INTEGER NOT NULL CHECK (is_monotonic_descent IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewL1DescentLossAudit AS
SELECT 
    complex_name,
    move_type,
    gamma_before,
    gamma_after,
    delta_gamma,
    curl_mass_canceled,
    is_monotonic_descent,
    CASE 
        WHEN delta_gamma > 0.0 AND curl_mass_canceled = 0.0 AND is_monotonic_descent = 0
        THEN 'NON_MONOTONIC_LOSS_HONESTLY_RECORDED'
        ELSE 'INVALID_DESCENT_LEDGER'
    END AS audit_status
FROM L1DescentLedger;

-- Finding 8: Ponzano--Regge Semiclassical Bounds (§6.2)
CREATE TABLE IF NOT EXISTS L1PonzanoReggeBounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_name TEXT NOT NULL UNIQUE,
    base_spins TEXT NOT NULL,
    semiclassical_phase REAL NOT NULL,
    shifted_envelope REAL NOT NULL,
    unshifted_envelope REAL NOT NULL,
    schlafli_path_bound REAL NOT NULL,
    satisfies_schlafli_bound INTEGER NOT NULL CHECK (satisfies_schlafli_bound IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Finding 9: High-Energy Quarantines (§7)
CREATE TABLE IF NOT EXISTS L1HighEnergyQuarantine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id TEXT NOT NULL UNIQUE,
    claim_name TEXT NOT NULL,
    verdict TEXT NOT NULL CHECK (verdict = 'QUARANTINED_FALSIFIED'),
    mathematical_proof_of_failure TEXT NOT NULL,
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewL1QuarantineAudit AS
SELECT 
    COUNT(*) AS total_quarantines,
    SUM(CASE WHEN verdict = 'QUARANTINED_FALSIFIED' THEN 1 ELSE 0 END) AS falsified_count,
    CASE 
        WHEN COUNT(*) = 5 AND SUM(CASE WHEN verdict = 'QUARANTINED_FALSIFIED' THEN 1 ELSE 0 END) = 5
        THEN 'ALL_QUARANTINES_FORMALLY_FALSIFIED'
        ELSE 'UNAUDITED_QUARANTINE_PRESENT'
    END AS quarantine_status
FROM L1HighEnergyQuarantine;

-- =========================================================================
-- 13. Dynamical Matter & Compact Lattice Gauge Fields on 4D CDT (CDT-MATTER-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtScalarMatterField (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id TEXT NOT NULL,
    vertex_id INTEGER NOT NULL,
    phi_val REAL NOT NULL,
    potential_energy REAL NOT NULL,
    kinetic_dirichlet_contrib REAL NOT NULL,
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(config_id, vertex_id)
);

CREATE TABLE IF NOT EXISTS CdtGaugeFieldLink (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id TEXT NOT NULL,
    edge_id TEXT NOT NULL,
    u INTEGER NOT NULL,
    v INTEGER NOT NULL,
    theta_link REAL NOT NULL,
    theta_transformed REAL NOT NULL,
    gauge_rot_u REAL NOT NULL,
    gauge_rot_v REAL NOT NULL,
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(config_id, edge_id)
);

CREATE TABLE IF NOT EXISTS CdtCoupledEnsembleTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sweep_id INTEGER NOT NULL,
    beta_geom REAL NOT NULL,
    kappa_scalar REAL NOT NULL,
    beta_gauge REAL NOT NULL,
    s_geom REAL NOT NULL,
    s_scalar REAL NOT NULL,
    s_gauge REAL NOT NULL,
    s_total REAL NOT NULL,
    s_gauge_transformed REAL NOT NULL,
    gauge_invariance_residual REAL NOT NULL,
    ds_planck REAL NOT NULL,
    ds_macro REAL NOT NULL,
    delta_ds REAL NOT NULL,
    is_geometric_collapse INTEGER NOT NULL CHECK (is_geometric_collapse IN (0, 1)),
    is_gauge_invariant INTEGER NOT NULL CHECK (is_gauge_invariant IN (0, 1)),
    is_spectral_dim_preserved INTEGER NOT NULL CHECK (is_spectral_dim_preserved IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtGaugeInvarianceAudit AS
SELECT 
    sweep_id,
    beta_gauge,
    s_gauge,
    s_gauge_transformed,
    gauge_invariance_residual,
    is_gauge_invariant,
    CASE 
        WHEN gauge_invariance_residual <= 1e-12 AND is_gauge_invariant = 1
        THEN 'GAUGE_INVARIANCE_CERTIFIED'
        ELSE 'GAUGE_INVARIANCE_BREACH'
    END AS audit_status
FROM CdtCoupledEnsembleTrajectory;

CREATE VIEW IF NOT EXISTS ViewCdtCoupledSpectralDimensionAudit AS
SELECT 
    sweep_id,
    beta_geom,
    kappa_scalar,
    beta_gauge,
    ds_planck,
    ds_macro,
    delta_ds,
    is_geometric_collapse,
    is_spectral_dim_preserved,
    CASE 
        WHEN is_geometric_collapse = 1
        THEN 'GEOMETRIC_COLLAPSE_DETECTED'
        WHEN ds_planck BETWEEN 1.5 AND 2.5 
         AND ds_macro BETWEEN 3.5 AND 4.5 
         AND delta_ds >= 1.5 
         AND is_spectral_dim_preserved = 1
        THEN 'COUPLED_DIMENSIONAL_REDUCTION_PRESERVED'
        ELSE 'DIVERGENT_SPECTRAL_SCALING'
    END AS spectral_status
FROM CdtCoupledEnsembleTrajectory;

-- =========================================================================
-- 14. 4D Pachner Moves & Joint Direct-Sum LP Scaling Bounds (L1PSNF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS L1PachnerScalingTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    step_id INTEGER NOT NULL,
    move_type TEXT NOT NULL CHECK (move_type IN ('seed', '2_to_4', '3_to_3')),
    num_vertices INTEGER NOT NULL,
    num_edges INTEGER NOT NULL,
    num_triangles INTEGER NOT NULL,
    num_tetrahedra INTEGER NOT NULL,
    num_4simplices INTEGER NOT NULL,
    euler_characteristic INTEGER NOT NULL,
    lp_rows INTEGER NOT NULL,
    lp_cols INTEGER NOT NULL,
    solve_time_ms REAL NOT NULL,
    primal_obj REAL NOT NULL,
    dual_obj REAL NOT NULL,
    duality_gap REAL NOT NULL,
    is_certified INTEGER NOT NULL CHECK (is_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS L1PachnerScalingSummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL UNIQUE,
    min_4simplices INTEGER NOT NULL,
    max_4simplices INTEGER NOT NULL,
    num_steps INTEGER NOT NULL,
    mean_solve_time_ms REAL NOT NULL,
    max_solve_time_ms REAL NOT NULL,
    max_duality_gap REAL NOT NULL,
    empirical_scaling_exponent REAL NOT NULL,
    r2_fit REAL NOT NULL,
    all_certified INTEGER NOT NULL CHECK (all_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewL1PachnerScalingAudit AS
SELECT 
    run_id,
    min_4simplices,
    max_4simplices,
    num_steps,
    mean_solve_time_ms,
    max_solve_time_ms,
    max_duality_gap,
    empirical_scaling_exponent,
    r2_fit,
    all_certified,
    CASE 
        WHEN max_duality_gap <= 1e-9 
         AND all_certified = 1 
         AND empirical_scaling_exponent <= 3.5
        THEN 'SCALING_BOUNDS_CERTIFIED'
        ELSE 'SCALING_BOUNDS_BREACH'
    END AS scaling_audit_status
FROM L1PachnerScalingSummary;

-- =========================================================================
-- 15. Fermionic Grassmann Path Integrals & BQNF Sign Normal Form (CDT-FSIGN-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtFermionicEnsembleTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL,
    config_id TEXT NOT NULL,
    s_geom REAL NOT NULL,
    s_matter REAL NOT NULL,
    s_total REAL NOT NULL,
    boltzmann_weight REAL NOT NULL,
    det_d_real REAL NOT NULL,
    det_d_imag REAL NOT NULL,
    fermion_sign INTEGER NOT NULL CHECK (fermion_sign IN (-1, 1)),
    is_paired INTEGER NOT NULL CHECK (is_paired IN (0, 1)),
    paired_config_id TEXT,
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ensemble_id, config_id)
);

CREATE TABLE IF NOT EXISTS CdtBqnfInvolutionAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL UNIQUE,
    ensemble_type TEXT NOT NULL CHECK (ensemble_type IN ('BIPARTITE_REFLECTION', 'CHIRAL_FRUSTRATED')),
    num_configurations INTEGER NOT NULL,
    num_positive_configs INTEGER NOT NULL,
    num_negative_configs INTEGER NOT NULL,
    has_exact_involution INTEGER NOT NULL CHECK (has_exact_involution IN (0, 1)),
    involution_name TEXT,
    is_involutive INTEGER NOT NULL CHECK (is_involutive IN (0, 1)),
    is_fixed_point_free INTEGER NOT NULL CHECK (is_fixed_point_free IN (0, 1)),
    is_sign_reversing INTEGER NOT NULL CHECK (is_sign_reversing IN (0, 1)),
    is_weight_preserving INTEGER NOT NULL CHECK (is_weight_preserving IN (0, 1)),
    is_involution_certified INTEGER NOT NULL CHECK (is_involution_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtBqnfSignQuotientSummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL UNIQUE,
    z_b REAL NOT NULL,
    z_f REAL NOT NULL,
    average_sign REAL NOT NULL,
    c1_norm1 REAL NOT NULL,
    phi_1_quotient_norm REAL NOT NULL,
    sign_bound_lower REAL NOT NULL,
    bound_satisfied INTEGER NOT NULL CHECK (bound_satisfied IN (0, 1)),
    classification TEXT NOT NULL CHECK (classification IN ('ExactCancellation', 'OpenSignObstruction')),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtFermionSignBqnfAudit AS
SELECT 
    s.ensemble_id,
    a.ensemble_type,
    a.num_configurations,
    a.has_exact_involution,
    a.is_involution_certified,
    s.z_b,
    s.z_f,
    s.average_sign,
    s.phi_1_quotient_norm,
    s.sign_bound_lower,
    s.bound_satisfied,
    s.classification,
    CASE 
        WHEN a.has_exact_involution = 1 AND a.is_involution_certified = 1 AND s.classification = 'ExactCancellation'
        THEN 'EXACT_INVOLUTION_CANCELLED'
        WHEN a.has_exact_involution = 0 AND s.bound_satisfied = 1 AND s.classification = 'OpenSignObstruction'
        THEN 'BOUNDED_OPEN_SIGN_OBSTRUCTION'
        ELSE 'UNAUDITED_SIGN_IRREGULARITY'
    END AS audit_verdict
FROM CdtBqnfSignQuotientSummary s
JOIN CdtBqnfInvolutionAudit a ON s.ensemble_id = a.ensemble_id;

-- =========================================================================
-- 16. Kähler-Dirac Fermion Doubling Resolution & Topological Spin Obstruction (CDT-KD-DOUBLING-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtKahlerDiracBundleTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL,
    geometry_type TEXT NOT NULL CHECK (geometry_type IN ('FLAT_SIMPLEX', 'CURVED_CDT_CLUSTER')),
    num_vertices INTEGER NOT NULL,
    num_edges INTEGER NOT NULL,
    num_triangles INTEGER NOT NULL,
    num_tetrahedra INTEGER NOT NULL,
    num_4simplices INTEGER NOT NULL,
    kd_bundle_dim INTEGER NOT NULL,
    projected_spinor_dim INTEGER NOT NULL,
    species_multiplication_factor INTEGER NOT NULL,
    boundary_sq_residual REAL NOT NULL,
    coboundary_sq_residual REAL NOT NULL,
    projector_idempotence_residual REAL NOT NULL,
    dirac_projector_commutator_residual REAL NOT NULL,
    is_boundary_nilpotent INTEGER NOT NULL CHECK (is_boundary_nilpotent IN (0, 1)),
    is_projector_idempotent INTEGER NOT NULL CHECK (is_projector_idempotent IN (0, 1)),
    is_commutator_vanishing INTEGER NOT NULL CHECK (is_commutator_vanishing IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(complex_id)
);

CREATE TABLE IF NOT EXISTS CdtOrientifoldProjectionAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL UNIQUE,
    orientifold_sq_residual REAL NOT NULL,
    is_involution INTEGER NOT NULL CHECK (is_involution IN (0, 1)),
    self_dual_dim INTEGER NOT NULL,
    anti_self_dual_dim INTEGER NOT NULL,
    trace_chiral_projector REAL NOT NULL,
    trace_spinor_projector REAL NOT NULL,
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtKahlerDiracDoublingSummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL UNIQUE,
    geometry_type TEXT NOT NULL CHECK (geometry_type IN ('FLAT_SIMPLEX', 'CURVED_CDT_CLUSTER')),
    euler_characteristic INTEGER NOT NULL,
    a_hat_genus REAL NOT NULL,
    kd_index INTEGER NOT NULL,
    spinor_index REAL NOT NULL,
    index_mismatch REAL NOT NULL,
    classification TEXT NOT NULL CHECK (classification IN ('MinimalSpinorRecovered', 'KahlerDiracIndexObstruction')),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtKahlerDiracDoublingAudit AS
SELECT 
    t.complex_id,
    t.geometry_type,
    t.kd_bundle_dim,
    t.projected_spinor_dim,
    t.species_multiplication_factor,
    t.boundary_sq_residual,
    t.coboundary_sq_residual,
    t.projector_idempotence_residual,
    t.dirac_projector_commutator_residual,
    s.euler_characteristic,
    s.index_mismatch,
    s.classification,
    CASE 
        WHEN t.boundary_sq_residual <= 1e-12 
         AND t.coboundary_sq_residual <= 1e-12
         AND t.projector_idempotence_residual <= 1e-12
         AND t.dirac_projector_commutator_residual <= 1e-12
         AND s.classification = 'MinimalSpinorRecovered'
        THEN 'EXACT_MINIMAL_SPINOR_RECOVERED'
        WHEN t.boundary_sq_residual <= 1e-12 
         AND t.coboundary_sq_residual <= 1e-12
         AND t.projector_idempotence_residual <= 1e-12
         AND t.dirac_projector_commutator_residual > 1e-6
         AND s.classification = 'KahlerDiracIndexObstruction'
        THEN 'BOUNDED_TOPOLOGICAL_SPIN_OBSTRUCTION'
        ELSE 'UNAUDITED_DOUBLING_ANOMALY'
    END AS doubling_audit_verdict
FROM CdtKahlerDiracBundleTrajectory t
JOIN CdtKahlerDiracDoublingSummary s ON t.complex_id = s.complex_id;

-- =========================================================================
-- 17. Ginsparg-Wilson & Overlap Dirac Operators on 4D CDT (CDT-OVERLAP-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtOverlapDiracTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL,
    geometry_type TEXT NOT NULL CHECK (geometry_type IN ('REGULAR_GAPPED', 'SINGULAR_GAPLESS')),
    num_vertices INTEGER NOT NULL,
    num_edges INTEGER NOT NULL,
    lattice_spacing_a REAL NOT NULL,
    wilson_mass_m0 REAL NOT NULL,
    wilson_r REAL NOT NULL,
    spectral_gap REAL NOT NULL,
    gw_relation_residual REAL NOT NULL,
    luscher_invariance_residual REAL NOT NULL,
    doubler_mass_gap REAL NOT NULL,
    is_gw_satisfied INTEGER NOT NULL CHECK (is_gw_satisfied IN (0, 1)),
    is_chiral_invariant INTEGER NOT NULL CHECK (is_chiral_invariant IN (0, 1)),
    is_doubler_free INTEGER NOT NULL CHECK (is_doubler_free IN (0, 1)),
    is_spectrally_gapped INTEGER NOT NULL CHECK (is_spectrally_gapped IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(complex_id)
);

CREATE TABLE IF NOT EXISTS CdtOverlapIndexAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL UNIQUE,
    num_zero_modes INTEGER NOT NULL,
    n_pos_chirality INTEGER NOT NULL,
    n_neg_chirality INTEGER NOT NULL,
    index_trace REAL NOT NULL,
    topological_charge INTEGER NOT NULL,
    index_residual REAL NOT NULL,
    is_index_certified INTEGER NOT NULL CHECK (is_index_certified IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtOverlapLocalitySummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL UNIQUE,
    geometry_type TEXT NOT NULL CHECK (geometry_type IN ('REGULAR_GAPPED', 'SINGULAR_GAPLESS')),
    min_spectral_gap REAL NOT NULL,
    decay_length_xi REAL NOT NULL,
    max_nonlocal_tail REAL NOT NULL,
    is_exponentially_local INTEGER NOT NULL CHECK (is_exponentially_local IN (0, 1)),
    classification TEXT NOT NULL CHECK (classification IN ('ExactChiralOverlapPreserved', 'GinspargWilsonLocalityObstruction')),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtOverlapDiracAudit AS
SELECT 
    t.complex_id,
    t.geometry_type,
    t.lattice_spacing_a,
    t.spectral_gap,
    t.gw_relation_residual,
    t.luscher_invariance_residual,
    t.doubler_mass_gap,
    i.index_trace,
    i.topological_charge,
    l.decay_length_xi,
    l.is_exponentially_local,
    l.classification,
    CASE 
        WHEN t.gw_relation_residual <= 1e-12
         AND t.luscher_invariance_residual <= 1e-12
         AND t.is_doubler_free = 1
         AND l.is_exponentially_local = 1
         AND l.classification = 'ExactChiralOverlapPreserved'
        THEN 'EXACT_CHIRAL_OVERLAP_CERTIFIED'
        WHEN t.gw_relation_residual <= 1e-12
         AND (t.spectral_gap < 1e-6 OR l.is_exponentially_local = 0)
         AND l.classification = 'GinspargWilsonLocalityObstruction'
        THEN 'LOCALITY_OBSTRUCTION_DETECTED'
        ELSE 'UNAUDITED_OVERLAP_ANOMALY'
    END AS overlap_audit_verdict
FROM CdtOverlapDiracTrajectory t
JOIN CdtOverlapIndexAudit i ON t.complex_id = i.complex_id
JOIN CdtOverlapLocalitySummary l ON t.complex_id = l.complex_id;

-- =========================================================================
-- 18. Rational Zolotarev / Lanczos Bounds for CDT Overlap Fermions (CDT-ZOLOTAREV-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtZolotarevTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL,
    geometry_type TEXT NOT NULL CHECK (geometry_type IN ('REGULAR_GAPPED', 'SINGULAR_GAPLESS', 'DEFLATED_SINGULAR')),
    num_vertices INTEGER NOT NULL,
    spectral_gap REAL NOT NULL,
    cond_number_kappa REAL NOT NULL,
    zolotarev_degree_m INTEGER NOT NULL,
    lanczos_steps_k INTEGER NOT NULL,
    gw_residual REAL NOT NULL,
    dense_solve_time_ms REAL NOT NULL,
    multishift_solve_time_ms REAL NOT NULL,
    speedup_ratio REAL NOT NULL,
    is_gw_within_tolerance INTEGER NOT NULL CHECK (is_gw_within_tolerance IN (0, 1)),
    is_subcubic INTEGER NOT NULL CHECK (is_subcubic IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(complex_id)
);

CREATE TABLE IF NOT EXISTS CdtZolotarevMultiShiftAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL UNIQUE,
    num_shifts INTEGER NOT NULL,
    max_shift_residual REAL NOT NULL,
    cg_iterations INTEGER NOT NULL,
    all_shifts_converged INTEGER NOT NULL CHECK (all_shifts_converged IN (0, 1)),
    deflation_modes_count INTEGER NOT NULL,
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtZolotarevComplexitySummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_id TEXT NOT NULL UNIQUE,
    geometry_type TEXT NOT NULL CHECK (geometry_type IN ('REGULAR_GAPPED', 'SINGULAR_GAPLESS', 'DEFLATED_SINGULAR')),
    empirical_scaling_exponent REAL NOT NULL,
    max_gw_residual REAL NOT NULL,
    classification TEXT NOT NULL CHECK (classification IN ('SubcubicZolotarevCertified', 'ZolotarevSpectralStiffeningObstruction')),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtZolotarevAudit AS
SELECT 
    t.complex_id,
    t.geometry_type,
    t.spectral_gap,
    t.cond_number_kappa,
    t.zolotarev_degree_m,
    t.gw_residual,
    t.multishift_solve_time_ms,
    t.speedup_ratio,
    t.is_gw_within_tolerance,
    t.is_subcubic,
    m.all_shifts_converged,
    m.deflation_modes_count,
    s.classification,
    CASE 
        WHEN t.gw_residual <= 1e-8
         AND t.is_subcubic = 1
         AND m.all_shifts_converged = 1
         AND s.classification = 'SubcubicZolotarevCertified'
        THEN 'SUBCUBIC_ZOLOTAREV_CERTIFIED'
        WHEN (t.cond_number_kappa > 100.0 OR t.gw_residual > 1e-8)
         AND m.deflation_modes_count = 0
         AND s.classification = 'ZolotarevSpectralStiffeningObstruction'
        THEN 'SPECTRAL_STIFFENING_OBSTRUCTION_DETECTED'
        ELSE 'UNAUDITED_ZOLOTAREV_ANOMALY'
    END AS zolotarev_audit_verdict
FROM CdtZolotarevTrajectory t
JOIN CdtZolotarevMultiShiftAudit m ON t.complex_id = m.complex_id
JOIN CdtZolotarevComplexitySummary s ON t.complex_id = s.complex_id;

-- =========================================================================
-- 19. Topological Charge Fluctuations & Instanton Susceptibility on 4D CDT (CDT-TOPO-CHARGE-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtTopologicalChargeTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL,
    config_id TEXT NOT NULL,
    sweep_id INTEGER NOT NULL,
    num_vertices INTEGER NOT NULL,
    four_volume INTEGER NOT NULL,
    n_pos_zero_modes INTEGER NOT NULL,
    n_neg_zero_modes INTEGER NOT NULL,
    topological_charge INTEGER NOT NULL,
    trace_gamma5_rat REAL NOT NULL,
    index_residual REAL NOT NULL,
    is_charge_integer INTEGER NOT NULL CHECK (is_charge_integer IN (0, 1)),
    wdw_defect_norm REAL NOT NULL,
    is_wdw_satisfied INTEGER NOT NULL CHECK (is_wdw_satisfied IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ensemble_id, config_id)
);

CREATE TABLE IF NOT EXISTS CdtInstantonSusceptibilityAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL UNIQUE,
    geometry_regime TEXT NOT NULL CHECK (geometry_regime IN ('SMOOTH_SEMICLASSICAL', 'QUANTUM_FOAM_TEARING')),
    num_configurations INTEGER NOT NULL,
    mean_four_volume REAL NOT NULL,
    mean_q REAL NOT NULL,
    variance_q REAL NOT NULL,
    instanton_susceptibility REAL NOT NULL,
    susceptibility_scaling_exponent REAL NOT NULL,
    tunneling_rate_per_volume REAL NOT NULL,
    is_susceptibility_finite INTEGER NOT NULL CHECK (is_susceptibility_finite IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtTopologicalWdwSummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL UNIQUE,
    geometry_regime TEXT NOT NULL CHECK (geometry_regime IN ('SMOOTH_SEMICLASSICAL', 'QUANTUM_FOAM_TEARING')),
    max_wdw_defect REAL NOT NULL,
    mean_wdw_defect REAL NOT NULL,
    instanton_tunneling_permitted INTEGER NOT NULL CHECK (instanton_tunneling_permitted IN (0, 1)),
    classification TEXT NOT NULL CHECK (classification IN ('TopologicalTunnelingWdwCertified', 'TopologicalSusceptibilityWdwBreachObstruction')),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtTopologicalChargeAudit AS
SELECT 
    t.ensemble_id,
    s.geometry_regime,
    a.num_configurations,
    a.mean_four_volume,
    a.mean_q,
    a.variance_q,
    a.instanton_susceptibility,
    s.max_wdw_defect,
    s.instanton_tunneling_permitted,
    s.classification,
    CASE 
        WHEN s.max_wdw_defect <= 1e-8
         AND s.instanton_tunneling_permitted = 1
         AND s.classification = 'TopologicalTunnelingWdwCertified'
        THEN 'TOPOLOGICAL_TUNNELING_WDW_CERTIFIED'
        WHEN s.max_wdw_defect > 1e-8
         AND s.classification = 'TopologicalSusceptibilityWdwBreachObstruction'
        THEN 'WDW_CONSTRAINT_BREACH_OBSTRUCTION_DETECTED'
        ELSE 'UNAUDITED_TOPOLOGICAL_ANOMALY'
    END AS topological_audit_verdict
FROM CdtTopologicalWdwSummary s
JOIN CdtInstantonSusceptibilityAudit a ON s.ensemble_id = a.ensemble_id
JOIN (
    SELECT ensemble_id, MIN(is_charge_integer) AS all_int, MAX(index_residual) AS max_res
    FROM CdtTopologicalChargeTrajectory GROUP BY ensemble_id
) t ON s.ensemble_id = t.ensemble_id;

-- =========================================================================
-- 20. 4D Supersymmetric CDT, Topological Witten Index & Nicolai Map (CDT-SUSY-WITTEN-NF)
-- AuthorityEffect: None.
-- =========================================================================

CREATE TABLE IF NOT EXISTS CdtSusyWittenTrajectory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL,
    config_id TEXT NOT NULL,
    sweep_id INTEGER NOT NULL,
    num_vertices INTEGER NOT NULL,
    four_volume INTEGER NOT NULL,
    n_boson_zero_modes INTEGER NOT NULL,
    n_fermion_zero_modes INTEGER NOT NULL,
    witten_index INTEGER NOT NULL,
    beta_param REAL NOT NULL,
    susy_ground_energy REAL NOT NULL,
    nicolai_jacobian_residual REAL NOT NULL,
    fermion_determinant REAL NOT NULL,
    fermion_sign INTEGER NOT NULL CHECK (fermion_sign IN (-1, 1)),
    super_wdw_defect_norm REAL NOT NULL,
    is_susy_preserved INTEGER NOT NULL CHECK (is_susy_preserved IN (0, 1)),
    is_super_wdw_satisfied INTEGER NOT NULL CHECK (is_super_wdw_satisfied IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ensemble_id, config_id)
);

CREATE TABLE IF NOT EXISTS CdtSusyCancellationAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL UNIQUE,
    susy_regime TEXT NOT NULL CHECK (susy_regime IN ('EXACT_UNBROKEN_SUSY', 'SPONTANEOUS_BROKEN_SUSY')),
    num_configurations INTEGER NOT NULL,
    mean_witten_index REAL NOT NULL,
    witten_temperature_derivative REAL NOT NULL,
    mean_fermion_sign REAL NOT NULL,
    nicolai_map_isometry_residual REAL NOT NULL,
    is_sign_problem_suppressed INTEGER NOT NULL CHECK (is_sign_problem_suppressed IN (0, 1)),
    is_witten_topological INTEGER NOT NULL CHECK (is_witten_topological IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CdtSuperWdwSummary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ensemble_id TEXT NOT NULL UNIQUE,
    susy_regime TEXT NOT NULL CHECK (susy_regime IN ('EXACT_UNBROKEN_SUSY', 'SPONTANEOUS_BROKEN_SUSY')),
    max_super_wdw_defect REAL NOT NULL,
    mean_super_wdw_defect REAL NOT NULL,
    super_wdw_preserved INTEGER NOT NULL CHECK (super_wdw_preserved IN (0, 1)),
    classification TEXT NOT NULL CHECK (classification IN ('SuperWdwExactCancellationCertified', 'SusyBreakingSignResurgenceObstruction')),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS ViewCdtSusyWittenAudit AS
SELECT 
    t.ensemble_id,
    s.susy_regime,
    a.num_configurations,
    a.mean_witten_index,
    a.witten_temperature_derivative,
    a.mean_fermion_sign,
    a.nicolai_map_isometry_residual,
    s.max_super_wdw_defect,
    s.super_wdw_preserved,
    s.classification,
    CASE 
        WHEN s.max_super_wdw_defect <= 1e-8
         AND a.is_sign_problem_suppressed = 1
         AND a.is_witten_topological = 1
         AND s.classification = 'SuperWdwExactCancellationCertified'
        THEN 'SUPER_WDW_EXACT_CANCELLATION_CERTIFIED'
        WHEN (s.max_super_wdw_defect > 1e-8 OR a.mean_fermion_sign < 1.0)
         AND s.classification = 'SusyBreakingSignResurgenceObstruction'
        THEN 'SUSY_BREAKING_SIGN_RESURGENCE_OBSTRUCTION_DETECTED'
        ELSE 'UNAUDITED_SUSY_ANOMALY'
    END AS susy_audit_verdict
FROM CdtSuperWdwSummary s
JOIN CdtSusyCancellationAudit a ON s.ensemble_id = a.ensemble_id
JOIN (
    SELECT ensemble_id, MIN(is_susy_preserved) AS all_susy, MAX(super_wdw_defect_norm) AS max_def
    FROM CdtSusyWittenTrajectory GROUP BY ensemble_id
) t ON s.ensemble_id = t.ensemble_id;




