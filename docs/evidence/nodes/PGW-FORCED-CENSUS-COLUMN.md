# PGW-FORCED-CENSUS-COLUMN

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuation attempt two decides the FORCED column of all twelve rows of the definability census over the declared engine class at its bounds (rounds zero to fifteen, both readings), each NOT FORCED verdict naming a first failing engine and a path of its run. The element count and irreversibility are FORCED, at the bounds by computation and beyond them by the every-history theorems, every cycle of every run being made of switch edges; two-ness is FORCED over the 64 LIVE engines, every path holding two before any bound or guard node. Every other row (the observational class count, succession, duration, adjacency, reach, symmetry, branching, exhaustion and recurrence) is NOT FORCED with an executable countermodel; one state of one run is reached in five rounds and in six, so succession and duration are not functions of the state.

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

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Declared engine class of continuation attempt one, 144 members, run from both sealed readings (assumption)
- Declared policy of how the runs read the DEFINABLE and USEFUL REALIZATION columns (SD-R-14) (assumption)

## Bottleneck

Verdicts other than the element count, irreversibility and two-ness over the LIVE members are computations at fifteen rounds and a guard of 250; whether the four streamless E4 carriers continue past the bounds is OPEN (H-1), and two is not shown to be the floor of declared inputs.

## Source status

continuation.txt section 7 table and section 11; run ledger SD-CF-1 to SD-CF-12; finite computation with two rows proved for every history

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0476_forced_census_column.md`

- file: [dag/derivations/02_genesis/tfq_0476_forced_census_column.md](../../../dag/derivations/02_genesis/tfq_0476_forced_census_column.md)
- sha256 (`lf-normalised`): `c1bc0da54543ab0bccbc0543b4705956fabf8b04f7b787c5419c668f7d16376c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0476
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_census.py::forced_over`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_census.py::stage_verdict`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::ereplay_elems_le`

## Absences recorded by the TFQ records

- TFQ-0476 rust: the second-derivation run tree holds no Rust

## Routes

Incoming (1):

- `PGW-R-FORCED-CENSUS-COLUMN` `COMPUTED`: [PGW-C2-RUN-FORWARD-EVERY-HISTORY](PGW-C2-RUN-FORWARD-EVERY-HISTORY.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GENESIS-FREEZE-ENDPOINT-LEDGER` `DERIVED_PROSE`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)
