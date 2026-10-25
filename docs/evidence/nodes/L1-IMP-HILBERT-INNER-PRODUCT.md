# L1-IMP-HILBERT-INNER-PRODUCT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A Hilbert inner product on the linearized carrier is admitted up to two laws of its quadratic readout: sector additivity on disjoint supports and transitive sector symmetry. Under these laws the form is unique up to a unit scale and equals the standard form of the Born carriers (dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form). H005 exhibits more than one admissible Gram form on the same carrier; its form diag(1,2) is a sector-additive form that violates the symmetry law, so the non-uniqueness is exactly the absence of that law.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 17
- cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- sector additivity of the quadratic readout on disjoint supports: assumption (transcribed from l1 additivity)
- transitive sector symmetry of the readout: assumption (node L1-IMP-SECTOR-SYMMETRY-LAW)
- sector carrier, scalar field and quadratic readout shape: assumption
- free linearization coefficient pack: assumption

## Bottleneck

Sector additivity of the quadratic readout (transcribed from edgewise l1 additivity) and transitive sector symmetry (node L1-IMP-SECTOR-SYMMETRY-LAW) are supplied as laws of the readout, not derived from primitives; the sector carrier, the scalar field and the quadratic shape of the readout remain imports. Without transitivity the diagonal is constant only on orbits.

## Source status

Sector-form selection kernel-checked in dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form: a symmetric (Hermitian) Gram form whose readout is additive on disjoint sector supports and invariant under a set of sector permutations generating a transitive group equals G i0 i0 * 1 (SectorFormUniqueness.eq_smul_one, eq_smul_one_generated; SectorFormHermitian.eq_smul_one over Q(i)); the scale is positive for a positive-definite readout (scale_pos), two such forms are proportional (unique_up_to_scale), and the unit-normalised form is the standard form qf 1 / hf 1 of the Born carriers (eq_one_of_normalized). Countermodels diag(1,2) (the H005 form; sector additive, not swap invariant) and 1+(all ones) (swap invariant, not sector additive) show each law is used. Exact replays: code/python/src/qm/inner_product_uniqueness.py, code/rust/src/qm/inner_product_uniqueness.rs. Earlier: QM_122 H004 free linearization needs an imported coefficient pack; H005 inner-product admission, gram not unique

## Review

- PFP review: [dag/results/L1-IMP-HILBERT-INNER-PRODUCT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-IMP-HILBERT-INNER-PRODUCT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Exact three Gram pairings/norms and anisotropy controls, with general weighted difference and concrete nonuniqueness in Lean.
  - does not support: Prove positive-definite inner-product instances and source-carrier refinement, then justify any physical selection. The inner product remains admitted structure.
  - next test: Prove positive-definite inner-product instances and source-carrier refinement, then justify any physical selection. The inner product remains admitted structure.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |
- counts toward the grade: yes

### Lean: `lean4/H005InnerProductAdmission.lean`

- file: [lean4/H005InnerProductAdmission.lean](../../../lean4/H005InnerProductAdmission.lean)
- sha256 (`bytes`): `25072066552c061b7ce2206ed10846ef1fe954edbb7dc5056a34de573929e55c`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H005InnerProductAdmission`): recorded sha256 `25072066552c061b7ce2206ed10846ef1fe954edbb7dc5056a34de573929e55c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H005InnerProductAdmission`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gram_not_unique` | yes | yes | yes | propext | `#print axioms gram_not_unique` |
| `inner_product_admission` | yes | yes | yes | Quot.sound, propext | `#print axioms inner_product_admission` |
- counts toward the grade: yes

### Lean: `lean4/SectorFormHermitian.lean`

- file: [lean4/SectorFormHermitian.lean](../../../lean4/SectorFormHermitian.lean)
- sha256 (`bytes`): `78ea0b521e573c51d4a1ced879454648a6ba2ca37d87f54f5383eaaccd551efc`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `SectorFormHermitian`): recorded sha256 `78ea0b521e573c51d4a1ced879454648a6ba2ca37d87f54f5383eaaccd551efc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SectorFormHermitian`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InnerProductFable.HermitianSectorForm.eq_smul_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.HermitianSectorForm.eq_smul_one` |
| `InnerProductFable.HermitianSectorForm.eq_smul_one_generated` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.HermitianSectorForm.eq_smul_one_generated` |
| `InnerProductFable.HermitianSectorForm.hf_eq_scale_vnorm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.HermitianSectorForm.hf_eq_scale_vnorm` |
| `InnerProductFable.HermitianSectorForm.imagLeak12_not_sectorAdditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.HermitianSectorForm.imagLeak12_not_sectorAdditive` |
- counts toward the grade: yes

