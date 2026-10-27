# GP-IMPORT-GLEASON

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Uniqueness of the Born quadratic form at dimension n \>= 3 needs Gleason-type hypotheses (noncontextuality, sigma-additivity, continuity). On the two-label host the dimension extra already fails; the weaker unit-effect contract has two disagreeing pairings (4 versus 1 on the false-indicator at amplitudes (2,1)).

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

- PFP review: [dag/results/GP-IMPORT-GLEASON/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-GLEASON/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_two_label_pairing_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: On the two-label host, 2 \< 3 and 3 ≤ 2 fails, and no three pairwise distinct labels exist. Amplitudes 2 on the false label and 1 on the true label have squared weights 4 and 1. The unit effect pairs both readout orders with 5. The false-indicator pairs as 4 in the direct order and as 1 after swapping the effect.
  - does not support: Uniqueness of the Born quadratic form for dimension at least 3 under noncontextuality, sigma-additivity and continuity, or a refutation of that uniqueness.
  - next test: Admit the Gleason hypotheses and a host with at least three labels before treating Born uniqueness as derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GleasonImport.lean`

- file: [lean4/GleasonImport.lean](../../../lean4/GleasonImport.lean)
- sha256 (`bytes`): `1780f3c3039fcf145a0e05c4521be94eca2db8f76c4f0f588507efd776a9655a`
- cited in: node.lean, receipt dag/research/campaign_gp-import-gleason_lean_replay.json (GleasonImport), record TFQ-1031
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-gleason_lean_replay.json](../../../dag/research/campaign_gp-import-gleason_lean_replay.json) (module `GleasonImport`): recorded sha256 `1780f3c3039fcf145a0e05c4521be94eca2db8f76c4f0f588507efd776a9655a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build GleasonImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonImport.dimensionExtraFails` | yes | yes | yes | none | `#print axioms GleasonImport.dimensionExtraFails` |
| `GleasonImport.falseIndicatorDisagrees` | yes | yes | yes | none | `#print axioms GleasonImport.falseIndicatorDisagrees` |
| `GleasonImport.noThreeDistinctLabels` | yes | yes | yes | none | `#print axioms GleasonImport.noThreeDistinctLabels` |
| `GleasonImport.squaredWeights` | yes | yes | yes | none | `#print axioms GleasonImport.squaredWeights` |
| `GleasonImport.twoLabelsBelowThree` | yes | yes | yes | none | `#print axioms GleasonImport.twoLabelsBelowThree` |
| `GleasonImport.unitPairingsAgree` | yes | yes | yes | none | `#print axioms GleasonImport.unitPairingsAgree` |
| `dimensionExtraFails` | yes | yes | yes | none | `#print axioms dimensionExtraFails` |
| `falseIndicatorDisagrees` | yes | yes | yes | none | `#print axioms falseIndicatorDisagrees` |
| `noThreeDistinctLabels` | yes | yes | yes | none | `#print axioms noThreeDistinctLabels` |
| `squaredWeights` | yes | yes | yes | none | `#print axioms squaredWeights` |
| `twoLabelsBelowThree` | yes | yes | yes | none | `#print axioms twoLabelsBelowThree` |
| `unitPairingsAgree` | yes | yes | yes | none | `#print axioms unitPairingsAgree` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md](../../../dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md)
- sha256 (`lf-normalised`): `156162fed5a0d7528929b145bc0fc7cc1083f25d1898782ddf8ca8f2b47f4caa`
- generated view: listed, not counted
- cited in: record TFQ-1031
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-004`
- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-010`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:a635008d68c51a062b794996dc85a68693522928a157d619d01ffada1ba595f1#PRICE-HD-05`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:153`

## Routes

Incoming (0):


Outgoing (1):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)

No incoming route.
