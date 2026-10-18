# [TFQ-0241] Projection postulate and Born pairing remain imported

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `1f19289b-e4b8-52dc-89ee-c2f77bf93b64`  
> **Parent Derivation**: [TFQ-0239](TFQ-0239_finite_path_sum_on_a_unique_intermediate_cut.md)

---

## 1. Abstract & Formal Statement

QM_030's ledger, as extracted in DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT, separates a finite descent reading of measurement from the projection postulate. Spectral projectors with E squared equal to E, and the observer pairing that turns weights into probabilities, are imported. The same node says an audit of several pairings does not select one Born rule. That matches Finite Quantum Mechanics section 1.1, rung 3, where positive states, effects, and a pairing are additional supplied structure, and the Born rule is not derived from difference.

### Governing Obligation
Do not read the finite path sum as having selected the projection postulate or a unique Born pairing.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `probability pairing and normalization (assumption)`
- **Admitted**: `projection postulate / spectral structure (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Overlaps L1_TO_L2 Born nodes (QM_020, other fragment).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/GleasonTheorem.lean::d2_binary_non_bornian_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_pairing_boundary`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
