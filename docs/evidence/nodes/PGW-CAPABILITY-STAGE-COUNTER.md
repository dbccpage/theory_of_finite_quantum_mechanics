# PGW-CAPABILITY-STAGE-COUNTER

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the stage index n of S(n): it counts licensed stage changes, each consuming one recorded challenge import (TFQ-0488), and not rounds or events. The second derivation's census motivates the choice: succession of accepted rounds is NOT FORCED under EVERY and CHANGING because one state is reached in five rounds and in six (SD-CF-3), so a round count is not a function of the state, while under the CHANGING reading (an accepted round after which the regime differs) the count is definable from base and regime, and from the regime alone when counted from the empty regime. In Lean, along any history of sealed events and switch markers the element count never falls, and a step or history that changes the regime raises it (estep_elems_lt_of_ne, ereplay_elems_lt_of_ne).

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

- Stage index counting licensed stage changes, a construction declared by this programme (assumption)

## Bottleneck

A declared counter, not a derived invariant: no theorem makes a stage count a function of the state under EVERY or ADMITTING, and the education audit's link to nf.derivation.lsnf names a skeletal filtration form, not a stage counter.

## Source status

declared here; continuation.txt §3 definition 12 and §7 succession row (SD-CF-3); education archive §6 item 4

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0491_capability_stage_counter.md`

- file: [dag/derivations/02_genesis/tfq_0491_capability_stage_counter.md](../../../dag/derivations/02_genesis/tfq_0491_capability_stage_counter.md)
- sha256 (`lf-normalised`): `8e5b7284ab4c6a79c75cba2f5d3550140a1cb30b05befeeddc0e29ad2ceb262b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0491
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/succession.py::counts`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::ereplay_elems_lt_of_ne`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean::estep_elems_lt_of_ne`

## Absences recorded by the TFQ records

- TFQ-0491 rust: no Rust stage counter

## Routes

Incoming (1):

- `PGW-R-CAPABILITY-STAGE-COUNTER` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION), [PGW-RUNG6-SUCCESSION-ELEMENT-COUNT](PGW-RUNG6-SUCCESSION-ELEMENT-COUNT.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
