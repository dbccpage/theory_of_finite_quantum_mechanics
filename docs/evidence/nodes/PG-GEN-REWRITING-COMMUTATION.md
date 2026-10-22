# PG-GEN-REWRITING-COMMUTATION

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Changes commute with injective rewriting of terms (Step.rename, Reach.rename, fewest_changes_every_writing_A/B for O3), and asserted obstructions persist across multi-step ReachNoRemove sequences (obstruction_persists_reach for O6).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Not covered by the PFP review: Prove source Step/ReachNoRemove and cost-potential transports for all term writings and the multi-step obstruction persistence theorem. Do not promote a finite permutation test into that source-wide result.

## Source status

O3 and O6 MECHANIZED in Second/Rename.lean and DerivationDagQMClosure.lean (pg_gen_rewriting_commutation_and_obstruction_persistence)

## Review

- PFP review: [dag/results/PG-GEN-REWRITING-COMMUTATION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-REWRITING-COMMUTATION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Full six-permutation merge squares and legality invariance are exact; general injective merge rewriting and map composition are kernel checked.
  - does not support: Prove source Step/ReachNoRemove and cost-potential transports for all term writings and the multi-step obstruction persistence theorem. Do not promote a finite permutation test into that source-wide result.
  - next test: Prove source Step/ReachNoRemove and cost-potential transports for all term writings and the multi-step obstruction persistence theorem. Do not promote a finite permutation test into that source-wide result.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, node.source
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md`

- file: [dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md](../../../dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md)
- sha256 (`lf-normalised`): `5d76448b3433e04b7ff13bea15c487f93dd03ac705cd86c8b3643c5c6671f105`
- generated view: listed, not counted
- cited in: record TFQ-0390
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0390 lean4: declaration obligation: compare fewest_changes_every_writing_A and obstruction_persists_reach with ledger rows O3 and O6
- TFQ-0390 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean
- TFQ-0390 python: missing obligation: a witness table under 001_genesis_ongoing_h3v7n5qf that cites rows O3 and O6 beside the Rename.lean declaration names without a status change
- TFQ-0390 rust: missing obligation: no Rust renaming module was listed for the ongoing package; do not invent one to close O3

## Routes

Incoming (1):

- `PG-R-REWRITING` `DERIVED_LEAN`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)

Outgoing (4):

- `APP-R-AUTH-DTM0-FINITE-RULE-MACHINE` `DERIVED_PROSE`: [AUTH-DTM0-FINITE-RULE-MACHINE](AUTH-DTM0-FINITE-RULE-MACHINE.md) (DEFINITION)
- `APP-R-AUTHF-DTM0-RULE-MACHINE` `DERIVED_PROSE`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)
- `APP-R-COMP-C2-LETTER-RENAME-COMMUTES` `DERIVED_LEAN`: [COMP-C2-LETTER-RENAME-COMMUTES](COMP-C2-LETTER-RENAME-COMMUTES.md) (PROVED_LEAN)
- `APP-R-COMP-C2-STEP3-NOT-WORD-STEP` `GAP_NO_DERIVATION`: [COMP-C2-STEP3-NOT-WORD-STEP](COMP-C2-STEP3-NOT-WORD-STEP.md) (OPEN)
