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

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Quot.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Quot.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Quot.lean)
- sha256 (`bytes`): `8336fd5a34d1c54d909f648f7f528dc24c17696f9376c05610e0c80f3da564de`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Quot`): recorded sha256 `8336fd5a34d1c54d909f648f7f528dc24c17696f9376c05610e0c80f3da564de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Quot.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quotient_barrier` | yes | yes | yes | Quot.sound | `#print axioms quotient_barrier` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Paper000.lean`

- file: [lean4/Imported/GenesisDerivation/Paper000.lean](../../../lean4/Imported/GenesisDerivation/Paper000.lean)
- sha256 (`bytes`): `9a0973383847018f21e8dbd13ceadda298a6cdbd10321d4bfa7eabf1a1e76d04`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.GenesisDerivation.Paper000`): recorded sha256 `9a0973383847018f21e8dbd13ceadda298a6cdbd10321d4bfa7eabf1a1e76d04` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Paper000.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `separation_not_on_quotient` | yes | yes | yes | none | `#print axioms separation_not_on_quotient` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Observation.lean`

- file: [lean4/Imported/PreGenesisToMssn/Observation.lean](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)
- sha256 (`bytes`): `ccbdc2919571c7267a4dc3697bf9b59bbbaa4e37481a731dd6649ebdefce12e1`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Observation`): recorded sha256 `ccbdc2919571c7267a4dc3697bf9b59bbbaa4e37481a731dd6649ebdefce12e1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
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
- sha256 (`lf-normalised`): `9f9870c26792172efdb98e78f65a8b53e5398e4f2f8b8b59664819c6d5c6d1e9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0425
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149:283-305`
- `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:81-88`

## Routes

Incoming (1):

- `PGW-R-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `DERIVED_LEAN`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN)

Outgoing (0):

