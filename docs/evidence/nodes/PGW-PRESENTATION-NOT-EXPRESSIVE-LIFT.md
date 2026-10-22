# PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Write P for the presented inscriptions and O for the internal observations. Supplying \<a\> after \<\> changes P from {\<\>} to {\<a\>} and leaves O_1 = O_0 = ∅, so no new internal distinction is available. With q : P → N sending an inscription to the distinctions the regime has, x ≠ y in P can hold while q(x) = q(y) in N, so a new presentation does not imply a new internal class, and in the other direction q(x) = q(y) does not imply x = y. Under the opaque convention \<a\> is a new presentation state in the same internal class as \<\>; the statement holds under that convention only.

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

- Opaque identity convention: a state is what the regime can tell apart, so internal identity is the quotient by ≈ₙ (assumption)

## Bottleneck

Under the exact-inscription convention \<a\> is a new state; the statement concerns discriminating power, not meaning, since a regime can gain a syntactic distinction such as empty versus nonempty payload without assigning a a referent.

## Source status

000_oepregen 03_results_and_arguments.md section 2 (statement 2, holds under one convention); v1 Derivation 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0422_presentation_not_expressive_lift.md`

- file: [dag/derivations/01_pregenesis/tfq_0422_presentation_not_expressive_lift.md](../../../dag/derivations/01_pregenesis/tfq_0422_presentation_not_expressive_lift.md)
- sha256 (`lf-normalised`): `a742d4d0d12165bc6bdc301b520a8c9b05680050a39de51a0ba299ba5e77bc7b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0422
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Observation.lean::empty_profiles_equal`

## Absences recorded by the TFQ records

- TFQ-0422 python: no Python record separating presentation state from internal class
- TFQ-0422 rust: no Rust record separating presentation state from internal class

## Routes

Incoming (1):

- `PGW-R-PRESENTATION-NOT-EXPRESSIVE-LIFT` `CONDITIONAL_ON_IMPORT`: [PGW-OBSERVATIONAL-EQUIVALENCE](PGW-OBSERVATIONAL-EQUIVALENCE.md) (DEFINITION)

Outgoing (2):

- `APP-R-AUTH-TC0-TAPE-CONTROL-TYPING` `COMPUTED`: [AUTH-TC0-TAPE-CONTROL-TYPING](AUTH-TC0-TAPE-CONTROL-TYPING.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-IDENTITY-CONVENTION-UNDECIDABLE` `CONDITIONAL_ON_IMPORT`: [PGW-IDENTITY-CONVENTION-UNDECIDABLE](PGW-IDENTITY-CONVENTION-UNDECIDABLE.md) (CONDITIONAL)
