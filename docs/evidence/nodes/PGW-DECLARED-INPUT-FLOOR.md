# PGW-DECLARED-INPUT-FLOOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No floor proof exists for the count of declared inputs (D10, H-1); the count stays two. Continuation attempt two found, at its declared bounds (fifteen rounds, a node guard of 250 per run, growth below four data, two items) and under its literal reading of carrying forward, four engines that carry the grammar forward declaring the stake and not the stream (SD-R-11), and calls this neither a floor proof nor a reduction outside those bounds. The completion-gate clause admits two readings of these bounded one-input carriers and was frozen as NOT_ESTABLISHED; whether the four carry forward past the bounds is OPEN (H-1, which needs the responder in Lean).

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; the bounded one-input carriers are a computation at declared bounds, and the clause's other reading was left to the author, who approved the freeze without a separate ruling.

## Source status

closeout.txt §9.1 D10 and §8; continuation.txt §13 declared-input floor (H-1)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0498_declared_input_floor.md`

- file: [dag/derivations/02_genesis/tfq_0498_declared_input_floor.md](../../../dag/derivations/02_genesis/tfq_0498_declared_input_floor.md)
- sha256 (`lf-normalised`): `3061f9b5101c7f9769bd48eef22a888afbd7d421d9fb6abf4a41aa539a735627`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0498
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::carries_forward`

## Absences recorded by the TFQ records

- TFQ-0498 lean4: no Lean statement of a declared-input floor
- TFQ-0498 rust: no Rust check of the input count

## Routes

Incoming (1):

- `PGW-R-DECLARED-INPUT-FLOOR` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

