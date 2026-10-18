# [TFQ-0371] old-image-injective-lift

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `707d9ae7-10da-5964-ac23-973bd75471b7`  
> **Parent Derivation**: [TFQ-0370](TFQ-0370_supplied-binary-refinement.md)

---

## 1. Abstract & Formal Statement

PG-OLD-IMAGE-INJECTIVE and ledger row WDP-P001-005 say that if a lift has a typed recovery of old terms on the old image, then the lift is injective. Opened Paper.lean declares old_image_injective. Ledger row WDP-P001-006 says term recovery alone yields neither off-image rejection, nor observation preservation, nor obstruction repair. Pre-Genesis paper.md section 10 is the heading. The finite statement still required is injectivity on that old image only, with the three negative boundaries left standing. Declaration ground_carrier_empty on Carrier 0 is a separate empty-ground fact.

### Governing Obligation
Typed recovery of old terms on the old image yields injectivity of that lift, and does not yield off-image rejection, observation preservation, or repair.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Domain-restriction (off-image refusal) half is separate; see PG-SN-OFF-IMAGE-REFUSAL.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: old_image_injective, scoped to typed recovery on the old image`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::old_image_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::off_image_not_implied`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::old_image_injective`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: old-image injectivity in crate pre_mssn_preservation, with the three negative boundaries as separate tests`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: an injectivity check for recover_word on the old alphabet that does not also claim off-image refusal`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0372](TFQ-0372_off-image-refusal-half.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch04_report_maps_fibers_quotients_and_sections.md`
