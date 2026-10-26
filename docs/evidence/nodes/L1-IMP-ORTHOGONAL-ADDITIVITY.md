# L1-IMP-ORTHOGONAL-ADDITIVITY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a sector-additive rational Gram matrix, the sum of each off-diagonal pair is zero and the quadratic readout equals the sum of the diagonal squares. Symmetry of the matrix is a further hypothesis before each off-diagonal entry is zero. On the 2 by 2 integer matrix with entries 1, 1, -1 and 1, the off-diagonal pair sums to 0, neither off-diagonal entry is 0, and for every integer pair a, b the quadratic form equals a*a + b*b, which equals the sum of the forms on (a, 0) and (0, b). Probability additive on arbitrary orthogonal frames, and projection measures, stay supplied.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 11
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- sector additivity of the quadratic readout on disjoint supports: assumption (transcribed from l1 additivity)
- frame additivity on arbitrary orthogonal frames of the selected form and projection measures / frames beyond the sector basis: assumption

## Bottleneck

The 2 by 2 matrix is one witness that a sector-additive form can keep a nonzero off-diagonal entry when the pair sums to zero. Frame additivity on arbitrary orthogonal frames, projection measures, and Gleason-type uniqueness stay supplied. Sector additivity of the quadratic readout on a general carrier remains the hypothesis transcribed from l1 additivity. AuthorityEffect: None.

## Source status

Orthogonality of the sector basis derived from sector additivity of the readout alone in dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form (SectorFormUniqueness.offdiag_pair_sum_eq_zero, offdiag_eq_zero, eq_diagonal_of_sectorAdditive, qf_eq_sum_diag_sq_of_sectorAdditive; SectorFormHermitian.offdiag_eq_zero with the two directions 1 and i, and imagLeak12 showing the second direction is needed). Frame additivity on arbitrary orthogonal frames is not derived. Earlier: Thm 6 assumptions 4 and 7: orthogonal additivity; projection-measure / frame-function structure

## Review

- PFP review: [dag/results/L1-IMP-ORTHOGONAL-ADDITIVITY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-IMP-ORTHOGONAL-ADDITIVITY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Exact projector resolution of identity, quadratic frame totals and quartic basis dependence, with generic orthogonal-frame algebra in Lean.
  - does not support: Prove source/array refinement and the full frame-law uniqueness theorem; a few frame values neither derive orthogonality nor prove Gleason.
  - next test: Prove source/array refinement and the full frame-law uniqueness theorem; a few frame values neither derive orthogonality nor prove Gleason.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignL1OrthogonalAdditivity.lean`

- file: [lean4/CampaignL1OrthogonalAdditivity.lean](../../../lean4/CampaignL1OrthogonalAdditivity.lean)
- sha256 (`bytes`): `4cd851daef44f1583b0de85c2cf7729cb4c959c52568265be656c6ec62dd0421`
- cited in: node.lean, node.source, receipt dag/research/campaign_l1-imp-orthogonal-additivity_lean_replay.json (CampaignL1OrthogonalAdditivity)
- replay: `verified`
  - receipt [dag/research/campaign_l1-imp-orthogonal-additivity_lean_replay.json](../../../dag/research/campaign_l1-imp-orthogonal-additivity_lean_replay.json) (module `CampaignL1OrthogonalAdditivity`): recorded sha256 `4cd851daef44f1583b0de85c2cf7729cb4c959c52568265be656c6ec62dd0421` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignL1OrthogonalAdditivity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignL1OrthogonalAdditivity.axisSum` | yes | yes | yes | propext | `#print axioms CampaignL1OrthogonalAdditivity.axisSum` |
| `CampaignL1OrthogonalAdditivity.entriesNotZero` | yes | yes | yes | none | `#print axioms CampaignL1OrthogonalAdditivity.entriesNotZero` |
| `CampaignL1OrthogonalAdditivity.pairSum` | yes | yes | yes | none | `#print axioms CampaignL1OrthogonalAdditivity.pairSum` |
| `CampaignL1OrthogonalAdditivity.readout` | yes | yes | yes | propext | `#print axioms CampaignL1OrthogonalAdditivity.readout` |

- counts toward the grade: yes

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

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0299
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: yes

### Lean: `lean4/H013BornPairingBoundary.lean`

- file: [lean4/H013BornPairingBoundary.lean](../../../lean4/H013BornPairingBoundary.lean)
- sha256 (`bytes`): `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013BornPairingBoundary`): recorded sha256 `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H013BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quartic_rival` | yes | yes | yes | propext | `#print axioms quartic_rival` |

