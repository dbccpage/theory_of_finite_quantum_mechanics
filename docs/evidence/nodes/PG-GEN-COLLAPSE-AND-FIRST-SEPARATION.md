# PG-GEN-COLLAPSE-AND-FIRST-SEPARATION

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: All 111 declared candidate sequences are replayed; no cost\<2 response separates, six cost-two responses tie, and the two unary responses minimize the secondary arity sum.

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

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Declared candidate space of one-step augmentations (assumption)

## Bottleneck

Unmet after the PFP review: Transport this bounded alphabet to arbitrary source Item arguments/arities and the full validResponse requirements; do not claim a global or physical minimum from a finite declared candidate set. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Section 7 - cost-two first separation; U0/U1/BL/BD separable

## Review

- PFP review: [dag/results/PG-GEN-COLLAPSE-AND-FIRST-SEPARATION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-COLLAPSE-AND-FIRST-SEPARATION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All 111 declared candidate sequences are replayed; no cost\<2 response separates, six cost-two responses tie, and the two unary responses minimize the secondary arity sum.
  - does not support: Transport this bounded alphabet to arbitrary source Item arguments/arities and the full validResponse requirements; do not claim a global or physical minimum from a finite declared candidate set.
  - next test: Transport this bounded alphabet to arbitrary source Item arguments/arities and the full validResponse requirements; do not claim a global or physical minimum from a finite declared candidate set.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- sha256 (`bytes`): `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Minimality`): recorded sha256 `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U0_separable` | yes | yes | yes | Quot.sound, propext | `#print axioms U0_separable` |
| `deltaU0_valid` | yes | yes | yes | Quot.sound, propext | `#print axioms deltaU0_valid` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0381_cost_two_first_separation.md`

- file: [dag/derivations/02_genesis/tfq_0381_cost_two_first_separation.md](../../../dag/derivations/02_genesis/tfq_0381_cost_two_first_separation.md)
- sha256 (`lf-normalised`): `bb0b5162a99dd7ae687b47ecf310d8fe756f0413113d35038bf00e566435fad1`
- generated view: listed, not counted
- cited in: record TFQ-0381
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0382_refined_minimum_class.md`

- file: [dag/derivations/02_genesis/tfq_0382_refined_minimum_class.md](../../../dag/derivations/02_genesis/tfq_0382_refined_minimum_class.md)
- sha256 (`lf-normalised`): `5a6a51d1235e423b3739a481d864aaa4b0b3599aca456f512efd0272c0520d51`
- generated view: listed, not counted
- cited in: record TFQ-0382
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0381 lean4: declaration obligation: deltaU0_valid inside the declared response grammar
- TFQ-0381 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean
- TFQ-0381 python: missing obligation: a cost counter in 000_genesis_19l57g1/code/derivation/candidates.py, listed and not opened, scoped to the declared response grammar
- TFQ-0381 rust: missing obligation: minima.rs must record item cost two without dropping ties
- TFQ-0381 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs
- TFQ-0382 lean4: missing declaration obligation: refined class (2, 1) versus the unbounded reading-L family, file listed and not opened
- TFQ-0382 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/MinimalityF.lean
- TFQ-0382 python: missing obligation: a refined-cost key (2, 1) in 000_genesis_19l57g1/code/derivation/candidates.py that does not hide the unbounded reading-L family
- TFQ-0382 rust: missing obligation: separate counters for item-cost minima and the refined class
- TFQ-0382 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs

## Routes

Incoming (1):

- `PG-R-FIRST-SEPARATION` `COMPUTED`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN)

Outgoing (7):

- `APP-R-COMP-C1-FIRST-SEPARATION-REPLAY` `COMPUTED`: [COMP-C1-FIRST-SEPARATION-REPLAY](COMP-C1-FIRST-SEPARATION-REPLAY.md) (COMPUTATIONALLY_CHECKED)
- `FRO-R-CT-DEUTSCH-2013-SOURCE` `RECORD_PARENT`: [CT-DEUTSCH-2013-SOURCE](CT-DEUTSCH-2013-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CT-GENESIS-SEPARATION-TASK-ANALOGY` `GAP_NO_DERIVATION`: [CT-GENESIS-SEPARATION-TASK-ANALOGY](CT-GENESIS-SEPARATION-TASK-ANALOGY.md) (OPEN)
- `PG-R-NO-RETURN` `DERIVED_LEAN`: [PG-GEN-NO-RETURN](PG-GEN-NO-RETURN.md) (PROVED_LEAN)
- `PGW-R-CHALLENGE-SOURCE-POLICIES` `DERIVED_PROSE`: [PGW-CHALLENGE-SOURCE-POLICIES](PGW-CHALLENGE-SOURCE-POLICIES.md) (DEFINITION)
- `PGW-R-MU1-MINIMUM-NOT-UNIQUE-L` `DERIVED_LEAN`: [PGW-MU1-MINIMUM-NOT-UNIQUE-L](PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) (PROVED_LEAN)
- `UDG-R-TFQ-0383` `RECORD_PARENT`: [TFQ-0383](TFQ-0383.md) (SOURCE_RECORD)
