# PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Suppose an external task requires \<a\> and \<ab\> to differ while the current regime has \<a\> ≈ₙ \<ab\>. Every operation f on the quotient S_n/≈ₙ gives f(\[\<a\>\]) = f(\[\<ab\>\]), so no operation on the current quotient answers the task on every input, and a refinement adding at least one observation o with o(\<a\>) ≠ o(\<ab\>) is forced; the analysis gives this as an argument with proof. The lift is not unique: under a supplied string decoder, 'payload has more than one position' and 'payload contains b' both separate \<a\> from \<ab\> but disagree on \<aa\> (true and false), and full inscription identity also separates the pair while carrying more than one bit. A canonical tower therefore needs a declared minimality or initiality policy, such as fewest new predicates, minimum description length, maximal preservation of old equivalences, a free or initial completion, or retention of every tied minimum branch.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Supplied string decoder for the payloads of \<a\>, \<ab\> and \<aa\>, used only by the non-uniqueness example (assumption)

## Bottleneck

The Lean declarations cover the quotient barrier; the non-uniqueness of the lift rests on the two-predicate example, and no selection policy, fixed ladder of quotients or minimal multiplicity lift is derived.

## Source status

000_oepregen 03_results_and_arguments.md section 5 (statement 5, argument with proof); genesis paper.md Proposition 1; Lean Paper000.separation_not_on_quotient

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Quot.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Quot.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Quot.lean)
- sha256 (`bytes`): `e2cbacdf63dc0fb91a57c1f02f2dff617353b1973e80d6c78225289d5e08868f`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Quot`): recorded sha256 `e2cbacdf63dc0fb91a57c1f02f2dff617353b1973e80d6c78225289d5e08868f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Quot.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quotient_barrier` | yes | yes | yes | Quot.sound | `#print axioms quotient_barrier` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Paper000.lean`

- file: [lean4/Imported/Genesis19l57g1/Paper000.lean](../../../lean4/Imported/Genesis19l57g1/Paper000.lean)
- sha256 (`bytes`): `1257bc7a308228f6d966fb493abe022f65123d4d5b0bdfeb49ed9dcd9722ce46`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.Genesis19l57g1.Paper000`): recorded sha256 `1257bc7a308228f6d966fb493abe022f65123d4d5b0bdfeb49ed9dcd9722ce46` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Paper000.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `separation_not_on_quotient` | yes | yes | yes | none | `#print axioms separation_not_on_quotient` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Observation.lean`

- file: [lean4/Imported/PreGenesisToMssn/Observation.lean](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)
- sha256 (`bytes`): `cb6ccaec927d5bea865af8ae40f653a01f4b4301a4b022418e2a52e8df431d79`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Observation`): recorded sha256 `cb6ccaec927d5bea865af8ae40f653a01f4b4301a4b022418e2a52e8df431d79` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Observation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_quotient_barrier` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_quotient_barrier` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs)
- sha256 (`bytes`): `127c739edb34bb27c861a04090204049628934a3966c81bdbf1df33ab4a062dd`
- cited in: node.rust, record TFQ-0425

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `factor` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py)
- sha256 (`bytes`): `570c898692c070d22f655f96d74e0e468e1f4905ea52f917d28237056b7589c1`
- cited in: record TFQ-0425

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quotient_factor` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py)
- sha256 (`bytes`): `5bed3c5a8de7055ecba70dc88846ef73b3aed42cd7e713e08f6a3fd2e494d17e`
- cited in: record TFQ-0425
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_quotient_and_history_refuse_collapsed_answers` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md`

- file: [dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md](../../../dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md)
- sha256 (`lf-normalised`): `3ef23665fd16c4729b771a303bc8dd265a9b702772fcb2f7eed563d21fb0c5ae`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0425
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`

- file: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`

- file: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `DERIVED_LEAN`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN)

Outgoing (0):

