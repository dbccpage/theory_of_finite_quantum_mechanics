# GP-IMPORT-GLEASON

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the two-label host, 2 \< 3 and 3 ≤ 2 fails, and no three pairwise distinct labels exist. Amplitudes 2 on the false label and 1 on the true label have squared weights 4 and 1. The unit effect pairs both readout orders with 5. The false-indicator pairs as 4 in the direct order and as 1 after swapping the effect.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gleason hypotheses (noncontextuality, sigma-additivity, continuity): assumption
- dimension \>= 3: assumption

## Bottleneck

Uniqueness of the Born quadratic form for dimension at least 3, under noncontextuality, sigma-additivity and continuity, stays imported. The two-label disagreements do not refute that uniqueness under those hypotheses. Quartic readout under scale-2 frame additivity stays outside this slice.

## Source status

imported (OracleNeeded firewall, GTOC-8)

## Review

- PFP review: [dag/results/GP-IMPORT-GLEASON/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-GLEASON/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_two_label_pairing_reviewed`; scope effect `statement_narrowed`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: On the two-label host, 2 \< 3 and 3 ≤ 2 fails, and no three pairwise distinct labels exist. Amplitudes 2 on the false label and 1 on the true label have squared weights 4 and 1. The unit effect pairs both readout orders with 5. The false-indicator pairs as 4 in the direct order and as 1 after swapping the effect.
  - does not support: Uniqueness of the Born quadratic form for dimension at least 3 under noncontextuality, sigma-additivity and continuity, or a refutation of that uniqueness.
  - next test: Admit the Gleason hypotheses and a host with at least three labels before treating Born uniqueness as derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportGleason.lean`

- file: [lean4/CampaignGpImportGleason.lean](../../../lean4/CampaignGpImportGleason.lean)
- sha256 (`bytes`): `13a68c5bb1a92476960aa77de7ef1dd8dfe1a912ebc9ebb325fab5c1bbffa06a`
- cited in: node.lean, receipt dag/research/campaign_gp-import-gleason_lean_replay.json (CampaignGpImportGleason), record TFQ-1031
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-gleason_lean_replay.json](../../../dag/research/campaign_gp-import-gleason_lean_replay.json) (module `CampaignGpImportGleason`): recorded sha256 `13a68c5bb1a92476960aa77de7ef1dd8dfe1a912ebc9ebb325fab5c1bbffa06a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportGleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportGleason.dimensionExtraFails` | yes | yes | yes | none | `#print axioms CampaignGpImportGleason.dimensionExtraFails` |
| `CampaignGpImportGleason.falseIndicatorDisagrees` | yes | yes | yes | none | `#print axioms CampaignGpImportGleason.falseIndicatorDisagrees` |
| `CampaignGpImportGleason.noThreeDistinctLabels` | yes | yes | yes | none | `#print axioms CampaignGpImportGleason.noThreeDistinctLabels` |
| `CampaignGpImportGleason.squaredWeights` | yes | yes | yes | none | `#print axioms CampaignGpImportGleason.squaredWeights` |
| `CampaignGpImportGleason.twoLabelsBelowThree` | yes | yes | yes | none | `#print axioms CampaignGpImportGleason.twoLabelsBelowThree` |
| `CampaignGpImportGleason.unitPairingsAgree` | yes | yes | yes | none | `#print axioms CampaignGpImportGleason.unitPairingsAgree` |
| `dimensionExtraFails` | yes | yes | yes | none | `#print axioms dimensionExtraFails` |
| `falseIndicatorDisagrees` | yes | yes | yes | none | `#print axioms falseIndicatorDisagrees` |
| `noThreeDistinctLabels` | yes | yes | yes | none | `#print axioms noThreeDistinctLabels` |
| `squaredWeights` | yes | yes | yes | none | `#print axioms squaredWeights` |
| `twoLabelsBelowThree` | yes | yes | yes | none | `#print axioms twoLabelsBelowThree` |
| `unitPairingsAgree` | yes | yes | yes | none | `#print axioms unitPairingsAgree` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1031
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md](../../../dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md)
- sha256 (`lf-normalised`): `a91bd8a6b227bb738181b77c091de89fe44d578efa6229d26d244f8615b94771`
- generated view: listed, not counted
- cited in: record TFQ-1031
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
