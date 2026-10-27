# L1-IMP-ORTHOGONAL-ADDITIVITY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a sector-additive rational coefficient matrix, the sum of each off-diagonal pair is zero and the quadratic readout equals the sum of the diagonal squares. Symmetry of the matrix is a further hypothesis before each off-diagonal entry is zero. On the 2 by 2 integer matrix with entries 1, 1, -1 and 1, the off-diagonal pair sums to 0, neither off-diagonal entry is 0, and for every integer pair a, b the quadratic form equals a*a + b*b, which equals the sum of the forms on (a, 0) and (0, b). Probability additive on arbitrary orthogonal frames, and projection measures, stay supplied.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 13
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- distinct cited Lean declarations covered by a current replay receipt: 16
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

Sector additivity over disjoint supports gives off-diagonal pair-sum cancellation and the diagonal quadratic readout. Entrywise off-diagonal zero additionally requires symmetry; the complex Hermitian theorem uses Hermitian symmetry and both real and imaginary sector directions. Arbitrary orthogonal-frame additivity and projection-measure structure remain supplied. Earlier sector-form source and prior reviews remain cited.

## Review

- PFP review: [dag/research/pr440_statement_review_20261026.json](../../../dag/research/pr440_statement_review_20261026.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: The integer coefficient matrix \[\[1,1\],\[-1,1\]\] has nonzero off-diagonal entries whose sum is zero, and its quadratic form equals a*a+b*b and the sum of its two axis readouts for every integer a,b.
  - does not support: One nonsymmetric coefficient matrix; no Gram-matrix or arbitrary orthogonal-frame/projection-measure theorem. General sector additivity remains supplied. Entrywise off-diagonal zero needs symmetry (and in the Hermitian setting the stated real/imaginary sector hypotheses).
  - next test: Derive rather than assume arbitrary-frame probability additivity and the projection-measure hypotheses.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornPairingBoundary.lean`

- file: [lean4/BornPairingBoundary.lean](../../../lean4/BornPairingBoundary.lean)
- sha256 (`bytes`): `1a25c045a339b3b72e372dec8ea59683a40558820e302ab6f44bd0d8b518ee29`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornPairingBoundary`): recorded sha256 `1a25c045a339b3b72e372dec8ea59683a40558820e302ab6f44bd0d8b518ee29` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quartic_rival` | yes | yes | yes | propext | `#print axioms quartic_rival` |

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

### Lean: `lean4/FrameAdditivity.lean`

- file: [lean4/FrameAdditivity.lean](../../../lean4/FrameAdditivity.lean)
- sha256 (`bytes`): `206d6e450b91e9ae9c16b0e2ab305b735b5691215fe4ee185c111535f0fd89c3`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FrameAdditivity`): recorded sha256 `206d6e450b91e9ae9c16b0e2ab305b735b5691215fe4ee185c111535f0fd89c3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build FrameAdditivity`
- counts toward the grade: yes

### Lean: `lean4/HilbertWalkSameContract.lean`

- file: [lean4/HilbertWalkSameContract.lean](../../../lean4/HilbertWalkSameContract.lean)
- sha256 (`bytes`): `2eb51f295c76c23187d8f9edb6f0282199b1d867abe698b1cae2fe5a5d519d09`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `HilbertWalkSameContract`): recorded sha256 `2eb51f295c76c23187d8f9edb6f0282199b1d867abe698b1cae2fe5a5d519d09` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkSameContract`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_effect_rules_share_unit_total_and_disagree` | yes | yes | yes | Quot.sound, propext | `#print axioms two_effect_rules_share_unit_total_and_disagree` |

- counts toward the grade: yes

### Lean: `lean4/L1OrthogonalAdditivity.lean`

- file: [lean4/L1OrthogonalAdditivity.lean](../../../lean4/L1OrthogonalAdditivity.lean)
- sha256 (`bytes`): `d1efcb6a16253d9069632c564b0c5afdb7490adb5f5d6262a80653394e1f7555`
- cited in: node.lean, node.source, receipt dag/research/campaign_l1-imp-orthogonal-additivity_lean_replay.json (L1OrthogonalAdditivity), receipt dag/research/pr440_review_lean_replay.json (L1OrthogonalAdditivity)
- replay: `verified`
  - receipt [dag/research/campaign_l1-imp-orthogonal-additivity_lean_replay.json](../../../dag/research/campaign_l1-imp-orthogonal-additivity_lean_replay.json) (module `L1OrthogonalAdditivity`): recorded sha256 `d1efcb6a16253d9069632c564b0c5afdb7490adb5f5d6262a80653394e1f7555` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr440_review_lean_replay.json](../../../dag/research/pr440_review_lean_replay.json) (module `L1OrthogonalAdditivity`): recorded sha256 `d1efcb6a16253d9069632c564b0c5afdb7490adb5f5d6262a80653394e1f7555` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build L1OrthogonalAdditivity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `L1OrthogonalAdditivity.axisSum` | yes | yes | yes | propext | `#print axioms L1OrthogonalAdditivity.axisSum` |
