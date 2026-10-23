# TENSOR-BINARY-EFFECT-INTERVAL

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The constructed dual representation identifies functionals satisfying 0\<=e(x)\<=u(x) on the state cone with Hermitian matrices 0\<=E\<=I. Homogeneous bounds are equivalent to probabilities in \[0,1\] on all trace-one PSD states. Soundness plus explicit EffectSaturated identifies the available binary effects with this full interval.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- state-cone conclusion of quantum_state_cone
- sound operational effects
- EffectSaturated: every cone-bounded functional is available

## Bottleneck

EffectSaturated is a separate no-restriction premise, not a consequence of state-cone or generated-effect-cone equality. Local complex QM and the state-reconstruction assumptions remain supplied.

## Source status

Verified with Lean 4.33.1 and pinned Mathlib; theorem premises and standard logical axioms are recorded in the measurement validation receipt; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorEffectOrder.lean`

- file: [lean4/TensorEffectOrder.lean](../../../lean4/TensorEffectOrder.lean)
- sha256 (`bytes`): `7c7bd7e9d1f957a93c378f31e287ea459bc125c83d05a2843348334120372d52`
- cited in: node.lean, record TFQ-0415
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorEffectOrder`): recorded sha256 `7c7bd7e9d1f957a93c378f31e287ea459bc125c83d05a2843348334120372d52` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorEffectOrder`): recorded sha256 `7c7bd7e9d1f957a93c378f31e287ea459bc125c83d05a2843348334120372d52` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorEffectOrder`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `binary_iff_bounds` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms binary_iff_bounds` |
| `binary_iff_interval` | yes | yes | yes | module-level | `#print axioms binary_iff_interval` |
| `binary_iff_normalized` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms binary_iff_normalized` |
- counts toward the grade: yes

### Lean: `lean4/TensorMeasurements.lean`

- file: [lean4/TensorMeasurements.lean](../../../lean4/TensorMeasurements.lean)
- sha256 (`bytes`): `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9`
- cited in: node.lean, record TFQ-0415
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorMeasurements`): recorded sha256 `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorMeasurements`): recorded sha256 `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorMeasurements`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `available_effects_eq_interval` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms available_effects_eq_interval` |
| `effectRepresentation` | yes | yes | yes | module-level | `#print axioms effectRepresentation` |
| `effectRepresentation_product` | yes | yes | yes | module-level | `#print axioms effectRepresentation_product` |
| `effectRepresentation_unit` | yes | yes | yes | module-level | `#print axioms effectRepresentation_unit` |
| `validEffect_iff_binary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms validEffect_iff_binary` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md`

- file: [dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md](../../../dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md)
- sha256 (`lf-normalised`): `2c5fb04175f367a1d58477d317882002336577f65d895226c9ab4bc01eb9377a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0415
- counts toward the grade: no

### Documents and data: `dag/research/tensor_measurement_validation.json`

- file: [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json)
- sha256 (`lf-normalised`): `0ba5c6fbd2b445aaf6f372a6f0b46427b7440245e863408a41ef7d6f0a2c6e90`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-BINARY-EFFECT-INTERVAL` `DERIVED_LEAN`: [TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION](TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-TENSOR-ASSUMPTION-COUNTERMODELS` `DERIVED_LEAN`: [TENSOR-ASSUMPTION-COUNTERMODELS](TENSOR-ASSUMPTION-COUNTERMODELS.md) (PROVED_LEAN)
- `APP-R-TENSOR-FINITE-POVM-AVAILABILITY` `DERIVED_LEAN`: [TENSOR-FINITE-POVM-AVAILABILITY](TENSOR-FINITE-POVM-AVAILABILITY.md) (PROVED_LEAN)
