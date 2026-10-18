# [TFQ-0369] finite-demand-count

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9d256284-9cd6-5d22-8d95-b63e5e792893`  
> **Parent Derivation**: [TFQ-0368](TFQ-0368_index-layer-separation.md)

---

## 1. Abstract & Formal Statement

PG-DEMAND-ACCOUNTING and ledger row WDP-P001-002 record the next active-demand count s_next = s - d + b when the discharged set is a subset and births are disjoint. Opened Paper.lean declares demand_accounting. preservation.demand_step in the opened preservation.py returns the next active set as a frozenset, which is not yet the count identity. Pre-Genesis paper.md section 8 is the prose site. The finite statement still required is that count identity under those two hypotheses, together with ledger row WDP-P001-003: a displayed survivor sequence stays a chosen example and is not a native law.

### Governing Obligation
With discharged demands a subset and births disjoint, the next active count is s - d + b, and a chosen survivor list is not a law.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none (pure finite cardinality; survivor sequence example in WDP-P001-003 is a chosen ledger example, not a law).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: demand_accounting, hypotheses kept in the statement rather than dropped`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::demand_accounting`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::demand_accounting`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: the same cardinality step in crate pre_mssn_preservation, with the two hypotheses as fields`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a count wrapper around demand_step that states s_next = s - d + b only when discharged is a subset and births are disjoint`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0370](TFQ-0370_supplied-binary-refinement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
