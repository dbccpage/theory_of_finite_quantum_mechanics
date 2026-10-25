# PGW-CAPABILITY-STAGE-COUNTER

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the stage index n of S(n): it counts licensed stage changes, each consuming one recorded challenge import (TFQ-0488), and not rounds or events. The second derivation's census motivates the choice: succession of accepted rounds is NOT FORCED under EVERY and CHANGING because one state is reached in five rounds and in six (SD-CF-3), so a round count is not a function of the state, while under the CHANGING reading (an accepted round after which the regime differs) the count is definable from base and regime, and from the regime alone when counted from the empty regime. In Lean, along any history of sealed events and switch markers the element count never falls, and a step or history that changes the regime raises it (estep_elems_lt_of_ne, ereplay_elems_lt_of_ne).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

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

### Lean: `lean4/Imported/Genesis19l57g1/SecondRun/Run.lean`

- file: [lean4/Imported/Genesis19l57g1/SecondRun/Run.lean](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)
- sha256 (`bytes`): `4db53efe47bb57435f39520ea44cacaab6e0a73f03f8a9e4d5a3fee64c44259e`
- cited in: node.lean, record TFQ-0491
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.SecondRun.Run`): recorded sha256 `4db53efe47bb57435f39520ea44cacaab6e0a73f03f8a9e4d5a3fee64c44259e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/SecondRun/Run.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ereplay_elems_lt_of_ne` | yes | yes | yes | Quot.sound, propext | `#print axioms ereplay_elems_lt_of_ne` |
| `estep_elems_lt_of_ne` | yes | yes | yes | Quot.sound, propext | `#print axioms estep_elems_lt_of_ne` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0491_capability_stage_counter.md`

- file: [dag/derivations/02_genesis/tfq_0491_capability_stage_counter.md](../../../dag/derivations/02_genesis/tfq_0491_capability_stage_counter.md)
- sha256 (`lf-normalised`): `868e8603f8d4909201a91075f773f5eec25867bdfcb215f08b00b960f899fd93`
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

## Absences recorded by the TFQ records

- TFQ-0491 rust: no Rust stage counter

## Routes

Incoming (1):

- `PGW-R-CAPABILITY-STAGE-COUNTER` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION), [PGW-RUNG6-SUCCESSION-ELEMENT-COUNT](PGW-RUNG6-SUCCESSION-ELEMENT-COUNT.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
