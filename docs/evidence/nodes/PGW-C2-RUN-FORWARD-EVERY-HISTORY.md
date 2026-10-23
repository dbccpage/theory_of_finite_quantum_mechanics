# PGW-C2-RUN-FORWARD-EVERY-HISTORY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuation attempt two (pull request 269) takes Challenge 4 and runs every one of the 144 engines forward from both sealed readings to declared bounds (two items, growth below four data, fifteen rounds, a node guard of 250 per run): 288 runs, 25,932 nodes, 69,490 edges and 43,846 merges, every node and edge replayed and quotiented by the implemented isomorphism. In the local Lean package SecondRun/Run.lean, for every history of sealed events and switch markers from any engine state, the element count never falls (ereplay_elems_le), a history leaving it unchanged leaves the regime unchanged, no further history reaches a regime once left (no_return), and on a history returning to its starting state every state part of the way holds the starting regime (cycle_regime_const). A pair collapsed with a common third datum is not separable in that regime (not_separable_through), the shape of all 772 refused apart demands of the runs.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Sealed kernel slice reconstructed verbatim in SecondRun/Kernel.lean from Derivation/Basic.lean and Derivation/Inertia.lean (assumption)
- Engine event grammar: a sealed event, or a switch marker that keeps the regime and flips the mode (assumption)

## Bottleneck

The Lean speaks of histories, not of the Python runs: that each run edge is such a history is read, not proved; the responder and generators are not reconstructed in Lean, not_separable_through is about one regime, and the run counts hold at the declared bounds only.

## Source status

lean4/SecondRun/Run.lean; continuation.txt section 4 row 4 and section 12 attempt two; run ledger SD-R-2 to SD-R-4

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/SecondRun/Run.lean`

- file: [lean4/Imported/Genesis19l57g1/SecondRun/Run.lean](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)
- sha256 (`bytes`): `4db53efe47bb57435f39520ea44cacaab6e0a73f03f8a9e4d5a3fee64c44259e`
- cited in: node.lean, node.source, record TFQ-0475
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.SecondRun.Run`): recorded sha256 `4db53efe47bb57435f39520ea44cacaab6e0a73f03f8a9e4d5a3fee64c44259e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/SecondRun/Run.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cycle_regime_const` | yes | yes | yes | Quot.sound, propext | `#print axioms cycle_regime_const` |
| `ereplay_elems_le` | yes | yes | yes | Quot.sound, propext | `#print axioms ereplay_elems_le` |
| `no_return` | yes | yes | yes | Quot.sound, propext | `#print axioms no_return` |
| `not_separable_through` | yes | yes | yes | propext | `#print axioms not_separable_through` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0475_c2_run_forward_every_history.md`

- file: [dag/derivations/02_genesis/tfq_0475_c2_run_forward_every_history.md](../../../dag/derivations/02_genesis/tfq_0475_c2_run_forward_every_history.md)
- sha256 (`lf-normalised`): `7ab6a8ab5182b23f88a16b131faf0f636688bc5c09824a51cd35669a6c7207b6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0475
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::build_run`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py::replay_mismatches`

## Absences recorded by the TFQ records

- TFQ-0475 rust: the second-derivation run tree holds no Rust; the sealed Rust predates the switch marker

## Routes

Incoming (1):

- `PGW-R-C2-RUN-FORWARD-EVERY-HISTORY` `DERIVED_LEAN`: [PGW-C1-ENGINE-CLASS-144](PGW-C1-ENGINE-CLASS-144.md) (CONDITIONAL), [PG-GEN-NO-RETURN](PG-GEN-NO-RETURN.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-FORCED-CENSUS-COLUMN` `COMPUTED`: [PGW-FORCED-CENSUS-COLUMN](PGW-FORCED-CENSUS-COLUMN.md) (COMPUTATIONALLY_CHECKED)
