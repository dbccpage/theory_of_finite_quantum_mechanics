# PGW-RUNG1-STREAM-AS-RESPONSE

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Challenge 1, whether the stream can be a response, stays OPEN after rung one (pull request 133). On the rectangle of both readings, five stakes, two measures, at most three items, arity two, fifteen rounds and a pre-expansion guard of 250 nodes, none of the 1680 retained V1 minimum response edges carries a datum, and 32 of them were selected at three items. The frontier has 1974 nodes, 1039 of them stopped at the guard in six runs, and targets after a node's first refusal were not searched. At two items a fresh datum is valid but priced out in 219 rows, 58 of them for a same demand; the four-item prediction R1-X was not computed.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared stream: growth by the supply and admission of one fresh datum at a demand-free state (assumption)
- Declared three-item candidate space of rung one, checked against the sealed enumeration below three items (assumption)

## Bottleneck

Finite results on the measured V1 tree only, with no Lean; the stream is not shown to be a response or not to be one, and continuation attempt two adds only that no response edge of its runs carries a datum at two items.

## Source status

continuation.txt section 4 row 1, section 6 rung one and section 13; run ledger SD-01-1 to SD-01-10; open obligation

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0463_rung1_stream_as_response.md`

- file: [dag/derivations/02_genesis/tfq_0463_rung1_stream_as_response.md](../../../dag/derivations/02_genesis/tfq_0463_rung1_stream_as_response.md)
- sha256 (`lf-normalised`): `6acb636f6a4fd0503d38c94517fa7cc37807fdbf4a954c4be2e40f1fea399ffa`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0463
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:114`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py::fresh_datum_availability`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py::min_responses_three`

## Absences recorded by the TFQ records

- TFQ-0463 lean4: rung one has no Lean package; its results are finite computation and one open item
- TFQ-0463 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG1-STREAM-AS-RESPONSE` `GAP_NO_DERIVATION`: [PGW-RUNG0-INHERITANCE-REPLAY](PGW-RUNG0-INHERITANCE-REPLAY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

