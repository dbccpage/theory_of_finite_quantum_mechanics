# PGW-QUOTIENT-RETENTION

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let fine and coarse be equivalence relations on one set with every fine identification also a coarse one. The map \[x\]_fine ↦ \[x\]_coarse is well defined and surjective (collapseMap_surjective), injective exactly when every coarse identification also holds finely (collapseMap_injective_iff_reverse_refinement), and successive such maps compose without choosing representatives (collapseMap_compose). If a former identification fails in the finer relation, two distinct fine classes remain over one coarse class (failed_identification_retains_two_classes).

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

A theorem about supplied equivalence relations: no class is manufactured and no new primitive is inferred, and which identifications a later stage must retain is a declared task.

## Source status

paper.md section 10 (ledger WDP-P000-020); QuotientRetention.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/QuotientRetention.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/QuotientRetention.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0457_quotient_retention.md`

- file: [dag/derivations/02_genesis/tfq_0457_quotient_retention.md](../../../dag/derivations/02_genesis/tfq_0457_quotient_retention.md)
- sha256 (`lf-normalised`): `677547235d334797b9cb3997cdfcd6e26fdda2dfe351c2e855ede1d1653f41ea`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0457
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/QuotientRetention.lean::collapseMap_compose`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/QuotientRetention.lean::collapseMap_injective_iff_reverse_refinement`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/QuotientRetention.lean::collapseMap_surjective`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/QuotientRetention.lean::failed_identification_retains_two_classes`

## Absences recorded by the TFQ records

- TFQ-0457 python: no Python check of quotient retention
- TFQ-0457 rust: no Rust check of quotient retention

## Routes

Incoming (1):

- `PGW-R-QUOTIENT-RETENTION` `DERIVED_LEAN`: [PGW-FIVE-PRESENTATION-QUESTIONS](PGW-FIVE-PRESENTATION-QUESTIONS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-FAITHFUL-DESCENT-ROUND-TRIP` `DERIVED_LEAN`: [PGW-FAITHFUL-DESCENT-ROUND-TRIP](PGW-FAITHFUL-DESCENT-ROUND-TRIP.md) (PROVED_LEAN)