- counts toward the grade: yes

### Lean: `lean4/H013FrameAdditivity.lean`

- file: [lean4/H013FrameAdditivity.lean](../../../lean4/H013FrameAdditivity.lean)
- sha256 (`bytes`): `626dd1c874e5a1add3f02cb81f5f535c17637c2f55fdffa12a094b1c34f928a8`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013FrameAdditivity`): recorded sha256 `626dd1c874e5a1add3f02cb81f5f535c17637c2f55fdffa12a094b1c34f928a8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H013FrameAdditivity`
- counts toward the grade: yes

### Lean: `lean4/H013SameContract.lean`

- file: [lean4/H013SameContract.lean](../../../lean4/H013SameContract.lean)
- sha256 (`bytes`): `47568af5eaa40e031525b641574866c3044176756fb245b6084c96711e8bcca8`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013SameContract`): recorded sha256 `47568af5eaa40e031525b641574866c3044176756fb245b6084c96711e8bcca8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H013SameContract`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_effect_rules_share_unit_total_and_disagree` | yes | yes | yes | Quot.sound, propext | `#print axioms two_effect_rules_share_unit_total_and_disagree` |

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
| `InnerProductFable.HermitianSectorForm.imagLeak12_imag_direction_not_additive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.HermitianSectorForm.imagLeak12_imag_direction_not_additive` |
| `InnerProductFable.HermitianSectorForm.offdiag_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.HermitianSectorForm.offdiag_eq_zero` |

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
| `InnerProductFable.SectorForm.eq_diagonal_of_sectorAdditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.eq_diagonal_of_sectorAdditive` |
| `InnerProductFable.SectorForm.l1_disjoint_additive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.l1_disjoint_additive` |
| `InnerProductFable.SectorForm.offdiag_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.offdiag_eq_zero` |
| `InnerProductFable.SectorForm.offdiag_pair_sum_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.offdiag_pair_sum_eq_zero` |
| `InnerProductFable.SectorForm.qf_eq_sum_diag_sq_of_sectorAdditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFable.SectorForm.qf_eq_sum_diag_sq_of_sectorAdditive` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/inner_product_uniqueness.rs`

- file: [code/rust/src/qm/inner_product_uniqueness.rs](../../../code/rust/src/qm/inner_product_uniqueness.rs)
- sha256 (`bytes`): `3288c2617990e81fef8a9796a537a60c3f639a1eedc3c373d6860ae59a94fdd7`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `hermitian_sector_additivity_certificate` (rust_symbol) | yes | yes | yes | - | - |
| `sector_additivity_certificate` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/l1-imp-orthogonal-additivity.py`

- file: [checks/independent/l1-imp-orthogonal-additivity.py](../../../checks/independent/l1-imp-orthogonal-additivity.py)
- sha256 (`bytes`): `4706587ab3aec62b016a1b3099552d9fd24e9345418bbbc57bc5f6272ac8605b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0299_orthogonal_additivity_is_an_extra_frame_law.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0299_orthogonal_additivity_is_an_extra_frame_law.md](../../../dag/derivations/08_l1_to_l2/tfq_0299_orthogonal_additivity_is_an_extra_frame_law.md)
- sha256 (`lf-normalised`): `1063b6852f23b60ef029ea2e4b527b92e1d94778ff67de2bd4a4777407e4cb89`
- generated view: listed, not counted
- cited in: record TFQ-0299
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/l1-imp-orthogonal-additivity.md`

- file: [dag/derivations/independent/l1-imp-orthogonal-additivity.md](../../../dag/derivations/independent/l1-imp-orthogonal-additivity.md)
- sha256 (`lf-normalised`): `01662431ac263370e0b508b2c904844d915710e6a4b18f149a9113801a03e38f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (2):

- `L1-R-ORTHOGONAL-ADDITIVITY-GAP` `GAP_NO_DERIVATION`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (PROVED_LEAN)
- `L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (PROVED_LEAN), [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) (PROVED_LEAN)

Outgoing (2):

- `L1-R-BORN-PAIRING-BOUNDARY` `DERIVED_LEAN`: [L1-QM122-BORN-PAIRING-NONUNIQUE](L1-QM122-BORN-PAIRING-NONUNIQUE.md) (PROVED_LEAN)
- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM6-P2-GLEASON](L1-QM020-THM6-P2-GLEASON.md) (IMPORTED_ASSUMPTION)
