# PGW-GO-LEFTOVER-UNBOUNDEDNESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The tenth derivation records a leftover with each change in a side ledger and keeps the ninth's state model; the sixteenth admits the recorded leftover back into the state. The feedback does not terminate: remove-then-admit is a two-change cycle at every state with an assertion, and a term added and identified away is one at every state with a term, while the ninth's add-then-remove is not a cycle. In Lean, if Reach16 s t n holds from a well-formed state with a term then Reach16 s t (2k + n) holds for every k (Reach16.unbounded), and ara reaches itself in 2k changes by removing and admitting for every k (admit_remove_unbounded), so the lengths of sequences reaching a result are unbounded.

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

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

Unbounded lengths of sequences reaching a result, not an unbounded set of results; the fewest changes to a result stays its potential (ledger D3), and nothing here is a claim about time or physical recurrence.

## Source status

001_genesis_ongoing_h3v7n5qf paper/sixteenth/claim_ledger.md D9; lean4/Sixteenth/Reach.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/Reach.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/Reach.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0482_go_leftover_unboundedness.md`

- file: [dag/derivations/02_genesis/tfq_0482_go_leftover_unboundedness.md](../../../dag/derivations/02_genesis/tfq_0482_go_leftover_unboundedness.md)
- sha256 (`lf-normalised`): `45408cb6696c286e8765f6624e795fd2a9bfa27ca602ef7b1e81b848c15683a1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0482
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/sixteenth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/sixteenth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_18_leftovers_unboundedness.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_18_leftovers_unboundedness.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/sixteenth/reach.py::reachable16`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/Reach.lean::Reach16.unbounded`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/Reach.lean::admit_remove_unbounded`

## Absences recorded by the TFQ records

- TFQ-0482 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-LEFTOVER-UNBOUNDEDNESS` `DERIVED_LEAN`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (2):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-GO-H1-CANCELLATION-EXCESS` `DERIVED_LEAN`: [PGW-GO-H1-CANCELLATION-EXCESS](PGW-GO-H1-CANCELLATION-EXCESS.md) (PROVED_LEAN)
