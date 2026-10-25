# GP-IMPORT-CIRCLE-U1

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Each sign squares to 1. The pairs (1, 1) and (1, -1) differ, and each of their coordinates is a sign. The integer pair 0, 1 has square norm 1, and the product of that pair with itself is the pair -1, 0, which differs from the pair 1, 0. The map sending 0 to 1, 1 to 2 and 2 to 0 returns 2 at the second step from 0 and returns 0 at the third step from 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- U(1) phase group: assumption
- continuity of one-parameter phase group: assumption

## Bottleneck

The circle group U(1) and continuity of a one-parameter phase group stay hypotheses. The selector for that circle stays imported.

## Source status

imported; sign group excluded only under an extra

## Review

- PFP review: [dag/results/GP-IMPORT-CIRCLE-U1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CIRCLE-U1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Complete C2/C3/C4 group tables, exponent-two controls and sign-interference values, plus exact cyclic controls in Lean.
  - does not support: A circle group, topology and continuous one-parameter action remain extra hypotheses. Finite alternatives do not select U(1).
  - next test: A circle group, topology and continuous one-parameter action remain extra hypotheses. Finite alternatives do not select U(1).

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportCircleU1.lean`

- file: [lean4/CampaignGpImportCircleU1.lean](../../../lean4/CampaignGpImportCircleU1.lean)
- sha256 (`bytes`): `ee2379460eece0f18f28d6603f4e411a008537cb7983e39e3b40d0a3061adbd7`
- cited in: node.lean, receipt dag/research/campaign_gp-import-circle-u1_lean_replay.json (CampaignGpImportCircleU1), record TFQ-1030
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-circle-u1_lean_replay.json](../../../dag/research/campaign_gp-import-circle-u1_lean_replay.json) (module `CampaignGpImportCircleU1`): recorded sha256 `ee2379460eece0f18f28d6603f4e411a008537cb7983e39e3b40d0a3061adbd7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportCircleU1`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportCircleU1.cycThrice` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.cycThrice` |
| `CampaignGpImportCircleU1.cycTwice` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.cycTwice` |
| `CampaignGpImportCircleU1.iNorm` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.iNorm` |
| `CampaignGpImportCircleU1.iSquare` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.iSquare` |
| `CampaignGpImportCircleU1.iSquareNeOne` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.iSquareNeOne` |
| `CampaignGpImportCircleU1.pairCoordsAreSigns` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.pairCoordsAreSigns` |
| `CampaignGpImportCircleU1.pairsDiffer` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.pairsDiffer` |
| `CampaignGpImportCircleU1.signSquare` | yes | yes | yes | none | `#print axioms CampaignGpImportCircleU1.signSquare` |
| `cycThrice` | yes | yes | yes | none | `#print axioms cycThrice` |
| `cycTwice` | yes | yes | yes | none | `#print axioms cycTwice` |
| `iNorm` | yes | yes | yes | none | `#print axioms iNorm` |
| `iSquare` | yes | yes | yes | none | `#print axioms iSquare` |
| `iSquareNeOne` | yes | yes | yes | none | `#print axioms iSquareNeOne` |
| `pairCoordsAreSigns` | yes | yes | yes | none | `#print axioms pairCoordsAreSigns` |
| `pairsDiffer` | yes | yes | yes | none | `#print axioms pairsDiffer` |
| `signSquare` | yes | yes | yes | none | `#print axioms signSquare` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1030
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1030_gp_import_circle_u1.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1030_gp_import_circle_u1.md](../../../dag/derivations/08_l1_to_l2/tfq_1030_gp_import_circle_u1.md)
- sha256 (`lf-normalised`): `c37413a900d0a57ff15b62e1dafef041bfd9ae79e7bb9123f4a25e0936736bb3`
- generated view: listed, not counted
- cited in: record TFQ-1030
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


Outgoing (1):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)

No incoming route.
