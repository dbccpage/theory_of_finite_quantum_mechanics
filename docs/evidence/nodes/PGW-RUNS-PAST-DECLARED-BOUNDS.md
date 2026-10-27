# PGW-RUNS-PAST-DECLARED-BOUNDS

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Challenge 4 was run to declared bounds only (fifteen rounds, a node guard of 250 per run, growth below four data, two items): 11,266 nodes stopped at the guard and 368 at the bound, and 116 runs are not closed. Attempt two's leftovers H-2 to H-9 remain: the 970 refused same demands (H-2), the twenty-eight merges rung two's observable budget refused (H-3), the 482 regimes above the brute-force key limit (H-4), a distance on adjacency (H-5), a reading of carrying forward that admits switch (H-6), the forty-four closed runs with switch cycles UNDECIDED under ONE VALUE PER NODE (H-7), why E1 and E5 share one run under mu2 (H-8), and five data (H-9). Whether the augmentation sequence is unbounded is unresolved in the sealed paper (question 7): with the external continuation policy every requested depth tried was reached and every supplied demand has a response (mark_progress), and no unboundedness claim is made.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; every FORCED verdict other than the element count, irreversibility and two-ness over the LIVE members is a computation at the declared bounds. Narrowed in Lean 4 to five records on that line: (15, 250, 3, 2) is inside, and one extra round, one extra node, data 4, or three items is outside. The census of stopped runs, leftovers H-2 to H-9, and whether the augmentation sequence is unbounded stay open.

## Source status

continuation.txt §13 runs past the bounds and attempt two's leftovers H-2 to H-9; genesis_source.txt §10 question 7

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Progress.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Progress.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Progress.lean)
- sha256 (`bytes`): `1a6864314f6909227f3b41d3af68bcbca5b1c286e8a2c1e889381d302e8a92ce`
- cited in: node.lean, record TFQ-0501
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Progress`): recorded sha256 `1a6864314f6909227f3b41d3af68bcbca5b1c286e8a2c1e889381d302e8a92ce` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Progress.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mark_progress` | yes | yes | yes | Quot.sound, propext | `#print axioms mark_progress` |

- counts toward the grade: yes

### Lean: `lean4/PregenesisRunsPastDeclaredBounds.lean`

- file: [lean4/PregenesisRunsPastDeclaredBounds.lean](../../../lean4/PregenesisRunsPastDeclaredBounds.lean)
- sha256 (`bytes`): `a8ca3ae2ff2c74e52d4ebdfbc8d625d47beb643a6fc0c6d0ace2cb589fd0b574`
- cited in: node.lean, receipt dag/research/campaign_pgw-runs-past-declared-bounds_lean_replay.json (PregenesisRunsPastDeclaredBounds), receipt dag/research/pr_353_review_replay.json (PregenesisRunsPastDeclaredBounds), record TFQ-0501
- replay: `verified`
  - receipt [dag/research/campaign_pgw-runs-past-declared-bounds_lean_replay.json](../../../dag/research/campaign_pgw-runs-past-declared-bounds_lean_replay.json) (module `PregenesisRunsPastDeclaredBounds`): recorded sha256 `a8ca3ae2ff2c74e52d4ebdfbc8d625d47beb643a6fc0c6d0ace2cb589fd0b574` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_353_review_replay.json](../../../dag/research/pr_353_review_replay.json) (module `PregenesisRunsPastDeclaredBounds`): recorded sha256 `a8ca3ae2ff2c74e52d4ebdfbc8d625d47beb643a6fc0c6d0ace2cb589fd0b574` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisRunsPastDeclaredBounds`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwBoundDataFour` | yes | yes | yes | none | `#print axioms pgwBoundDataFour` |
| `pgwBoundItemPast` | yes | yes | yes | none | `#print axioms pgwBoundItemPast` |
| `pgwBoundNodePast` | yes | yes | yes | none | `#print axioms pgwBoundNodePast` |
| `pgwBoundOnLine` | yes | yes | yes | none | `#print axioms pgwBoundOnLine` |
| `pgwBoundRoundPast` | yes | yes | yes | none | `#print axioms pgwBoundRoundPast` |

- counts toward the grade: yes

### Python: `checks/independent/pgw-runs-past-declared-bounds.py`

- file: [checks/independent/pgw-runs-past-declared-bounds.py](../../../checks/independent/pgw-runs-past-declared-bounds.py)
- sha256 (`bytes`): `ce0b5310719dfe57edd31eb5be4cc9caccb6f845d6a098e52e2e240d87ecf462`
- cited in: record TFQ-0501

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0501_runs_past_declared_bounds.md`

- file: [dag/derivations/02_genesis/tfq_0501_runs_past_declared_bounds.md](../../../dag/derivations/02_genesis/tfq_0501_runs_past_declared_bounds.md)
- sha256 (`lf-normalised`): `a190c0ae5eeff74f4ede2ad45650fdeb4b421d42a56e14e1a0b6922f7ead6825`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0501
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-runs-past-declared-bounds.md`

- file: [dag/derivations/independent/pgw-runs-past-declared-bounds.md](../../../dag/derivations/independent/pgw-runs-past-declared-bounds.md)
- sha256 (`lf-normalised`): `a56e45ef1d4fa64579db2d6ffe9b4131a3845c2e1cd92be0f6fef6815e206a7b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-runs-past-declared-bounds_lean_replay.json`

- file: [dag/research/campaign_pgw-runs-past-declared-bounds_lean_replay.json](../../../dag/research/campaign_pgw-runs-past-declared-bounds_lean_replay.json)
- sha256 (`lf-normalised`): `7e821dcc60b111024286b2480bc55678b9479dd1ecd475656b768e207fe75132`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::frontier`

## Absences recorded by the TFQ records

- TFQ-0501 rust: no Rust port of the forward runs

## Routes

Incoming (1):

- `PGW-R-RUNS-PAST-DECLARED-BOUNDS` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (4):

- `APP-R-AUTH-FUEL-EXHAUSTION-TYPED-STOP` `DERIVED_PROSE`: [AUTH-FUEL-EXHAUSTION-TYPED-STOP](AUTH-FUEL-EXHAUSTION-TYPED-STOP.md) (DEFINITION)
- `APP-R-AUTHF-DTM0-FIXTURES` `COMPUTED`: [AUTHF-DTM0-FIXTURES](AUTHF-DTM0-FIXTURES.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-AUTHF-DTM0-SIMULATION-OPEN` `GAP_NO_DERIVATION`: [AUTHF-DTM0-SIMULATION-OPEN](AUTHF-DTM0-SIMULATION-OPEN.md) (OPEN)
- `APP-R-COMP-C3-BOUNDED-REACH-DECIDABLE` `DERIVED_LEAN`: [COMP-C3-BOUNDED-REACH-DECIDABLE](COMP-C3-BOUNDED-REACH-DECIDABLE.md) (PROVED_LEAN)
