# PGW-STREAM-AT-FOUR-ITEMS

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Challenge 1, the stream as a response, is OPEN with scoped finite results only: no retained V1 minimum of 1680 carries a datum, 32 of them were selected at three items, all fourteen recorded refusal situations are answered at exactly three items, and two new first refusals appear. 1039 nodes stopped at the guard, targets after a node's first refusal were not searched (the first-refusal short-circuit), and four items were not computed (R1-X PENDING); V2 beyond nineteen situations and the narrow-versus-wide comparison are also OPEN. Attempt two's runs add only that no response carries a datum at two items, and the continuation was not authorized to take Challenge 1 up.

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

Open; the three-item answers hold at the computed scope only, and a refusal at three items is not a refusal at four.

## Source status

continuation.txt §4 row 1 (Challenge 1) and §13 stream as a response

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0502_stream_at_four_items.md`

- file: [dag/derivations/02_genesis/tfq_0502_stream_at_four_items.md](../../../dag/derivations/02_genesis/tfq_0502_stream_at_four_items.md)
- sha256 (`lf-normalised`): `ce1b0f93e4e3d31e3fff25e65aee7565e601ca38164fcf8976c566ea49364a57`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0502
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py::build_stream_tree`

## Absences recorded by the TFQ records

- TFQ-0502 lean4: no Lean statement of the stream challenge
- TFQ-0502 rust: no Rust port of the stream tree

## Routes

Incoming (1):

- `PGW-R-STREAM-AT-FOUR-ITEMS` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

