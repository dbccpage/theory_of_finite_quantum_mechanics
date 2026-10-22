# PGW-C2-RUN-FORWARD-EVERY-HISTORY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuation attempt two (pull request 269) takes Challenge 4 and runs every one of the 144 engines forward from both sealed readings to declared bounds (two items, growth below four data, fifteen rounds, a node guard of 250 per run): 288 runs, 25,932 nodes, 69,490 edges and 43,846 merges, every node and edge replayed and quotiented by the implemented isomorphism. In the local Lean package SecondRun/Run.lean, for every history of sealed events and switch markers from any engine state, the element count never falls (ereplay_elems_le), a history leaving it unchanged leaves the regime unchanged, no further history reaches a regime once left (no_return), and on a history returning to its starting state every state part of the way holds the starting regime (cycle_regime_const). A pair collapsed with a common third datum is not separable in that regime (not_separable_through), the shape of all 772 refused apart demands of the runs.

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

- Sealed kernel slice reconstructed verbatim in SecondRun/Kernel.lean from Derivation/Basic.lean and Derivation/Inertia.lean (assumption)
- Engine event grammar: a sealed event, or a switch marker that keeps the regime and flips the mode (assumption)

## Bottleneck

The Lean speaks of histories, not of the Python runs: that each run edge is such a history is read, not proved; the responder and generators are not reconstructed in Lean, not_separable_through is about one regime, and the run counts hold at the declared bounds only.

## Source status

lean4/SecondRun/Run.lean; continuation.txt section 4 row 4 and section 12 attempt two; run ledger SD-R-2 to SD-R-4

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0475_c2_run_forward_every_history.md`

- file: [dag/derivations/02_genesis/tfq_0475_c2_run_forward_every_history.md](../../../dag/derivations/02_genesis/tfq_0475_c2_run_forward_every_history.md)
- sha256 (`lf-normalised`): `c9a22fe9b5e12f14b0d301558b336067172c25a9f2d3a84eeb43adeca42ed00a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0475
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::build_run`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::replay_mismatches`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::cycle_regime_const`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::ereplay_elems_le`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::no_return`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::not_separable_through`

## Absences recorded by the TFQ records

- TFQ-0475 rust: the second-derivation run tree holds no Rust; the sealed Rust predates the switch marker

## Routes

Incoming (1):

- `PGW-R-C2-RUN-FORWARD-EVERY-HISTORY` `DERIVED_LEAN`: [PGW-C1-ENGINE-CLASS-144](PGW-C1-ENGINE-CLASS-144.md) (CONDITIONAL), [PG-GEN-NO-RETURN](PG-GEN-NO-RETURN.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-FORCED-CENSUS-COLUMN` `COMPUTED`: [PGW-FORCED-CENSUS-COLUMN](PGW-FORCED-CENSUS-COLUMN.md) (COMPUTATIONALLY_CHECKED)
