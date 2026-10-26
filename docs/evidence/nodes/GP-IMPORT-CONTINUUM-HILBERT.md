# GP-IMPORT-CONTINUUM-HILBERT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Transition from the finite presented carrier (integer weights, finite report labels) to a continuous infinite-dimensional Hilbert space. QM_122 section 6 refuses it; QM_020 demotion box fences it.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- distinct cited Lean declarations covered by a current replay receipt: 13
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- infinite-dimensional Hilbert space: lift
- metric completion: lift

## Bottleneck

The transition from a finite presented carrier, with integer weights and finite report labels, to a continuous infinite-dimensional Hilbert space stays imported. Scalar-field selection, l2 uniformity, a verified topology, a Cauchy completion and the lift of bounded exact operators stay imported. The completion record sits at FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION (runs 20261020T230000Z_completion and 20261021T003000Z_lift_steps). QM_122 section 6 refuses that transition, and the QM_020 demotion box fences it. The length-4 window and the finite power-of-four identity are one finite case.

## Source status

OPEN gap GAP-F001-S000-002 (continuum interface)

## Review

- PFP review: [dag/results/GP-IMPORT-CONTINUUM-HILBERT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CONTINUUM-HILBERT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact truncation coordinates, norm, positive tail and successive difference controls; general finite recurrence identity and positivity interface in Lean.
  - does not support: Construct and verify the topology, Cauchy completion and infinite-dimensional Hilbert carrier. No finite truncation settles those imports.
  - next test: Construct and verify the topology, Cauchy completion and infinite-dimensional Hilbert carrier. No finite truncation settles those imports.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportContinuumHilbert.lean`

- file: [lean4/CampaignGpImportContinuumHilbert.lean](../../../lean4/CampaignGpImportContinuumHilbert.lean)
- sha256 (`bytes`): `c295d54bb448053163b2de830650a5724201901cb8b4f00e1a3c70418524e965`
- cited in: node.lean, receipt dag/research/campaign_gp-import-continuum-hilbert_lean_replay.json (CampaignGpImportContinuumHilbert), record TFQ-1035
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-continuum-hilbert_lean_replay.json](../../../dag/research/campaign_gp-import-continuum-hilbert_lean_replay.json) (module `CampaignGpImportContinuumHilbert`): recorded sha256 `c295d54bb448053163b2de830650a5724201901cb8b4f00e1a3c70418524e965` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportContinuumHilbert`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportContinuumHilbert.closedTail` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportContinuumHilbert.closedTail` |
| `CampaignGpImportContinuumHilbert.halves` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.halves` |
| `CampaignGpImportContinuumHilbert.noPositiveDoubleOfOne` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportContinuumHilbert.noPositiveDoubleOfOne` |
| `CampaignGpImportContinuumHilbert.pow4Four` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.pow4Four` |
| `CampaignGpImportContinuumHilbert.scaledTailIsOne` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportContinuumHilbert.scaledTailIsOne` |
| `CampaignGpImportContinuumHilbert.squareDiffs` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.squareDiffs` |
| `CampaignGpImportContinuumHilbert.sumDiff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportContinuumHilbert.sumDiff` |
| `CampaignGpImportContinuumHilbert.windowIsSum` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.windowIsSum` |
| `CampaignGpImportContinuumHilbert.windowScaled` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.windowScaled` |
| `CampaignGpImportContinuumHilbert.windowSquares` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.windowSquares` |
| `CampaignGpImportContinuumHilbert.windowSum` | yes | yes | yes | none | `#print axioms CampaignGpImportContinuumHilbert.windowSum` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1035
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1035
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1035_gp_import_continuum_hilbert.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1035_gp_import_continuum_hilbert.md](../../../dag/derivations/08_l1_to_l2/tfq_1035_gp_import_continuum_hilbert.md)
- sha256 (`lf-normalised`): `97f91be837764652ab1542bb8619f2cf079ec1083ee845bac40074ce489470dd`
- generated view: listed, not counted
- cited in: record TFQ-1035
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


Outgoing (0):


No incoming route.
