# GP-IMPORT-TENSOR-PRODUCT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Hilbert tensor product as the unique way to combine systems. On Bool x Bool a bilinear integer-homogeneous Kronecker-normalized map equals the pointwise product; a weaker same-host combining interface has a rival (dump-the-right-report map).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 27
- distinct cited Lean declarations covered by a current replay receipt: 15
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

### Lean: `lean4/BilinearProduct.lean`

- file: [lean4/BilinearProduct.lean](../../../lean4/BilinearProduct.lean)
- sha256 (`bytes`): `4f8a0b0fa545b236994c9500ea184e2e9dc5b23432a2052bc55af8fa1313e194`
- cited in: node.lean, record TFQ-1032
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `BilinearProduct`): recorded sha256 `4f8a0b0fa545b236994c9500ea184e2e9dc5b23432a2052bc55af8fa1313e194` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BilinearProduct`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `embed_eq_tensor` | yes | yes | yes | module-level | `#print axioms embed_eq_tensor` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1032
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/HilbertWalkInterface.lean`

- file: [lean4/HilbertWalkInterface.lean](../../../lean4/HilbertWalkInterface.lean)
- sha256 (`bytes`): `7c3e814fb15d303798bd5e66baddec08ede2033a7471e83f03bb178e7a2eb9c5`
- cited in: node.lean, record TFQ-1032
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `HilbertWalkInterface`): recorded sha256 `7c3e814fb15d303798bd5e66baddec08ede2033a7471e83f03bb178e7a2eb9c5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkInterface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_combinings_share_interface_and_disagree` | yes | yes | yes | module-level | `#print axioms two_combinings_share_interface_and_disagree` |

- counts toward the grade: yes

### Lean: `lean4/TensorProductImport.lean`

- file: [lean4/TensorProductImport.lean](../../../lean4/TensorProductImport.lean)
- sha256 (`bytes`): `ea58fdf4e63eb852f70a055f047a8ba8712236346847b1fa45582e5879731246`
- cited in: node.lean, receipt dag/research/campaign_gp-import-tensor-product_lean_replay.json (TensorProductImport), record TFQ-1032
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-tensor-product_lean_replay.json](../../../dag/research/campaign_gp-import-tensor-product_lean_replay.json) (module `TensorProductImport`): recorded sha256 `ea58fdf4e63eb852f70a055f047a8ba8712236346847b1fa45582e5879731246` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorProductImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `TensorProductImport.dumpRight_add_left` | yes | yes | yes | propext | `#print axioms TensorProductImport.dumpRight_add_left` |
| `TensorProductImport.dumpRight_add_right` | yes | yes | yes | Quot.sound, propext | `#print axioms TensorProductImport.dumpRight_add_right` |
| `TensorProductImport.dumpRight_collapsed_tag` | yes | yes | yes | propext | `#print axioms TensorProductImport.dumpRight_collapsed_tag` |
| `TensorProductImport.dumpRight_false_coord` | yes | yes | yes | none | `#print axioms TensorProductImport.dumpRight_false_coord` |
| `TensorProductImport.dumpRight_ne_tensor` | yes | yes | yes | propext | `#print axioms TensorProductImport.dumpRight_ne_tensor` |
| `TensorProductImport.dumpRight_smul_left` | yes | yes | yes | propext | `#print axioms TensorProductImport.dumpRight_smul_left` |
| `TensorProductImport.dumpRight_smul_right` | yes | yes | yes | propext | `#print axioms TensorProductImport.dumpRight_smul_right` |
| `TensorProductImport.dumpRight_true_coord` | yes | yes | yes | none | `#print axioms TensorProductImport.dumpRight_true_coord` |
| `TensorProductImport.embed_eq_tensor` | yes | yes | yes | Quot.sound, propext | `#print axioms TensorProductImport.embed_eq_tensor` |
| `TensorProductImport.tensor_pointwise` | yes | yes | yes | none | `#print axioms TensorProductImport.tensor_pointwise` |
| `TensorProductImport.witness_dump_zero` | yes | yes | yes | none | `#print axioms TensorProductImport.witness_dump_zero` |
| `TensorProductImport.witness_tensor_one` | yes | yes | yes | propext | `#print axioms TensorProductImport.witness_tensor_one` |
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
- sha256 (`lf-normalised`): `f80b444e3e5a7d5a23870ff15dc21c0ce8d861b4408538757d61e091adfdd005`
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
