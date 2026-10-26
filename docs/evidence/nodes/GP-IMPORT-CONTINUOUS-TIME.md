# GP-IMPORT-CONTINUOUS-TIME

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuous time, topology, a one-parameter unitary group and Stone's theorem. The two-state toggle has no report-level square root; after complex coefficients, interpolants exist at scale 4 and are not unique.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuous time: assumption
- topology on the carrier: assumption
- one-parameter group: assumption
- Stone's theorem: import

## Bottleneck

Continuous time, a topology, a one-parameter unitary group and Stone's theorem stay imported. The Boolean toggle and the two Gaussian-integer interpolants at scale 4 are one finite case. A rational Cayley transform and a hyperoctahedral residue stay outside this case.

## Source status

imported / refused on this host

## Review

- PFP review: [dag/results/GP-IMPORT-CONTINUOUS-TIME/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CONTINUOUS-TIME/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Complete Boolean square-root obstruction and both exact complex unitary square roots of toggle; generic projector-square algebra and Boolean enumeration in Lean.
  - does not support: Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics.
  - next test: Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportContinuousTime.lean`

- file: [lean4/CampaignGpImportContinuousTime.lean](../../../lean4/CampaignGpImportContinuousTime.lean)
- sha256 (`bytes`): `efc118c4a3ef4ec32ac5fdad45c4b4db15e393cc2298e84156076b31eeaaf7b1`
- cited in: node.lean, receipt dag/research/campaign_gp-import-continuous-time_lean_replay.json (CampaignGpImportContinuousTime), record TFQ-1034
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-continuous-time_lean_replay.json](../../../dag/research/campaign_gp-import-continuous-time_lean_replay.json) (module `CampaignGpImportContinuousTime`): recorded sha256 `efc118c4a3ef4ec32ac5fdad45c4b4db15e393cc2298e84156076b31eeaaf7b1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportContinuousTime`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportContinuousTime.gAdd_coords` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.gAdd_coords` |
| `CampaignGpImportContinuousTime.gMul_coords` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.gMul_coords` |
| `CampaignGpImportContinuousTime.interpNeg_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportContinuousTime.interpNeg_twice_is_scaled_swap` |
| `CampaignGpImportContinuousTime.interp_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportContinuousTime.interp_twice_is_scaled_swap` |
| `CampaignGpImportContinuousTime.interpolants_differ` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.interpolants_differ` |
| `CampaignGpImportContinuousTime.no_toggle_square_root` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.no_toggle_square_root` |
| `CampaignGpImportContinuousTime.scale4_swap` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.scale4_swap` |
| `CampaignGpImportContinuousTime.swap_exchanges` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.swap_exchanges` |
| `CampaignGpImportContinuousTime.toggle_images` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.toggle_images` |
| `CampaignGpImportContinuousTime.witness_interp` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.witness_interp` |
| `CampaignGpImportContinuousTime.witness_neg` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuousTime.witness_neg` |
| `gAdd_coords` | yes | yes | yes | none | `#print axioms gAdd_coords` |
| `gMul_coords` | yes | yes | yes | none | `#print axioms gMul_coords` |
| `interpNeg_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms interpNeg_twice_is_scaled_swap` |
| `interp_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms interp_twice_is_scaled_swap` |
| `interpolants_differ` | yes | yes | yes | none | `#print axioms interpolants_differ` |
| `no_toggle_square_root` | yes | yes | yes | none | `#print axioms no_toggle_square_root` |
| `scale4_swap` | yes | yes | yes | none | `#print axioms scale4_swap` |
| `swap_exchanges` | yes | yes | yes | none | `#print axioms swap_exchanges` |
| `toggle_images` | yes | yes | yes | none | `#print axioms toggle_images` |
| `witness_interp` | yes | yes | yes | none | `#print axioms witness_interp` |
| `witness_neg` | yes | yes | yes | none | `#print axioms witness_neg` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1034
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` |

- counts toward the grade: yes

### Lean: `lean4/H016ContinuousDynamicsFork.lean`

- file: [lean4/H016ContinuousDynamicsFork.lean](../../../lean4/H016ContinuousDynamicsFork.lean)
- sha256 (`bytes`): `906b145d8626c1887b1075e9b900858ca3f0c16df6fa65a2d8a87aa68b06de85`
- cited in: node.lean, record TFQ-1034
- replay: `none`
- check: `cd lean4 && lake build H016ContinuousDynamicsFork`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `toggle` | yes | yes | no | - | `#print axioms toggle` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1034
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md](../../../dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md)
- sha256 (`lf-normalised`): `07a5e5f6f3642cdf9b0534bc4752443b5dbf8be07f8d2b12b75d122917b8e41a`
- generated view: listed, not counted
- cited in: record TFQ-1034
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/continuum_price_ledger.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/continuum_price_ledger.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (2):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
