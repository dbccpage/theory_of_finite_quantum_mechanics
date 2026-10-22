# PGW-OBSERVATIONAL-EQUIVALENCE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Relative to the family O_n of internal observations available at stage n, x ≈ₙ y holds exactly when o(x) = o(y) for every o in O_n, with equality taken in each observation's codomain. If O_n is empty, every pair is equivalent vacuously, so with no observations \<a\> ≈ₙ \<ab\>. This is regime-relative equivalence: it does not make the strings equal and does not install an equality operator inside the regime.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- A declared carrier of inscriptions and a declared family O_n of observations on it (assumption)

## Bottleneck

The relation depends on the declared O_n and compares observation values in the metatheory; it is not literal string equality and does not say which observations a regime should have.

## Source status

000_genesis_19l57g1 paper.md section 4 definition; v1 Formalization B; 000_oepregen rewriting Definition 2.3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0421_observational_equivalence.md`

- file: [dag/derivations/01_pregenesis/tfq_0421_observational_equivalence.md](../../../dag/derivations/01_pregenesis/tfq_0421_observational_equivalence.md)
- sha256 (`lf-normalised`): `780e758891f073358faa5070a36a9ccdd9144bd024d5131579c80320b66c74ba`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0421
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`

- file: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`

- file: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean::SameProfile`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean::empty_profiles_equal`

## Absences recorded by the TFQ records

- TFQ-0421 python: no Python ≈ₙ check over Pre-Genesis inscriptions; the Genesis profile instance is separable in 000_genesis_19l57g1/code/derivation/observe.py
- TFQ-0421 rust: no Rust observation-family type for Pre-Genesis inscriptions; the Genesis profile instance is separable in 000_genesis_19l57g1/code/rust/src/separability.rs

## Routes

Incoming (1):

- `PGW-R-OBSERVATIONAL-EQUIVALENCE` `DERIVED_PROSE`: [PG-INERT-DIAMOND](PG-INERT-DIAMOND.md) (DEFINITION)

Outgoing (1):

- `PGW-R-PRESENTATION-NOT-EXPRESSIVE-LIFT` `CONDITIONAL_ON_IMPORT`: [PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT](PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md) (CONDITIONAL)
