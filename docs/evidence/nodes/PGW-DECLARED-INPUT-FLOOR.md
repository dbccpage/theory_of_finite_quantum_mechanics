# PGW-DECLARED-INPUT-FLOOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. The declared bound record is rounds 15, node guard 250, data ceiling 4, item bound 2, input count 2, engine count 4, and reading count 2. The input count equals the item bound. One is strictly below the input count. The guard is strictly above the round count. The engine count is not the reading count. The data counts strictly below 4, taken from the candidates 0, 1, 2, 3, and 4, are 0, 1, 2, and 3. There are 4 such counts. The ceiling itself is not strictly below 4.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The seven numerals are a declared bound record. They are not a floor for the input count. They do not show that four engines carry the grammar forward, and they do not decide the other reading of the completion gate. Whether the four carry forward past the bounds stays open (H-1, SD-R-11). A reduction below two that holds past the bounds of attempt two stays open. The completion-gate clause was frozen as NOT_ESTABLISHED. Status stays OPEN.

## Source status

closeout.txt §9.1 D10 and §8; continuation.txt §13 declared-input floor (H-1)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwDeclaredInputFloor.lean`

- file: [lean4/CampaignPgwDeclaredInputFloor.lean](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- sha256 (`bytes`): `4d60da82673bbba0522a875cbfa3b99c7ba076845b877b5a97438110da6e5beb`
- cited in: node.lean, receipt dag/research/campaign_pgw-declared-input-floor_lean_replay.json (CampaignPgwDeclaredInputFloor), record TFQ-0498
- replay: `verified`
  - receipt [dag/research/campaign_pgw-declared-input-floor_lean_replay.json](../../../dag/research/campaign_pgw-declared-input-floor_lean_replay.json) (module `CampaignPgwDeclaredInputFloor`): recorded sha256 `4d60da82673bbba0522a875cbfa3b99c7ba076845b877b5a97438110da6e5beb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwDeclaredInputFloor`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwBounds_values` | yes | yes | yes | none | `#print axioms pgwBounds_values` |
| `pgwCeiling_not_below` | yes | yes | yes | none | `#print axioms pgwCeiling_not_below` |
| `pgwEngines_ne_readings` | yes | yes | yes | none | `#print axioms pgwEngines_ne_readings` |
| `pgwGuard_above_rounds` | yes | yes | yes | none | `#print axioms pgwGuard_above_rounds` |
| `pgwInput_eq_items` | yes | yes | yes | none | `#print axioms pgwInput_eq_items` |
| `pgwOne_below_input` | yes | yes | yes | none | `#print axioms pgwOne_below_input` |
| `pgwStrictlyBelow_length` | yes | yes | yes | none | `#print axioms pgwStrictlyBelow_length` |
| `pgwStrictlyBelow_list` | yes | yes | yes | none | `#print axioms pgwStrictlyBelow_list` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-declared-input-floor.py`

- file: [checks/independent/pgw-declared-input-floor.py](../../../checks/independent/pgw-declared-input-floor.py)
- sha256 (`bytes`): `98956050fb938c093d9fa9beab28ca52c8cb1cbe64d40775e28d4dd12333d4ea`
- cited in: record TFQ-0498

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0498_declared_input_floor.md`

- file: [dag/derivations/02_genesis/tfq_0498_declared_input_floor.md](../../../dag/derivations/02_genesis/tfq_0498_declared_input_floor.md)
- sha256 (`lf-normalised`): `c4907557713f1bfee4c281f1f8bf6e52d53351e0c9b02a04562eeb0d825dd4d6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0498
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-declared-input-floor.md`

- file: [dag/derivations/independent/pgw-declared-input-floor.md](../../../dag/derivations/independent/pgw-declared-input-floor.md)
- sha256 (`lf-normalised`): `c202e43a16dd568440cfec943b4a5c4a30191d9b2e0b6aa1c60da6635fd2e6ea`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-declared-input-floor_lean_replay.json`

- file: [dag/research/campaign_pgw-declared-input-floor_lean_replay.json](../../../dag/research/campaign_pgw-declared-input-floor_lean_replay.json)
- sha256 (`lf-normalised`): `93357c5e4b54a4901396df7a213d1f37cd17cc8329546481222586b053f4151f`
- cited in: node.source
- counts toward the grade: yes

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

- TFQ-0498 lean4: no Lean statement of a declared-input floor
- TFQ-0498 rust: no Rust check of the input count

## Routes

Incoming (1):

- `PGW-R-DECLARED-INPUT-FLOOR` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

