# PGW-NO-TRANSITION-QUIESCENCE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If a regime's transition relation is empty, no state has a successor; that is the definition of an empty relation and needs no experiment. All three replies to Prompt 11 said no continuation is forced, so a move from \<\> to \<a\> has to come from outside: a caller supplies it, or a rule is added.

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

None recorded.

## Bottleneck

True by definition of an empty relation; the trial replies are behaviour, not evidence for the definition.

## Source status

000_oepregen 03_results_and_arguments.md section 1 (statement 1, true by definition)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/01_pregenesis/tfq_0418_no_transition_quiescence.md`

- file: [dag/derivations/01_pregenesis/tfq_0418_no_transition_quiescence.md](../../../dag/derivations/01_pregenesis/tfq_0418_no_transition_quiescence.md)
- sha256 (`lf-normalised`): `fc5e148a0eb534f92fd41c391106009a43d8dfc4b5b2484453e46fb9b0eb5809`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0418
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`

- file: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0418 lean4: the Genesis counterpart is genesis_underivable in Derivation/Inertia.lean, recorded under Challenge 0
- TFQ-0418 python: no Python check of an empty transition relation
- TFQ-0418 rust: no Rust check of an empty transition relation

## Routes

Incoming (1):

- `PGW-R-NO-TRANSITION-QUIESCENCE` `DERIVED_PROSE`: [PGW-PREGENESIS-GRAMMAR](PGW-PREGENESIS-GRAMMAR.md) (DEFINITION)

Outgoing (1):

- `UDG-R-TFQ-0419` `RECORD_PARENT`: [TFQ-0419](TFQ-0419.md) (SOURCE_RECORD)
