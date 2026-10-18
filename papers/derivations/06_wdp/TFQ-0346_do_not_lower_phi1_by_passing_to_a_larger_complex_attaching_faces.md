# [TFQ-0346] Do not lower Phi1 by passing to a larger complex, attaching faces,

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `61cbff6c-093e-5d92-9d1d-2c34d3944d59`  
> **Parent Derivation**: [TFQ-0345](TFQ-0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P09 states that restricting an edge field to a subcomplex with restricted weights never raises Phi1, that attaching 2-simplices leaves Phi1 unchanged while it can raise Gamma2, and that equal-weight subdivision through a new degree-two vertex leaves Phi1 unchanged. WDP-CH04-N02 says growth does not repair a quotient residual: a decrease requires deleting cells, changing declared weights, or changing existing edge values. Survival of a class to a filtration limit page records cohomology of the final complex rather than positivity of Phi1.

### Governing Obligation
Do not lower Phi1 by passing to a larger complex, attaching faces, or using equal-weight subdivision.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Chain complex over a declared coefficient ring (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized for 1-skeleton residual sums and 2-simplex attachments.

> [!WARNING]
> Statement is about declared finite complexes; it supplies the 'growth does not repair' direction used by WDP-CH04-N02.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_growth_subcomplex_monotone`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_two_simplex_attachment_preserves_phi1`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Homology.lean::induced_homology_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::chain_retraction_cannot_kill`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::homology_injective_of_chain_retraction`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::triangle_retraction_impossible`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::two_point_retraction_impossible`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_homology/src/chain_map.rs::CertifiedChainMap`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/integral_chain_equivalence.rs::CheckedChainEquivalence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_wdp_obligations_and_growth_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
