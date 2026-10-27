# PGW-K-ITEM-DELTA-GRAMMAR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed candidate space is enumerated to cost two (at most two items, arity at most two), with pruning lemmas certified against the unpruned space: unreferenced fresh data and forms never matter, an instance-only delta changes the target pair's profiles only if an instance mentions a target datum, and a delta holding a uniform-rule item is never a minimum valid response (rule_item_never_minimal). The second derivation's rung one enumerated three-item deltas (min_responses_three) under a node guard, but no k-item delta grammar with pruning lemmas proved beyond cost two exists, and the distance bound of two is not known to be the grammar's (S-4). The education audit lists k-item delta grammars with pruning lemmas as a missing prerequisite of the S(n) bridge.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 30
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open: the cost-two minimum (CL-3-MIN-TWO) is relative to the sealed grammar and bounds, and nothing here establishes a k-item minimum or a bound on response size. This file checks one empty base with two data and arity one: 9 well-formed deltas of at most two items, 2 of them with unequal target bits. The 3-item rule extension equalizes those bits, and an instance of argument 2 keeps them false. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum stay open. Checked slice, status unchanged. Narrowed in Lean 4 to one empty base with two data and arity one. Over a 10-atom universe, the well-formed admissions of one item are a fresh datum and one unary form, and the well-formed admissions of two items are datum-then-datum, datum-then-form, form-then-datum, form-then-form, form-then-rule, form-then-instance of argument 0, and form-then-instance of argument 1. That census has 9 well-formed deltas, and 7 of them leave the two target profile bits equal. The two form-then-instance deltas leave those bits unequal. The form-then-rule delta sets both bits true. Extending the argument-0 instance by the uniform rule makes a 3-item delta whose bits are equal, while the 2-item prefix has unequal bits. A fresh datum, then a form, then an instance of argument 2, keeps both target bits false and records that fresh argument. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum on the full unpruned space stay open. The mention file and the rule-bridge file are not rechecked. AuthorityEffect is None.

## Source status

continuation.txt §13 Responses in Lean (S-4); genesis_source.txt §8.3 pruning lemmas; education archive §6 item 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Mention.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Mention.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- sha256 (`bytes`): `73f4b5ee8c91290124be0c39541217256f2ec47e26d23b887fa40f8ba9b97f38`
- cited in: node.lean, record TFQ-0490
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Mention`): recorded sha256 `73f4b5ee8c91290124be0c39541217256f2ec47e26d23b887fa40f8ba9b97f38` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Mention.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_fresh_datum` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_fresh_datum` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean)
- sha256 (`bytes`): `2f5e9cbd5fa01227b953951195d39129ad389ccad6d9098a99ac78920356f467`
- cited in: node.lean, record TFQ-0490
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.RuleBridge`): recorded sha256 `2f5e9cbd5fa01227b953951195d39129ad389ccad6d9098a99ac78920356f467` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rule_item_never_minimal` | yes | yes | yes | propext | `#print axioms rule_item_never_minimal` |

- counts toward the grade: yes

### Lean: `lean4/PregenesisKItemDeltaGrammar.lean`

