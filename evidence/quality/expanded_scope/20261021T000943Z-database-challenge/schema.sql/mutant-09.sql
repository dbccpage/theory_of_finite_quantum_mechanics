-- SQLite finite ledger migration, tested with SQLite 3.50.4 (STRICT required).
-- Origin: the sealed prior schema.sql, primitive difference/survivor ledger.
-- Claim: urn:omega:fqm:sql:bounded-survivor-ledger:v2
-- AuthorityEffect: None. Profile: Non-Numeric (bounded integer metadata).
-- Apply through migrations.apply_migration on an idle, exclusively owned
-- connection; it enables/verifies foreign keys and rolls back any failed DDL.
-- This is a fresh-install migration: existing objects cause an atomic refusal.
-- Row caps and field limits are engineering policies, not physical constants.
-- Receipt digests are references. The database does not verify artifact bytes,
-- Stokes' theorem, or the truth of imported observations/verification claims.
BEGIN IMMEDIATE;

CREATE TABLE ledger_schema_version (
    schema_key TEXT PRIMARY KEY CHECK (schema_key = 'finite_qm_ledger'),
    version INTEGER NOT NULL CHECK (version = 1)
) STRICT, WITHOUT ROWID;
INSERT INTO ledger_schema_version VALUES ('finite_qm_ledger', 1);

CREATE TABLE genesis_stages (
    stage_num ANY PRIMARY KEY CHECK (typeof(stage_num) = 'integer' AND stage_num BETWEEN 0 AND 1000000),
    category_name TEXT NOT NULL CHECK (length(trim(category_name)) BETWEEN 1 AND 256 AND instr(category_name, char(0)) = 0),
    carrier_type TEXT NOT NULL CHECK (length(trim(carrier_type)) BETWEEN 1 AND 256 AND instr(carrier_type, char(0)) = 0),
    boundary_formula TEXT CHECK (boundary_formula IS NULL OR (length(boundary_formula) <= 4096 AND instr(boundary_formula, char(0)) = 0)),
    degrees_of_freedom ANY NOT NULL CHECK (typeof(degrees_of_freedom) = 'integer' AND degrees_of_freedom BETWEEN 0 AND 1000000),
    status TEXT NOT NULL CHECK (status IN ('proposed', 'running', 'observed', 'refused'))
) STRICT, WITHOUT ROWID;

CREATE TABLE ledger_receipts (
    sha256 TEXT PRIMARY KEY CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*' AND instr(sha256, char(0)) = 0),
    reference TEXT NOT NULL CHECK (length(trim(reference)) BETWEEN 1 AND 4096 AND instr(reference, char(0)) = 0),
    kind TEXT NOT NULL CHECK (kind IN ('observation', 'kernel_report', 'assertion'))
) STRICT, WITHOUT ROWID;

CREATE TABLE survivor_witnesses (
    witness_id TEXT PRIMARY KEY CHECK (length(witness_id) BETWEEN 1 AND 128 AND witness_id NOT GLOB '*[^A-Za-z0-9_.:-]*' AND instr(witness_id, char(0)) = 0),
    stage_id ANY NOT NULL CHECK (typeof(stage_id) = 'integer') REFERENCES genesis_stages(stage_num) ON DELETE RESTRICT ON UPDATE RESTRICT,
    x_locus TEXT NOT NULL CHECK (length(trim(x_locus)) BETWEEN 1 AND 8192 AND instr(x_locus, char(0)) = 0),
    y_locus TEXT NOT NULL CHECK (length(trim(y_locus)) BETWEEN 1 AND 4096 AND instr(y_locus, char(0)) = 0),
    demand_type TEXT NOT NULL CHECK (length(trim(demand_type)) BETWEEN 1 AND 256 AND instr(demand_type, char(0)) = 0),
    qx_observation TEXT NOT NULL CHECK (length(qx_observation) <= 4096 AND instr(qx_observation, char(0)) = 0),
    qy_observation TEXT NOT NULL CHECK (length(qy_observation) <= 4096 AND instr(qy_observation, char(0)) = 0),
    reason TEXT NOT NULL CHECK (length(trim(reason)) BETWEEN 1 AND 4096 AND instr(reason, char(0)) = 0),
    is_retained ANY NOT NULL DEFAULT 1 CHECK (typeof(is_retained) = 'integer' AND is_retained IN (0, 1)),
    evidence_sha256 TEXT REFERENCES ledger_receipts(sha256) ON DELETE RESTRICT ON UPDATE RESTRICT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        CHECK (length(created_at) = 19 AND strftime('%Y-%m-%d %H:%M:%S', created_at) IS NOT NULL AND created_at = strftime('%Y-%m-%d %H:%M:%S', created_at))
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_survivor_stage ON survivor_witnesses(stage_id);
CREATE INDEX idx_survivor_receipt ON survivor_witnesses(evidence_sha256);

CREATE TABLE simplicial_chains (
    chain_id TEXT PRIMARY KEY CHECK (length(chain_id) BETWEEN 1 AND 128 AND chain_id NOT GLOB '*[^A-Za-z0-9_.:-]*' AND instr(chain_id, char(0)) = 0),
    stage_id ANY NOT NULL CHECK (typeof(stage_id) = 'integer') REFERENCES genesis_stages(stage_num) ON DELETE RESTRICT ON UPDATE RESTRICT,
    dimension ANY NOT NULL CHECK (typeof(dimension) = 'integer' AND dimension BETWEEN 0 AND 64),
    simplex_label TEXT NOT NULL CHECK (length(trim(simplex_label)) BETWEEN 1 AND 4096 AND instr(simplex_label, char(0)) = 0),
    boundary_representation TEXT NOT NULL CHECK (length(boundary_representation) <= 4096 AND instr(boundary_representation, char(0)) = 0),
    -- Legacy name retained: this records an imported assertion, never a proof.
    stokes_verified ANY NOT NULL DEFAULT 0 CHECK (typeof(stokes_verified) = 'integer' AND stokes_verified IN (0, 1)),
    evidence_sha256 TEXT REFERENCES ledger_receipts(sha256) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CHECK (stokes_verified = 0 OR (stokes_verified = 1 AND evidence_sha256 IS NOT NULL))
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_chain_stage ON simplicial_chains(stage_id);
CREATE INDEX idx_chain_receipt ON simplicial_chains(evidence_sha256);

CREATE TRIGGER stage_row_budget BEFORE INSERT ON genesis_stages
WHEN (SELECT COUNT(*) FROM genesis_stages) >= 4096
BEGIN SELECT RAISE(ABORT, 'stage row budget exceeded'); END;
CREATE TRIGGER receipt_row_budget BEFORE INSERT ON ledger_receipts
WHEN (SELECT COUNT(*) FROM ledger_receipts) >= 4096
BEGIN SELECT RAISE(ABORT, 'receipt row budget exceeded'); END;
CREATE TRIGGER witness_row_budget BEFORE INSERT ON survivor_witnesses
WHEN (SELECT COUNT(*) FROM survivor_witnesses) >= 4096
BEGIN SELECT RAISE(ABORT, 'witness row budget exceeded'); END;
CREATE TRIGGER chain_row_budget BEFORE INSERT ON simplicial_chains
WHEN (SELECT COUNT(*) FROM simplicial_chains) >= 4096
BEGIN SELECT RAISE(ABORT, 'chain row budget exceeded'); END;
COMMIT;
