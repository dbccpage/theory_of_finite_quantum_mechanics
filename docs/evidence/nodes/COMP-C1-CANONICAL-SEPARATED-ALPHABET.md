# COMP-C1-CANONICAL-SEPARATED-ALPHABET

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every n, the regime with n data, n-1 unary forms and the instances (i,\[i\]) is pairwise separated under the unary separation mirror UnarySep, which is decidable with Collapsed and PairwiseSeparated; two admitted marks with no form are collapsed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- UnarySep as a mirror of the unary hole-only separable

## Bottleneck

UnarySep is a mirror of the hole-only unary case of the Genesis separable, not the external definition; the lift to all contexts including uniform rules is not done.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C1b claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1284
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonicalRegime_four_pairwise_decide` | yes | yes | yes | Quot.sound, propext | `#print axioms canonicalRegime_four_pairwise_decide` |
| `canonicalRegime_pairwise` | yes | yes | yes | Quot.sound, propext | `#print axioms canonicalRegime_pairwise` |
| `pairwiseSeparated_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms pairwiseSeparated_iff` |
| `two_marks_without_forms_collapsed` | yes | yes | yes | Quot.sound, propext | `#print axioms two_marks_without_forms_collapsed` |
| `unarySep_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms unarySep_iff` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1284

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonical_regime` (rust_symbol) | yes | yes | yes | - | - |
| `collapsed` (rust_symbol) | yes | yes | yes | - | - |
| `pairwise_separated` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1284

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonical_regime` (python_symbol) | yes | yes | yes | - | - |
| `collapsed` (python_symbol) | yes | yes | yes | - | - |
| `pairwise_separated` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1284_comp_c1_canonical_separated_alphabet.md`

- file: [dag/derivations/29_computation/tfq_1284_comp_c1_canonical_separated_alphabet.md](../../../dag/derivations/29_computation/tfq_1284_comp_c1_canonical_separated_alphabet.md)
- sha256 (`lf-normalised`): `46fa853f954dbfab626d2a0ee5217cf207f553a03bccbb4672602abcc533c4f1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1284
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C1-CANONICAL-SEPARATED-ALPHABET` `DERIVED_LEAN`: [COMP-C1-FIRST-SEPARATION-REPLAY](COMP-C1-FIRST-SEPARATION-REPLAY.md) (COMPUTATIONALLY_CHECKED), [PG-GEN-IRREFLEXIVE-DISTINCT](PG-GEN-IRREFLEXIVE-DISTINCT.md) (PROVED_LEAN)

Outgoing (4):

- `APP-R-COMP-C2-WORD-REWRITING` `DERIVED_PROSE`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION)
- `APP-R-COMP-C5-MARK-BUDGET-RULE-LIST` `DERIVED_LEAN`: [COMP-C5-MARK-BUDGET-RULE-LIST](COMP-C5-MARK-BUDGET-RULE-LIST.md) (PROVED_LEAN)
- `APP-R-COMP-C5-TM0-STEP-SIMULATION` `DERIVED_LEAN`: [COMP-C5-TM0-STEP-SIMULATION](COMP-C5-TM0-STEP-SIMULATION.md) (PROVED_LEAN)
- `APP-R-COMP-C8-BINARY-CODING` `DERIVED_LEAN`: [COMP-C8-BINARY-CODING](COMP-C8-BINARY-CODING.md) (PROVED_LEAN)
