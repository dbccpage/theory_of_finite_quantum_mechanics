# PGW-K-ITEM-DELTA-GRAMMAR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed candidate space is enumerated to cost two (at most two items, arity at most two), with pruning lemmas certified against the unpruned space: unreferenced fresh data and forms never matter, an instance-only delta changes the target pair's profiles only if an instance mentions a target datum, and a delta holding a uniform-rule item is never a minimum valid response (rule_item_never_minimal). The second derivation's rung one enumerated three-item deltas (min_responses_three) under a node guard, but no k-item delta grammar with pruning lemmas proved beyond cost two exists, and the distance bound of two is not known to be the grammar's (S-4). The education audit lists k-item delta grammars with pruning lemmas as a missing prerequisite of the S(n) bridge. Narrowed in Lean 4 to one empty base with two data and arity one. Over a 10-atom universe, the well-formed admissions of one item are a fresh datum and one unary form, and the well-formed admissions of two items are datum-then-datum, datum-then-form, form-then-datum, form-then-form, form-then-rule, form-then-instance of argument 0, and form-then-instance of argument 1. That census has 9 well-formed deltas, and 7 of them leave the two target profile bits equal. The two form-then-instance deltas leave those bits unequal. The form-then-rule delta sets both bits true. Extending the argument-0 instance by the uniform rule makes a 3-item delta whose bits are equal, while the 2-item prefix has unequal bits. A fresh datum, then a form, then an instance of argument 2, keeps both target bits false and records that fresh argument. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum on the full unpruned space stay open. The mention file and the rule-bridge file are not rechecked. AuthorityEffect is None.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 28
- cited Lean declarations covered by a current replay receipt: 28
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open: the cost-two minimum (CL-3-MIN-TWO) is relative to the sealed grammar and bounds, and nothing here establishes a k-item minimum or a bound on response size. This file checks one empty base with two data and arity one: 9 well-formed deltas of at most two items, 2 of them with unequal target bits. The 3-item rule extension equalizes those bits, and an instance of argument 2 keeps them false. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum stay open.

## Source status

continuation.txt §13 Responses in Lean (S-4); genesis_source.txt §8.3 pruning lemmas; education archive §6 item 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwKItemDeltaGrammar.lean`

- file: [lean4/CampaignPgwKItemDeltaGrammar.lean](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- sha256 (`bytes`): `9c9138a0fe4c8f8481789c6560ebf5a4c301a440ebf76bd0658c80be07f05670`
- cited in: node.lean, receipt dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json (CampaignPgwKItemDeltaGrammar), receipt dag/research/pr_350_review_replay.json (CampaignPgwKItemDeltaGrammar), record TFQ-0490
- replay: `verified`
  - receipt [dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json](../../../dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json) (module `CampaignPgwKItemDeltaGrammar`): recorded sha256 `9c9138a0fe4c8f8481789c6560ebf5a4c301a440ebf76bd0658c80be07f05670` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_350_review_replay.json](../../../dag/research/pr_350_review_replay.json) (module `CampaignPgwKItemDeltaGrammar`): recorded sha256 `9c9138a0fe4c8f8481789c6560ebf5a4c301a440ebf76bd0658c80be07f05670` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwKItemDeltaGrammar`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignPgwKItemDeltaGrammar.form_rule_both_true` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.form_rule_both_true` |
| `CampaignPgwKItemDeltaGrammar.fresh_datum_pairs_do_not_separate` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.fresh_datum_pairs_do_not_separate` |
| `CampaignPgwKItemDeltaGrammar.nine_well_formed` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.nine_well_formed` |
| `CampaignPgwKItemDeltaGrammar.no_single_item_separates` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.no_single_item_separates` |
| `CampaignPgwKItemDeltaGrammar.off_target_instance_keeps_bits` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.off_target_instance_keeps_bits` |
| `CampaignPgwKItemDeltaGrammar.one_hundred_pairs` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.one_hundred_pairs` |
| `CampaignPgwKItemDeltaGrammar.rule_extension_equalizes` | yes | yes | yes | propext | `#print axioms CampaignPgwKItemDeltaGrammar.rule_extension_equalizes` |
| `CampaignPgwKItemDeltaGrammar.rule_extension_is_longer` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.rule_extension_is_longer` |
| `CampaignPgwKItemDeltaGrammar.separating_pairs_are_two` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.separating_pairs_are_two` |
| `CampaignPgwKItemDeltaGrammar.seven_leave_bits_equal` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.seven_leave_bits_equal` |
| `CampaignPgwKItemDeltaGrammar.ten_atoms` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.ten_atoms` |
| `CampaignPgwKItemDeltaGrammar.well_formed_pairs_are` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.well_formed_pairs_are` |
| `CampaignPgwKItemDeltaGrammar.well_formed_singles_are` | yes | yes | yes | none | `#print axioms CampaignPgwKItemDeltaGrammar.well_formed_singles_are` |
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

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-k-item-delta-grammar.py`

- file: [checks/independent/pgw-k-item-delta-grammar.py](../../../checks/independent/pgw-k-item-delta-grammar.py)
- sha256 (`bytes`): `2591814ebe23b01a3a4e8f1983ba9f3276f8b82b6ab2bb66a6cd17e5928f735f`
- cited in: record TFQ-0490
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md`

- file: [dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md](../../../dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md)
- sha256 (`lf-normalised`): `3145e4349c8d32c31de549722b19f18b45fe7b070005421bec14b35eac45989a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0490
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py::iter_k_item_deltas`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::iter_cost2_deltas`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs::iter_cost2_deltas`

## Routes

Incoming (1):

- `PGW-R-K-ITEM-DELTA-GRAMMAR` `GAP_NO_DERIVATION`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)

Outgoing (1):

- `PGW-R-RESPONDER-IN-LEAN` `GAP_NO_DERIVATION`: [PGW-RESPONDER-IN-LEAN](PGW-RESPONDER-IN-LEAN.md) (OPEN)
