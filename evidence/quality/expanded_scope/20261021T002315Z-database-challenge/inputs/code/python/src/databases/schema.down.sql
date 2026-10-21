-- SQLite 3.50.4 tested; rollback for schema.sql version 1.
-- Claim: urn:omega:fqm:sql:empty-ledger-rollback:v1. AuthorityEffect: None.
-- Profile: Non-Numeric. Apply through migrations.apply_migration.
-- Rollback is allowed only before any data are stored. It refuses nonempty
-- ledgers; it does not pretend DROP restores or backs up application data.
BEGIN IMMEDIATE;
CREATE TEMP TABLE _finite_qm_ledger_down_guard (ok INTEGER NOT NULL CHECK (ok = 1));
INSERT INTO _finite_qm_ledger_down_guard
SELECT CASE WHEN
    (SELECT version FROM ledger_schema_version WHERE schema_key = 'finite_qm_ledger') = 1
    AND NOT EXISTS (SELECT 1 FROM genesis_stages)
    AND NOT EXISTS (SELECT 1 FROM ledger_receipts)
    AND NOT EXISTS (SELECT 1 FROM survivor_witnesses)
    AND NOT EXISTS (SELECT 1 FROM simplicial_chains)
THEN 1 ELSE 0 END;
DROP TABLE simplicial_chains;
DROP TABLE survivor_witnesses;
DROP TABLE ledger_receipts;
DROP TABLE genesis_stages;
DROP TABLE ledger_schema_version;
DROP TABLE _finite_qm_ledger_down_guard;
COMMIT;
