# [TFQ-0266] No derivation from stochastic kernels to complete positivity

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `GAP`  
> **UUID**: `bc4061e5-23b4-5fa2-8123-180d87317a10`  
> **Parent Derivation**: [TFQ-0265](TFQ-0265_stochastic_population_shadow_of_a_channel.md)

---

## 1. Abstract & Formal Statement

The derivation-graph reading note says no source that was read derives completely positive maps from stochastic kernels. QM_082 records the opposite arrow and a fence: complete positivity, Kraus, Choi, and Stinespring form, and coherence transport, are not forced by the kernel. A positive trace-preserving map can share the identity kernel and still fail complete positivity. DS-CPTP-COMPLETE-POSITIVITY-IMPORT marks complete positivity, the tensor with identity, and the environment extension as assumptions. QM_083 is only the annex for that fence.

### Governing Obligation
Leave the passage from a stochastic kernel to a completely positive map underived, and keep coherence transport imported.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complete positivity (assumption)`
- **Admitted**: `environment extension (assumption)`
- **Admitted**: `tensor product with identity (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open upgrade row: when off-diagonal transport is admissible.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H063CptpChannelsStinespring.lean::stinespring_requires_extension_verified`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/cptp_channels_stinespring.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0267](TFQ-0267_completely-positive_import_annex.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
