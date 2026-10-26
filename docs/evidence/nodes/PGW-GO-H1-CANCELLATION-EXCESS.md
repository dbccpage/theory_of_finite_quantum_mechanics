# PGW-GO-H1-CANCELLATION-EXCESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Climbing round H1, installed as the twenty-second derivation, replaces one sameness sentence of the ninth seed: two results are the same when they differ only in how their terms are written, or only by an xry and an xsy asserted together. Two states are then one result exactly when they have equally many terms and, after one rewriting, the same excess e = M_r − M_s at every ordered pair (gen_iff_same, same_iff_excess), and each result has one plain state up to writing, asserting no pair in both relations (plain_reduced). The fewest changes to a result is Φ(G) = n + Σ|e(x,y)|, the plain state's size, and a shortest sequence is additions only through plain states (fewest_changes).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Chosen reading C-J1: one more xry and xsy on one pair, x = y allowed, sameness the equivalence generated with rewriting (assumption)

## Bottleneck

For the chosen reading C-J1 only (the unchosen C-J2 and C-J3 give 29 and 1081 results against 673 at two terms and eight rounds); here an addition can undo an addition, so the ninth's no-return for additions does not survive the new sameness.

## Source status

001_genesis_ongoing_h3v7n5qf paper/twentysecond/claim_ledger.md D1 and D4; lean4_core/Twentysecond

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean)
- sha256 (`bytes`): `5c5435dae41ae384a3b9a9c003d45a6feb9f70f6e87b69275b74b4fecd299359`
- cited in: node.lean, record TFQ-0483
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentysecond.Cost`): recorded sha256 `5c5435dae41ae384a3b9a9c003d45a6feb9f70f6e87b69275b74b4fecd299359` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fewest_changes` | yes | yes | yes | Quot.sound, propext | `#print axioms fewest_changes` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean)
- sha256 (`bytes`): `53e255f2501fb9e54f1e440348ee89c917ffb1ff86de9c9a504d55f8989e2ab2`
- cited in: node.lean, record TFQ-0483
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentysecond.Plain`): recorded sha256 `53e255f2501fb9e54f1e440348ee89c917ffb1ff86de9c9a504d55f8989e2ab2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `plain_reduced` | yes | yes | yes | Quot.sound, propext | `#print axioms plain_reduced` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean)
- sha256 (`bytes`): `60043763e2bc84e81653454381f08e658b5d40cb6fe3bc08c3a584e639650097`
- cited in: node.lean, record TFQ-0483
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentysecond.Same`): recorded sha256 `60043763e2bc84e81653454381f08e658b5d40cb6fe3bc08c3a584e639650097` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gen_iff_same` | yes | yes | yes | Quot.sound, propext | `#print axioms gen_iff_same` |
| `same_iff_excess` | yes | yes | yes | Quot.sound, propext | `#print axioms same_iff_excess` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0483_go_h1_cancellation_excess.md`

- file: [dag/derivations/02_genesis/tfq_0483_go_h1_cancellation_excess.md](../../../dag/derivations/02_genesis/tfq_0483_go_h1_cancellation_excess.md)
- sha256 (`lf-normalised`): `9fc3bcced0328cd6e4a0691b1cca9e1af02a80dfc7896c74740e45d60af7d418`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0483
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentysecond/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentysecond/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_19_round_r1_cancellation.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_19_round_r1_cancellation.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentysecond/state.py::cost`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentysecond/state.py::excess`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentysecond/state.py::plain`

## Absences recorded by the TFQ records

- TFQ-0483 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-H1-CANCELLATION-EXCESS` `DERIVED_LEAN`: [PGW-GO-LEFTOVER-UNBOUNDEDNESS](PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-H2-STATE-RAISING-GAUGE` `DERIVED_LEAN`: [PGW-GO-H2-STATE-RAISING-GAUGE](PGW-GO-H2-STATE-RAISING-GAUGE.md) (PROVED_LEAN)
