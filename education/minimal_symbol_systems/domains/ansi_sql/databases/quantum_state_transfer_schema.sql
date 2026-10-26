-- ============================================================================
-- ANSI SQL Relational Schema: Categorical Quantum State Transfer Cochains
-- AuthorityEffect: None
--
-- Relational auditing of Quantum Teleportation, Entanglement Distillation,
-- Bell and GHZ Entanglement Witness inequalities, and BQNF terminal routing.
-- ============================================================================

-- 1. Quantum Network Topology
CREATE TABLE IF NOT EXISTS QuantumNodes (
    node_id TEXT PRIMARY KEY,
    node_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('SENDER', 'RECEIVER', 'EPR_SOURCE', 'ANCILLA'))
);

CREATE TABLE IF NOT EXISTS QuantumChannels (
    channel_id TEXT PRIMARY KEY,
    source_node TEXT NOT NULL REFERENCES QuantumNodes(node_id),
    target_node TEXT NOT NULL REFERENCES QuantumNodes(node_id),
    channel_type TEXT NOT NULL CHECK (channel_type IN ('BELL_EPR', 'GHZ_TRIPARTITE', 'CLASSICAL_FEEDFORWARD'))
);

-- 2. Quantum States and Density Matrices
CREATE TABLE IF NOT EXISTS DensityMatrices (
    state_id TEXT PRIMARY KEY,
    state_name TEXT NOT NULL,
    num_qubits INT NOT NULL,
    dim INT NOT NULL,
    is_pure INT NOT NULL CHECK (is_pure IN (0, 1))
);

CREATE TABLE IF NOT EXISTS DensityMatrixEntries (
    state_id TEXT NOT NULL REFERENCES DensityMatrices(state_id),
    row_idx INT NOT NULL,
    col_idx INT NOT NULL,
    val_re REAL NOT NULL,
    val_im REAL NOT NULL,
    PRIMARY KEY (state_id, row_idx, col_idx)
);

