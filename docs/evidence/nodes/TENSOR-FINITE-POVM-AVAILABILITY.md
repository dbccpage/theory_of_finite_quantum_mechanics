# TENSOR-FINITE-POVM-AVAILABILITY

Stage: [TENSOR_COMPOSITION](../stages/TENSOR_COMPOSITION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any finite outcome type, sound available tests correspond to positive Hermitian families summing to I. Conversely every such POVM is available under both EffectSaturated and the separate FiniteTestSaturated premise. The end-to-end quantum_measurements theorem invokes quantum_state_cone and returns the generated cone, binary interval and finite-POVM equivalence.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- state-cone conclusion of quantum_state_cone
- sound available effects and finite tests
- EffectSaturated
- FiniteTestSaturated

## Bottleneck

FiniteTestSaturated requires jointly implementing each finite family of available effects summing to the deterministic unit. It is distinct from individual effect saturation. No availability or classification of instruments or channels is asserted.

## Source status

Verified with Lean 4.33.1 and pinned Mathlib; theorem premises and standard logical axioms are recorded in the measurement validation receipt; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TensorMeasurements.lean`

- file: [lean4/TensorMeasurements.lean](../../../lean4/TensorMeasurements.lean)
- sha256 (`bytes`): `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9`
- cited in: node.lean, record TFQ-0416
- replay: `verified`
  - receipt [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json) (module `TensorMeasurements`): recorded sha256 `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `TensorMeasurements`): recorded sha256 `41154dcd26b10ee87ae04b881c1c8bcc20cbd7fc7e9da12e94381eef67efcfd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TensorMeasurements`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `povm_binary` | yes | yes | yes | module-level | `#print axioms povm_binary` |
| `quantum_measurements` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms quantum_measurements` |
| `test_iff_povm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms test_iff_povm` |
| `test_povm_of_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms test_povm_of_sound` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md`

- file: [dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md](../../../dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md)
- sha256 (`lf-normalised`): `db945ab62338d7c0037b8c012ad05d4c893694524faf0397ac79ffee4ddda4e9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0416
- counts toward the grade: no

### Documents and data: `dag/research/tensor_measurement_validation.json`

- file: [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json)
- sha256 (`lf-normalised`): `bb11d3a6987e07d70baa1d6530c757fc29ca7c7dffc24847c6979f11467129b1`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-TENSOR-FINITE-POVM-AVAILABILITY` `DERIVED_LEAN`: [TENSOR-BINARY-EFFECT-INTERVAL](TENSOR-BINARY-EFFECT-INTERVAL.md) (PROVED_LEAN)

Outgoing (0):

