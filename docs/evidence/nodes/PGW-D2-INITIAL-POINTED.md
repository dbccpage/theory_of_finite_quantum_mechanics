# PGW-D2-INITIAL-POINTED

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let D₂ have carrier {0, 1} and the single edge 0 → 1. For any relation R with a supplied witness R(a, b), the map f(0) = a, f(1) = b preserves the edge, and every map sending 0 to a and 1 to b equals it, so f is the unique endpoint-preserving map from D₂ (D2_initial_pointed). Under irreflexivity this map is injective, because the endpoints of an irreflexive witnessed edge differ (irrefl_witness_ne).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean)
- sha256 (`bytes`): `1f3f373e979d9199c73ef9e63ea863a0ac41692c247e23052dba6588c6e16f26`
- cited in: node.lean, node.source, record TFQ-0455
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.PrimDiff`): recorded sha256 `1f3f373e979d9199c73ef9e63ea863a0ac41692c247e23052dba6588c6e16f26` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `D2_initial_pointed` | yes | yes | yes | propext | `#print axioms D2_initial_pointed` |
| `irrefl_witness_ne` | yes | yes | yes | none | `#print axioms irrefl_witness_ne` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md`

- file: [dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md](../../../dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md)
- sha256 (`lf-normalised`): `9ab0e39c9b1dc9acc6c2b5d2dd95338365fa704f83a580c943953ccf826158a2`
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

## Absences recorded by the TFQ records

- TFQ-0455 python: no Python check of the pointed two-point witness map
- TFQ-0455 rust: no Rust check of the pointed two-point witness map

## Routes

Incoming (1):

- `PGW-R-D2-INITIAL-POINTED` `DERIVED_LEAN`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE), [PG-GEN-IRREFLEXIVE-DISTINCT](PG-GEN-IRREFLEXIVE-DISTINCT.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-FIVE-PRESENTATION-QUESTIONS` `DERIVED_PROSE`: [PGW-FIVE-PRESENTATION-QUESTIONS](PGW-FIVE-PRESENTATION-QUESTIONS.md) (DEFINITION)
- `PGW-R-INCIDENCE-CONSTRUCTION-BETTI` `DERIVED_LEAN`: [PGW-INCIDENCE-CONSTRUCTION-BETTI](PGW-INCIDENCE-CONSTRUCTION-BETTI.md) (PROVED_LEAN)
