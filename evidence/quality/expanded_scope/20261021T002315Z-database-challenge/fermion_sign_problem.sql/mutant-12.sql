-- Exact finite signed-ensemble relational audit. SQLite 3.50.4 tested, STRICT.
-- Origin: sealed prior fermion_sign_problem.sql CTE/window examples.
-- Claim: urn:omega:fqm:sql:bounded-exact-signed-ensembles:v2
-- AuthorityEffect: None. Profile: Exact.
-- Apply through migrations.apply_migration with verified foreign keys enabled.
-- Each ensemble declares a common positive denominator. A row's amplitude is
-- sign*magnitude/common_denominator; input magnitudes are nonnegative integers.
-- Ratios are returned as numerator/denominator pairs, NEVER SQLite division.
-- STRICT ANY + typeof guards refuse REAL/TEXT coercion at integer cells.
-- SQLite sees SQL values, not the original Python adapter object's provenance.
-- 4096 rows * magnitude<=1000000 bounds every sum by 4096000000 (<2^63).
-- Complete zero mass has no normalized sign: NULL ratio and explicit status.
-- No orbit involution, observable preservation, sign repair, polynomial model
-- solution or physical ensemble completeness is inferred from these sums.
BEGIN IMMEDIATE;
CREATE TABLE signed_schema_version (
    schema_key TEXT PRIMARY KEY CHECK (schema_key = 'finite_qm_signed_ensemble'),
    version INTEGER NOT NULL CHECK (version = 1)
) STRICT, WITHOUT ROWID;
INSERT INTO signed_schema_version VALUES ('finite_qm_signed_ensemble', 1);

CREATE TABLE signed_ensembles (
    ensemble_id TEXT PRIMARY KEY CHECK (length(ensemble_id) BETWEEN 1 AND 128 AND ensemble_id NOT GLOB '*[^A-Za-z0-9_.:-]*' AND instr(ensemble_id, char(0)) = 0),
    common_denominator ANY NOT NULL CHECK (typeof(common_denominator) = 'integer' AND common_denominator BETWEEN 1 AND 1000000000)
) STRICT, WITHOUT ROWID;

CREATE TABLE signed_configurations (
    ensemble_id TEXT NOT NULL REFERENCES signed_ensembles(ensemble_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    path_id ANY NOT NULL CHECK (typeof(path_id) = 'integer' AND path_id BETWEEN 0 AND 1000000000),
    orbit_id TEXT NOT NULL CHECK (length(orbit_id) BETWEEN 1 AND 128 AND orbit_id NOT GLOB '*[^A-Za-z0-9_.:-]*' AND instr(orbit_id, char(0)) = 0),
    magnitude ANY NOT NULL CHECK (typeof(magnitude) = 'integer' AND magnitude BETWEEN 0 AND 1000000),
    sign ANY NOT NULL CHECK (typeof(sign) = 'integer' AND sign IN (-1, 1)),
    PRIMARY KEY (ensemble_id, path_id)
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_signed_orbit ON signed_configurations(ensemble_id, orbit_id);

CREATE TRIGGER signed_ensemble_row_budget BEFORE INSERT ON signed_ensembles
WHEN (SELECT COUNT(*) FROM signed_ensembles) >= 128
BEGIN SELECT RAISE(ABORT, 'ensemble row budget exceeded'); END;
CREATE TRIGGER signed_configuration_row_budget BEFORE INSERT ON signed_configurations
WHEN (SELECT COUNT(*) FROM signed_configurations) >= 4096
BEGIN SELECT RAISE(ABORT, 'configuration row budget exceeded'); END;
CREATE TRIGGER signed_denominator_frozen BEFORE UPDATE OF common_denominator ON signed_ensembles
WHEN NEW.common_denominator != OLD.common_denominator
 AND EXISTS (SELECT 1 FROM signed_configurations WHERE ensemble_id = OLD.ensemble_id)
BEGIN SELECT RAISE(ABORT, 'populated ensemble denominator is frozen'); END;

CREATE VIEW SignedEnsembleAudit AS
WITH totals AS (
    SELECT e.ensemble_id, e.common_denominator,
           COUNT(c.path_id) AS path_count,
           COALESCE(SUM(c.magnitude * c.sign), 0) AS signed_numerator,
           COALESCE(SUM(c.magnitude), 0) AS unsigned_numerator
    FROM signed_ensembles e
    LEFT JOIN signed_configurations c ON c.ensemble_id = e.ensemble_id
    GROUP BY e.ensemble_id, e.common_denominator
)
SELECT *,
       CASE WHEN unsigned_numerator > 0 THEN signed_numerator ELSE NULL END AS average_sign_num,
       CASE WHEN unsigned_numerator > 0 THEN unsigned_numerator ELSE NULL END AS average_sign_den,
       CASE WHEN path_count = 0 THEN 'EMPTY_ENSEMBLE'
            WHEN unsigned_numerator = 0 THEN 'ZERO_UNSIGNED_MASS'
            ELSE 'FINITE_SUM' END AS audit_status
FROM totals;

-- No ORDER BY: these are whole partitions, not order-dependent running sums.
CREATE VIEW SignedPathWindowAudit AS
SELECT c.ensemble_id, e.common_denominator, c.path_id, c.orbit_id,
       c.magnitude, c.sign,
       COUNT(*) OVER (PARTITION BY c.ensemble_id, c.orbit_id) AS orbit_path_count,
       SUM(c.magnitude) OVER (PARTITION BY c.ensemble_id, c.orbit_id) AS orbit_unsigned_numerator,
       SUM(c.magnitude * c.sign) OVER (PARTITION BY c.ensemble_id, c.orbit_id) AS orbit_signed_numerator
FROM signed_configurations c JOIN signed_ensembles e ON e.ensemble_id = c.ensemble_id;

CREATE VIEW SignedOrbitAudit AS
SELECT DISTINCT ensemble_id, orbit_id, common_denominator, orbit_path_count,
       orbit_unsigned_numerator, orbit_signed_numerator,
       CASE WHEN orbit_unsigned_numerator > 0 THEN orbit_signed_numerator ELSE NULL END AS average_sign_num,
       CASE WHEN orbit_unsigned_numerator > 0 THEN orbit_unsigned_numerator ELSE NULL END AS average_sign_den,
       CASE WHEN orbit_unsigned_numerator = 0 THEN 'ZERO_UNSIGNED_MASS'
            ELSE 'FINITE_ORBIT_SUM' END AS audit_status
FROM SignedPathWindowAudit WHERE orbit_signed_numerator > 0;
COMMIT;
