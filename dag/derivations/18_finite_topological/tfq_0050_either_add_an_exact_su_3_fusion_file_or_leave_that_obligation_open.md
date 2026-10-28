# [TFQ-0050] Either add an exact SU(3) fusion file or leave that obligation open

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `63c6efed-2e38-5a2c-a9d0-91e003055f72`  
> **Parent Derivation**: [TFQ-0049](tfq_0049_keep_frobenius_and_multiplicity_free_fusion_off_the_missing_color_hopf_algebra.md)

---

## 1. Abstract & Formal Statement

catalog.rs pins exact ribbon data for Ising, Fibonacci, semion, pointed braided categories, the toric code as D(Z_2), a three-fermion model, and quantum doubles D(Z_n). A coefficient field that lacks the needed root of unity is FusionError::FieldTooSmall, not an approximation. su2_level.rs is the SU(2) family in a Racah gauge. The file su3_level.rs is absent from tfqm_fusion_categories/src, so there is no fusion-category obligation already discharged for SU(3)_k. The catalog does not assert a material host. This absence is an open obligation, not a negative theorem about fusion categories.

### Governing Obligation
Either add an exact SU(3) fusion file or leave that obligation open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/RibbonCategoryCatalog.lean`)
- `RibbonCategoryCatalog.catalog_ribbon_ranks_and_total_squared_dimensions`: Proves `isingTotalDimSq = 4`, `semionTotalDimSq = 2`, `z2x2PointedTotalDimSq = 4`, and `quantumDoubleCyclicRank n = n^2` (`4, 9, 16`).
- `RibbonCategoryCatalog.toric_code_vs_three_fermion_topological_spin_twists`: Proves `[0, 0, 0, 1]` vs. `[0, 1, 1, 1]` spin parities on `ℤ_2 × ℤ_2`.
- `RibbonCategoryCatalog.catalog_cyclotomic_field_admission_and_refusal`: Proves `fieldAdmitsRootOrder` rejects `Cyclotomic<8>` for Ising, Fibonacci, and `SU(2)_3`, and admits exact multiples.
- `RibbonCategoryCatalog.su3_level1_pointed_z3_fusion_vs_higher_level_nonpointed`: Proves `su3WeylAlcoveCount k` values for `k = 1..6`.
- `RibbonCategoryCatalog.quantum_double_z3_rank9_not_su3_level_k_fence`: Proves `su3WeylAlcoveCount k ≠ 9 = quantumDoubleCyclicRank 3` for `k = 1..6`.
- `RibbonCategoryCatalog.catalog_self_dual_models_not_su3_conjugate_pair_fence`: Proves `su3WeightConjugate (1, 0) = (0, 1) ≠ (1, 0)`.
- `RibbonCategoryCatalog.su3_level2_fundamental_quantum_dimension_golden_ratio`: Proves `d_{(1,0)}^2 = d_{(0,1)} + d_{(2,0)} = 1 + 2φ` in `QPhi`.
- `RibbonCategoryCatalog.absence_of_su3_level_rs_is_open_obligation_not_impossibility_theorem_fence`: Proves `su3LevelRepoClassification = OpenImplementationObligation`.
- `RibbonCategoryCatalog.catalog_ribbon_categories_do_not_assert_material_host_or_qcd_confinement_fence`: Audits `RibbonCatalogEntryAudit`.
- `RibbonCategoryCatalog.tfq0050_catalog_and_su3_level_scope_ledger_fence`: Audits `Tfq0050ScopeLedger`.

### Sovereign Rust Certifiers (`code/rust/src/fusion_categories/catalog.rs`, `code/rust/src/fusion_categories/su2_level.rs`)
- `code/rust/src/fusion_categories/catalog.rs::ising`
- `code/rust/src/fusion_categories/catalog.rs::fibonacci`
- `code/rust/src/fusion_categories/catalog.rs::semion`
- `code/rust/src/fusion_categories/catalog.rs::toric_code`
- `code/rust/src/fusion_categories/catalog.rs::three_fermion`
- `code/rust/src/fusion_categories/catalog.rs::quantum_double_cyclic`
- `code/rust/src/fusion_categories/su2_level.rs::su2_level`
- `code/rust/src/fusion_categories/su2_level.rs::unsupported_field_and_unbounded_level_are_typed_refusals`

### Independent Python Verification (`checks/independent/tfq-0050.py`)
- Executes `1357` exact rational and `ℚ(φ)` algebraic checks across `catalog.rs` models, `FieldTooSmall` refusals, `SU(3)_k` Weyl alcove counts, and `SU(3)_2` golden-ratio dimensions (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0051](tfq_0051_keep_the_spin_lift_on_declared_flat_complexes_and_off_the_dirac.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
