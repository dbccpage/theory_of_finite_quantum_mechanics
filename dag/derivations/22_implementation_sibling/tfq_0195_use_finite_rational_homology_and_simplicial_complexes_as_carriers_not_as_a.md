# [TFQ-0195] Use finite rational homology and simplicial complexes as carriers, not as a

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `34c3fba2-a972-5fd2-b4a6-c8847cc6295d`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

omega_homology supplies finite carriers for later shadows and is not itself a quantum derivation. src/lib.rs opens as computational algebraic topology with AuthorityEffect None and says new TDA modules are best-effort shells unless marked otherwise. src/finite_rational_homology.rs computes rational homology quotients through the shared exact linear-algebra owner and states that it makes no integer-quotient transport or homotopy claim. src/simplicial.rs is the face-closed complex used by the gravity shadow. The obligation is to cite chain maps and simplices as finite controls only.

### Governing Obligation
Use finite rational homology and simplicial complexes as carriers, not as a quantum derivation.

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
- [`lean4/quantum_mechanics/FiniteCochain.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Homology.lean::induced_homology_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::chain_retraction_cannot_kill`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::homology_injective_of_chain_retraction`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::triangle_retraction_impossible`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::two_point_retraction_impossible`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_homology/src/chain_map.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/chain_map.rs::CertifiedChainMap`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/cochain_primitive_difference.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/finite_rational_homology.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/integral_chain_equivalence.rs::CheckedChainEquivalence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/lib.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_homology/src/simplicial.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/shelf.yaml`
