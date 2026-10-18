# [TFQ-0335] From typed old-image recovery, record injectivity of the lift only, and refuse

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e5f79f78-4df5-5d3d-9750-460ba2d2e7d9`  
> **Parent Derivation**: [TFQ-0334](TFQ-0334_let_one_supplied_binary_tag_separate_one_collapsed_pair_and_keep_the.md)

---

## 1. Abstract & Formal Statement

WDP-P001-005 records that typed old-image recovery implies injectivity of the lift, and that off-image rejection is not this row. WDP-P001-006 is the negative boundary: term recovery alone implies neither off-image rejection, observation preservation, nor obstruction repair. The DAG node PG-OLD-IMAGE-INJECTIVE carries the same split, including the negative symbols for off-image, observation, and repair. PG-SN-OFF-IMAGE-REFUSAL is a separate node for the domain-restriction half of WDP-P001-019. This slice does not promote either row. AuthorityEffect is None.

### Governing Obligation
From typed old-image recovery, record injectivity of the lift only, and refuse off-image rejection, observation preservation, and obstruction repair as consequences.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Domain-restriction (off-image refusal) half is separate; see PG-SN-OFF-IMAGE-REFUSAL.

> [!WARNING]
> Closes the domain-restriction half of WDP-P001-019; off-image points are refused by section-retraction roundtrip.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::old_image_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::off_image_not_implied`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::old_image_injective`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.accepted_only_from_section`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.nonDescent_iff_off_image`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.old_image_base'`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_sn_off_image_refusal_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0336](TFQ-0336_keep_unequal_finite_alphabets_from_a_free-monoid_isomorphism_and_keep_language_restriction.md)
- [TFQ-0341](TFQ-0341_refuse_unrestricted_old-image_recovery_and_the_advertised_sncarrier_cardinalities_until_a.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
