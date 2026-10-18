# Relational Database Schemas: Fermion Sign Problem & Genesis Survivor Witness Ledgers

> **Provenance.** Copied on 2026-09-23 from `the_symbol_game` at commit `e7596da`, path `research/relational_foundations/sql_fermion_sign/` (consolidated into `databases/`). Line endings and trailing whitespace were normalized, and link targets were re-pointed to this package. The research note it describes is the package's [`../fermion_sign_problem.md`](../fermion_sign_problem.md), which carries the 2026-09-22 scope correction: the SQL here is illustrative and does not establish a model-preserving or efficient sign-problem solution.

**Directory:** `coda_atlas/F004_papers/008_fsp/databases/`  
**Status:** LAB APPARATUS  
**AuthorityEffect:** None  
**Primary Formal Reference:** `sealed-derivation-v1` (`3100c4e`)  

---

## 1. Directory Contents & Scope

This directory contains the relational database schemas (SQLite / PostgreSQL), DDL specifications, and SQL queries for analyzing the Fermion Sign Problem, tracking Genesis survivor witnesses, and simplicial boundary complexes for the discrete primitive difference tower and Minimal Symbol Game $\mathcal{S}(N)$:

- **[`fermion_sign_problem.md`](../fermion_sign_problem.md):** Research discussion on the Fermion Sign Problem as SQL CTEs, algebraic window quotients `OVER (PARTITION BY state_orbit_hash)`, and PostgreSQL declarative hash sharding.
- **[`fermion_sign_problem.sql`](fermion_sign_problem.sql):**
  1. SQLite-compatible Common Table Expressions (CTEs) demonstrating algebraic state cancellation via window quotient aggregations: `OVER (PARTITION BY state_orbit_hash)`. The Python integration test executes the first two statements.
  2. Illustrative PostgreSQL declarative hash sharding DDL (`CREATE TABLE state_space_sharded ... PARTITION BY HASH (orbit_hash)`), partitioning positive and negative sign contributions across discrete relational shards.
- **`meron_hubbard.sql`:** Relational SQL schema for Meron cluster transformations, pairing projectors, and Hubbard sign cancellation evaluations.
- **`regge_wdw_schema.sql`:** Relational schema and auditing views for 4D CDT simplicial complexes, fermionic matter fields, Kähler-Dirac doubling, overlap Ginsparg-Wilson relations, and Super-WDW constraints (`ViewCdtFermionSignBqnfAudit`, `ViewCdtSusyWittenAudit`).
- **`fermion_gin_index_schema.sql`:** Relational schema for Generalized Inverted Index (GIN) over fermionic Fock space configurations and occupation number bitsets.
- **`chiral_superconductor_schema.sql`:** Relational CTE schema for 2D/3D chiral p-wave topological superconductors and Majorana zero mode edge audits.
- **`kitaev_honeycomb_schema.sql`:** Relational CTE schema for the Kitaev honeycomb lattice model and Z2 vortex flux audits.
- **[`schema.sql`](schema.sql):** Standard ANSI SQL DDL schema defining survivor witness ledgers (`survivor_witnesses`), simplicial boundary complexes (`genesis_stages`, `boundary_simplices`), and Genesis run receipts.

---

## 2. Relational Schema Blueprint

```sql
-- Survivor Witness Ledger
CREATE TABLE IF NOT EXISTS survivor_witnesses (
    witness_id TEXT PRIMARY KEY,
    stage_id INTEGER NOT NULL,
    x_locus TEXT NOT NULL,
    y_locus TEXT NOT NULL,
    demand_type TEXT NOT NULL,
    qx_observation TEXT NOT NULL,
    qy_observation TEXT NOT NULL,
    reason TEXT NOT NULL,
    is_retained BOOLEAN NOT NULL DEFAULT 1
);

-- Genesis Stage Ledger
CREATE TABLE IF NOT EXISTS genesis_stages (
    stage_num INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    carrier_type TEXT NOT NULL,
    boundary_formula TEXT,
    degrees_of_freedom INTEGER NOT NULL,
    status TEXT NOT NULL
);
```

---

## 3. Claim Hygiene Ledger

1. **What this supports:**  
   Structured relational representation of signed state spaces, algebraic sign cancellation in quotient orbits, and persistent storage of survivor witnesses in 1NF relations.
2. **What this does not support:**  
   Polynomial-time classical solution to arbitrary NP-hard quantum Monte Carlo sign problems, infinite continuum field configurations, or non-deterministic SQL engines.
3. **The narrowest defensible claim:**  
   Finite state space signed path cancellations can be evaluated within standard relational SQL using window quotient aggregations, and finite 6-tuple witness ledgers and simplicial boundary complexes can be losslessly represented in standard First Normal Form (1NF) SQL relations.
4. **The next test needed:**  
   Execute SQLite integration tests verifying exact cancellation $\sum_{s \in \mathcal{O}} \mathrm{sgn}(s) = 0$ for balanced non-trivial permutation orbits and storing and querying `genesis_stages.py` simulation outputs.
