# PGW-WDP-POINTED-APARTNESS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH01-P02: for a pointed relation (X, R, a, b) on a finite carrier, R(a,b) does not imply a ≠ b (one-point carrier with R = {(a,a)} and b = a), a ≠ b does not imply R(a,b) (the empty relation on two points), and R(a,b) with R irreflexive implies a ≠ b, since a = b would give R(a,a). Irreflexivity is therefore a declared ingredient of the admitted package, not a consequence of relatedness, and a carrier hosting an irreflexive related pair has at least two elements; PrimDiff.lean states the same endpoint fact for an irreflexive witness. The Python census over every pointed relation on carriers of size 1 to 3 counts 4674 relations, 2337 with R(a,b), 196 with R(a,b) and R irreflexive, 3104 with a ≠ b, and none with R irreflexive, R(a,b) and a = b.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean)
- sha256 (`bytes`): `abf14f0a60ee68e7b9d5645f9241620f666ec6336c3f25d8e2b69507ffc827d0`
- cited in: node.lean, record TFQ-0537
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.PointedRelation`): recorded sha256 `abf14f0a60ee68e7b9d5645f9241620f666ec6336c3f25d8e2b69507ffc827d0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pointed_relation_independence_fin` | yes | yes | yes | propext | `#print axioms pointed_relation_independence_fin` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md`

- file: [dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md](../../../dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md)
- sha256 (`lf-normalised`): `7406edd8b4d33f6a8a0b0f80bc5d3ed2487fa7903645dbb5dd6694fa29d0bdc1`
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

- `external:upstream/omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::GenesisAdmissionKernel`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_pointed_relation.py::test_census_matches_the_closed_forms_on_carriers_up_to_three`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/pointed_relation.py::enumerate_pointed_relations`

## Routes

Incoming (1):

- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN), [PGW-SN-ENDPOINT-LEMMA](PGW-SN-ENDPOINT-LEMMA.md) (PROVED_LEAN)

Outgoing (0):

