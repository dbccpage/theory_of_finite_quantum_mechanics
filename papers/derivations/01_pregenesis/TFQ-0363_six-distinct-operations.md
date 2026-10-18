# [TFQ-0363] six-distinct-operations

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `23f3688a-199b-57d1-8e40-0385eb4c71d2`  
> **Parent Derivation**: [TFQ-0362](TFQ-0362_four-host-conditions.md)

---

## 1. Abstract & Formal Statement

PG-SIX-OPERATIONS and historical ledger row WDP-P000-003 require Mention, Supply, Designate, Admit, Retain, and Operate to stay six operations. Opened Pre-Genesis paper.md section 3 and Genesis paper.md section 3 are the cited headings. The DAG statement says only Admit changes admitted state, and that conflating supply with admission is the source of the later Reading L and Reading F split. The finite statement still required is six separately typed operations, with a check that Supply and Designate do not write the admitted regime. No single enum in the opened Python preservation module carries those six names.

### Governing Obligation
Mention, Supply, Designate, Admit, Retain, and Operate stay six operations, and only Admit changes admitted state.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Definitional separation; no theorem is attached to the list itself. The one Lean-checked consequence is supply_no_op (PG-GEN-SUPPLY-NO-OP).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate`](../../code/lean4/)
- [`missing declaration obligation: six operation names beside supply_no_op in Derivation/Inertia.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: six named operations in omega_ooutwire_primitives rather than one event enum that merges them`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/supply.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: six operation constructors in 000_genesis_19l57g1/code/derivation/model.py, listed but not opened, kept distinct from one another`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0364](TFQ-0364_three-trial-record-bound.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
