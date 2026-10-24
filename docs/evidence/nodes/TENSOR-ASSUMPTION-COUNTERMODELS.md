# TENSOR-ASSUMPTION-COUNTERMODELS

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Full SEP/BP duality, local preservation and binary-product tomography do not select PSD: exact Bell/partial-transpose separations embed into every n,m\>=2. Two-qubit ordinary, twisted and dephased controlled shifts separate calibrated preservation, coherent calibration and reversibility despite matching classical tables. A doubled positive carrier has distinct normalized states with identical product statistics.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 33
- cited Lean declarations covered by a current replay receipt: 33
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- finite complex Hermitian matrix carriers with the real trace pairing
- full local positive and binary matrix tests; operational availability is not inferred
- dimensions n,m\>=2 for cone separations; exact two-qubit gate witnesses
- supplied unitary transformations; supplied continuous paths for the continuity theorem
- positive trace-one state for normalized doubled-carrier witnesses; a basis index constructs one

## Bottleneck

Countermodels delimit weakened hypotheses, not logical minimality of the sufficient package. No primitive derivation, arbitrary-GPT classification, operational saturation, or new proof of SEP closedness is claimed. The identical-qubit family classification remains external.

## Source status

Lean 4.33.1 with pinned Mathlib verifies the full-cone algebra, exact two-qubit calibration failures, all-dimension cone embeddings, and hidden-coordinate tomography failure. The countermodel receipt records the precise scope and standard-axiom audits; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorCountermodelCones.lean`

- file: [lean4/TensorCountermodelCones.lean](../../../lean4/TensorCountermodelCones.lean)
- sha256 (`bytes`): `00bb1a1bb491e342fa6aa91f2e55e2827d1d3d52eea5459370f85150cb14a5bd`
- cited in: node.lean, record TFQ-0413
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorCountermodelCones`): recorded sha256 `00bb1a1bb491e342fa6aa91f2e55e2827d1d3d52eea5459370f85150cb14a5bd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorCountermodelCones`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `binary_product_statistics_separate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms binary_product_statistics_separate` |
| `blockPositive_iff_dual_sep` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms blockPositive_iff_dual_sep` |
| `bp_local` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms bp_local` |
| `bp_salient` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms bp_salient` |
| `sep_local` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sep_local` |
| `sep_ppt` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sep_ppt` |
| `twist_path_continuous` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twist_path_continuous` |
| `twist_reversible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twist_reversible` |
| `twist_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twist_trace` |
| `twisted_local` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twisted_local` |
| `twisted_self_dual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twisted_self_dual` |
- counts toward the grade: yes

### Lean: `lean4/TensorCountermodelEmbeddings.lean`

- file: [lean4/TensorCountermodelEmbeddings.lean](../../../lean4/TensorCountermodelEmbeddings.lean)
- sha256 (`bytes`): `c9186b3d5bf366ee248f398fff26ecea37b48f828fff7fafdcfe297c64581ae7`
- cited in: node.lean, record TFQ-0413
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorCountermodelEmbeddings`): recorded sha256 `c9186b3d5bf366ee248f398fff26ecea37b48f828fff7fafdcfe297c64581ae7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorCountermodelEmbeddings`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cone_separations_all_dimensions` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cone_separations_all_dimensions` |
- counts toward the grade: yes

### Lean: `lean4/TensorCountermodelWitnesses.lean`

