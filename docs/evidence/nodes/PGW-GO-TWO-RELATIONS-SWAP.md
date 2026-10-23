# PGW-GO-TWO-RELATIONS-SWAP

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The eighth derivation adds a second relation s beside r, and the ninth combines two relations with an empty beginning: a state has terms and a multiplicity table per relation. The two relations interact through the terms alone: an assertion of one leaves the other part as it is, a term or an identification acts on both, and a sequence projects to a sequence on either part. The seventh derivation's one-relation states embed with nothing in s (proj_ofR9_false, proj_ofR9_true), and the exchange of the two relations is an involution (swap9_swap) and a symmetry of the results, the cost and reachability (ledger D16, with Reach9.swap and reach9_swap).

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

None recorded.

## Bottleneck

proj_ofR9_false and proj_ofR9_true hold by rfl, so the embedding statements are definitional; the exchange symmetry is stated for the ninth seed's states, and later seeds that change the sameness re-prove it for their own (22:D10).

## Source status

001_genesis_ongoing_h3v7n5qf paper/ninth/claim_ledger.md D16 and D17; lean4/Ninth/State.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Ninth/Reach.lean`

- file: [lean4/Imported/GenesisOngoing/Ninth/Reach.lean](../../../lean4/Imported/GenesisOngoing/Ninth/Reach.lean)
- sha256 (`bytes`): `d6c935917fae01bc184e560e2332ff3fbd6d2ba5695d2211f421439e4a14827a`
- cited in: node.lean, record TFQ-0480
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Ninth.Reach`): recorded sha256 `d6c935917fae01bc184e560e2332ff3fbd6d2ba5695d2211f421439e4a14827a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Ninth/Reach.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `reach9_swap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach9_swap` |
- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Ninth/State.lean`

- file: [lean4/Imported/GenesisOngoing/Ninth/State.lean](../../../lean4/Imported/GenesisOngoing/Ninth/State.lean)
- sha256 (`bytes`): `9e9758caabc4303cdf8051c37ea6001e12448b2b4bde2798da2073a3a29d6433`
- cited in: node.lean, record TFQ-0480
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Ninth.State`): recorded sha256 `9e9758caabc4303cdf8051c37ea6001e12448b2b4bde2798da2073a3a29d6433` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Ninth/State.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `proj_ofR9_false` | yes | yes | yes | Quot.sound, propext | `#print axioms proj_ofR9_false` |
| `proj_ofR9_true` | yes | yes | yes | Quot.sound, propext | `#print axioms proj_ofR9_true` |
| `swap9_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms swap9_swap` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md`

- file: [dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md](../../../dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md)
- sha256 (`lf-normalised`): `78dbd947e9319edff0a5eae2db5a27a0cb532dfa0819339d369023ace52573e8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0480
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/ninth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/ninth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/genesis_ongoing.md`

- file: `omega_engine_education/documentation/005_oegenong/genesis_ongoing.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/ninth/state.py::of_s`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/ninth/state.py::swap`

## Absences recorded by the TFQ records

- TFQ-0480 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-TWO-RELATIONS-SWAP` `DERIVED_LEAN`: [PGW-GO-MULTIPLICITY-MONOTONE](PGW-GO-MULTIPLICITY-MONOTONE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-ADMISSION-GATE` `DERIVED_PROSE`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)