- file: [lean4/PregenesisKItemDeltaGrammar.lean](../../../lean4/PregenesisKItemDeltaGrammar.lean)
- sha256 (`bytes`): `52b73aa3de75fa53ed068550450f0c7b6cbceb0646de2a6b9633ae16914f996b`
- cited in: node.lean, receipt dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json (PregenesisKItemDeltaGrammar), receipt dag/research/pr_350_review_replay.json (PregenesisKItemDeltaGrammar), record TFQ-0490
- replay: `verified`
  - receipt [dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json](../../../dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json) (module `PregenesisKItemDeltaGrammar`): recorded sha256 `52b73aa3de75fa53ed068550450f0c7b6cbceb0646de2a6b9633ae16914f996b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_350_review_replay.json](../../../dag/research/pr_350_review_replay.json) (module `PregenesisKItemDeltaGrammar`): recorded sha256 `52b73aa3de75fa53ed068550450f0c7b6cbceb0646de2a6b9633ae16914f996b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisKItemDeltaGrammar`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PregenesisKItemDeltaGrammar.form_rule_both_true` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.form_rule_both_true` |
| `PregenesisKItemDeltaGrammar.fresh_datum_pairs_do_not_separate` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.fresh_datum_pairs_do_not_separate` |
| `PregenesisKItemDeltaGrammar.nine_well_formed` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.nine_well_formed` |
| `PregenesisKItemDeltaGrammar.no_single_item_separates` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.no_single_item_separates` |
| `PregenesisKItemDeltaGrammar.off_target_instance_keeps_bits` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.off_target_instance_keeps_bits` |
| `PregenesisKItemDeltaGrammar.one_hundred_pairs` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.one_hundred_pairs` |
| `PregenesisKItemDeltaGrammar.rule_extension_equalizes` | yes | yes | yes | propext | `#print axioms PregenesisKItemDeltaGrammar.rule_extension_equalizes` |
| `PregenesisKItemDeltaGrammar.rule_extension_is_longer` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.rule_extension_is_longer` |
| `PregenesisKItemDeltaGrammar.separating_pairs_are_two` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.separating_pairs_are_two` |
| `PregenesisKItemDeltaGrammar.seven_leave_bits_equal` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.seven_leave_bits_equal` |
| `PregenesisKItemDeltaGrammar.ten_atoms` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.ten_atoms` |
| `PregenesisKItemDeltaGrammar.well_formed_pairs_are` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.well_formed_pairs_are` |
| `PregenesisKItemDeltaGrammar.well_formed_singles_are` | yes | yes | yes | none | `#print axioms PregenesisKItemDeltaGrammar.well_formed_singles_are` |
| `form_rule_both_true` | yes | yes | yes | none | `#print axioms form_rule_both_true` |
| `fresh_datum_pairs_do_not_separate` | yes | yes | yes | none | `#print axioms fresh_datum_pairs_do_not_separate` |
| `nine_well_formed` | yes | yes | yes | none | `#print axioms nine_well_formed` |
| `no_single_item_separates` | yes | yes | yes | none | `#print axioms no_single_item_separates` |
| `off_target_instance_keeps_bits` | yes | yes | yes | none | `#print axioms off_target_instance_keeps_bits` |
| `one_hundred_pairs` | yes | yes | yes | none | `#print axioms one_hundred_pairs` |
| `rule_extension_equalizes` | yes | yes | yes | propext | `#print axioms rule_extension_equalizes` |
| `rule_extension_is_longer` | yes | yes | yes | none | `#print axioms rule_extension_is_longer` |
| `separating_pairs_are_two` | yes | yes | yes | none | `#print axioms separating_pairs_are_two` |
| `seven_leave_bits_equal` | yes | yes | yes | none | `#print axioms seven_leave_bits_equal` |
| `ten_atoms` | yes | yes | yes | none | `#print axioms ten_atoms` |
| `well_formed_pairs_are` | yes | yes | yes | none | `#print axioms well_formed_pairs_are` |
| `well_formed_singles_are` | yes | yes | yes | none | `#print axioms well_formed_singles_are` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/enumeration.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/enumeration.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/enumeration.rs)
- sha256 (`bytes`): `a829a2a7ef365ce27b07cbd4d2fc3069f7b0653ce7a2a82fd3e5cd437407708a`
- cited in: node.rust, record TFQ-0490

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `iter_cost2_deltas` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0490

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `iter_cost2_deltas` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-k-item-delta-grammar.py`

- file: [checks/independent/pgw-k-item-delta-grammar.py](../../../checks/independent/pgw-k-item-delta-grammar.py)
- sha256 (`bytes`): `2591814ebe23b01a3a4e8f1983ba9f3276f8b82b6ab2bb66a6cd17e5928f735f`
- cited in: record TFQ-0490
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md`

- file: [dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md](../../../dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md)
- sha256 (`lf-normalised`): `64e4774a0913c6c8287c37b6e2d801af16d9c5a98cdabd053e99e2f0b35fbcf9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0490
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py::iter_k_item_deltas`

## Routes

Incoming (1):

- `PGW-R-K-ITEM-DELTA-GRAMMAR` `GAP_NO_DERIVATION`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)

Outgoing (1):

- `PGW-R-RESPONDER-IN-LEAN` `GAP_NO_DERIVATION`: [PGW-RESPONDER-IN-LEAN](PGW-RESPONDER-IN-LEAN.md) (OPEN)
