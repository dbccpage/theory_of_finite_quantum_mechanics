# PGW-GO-TWO-RELATIONS-SWAP

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The eighth derivation adds a second relation s beside r, and the ninth combines two relations with an empty beginning: a state has terms and a multiplicity table per relation. The two relations interact through the terms alone: an assertion of one leaves the other part as it is, a term or an identification acts on both, and a sequence projects to a sequence on either part. The seventh derivation's one-relation states embed with nothing in s (proj_ofR9_false, proj_ofR9_true), and the exchange of the two relations is an involution (swap9_swap) and a symmetry of the results, the cost and reachability (ledger D16, with Reach9.swap and reach9_swap).

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 4 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 4 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

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

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/Reach.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/Reach.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/State.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/State.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md`

- file: [dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md](../../../dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md)
- sha256 (`lf-normalised`): `4a6fe7e103158c7e8c6aa21505210ada0dd6a747c0b4b5fdc9cf63de8ce6162a`
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
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/Reach.lean::reach9_swap`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/State.lean::proj_ofR9_false`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/State.lean::proj_ofR9_true`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Ninth/State.lean::swap9_swap`

## Absences recorded by the TFQ records

- TFQ-0480 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-TWO-RELATIONS-SWAP` `DERIVED_LEAN`: [PGW-GO-MULTIPLICITY-MONOTONE](PGW-GO-MULTIPLICITY-MONOTONE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-ADMISSION-GATE` `DERIVED_PROSE`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)
