# [TFQ-0291] Disjoint aggregation and the real p>1 import

> **Stage**: `L1_TO_L2` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `d7832be5-6ffb-5b12-a45f-93bdb0319e30`  
> **Parent Derivation**: [TFQ-0290](TFQ-0290_direct_normalization_of_sector_weights.md)

---

## 1. Abstract & Formal Statement

qm_020_born_normalization_and_conditional_hilbert_lift.md separates an l1 coordinate defect from a strict comparison for exponents above one on disjoint supports. The finite obligation on the rational side is the sign defect: the coordinate triangle defect vanishes when the two entries are not of opposite sign, which is the fragment BornRedundancy.lean actually states. The claim ledger says the real-exponent comparison is prose and that Lean hardens a rational defect plus natural-exponent cases.

### Governing Obligation
Keep the rational sign defect in the finite file and import real p>1 subadditivity.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `real analysis (Minkowski, strict convexity): assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Real-exponent p>1 is node L1-QM020-THM2B-MINKOWSKI. Lean covers integer D1 only.

> [!WARNING]
> Not mechanized.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::D1_zero_iff_mul_nonneg`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::D1_zero_iff_same_sign`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0292](TFQ-0292_square-root_field_for_amplitude_coordinates.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
