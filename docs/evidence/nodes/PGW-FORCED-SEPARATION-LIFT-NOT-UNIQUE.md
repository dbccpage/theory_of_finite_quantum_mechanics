# PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Suppose an external task requires \<a\> and \<ab\> to differ while the current regime has \<a\> ≈ₙ \<ab\>. Every operation f on the quotient S_n/≈ₙ gives f(\[\<a\>\]) = f(\[\<ab\>\]), so no operation on the current quotient answers the task on every input, and a refinement adding at least one observation o with o(\<a\>) ≠ o(\<ab\>) is forced; the analysis gives this as an argument with proof. The lift is not unique: under a supplied string decoder, 'payload has more than one position' and 'payload contains b' both separate \<a\> from \<ab\> but disagree on \<aa\> (true and false), and full inscription identity also separates the pair while carrying more than one bit. A canonical tower therefore needs a declared minimality or initiality policy, such as fewest new predicates, minimum description length, maximal preservation of old equivalences, a free or initial completion, or retention of every tied minimum branch.

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

- Supplied string decoder for the payloads of \<a\>, \<ab\> and \<aa\>, used only by the non-uniqueness example (assumption)

## Bottleneck

The Lean declarations cover the quotient barrier; the non-uniqueness of the lift rests on the two-predicate example, and no selection policy, fixed ladder of quotients or minimal multiplicity lift is derived.

## Source status

000_oepregen 03_results_and_arguments.md section 5 (statement 5, argument with proof); 000_genesis_19l57g1 paper.md Proposition 1; Lean Paper000.separation_not_on_quotient

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Quot.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Quot.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper000.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper000.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md`

- file: [dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md](../../../dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md)
- sha256 (`lf-normalised`): `ad8dbc341e74ff3ab48f2da668d697b26dbb7c347915f33730442d94674c19f9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0425
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/genesis_checks.py::quotient_factor`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Quot.lean::quotient_barrier`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper000.lean::separation_not_on_quotient`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs::factor`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean::collapsed_quotient_barrier`

## Routes

Incoming (1):

- `PGW-R-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `DERIVED_LEAN`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN)

Outgoing (0):

