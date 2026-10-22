# PGW-RESPONSE-EXISTENCE-MARK-PROGRESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On any well-formed regime whose imposed requirements are all separated, for any two distinct admitted data i and j, the two-item delta of one fresh unary form and one instance of it at datum j is a valid response to Separate(i, j) and keeps every imposed requirement separated (mark_progress). Derivability of instances of the old forms is unchanged by this extension, so old witnesses survive (derivable_extend). The standalone replay checks fresh-mark preservation for 3,996 targets across 1,436 regimes, and no terminal_no_response node occurs in any exported run.

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

This is response existence for a supplied demand only; it does not establish autonomous demand generation or an unbounded tower, and the preserved conjunct ranges over the requirement store, not over all separable pairs.

## Source status

genesis_source.txt section 8.2 \[theorem\] (CL-PROGRESS); Progress.lean mark_progress

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Progress.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Progress.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md`

- file: [dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md](../../../dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md)
- sha256 (`lf-normalised`): `29f3ce71754bca85aeee7ec8cdd052bebdb4443a964003f0dc803bab31af3c6b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0445
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Progress.lean::derivable_extend`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Progress.lean::mark_progress`

## Absences recorded by the TFQ records

- TFQ-0445 rust: no Rust check of fresh-mark progress; the standalone replay checks it against the frozen Python model

## Routes

Incoming (1):

- `PGW-R-RESPONSE-EXISTENCE-MARK-PROGRESS` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN), [PGW-RESPONSES-COSTS-MU1-MU2](PGW-RESPONSES-COSTS-MU1-MU2.md) (DEFINITION)

Outgoing (1):

- `PGW-R-PRUNING-LEMMAS-COST-TWO` `DERIVED_LEAN`: [PGW-PRUNING-LEMMAS-COST-TWO](PGW-PRUNING-LEMMAS-COST-TWO.md) (PROVED_LEAN)
