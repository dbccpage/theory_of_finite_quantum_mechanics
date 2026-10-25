# PGW-RUNG7-DURATION-UNDER-CHANGING

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung seven (pull request 260) takes W-1, duration under CHANGING: a growth is a changing round that adds a datum, a rest round a changing round that does not, and the duration vector counts rest rounds between successive growths. In Lean the growths and rest rounds of any replayed history are functions of base and regime, so the number of segments and their sum are definable, and the data that instances and requirements name bound later segments from below. Countermodels: no segment is a function of position, base and regime, and no duration between the first two growths is a function of the regime, even over histories from the empty regime. On the rectangle the vectors reached at every regime are exactly the envelope, and the envelope is not a class invariant.

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

- Lean declaration SecondDuration.Rounds.growths_counted at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondDuration.Gaps.gap_not_from_genesis at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

Each duration between growths is not definable from the state; attainment of the envelope beyond the four-event rectangle (V-1) and the multiset of envelopes of a class (V-3) are OPEN.

## Source status

continuation.txt section 5.2 attempt 9 and section 6 rung seven; run ledger SD-07-1 to SD-07-6; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0470_rung7_duration_under_changing.md`

- file: [dag/derivations/02_genesis/tfq_0470_rung7_duration_under_changing.md](../../../dag/derivations/02_genesis/tfq_0470_rung7_duration_under_changing.md)
- sha256 (`lf-normalised`): `a71d39892a272cb1e54ac41f61b26e0b2084c87f16e1590d6da6d7add8165fa2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0470
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/duration.py::envelope`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/duration.py::vector`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Gaps.lean::gap_not_from_genesis`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Gaps.lean::segment_not_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Rounds.lean::growths_counted`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Rounds.lean::rest_given_base`

## Absences recorded by the TFQ records

- TFQ-0470 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG7-DURATION-UNDER-CHANGING` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG6-SUCCESSION-ELEMENT-COUNT](PGW-RUNG6-SUCCESSION-ELEMENT-COUNT.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-RUNG8-ELEMENT-COUNT-ACROSS-ISO` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO](PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO.md) (CONDITIONAL)
