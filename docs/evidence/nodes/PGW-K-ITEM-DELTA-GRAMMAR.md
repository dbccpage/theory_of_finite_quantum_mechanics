# PGW-K-ITEM-DELTA-GRAMMAR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN: the four declared Challenge 3 lists copied from deltaU0, deltaU1, deltaBL, and deltaBD each have length 2. Their new-form arities are 1, 1, 2, and 2, and the sum of those arities is 6. The argument lists are \[0\], \[1\], \[0, 1\], and \[0, 0\], and the four lists are pairwise distinct across 6 comparisons. One three-item list has length 3, and 3 \> 2. This census is those four named lists. A k-item grammar for k at least 3, an exhaustive cost-two enumeration, and a response-size bound stay open. Status stays OPEN.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The four lists are a copied census of deltaU0, deltaU1, deltaBL, and deltaBD. They are not an exhaustive enumeration of the sealed candidate space, and they do not define a k-item grammar for k at least 3. The cost-two minimum CL-3-MIN-TWO stays relative to the sealed grammar. A bound on response size stays open. Status stays OPEN.

## Source status

continuation.txt §13 Responses in Lean (S-4); genesis_source.txt §8.3 pruning lemmas; education archive §6 item 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwKItemDeltaGrammar.lean`

- file: [lean4/CampaignPgwKItemDeltaGrammar.lean](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- sha256 (`bytes`): `ec5e9fc278a581722704503dcc453a9421c86e63da5a3fdb90f04de94ccf3e9b`
- cited in: node.lean, receipt dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json (CampaignPgwKItemDeltaGrammar), record TFQ-0490
- replay: `verified`
  - receipt [dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json](../../../dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json) (module `CampaignPgwKItemDeltaGrammar`): recorded sha256 `ec5e9fc278a581722704503dcc453a9421c86e63da5a3fdb90f04de94ccf3e9b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwKItemDeltaGrammar`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwKItem_arities` | yes | yes | yes | propext | `#print axioms pgwKItem_arities` |
| `pgwKItem_arity_sum` | yes | yes | yes | propext | `#print axioms pgwKItem_arity_sum` |
| `pgwKItem_lengths` | yes | yes | yes | none | `#print axioms pgwKItem_lengths` |
| `pgwKItem_pairwise` | yes | yes | yes | none | `#print axioms pgwKItem_pairwise` |
| `pgwKItem_three_above_two` | yes | yes | yes | none | `#print axioms pgwKItem_three_above_two` |
| `pgwKItem_three_length` | yes | yes | yes | none | `#print axioms pgwKItem_three_length` |
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
- sha256 (`bytes`): `048ddb8b3ae5710effa3e2d9bd5a7a93292dc538985715577e8aa0d6d6c8d3d2`
- cited in: record TFQ-0490
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md`

- file: [dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md](../../../dag/derivations/02_genesis/tfq_0490_k_item_delta_grammar.md)
- sha256 (`lf-normalised`): `d0ece8cc3fbdbd34e17356f4e8418b22e29ed73b183a634c7d8824366b6d7b84`
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
