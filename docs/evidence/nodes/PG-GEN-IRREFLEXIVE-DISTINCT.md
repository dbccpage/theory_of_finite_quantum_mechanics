# PG-GEN-IRREFLEXIVE-DISTINCT

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the Genesis Ongoing model the two given names are distinct terms (a ≠ b), derived from the irreflexivity constraint on the given assertion arb; bra is independent (bra_not_derived). Irreflexive endpoints are distinct in general (irreflexive_endpoints).

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

- Ban on xrx (assumption: a stated part of the seed)

## Bottleneck

The distinctness rests on the ban on xrx being given; when the ban is struck (17th derivation) it is re-derived only under the obstruction rule.

## Source status

D1 a ≠ b from irreflexive witness; given_distinct

## Review

- PFP review: [dag/results/PG-GEN-IRREFLEXIVE-DISTINCT/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-IRREFLEXIVE-DISTINCT/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: All two-term relation tables are checked, and irreflexive related endpoints are generally distinct in Lean.
  - does not support: Relate the bounded tables to the intended Genesis semantics and retain the irreflexivity premise. No assertion of seed-free distinctness, transitivity or orientation selection is made.
  - next test: Relate the bounded tables to the intended Genesis semantics and retain the irreflexivity premise. No assertion of seed-free distinctness, transitivity or orientation selection is made.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0387_irreflexive_endpoints_distinct.md`

- file: [dag/derivations/02_genesis/tfq_0387_irreflexive_endpoints_distinct.md](../../../dag/derivations/02_genesis/tfq_0387_irreflexive_endpoints_distinct.md)
- sha256 (`lf-normalised`): `e12328e8f3d16a8e45be150107ee684e7b4f0720c6aaa50dd95138ac70d51b51`
- generated view: listed, not counted
- cited in: record TFQ-0387
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0387 lean4: declaration obligation: given_distinct and irreflexive_endpoints, with bra left undecided
- TFQ-0387 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0387 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean
- TFQ-0387 python: missing obligation: a seed checker under 001_genesis_ongoing_h3v7n5qf/code that accepts arb, rejects xrx, and leaves bra unset
- TFQ-0387 rust: missing obligation: no Rust seed module was listed under 001_genesis_ongoing_h3v7n5qf; the ban on xrx still needs a carrier there or an explicit absence

## Routes

Incoming (1):

- `PG-R-IRREFLEXIVE` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (3):

- `APP-R-COMP-C1-CANONICAL-SEPARATED-ALPHABET` `DERIVED_LEAN`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN)
- `PG-R-ONGOING-OBSTRUCTION` `DERIVED_LEAN`: [PG-GEN-ONGOING-OBSTRUCTION](PG-GEN-ONGOING-OBSTRUCTION.md) (PROVED_LEAN)
- `PGW-R-D2-INITIAL-POINTED` `DERIVED_LEAN`: [PGW-D2-INITIAL-POINTED](PGW-D2-INITIAL-POINTED.md) (PROVED_LEAN)
