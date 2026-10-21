-- SQLite 3.50.4 tested; empty-only rollback for the exact signed-ensemble schema.
-- Claim: urn:omega:fqm:sql:empty-signed-ensemble-rollback:v1
-- AuthorityEffect: None. Profile: Non-Numeric. Use migrations.apply_migration.
-- Refuses even empty named ensembles, and any stored configuration; no data loss.
BEGIN IMMEDIATE;
CREATE TEMP TABLE _finite_qm_signed_down_guard (ok INTEGER NOT NULL CHECK (ok = 1));
INSERT INTO _finite_qm_signed_down_guard
SELECT CASE WHEN
    (SELECT version FROM signed_schema_version WHERE schema_key = 'finite_qm_signed_ensemble') = 1
    AND NOT EXISTS (SELECT 1 FROM signed_ensembles)
    AND NOT EXISTS (SELECT 1 FROM signed_configurations)
THEN 1 ELSE 0 END;
-- omitted orbit view drop
DROP VIEW SignedPathWindowAudit;
DROP VIEW SignedEnsembleAudit;
DROP TABLE signed_configurations;
DROP TABLE signed_ensembles;
DROP TABLE signed_schema_version;
DROP TABLE _finite_qm_signed_down_guard;
COMMIT;
