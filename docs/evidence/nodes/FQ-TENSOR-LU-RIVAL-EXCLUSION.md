# FQ-TENSOR-LU-RIVAL-EXCLUSION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact tensor/right-Z and dump/right-Z arrays plus the genuine report-action non-descent witness are native/kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- bilinearity and local-unitary covariance requirements (assumption)
- two-label host Bool x Bool (assumption)

## Bottleneck

Unmet after the PFP review: Transport to the original abstract bilinear Kronecker interface, full local-unitary group and physical tensor/basis/inner-product admission. The rival counterexample alone does not derive the tensor product. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H062 / campaign C250 Block 05; ledger LEAN PROVED (RECEIPTED)

## Review

- PFP review: [dag/results/FQ-TENSOR-LU-RIVAL-EXCLUSION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-TENSOR-LU-RIVAL-EXCLUSION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact tensor/right-Z and dump/right-Z arrays plus the genuine report-action non-descent witness are native/kernel checked.
  - does not support: Transport to the original abstract bilinear Kronecker interface, full local-unitary group and physical tensor/basis/inner-product admission. The rival counterexample alone does not derive the tensor product.
  - next test: Transport to the original abstract bilinear Kronecker interface, full local-unitary group and physical tensor/basis/inner-product admission. The rival counterexample alone does not derive the tensor product.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/H014BilinearProduct.lean`

- file: [lean4/H014BilinearProduct.lean](../../../lean4/H014BilinearProduct.lean)
- sha256 (`bytes`): `fabd54a913240848de949fb629a744d82f0485b3a40aeba32fc1c39e55353cde`
- cited in: node.lean, record TFQ-1018
- replay: `none`
- check: `cd lean4 && lake build H014BilinearProduct`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bilinear_product_unique_on_bool_prod` | yes | yes | yes | - | `#print axioms bilinear_product_unique_on_bool_prod` |
- counts toward the grade: yes

### Lean: `lean4/H014Interface.lean`

- file: [lean4/H014Interface.lean](../../../lean4/H014Interface.lean)
- sha256 (`bytes`): `320a143feb167f7665d81508f191954b270d47bfc9a14fab1d51fe6428e0fba0`
- cited in: node.lean, record TFQ-1018
- replay: `none`
- check: `cd lean4 && lake build H014Interface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dumpRight_not_tensor` | yes | yes | yes | - | `#print axioms dumpRight_not_tensor` |
- counts toward the grade: yes

### Lean: `lean4/H062CompositionTensorMub.lean`

- file: [lean4/H062CompositionTensorMub.lean](../../../lean4/H062CompositionTensorMub.lean)
- sha256 (`bytes`): `b82630181e53bc72b003962d4b426d98c1967ba32127587195654231074d1cd2`
- cited in: node.lean, record TFQ-1018
- replay: `none`
- check: `cd lean4 && lake build H062CompositionTensorMub`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rival_fails_local_unitary_covariance` | yes | yes | yes | - | `#print axioms rival_fails_local_unitary_covariance` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/composition_quantum_bound.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/composition_quantum_bound.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1018
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/composition_tensor_mub.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/composition_tensor_mub.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1018
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1018_fq_tensor_lu_rival_exclusion.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1018_fq_tensor_lu_rival_exclusion.md](../../../dag/derivations/12_finite_qm_structure/tfq_1018_fq_tensor_lu_rival_exclusion.md)
- sha256 (`lf-normalised`): `2f47b408c3146f8e355539eb3c2c4e0f1114c8630e7d27b0e9e1c657c92768ad`
- generated view: listed, not counted
- cited in: record TFQ-1018
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-TENSOR-RIVAL` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `FQ-R-BELL-VIOLATION` `DERIVED_LEAN`: [FQ-BELL-RATIONAL-VIOLATION-14-5](FQ-BELL-RATIONAL-VIOLATION-14-5.md) (PROVED_LEAN)
- `FQ-R-GAP-TENSOR` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-TENSOR-UNIQUENESS](FQ-GAP-TENSOR-UNIQUENESS.md) (CONDITIONAL)
