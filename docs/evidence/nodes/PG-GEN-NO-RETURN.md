# PG-GEN-NO-RETURN

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Along the admitted closure rounds the element count is cumulative and a regime once left is not returned to; cycle regimes are constant (cycle_regime_const).

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

Not covered by the PFP review: Prove the complete array-to-source Regime interpreter refinement and that every real source regime change strictly raises the source potential. A count comparison alone is not that refinement.

## Source status

Rounds / no-return / cumulative element count (Genesis §8-§9)

## Review

- PFP review: [dag/results/PG-GEN-NO-RETURN/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-NO-RETURN/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual guarded regime traces, duplicate/no-op controls and two-switch mode cycles are retained; conditional count no-return/cycle lemmas are kernel checked.
  - does not support: Prove the complete array-to-source Regime interpreter refinement and that every real source regime change strictly raises the source potential. A count comparison alone is not that refinement.
  - next test: Prove the complete array-to-source Regime interpreter refinement and that every real source regime change strictly raises the source potential. A count comparison alone is not that refinement.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0384_cumulative_count_no_return.md`

- file: [dag/derivations/02_genesis/tfq_0384_cumulative_count_no_return.md](../../../dag/derivations/02_genesis/tfq_0384_cumulative_count_no_return.md)
- sha256 (`lf-normalised`): `87319e2ba3f4033aa40fa531d480ba409fc5ea34c38738a555025c94963259d3`
- generated view: listed, not counted
- cited in: record TFQ-0384
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0384 lean4: declaration obligation: no_return and cycle_regime_const on EEvent histories
- TFQ-0384 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/SecondRun/Run.lean
- TFQ-0384 python: missing obligation: an element-count trace in 000_genesis_19l57g1/code/derivation/engine.py that can show a constant cycle regime
- TFQ-0384 rust: missing obligation: replay history must record non-decrease of element count on the defined events
- TFQ-0384 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs

## Routes

Incoming (1):

- `PG-R-NO-RETURN` `DERIVED_LEAN`: [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (4):

- `PG-R-DEMAND` `DERIVED_LEAN`: [PG-DEMAND-ACCOUNTING](PG-DEMAND-ACCOUNTING.md) (PROVED_LEAN)
- `PG-R-HISTORY-CRITERION` `DERIVED_LEAN`: [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)
- `PGW-R-C2-RUN-FORWARD-EVERY-HISTORY` `DERIVED_LEAN`: [PGW-C2-RUN-FORWARD-EVERY-HISTORY](PGW-C2-RUN-FORWARD-EVERY-HISTORY.md) (PROVED_LEAN)
- `UDG-R-TFQ-0385` `GAP_NO_DERIVATION`: [TFQ-0385](TFQ-0385.md) (OPEN)