### Lean: `lean4/SectorFormUniqueness.lean`

- file: [lean4/SectorFormUniqueness.lean](../../../lean4/SectorFormUniqueness.lean)
- sha256 (`bytes`): `2a08c38a779ba3b7cba8520f9134cfe8e9c8a5020d063c8d316c37e78aef79be`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `SectorFormUniqueness`): recorded sha256 `2a08c38a779ba3b7cba8520f9134cfe8e9c8a5020d063c8d316c37e78aef79be` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SectorFormUniqueness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InnerProductFable.SectorForm.diag12_not_invariant_swap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.diag12_not_invariant_swap` |
| `InnerProductFable.SectorForm.eq_one_of_normalized` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.eq_one_of_normalized` |
| `InnerProductFable.SectorForm.eq_smul_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.eq_smul_one` |
| `InnerProductFable.SectorForm.eq_smul_one_generated` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.eq_smul_one_generated` |
| `InnerProductFable.SectorForm.qf_eq_scale_dot` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.qf_eq_scale_dot` |
| `InnerProductFable.SectorForm.scale_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.scale_pos` |
| `InnerProductFable.SectorForm.unif12_not_sectorAdditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.unif12_not_sectorAdditive` |
| `InnerProductFable.SectorForm.unique_up_to_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.unique_up_to_scale` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/inner_product_uniqueness.rs`

- file: [code/rust/src/qm/inner_product_uniqueness.rs](../../../code/rust/src/qm/inner_product_uniqueness.rs)
- sha256 (`bytes`): `3288c2617990e81fef8a9796a537a60c3f639a1eedc3c373d6860ae59a94fdd7`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `derive_scale` (rust_symbol) | yes | yes | yes | - | - |
| `hermitian_derive_scale` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md`

- file: [dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md](../../../dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md)
- sha256 (`lf-normalised`): `afafc9b824245cd2b19b9f248fe02687da0b8782d2f01dd84904020ef321fe45`
- generated view: listed, not counted
- cited in: record TFQ-0355 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0296_hilbert_inner_product_is_admitted_structure.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0296_hilbert_inner_product_is_admitted_structure.md](../../../dag/derivations/08_l1_to_l2/tfq_0296_hilbert_inner_product_is_admitted_structure.md)
- sha256 (`lf-normalised`): `83cda23d2fb389c5c0c531914f4340dc368e3bf075b4685be3f734f54aec9f9e`
- generated view: listed, not counted
- cited in: record TFQ-0296
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0296 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs
- TFQ-0296 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs

## Routes

Incoming (2):

- `L1-R-INNER-PRODUCT-GAP` `GAP_NO_DERIVATION`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)
- `L1-R-INNER-PRODUCT-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (PROVED_LEAN), [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) (PROVED_LEAN), [L1-IMP-SECTOR-SYMMETRY-LAW](L1-IMP-SECTOR-SYMMETRY-LAW.md) (IMPORTED_ASSUMPTION)

Outgoing (9):

- `APP-R-FSP-CAR-EXTERIOR-FOCK` `DERIVED_PROSE`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)
- `L1-R-DYNAMICS-FINITE-WIGNER` `CONDITIONAL_ON_IMPORT`: [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL)
- `L1-R-DYNAMICS-GAP` `CONDITIONAL_ON_IMPORT`: [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL)
- `L1-R-MNC-LEFTOVER` `DERIVED_LEAN`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (PROVED_LEAN)
- `L1-R-ORTHOGONAL-ADDITIVITY-GAP` `GAP_NO_DERIVATION`: [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)
- `L1-R-THM5` `DERIVED_LEAN`: [L1-QM020-THM5-PHASE-AVERAGED-SHADOW](L1-QM020-THM5-PHASE-AVERAGED-SHADOW.md) (PROVED_LEAN)
- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM6-P2-GLEASON](L1-QM020-THM6-P2-GLEASON.md) (IMPORTED_ASSUMPTION)
- `UDG-R-TFQ-0297` `GAP_NO_DERIVATION`: [TFQ-0297](TFQ-0297.md) (OPEN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
