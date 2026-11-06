-- Finite numerical fixtures. No physical certification follows from these tables.

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

CREATE TABLE IF NOT EXISTS ReggeDeficitAngles (
    hinge_edge_id INTEGER PRIMARY KEY,
    hinge_length REAL NOT NULL,
    sum_dihedral_angles REAL NOT NULL,
    deficit_angle REAL NOT NULL, -- 2*pi - sum_dihedral_angles
    regge_action_contribution REAL NOT NULL, -- hinge_length * deficit_angle
    FOREIGN KEY (hinge_edge_id) REFERENCES ReggeSimplexEdges(edge_id)
);

CREATE VIEW IF NOT EXISTS ReggeActionTotalView AS
SELECT
    COUNT(*) AS total_hinges,
    SUM(regge_action_contribution) AS total_einstein_regge_action,
    SUM(hinge_length) AS total_hinge_length
FROM ReggeDeficitAngles;

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

CREATE TABLE IF NOT EXISTS HistoryState (
    clock_id INTEGER NOT NULL,
    volume_state_id INTEGER NOT NULL,
    amplitude REAL NOT NULL,
    PRIMARY KEY (clock_id, volume_state_id)
);

CREATE TABLE IF NOT EXISTS HistoryTransferOperator (
    source_state_id INTEGER NOT NULL,
    target_state_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    PRIMARY KEY (source_state_id, target_state_id)
);

CREATE VIEW IF NOT EXISTS RelationalEvolutionView AS
SELECT
    src.clock_id AS current_clock,
    src.clock_id + 1 AS next_clock,
    op.target_state_id AS evolved_state_id,
    SUM(src.amplitude * op.weight) AS evolved_amplitude
FROM HistoryState src
JOIN HistoryTransferOperator op ON src.volume_state_id = op.source_state_id
GROUP BY src.clock_id, op.target_state_id;

CREATE VIEW IF NOT EXISTS HistoryRecurrenceResidualView AS
SELECT
    v.next_clock,
    v.evolved_state_id,
    v.evolved_amplitude,
    tgt.amplitude AS actual_amplitude,
    ABS(v.evolved_amplitude - tgt.amplitude) AS evolution_residual
FROM RelationalEvolutionView v
JOIN HistoryState tgt
  ON tgt.clock_id = v.next_clock
 AND tgt.volume_state_id = v.evolved_state_id;

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

CREATE TABLE IF NOT EXISTS CdtDiffusionTrajectory (
    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tau INTEGER NOT NULL,
    return_prob REAL NOT NULL,
    log_tau REAL NOT NULL,
    log_return_prob REAL NOT NULL,
    spectral_dimension REAL NOT NULL,
    regime TEXT NOT NULL CHECK (regime IN ('LOW_SLOPE', 'MID_SLOPE', 'HIGH_SLOPE', 'FINITE_SIZE_SATURATION')),
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
        WHEN complex_name = 's4_carroll_perturbed' AND d2_eps_l1_norm > 1.90 AND d2_eps_linf_norm > 0.24 THEN 'NONZERO_ABELIAN_BOUNDARY'
        ELSE 'UNEXPECTED_BIANCHI_STATE'
    END AS bianchi_status
FROM L1BianchiS4Audit;

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

CREATE TABLE IF NOT EXISTS L1HomogeneityFit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fit_id TEXT NOT NULL UNIQUE,
    num_samples INTEGER NOT NULL,
    r2_linear REAL NOT NULL,
    r2_quartic REAL NOT NULL,
    origin_is_global_minimum INTEGER NOT NULL CHECK (origin_is_global_minimum IN (0, 1)),
    is_absolute_value_fixture INTEGER NOT NULL CHECK (is_absolute_value_fixture IN (0, 1)),
    authority_effect TEXT NOT NULL DEFAULT 'None',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

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
        THEN 'SAMPLED_SCALING_THRESHOLD_MET'
        ELSE 'SAMPLED_SCALING_THRESHOLD_NOT_MET'
    END AS scaling_audit_status
FROM L1PachnerScalingSummary;
