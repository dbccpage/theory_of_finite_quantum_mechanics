-- ============================================================================
-- ANSI SQL Relational Schema: Mock GIN Index for the Fermion Sign Problem (FSP)
-- and Majorana Zero Mode (MZM) Boundary Cochains
-- AuthorityEffect: None
-- ============================================================================

-- 1. Fermionic Many-Body Configurations
CREATE TABLE IF NOT EXISTS FermionConfigurations (
    cfg_id INT PRIMARY KEY,
    model_name TEXT NOT NULL,
    num_particles INT NOT NULL,
    total_modes INT NOT NULL,
    weight REAL NOT NULL,
    jw_sign INT NOT NULL CHECK (jw_sign IN (-1, 1)),
    parity_sector INT NOT NULL CHECK (parity_sector IN (-1, 1))
);

-- 2. Generalized Inverted Index (GIN) Mode Posting List
-- Inverted index mapping each orbital/mode_id to the list of configurations containing it.
CREATE TABLE IF NOT EXISTS GinModePostingList (
    mode_id INT NOT NULL,
    cfg_id INT NOT NULL REFERENCES FermionConfigurations(cfg_id),
    is_occupied INT NOT NULL CHECK (is_occupied IN (0, 1)),
    PRIMARY KEY (mode_id, cfg_id)
);

CREATE INDEX IF NOT EXISTS idx_gin_mode ON GinModePostingList(mode_id, cfg_id);

-- 3. Majorana Zero Mode & Bulk Bond Index
CREATE TABLE IF NOT EXISTS GinMajoranaBonds (
    bond_id INT PRIMARY KEY,
    cfg_id INT NOT NULL REFERENCES FermionConfigurations(cfg_id),
    u INT NOT NULL,
    v INT NOT NULL,
    is_bulk_bond INT NOT NULL CHECK (is_bulk_bond IN (0, 1))
);

-- 4. Inverted Involution Pairs (Meron / Kramers Pairings)
CREATE TABLE IF NOT EXISTS GinInvolutionPairs (
    pair_id INT PRIMARY KEY,
    cfg_pos_id INT NOT NULL REFERENCES FermionConfigurations(cfg_id),
    cfg_neg_id INT NOT NULL REFERENCES FermionConfigurations(cfg_id),
    involution_type TEXT NOT NULL,
    is_exact_partner INT NOT NULL CHECK (is_exact_partner IN (0, 1))
);

-- ============================================================================
-- AUDITING CTE VIEWS
-- ============================================================================

-- View 1: GIN Inverted Index Mode Coverage & Posting Audit
CREATE VIEW IF NOT EXISTS ViewGinModePostingAudit AS
SELECT 
    mode_id,
    COUNT(*) AS total_postings,
    SUM(is_occupied) AS occupied_postings,
    COUNT(*) - SUM(is_occupied) AS empty_postings
FROM GinModePostingList
GROUP BY mode_id;

-- View 2: FSP Involution Sign Cancellation Audit
-- Evaluates that paired states have opposite signs (s_+ + s_- = 0) and identical weights (|W_+ - W_-| < 1e-12)
CREATE VIEW IF NOT EXISTS ViewFspInvolutionSignCancellationAudit AS
SELECT 
    p.pair_id,
    p.involution_type,
    p.cfg_pos_id,
    p.cfg_neg_id,
    cp.weight AS pos_weight,
    cn.weight AS neg_weight,
    cp.jw_sign AS pos_sign,
    cn.jw_sign AS neg_sign,
    (cp.jw_sign + cn.jw_sign) AS net_sign_sum,
    ABS(cp.weight - cn.weight) AS weight_defect,
    CASE 
        WHEN cp.jw_sign = 1 AND cn.jw_sign = -1 AND ABS(cp.weight - cn.weight) < 1e-12 THEN 'EXACT_CANCELLATION'
        ELSE 'SIGN_DEFECT'
    END AS cancellation_status
FROM GinInvolutionPairs p
JOIN FermionConfigurations cp ON p.cfg_pos_id = cp.cfg_id
JOIN FermionConfigurations cn ON p.cfg_neg_id = cn.cfg_id;