| `L1OrthogonalAdditivity.entriesNotZero` | yes | yes | yes | none | `#print axioms L1OrthogonalAdditivity.entriesNotZero` |
| `L1OrthogonalAdditivity.negCross` | yes | yes | yes | propext | `#print axioms L1OrthogonalAdditivity.negCross` |
| `L1OrthogonalAdditivity.pairSum` | yes | yes | yes | none | `#print axioms L1OrthogonalAdditivity.pairSum` |
| `L1OrthogonalAdditivity.qf` | yes | yes | yes | none | `#print axioms L1OrthogonalAdditivity.qf` |
| `L1OrthogonalAdditivity.readout` | yes | yes | yes | propext | `#print axioms L1OrthogonalAdditivity.readout` |

- counts toward the grade: yes

### Lean: `lean4/SectorFormHermitian.lean`

- file: [lean4/SectorFormHermitian.lean](../../../lean4/SectorFormHermitian.lean)
- sha256 (`bytes`): `0aa46359b858583bc44444f0db0c56937ea1da8b464ee517a5b4ab1134abfce1`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `SectorFormHermitian`): recorded sha256 `0aa46359b858583bc44444f0db0c56937ea1da8b464ee517a5b4ab1134abfce1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SectorFormHermitian`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InnerProductFinite.HermitianSectorForm.imagLeak12_imag_direction_not_additive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_imag_direction_not_additive` |
| `InnerProductFinite.HermitianSectorForm.offdiag_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.HermitianSectorForm.offdiag_eq_zero` |

- counts toward the grade: yes

### Lean: `lean4/SectorFormUniqueness.lean`

- file: [lean4/SectorFormUniqueness.lean](../../../lean4/SectorFormUniqueness.lean)
- sha256 (`bytes`): `f8cf9b4ea79966f80a4d30fc5d4975aaf00b6ae6e282a8e58f5adf77185a8dde`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `SectorFormUniqueness`): recorded sha256 `f8cf9b4ea79966f80a4d30fc5d4975aaf00b6ae6e282a8e58f5adf77185a8dde` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SectorFormUniqueness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InnerProductFinite.SectorForm.eq_diagonal_of_sectorAdditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.SectorForm.eq_diagonal_of_sectorAdditive` |
| `InnerProductFinite.SectorForm.l1_disjoint_additive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.SectorForm.l1_disjoint_additive` |
| `InnerProductFinite.SectorForm.offdiag_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.SectorForm.offdiag_eq_zero` |
| `InnerProductFinite.SectorForm.offdiag_pair_sum_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.SectorForm.offdiag_pair_sum_eq_zero` |
| `InnerProductFinite.SectorForm.qf_eq_sum_diag_sq_of_sectorAdditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms InnerProductFinite.SectorForm.qf_eq_sum_diag_sq_of_sectorAdditive` |

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
- sha256 (`bytes`): `53301605a494e593942ec185a5e0fa8d9be8d6ce4faabf827ea7566ba433fd67`
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
- sha256 (`lf-normalised`): `966c3c7a5ee5448793a70c3d11d89099a9c99d4cd46297dfe516096ebd956889`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr440_review_lean_replay.json`

- file: [dag/research/pr440_review_lean_replay.json](../../../dag/research/pr440_review_lean_replay.json)
- sha256 (`lf-normalised`): `fbb77d98ed0c77c95ad0cca6e195494783ca4bfb25cc3749e970870988241a53`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr440_statement_review_20261026.json`

- file: [dag/research/pr440_statement_review_20261026.json](../../../dag/research/pr440_statement_review_20261026.json)
- sha256 (`lf-normalised`): `e536b9d41007d760488136eeb876eb840cdb5a14c3ee845e56c856ae3dd01e4f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (2):

- `L1-R-ORTHOGONAL-ADDITIVITY-GAP` `GAP_NO_DERIVATION`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (COMPUTATIONALLY_CHECKED), [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) (PROVED_LEAN)

Outgoing (2):

- `L1-R-BORN-PAIRING-BOUNDARY` `COMPUTED`: [L1-QM122-BORN-PAIRING-NONUNIQUE](L1-QM122-BORN-PAIRING-NONUNIQUE.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM6-P2-GLEASON](L1-QM020-THM6-P2-GLEASON.md) (IMPORTED_ASSUMPTION)
