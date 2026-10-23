# PGW-RUNS-PAST-DECLARED-BOUNDS

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Challenge 4 was run to declared bounds only (fifteen rounds, a node guard of 250 per run, growth below four data, two items): 11,266 nodes stopped at the guard and 368 at the bound, and 116 runs are not closed. Attempt two's leftovers H-2 to H-9 remain: the 970 refused same demands (H-2), the twenty-eight merges rung two's observable budget refused (H-3), the 482 regimes above the brute-force key limit (H-4), a distance on adjacency (H-5), a reading of carrying forward that admits switch (H-6), the forty-four closed runs with switch cycles UNDECIDED under ONE VALUE PER NODE (H-7), why E1 and E5 share one run under mu2 (H-8), and five data (H-9). Whether the augmentation sequence is unbounded is unresolved in the sealed paper (question 7): with the external continuation policy every requested depth tried was reached and every supplied demand has a response (mark_progress), and no unboundedness claim is made.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; every FORCED verdict other than the element count, irreversibility and two-ness over the LIVE members is a computation at the declared bounds.

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

### Documents and data: `dag/derivations/02_genesis/tfq_0501_runs_past_declared_bounds.md`

- file: [dag/derivations/02_genesis/tfq_0501_runs_past_declared_bounds.md](../../../dag/derivations/02_genesis/tfq_0501_runs_past_declared_bounds.md)
- sha256 (`lf-normalised`): `6f80ac71305e1c02d49ffd198c71f9f92e567ad4ce61ed7d64bf4a45b64813ed`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0501
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

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
