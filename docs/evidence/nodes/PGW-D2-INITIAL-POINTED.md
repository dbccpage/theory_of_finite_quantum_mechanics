# PGW-D2-INITIAL-POINTED

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let D₂ have carrier {0, 1} and the single edge 0 → 1. For any relation R with a supplied witness R(a, b), the map f(0) = a, f(1) = b preserves the edge, and every map sending 0 to a and 1 to b equals it, so f is the unique endpoint-preserving map from D₂ (D2_initial_pointed). Under irreflexivity this map is injective, because the endpoints of an irreflexive witnessed edge differ (irrefl_witness_ne).

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

This represents the chosen witness only: the map need not describe every edge of R or preserve non-edges, needs no reverse edge or composition law, and does not force irreflexivity from opaque marks.

## Source status

paper.md section 9 (ledger WDP-P000-010); PrimDiff.lean D2_initial_pointed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md`

- file: [dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md](../../../dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md)
- sha256 (`lf-normalised`): `8450f34ea5469f778f8b6eeb4e070320850b78173f6beea20bc82fa4cd593103`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0455
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean::D2_initial_pointed`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean::irrefl_witness_ne`

## Absences recorded by the TFQ records

- TFQ-0455 python: no Python check of the pointed two-point witness map
- TFQ-0455 rust: no Rust check of the pointed two-point witness map

## Routes

Incoming (1):

- `PGW-R-D2-INITIAL-POINTED` `DERIVED_LEAN`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE), [PG-GEN-IRREFLEXIVE-DISTINCT](PG-GEN-IRREFLEXIVE-DISTINCT.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-FIVE-PRESENTATION-QUESTIONS` `DERIVED_PROSE`: [PGW-FIVE-PRESENTATION-QUESTIONS](PGW-FIVE-PRESENTATION-QUESTIONS.md) (DEFINITION)
- `PGW-R-INCIDENCE-CONSTRUCTION-BETTI` `DERIVED_LEAN`: [PGW-INCIDENCE-CONSTRUCTION-BETTI](PGW-INCIDENCE-CONSTRUCTION-BETTI.md) (PROVED_LEAN)
