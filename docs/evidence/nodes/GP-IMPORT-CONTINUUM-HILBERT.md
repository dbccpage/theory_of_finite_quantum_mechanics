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

### Lean: `lean4/ContinuumHilbertImport.lean`

- file: [lean4/ContinuumHilbertImport.lean](../../../lean4/ContinuumHilbertImport.lean)
- sha256 (`bytes`): `9e7afdeacea7f90b7280915b655a20aff4e66ea6ef902a2f8f91b66f883c1989`
- cited in: node.lean, receipt dag/research/campaign_gp-import-continuum-hilbert_lean_replay.json (ContinuumHilbertImport), record TFQ-1035
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-continuum-hilbert_lean_replay.json](../../../dag/research/campaign_gp-import-continuum-hilbert_lean_replay.json) (module `ContinuumHilbertImport`): recorded sha256 `9e7afdeacea7f90b7280915b655a20aff4e66ea6ef902a2f8f91b66f883c1989` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContinuumHilbertImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ContinuumHilbertImport.closedTail` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuumHilbertImport.closedTail` |
| `ContinuumHilbertImport.halves` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.halves` |
| `ContinuumHilbertImport.noPositiveDoubleOfOne` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuumHilbertImport.noPositiveDoubleOfOne` |
| `ContinuumHilbertImport.pow4Four` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.pow4Four` |
| `ContinuumHilbertImport.scaledTailIsOne` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuumHilbertImport.scaledTailIsOne` |
| `ContinuumHilbertImport.squareDiffs` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.squareDiffs` |
| `ContinuumHilbertImport.sumDiff` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuumHilbertImport.sumDiff` |
| `ContinuumHilbertImport.windowIsSum` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.windowIsSum` |
| `ContinuumHilbertImport.windowScaled` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.windowScaled` |
| `ContinuumHilbertImport.windowSquares` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.windowSquares` |
| `ContinuumHilbertImport.windowSum` | yes | yes | yes | none | `#print axioms ContinuumHilbertImport.windowSum` |

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

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1035_gp_import_continuum_hilbert.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1035_gp_import_continuum_hilbert.md](../../../dag/derivations/08_l1_to_l2/tfq_1035_gp_import_continuum_hilbert.md)
- sha256 (`lf-normalised`): `621842c9ace7081f690902b3b6bd9e725f9155584c993ae7413fbafbdb0900d5`
- generated view: listed, not counted
- cited in: record TFQ-1035
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-002`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:188`

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
