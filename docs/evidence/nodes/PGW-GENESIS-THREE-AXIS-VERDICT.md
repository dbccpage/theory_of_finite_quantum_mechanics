# PGW-GENESIS-THREE-AXIS-VERDICT

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The final source closeout records three independent axes after the author's 2026-09-28 freeze of snapshot 90ab34a0: research_phase CLOSED_WITH_OPEN_OBSTRUCTIONS, alpha_reference READY_WITHIN_DECLARED_SCOPE and original_seed_completion_gate UNSATISFIED, the last with its live-injection and comparison clauses unmet and the input-count floor NOT_ESTABLISHED. A source defect stays on the record: delta_events names a fresh datum w\<n\> from the current datum count, so when the sole admitted token is w1 a NewDatum item emits AdmitDatum(w1) and deduplication leaves the state unchanged; the standalone replay reproduces this. Pinned Lean modules use only propext and Quot.sound, companion results such as the carrier-general image factorization also use Classical.choice, and the compiled census reports 2,475 non-internal theorem constants. Native Rust and frozen Python agree on every context observation and portable key over 1,436 regimes, and the compiled Lean wire encoder agrees with Python on 1,439 tuples.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

The axis values are recorded author-approved verdicts, not computed results: a closed stage does not imply readiness, companion work does not rewrite the frozen gate, and finite agreement is not a compiler-verified refinement proof for all source code.

## Source status

closeout.txt section 10 recorded verdicts; paper.md section 12 defect and agreement counts (ledger WDP-P000-023, -024)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/bin/genesis_replay.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/bin/genesis_replay.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0461_genesis_three_axis_verdict.md`

- file: [dag/derivations/02_genesis/tfq_0461_genesis_three_axis_verdict.md](../../../dag/derivations/02_genesis/tfq_0461_genesis_three_axis_verdict.md)
- sha256 (`lf-normalised`): `ecec88c9517a4843cabf72b5d6972c8a341f92695523ece754e0dd0524c50413`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0461
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::delta_events`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::compare_rust`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/bin/genesis_replay.rs::run`

## Absences recorded by the TFQ records

- TFQ-0461 lean4: no Lean statement of the verdicts or of the fresh-label defect; the axiom census is the compiled lean4/axiom_report.txt

## Routes

Incoming (1):

- `PGW-R-GENESIS-THREE-AXIS-VERDICT` `COMPUTED`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-GENESIS-FREEZE-ENDPOINT-LEDGER` `DERIVED_PROSE`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)
- `PGW-R-RUNG0-INHERITANCE-REPLAY` `COMPUTED`: [PGW-RUNG0-INHERITANCE-REPLAY](PGW-RUNG0-INHERITANCE-REPLAY.md) (COMPUTATIONALLY_CHECKED)
