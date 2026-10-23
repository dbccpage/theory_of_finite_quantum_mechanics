# normal_forms/sql: a first relational slice of the repository

Authority effect: None. Everything here restates facts that already sit in
`dag/derivation_dag.json`, `dag/evidence/evidence_map.json`,
`dag/research/*lean_replay*.json` and the imported contracts under
`normal_forms/contracts/`. Loading a row does not change what any claim is
entitled to.

## Files

| File | Role |
|---|---|
| `universe.sql` | ANSI SQL:2016 core DDL: 76 tables, 3 views. Each table has a comment block naming its normal form and candidate keys. |
| `load_universe.py` | Builds an SQLite database from `universe.sql` and the source files. Fails on the first key, check or foreign-key violation. |
| `test_universe.py` | pytest suite: lossless join, keys and counts, normal-form sanity, DDL portability, README queries. |
| `universe.sqlite` | Generated, git-ignored. |

## Load

From the repository root:

```
python -I -X utf8 normal_forms/sql/load_universe.py            # writes normal_forms/sql/universe.sqlite
python -I -X utf8 normal_forms/sql/load_universe.py --db some.sqlite
python -I -X utf8 normal_forms/sql/load_universe.py --check     # in memory, then runs the tests
pytest normal_forms/sql/test_universe.py
```

The loader needs only the standard library and PyYAML. SQLite is used as an
engine for the DDL; the DDL itself uses no SQLite-specific syntax. It was
executed on SQLite only. "Portable" here means a denylist test and a review
against SQL:2016 core, not a run on a second engine.

## Design

* **Atomic facts.** A node is a bare key (`node`). Its stage, status, statement,
  bottleneck and source status are separate one-attribute relations that join
  back on `node_id`. A list in the source (`lean`, `rust`, `tags`, `inputs`,
  ...) is one row per element with an `ordinal`, because order and repeats
  are part of the source value (one node lists the same Rust file ten times).
* **No NULLs.** An optional source field is an optional row. Every column is
  `NOT NULL`.
* **Normal forms.** Each table says in its comment whether it is "6NF-style"
  (a key plus at most one independently varying attribute, or key only) or
  plain BCNF (several attributes that belong together, such as the four audit
  flags of one replayed module). The label is a design claim. The tests check
  that the declared keys exist, that no attribute depends on a proper subset of
  a composite key, and that no pair of short attributes of a single-key table
  determines one another in the loaded data, apart from coincidences the test
  names. One such coincidence: receipts that share a `checked_at` date in this
  checkout also share one Lean version string. The version stays a fact of the
  receipt file. The data checks can refute a design; they cannot prove one.
* **Changes the first draft needed.** Two checks found real faults while this
  was written: a citation table in which the cited work determined its authors
  and year (now split into `nf_work` and `nf_citation`), and a
  `built_successfully` flag that the draft treated as a function of `exit_code`
  but that the source records for only one receipt file (now an optional-row
  table). One later receipt omits `source_unchanged_during_build`, so that
  flag is its own optional-row table too.

## Tables

Vocabularies: `stage`, `node_status_code`, `route_status_code`,
`record_status_code`, `evidence_grade_code`, `lean_axiom`, `lean_axiom_allowed`.

Nodes: `node`, `node_stage`, `node_status`, `node_source_status`,
`node_statement`, `node_bottleneck`, `node_source_ref`, `node_lean_ref`,
`node_rust_ref`, `node_python_ref`, `node_imported_structure`, `node_tag`,
`node_see_also`.

Routes: `route`, `route_status`, `route_input`, `route_output`,
`route_source_ref`, `route_mechanism`, `route_note`.

Records: `record`, `record_name`, `record_summary`, `record_obligation`,
`record_stage`, `record_status`, `record_source_slice`, `record_parent`,
`record_coda_atlas_id`, `record_coda_atlas_path`, `record_dag_id`,
`record_f004_ref`, `record_lean4_ref`, `record_python_ref`, `record_rust_ref`,
`record_pfp_review_ref`.

