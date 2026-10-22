# PGW-GO-MULTIPLICITY-MONOTONE

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fourth derivation counts assertions: a state has terms, a multiplicity per ordered pair and the names, arb is asserted once to begin with, and every change adds one term or raises one multiplicity by one, taking nothing away. Every change leaves its state contained in its outcome and containment composes, so along every sequence Reach4 s t n each multiplicity is the same or higher (Reach4.mult_le), at the pair writing arb as well (Reach4.arb_mult_le); terms, assertions and names persist and an obstruction is never cleared. A counted containment gives a containment of the supports, so the third derivation's conclusions survive on the supports.

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Reading C1': asserted means multiplicity at least one, with support and indicator maps to the earlier model (assumption)

## Bottleneck

Monotone for the fourth seed's additions only; the fifth derivation restores the four kinds of change on counted assertions, so this monotonicity is not claimed there, and a multiplicity can rise above one (arb_twice).

## Source status

001_genesis_ongoing_h3v7n5qf paper/fourth/claim_ledger.md D5 to D7; lean4/Fourth/Contain.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fourth/Contain.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fourth/Contain.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0479_go_multiplicity_monotone.md`

- file: [dag/derivations/02_genesis/tfq_0479_go_multiplicity_monotone.md](../../../dag/derivations/02_genesis/tfq_0479_go_multiplicity_monotone.md)
- sha256 (`lf-normalised`): `deba923365e52217d573f241a627ba669d7f255c5f4ed171efc3de9efbf79a3c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0479
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/fourth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/fourth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_05_monotone_mass_growth.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_05_monotone_mass_growth.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/fourth/invariants.py::never_decreases`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fourth/Contain.lean::Reach4.arb_mult_le`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fourth/Contain.lean::Reach4.contains`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fourth/Contain.lean::Reach4.mult_le`

## Absences recorded by the TFQ records

- TFQ-0479 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-MULTIPLICITY-MONOTONE` `DERIVED_LEAN`: [PGW-GO-CONTRACTION-STEP2-STEP3](PGW-GO-CONTRACTION-STEP2-STEP3.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-TWO-RELATIONS-SWAP` `DERIVED_LEAN`: [PGW-GO-TWO-RELATIONS-SWAP](PGW-GO-TWO-RELATIONS-SWAP.md) (PROVED_LEAN)
