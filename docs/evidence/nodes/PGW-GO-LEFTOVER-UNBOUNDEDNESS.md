# PGW-GO-LEFTOVER-UNBOUNDEDNESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The tenth derivation records a leftover with each change in a side ledger and keeps the ninth's state model; the sixteenth admits the recorded leftover back into the state. The feedback does not terminate: remove-then-admit is a two-change cycle at every state with an assertion, and a term added and identified away is one at every state with a term, while the ninth's add-then-remove is not a cycle. In Lean, if Reach16 s t n holds from a well-formed state with a term then Reach16 s t (2k + n) holds for every k (Reach16.unbounded), and ara reaches itself in 2k changes by removing and admitting for every k (admit_remove_unbounded), so the lengths of sequences reaching a result are unbounded.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Unbounded lengths of sequences reaching a result, not an unbounded set of results; the fewest changes to a result stays its potential (ledger D3), and nothing here is a claim about time or physical recurrence.

## Source status

001_genesis_ongoing_h3v7n5qf paper/sixteenth/claim_ledger.md D9; lean4/Sixteenth/Reach.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean`

- file: [lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean](../../../lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean)
- sha256 (`bytes`): `a566d3fd20c1d547de13b81216d8da513ee7b427cc9d8d51e9cdd2a2cf76e7b1`
- cited in: node.lean, node.source, record TFQ-0482
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Sixteenth.Reach`): recorded sha256 `a566d3fd20c1d547de13b81216d8da513ee7b427cc9d8d51e9cdd2a2cf76e7b1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach16.unbounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach16.unbounded` |
| `admit_remove_unbounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms admit_remove_unbounded` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0482_go_leftover_unboundedness.md`

- file: [dag/derivations/02_genesis/tfq_0482_go_leftover_unboundedness.md](../../../dag/derivations/02_genesis/tfq_0482_go_leftover_unboundedness.md)
- sha256 (`lf-normalised`): `3194d80f19535f89033c19da0c43a9214e7accdf278172046109569c7f78d0c8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0482
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/sixteenth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/sixteenth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_18_leftovers_unboundedness.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_18_leftovers_unboundedness.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/sixteenth/reach.py::reachable16`

## Absences recorded by the TFQ records

- TFQ-0482 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-LEFTOVER-UNBOUNDEDNESS` `DERIVED_LEAN`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (2):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-GO-H1-CANCELLATION-EXCESS` `DERIVED_LEAN`: [PGW-GO-H1-CANCELLATION-EXCESS](PGW-GO-H1-CANCELLATION-EXCESS.md) (PROVED_LEAN)
