# PGW-FIVE-PRESENTATION-QUESTIONS

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a presentation S(n), its active demand register and its maps between stages, the Genesis account hands on five declared questions: which data and operations are admitted at the current stage; which declared task cannot be answered with the current observations; which candidate extensions are permitted, and under which costs; which prior answers, inscriptions or algebraic laws must survive; and what evidence shows both preservation and resolution of the selected problem. Selecting a new operation remains a declared construction decision, with its preservation obligations stated.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared presentation S(n) with its active demand register and stage maps (assumption)

## Bottleneck

The questions frame the later stages and select no operation; the quotient-retention and round-trip results that follow make the preservation questions concrete without answering the selection question.

## Source status

paper.md section 10 declared questions

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0456_five_presentation_questions.md`

- file: [dag/derivations/02_genesis/tfq_0456_five_presentation_questions.md](../../../dag/derivations/02_genesis/tfq_0456_five_presentation_questions.md)
- sha256 (`lf-normalised`): `7bb5e380f76cc927a0a2894878db345c14c20b5b54932c5936f4b4fd8dd2b4df`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0456
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0456 lean4: no Lean statement; the five questions are declared
- TFQ-0456 python: no Python check; the five questions are declared
- TFQ-0456 rust: no Rust check; the five questions are declared

## Routes

Incoming (1):

- `PGW-R-FIVE-PRESENTATION-QUESTIONS` `DERIVED_PROSE`: [PGW-D2-INITIAL-POINTED](PGW-D2-INITIAL-POINTED.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
- `PGW-R-QUOTIENT-RETENTION` `DERIVED_LEAN`: [PGW-QUOTIENT-RETENTION](PGW-QUOTIENT-RETENTION.md) (PROVED_LEAN)
