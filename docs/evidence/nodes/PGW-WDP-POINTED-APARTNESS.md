# PGW-WDP-POINTED-APARTNESS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH01-P02: for a pointed relation (X, R, a, b) on a finite carrier, R(a,b) does not imply a ≠ b (one-point carrier with R = {(a,a)} and b = a), a ≠ b does not imply R(a,b) (the empty relation on two points), and R(a,b) with R irreflexive implies a ≠ b, since a = b would give R(a,a). Irreflexivity is therefore a declared ingredient of the admitted package, not a consequence of relatedness, and a carrier hosting an irreflexive related pair has at least two elements; PrimDiff.lean states the same endpoint fact for an irreflexive witness. The Python census over every pointed relation on carriers of size 1 to 3 counts 4674 relations, 2337 with R(a,b), 196 with R(a,b) and R irreflexive, 3104 with a ≠ b, and none with R irreflexive, R(a,b) and a = b.

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

- `proved_lean_below_e3`: grade E0; 1 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 1 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared irreflexivity law on the relation R (assumption)

## Bottleneck

Lean pointed_relation_independence_fin gives the Fin 1 and Fin 2 countermodels and the irreflexive implication over every type; the census stops at size 3, and neither the relation nor the irreflexivity law is derived from \<\>.

## Source status

WDP monograph §1.4 WDP-CH01-P02; Lean PointedRelation.pointed_relation_independence_fin; Python census to size 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PointedRelation.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PointedRelation.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md`

- file: [dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md](../../../dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md)
- sha256 (`lf-normalised`): `0c5907c18030e032588c61301f4601836a24525c2d6088f737b996a093a383e3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0537
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_00_admitted_cut.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_00_admitted_cut.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::GenesisAdmissionKernel`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_pointed_relation.py::test_census_matches_the_closed_forms_on_carriers_up_to_three`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/pointed_relation.py::enumerate_pointed_relations`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PointedRelation.lean::pointed_relation_independence_fin`

## Routes

Incoming (1):

- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN), [PGW-SN-ENDPOINT-LEMMA](PGW-SN-ENDPOINT-LEMMA.md) (PROVED_LEAN)

Outgoing (0):

