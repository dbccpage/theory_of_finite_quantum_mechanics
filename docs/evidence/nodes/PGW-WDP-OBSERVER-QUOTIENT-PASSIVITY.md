# PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Chapter 10 replaces one observer tuple by four declared layers joined by typed adapters: presentation (X, P, q, C), memory (a retention packet), evaluator (D, A, d, J, Γ, T) and policy, with policy not authority; the quotient evaluator computes Φ_O(\[δ\]) = inf_α J(δ − dα), and a terminalizer may return Accept, Reject or Undetermined against observer-profile data. For source adapters, a partial operation descends along onto sort maps iff its output, including undefinedness, is constant on each input fibre after the output map, and a relation descends iff its truth value is fibre-constant. WDP-CH10-D06: a quotient observer is a linear report map R: C¹ → F^k with Rd₀ = 0, entering only as a presentation report and as the induced cost Φ_O(y) = inf{Φ₁(r) : O(r) = y} on im R, with memory, policy and authority refused. WDP-CH10-P01: Φ_O(O q) ≤ Φ₁(q), so no observer reports positive obstruction for an exact class; WDP-CH10-P02 orders a declared observer family by kernel inclusion (identity finest, zero coarsest); WDP-CH10-P03: a report map into a finite grammar G exposes at most |G| visible classes, so more than |G| core classes collide.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared presentation, memory, evaluator and policy packets with typed adapters (assumption)

## Bottleneck

Evaluation is not perception or proposal and policy is not authority; Lean observer_passivity_of_infimum takes the fibrewise lower bound as hypothesis and leaves the core-identification clause unformalized, while declared_family_order and grammar_resolution_bound cover P02 and P03 at their finite scope.

## Source status

WDP monograph §10.1-§10.5 WDP-CH10-D01..D06 definitions with P01-P03; Lean Obstruction and ObserverResolution

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/ObserverResolution.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/ObserverResolution.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ObserverResolution.lean)
- sha256 (`bytes`): `880cf8f70ac1b583e07438f834cc52c2ce9f5e7eeeb2f4829a5393546658e6af`
- cited in: node.lean, record TFQ-0553
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.ObserverResolution`): recorded sha256 `880cf8f70ac1b583e07438f834cc52c2ce9f5e7eeeb2f4829a5393546658e6af` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/ObserverResolution.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `declared_family_order` | yes | yes | yes | none | `#print axioms declared_family_order` |
| `grammar_resolution_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms grammar_resolution_bound` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885`
- cited in: node.lean, record TFQ-0553
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `observer_passivity_of_infimum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms observer_passivity_of_infimum` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_category_theory/src/finite_partial_structure.rs`

- file: `omega_engine/crates_rs/omega_category_theory/src/finite_partial_structure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_quotient_observer.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_quotient_observer.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_quotient_observer.py)
- sha256 (`bytes`): `49232555ff35e0baf85bf8e7f00e55a2b60ba574d6d1c29a9317ac12b7cae0ac`
- cited in: record TFQ-0553
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_quotient_observer.py::test_passivity_can_be_strict_and_core_identifications_survive`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_passivity_can_be_strict_and_core_identifications_survive` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_quotient_observer.py::test_passivity_can_be_strict_and_core_identifications_survive` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quotient_observer.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quotient_observer.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quotient_observer.py)
- sha256 (`bytes`): `037619f360a6fa6dce659c386938e6acddff57536f2d6fe363ee479c4f08adfc`
- cited in: record TFQ-0553

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check_passivity` (python_symbol) | yes | yes | yes | - | - |
| `make_linear_quotient_observer` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0553_wdp_observer_quotient_passivity.md`

- file: [dag/derivations/06_wdp/tfq_0553_wdp_observer_quotient_passivity.md](../../../dag/derivations/06_wdp/tfq_0553_wdp_observer_quotient_passivity.md)
- sha256 (`lf-normalised`): `1fef38d3dc07e355ad65a0f627b2ffe7ad30611eac7a42fb7b268f86301f468f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0553
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_09_behavioral_quotients_finite_states.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_09_behavioral_quotients_finite_states.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_category_theory/src/finite_partial_structure.rs::descend`

## Routes

Incoming (1):

- `PGW-R-WDP-OBSERVER-QUOTIENT-PASSIVITY` `DERIVED_PROSE`: [PG-WDP-PROTECTED-QUESTIONS](PG-WDP-PROTECTED-QUESTIONS.md) (PROVED_LEAN), [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)

Outgoing (4):

- `OPS-R-AXIS3-RELABELING` `CONDITIONAL_ON_IMPORT`: [OPS-AXIS3-RELABELING](OPS-AXIS3-RELABELING.md) (CONDITIONAL)
- `OPS-R-OBSERVER-TUPLE` `RECORD_PARENT`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)
- `PGW-R-WDP-BRIDGE-REPORT-FIBER-OBSERVER` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER](PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER.md) (CONDITIONAL)
- `PGW-R-WDP-GENESIS-BRIDGES-LEDGER` `DERIVED_PROSE`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION)