- file: [lean4/TensorCountermodelWitnesses.lean](../../../lean4/TensorCountermodelWitnesses.lean)
- sha256 (`bytes`): `252376bed56d7ca7eae9e7edc23b64006a5fbdbd01ec640cee956133a8e0a37c`
- cited in: node.lean, record TFQ-0413
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorCountermodelWitnesses`): recorded sha256 `252376bed56d7ca7eae9e7edc23b64006a5fbdbd01ec640cee956133a8e0a37c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorCountermodelWitnesses`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bp_fails_inverse_controlled_shift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms bp_fails_inverse_controlled_shift` |
| `coherent_calibration_separates` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms coherent_calibration_separates` |
| `dephased_coherent_calibration_separates` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dephased_coherent_calibration_separates` |
| `dephased_controlled_shift_not_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dephased_controlled_shift_not_injective` |
| `dephased_same_classical_table` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dephased_same_classical_table` |
| `imaginary_effect_binary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms imaginary_effect_binary` |
| `plus_binary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms plus_binary` |
| `seed_normalized` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms seed_normalized` |
| `sep_fails_controlled_shift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sep_fails_controlled_shift` |
| `twisted_fails_ordinary_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twisted_fails_ordinary_calibration` |
| `twisted_same_classical_table` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms twisted_same_classical_table` |
- counts toward the grade: yes

### Lean: `lean4/TensorHiddenCoordinates.lean`

- file: [lean4/TensorHiddenCoordinates.lean](../../../lean4/TensorHiddenCoordinates.lean)
- sha256 (`bytes`): `9dd11ca5ef7eacf97d9ed9f5ea1125a5fb146724ac34eb8bc10fdb4fbef67e27`
- cited in: node.lean, record TFQ-0413
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorHiddenCoordinates`): recorded sha256 `9dd11ca5ef7eacf97d9ed9f5ea1125a5fb146724ac34eb8bc10fdb4fbef67e27` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorHiddenCoordinates`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `basis_state_normalized` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms basis_state_normalized` |
| `dimension_doubled` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dimension_doubled` |
| `doubledConj_inverse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms doubledConj_inverse` |
| `hidden_normalized_states` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms hidden_normalized_states` |
| `independent_probabilities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms independent_probabilities` |
| `no_local_tomography` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_local_tomography` |
- counts toward the grade: yes

### Lean: `lean4/TensorPartialTranspose.lean`

- file: [lean4/TensorPartialTranspose.lean](../../../lean4/TensorPartialTranspose.lean)
- sha256 (`bytes`): `b1b8ad92013a3edbb5ddf3700beabf705b411a82632f0a50cedcd525eb06580d`
- cited in: node.lean, record TFQ-0413
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorPartialTranspose`): recorded sha256 `b1b8ad92013a3edbb5ddf3700beabf705b411a82632f0a50cedcd525eb06580d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorPartialTranspose`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `conjMap_inverse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms conjMap_inverse` |
| `gamma` | yes | yes | yes | module-level | `#print axioms gamma` |
| `gamma_conjMap_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms gamma_conjMap_product` |
| `pairing_gamma_gamma` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pairing_gamma_gamma` |
- counts toward the grade: yes

### Python: `code/python/src/qm/tensor_composition.py`

- file: [code/python/src/qm/tensor_composition.py](../../../code/python/src/qm/tensor_composition.py)
- sha256 (`bytes`): `27de072b677956282bf19a244886dc508fe64982b7823145803f261cc05c2f56`
- cited in: node.source, record TFQ-0413
- counts toward the grade: yes

### Python: `code/python/tests/test_tensor_composition.py`

- file: [code/python/tests/test_tensor_composition.py](../../../code/python/tests/test_tensor_composition.py)
- sha256 (`bytes`): `7ff81adb7558a8741bfb648bf1e832a65e2857b320986f1447d0c5890e3b18c4`
- cited in: node.source
- check: `python -m pytest code/python/tests/test_tensor_composition.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`

- file: [dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md](../../../dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md)
- sha256 (`lf-normalised`): `3d1f897722aad08811a52c863e8bc47cfda41d9d087929a00c3925f4782de12f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0413
- counts toward the grade: no

### Documents and data: `dag/research/tensor_countermodel_validation.json`

- file: [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json)
- sha256 (`lf-normalised`): `efc7aef071bd247287095b06c05e5ecd8ef2e777af7b6a0e3bf685b52d5f7459`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-ASSUMPTION-COUNTERMODELS` `DERIVED_LEAN`: [TENSOR-TOMOGRAPHIC-COORDINATES](TENSOR-TOMOGRAPHIC-COORDINATES.md) (PROVED_LEAN), [TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION](TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION.md) (PROVED_LEAN), [TENSOR-BINARY-EFFECT-INTERVAL](TENSOR-BINARY-EFFECT-INTERVAL.md) (PROVED_LEAN)

Outgoing (0):

