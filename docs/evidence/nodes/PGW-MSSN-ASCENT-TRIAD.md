# PGW-MSSN-ASCENT-TRIAD

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> MSS-N separates three evidence states: declared successor ≠ candidate lift ≠ licensed lift. A declared successor is a research obligation stated by an atlas row; a candidate lift is submitted data, a proposed pair of maps with repair witnesses; a licensed lift has exhausted repairs, a minimized extension, a verified retraction and a passing host replay. Every atlas row is a declared successor specification, and its successor rationale stays unproved until an accepted lift record is attested.

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

None recorded.

## Bottleneck

The levels catalogue sets lift_status unlicensed; a PASS LiftReceipt from evaluate_two_boxed_laws_gate consumes supplied flags and is a candidate check, not a licensed lift, and the CandidateLift record shape is metadata only.

## Source status

000_pre_genesis_to_mssn paper.md section 15; 003_oemssn levels/README.md invariant 3 and curriculum.md Lesson 1

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs`

- file: `omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0529_mssn_ascent_triad.md`

- file: [dag/derivations/05_mssn_sn/tfq_0529_mssn_ascent_triad.md](../../../dag/derivations/05_mssn_sn/tfq_0529_mssn_ascent_triad.md)
- sha256 (`lf-normalised`): `1d21cbc390bd1bde5e477802ba6b779fcdb0320553c00e2be707ee58585492c1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0529
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/curriculum.md`

- file: `omega_engine_education/documentation/003_oemssn/curriculum.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/levels/README.md`

- file: `omega_engine_education/documentation/003_oemssn/levels/README.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs::CandidateLift`

## Absences recorded by the TFQ records

- TFQ-0529 lean4: no Lean statement of the ascent triad; candidateLiftCondition is recorded under TFQ-0534
- TFQ-0529 python: no Python check of lift evidence states

## Routes

Incoming (1):

- `PGW-R-MSSN-ASCENT-TRIAD` `DERIVED_PROSE`: [PGW-MSSN-ATLAS-NOT-DERIVATION](PGW-MSSN-ATLAS-NOT-DERIVATION.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-ALPHABET-DECLARATIONS` `DERIVED_PROSE`: [PGW-MSSN-ALPHABET-DECLARATIONS](PGW-MSSN-ALPHABET-DECLARATIONS.md) (DEFINITION)
