# PGW-GO-CONTRACTION-STEP2-STEP3

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The contraction family strikes changes from the base seed. The second derivation strikes removal and keeps identification, adding a term and adding an assertion (Lean Step3); every change comes with a carrying map q, the identity for an addition and a merge for an identification, sending terms to terms, each asserted xry to an asserted q(x) r q(y) and the names to the names, and carrying maps compose along every sequence (Step3.carries, Reach3.carries). The third derivation also strikes identification (Lean Step2, two kinds): Step2.toStep3 embeds each of its changes as a second-seed change and Reach2.toReach3 each sequence, so the earlier one-change and sequence theorems restrict to it, and its containment of a state in its outcome is a carrying map with the identity.

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

None recorded.

## Bottleneck

The Lean names run opposite to the derivation numbers (Step3 is the second seed's three-kind step, Step2 the third seed's two-kind step); the embedding is a restriction, and no carrying map exists under the base seed, where a removal un-asserts.

## Source status

001_genesis_ongoing_h3v7n5qf paper/second/claim_ledger.md D5 and paper/third/claim_ledger.md D5; lean4/Second/Carry.lean, lean4/Third/Step.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Carry.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Carry.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Third/Step.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Third/Step.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0478_go_contraction_step2_step3.md`

- file: [dag/derivations/02_genesis/tfq_0478_go_contraction_step2_step3.md](../../../dag/derivations/02_genesis/tfq_0478_go_contraction_step2_step3.md)
- sha256 (`lf-normalised`): `1f0c32a7f42d20560f786dd6444d366d8f2ebce066170cdbaba61a1b6f97ef10`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0478
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/second/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/second/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/third/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/third/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_06_stage_embeddings.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_06_stage_embeddings.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/second/reach.py::carrying_map`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/third/reach.py::embedding`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Carry.lean::Reach3.carries`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Carry.lean::Step3.carries`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Third/Step.lean::Reach2.toReach3`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Third/Step.lean::Step2.toStep3`

## Absences recorded by the TFQ records

- TFQ-0478 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-CONTRACTION-STEP2-STEP3` `DERIVED_LEAN`: [PGW-GO-REACH-CEILING](PGW-GO-REACH-CEILING.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-MULTIPLICITY-MONOTONE` `DERIVED_LEAN`: [PGW-GO-MULTIPLICITY-MONOTONE](PGW-GO-MULTIPLICITY-MONOTONE.md) (PROVED_LEAN)
