# PGW-FAITHFUL-DESCENT-ROUND-TRIP

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For supplied translations f : P → Q and g : Q → P, injective maps i : P → C and j : Q → C with i = j ∘ f and j = i ∘ g exist if and only if g ∘ f = id_P and f ∘ g = id_Q (faithful_descent_iff_round_trip_coherent). One direction substitutes the identifying equations and cancels the injective maps (faithful_descent_to_coherent); the other takes C = P, i = id and j = g. A failed round trip for this declared pair therefore excludes a faithful common carrier that eliminates the presentation index.

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

Failure concerns the declared translation pair only: another pair of translations may still close, and no common world prior to P and Q is assumed.

## Source status

paper.md section 10 (ledger WDP-P000-021); PresentationDescent.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PresentationDescent.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PresentationDescent.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0458_faithful_descent_round_trip.md`

- file: [dag/derivations/02_genesis/tfq_0458_faithful_descent_round_trip.md](../../../dag/derivations/02_genesis/tfq_0458_faithful_descent_round_trip.md)
- sha256 (`lf-normalised`): `318fa014d85d35a8c75a80a1fe99c0d544f7c2b45ce1f4b91c32b05559b0013d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0458
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PresentationDescent.lean::faithful_descent_iff_round_trip_coherent`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PresentationDescent.lean::faithful_descent_to_coherent`

## Absences recorded by the TFQ records

- TFQ-0458 python: no Python check of presentation descent
- TFQ-0458 rust: no Rust check of presentation descent

## Routes

Incoming (1):

- `PGW-R-FAITHFUL-DESCENT-ROUND-TRIP` `DERIVED_LEAN`: [PGW-QUOTIENT-RETENTION](PGW-QUOTIENT-RETENTION.md) (PROVED_LEAN)

Outgoing (0):

