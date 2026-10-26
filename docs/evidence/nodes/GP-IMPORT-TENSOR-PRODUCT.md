# GP-IMPORT-TENSOR-PRODUCT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Hilbert tensor product as the unique way to combine systems. On Bool x Bool a bilinear integer-homogeneous Kronecker-normalized map equals the pointwise product; a weaker same-host combining interface has a rival (dump-the-right-report map).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- tensor product combining rule: assumption

## Bottleneck

The Hilbert-space tensor product is not derived as the unique way to combine systems. The agreement above uses additivity, integer homogeneity and the identity tag (i, j) on one Bool-by-Bool host. The dump-right map is a same-host rival whose tag collapses the second Boolean factor, so a weaker tag does not select the pointwise product. A second presented carrier and a physical composition rule stay imported (QM_122 7.1 item 1).

## Source status

imported; unique only on the named bilinear Kronecker interface

## Review

- PFP review: [dag/results/GP-IMPORT-TENSOR-PRODUCT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-TENSOR-PRODUCT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact tensor/dumpRight and norm-multiplicativity arrays, with generic bilinearity and a basis-collision control in Lean.
  - does not support: Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product.
  - next test: Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportTensorProduct.lean`

- file: [lean4/CampaignGpImportTensorProduct.lean](../../../lean4/CampaignGpImportTensorProduct.lean)
- sha256 (`bytes`): `5d83a84e8099d4d38e989378b276244c701c6bbfe31aab4c78171d09e5277a42`
- cited in: node.lean, receipt dag/research/campaign_gp-import-tensor-product_lean_replay.json (CampaignGpImportTensorProduct), record TFQ-1032
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-tensor-product_lean_replay.json](../../../dag/research/campaign_gp-import-tensor-product_lean_replay.json) (module `CampaignGpImportTensorProduct`): recorded sha256 `5d83a84e8099d4d38e989378b276244c701c6bbfe31aab4c78171d09e5277a42` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportTensorProduct`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportTensorProduct.dumpRight_add_left` | yes | yes | yes | propext | `#print axioms CampaignGpImportTensorProduct.dumpRight_add_left` |
| `CampaignGpImportTensorProduct.dumpRight_add_right` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportTensorProduct.dumpRight_add_right` |
| `CampaignGpImportTensorProduct.dumpRight_collapsed_tag` | yes | yes | yes | propext | `#print axioms CampaignGpImportTensorProduct.dumpRight_collapsed_tag` |
| `CampaignGpImportTensorProduct.dumpRight_false_coord` | yes | yes | yes | none | `#print axioms CampaignGpImportTensorProduct.dumpRight_false_coord` |
| `CampaignGpImportTensorProduct.dumpRight_ne_tensor` | yes | yes | yes | propext | `#print axioms CampaignGpImportTensorProduct.dumpRight_ne_tensor` |
| `CampaignGpImportTensorProduct.dumpRight_smul_left` | yes | yes | yes | propext | `#print axioms CampaignGpImportTensorProduct.dumpRight_smul_left` |
| `CampaignGpImportTensorProduct.dumpRight_smul_right` | yes | yes | yes | propext | `#print axioms CampaignGpImportTensorProduct.dumpRight_smul_right` |
| `CampaignGpImportTensorProduct.dumpRight_true_coord` | yes | yes | yes | none | `#print axioms CampaignGpImportTensorProduct.dumpRight_true_coord` |
| `CampaignGpImportTensorProduct.embed_eq_tensor` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportTensorProduct.embed_eq_tensor` |
| `CampaignGpImportTensorProduct.tensor_pointwise` | yes | yes | yes | none | `#print axioms CampaignGpImportTensorProduct.tensor_pointwise` |
| `CampaignGpImportTensorProduct.witness_dump_zero` | yes | yes | yes | none | `#print axioms CampaignGpImportTensorProduct.witness_dump_zero` |
| `CampaignGpImportTensorProduct.witness_tensor_one` | yes | yes | yes | propext | `#print axioms CampaignGpImportTensorProduct.witness_tensor_one` |
| `dumpRight_add_left` | yes | yes | yes | propext | `#print axioms dumpRight_add_left` |
| `dumpRight_add_right` | yes | yes | yes | Quot.sound, propext | `#print axioms dumpRight_add_right` |
| `dumpRight_collapsed_tag` | yes | yes | yes | propext | `#print axioms dumpRight_collapsed_tag` |
| `dumpRight_false_coord` | yes | yes | yes | none | `#print axioms dumpRight_false_coord` |
| `dumpRight_ne_tensor` | yes | yes | yes | propext | `#print axioms dumpRight_ne_tensor` |
| `dumpRight_smul_left` | yes | yes | yes | propext | `#print axioms dumpRight_smul_left` |
| `dumpRight_smul_right` | yes | yes | yes | propext | `#print axioms dumpRight_smul_right` |
| `dumpRight_true_coord` | yes | yes | yes | none | `#print axioms dumpRight_true_coord` |
| `embed_eq_tensor` | yes | yes | yes | Quot.sound, propext | `#print axioms embed_eq_tensor` |
| `tensor_pointwise` | yes | yes | yes | none | `#print axioms tensor_pointwise` |
| `witness_dump_zero` | yes | yes | yes | none | `#print axioms witness_dump_zero` |
| `witness_tensor_one` | yes | yes | yes | propext | `#print axioms witness_tensor_one` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1032
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1032_gp_import_tensor_product.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1032_gp_import_tensor_product.md](../../../dag/derivations/08_l1_to_l2/tfq_1032_gp_import_tensor_product.md)
- sha256 (`lf-normalised`): `cf8bee3ea5b4ae34f451543aef1586ef81fb5abb41c22a43c2806a49a43bc4c9`
- generated view: listed, not counted
- cited in: record TFQ-1032
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


Outgoing (3):

- `APP-R-MUB6-QUHEX-TENSOR-CARRIER` `DERIVED_PROSE`: [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION)
- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
