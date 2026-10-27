# FQ-GAP-TENSOR-UNIQUENESS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> General finite-dimensional quantum composition follows from supplied local complex QM, independent preparation and testing, local tomography, local unitaries, and a fully calibrated reversible controlled shift. The state and generated effect cones are PSD; full effect and POVM availability has explicit saturation assumptions. Primitive difference has not supplied these operational premises. On integer coefficients, every 2 by 2 outer product of two vectors has determinant 0, and the matrix with entries 1, 0, 0 and 1 has determinant 1, so that matrix is not an outer product of two integer vectors.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 13
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- local finite complex quantum state and effect spaces with trace probabilities
- independent preparation, testing and convex composition
- local tomography
- all local unitary operations
- fully coherently calibrated reversible controlled shift
- effect and finite-test saturation for full measurement availability

## Bottleneck

The state and measurement corollaries are verified under their stated operational hypotheses. Deriving local complex QM, tomography, calibrated reversible interactions and both saturation assumptions from primitive difference remains conditional. The integer determinant split separates the matrix with entries 1, 0, 0 and 1 from the outer products of integer vectors. It does not select a tensor product, compare state or effect cones, or discharge the operational premises. AuthorityEffect: None.

## Source status

The 20261019 scope audit remains a determinant obstruction on a supplied rational host. TFQ-0410--TFQ-0412 verify general Lean tomography, Schmidt reachability and operational state-cone reconstruction. TFQ-0414--TFQ-0416 verify the generated effect cone, saturated binary interval and finite POVM corollaries. TFQ-0413 verifies assumption countermodels in Lean: full-cone duality, all-dimension cone separations, exact two-qubit calibration failures and hidden-coordinate tomography failure; external classification and primitive selection remain outside scope.

## Review

- PFP review: [dag/research/pr442_statement_review_20261026.json](../../../dag/research/pr442_statement_review_20261026.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Every 2 by 2 outer product of integer vectors has determinant zero; the identity matrix has determinant one and is not such an outer product.
  - does not support: This integer coefficient-matrix obstruction does not select a tensor product or establish state/effect-cone reconstruction. Previously verified conditional reconstruction and measurement results remain separately cited; local complex QM, tomography, calibrated reversible interactions and saturation hypotheses remain supplied.
  - next test: Derive the supplied operational hypotheses from primitive difference; do not replace the existing conditional reconstruction with this finite obstruction.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1019
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_tensor_uniqueness_min_vs_max_tensor_and_covariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_tensor_uniqueness_min_vs_max_tensor_and_covariance` |

- counts toward the grade: yes

### Lean: `lean4/TensorUniquenessOuterProducts.lean`

- file: [lean4/TensorUniquenessOuterProducts.lean](../../../lean4/TensorUniquenessOuterProducts.lean)
- sha256 (`bytes`): `704f7257117a184fde850bb9fe6ff1c9d642db392ff75379b2b0f50806b0e43c`
- cited in: node.lean, node.source, receipt dag/research/campaign_fq-gap-tensor-uniqueness_lean_replay.json (TensorUniquenessOuterProducts), receipt dag/research/pr442_review_lean_replay.json (TensorUniquenessOuterProducts), record TFQ-1019
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-tensor-uniqueness_lean_replay.json](../../../dag/research/campaign_fq-gap-tensor-uniqueness_lean_replay.json) (module `TensorUniquenessOuterProducts`): recorded sha256 `704f7257117a184fde850bb9fe6ff1c9d642db392ff75379b2b0f50806b0e43c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr442_review_lean_replay.json](../../../dag/research/pr442_review_lean_replay.json) (module `TensorUniquenessOuterProducts`): recorded sha256 `704f7257117a184fde850bb9fe6ff1c9d642db392ff75379b2b0f50806b0e43c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorUniquenessOuterProducts`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `TensorUniquenessOuterProducts.det` | yes | yes | yes | none | `#print axioms TensorUniquenessOuterProducts.det` |
| `TensorUniquenessOuterProducts.identityDet` | yes | yes | yes | propext | `#print axioms TensorUniquenessOuterProducts.identityDet` |
| `TensorUniquenessOuterProducts.identityNotOuter` | yes | yes | yes | propext | `#print axioms TensorUniquenessOuterProducts.identityNotOuter` |
| `TensorUniquenessOuterProducts.outerDet` | yes | yes | yes | propext | `#print axioms TensorUniquenessOuterProducts.outerDet` |
| `TensorUniquenessOuterProducts.productsEq` | yes | yes | yes | propext | `#print axioms TensorUniquenessOuterProducts.productsEq` |

- counts toward the grade: yes

### Python: `checks/independent/fq-gap-tensor-uniqueness.py`

