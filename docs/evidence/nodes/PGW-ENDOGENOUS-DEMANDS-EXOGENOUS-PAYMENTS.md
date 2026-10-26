# PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Without the external continuation policy the closed system saturates: under the declared round shape a closed run from an empty requirement store makes at most n(n-1)/2 rounds (Lean closedRun_round_bound_from_empty, 2 * rounds ≤ n * (n - 1)), and at the fixpoint any further requirement needs a fresh datum (external supply) or a new requirement kind (external goal) (genesis_source §9 item 6). With external supply the runs grow in width, not in kind: the sealed mu2 trees record 53 (reading L) and 83 (reading F) innovation edges (fresh form plus instance), which the education audit reads as unary forms with 0 binary (finite computation to the requested depth of 15 transition steps). In the reflective composite reflState n demand never dries: for n ≥ 3 the distinct data 1 and 2 have equal depth-one profiles (Lean Generator.generation_never_dries). Within the declared local finite-alphabet class (one radius d, one colour bound k independent of chain length) every strategy fires and none clears (Lean G1Class.g1_class_exclusion), while the clearing members perPairFreshMark (recurring import) and valued (one-time identity-grade rule) lie outside the finite declaration. The education audit names the pattern 'endogenous demands, exogenous payments'.

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

- Declared round shape of a closed run: a fresh imposed target and a response admitting no fresh datum (assumption)
- Declared local finite-alphabet strategy class LocalStrategy d with FiniteDeclaration k (assumption)

## Bottleneck

Class-relative and carrier-relative: g1_class_exclusion speaks only of finite-alphabet local strategies on the reflective chain, the one-time valued rule clears with no recurring import (clears_does_not_imply_not_fires), and the unary-only innovation count is a bounded computation, not a theorem about longer runs.

## Source status

genesis_source.txt §8.4-§9; Derivation/Rounds.lean, Generator.lean, G1Class.lean; education archive §1 (audit reading)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/G1Class.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/G1Class.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/G1Class.lean)
- sha256 (`bytes`): `8d4fe298b5673c098cc4ea017e1b2ba5f7f9aa80fae2768dd93781885fab6073`
- cited in: node.lean, record TFQ-0487
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.G1Class`): recorded sha256 `8d4fe298b5673c098cc4ea017e1b2ba5f7f9aa80fae2768dd93781885fab6073` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/G1Class.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `clears_does_not_imply_not_fires` | yes | yes | yes | Quot.sound, propext | `#print axioms clears_does_not_imply_not_fires` |
| `g1_class_exclusion` | yes | yes | yes | Quot.sound, propext | `#print axioms g1_class_exclusion` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Generator.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Generator.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Generator.lean)
- sha256 (`bytes`): `62f194eb1e5b947c99657d3d308c32cb2839f636143a7b36ded8af5d65da36ae`
- cited in: node.lean, record TFQ-0487
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Generator`): recorded sha256 `62f194eb1e5b947c99657d3d308c32cb2839f636143a7b36ded8af5d65da36ae` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Generator.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `generation_never_dries` | yes | yes | yes | Quot.sound, propext | `#print axioms generation_never_dries` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean)
- sha256 (`bytes`): `516b2e4ea8d722a27a9ddd9509b1002f0a35354b6a0e586795318a0924f57655`
- cited in: node.lean, record TFQ-0487
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Rounds`): recorded sha256 `516b2e4ea8d722a27a9ddd9509b1002f0a35354b6a0e586795318a0924f57655` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closedRun_round_bound_from_empty` | yes | yes | yes | Quot.sound, propext | `#print axioms closedRun_round_bound_from_empty` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md`

- file: [dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md](../../../dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md)
- sha256 (`lf-normalised`): `5bee688a7c0ec43f43a981425722d4a2897623b28f70720a394f43e6459df391`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0487
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/local_strategy.py::classification`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::closure_round_bound`

## Routes

Incoming (1):

- `PGW-R-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS` `DERIVED_LEAN`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION), [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-DECLARED-CHALLENGE-IMPORT-PER-LEVEL` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)
- `PGW-R-ENDOGENOUS-DEMAND-OB1` `GAP_NO_DERIVATION`: [PGW-ENDOGENOUS-DEMAND-OB1](PGW-ENDOGENOUS-DEMAND-OB1.md) (OPEN)
