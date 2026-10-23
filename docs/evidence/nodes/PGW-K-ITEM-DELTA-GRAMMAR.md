# PGW-K-ITEM-DELTA-GRAMMAR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed candidate space is enumerated to cost two (at most two items, arity at most two), with pruning lemmas certified against the unpruned space: unreferenced fresh data and forms never matter, an instance-only delta changes the target pair's profiles only if an instance mentions a target datum, and a delta holding a uniform-rule item is never a minimum valid response (rule_item_never_minimal). The second derivation's rung one enumerated three-item deltas (min_responses_three) under a node guard, but no k-item delta grammar with pruning lemmas proved beyond cost two exists, and the distance bound of two is not known to be the grammar's (S-4). The education audit lists k-item delta grammars with pruning lemmas as a missing prerequisite of the S(n) bridge.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open: the cost-two minimum (CL-3-MIN-TWO) is relative to the sealed grammar and bounds, and nothing here establishes a k-item minimum or a bound on response size.

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

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md`

- file: [dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md](../../../dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md)
- sha256 (`lf-normalised`): `f9687728365f9265ab6ea21d1d77ad28f27a1f6baa537daedc4edb743aef2868`
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
