# PGW-RUNG10-RESPONDER-ADJACENCY-REACH

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung ten (pull request 265) takes X-6 for adjacency, reach, branching and exhaustion through the sealed responder: the demand is a collapsed pair, a response is a minimum of the sealed candidate space of at most two items and arity two under mu1 or mu2, and the responder refuses a regime holding a uniform rule. Adjacency, reach and branching are useful realizations at two declared capabilities, and exhaustion is definable: in Lean a form is exhausted exactly when it does not distinguish, exhaustion is carried by the isomorphism, and for a well-formed base a pair a history moves is mentioned by an instance admission of the history or the history holds a rule admission. On the rectangle 3110 demands are answered with none refused within two items, reach is at most three and finite adjacency distance at most two, and the measure changes the adjacency graph and the tie counts.

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

- Lean declaration SecondResponse.Exhaust.exhausted_iff_not_distinguishes at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondResponse.Move.moved_pairs_meet_mentions at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Sealed responder under mu1 or mu2 at two items and arity two, priced as two declared capabilities (assumption)

## Bottleneck

No Lean statement is about a minimum, a cost or a tie (S-3); response_collapses_a_pair is about one instance admission, not a sealed-responder minimum; the distance bound of two is not known to be the grammar's (S-4), and branching is finite computation only.

## Source status

continuation.txt section 5.2 attempt 12 and section 6 rung ten; run ledger SD-10-1 to SD-10-7; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0473_rung10_responder_adjacency_reach.md`

- file: [dag/derivations/02_genesis/tfq_0473_rung10_responder_adjacency_reach.md](../../../dag/derivations/02_genesis/tfq_0473_rung10_responder_adjacency_reach.md)
- sha256 (`lf-normalised`): `17fff3df541c645436daae984d0f5450db081d0df6f466426d5205b7e39a2e4c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0473
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/lean/SecondResponse/Exhaust.lean::exhausted_iff_not_distinguishes`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/lean/SecondResponse/Move.lean::moved_pairs_meet_mentions`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/lean/SecondResponse/Move.lean::response_collapses_a_pair`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/response_rows.py::adjacency`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/response_rows.py::moved_pairs`

## Absences recorded by the TFQ records

- TFQ-0473 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG10-RESPONDER-ADJACENCY-REACH` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES](PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-C1-ENGINE-CLASS-144` `CONDITIONAL_ON_IMPORT`: [PGW-C1-ENGINE-CLASS-144](PGW-C1-ENGINE-CLASS-144.md) (CONDITIONAL)
