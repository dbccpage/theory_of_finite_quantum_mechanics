# [TFQ-0382] refined-minimum-class

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `a0733504-b98c-513f-af45-ee85a2d51ae6`  
> **Parent Derivation**: [TFQ-0381](tfq_0381_cost_two_first_separation.md)

---

## 1. Abstract & Formal Statement

Ledger row WDP-P000-008 says Reading L has infinitely many nonisomorphic item-cost minima, while both readings have one refined-cost minimum class at the pair (2, 1). A separate source enumeration at arity at most two is also recorded there: six deltas in three classes for L, and ten in five classes for F. MinimalityF.lean is listed and was not opened. The finite statement still required is to keep the refined class (2, 1) distinct from that unbounded item-cost family, and to keep the arity-at-most-two census as a bounded count rather than a stand-in for the unbounded family.

### Governing Obligation
Both readings have one refined-cost minimum class at (2, 1), while Reading L still has an unbounded family of item-cost minima.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared candidate space of one-step augmentations (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Minimality is relative to the declared finite candidate space; not a global minimality claim.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`missing declaration obligation: refined class (2, 1) versus the unbounded reading-L family, file listed and not opened`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::U0_separable`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::deltaU0_valid`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/MinimalityF.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: separate counters for item-cost minima and the refined class`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a refined-cost key (2, 1) in 000_genesis_19l57g1/code/derivation/candidates.py that does not hide the unbounded reading-L family`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0383](tfq_0383_closure_round_inequality.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