Lean evidence: `evidence_grade`, `evidence_fact`, `evidence_file`, `lean_file`,
`lean_file_replay`, `lean_declaration`, `lean_declaration_scan`,
`lean_declaration_listing`, `replay_receipt`, `lean_module`, `lean_module_node`,
`receipt_module`, `receipt_module_build`, `receipt_module_source_unchanged`, `receipt_module_audit`,
`receipt_declaration`, `receipt_axiom` (one row per declaration and axiom).

Reviews: `pfp_review_file`, `pfp_review`, `pfp_review_claim`, `pfp_review_prior`,
`pfp_review_ref`, `pfp_review_superseded_by`, `pfp_review_prior_route_status`.

Contracts: `nf_contract`, `nf_contract_status`, `nf_verification_status`,
`nf_theory_status`, `nf_work`, `nf_citation`, `nf_citation_label`,
`nf_non_claim`, `nf_source_file`.

Views, each a `NATURAL JOIN` of the one-row-per-key relations: `node_core`,
`route_core`, `record_core`.

## What the tests establish

* **Lossless join.** Every node (all 13 source fields, including the nested
  `pfp_review`), route and record is rebuilt from the tables and compared with
  the JSON for equality. Replay receipts, per-declaration axiom sets, evidence
  grades and facts, Lean file and declaration flags, and every contract field
  that was taken are rebuilt the same way. Row counts are read from the source
  files, never hard-coded.
* **What "lossless" excludes.** The order of the `nodes`, `routes` and
  `records` arrays is not stored; they are treated as sets. An explicit empty
  list and an absent key are both zero rows: 36 nodes have `see_also: []` and
  6 routes have `source: []`, and the tests remove those empties from the
  expected side and say so.
* **Keys.** `PRAGMA foreign_key_check` is empty, the constraints reject a
  duplicate key, a dangling reference and a bad value, and the loader raises on
  a mutated source.
* **Widths.** SQLite ignores `CHARACTER VARYING(n)`, so a test checks that
  every loaded value fits its declared width.

## Example queries

All six run against the loaded database (the test suite executes every block
below and requires rows back). They use only joins, `GROUP BY`, `HAVING`,
`CASE` and `||`, and no row-limiting clause, which SQLite spells differently
from the standard.

1. Nodes per stage and status, largest groups first.

```sql
SELECT s.stage_name, st.status_code, COUNT(*) AS nodes
FROM node_stage AS s
JOIN node_status AS st ON st.node_id = s.node_id
GROUP BY s.stage_name, st.status_code
ORDER BY nodes DESC, s.stage_name, st.status_code;
```

2. For nodes whose status is `PROVED_LEAN`, how much evidence the repository
   holds for them. A grade says what is present in the checkout, not whether
   the claim is true.

```sql
SELECT eg.grade_code, COUNT(*) AS nodes
FROM node_status AS ns
JOIN evidence_grade AS eg ON eg.node_id = ns.node_id
WHERE ns.status_code = 'PROVED_LEAN'
GROUP BY eg.grade_code
ORDER BY eg.grade_code;
```

3. Routes that the source marks `GAP_NO_DERIVATION` and that need three or more
   inputs.

```sql
SELECT rs.route_id, ro.output_node_id, COUNT(ri.node_id) AS inputs
FROM route_status AS rs
JOIN route_output AS ro ON ro.route_id = rs.route_id
JOIN route_input AS ri ON ri.route_id = rs.route_id
WHERE rs.status_code = 'GAP_NO_DERIVATION'
GROUP BY rs.route_id, ro.output_node_id
HAVING COUNT(ri.node_id) >= 3
ORDER BY inputs DESC, rs.route_id;
```

4. Which axioms the replayed Lean declarations use, and in how many modules.

```sql
SELECT axiom_name, COUNT(*) AS declaration_uses, COUNT(DISTINCT lean_module_name) AS modules
FROM receipt_axiom
GROUP BY axiom_name
ORDER BY declaration_uses DESC, axiom_name;
```

5. Contracts whose status in the source `index.yaml` differs from the
   contract's own `contract_status`.

```sql
SELECT c.nf_id, c.index_status, s.contract_status
FROM nf_contract AS c
JOIN nf_contract_status AS s ON s.nf_id = c.nf_id
WHERE c.index_status <> s.contract_status
ORDER BY c.nf_id;
```

