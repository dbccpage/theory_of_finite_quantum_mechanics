# TENSOR-CONE-ORBIT-KERNEL

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any finite complex matrix size, a Hermitian set containing zero and closed under addition equals PSD when seed preparations and positive seed tests are transported by preserving operations whose seed-vector orbits cover all vectors.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- finite complex matrix and spectral theory
- explicit OrbitData reachability and transport hypotheses

## Bottleneck

The general finite-index cone kernel retains explicit OrbitData assumptions. TensorOperationalCone now instantiates its transports and reachability using the proved Schmidt controlled-shift construction; TensorComposition connects that instance to the constructed operational coordinates.

## Source status

Verified with Lean 4.33.1 and pinned Mathlib; checked theorem scope and remaining prose corollaries are distinguished in the derivation and tensor formalization receipt; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorConeReconstruction.lean`

- file: [lean4/TensorConeReconstruction.lean](../../../lean4/TensorConeReconstruction.lean)
- sha256 (`bytes`): `b95e0257776bed514b2bb0b08504f399650d11c0a8090668c32949ea576722d8`
- cited in: node.lean, record TFQ-0411
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorConeReconstruction`): recorded sha256 `b95e0257776bed514b2bb0b08504f399650d11c0a8090668c32949ea576722d8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json) (module `TensorConeReconstruction`): recorded sha256 `b95e0257776bed514b2bb0b08504f399650d11c0a8090668c32949ea576722d8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorConeReconstruction`): recorded sha256 `b95e0257776bed514b2bb0b08504f399650d11c0a8090668c32949ea576722d8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorConeReconstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `operational_orbit_selects_positive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms operational_orbit_selects_positive` |
| `positive_mem_of_rankOne` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms positive_mem_of_rankOne` |

- counts toward the grade: yes

### Python: `code/python/src/qm/tensor_composition.py`

- file: [code/python/src/qm/tensor_composition.py](../../../code/python/src/qm/tensor_composition.py)
- sha256 (`bytes`): `27de072b677956282bf19a244886dc508fe64982b7823145803f261cc05c2f56`
- cited in: node.source, record TFQ-0411
- counts toward the grade: yes

### Python: `code/python/tests/test_tensor_composition.py`

- file: [code/python/tests/test_tensor_composition.py](../../../code/python/tests/test_tensor_composition.py)
- sha256 (`bytes`): `7ff81adb7558a8741bfb648bf1e832a65e2857b320986f1447d0c5890e3b18c4`
- cited in: node.source
- check: `python -m pytest code/python/tests/test_tensor_composition.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0411_tensor_cone_orbit_kernel.md`

- file: [dag/derivations/27_tensor_composition/tfq_0411_tensor_cone_orbit_kernel.md](../../../dag/derivations/27_tensor_composition/tfq_0411_tensor_cone_orbit_kernel.md)
- sha256 (`lf-normalised`): `63120a31cac72a80dc162baf4ac1782299c290aec39401e0bc428da88c399bb5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0411
- counts toward the grade: no

### Documents and data: `dag/research/tensor_formalization_validation.json`

- file: [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json)
- sha256 (`lf-normalised`): `ca55404cc4a6e1f125b85d21f9bd60a7bc9dfe0e65c85207110c788f0203c120`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-CONE-ORBIT-KERNEL` `DERIVED_LEAN`: [TENSOR-TOMOGRAPHIC-COORDINATES](TENSOR-TOMOGRAPHIC-COORDINATES.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION` `DERIVED_LEAN`: [TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION](TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION.md) (PROVED_LEAN)
