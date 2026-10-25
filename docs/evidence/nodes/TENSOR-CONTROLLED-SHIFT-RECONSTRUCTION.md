# TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For arbitrary finite n\<=m with m nonzero (the smaller subsystem is the control), supplied local complex QM, independent bilinear preparation/testing, local tomography, positive product tests, finite-sum state closure, and calibrated local-unitary and reversible controlled-shift preservation force the represented state cone to be PSD(nm). Tomographic coordinates, Schmidt reachability, cone equality and trace normalization are verified in Lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- local complex QM and spectral theory
- independent preparation, testing and convex composition
- local tomography
- all local unitary operations
- coherently calibrated reversible controlled shift
- effect and finite-test saturation for full measurement availability

## Bottleneck

Lean constructs complete rectangular Schmidt bases, local unitaries and one modular controlled shift, then checks the operational state cone. TFQ-0414--TFQ-0416 check the generated effect cone, binary interval and finite POVMs with explicit effect and finite-test saturation premises. Calibration and operational preservation remain supplied; primitive difference has not supplied these hypotheses.

## Source status

Verified state-space theorem with measurement corollaries separately verified in TFQ-0414--TFQ-0416.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorComposition.lean`

- file: [lean4/TensorComposition.lean](../../../lean4/TensorComposition.lean)
- sha256 (`bytes`): `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926`
- cited in: node.lean, record TFQ-0412
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorComposition`): recorded sha256 `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorComposition`): recorded sha256 `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorComposition`): recorded sha256 `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorComposition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quantum_state_cone` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms quantum_state_cone` |
| `unit_test_is_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms unit_test_is_trace` |

- counts toward the grade: yes

### Lean: `lean4/TensorOperationalCone.lean`

- file: [lean4/TensorOperationalCone.lean](../../../lean4/TensorOperationalCone.lean)
- sha256 (`bytes`): `087b80fa37cb33daa2e357d59e4c1d076feabdd7b8cdc01f5e78686b10c1c7c0`
- cited in: node.lean, record TFQ-0412
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorOperationalCone`): recorded sha256 `087b80fa37cb33daa2e357d59e4c1d076feabdd7b8cdc01f5e78686b10c1c7c0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorOperationalCone`): recorded sha256 `087b80fa37cb33daa2e357d59e4c1d076feabdd7b8cdc01f5e78686b10c1c7c0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorOperationalCone`): recorded sha256 `087b80fa37cb33daa2e357d59e4c1d076feabdd7b8cdc01f5e78686b10c1c7c0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorOperationalCone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `controlled_shift_selects_positive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms controlled_shift_selects_positive` |

- counts toward the grade: yes

### Lean: `lean4/TensorReachability.lean`

- file: [lean4/TensorReachability.lean](../../../lean4/TensorReachability.lean)
- sha256 (`bytes`): `7c0eedbf908441983f51d2f431b01ca335087b44754b35a9db1ccea1f40bd38e`
- cited in: node.lean, record TFQ-0412
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorReachability`): recorded sha256 `7c0eedbf908441983f51d2f431b01ca335087b44754b35a9db1ccea1f40bd38e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorReachability`): recorded sha256 `7c0eedbf908441983f51d2f431b01ca335087b44754b35a9db1ccea1f40bd38e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorReachability`): recorded sha256 `7c0eedbf908441983f51d2f431b01ca335087b44754b35a9db1ccea1f40bd38e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorReachability`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_schmidt_coefficients` | yes | yes | yes | module-level | `#print axioms exists_schmidt_coefficients` |
| `schmidt_reachability` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms schmidt_reachability` |

- counts toward the grade: yes

### Lean: `lean4/TensorSchmidt.lean`

- file: [lean4/TensorSchmidt.lean](../../../lean4/TensorSchmidt.lean)
- sha256 (`bytes`): `ef05cc11f534a796a50aa1755b06346ce37213a31cebd0c737fc2d0fe7deb528`
- cited in: node.lean, record TFQ-0412
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorSchmidt`): recorded sha256 `ef05cc11f534a796a50aa1755b06346ce37213a31cebd0c737fc2d0fe7deb528` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorSchmidt`): recorded sha256 `ef05cc11f534a796a50aa1755b06346ce37213a31cebd0c737fc2d0fe7deb528` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorSchmidt`): recorded sha256 `ef05cc11f534a796a50aa1755b06346ce37213a31cebd0c737fc2d0fe7deb528` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorSchmidt`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_schmidt_bases` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_schmidt_bases` |

- counts toward the grade: yes

### Python: `code/python/src/qm/tensor_composition.py`

- file: [code/python/src/qm/tensor_composition.py](../../../code/python/src/qm/tensor_composition.py)
- sha256 (`bytes`): `27de072b677956282bf19a244886dc508fe64982b7823145803f261cc05c2f56`
- cited in: node.source, record TFQ-0412
- counts toward the grade: yes

### Python: `code/python/tests/test_tensor_composition.py`

- file: [code/python/tests/test_tensor_composition.py](../../../code/python/tests/test_tensor_composition.py)
- sha256 (`bytes`): `7ff81adb7558a8741bfb648bf1e832a65e2857b320986f1447d0c5890e3b18c4`
- cited in: node.source
- check: `python -m pytest code/python/tests/test_tensor_composition.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md`

- file: [dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md](../../../dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md)
- sha256 (`lf-normalised`): `3dd28ec9850c6667c6b8ca677516507f3a56667b03d264c225f3b5056b7b2a34`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0412
- counts toward the grade: no

### Documents and data: `dag/research/tensor_formalization_validation.json`

- file: [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json)
- sha256 (`lf-normalised`): `ca55404cc4a6e1f125b85d21f9bd60a7bc9dfe0e65c85207110c788f0203c120`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION` `DERIVED_LEAN`: [TENSOR-TOMOGRAPHIC-COORDINATES](TENSOR-TOMOGRAPHIC-COORDINATES.md) (PROVED_LEAN), [TENSOR-CONE-ORBIT-KERNEL](TENSOR-CONE-ORBIT-KERNEL.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-TENSOR-ASSUMPTION-COUNTERMODELS` `DERIVED_LEAN`: [TENSOR-ASSUMPTION-COUNTERMODELS](TENSOR-ASSUMPTION-COUNTERMODELS.md) (PROVED_LEAN)
- `APP-R-TENSOR-BINARY-EFFECT-INTERVAL` `DERIVED_LEAN`: [TENSOR-BINARY-EFFECT-INTERVAL](TENSOR-BINARY-EFFECT-INTERVAL.md) (PROVED_LEAN)
- `APP-R-TENSOR-GENERATED-EFFECT-CONE` `DERIVED_LEAN`: [TENSOR-GENERATED-EFFECT-CONE](TENSOR-GENERATED-EFFECT-CONE.md) (PROVED_LEAN)