- file: [checks/independent/fq-gap-tensor-uniqueness.py](../../../checks/independent/fq-gap-tensor-uniqueness.py)
- sha256 (`bytes`): `594234df43a5586a86eb7032972338e3111d6f7bb0d628668a905bf0aa6786b4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md](../../../dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md)
- sha256 (`lf-normalised`): `4f0b039232e8a52f9cbc1ad8ecb3902e3921c4dc8f5d469b180b155d1600426b`
- generated view: listed, not counted
- cited in: record TFQ-1019
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md`

- file: [dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md](../../../dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md)
- sha256 (`lf-normalised`): `3dd28ec9850c6667c6b8ca677516507f3a56667b03d264c225f3b5056b7b2a34`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`

- file: [dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md](../../../dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md)
- sha256 (`lf-normalised`): `3d1f897722aad08811a52c863e8bc47cfda41d9d087929a00c3925f4782de12f`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md`

- file: [dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md](../../../dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md)
- sha256 (`lf-normalised`): `126de574698271544d28d12fda6f87f088637b5f3b4cf0ddd0aa6a974362cc02`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md`

- file: [dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md](../../../dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md)
- sha256 (`lf-normalised`): `2c5fb04175f367a1d58477d317882002336577f65d895226c9ab4bc01eb9377a`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md`

- file: [dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md](../../../dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md)
- sha256 (`lf-normalised`): `db945ab62338d7c0037b8c012ad05d4c893694524faf0397ac79ffee4ddda4e9`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fq-gap-tensor-uniqueness.md`

- file: [dag/derivations/independent/fq-gap-tensor-uniqueness.md](../../../dag/derivations/independent/fq-gap-tensor-uniqueness.md)
- sha256 (`lf-normalised`): `04eb1d6dc825b1a3232910843d1dc5c132ec230a8a1b7b9c32fa1f91ff6af1bb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fq-gap-tensor-uniqueness_lean_replay.json`

- file: [dag/research/campaign_fq-gap-tensor-uniqueness_lean_replay.json](../../../dag/research/campaign_fq-gap-tensor-uniqueness_lean_replay.json)
- sha256 (`lf-normalised`): `d5c2ce6d0f8f44b64c52a6e3f02149de0a93d547fa0500cf7b3728c42f569abe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr442_review_lean_replay.json`

- file: [dag/research/pr442_review_lean_replay.json](../../../dag/research/pr442_review_lean_replay.json)
- sha256 (`lf-normalised`): `c63a6d23a78dbb859f2f832ad7b299d933dff0295bf52b376cf5c1cf66ea6a8d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr442_statement_review_20261026.json`

- file: [dag/research/pr442_statement_review_20261026.json](../../../dag/research/pr442_statement_review_20261026.json)
- sha256 (`lf-normalised`): `d51b5f63eb5406f70a7bf87f880fd5cf0ccdd505bc219db36a8b62f11f493299`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_composition_validation.json`

- file: [dag/research/tensor_composition_validation.json](../../../dag/research/tensor_composition_validation.json)
- sha256 (`lf-normalised`): `9f4014f2485a76aeaa79e6ea0a10f50ce6176aa3f66df26ccbbe86e6f0621c3a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_countermodel_validation.json`

- file: [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json)
- sha256 (`lf-normalised`): `151b50b941d8048c73c4b7baf8e42e2f9156421a145edb88b542f988d4769eb9`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_formalization_validation.json`

- file: [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json)
- sha256 (`lf-normalised`): `ca55404cc4a6e1f125b85d21f9bd60a7bc9dfe0e65c85207110c788f0203c120`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_measurement_validation.json`

- file: [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json)
- sha256 (`lf-normalised`): `0ba5c6fbd2b445aaf6f372a6f0b46427b7440245e863408a41ef7d6f0a2c6e90`
- cited in: node.source
- counts toward the grade: yes

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

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`
- `external:sha256:90a3d4db1c5ee741479f5a5ecbdd3100a808824a748a726b863e2d48bae270ad::evaluate_coupled_relational_operad`

## Routes

Incoming (2):

- `FQ-R-GAP-TENSOR` `CONDITIONAL_ON_IMPORT`: [FQ-TENSOR-LU-RIVAL-EXCLUSION](FQ-TENSOR-LU-RIVAL-EXCLUSION.md) (PROVED_LEAN)
- `FRO-R-BACK-CT-INTEROP-TO-TENSOR` `GAP_NO_DERIVATION`: [CT-INFORMATION-MEDIA-INTEROPERABILITY](CT-INFORMATION-MEDIA-INTEROPERABILITY.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-TENSOR-TOMOGRAPHIC-COORDINATES` `DERIVED_LEAN`: [TENSOR-TOMOGRAPHIC-COORDINATES](TENSOR-TOMOGRAPHIC-COORDINATES.md) (PROVED_LEAN)
