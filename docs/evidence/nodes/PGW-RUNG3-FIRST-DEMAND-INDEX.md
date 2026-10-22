# PGW-RUNG3-FIRST-DEMAND-INDEX

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung three (pull request 239) takes leftover L-2, the first-demand index over an arbitrary run: a first count is a prefix length at which a demand stands with no shorter prefix carrying one. In Lean the first count is unique with no decidability hypothesis, every event preserves well-formedness, a successor first count never consumes a demand-inert event last, and from the empty base no count below two is a first count. Existence is proved only given a decision for a demand at a regime (X-1, OPEN). Countermodels: the first count is not a function of the reached regime (two datum admissions, and a supply followed by the same two, give counts two and three under the all-apart stake), and a demand can cease.

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

- Lean declaration SecondIndex.Index.first_demand_unique at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondIndex.Index.first_demand_exists_when_a_demand_is_decidable at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondIndex.Countermodel.index_is_not_a_function_of_the_reached_regime at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Declared two-sided stake of rung two track one (assumption)

## Bottleneck

Existence of a first count waits on a decision procedure over contexts (X-1), which no rung built; the rectangle results (577, 3928 and 14293 sequences) stop at four events, and nothing here concerns a run driven by a responder (I-X PENDING).

## Source status

continuation.txt section 5.2 attempt 5 and section 6 rung three; run ledger SD-03-1 to SD-03-8; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0466_rung3_first_demand_index.md`

- file: [dag/derivations/02_genesis/tfq_0466_rung3_first_demand_index.md](../../../dag/derivations/02_genesis/tfq_0466_rung3_first_demand_index.md)
- sha256 (`lf-normalised`): `5619a77ac2c0e1ab68a221cf85721bdcef39bcbb0762ca1a6ce07a2948418e69`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0466
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:161`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/index.py::first_index_forward`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Countermodel.lean::demand_can_cease`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Countermodel.lean::index_is_not_a_function_of_the_reached_regime`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Index.lean::first_demand_exists_when_a_demand_is_decidable`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Index.lean::first_demand_unique`

## Absences recorded by the TFQ records

- TFQ-0466 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG3-FIRST-DEMAND-INDEX` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG2A-STAKE-DECLARED-LABEL](PGW-RUNG2A-STAKE-DECLARED-LABEL.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-RUNG4-INDEX-UP-TO-ISOMORPHISM` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM](PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM.md) (CONDITIONAL)