-- View 3: Majorana Zero Mode (MZM) Boundary Isolation Audit
-- Audits that edge modes (1 and 2L) are strictly unpaired by bulk bonds
CREATE VIEW IF NOT EXISTS ViewMajoranaZeroModeAudit AS
WITH AllMajoranaModes AS (
    SELECT DISTINCT u AS mode_idx FROM GinMajoranaBonds
    UNION
    SELECT DISTINCT v AS mode_idx FROM GinMajoranaBonds
),
BulkConnectedModes AS (
    SELECT DISTINCT u AS mode_idx FROM GinMajoranaBonds WHERE is_bulk_bond = 1
    UNION
    SELECT DISTINCT v AS mode_idx FROM GinMajoranaBonds WHERE is_bulk_bond = 1
)
SELECT 
    a.mode_idx,
    CASE WHEN b.mode_idx IS NULL THEN 1 ELSE 0 END AS is_unpaired_zero_mode,
    CASE WHEN b.mode_idx IS NULL THEN 'MZM_EDGE_ISOLATED' ELSE 'BULK_BONDED' END AS mode_status
FROM AllMajoranaModes a
LEFT JOIN BulkConnectedModes b ON a.mode_idx = b.mode_idx;

-- View 4: Average Sign Recovery Audit
-- Computes raw average sign vs GIN-paired quotiented sign
CREATE VIEW IF NOT EXISTS ViewAverageSignRecoveryAudit AS
WITH RawAverages AS (
    SELECT 
        model_name,
        COUNT(*) AS total_cfgs,
        SUM(weight * jw_sign) AS signed_partition_sum,
        SUM(weight) AS bosonic_partition_sum,
        SUM(CASE WHEN jw_sign = -1 THEN weight ELSE 0.0 END) AS total_neg_weight,
        CASE 
            WHEN SUM(weight) > 0 THEN SUM(weight * jw_sign) / SUM(weight) 
            ELSE 0.0 
        END AS raw_average_sign
    FROM FermionConfigurations
    GROUP BY model_name
),
PairedStats AS (
    SELECT 
        cp.model_name,
        COUNT(p.pair_id) AS total_pairs,
        SUM(cn.weight) AS paired_neg_weight,
        SUM(ABS(cp.weight - cn.weight)) AS pair_weight_defects,
        SUM(CASE WHEN p.is_exact_partner = 1 AND ABS(cp.weight - cn.weight) < 1e-12 THEN 1 ELSE 0 END) AS exact_pairs_count
    FROM GinInvolutionPairs p
    JOIN FermionConfigurations cp ON p.cfg_pos_id = cp.cfg_id
    JOIN FermionConfigurations cn ON p.cfg_neg_id = cn.cfg_id
    WHERE cp.model_name = cn.model_name
    GROUP BY cp.model_name
)
SELECT 
    r.model_name,
    r.signed_partition_sum,
    r.bosonic_partition_sum,
    r.raw_average_sign,
    (
        MAX(0.0, r.total_neg_weight - COALESCE(ps.paired_neg_weight, 0.0)) + 
        COALESCE(ps.pair_weight_defects, 0.0)
    ) AS uncancelled_sign_mass,
    CASE 
        WHEN r.total_cfgs = 0 OR r.bosonic_partition_sum <= 0 THEN 0.0
        WHEN (MAX(0.0, r.total_neg_weight - COALESCE(ps.paired_neg_weight, 0.0)) + COALESCE(ps.pair_weight_defects, 0.0)) < 1e-12 
             AND (r.total_neg_weight = 0.0 OR (COALESCE(ps.total_pairs, 0) > 0 AND COALESCE(ps.exact_pairs_count, 0) = COALESCE(ps.total_pairs, 0)))
        THEN 1.0
        ELSE r.raw_average_sign
    END AS gin_quotiented_average_sign,
    CASE 
        WHEN r.total_cfgs = 0 OR r.bosonic_partition_sum <= 0 THEN 'EmptyEnsembleRefusal'
        WHEN (MAX(0.0, r.total_neg_weight - COALESCE(ps.paired_neg_weight, 0.0)) + COALESCE(ps.pair_weight_defects, 0.0)) < 1e-12 
             AND (r.total_neg_weight = 0.0 OR (COALESCE(ps.total_pairs, 0) > 0 AND COALESCE(ps.exact_pairs_count, 0) = COALESCE(ps.total_pairs, 0)))
        THEN 'Repair'
        ELSE 'SplitBrainRefusal'
    END AS terminal_route
FROM RawAverages r
LEFT JOIN PairedStats ps ON r.model_name = ps.model_name;