-- 3. Entanglement Witness Operators
-- Hermitian witness W such that Tr(W ρ_sep) >= separable_bound, but Tr(W ρ_ent) < separable_bound.
CREATE TABLE IF NOT EXISTS WitnessOperators (
    witness_id TEXT PRIMARY KEY,
    target_state TEXT NOT NULL,
    dim INT NOT NULL,
    separable_bound REAL NOT NULL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS WitnessEntries (
    witness_id TEXT NOT NULL REFERENCES WitnessOperators(witness_id),
    row_idx INT NOT NULL,
    col_idx INT NOT NULL,
    val_re REAL NOT NULL,
    val_im REAL NOT NULL,
    PRIMARY KEY (witness_id, row_idx, col_idx)
);

-- 4. Quantum Teleportation Protocol Execution Log
CREATE TABLE IF NOT EXISTS TeleportationRuns (
    run_id INT PRIMARY KEY,
    input_state TEXT NOT NULL,
    m1 INT NOT NULL CHECK (m1 IN (0, 1)),
    m2 INT NOT NULL CHECK (m2 IN (0, 1)),
    applied_correction TEXT NOT NULL CHECK (applied_correction IN ('Id', 'Z', 'X', 'XZ')),
    output_fidelity REAL NOT NULL,
    is_valid_protocol INT NOT NULL CHECK (is_valid_protocol IN (0, 1))
);

-- 5. Entanglement Distillation Purification Log
CREATE TABLE IF NOT EXISTS DistillationRuns (
    distillation_id INT PRIMARY KEY,
    pair_label TEXT NOT NULL,
    round_num INT NOT NULL,
    input_fidelity REAL NOT NULL,
    output_fidelity REAL NOT NULL,
    is_coincident INT NOT NULL CHECK (is_coincident IN (0, 1))
);

-- ============================================================================
-- AUDITING COMMON TABLE EXPRESSIONS (CTEs) & VIEWS
-- ============================================================================

-- View 1: Entanglement Witness Audit
-- Computes Tr(W ρ) = ∑_{r, c} (W_{r, c} * ρ_{c, r})
-- Real part of Tr(W ρ) = ∑ (W_re * ρ_re - W_im * ρ_im)
CREATE VIEW IF NOT EXISTS ViewEntanglementWitnessAudit AS
WITH MatrixProductTrace AS (
    SELECT 
        w.witness_id,
        w.target_state,
        w.separable_bound,
        rho.state_id,
        rho.state_name,
        SUM(w_ent.val_re * rho_ent.val_re - w_ent.val_im * rho_ent.val_im) AS computed_trace_val
    FROM WitnessOperators w
    JOIN WitnessEntries w_ent ON w.witness_id = w_ent.witness_id
    JOIN DensityMatrices rho ON w.dim = rho.dim
    JOIN DensityMatrixEntries rho_ent 
      ON rho.state_id = rho_ent.state_id 
     AND w_ent.col_idx = rho_ent.row_idx 
     AND w_ent.row_idx = rho_ent.col_idx
    GROUP BY w.witness_id, w.target_state, w.separable_bound, rho.state_id, rho.state_name
)
SELECT 
    witness_id,
    target_state,
    state_id,
    state_name,
    separable_bound,
    computed_trace_val,
    CASE 
        WHEN computed_trace_val < separable_bound THEN 1 
        ELSE 0 
    END AS is_entangled,
    CASE 
        WHEN computed_trace_val < separable_bound THEN 'ENTANGLED_CERTIFIED'
        ELSE 'SEPARABLE_DEFECT'
    END AS witness_status
FROM MatrixProductTrace;

-- View 2: Teleportation Fidelity & Feedforward Audit
-- Audits Bell measurement decoding and output state fidelity:
-- (0, 0) -> Id
-- (1, 0) -> Z
-- (0, 1) -> X
-- (1, 1) -> XZ
CREATE VIEW IF NOT EXISTS ViewTeleportationFidelityAudit AS
SELECT 
    run_id,
    input_state,
    m1,
    m2,
    applied_correction,
    CASE 
        WHEN m1 = 0 AND m2 = 0 THEN 'Id'
        WHEN m1 = 1 AND m2 = 0 THEN 'Z'
        WHEN m1 = 0 AND m2 = 1 THEN 'X'
        WHEN m1 = 1 AND m2 = 1 THEN 'XZ'
    END AS expected_correction,
    output_fidelity,
    is_valid_protocol,
    CASE 
        WHEN is_valid_protocol = 0 THEN 'ClosureFailure'
        WHEN applied_correction = (
            CASE 
                WHEN m1 = 0 AND m2 = 0 THEN 'Id'
                WHEN m1 = 1 AND m2 = 0 THEN 'Z'
                WHEN m1 = 0 AND m2 = 1 THEN 'X'
                WHEN m1 = 1 AND m2 = 1 THEN 'XZ'
            END
        ) AND output_fidelity >= 0.95 THEN 'Repair'
        ELSE 'SplitBrainRefusal'
    END AS terminal_route,
    CASE 
        WHEN is_valid_protocol = 0 THEN 'PROTOCOL_SYNTAX_DEFECT'
        WHEN applied_correction = (
            CASE 
                WHEN m1 = 0 AND m2 = 0 THEN 'Id'
                WHEN m1 = 1 AND m2 = 0 THEN 'Z'
                WHEN m1 = 0 AND m2 = 1 THEN 'X'
                WHEN m1 = 1 AND m2 = 1 THEN 'XZ'
            END
        ) AND output_fidelity >= 0.95 THEN 'TELEPORTATION_CERTIFIED'
        ELSE 'FEEDFORWARD_FIDELITY_DEFECT'
    END AS audit_status
FROM TeleportationRuns;

-- View 3: Entanglement Distillation Efficiency Audit
CREATE VIEW IF NOT EXISTS ViewDistillationEfficiencyAudit AS
SELECT 
    distillation_id,
    pair_label,
    round_num,
    input_fidelity,
    output_fidelity,
    is_coincident,
    (output_fidelity - input_fidelity) AS fidelity_gain,
    CASE 
        WHEN is_coincident = 1 AND output_fidelity > input_fidelity AND input_fidelity > 0.5 THEN 'DISTILLATION_PURIFIED'
        WHEN is_coincident = 0 THEN 'COINCIDENCE_DISCARDED'
        ELSE 'PURIFICATION_DEFECT'
    END AS distillation_status
FROM DistillationRuns;

-- View 4: Aggregate Quantum State Transfer Routing Audit
CREATE VIEW IF NOT EXISTS ViewStateTransferRoutingAudit AS
SELECT 
    'Teleportation' AS protocol_type,
    run_id AS protocol_id,
    terminal_route,
    audit_status AS status_detail
FROM ViewTeleportationFidelityAudit;
