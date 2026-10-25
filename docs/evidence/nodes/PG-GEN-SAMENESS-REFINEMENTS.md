# PG-GEN-SAMENESS-REFINEMENTS

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual excess/plain/together arrays, cancellation cost and bounded two-term rewriting orbits are exact; pointwise excess/cost identities are kernel checked.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Formalize the generated-sameness equivalence with rewriting, then address raising (23), filled terms (24) and filled triples/balance (25). Their ledgers are inspected source material, not newly verified results. The broader source statement is kept in pfp_review.prior_statement.

## Source status

MECHANIZED in Sixteenth..Twentyfirst Lean modules with Rust sameness/compatibility witness

## Review

- PFP review: [dag/results/PG-GEN-SAMENESS-REFINEMENTS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-SAMENESS-REFINEMENTS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual excess/plain/together arrays, cancellation cost and bounded two-term rewriting orbits are exact; pointwise excess/cost identities are kernel checked.
  - does not support: Formalize the generated-sameness equivalence with rewriting, then address raising (23), filled terms (24) and filled triples/balance (25). Their ledgers are inspected source material, not newly verified results.
  - next test: Formalize the generated-sameness equivalence with rewriting, then address raising (23), filled terms (24) and filled triples/balance (25). Their ledgers are inspected source material, not newly verified results.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Sixteenth/State.lean`

- file: [lean4/Imported/GenesisOngoing/Sixteenth/State.lean](../../../lean4/Imported/GenesisOngoing/Sixteenth/State.lean)
- sha256 (`bytes`): `9145a76e1704bd1b8b47b858be313d8c85722ad1fe2cb15c9d8d1cc191b175dd`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Sixteenth.State`): recorded sha256 `9145a76e1704bd1b8b47b858be313d8c85722ad1fe2cb15c9d8d1cc191b175dd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Sixteenth/State.lean`
- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Twentieth/Order.lean`

- file: [lean4/Imported/GenesisOngoing/Twentieth/Order.lean](../../../lean4/Imported/GenesisOngoing/Twentieth/Order.lean)
- sha256 (`bytes`): `3d2ba2dbac504fce151498a4ccec4314f70634d052fb36fcba20d7ca61974449`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Twentieth.Order`): recorded sha256 `3d2ba2dbac504fce151498a4ccec4314f70634d052fb36fcba20d7ca61974449` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Twentieth/Order.lean`
- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Twentyfirst/Refusal.lean`

- file: [lean4/Imported/GenesisOngoing/Twentyfirst/Refusal.lean](../../../lean4/Imported/GenesisOngoing/Twentyfirst/Refusal.lean)
- sha256 (`bytes`): `3dda5f94755bd75aeda3748fae0aff489903fd5b23ae582eeb695e5cf52b68b4`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Twentyfirst.Refusal`): recorded sha256 `3dda5f94755bd75aeda3748fae0aff489903fd5b23ae582eeb695e5cf52b68b4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Twentyfirst/Refusal.lean`
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0391_sameness_refinement_ledgers.md`

- file: [dag/derivations/02_genesis/tfq_0391_sameness_refinement_ledgers.md](../../../dag/derivations/02_genesis/tfq_0391_sameness_refinement_ledgers.md)
- sha256 (`lf-normalised`): `1fe2c76b4578903f211d18e85aa65bbab038be30d0d645ed90f438e30295fde5`
- generated view: listed, not counted
- cited in: record TFQ-0391
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/CLAUDE.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/CLAUDE.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0391 lean4: missing declaration obligation: row ids in the four later claim ledgers were not read
- TFQ-0391 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/State.lean
- TFQ-0391 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Twentieth/Order.lean
- TFQ-0391 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Twentyfirst/Refusal.lean
- TFQ-0391 python: missing obligation: do not import a sameness refinement into 001_genesis_ongoing_h3v7n5qf/code until the four unread claim ledgers are inventoried
- TFQ-0391 rust: missing obligation: no Rust sameness crate was listed; do not add one from the unread ledgers

## Routes

Incoming (1):

- `PG-R-SAMENESS` `COMPUTED`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)

Outgoing (0):

