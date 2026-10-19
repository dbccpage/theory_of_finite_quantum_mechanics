# [TFQ-0360] Supply the admitted cut (X, E, tau, K) as data, and do

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `009c2148-3b2c-50de-950b-1a22b5d66198`  
> **Parent Derivation**: [TFQ-0343](tfq_0343_leave_gen_wdp_o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md)

---

## 1. Abstract & Formal Statement

WDP-CH01-D01 defines an admitted cut as a finite tuple (X, E, tau, K) of tokens, incidences, roles, and admissible comparisons, supplied rather than selected from equality alone. WDP-CH01-P02 states that for a pointed relation on a finite carrier, relatedness does not imply distinctness, distinctness does not imply relatedness, and relatedness plus irreflexivity does imply distinctness. WDP-CH01-N01 says the admitted cut does not derive a spectral ground state, a physical vacuum, or a cosmological ground state.

### Governing Obligation
Supply the admitted cut (X, E, tau, K) as data, and do not obtain a ground state or a discharged O01 floor from equality alone.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Exhibited cut with law (assumption: supplied, not selected from equality alone)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Shows a law is needed to separate endpoints; does not derive the law from <> or from Real_0.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PointedRelation.lean::pointed_relation_independence`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::endpoints_apart`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::identification_breaks_law`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::no_cut_on_subsingleton`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_admission_execution.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
