# [TFQ-0337] Record homology injectivity under a chain-map retraction, and record that the two-point

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `3b76c446-671f-5473-9007-07bfd137f75f`  
> **Parent Derivation**: [TFQ-0336](TFQ-0336_keep_unequal_finite_alphabets_from_a_free-monoid_isomorphism_and_keep_language_restriction.md)

---

## 1. Abstract & Formal Statement

WDP-P001-012 records that a chain-map retraction forces homology injectivity, and that the two-point edge and the filled triangle admit no chain-map retraction fixing the original complex. WDP-P001-011 records that on the two-point graph, H0 counts undirected components and loops do not lower that count. WDP-P001-013 is a definition: chains, cochains, homology, homotopy, and directed reachability are distinct, and a vanishing homology class is not a homotopy contraction. DAG node PG-CHAIN-RETRACTION cites Pre-Genesis lines 493-519 and the Paper001.lean homology symbols. AuthorityEffect is None.

### Governing Obligation
Record homology injectivity under a chain-map retraction, and record that the two-point edge and filled triangle do not retract onto the original complex.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Chain complex over a declared coefficient ring (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Statement is about declared finite complexes; it supplies the 'growth does not repair' direction used by WDP-CH04-N02.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Homology.lean::induced_homology_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::chain_retraction_cannot_kill`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::homology_injective_of_chain_retraction`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::triangle_retraction_impossible`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::two_point_retraction_impossible`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_homology/src/chain_map.rs::CertifiedChainMap`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/integral_chain_equivalence.rs::CheckedChainEquivalence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0338](TFQ-0338_descend_a_question_to_the_realized_report_image_exactly_when_it_is.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
