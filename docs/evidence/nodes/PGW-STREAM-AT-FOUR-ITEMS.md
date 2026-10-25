# PGW-STREAM-AT-FOUR-ITEMS

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed in Lean 4 to one refusal pair and one search flag. A refusal at item count 3 is a refusal at 3 and is not a refusal at 4. A reply at item count 4 may refuse, and a reply at item count 4 may accept. With the short-circuit flag set, a target at 4 after a refusal at 3 is not searched, while the target at 3 is searched. With the flag clear, the target at 4 is searched. The retained minima, the refusal census, the guard-stopped frontier, and the four-item stream computation stay open.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; the three-item answers hold at the computed scope only, and a refusal at three items is not a refusal at four. Narrowed in Lean 4 to one reply at item count 3, two replies at item count 4, and one short-circuit flag. The retained minima, the refusal census, the guard-stopped frontier, and the four-item stream computation stay open.

## Source status

continuation.txt §4 row 1 (Challenge 1) and §13 stream as a response

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwStreamAtFourItems.lean`

- file: [lean4/CampaignPgwStreamAtFourItems.lean](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- sha256 (`bytes`): `8f9250d6b36cbf05890fd86f04f44b36a16c9dd83ee67161bd88f63aa2d88de5`
- cited in: node.lean, receipt dag/research/campaign_pgw-stream-at-four-items_lean_replay.json (CampaignPgwStreamAtFourItems), receipt dag/research/pr_354_review_replay.json (CampaignPgwStreamAtFourItems), record TFQ-0502
- replay: `verified`
  - receipt [dag/research/campaign_pgw-stream-at-four-items_lean_replay.json](../../../dag/research/campaign_pgw-stream-at-four-items_lean_replay.json) (module `CampaignPgwStreamAtFourItems`): recorded sha256 `8f9250d6b36cbf05890fd86f04f44b36a16c9dd83ee67161bd88f63aa2d88de5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_354_review_replay.json](../../../dag/research/pr_354_review_replay.json) (module `CampaignPgwStreamAtFourItems`): recorded sha256 `8f9250d6b36cbf05890fd86f04f44b36a16c9dd83ee67161bd88f63aa2d88de5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwStreamAtFourItems`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwStreamAtThree` | yes | yes | yes | none | `#print axioms pgwStreamAtThree` |
| `pgwStreamFourAccepts` | yes | yes | yes | none | `#print axioms pgwStreamFourAccepts` |
| `pgwStreamFourRefuses` | yes | yes | yes | none | `#print axioms pgwStreamFourRefuses` |
| `pgwStreamOpenSearchReachesFour` | yes | yes | yes | none | `#print axioms pgwStreamOpenSearchReachesFour` |
| `pgwStreamShortCircuitKeepsThree` | yes | yes | yes | none | `#print axioms pgwStreamShortCircuitKeepsThree` |
| `pgwStreamShortCircuitSkipsFour` | yes | yes | yes | none | `#print axioms pgwStreamShortCircuitSkipsFour` |
| `pgwStreamThreeNotFour` | yes | yes | yes | none | `#print axioms pgwStreamThreeNotFour` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-stream-at-four-items.py`

- file: [checks/independent/pgw-stream-at-four-items.py](../../../checks/independent/pgw-stream-at-four-items.py)
- sha256 (`bytes`): `1ed95383e063f8eba82c623fcd1ee2a33722e3d1c2a0e900dbd3cc5911fce2d6`
- cited in: record TFQ-0502

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0502_stream_at_four_items.md`

- file: [dag/derivations/02_genesis/tfq_0502_stream_at_four_items.md](../../../dag/derivations/02_genesis/tfq_0502_stream_at_four_items.md)
- sha256 (`lf-normalised`): `31340e8bf6486643dcdd4b5cda566e415079da6c4421cc0946ca4b767be06f9d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0502
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-stream-at-four-items.md`

- file: [dag/derivations/independent/pgw-stream-at-four-items.md](../../../dag/derivations/independent/pgw-stream-at-four-items.md)
- sha256 (`lf-normalised`): `ac5a8e38e8db5b2533adb9ddebf6d226b5a77555c06aa07b170c3e939783bbc7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-stream-at-four-items_lean_replay.json`

- file: [dag/research/campaign_pgw-stream-at-four-items_lean_replay.json](../../../dag/research/campaign_pgw-stream-at-four-items_lean_replay.json)
- sha256 (`lf-normalised`): `ffe53dba59438bacc9ada9367b76c4a7cd4266c08f5cfee36fd917fb7732847a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py::build_stream_tree`

## Absences recorded by the TFQ records

- TFQ-0502 rust: no Rust port of the stream tree

## Routes

Incoming (1):

- `PGW-R-STREAM-AT-FOUR-ITEMS` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

