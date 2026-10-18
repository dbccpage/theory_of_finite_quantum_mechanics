# [TFQ-0348] Certify a rational Phi1 value by a bounded circulation that meets a

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `4f0476d6-1a5b-54c7-84af-a9ef8eb5ffad`  
> **Parent Derivation**: [TFQ-0345](TFQ-0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P07 states that over Q, with positive rational weights, any circulation y with d0-star y equal to zero and absolute values bounded by the weights gives a pairing at most Phi1,w, so a repair and such a circulation with equal values certify the value without importing strong duality. WDP-CH04-P08 records the filled triangle with edges (01, 12, 02) and delta (1, 1, 0): Phi1 = 2 at f = (0, 1, 0), dual y = (1, 1, -1), Gamma2 = 2, and R_cl = 1. obstruction.rs says it emits a Kirchhoff divergence-free dual witness with zero duality gap against Phi1, using an exact rational simplex.

### Governing Obligation
Certify a rational Phi1 value by a bounded circulation that meets a repair, as on the filled triangle, without treating that certificate as a Genesis derivation of the window.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Norm hypothesis over R, C, or Q restricted from the real extension (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Ledger rows carry prose (P03) and prose plus computed (P04, P05) bindings, no L: binding. Lean symbols with matching names exist in Obstruction.lean (not checked against statements); they cover the exact sequence and ratio bounds at the symbols named, not necessarily every clause (claim_map.md not re-checked row by row).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::closure_ratio_le_opnorm`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::closure_ratio_nonneg`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_exact_sequence`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_well_defined`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_wdp_obligations_and_growth_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
