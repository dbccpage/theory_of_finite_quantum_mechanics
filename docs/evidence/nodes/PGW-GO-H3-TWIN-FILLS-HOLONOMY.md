# PGW-GO-H3-TWIN-FILLS-HOLONOMY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Climbing round H3 is two fills on the H2 carrier. In the twenty-fourth derivation a fifth change fills one term, and a filled term x balances exactly when its loop excess e(x,x) is zero, the same in every state of a result and every writing (balances_iff); a result is told from the one asserting nothing exactly when some filled term's loop excess is non-zero (told_iff). In the twenty-fifth a filled triple (x,y,z) balances when the sum around e(x,y) + e(y,z) + e(z,x) is zero, which the sameness keeps; a result is told exactly when some filled triple does not balance (nothing_balanced, told_iff), with three terms it is blind exactly when the sum around 0,1,2 is zero and the two-way sums add up to zero (blind_three_iff), and with every loop and two-way sum zero the triples through one term decide (cone_decides). A scratch rank computation of the sums around filled triples modulo raising gives 2 of 7 dimensions at three terms, 7 of 13 at four and 16 of 21 at five, only the loops unseen from five terms.

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

- `proved_lean_below_e3`: grade E0; 6 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 6 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- H2 sameness of the twenty-third derivation (Same3) as the carrier of both fills (assumption)

## Bottleneck

The ranks come from research/twentyfifth/scratch_rank.py, which labels itself scratch and not evidence; the general rank criterion C(n − 1, 2), the four-term blind converse and the counts are ledger row O2, proved in the paper and checked by computation up to five terms, with no Lean statement.

## Source status

001_genesis_ongoing_h3v7n5qf paper/twentyfourth/claim_ledger.md D2 and D4, paper/twentyfifth/claim_ledger.md D4, D6 and D7; lean4_core/Twentyfourth and Twentyfifth

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Balance.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Balance.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Blind.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Blind.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfourth/Same.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfourth/Same.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfourth/Tell.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfourth/Tell.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md`

- file: [dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md](../../../dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md)
- sha256 (`lf-normalised`): `b52bb6808efccc454f282751eba2719a4d58090a1eb7ceb5a43862643b49e1b1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0485
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfifth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfifth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfourth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfourth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/twentyfifth/reading_the_seed.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/twentyfifth/reading_the_seed.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfifth/told.py::decides`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfifth/told.py::rank`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfourth/state.py::balances`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Balance.lean::nothing_balanced`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Balance.lean::told_iff`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Blind.lean::blind_three_iff`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfifth/Blind.lean::cone_decides`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfourth/Same.lean::balances_iff`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentyfourth/Tell.lean::told_iff`

## Absences recorded by the TFQ records

- TFQ-0485 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-H3-TWIN-FILLS-HOLONOMY` `DERIVED_LEAN`: [PGW-GO-H2-STATE-RAISING-GAUGE](PGW-GO-H2-STATE-RAISING-GAUGE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-ONGOING-TO-WINDOW](PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.md) (OPEN)
