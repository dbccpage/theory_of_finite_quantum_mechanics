# TENSOR-TOMOGRAPHIC-COORDINATES

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Independent bilinear preparations and tests with trace-factorized product probabilities and local tomography construct a unique real linear equivalence with joint Hermitian matrices for arbitrary finite local complex dimensions. The equivalence preserves products and all product tests; the deterministic product test is trace. The joint state cone is not assumed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- finite local complex quantum state and effect spaces
- independent preparations and tests with factorized probabilities
- local tomography
- mixing and linear operational extension

## Bottleneck

Lean verifies Hermitian product spanning, nondegenerate trace pairing, finite dual-frame reconstruction, injectivity, surjectivity, uniqueness, and process calibration. Local complex QM and the operational bilinear/tomography premises remain supplied. The displayed positive projector-basis formula and SEP/BP commentary are prose corollaries, not additional Lean claims.

## Source status

Verified with Lean 4.33.1 and pinned Mathlib; checked theorem scope and remaining prose corollaries are distinguished in the derivation and tensor formalization receipt; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorComposition.lean`

- file: [lean4/TensorComposition.lean](../../../lean4/TensorComposition.lean)
- sha256 (`bytes`): `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926`
- cited in: node.lean, record TFQ-0410
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorComposition`): recorded sha256 `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorComposition`): recorded sha256 `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorComposition`): recorded sha256 `f91adb5ff654e3da899a3b94c1c081433b7338daee17508b2ecc66be49457926` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorComposition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `unit_test_is_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms unit_test_is_trace` |

- counts toward the grade: yes

### Lean: `lean4/TensorCoordinates.lean`

- file: [lean4/TensorCoordinates.lean](../../../lean4/TensorCoordinates.lean)
- sha256 (`bytes`): `9f218b9f0a2898ecf2e8307d63ea986089407afe9ac81944a254db1655b3bcba`
- cited in: node.lean, record TFQ-0410
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorCoordinates`): recorded sha256 `9f218b9f0a2898ecf2e8307d63ea986089407afe9ac81944a254db1655b3bcba` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorCoordinates`): recorded sha256 `9f218b9f0a2898ecf2e8307d63ea986089407afe9ac81944a254db1655b3bcba` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorCoordinates`): recorded sha256 `9f218b9f0a2898ecf2e8307d63ea986089407afe9ac81944a254db1655b3bcba` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorCoordinates`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `finite_frame_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms finite_frame_calibration` |
| `product_calibration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms product_calibration` |
| `tomographicEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tomographicEquiv` |
| `tomographicEquiv_prepare` | yes | yes | yes | module-level | `#print axioms tomographicEquiv_prepare` |
| `tomographicEquiv_test` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tomographicEquiv_test` |
| `tomographicEquiv_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tomographicEquiv_unique` |

- counts toward the grade: yes

### Lean: `lean4/TensorTomography.lean`

- file: [lean4/TensorTomography.lean](../../../lean4/TensorTomography.lean)
- sha256 (`bytes`): `eb4c4598cd7763211606bcd097a3bda46e6e0365cf42f7ea8ec97b6aae44b4de`
- cited in: node.lean, record TFQ-0410
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorTomography`): recorded sha256 `eb4c4598cd7763211606bcd097a3bda46e6e0365cf42f7ea8ec97b6aae44b4de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorTomography`): recorded sha256 `eb4c4598cd7763211606bcd097a3bda46e6e0365cf42f7ea8ec97b6aae44b4de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorTomography`): recorded sha256 `eb4c4598cd7763211606bcd097a3bda46e6e0365cf42f7ea8ec97b6aae44b4de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorTomography`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pairing_nondegenerate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pairing_nondegenerate` |
| `product_span` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms product_span` |

- counts toward the grade: yes

### Python: `code/python/src/qm/tensor_composition.py`

- file: [code/python/src/qm/tensor_composition.py](../../../code/python/src/qm/tensor_composition.py)
- sha256 (`bytes`): `27de072b677956282bf19a244886dc508fe64982b7823145803f261cc05c2f56`
- cited in: node.source, record TFQ-0410
- counts toward the grade: yes

### Python: `code/python/tests/test_tensor_composition.py`

- file: [code/python/tests/test_tensor_composition.py](../../../code/python/tests/test_tensor_composition.py)
- sha256 (`bytes`): `7ff81adb7558a8741bfb648bf1e832a65e2857b320986f1447d0c5890e3b18c4`
- cited in: node.source
- check: `python -m pytest code/python/tests/test_tensor_composition.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0410_tensor_tomographic_coordinates.md`

- file: [dag/derivations/27_tensor_composition/tfq_0410_tensor_tomographic_coordinates.md](../../../dag/derivations/27_tensor_composition/tfq_0410_tensor_tomographic_coordinates.md)
- sha256 (`lf-normalised`): `6b362297a378d6593662c638908ac1d8793a986c32929bf4f12fe4c77ce10025`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0410
- counts toward the grade: no

### Documents and data: `dag/research/tensor_formalization_validation.json`

- file: [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json)
- sha256 (`lf-normalised`): `ca55404cc4a6e1f125b85d21f9bd60a7bc9dfe0e65c85207110c788f0203c120`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-TOMOGRAPHIC-COORDINATES` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION), [FQ-GAP-TENSOR-UNIQUENESS](FQ-GAP-TENSOR-UNIQUENESS.md) (CONDITIONAL)

Outgoing (3):

- `APP-R-TENSOR-ASSUMPTION-COUNTERMODELS` `DERIVED_LEAN`: [TENSOR-ASSUMPTION-COUNTERMODELS](TENSOR-ASSUMPTION-COUNTERMODELS.md) (PROVED_LEAN)
- `APP-R-TENSOR-CONE-ORBIT-KERNEL` `DERIVED_LEAN`: [TENSOR-CONE-ORBIT-KERNEL](TENSOR-CONE-ORBIT-KERNEL.md) (PROVED_LEAN)
- `APP-R-TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION` `DERIVED_LEAN`: [TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION](TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION.md) (PROVED_LEAN)
