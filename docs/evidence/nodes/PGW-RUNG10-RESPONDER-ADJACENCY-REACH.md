# PGW-RUNG10-RESPONDER-ADJACENCY-REACH

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung ten (pull request 265) takes X-6 for adjacency, reach, branching and exhaustion through the sealed responder: the demand is a collapsed pair, a response is a minimum of the sealed candidate space of at most two items and arity two under mu1 or mu2, and the responder refuses a regime holding a uniform rule. Adjacency, reach and branching are useful realizations at two declared capabilities, and exhaustion is definable: in Lean a form is exhausted exactly when it does not distinguish, exhaustion is carried by the isomorphism, and for a well-formed base a pair a history moves is mentioned by an instance admission of the history or the history holds a rule admission. On the rectangle 3110 demands are answered with none refused within two items, reach is at most three and finite adjacency distance at most two, and the measure changes the adjacency graph and the tie counts.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

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

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean)
- sha256 (`bytes`): `e2d0c2ea1c49f613edb5efd542c1092ab43be08646f4e1d56662a44c9529bf64`
- cited in: node.lean, record TFQ-0473
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11.rung10_exhaustion_and_responder_move_witness` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.rung10_exhaustion_and_responder_move_witness` |
| `WitnessedDifference.WdpBatch11.uniform_rule_exhausts_form` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.uniform_rule_exhausts_form` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean)
- sha256 (`bytes`): `fb93c9f5733e92d52e89df3da4ab8183ded4cf103514b6ba0d3141cfadc26165`
- cited in: node.lean, record TFQ-0473
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11Rep.rung10_exhaustion_and_responder_move_witness` | yes | yes | no | - | `#print axioms WitnessedDifference.WdpBatch11Rep.rung10_exhaustion_and_responder_move_witness` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0473_rung10_responder_adjacency_reach.md`

- file: [dag/derivations/02_genesis/tfq_0473_rung10_responder_adjacency_reach.md](../../../dag/derivations/02_genesis/tfq_0473_rung10_responder_adjacency_reach.md)
- sha256 (`lf-normalised`): `091352f3c3192e57c622ac34f936ef699d0a82d456473bbc1c14fa08107458b5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0473
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

- `PGW-R-RUNG10-RESPONDER-ADJACENCY-REACH` `DERIVED_LEAN`: [PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES](PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-C1-ENGINE-CLASS-144` `CONDITIONAL_ON_IMPORT`: [PGW-C1-ENGINE-CLASS-144](PGW-C1-ENGINE-CLASS-144.md) (CONDITIONAL)
