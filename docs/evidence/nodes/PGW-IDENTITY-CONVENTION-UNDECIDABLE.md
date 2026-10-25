# PGW-IDENTITY-CONVENTION-UNDECIDABLE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Whether \<a\> supplied after \<\> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty \<\> and \<a\> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling \<a\> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- A declared identity convention, opaque or exact-inscription, chosen by the host (assumption)

## Bottleneck

Records that the answer is relative to the convention; it does not choose one, and the three replies are behaviour of one unrecorded model, not evidence for either convention.

## Source status

v1 Red round item 1 (conditional verdict); 000_oepregen 03_results_and_arguments.md section 2 and 02_trial_record.md Prompt 12

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md`

- file: [dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md](../../../dag/derivations/01_pregenesis/tfq_0423_identity_convention_undecidable.md)
- sha256 (`lf-normalised`): `2400d95576a16f2deb78da2aa917ae5bbf0049d2822e54c608f76578e1bb356b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0423
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`

- file: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`
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

## Absences recorded by the TFQ records

- TFQ-0423 lean4: no Lean statement of the opaque and exact-inscription identity conventions
- TFQ-0423 python: no Python switch between identity conventions
- TFQ-0423 rust: no Rust switch between identity conventions

## Routes

Incoming (1):

- `PGW-R-IDENTITY-CONVENTION-UNDECIDABLE` `CONDITIONAL_ON_IMPORT`: [PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT](PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md) (CONDITIONAL)

Outgoing (2):

- `APP-R-COMP-C1-IDENTITY-CONVENTION-INPUT` `CONDITIONAL_ON_IMPORT`: [COMP-C1-IDENTITY-CONVENTION-INPUT](COMP-C1-IDENTITY-CONVENTION-INPUT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-ABSENCE-OF-RULE-NOT-IDENTIFICATION` `DERIVED_PROSE`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION)
