# PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Without the external continuation policy the closed system saturates: under the declared round shape a closed run from an empty requirement store makes at most n(n-1)/2 rounds (Lean closedRun_round_bound_from_empty, 2 * rounds ≤ n * (n - 1)), and at the fixpoint any further requirement needs a fresh datum (external supply) or a new requirement kind (external goal) (genesis_source §9 item 6). With external supply the runs grow in width, not in kind: the sealed mu2 trees record 53 (reading L) and 83 (reading F) innovation edges (fresh form plus instance), which the education audit reads as unary forms with 0 binary (finite computation to the requested depth of 15 transition steps). In the reflective composite reflState n demand never dries: for n ≥ 3 the distinct data 1 and 2 have equal depth-one profiles (Lean Generator.generation_never_dries). Within the declared local finite-alphabet class (one radius d, one colour bound k independent of chain length) every strategy fires and none clears (Lean G1Class.g1_class_exclusion), while the clearing members perPairFreshMark (recurring import) and valued (one-time identity-grade rule) lie outside the finite declaration. The education audit names the pattern 'endogenous demands, exogenous payments'.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 4 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 4 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

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

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Generator.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Generator.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md`

- file: [dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md](../../../dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md)
- sha256 (`lf-normalised`): `f37b447dcb7db09b457f19ef4c715fe15cad95a4af7d8e828f90aa4741b4f052`
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/local_strategy.py::classification`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::closure_round_bound`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean::clears_does_not_imply_not_fires`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean::g1_class_exclusion`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Generator.lean::generation_never_dries`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean::closedRun_round_bound_from_empty`

## Routes

Incoming (1):

- `PGW-R-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS` `DERIVED_LEAN`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION), [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-DECLARED-CHALLENGE-IMPORT-PER-LEVEL` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)
- `PGW-R-ENDOGENOUS-DEMAND-OB1` `GAP_NO_DERIVATION`: [PGW-ENDOGENOUS-DEMAND-OB1](PGW-ENDOGENOUS-DEMAND-OB1.md) (OPEN)
