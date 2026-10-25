# PGW-RUNG6-SUCCESSION-ELEMENT-COUNT

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung six (pull request 259) takes Z-4, succession of accepted rounds through the element count, under three readings of a round: EVERY event, every ADMITTING event (not a supply) and every CHANGING event (the regime differs after it). In Lean, under CHANGING the count of any replayed history is the element count of the regime reached less the base's, so it is a function of base and regime, and counted from the empty regime a function of the regime alone; for every history CHANGING is at most ADMITTING, which is at most EVERY. Countermodels: EVERY and ADMITTING are not functions of base and regime, and CHANGING is not a function of the regime alone across bases (the Lean reading regime R2L is reached from the empty regime with count three and from itself with count zero).

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

- Lean declaration SecondSuccession.Count.changes_counted at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSuccession.Readings.every_not_given_base at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSuccession.Readings.changing_not_of_regime at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

The readings are of histories of the sealed step, not of an engine's run; class-level succession was OPEN at this rung and is closed for clean bases only by rung eight, and within continuation attempt two's runs one state is reached in five rounds and in six.

## Source status

continuation.txt section 3 definition 12, section 5.2 attempt 8 and section 6 rung six; run ledger SD-06-1 to SD-06-6; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0469_rung6_succession_element_count.md`

- file: [dag/derivations/02_genesis/tfq_0469_rung6_succession_element_count.md](../../../dag/derivations/02_genesis/tfq_0469_rung6_succession_element_count.md)
- sha256 (`lf-normalised`): `7213f380bc4d2bc045406aff0e0bb94773086fa209a2de36a2091070bcc9dc1c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0469
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:195`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Count.lean::changes_counted`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Count.lean::changes_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean::admitting_not_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean::changing_not_of_regime`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean::every_not_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/succession.py::counts`

## Absences recorded by the TFQ records

- TFQ-0469 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG6-SUCCESSION-ELEMENT-COUNT` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG5-SYMMETRY-ALONG-HISTORY](PGW-RUNG5-SYMMETRY-ALONG-HISTORY.md) (CONDITIONAL)

Outgoing (2):

- `PGW-R-CAPABILITY-STAGE-COUNTER` `DERIVED_PROSE`: [PGW-CAPABILITY-STAGE-COUNTER](PGW-CAPABILITY-STAGE-COUNTER.md) (DEFINITION)
- `PGW-R-RUNG7-DURATION-UNDER-CHANGING` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG7-DURATION-UNDER-CHANGING](PGW-RUNG7-DURATION-UNDER-CHANGING.md) (CONDITIONAL)
