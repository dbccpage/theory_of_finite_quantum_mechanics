# PGW-CLOSED-BASELINE-TERMINATES

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With the external continuation policy disabled, the closed-system baselines are small: reading L has 4 nodes and 3 terminal branches, reading F has 20 nodes and 16 terminal branches, and both have zero guard-cut, round-cut and open branches. Every maximal branch ends at the all-pairs-separated fixpoint within the pair bound, using 1 round in L (bound 1) and 3 in F (bound 3), and the termination flag is computed over all maximal branches rather than from one terminal node. Under the declared round shape a closed run from an empty requirement store makes at most n(n−1)/2 rounds (closedRun_round_bound_from_empty).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Declared resource bounds of genesis_source.txt section 1 with the external continuation policy disabled (assumption)

## Bottleneck

A bounded theorem: termination of every maximal branch is computed within the declared bounds, and that each exported round has the declared shape (one fresh imposition, no fresh-datum item) stays computational.

## Source status

genesis_source.txt section 8.5 \[bounded theorem\] (CL-CLOSURE-TERMINATION); Rounds.lean round bound

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean)
- sha256 (`bytes`): `516b2e4ea8d722a27a9ddd9509b1002f0a35354b6a0e586795318a0924f57655`
- cited in: node.lean, record TFQ-0449
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Rounds`): recorded sha256 `516b2e4ea8d722a27a9ddd9509b1002f0a35354b6a0e586795318a0924f57655` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closedRun_round_bound_from_empty` | yes | yes | yes | Quot.sound, propext | `#print axioms closedRun_round_bound_from_empty` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0449_closed_baseline_terminates.md`

- file: [dag/derivations/02_genesis/tfq_0449_closed_baseline_terminates.md](../../../dag/derivations/02_genesis/tfq_0449_closed_baseline_terminates.md)
- sha256 (`lf-normalised`): `31cd38351e7a2301a8a3c423c4e5eae4e6bd76b22542173199053489cb1927bd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0449
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::build_tree`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::closed_system_baseline_reading_f`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::closed_system_baseline_reading_l`

## Routes

Incoming (1):

- `PGW-R-CLOSED-BASELINE-TERMINATES` `COMPUTED`: [TFQ-0383](TFQ-0383.md) (SOURCE_RECORD)

Outgoing (1):

- `PGW-R-POLICY-ENDPOINT-ALL-SEPARATED` `DERIVED_LEAN`: [PGW-POLICY-ENDPOINT-ALL-SEPARATED](PGW-POLICY-ENDPOINT-ALL-SEPARATED.md) (PROVED_LEAN)
