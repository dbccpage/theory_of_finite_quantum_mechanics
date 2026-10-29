# TENSOR-GENERATED-EFFECT-CONE

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The conic hull of represented available effects equals PSD for arbitrary finite n\<=m with m nonzero, using the verified state cone, sound effects, all local binary product tests and calibrated local-unitary and controlled-shift pullbacks. Neither effect saturation nor finite-test saturation is required.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- state-cone conclusion of quantum_state_cone
- sound operational effects
- all products of local binary effects
- calibrated reversible effect pullbacks

## Bottleneck

Operational soundness, local binary product availability and reversible effect pullback closure remain explicit premises. The generated cone does not identify the available binary interval or available finite tests.

## Source status

Verified with Lean 4.33.1 and pinned Mathlib; theorem premises and standard logical axioms are recorded in the measurement validation receipt; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorEffectCone.lean`

- file: [lean4/TensorEffectCone.lean](../../../lean4/TensorEffectCone.lean)
- sha256 (`bytes`): `e88adf90c3f1f679209df8cb6ecf9a949fc00b1e272f06272c0cd679f1050f70`
- cited in: node.lean, record TFQ-0414
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorEffectCone`): recorded sha256 `e88adf90c3f1f679209df8cb6ecf9a949fc00b1e272f06272c0cd679f1050f70` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorEffectCone`): recorded sha256 `e88adf90c3f1f679209df8cb6ecf9a949fc00b1e272f06272c0cd679f1050f70` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorEffectCone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `effect_cone_eq_positive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms effect_cone_eq_positive` |

- counts toward the grade: yes

### Lean: `lean4/TensorEffectOrder.lean`

- file: [lean4/TensorEffectOrder.lean](../../../lean4/TensorEffectOrder.lean)
- sha256 (`bytes`): `7c7bd7e9d1f957a93c378f31e287ea459bc125c83d05a2843348334120372d52`
- cited in: node.lean, record TFQ-0414
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorEffectOrder`): recorded sha256 `7c7bd7e9d1f957a93c378f31e287ea459bc125c83d05a2843348334120372d52` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorEffectOrder`): recorded sha256 `7c7bd7e9d1f957a93c378f31e287ea459bc125c83d05a2843348334120372d52` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorEffectOrder`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `positive_iff_pairing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms positive_iff_pairing` |
| `positive_ray_binary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms positive_ray_binary` |

- counts toward the grade: yes

### Lean: `lean4/TensorMeasurements.lean`

- file: [lean4/TensorMeasurements.lean](../../../lean4/TensorMeasurements.lean)
- sha256 (`bytes`): `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9`
- cited in: node.lean, record TFQ-0414
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorMeasurements`): recorded sha256 `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorMeasurements`): recorded sha256 `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorMeasurements`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `operational_effect_cone` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms operational_effect_cone` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md`

- file: [dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md](../../../dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md)
- sha256 (`lf-normalised`): `126de574698271544d28d12fda6f87f088637b5f3b4cf0ddd0aa6a974362cc02`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0414
- counts toward the grade: no

### Documents and data: `dag/research/tensor_measurement_validation.json`

- file: [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json)
- sha256 (`lf-normalised`): `b527b722e90d69dd18aa762d109425189ff7636e0b6510c1481e8579cff0f597`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-GENERATED-EFFECT-CONE` `DERIVED_LEAN`: [TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION](TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION.md) (PROVED_LEAN)

Outgoing (0):

