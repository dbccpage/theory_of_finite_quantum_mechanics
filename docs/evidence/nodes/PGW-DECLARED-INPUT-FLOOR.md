# PGW-DECLARED-INPUT-FLOOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No floor proof exists for the count of declared inputs (D10, H-1); the count stays two. Continuation attempt two found, at its declared bounds (fifteen rounds, a node guard of 250 per run, growth below four data, two items) and under its literal reading of carrying forward, four engines that carry the grammar forward declaring the stake and not the stream (SD-R-11), and calls this neither a floor proof nor a reduction outside those bounds. The completion-gate clause admits two readings of these bounded one-input carriers and was frozen as NOT_ESTABLISHED; whether the four carry forward past the bounds is OPEN (H-1, which needs the responder in Lean). Narrowed in Lean 4 to two named inputs, stake and stream, and four carriers that each declare the stake and not the stream. The named list has length 2. Each of the four carriers has declared count 1, and 1 is below 2. The reading that every one of these four has count at least 2 is false. The reading that one of them has count 1 is true. The declared numerals are 15 rounds, a node guard of 250, a data bound of 4, and an item bound of 2. A carrier that declares neither input has count 0 and is not one of the four. These four carriers are not a floor for every later carrier, and the attempt-two search is not replayed. AuthorityEffect is None.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; the bounded one-input carriers are a computation at declared bounds, and the clause's other reading was left to the author, who approved the freeze without a separate ruling. This file checks four carriers on the two names stake and stream: each declares the stake only, so the count is 1, below 2. The numerals 15, 250, 4, and 2 are recorded and are not a search. A floor for every carrier, a reduction past these four, and the attempt-two replay stay open.

## Source status

closeout.txt §9.1 D10 and §8; continuation.txt §13 declared-input floor (H-1)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwDeclaredInputFloor.lean`

- file: [lean4/CampaignPgwDeclaredInputFloor.lean](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- sha256 (`bytes`): `90c4a432513ea82d1dddb40985300b11698a5045ac7109b1e26265496bdecb42`
- cited in: node.lean, receipt dag/research/campaign_pgw-declared-input-floor_lean_replay.json (CampaignPgwDeclaredInputFloor), receipt dag/research/pr_351_review_replay.json (CampaignPgwDeclaredInputFloor), record TFQ-0498
- replay: `verified`
  - receipt [dag/research/campaign_pgw-declared-input-floor_lean_replay.json](../../../dag/research/campaign_pgw-declared-input-floor_lean_replay.json) (module `CampaignPgwDeclaredInputFloor`): recorded sha256 `90c4a432513ea82d1dddb40985300b11698a5045ac7109b1e26265496bdecb42` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_351_review_replay.json](../../../dag/research/pr_351_review_replay.json) (module `CampaignPgwDeclaredInputFloor`): recorded sha256 `90c4a432513ea82d1dddb40985300b11698a5045ac7109b1e26265496bdecb42` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwDeclaredInputFloor`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignPgwDeclaredInputFloor.declared_bounds` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.declared_bounds` |
| `CampaignPgwDeclaredInputFloor.each_count_is_one` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.each_count_is_one` |
| `CampaignPgwDeclaredInputFloor.each_declares_stake_not_stream` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.each_declares_stake_not_stream` |
| `CampaignPgwDeclaredInputFloor.empty_carrier_is_not_among_the_four` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.empty_carrier_is_not_among_the_four` |
| `CampaignPgwDeclaredInputFloor.four_engines` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.four_engines` |
| `CampaignPgwDeclaredInputFloor.one_below_two` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.one_below_two` |
| `CampaignPgwDeclaredInputFloor.readings_disagree` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.readings_disagree` |
| `CampaignPgwDeclaredInputFloor.vocabulary_is_two` | yes | yes | yes | none | `#print axioms CampaignPgwDeclaredInputFloor.vocabulary_is_two` |
| `declared_bounds` | yes | yes | yes | none | `#print axioms declared_bounds` |
| `each_count_is_one` | yes | yes | yes | none | `#print axioms each_count_is_one` |
| `each_declares_stake_not_stream` | yes | yes | yes | none | `#print axioms each_declares_stake_not_stream` |
| `empty_carrier_is_not_among_the_four` | yes | yes | yes | none | `#print axioms empty_carrier_is_not_among_the_four` |
| `four_engines` | yes | yes | yes | none | `#print axioms four_engines` |
| `one_below_two` | yes | yes | yes | none | `#print axioms one_below_two` |
| `readings_disagree` | yes | yes | yes | none | `#print axioms readings_disagree` |
| `vocabulary_is_two` | yes | yes | yes | none | `#print axioms vocabulary_is_two` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-declared-input-floor.py`

- file: [checks/independent/pgw-declared-input-floor.py](../../../checks/independent/pgw-declared-input-floor.py)
- sha256 (`bytes`): `8a2e851ff5869b81e6c556146eb7e2fce8b8a27182fbcfd059ec54e75f9cb620`
- cited in: record TFQ-0498
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0498_declared_input_floor.md`

- file: [dag/derivations/02_genesis/tfq_0498_declared_input_floor.md](../../../dag/derivations/02_genesis/tfq_0498_declared_input_floor.md)
- sha256 (`lf-normalised`): `e9e9d2cc02ddef24dbb0445c2d0703730c504d5b83d18e4d75389b7557707b10`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0498
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

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::carries_forward`

## Absences recorded by the TFQ records

- TFQ-0498 rust: no Rust check of the input count

## Routes

Incoming (1):

- `PGW-R-DECLARED-INPUT-FLOOR` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

