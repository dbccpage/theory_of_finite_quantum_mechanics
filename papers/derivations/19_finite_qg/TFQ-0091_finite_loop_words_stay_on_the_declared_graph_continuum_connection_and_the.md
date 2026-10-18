# [TFQ-0091] Finite loop words stay on the declared graph. Continuum connection and the

> **Stage**: `FINITE_QG` | **Status**: `FINITE_SHADOW`  
> **UUID**: `3046dd61-ad8b-55ad-aaca-5951313c249b`  
> **Parent Derivation**: [TFQ-0090](TFQ-0090_gap_obl-r03_leaves_regge_deficit_uncoupled_from_cochain_curvature_obl-r01_leaves_the.md)

---

## 1. Abstract & Formal Statement

Closed-loop holonomy is the finite obstruction the later shadows share: an edge assignment, a loop product, and a class that survives gauge. The QM-207 goal checks mu_N cycle holonomy on a declared finite graph and keeps that check apart from Cauchy completion toward a circle. What is finite is a word in a finite group or a finite cyclic phase. What is not discharged is a continuum connection, smooth parallel transport, and the Einstein equation. The grammar is not a reconstruction of loop gravity and not a continuum limit.

### Governing Obligation
Finite loop words stay on the declared graph. Continuum connection and the Einstein equation are not discharged.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (derived from parent DS-QM062-U1-RESIDUES-IMPORT via ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization and ds_qm063_holonomy_coherent_intensity_and_gauge_invariance).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/CoboundaryHolonomy.lean::coboundary_closed_cycle_zero`](../../code/lean4/)
- [`lean4/quantum_mechanics/CoboundaryHolonomy.lean::flux_obstructs_coboundary`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs::is_gauge_trivial`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/holonomy_bridge_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0092](TFQ-0092_qm-110-c11_hamiltonian_constraint_stays_q-held_continuum_su_2_data_in_qm-110-c10_are_imported.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