6. A join across sections: where the Lean files cited by `PROVED_LEAN` nodes
   are. `node_lean_ref.lean_ref` holds the source string `path::symbol`, so it
   joins to `lean_declaration` through `||`. A node whose cited declarations
   all sit in files that are not `present` would be a `PROVED_LEAN` node with
   no Lean evidence in this checkout.

```sql
SELECT f.resolution, COUNT(DISTINCT n.node_id) AS nodes, COUNT(*) AS cited_declarations
FROM node_status AS n
JOIN node_lean_ref AS r ON r.node_id = n.node_id
JOIN lean_declaration AS d ON r.lean_ref = d.lean_path || '::' || d.symbol
JOIN lean_file AS f ON f.lean_path = d.lean_path
WHERE n.status_code = 'PROVED_LEAN'
GROUP BY f.resolution
ORDER BY f.resolution;
```

On the data at the time of writing, query 5 returns `nf.classical.eknf`
(index says active, the contract says draft) and `nf.cohomology.acnf`
(index says draft, the contract says deprecated), and query 6 shows every
cited declaration of a `PROVED_LEAN` node in a `present` file, which agrees
with the `proved_lean_external_only` mismatch count of 0 in
`dag/evidence/evidence_map.json` (it was 53 before the cited sibling-atlas Lean
files were imported into `lean4/Imported/`). That agreement is a cross-check
between two independent derivations, not a result about the mathematics.

## What is not yet modelled

* **Source structure that is dropped.** Array order of `nodes`, `routes` and
  `records`; the empty-list versus absent-key distinction; the top-level prose
  of `derivation_dag.json` (`title`, `scope`, `edge_semantics`,
  `non_discharge_notes`, `segment_notes`, `schema_notes`, `index_document`,
  `source_commit`).
* **Evidence map.** Only `lean_decl` items are modelled. The paper, Rust
  symbol, Python symbol, test and external items, `reviews`, `flags`,
  `absent_notes`, `mismatches`, `routes` in/out, `next_step`, `dependents`,
  `receipts_not_indexed` and the derived `summary` are not. `toolchain` is
  not stored because it is the numeric part of `lean_version`.
* **Replay files.** `receipt_declaration` and `receipt_axiom` come from every
  `dag/research/*lean_replay*.json` module result. Most files nest that list
  at `lean_replay.results`. The PGW campaign receipt puts the same list at
  the top level, and the loader reads that list. Evidence-map receipts whose
  file is not one of those replay files stay in `receipt_module` without
  itemised declarations. The `anchors`, `output`, `seconds` and
  `admission_scan` counts are not stored.
* **Declaration identity.** `receipt_declaration.declaration` is a Lean name
  and `lean_declaration` is a (path, symbol) pair. They are not linked by a
  foreign key because the name forms differ (module-qualified versus
  namespace-qualified).
* **Other repository facts.** `dag/results/**`, `dag/fragments`, the TFQ JSONL,
  `dag/prompts`, Lean, Rust and Python source, `papers/`, `problem_sets/`,
  `rules/`, `docs/`, `evidence/` and the git history have no tables.
* **Contracts.** Only identity, status, citation, `non_claims` and provenance
  are rows. `declarations_required`, `validation_criteria`, `terminal_routes`,
  `proof_obligations`, `failure_modes`, `examples` and the quadrilateral
  details are not. `_golden_nfs/normal_forms_schema.sql` was copied but not
  reconciled with this schema. The `category` column of `nf_contract` is a rule
  applied by the loader (documented in `universe.sql`), not a field in the
  contracts.
* **Constraints that are queries.** Cross-table rules such as "a `PROVED_LEAN`
  node should have an `E3` grade" are not declared as constraints; the
  repository already reports them as mismatches, and they are left as queries.
* **Engines.** Only SQLite has run the DDL, and SQLite enforces neither the
  `CHARACTER VARYING` widths nor `BOOLEAN`; the width check is a test.
* **`node_python_ref`** is empty because no node carries a `python` key; only
  records do.
