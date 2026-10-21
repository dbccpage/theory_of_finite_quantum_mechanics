# Finite database contracts and research schemas

AuthorityEffect: None. Claim: `urn:omega:fqm:sql:database-contract-guide:v2`.

This directory contains two bounded SQLite migration pairs and several separate
research schemas. A schema or view name does not establish the physical claim
named by it. Imported observations, receipt references and flags remain data.

The original directory reported a copy from `the_symbol_game` commit `e7596da`,
`research/relational_foundations/sql_fermion_sign/`. The exact pre-repair bytes
and executable counterexamples are retained in the
[initial database audit](../../../../evidence/quality/expanded_scope/20261020T235700Z-databases-before/receipt.json).
The current ledger/signed-sum implementations are local repairs of those files;
that reported historical origin is not a cross-repository attestation.

## Bounded SQLite migrations

The execution target is SQLite with STRICT tables, tested on SQLite 3.50.4.
These scripts are not ANSI/PostgreSQL portability claims.

| Name | Install | Empty-only rollback | Contract |
|---|---|---|---|
| `ledger` | [schema.sql](schema.sql) | [schema.down.sql](schema.down.sql) | Stages, survivor records, chain assertions and receipt references |
| `signed_ensemble` | [fermion_sign_problem.sql](fermion_sign_problem.sql) | [fermion_sign_problem.down.sql](fermion_sign_problem.down.sql) | Exact finite signed sums and whole-orbit partitions |

Use [migrations.apply_migration](migrations.py) on an idle, exclusively owned
built-in `sqlite3.Connection`. The function never closes the caller's connection.
It enables and verifies foreign keys and sets a 1000-ms SQLite busy timeout.
The caller must keep normal constraint enforcement enabled and not share that
connection during migration. There is no arbitrary callback/hostile interpreter,
filesystem-stall or hard real-time guarantee.

```python
import sqlite3
from src.databases.migrations import apply_migration

connection = sqlite3.connect(":memory:")
try:
    observation = apply_migration(connection, "signed_ensemble")
    connection.execute("INSERT INTO signed_ensembles VALUES (?, ?)", ("run", 10))
    connection.executemany(
        "INSERT INTO signed_configurations VALUES (?, ?, ?, ?, ?)",
        [("run", 0, "orbit", 3, 1), ("run", 1, "orbit", 1, -1)],
    )
    row = connection.execute("SELECT * FROM SignedEnsembleAudit").fetchone()
finally:
    connection.close()
```

The observation records the SHA-256 of the script bytes executed at that call.
It is immutable metadata, not a certificate of the truth of rows, future files
or the whole database. Script reads are capped at 65536 bytes. Expected failures
raise `MigrationError`; an SQLite refusal carries its error name. Unexpected
interrupts/errors propagate after owned-transaction cleanup. A rollback failure
explicitly reports that the connection state is unverified.

Install fails if schema objects already exist, instead of silently accepting an
unknown old definition. Any failed migration rolls back its own DDL. Admission
refuses an existing caller transaction without rolling that transaction back.
Rollback refuses **any stored application rows**, including named empty stages
or ensembles. It is a tested pre-data rollback, not a backup or a migration that
can restore writes made after installation.

## Exact signed sums

An ensemble declares one positive common denominator, at most 1000000000. Each
configuration has a sign in `{-1,1}` and integer magnitude in `[0,1000000]`.
At most 4096 configuration rows exist in the database, so each signed/unsigned
sum has magnitude at most 4096000000. Products and sums stay within signed
64-bit SQLite integers; no floating-point conversion or division is used.

`SignedEnsembleAudit` reports the two partition numerators, common denominator,
row count and an average-sign numerator/denominator pair. In the example, the
signed sum is `2/10`, absolute sum `4/10` and average sign `2/4 = 1/2`.
The integer pair need not be reduced. Empty ensembles report `EMPTY_ENSEMBLE`;
nonempty all-zero rows report `ZERO_UNSIGNED_MASS`. Both have NULL average-sign
components because the normalization is undefined.

`SignedPathWindowAudit` partitions by **both ensemble and orbit**, without an
ORDER BY running frame. `SignedOrbitAudit` returns the distinct whole-orbit
totals and the same explicit zero-mass handling. Equal orbit labels in different
ensembles never mix. Once a configuration is present, changing its ensemble's
common denominator refuses rather than silently reinterpreting stored weights.

The sums audit supplied finite records. They do not prove that the records form
a complete physical ensemble or a symmetry orbit. They do not supply an
observable-preserving involution or a sign-problem solution. In particular a
balanced signed ensemble has average sign 0; deleting cancelling pairs cannot
manufacture a normalized average sign of 1 from zero remaining mass.

## Ledger boundaries

Ledger tables have explicit key, type, range, text/NUL, parent-reference and
4096-row limits. Stage numbers and recorded degrees of freedom are bounded by
1000000, chain dimensions by 64, text fields by their declared 128/256/4096
character caps. These are engineering policies, not mathematical theorems or
physical constants. Identifiers use the declared ASCII character set; descriptive
text permits Unicode under a character cap.

`stokes_verified` retains its legacy column name but defaults to 0. A value of 1
requires a registered receipt reference and records an **imported assertion**.
The database neither hashes the referenced artifact nor checks Lean or Stokes'
theorem. Likewise `is_retained` records ledger retention, not scientific validity.

Primary/foreign keys have indexes. Explicit stage/orbit/receipt indexes support
the corresponding lookups. Row-budget triggers count existing bounded tables;
they have bounded polynomial cost rather than an unmeasured universal O(log N)
insertion guarantee. Query plans and actual database behavior belong in evidence.

## Other research schemas remain under review

| File | Current review boundary |
|---|---|
| [fermion_gin_index_schema.sql](fermion_gin_index_schema.sql) | The initial audit reproduces tolerance-to-exact labeling and a manufactured quotient sign. Its existing consumers and legacy display views need a separate repair; no complete L4 grade is implied. |
| [meron_hubbard.sql](meron_hubbard.sql) | Requires exact rational UDFs supplied by its caller. The initial audit reproduces a 64-cluster native shift wrap; source-only comments do not enforce bounds. |
| [kitaev_honeycomb_schema.sql](kitaev_honeycomb_schema.sql) | A one-link incomplete hexagon is reported flux-consistent. Residual thresholds and stored flags do not certify braiding. |
| [chiral_superconductor_schema.sql](chiral_superconductor_schema.sql) | Numerical metadata and heuristic views; no validated error model, independent topological classification or complete review is established. |
| [regge_wdw_schema.sql](regge_wdw_schema.sql) | Numerical geometry and discrete audit relations; compilation alone does not verify the imported geometry, dynamics or physical interpretation. |

The former mixed PostgreSQL hash-partition example is preserved in the sealed
before-source. It is not executed or claimed tested by the current SQLite file.
Copies under `fsp/databases` and paper trees are separate artifacts: tests that
execute those copies do not certify this directory's bytes. Consult each file's
canonical `.contract.score.yaml` for its own assessment and evidence ceiling.
