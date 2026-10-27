# FQ-TENSOR-LU-RIVAL-EXCLUSION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On Bool x Bool a bilinear, integer-homogeneous, Kronecker-normalized combining rule equals the pointwise product (bilinear_product_unique_on_bool_prod); the weaker interface has a dump-the-right-report rival u boxtimes v = (\<0|v\>+\<1|v\>) u, which fails local-unitary covariance (rival_fails_local_unitary_covariance).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- bilinearity and local-unitary covariance requirements (assumption)
- two-label host Bool x Bool (assumption)

## Bottleneck

Stated in BilinearProduct.lean, HilbertWalkInterface.lean and CompositionTensorMub.lean. The setting is two Boolean factors; larger factor sets are not covered.

## Source status

H062 / campaign C250 Block 05; ledger LEAN PROVED (RECEIPTED)

## Review

- PFP review: [dag/results/FQ-TENSOR-LU-RIVAL-EXCLUSION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-TENSOR-LU-RIVAL-EXCLUSION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact tensor/right-Z and dump/right-Z arrays plus the genuine report-action non-descent witness are native/kernel checked.
  - does not support: Transport to the original abstract bilinear Kronecker interface, full local-unitary group and physical tensor/basis/inner-product admission. The rival counterexample alone does not derive the tensor product.
  - next test: Transport to the original abstract bilinear Kronecker interface, full local-unitary group and physical tensor/basis/inner-product admission. The rival counterexample alone does not derive the tensor product.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BilinearProduct.lean`

- file: [lean4/BilinearProduct.lean](../../../lean4/BilinearProduct.lean)
- sha256 (`bytes`): `4f8a0b0fa545b236994c9500ea184e2e9dc5b23432a2052bc55af8fa1313e194`
- cited in: node.lean, record TFQ-1018
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `BilinearProduct`): recorded sha256 `4f8a0b0fa545b236994c9500ea184e2e9dc5b23432a2052bc55af8fa1313e194` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BilinearProduct`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bilinear_product_unique_on_bool_prod` | yes | yes | yes | Quot.sound, propext | `#print axioms bilinear_product_unique_on_bool_prod` |

- counts toward the grade: yes

### Lean: `lean4/CompositionTensorMub.lean`

- file: [lean4/CompositionTensorMub.lean](../../../lean4/CompositionTensorMub.lean)
- sha256 (`bytes`): `eb8f9a7cb10a07586df55ac8f5ca3eb8fda3f059dcff1bef1e80de645542dd42`
- cited in: node.lean, record TFQ-1018
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `CompositionTensorMub`): recorded sha256 `eb8f9a7cb10a07586df55ac8f5ca3eb8fda3f059dcff1bef1e80de645542dd42` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CompositionTensorMub`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rival_fails_local_unitary_covariance` | yes | yes | yes | none | `#print axioms rival_fails_local_unitary_covariance` |

- counts toward the grade: yes

### Lean: `lean4/HilbertWalkInterface.lean`

- file: [lean4/HilbertWalkInterface.lean](../../../lean4/HilbertWalkInterface.lean)
- sha256 (`bytes`): `7c3e814fb15d303798bd5e66baddec08ede2033a7471e83f03bb178e7a2eb9c5`
- cited in: node.lean, record TFQ-1018
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `HilbertWalkInterface`): recorded sha256 `7c3e814fb15d303798bd5e66baddec08ede2033a7471e83f03bb178e7a2eb9c5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkInterface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dumpRight_not_tensor` | yes | yes | yes | Quot.sound, propext | `#print axioms dumpRight_not_tensor` |

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
- sha256 (`lf-normalised`): `41c856043726ec5c04ba347ed6b73f06998a7790b897f9d2d13e54ed62a73d2e`
- generated view: listed, not counted
- cited in: record TFQ-1018
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-TENSOR-RIVAL` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `FQ-R-BELL-VIOLATION` `COMPUTED`: [FQ-BELL-RATIONAL-VIOLATION-14-5](FQ-BELL-RATIONAL-VIOLATION-14-5.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-GAP-TENSOR` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-TENSOR-UNIQUENESS](FQ-GAP-TENSOR-UNIQUENESS.md) (CONDITIONAL)
