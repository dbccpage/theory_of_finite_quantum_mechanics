# PGW-GO-REACH-CEILING

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the base genesis-ongoing seed (terms a and b, arb asserted, xrx forbidden; the changes are identification, removal, adding a term and adding an assertion), ledger row D9 says every finite legal state with at least one term, names anywhere, is a result under either beginning. The Lean edit path reach_by_edits reaches a legal well-formed goal that contains the start's terms and keeps its names, by removing what the goal does not assert, adding the missing terms and adding the missing assertions, in that many changes; givenA_to_oneTerm and givenB_to_oneTerm reach the one-term result in two and three changes. Row N5 is the expressive ceiling that follows from D9: no statement about the asserting that holds in one finite legal state and fails in another follows from the seed.

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared exploration bound C8 (at most 5 terms FREE, 4 terms ANCHORED) for the computed half of D9 (assumption)

## Bottleneck

The Lean witnesses fix the names at a = 0, b = 1 or a = b = 0; names elsewhere rest on the rewriting step that ledger row O3 tracks (TFQ-0390), and the computed half of D9 stops at the declared term bound.

## Source status

001_genesis_ongoing_h3v7n5qf paper/claim_ledger.md rows D9 and N5; lean4/H3V7N5QF/Paths.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0477_go_reach_ceiling.md`

- file: [dag/derivations/02_genesis/tfq_0477_go_reach_ceiling.md](../../../dag/derivations/02_genesis/tfq_0477_go_reach_ceiling.md)
- sha256 (`lf-normalised`): `510aecfcf9e2484bd86d5639ea2ff12ac0af5a6c5156bb45e67ff2a5c809e45b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0477
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_07_graph_reachability_closure.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_07_graph_reachability_closure.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/xry/explore.py::explore`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean::givenA_to_oneTerm`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean::givenB_to_oneTerm`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean::reach_by_edits`

## Absences recorded by the TFQ records

- TFQ-0477 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-REACH-CEILING` `DERIVED_LEAN`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-CONTRACTION-STEP2-STEP3` `DERIVED_LEAN`: [PGW-GO-CONTRACTION-STEP2-STEP3](PGW-GO-CONTRACTION-STEP2-STEP3.md) (PROVED_LEAN)
