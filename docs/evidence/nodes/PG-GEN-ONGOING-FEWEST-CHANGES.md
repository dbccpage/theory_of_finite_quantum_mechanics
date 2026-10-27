# PG-GEN-ONGOING-FEWEST-CHANGES

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fewest changes to reach a result is the first derivation's size-plus-twice-destroyed-givens formula, with matching lower and upper bounds (fewest_changes_A/B).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 48
- distinct cited Lean declarations covered by a current replay receipt: 48
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The complete source/wire state, Legal/WF/Step/Reach and cost refinement now covers merged names, arbitrary labels and every identification. Matching lower/upper bounds are transported for some initial writing and all-writing lower bounds. The unchanged original Second/Rename fails Lean 4.35.0; a separately scored compatibility proof port compiles. External runtime/compiler and serialization refinement remain separate.

## Source status

Fewest-changes formula (D8-D10)

## Review

- PFP review: [dag/results/PG-GEN-ONGOING-FEWEST-CHANGES/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-ONGOING-FEWEST-CHANGES/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Complete 68-state shortest-path tables for both apart seeds and exact edit-cost identities are retained; scalar lower-bound algebra is kernel checked.
  - does not support: Extend the refinement to merged-name states, arbitrary labels and all source identification steps and prove the full lower/upper transport. This apart-state search is not the unrestricted fewest_changes_A/B theorem.
  - next test: Extend the refinement to merged-name states, arbitrary labels and all source identification steps and prove the full lower/upper transport. This apart-state search is not the unrestricted fewest_changes_A/B theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisOngoingRefinement.lean`

- file: [lean4/GenesisOngoingRefinement.lean](../../../lean4/GenesisOngoingRefinement.lean)
- sha256 (`bytes`): `8efdfb4d1fc45ff8803ba9e76d2f6d66d4213e4e82de5a0c9a8fdf906829ae76`
- cited in: node.lean, receipt dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json (GenesisOngoingRefinement), receipt dag/research/genesis_merged_20261023_lean_replay.json (GenesisOngoingRefinement)
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json](../../../dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json) (module `GenesisOngoingRefinement`): recorded sha256 `8efdfb4d1fc45ff8803ba9e76d2f6d66d4213e4e82de5a0c9a8fdf906829ae76` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/genesis_merged_20261023_lean_replay.json](../../../dag/research/genesis_merged_20261023_lean_replay.json) (module `GenesisOngoingRefinement`): recorded sha256 `8efdfb4d1fc45ff8803ba9e76d2f6d66d4213e4e82de5a0c9a8fdf906829ae76` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisOngoingRefinement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisOngoingRefinement.assertion_obstruction_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.assertion_obstruction_iff` |
| `GenesisOngoingRefinement.build_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.build_lower_bound` |
| `GenesisOngoingRefinement.build_two_steps` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.build_two_steps` |
| `GenesisOngoingRefinement.costA_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.costA_exact` |
| `GenesisOngoingRefinement.costB_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.costB_exact` |
| `GenesisOngoingRefinement.decode_addAssertion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.decode_addAssertion` |
| `GenesisOngoingRefinement.decode_addTerm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.decode_addTerm` |
| `GenesisOngoingRefinement.decode_encode` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.decode_encode` |
| `GenesisOngoingRefinement.decode_identify` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.decode_identify` |
| `GenesisOngoingRefinement.decode_remove` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.decode_remove` |
| `GenesisOngoingRefinement.decode_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.decode_rename` |
| `GenesisOngoingRefinement.exact_transition_representation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.exact_transition_representation` |
| `GenesisOngoingRefinement.full_fewest_A` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.full_fewest_A` |
| `GenesisOngoingRefinement.full_fewest_B` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.full_fewest_B` |
| `GenesisOngoingRefinement.identify_obstruction_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.identify_obstruction_iff` |
| `GenesisOngoingRefinement.legal_iff_source` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.legal_iff_source` |
| `GenesisOngoingRefinement.legal_wf_preserved` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.legal_wf_preserved` |
| `GenesisOngoingRefinement.one_step_new_assertion_old_endpoints` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.one_step_new_assertion_old_endpoints` |
| `GenesisOngoingRefinement.reach_complete` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.reach_complete` |
| `GenesisOngoingRefinement.reach_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.reach_sound` |
| `GenesisOngoingRefinement.renaming_costs` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.renaming_costs` |
| `GenesisOngoingRefinement.source_reach_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.source_reach_rename` |
| `GenesisOngoingRefinement.source_step_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.source_step_rename` |
| `GenesisOngoingRefinement.step_complete` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.step_complete` |
| `GenesisOngoingRefinement.step_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.step_sound` |
| `GenesisOngoingRefinement.tracked_obstruction_persists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.tracked_obstruction_persists` |
| `GenesisOngoingRefinement.wf_iff_source` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.wf_iff_source` |
| `GenesisOngoingRefinement.wire_build_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.wire_build_lower_bound` |
| `GenesisOngoingRefinement.wire_reach_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisOngoingRefinement.wire_reach_rename` |

- counts toward the grade: yes

### Lean: `lean4/GenesisOngoingRename.lean`

- file: [lean4/GenesisOngoingRename.lean](../../../lean4/GenesisOngoingRename.lean)
- sha256 (`bytes`): `971377d196cba3ab5b36d0dad1ff0f2ba9c951634c944f6607f6c344aeac5cc2`
- cited in: node.lean, receipt dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json (GenesisOngoingRename)
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json](../../../dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json) (module `GenesisOngoingRename`): recorded sha256 `971377d196cba3ab5b36d0dad1ff0f2ba9c951634c944f6607f6c344aeac5cc2` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/genesis_merged_20261023_lean_replay.json](../../../dag/research/genesis_merged_20261023_lean_replay.json) (module `GenesisOngoingRename`): recorded sha256 `971377d196cba3ab5b36d0dad1ff0f2ba9c951634c944f6607f6c344aeac5cc2` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisOngoingRename`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Seed.Second.Reach.rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.Reach.rename` |
| `Seed.Second.Reach3.rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.Reach3.rename` |
| `Seed.Second.ReachNoRemove.obstruction_persists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.ReachNoRemove.obstruction_persists` |
| `Seed.Second.ReachNoRemove.pair_mem` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.ReachNoRemove.pair_mem` |
| `Seed.Second.ReachNoRemove.toReach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.ReachNoRemove.toReach` |
| `Seed.Second.Step.rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.Step.rename` |
| `Seed.Second.Step3.rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.Step3.rename` |
| `Seed.Second.costA_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.costA_rename` |
| `Seed.Second.costB_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.costB_rename` |
| `Seed.Second.fewest_changes3_every_writing_A` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.fewest_changes3_every_writing_A` |
| `Seed.Second.fewest_changes3_every_writing_B` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.fewest_changes3_every_writing_B` |
| `Seed.Second.fewest_changes_every_writing_A` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.fewest_changes_every_writing_A` |
| `Seed.Second.fewest_changes_every_writing_B` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.fewest_changes_every_writing_B` |
| `Seed.Second.obstruction_persists_reach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.obstruction_persists_reach` |
| `Seed.Second.rename_identify` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.rename_identify` |
| `Seed.Second.size_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Seed.Second.size_rename` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Cost.lean`

- file: [lean4/Imported/GenesisOngoing/H3V7N5QF/Cost.lean](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Cost.lean)
- sha256 (`bytes`): `9700381f45df6ad5eabc77142f4a5c77edc93298bded5247f7afc11c33101baa`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.H3V7N5QF.Cost`): recorded sha256 `9700381f45df6ad5eabc77142f4a5c77edc93298bded5247f7afc11c33101baa` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/H3V7N5QF/Cost.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach.names_stay_merged` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach.names_stay_merged` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean`

- file: [lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean)
- sha256 (`bytes`): `fae639f2f5edfbefafb06df750cba34a445d978ed3b9cccddf951aac61a6f32d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.H3V7N5QF.Paths`): recorded sha256 `fae639f2f5edfbefafb06df750cba34a445d978ed3b9cccddf951aac61a6f32d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fewest_changes_A` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fewest_changes_A` |
| `reach_by_edits` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach_by_edits` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md)
- sha256 (`lf-normalised`): `34530ca3f714274f7f03a1cd5dffcdd1fb76e50ec20749a03a72956e5f93fd1c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md`

- file: [dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md](../../../dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md)
- sha256 (`lf-normalised`): `a104cc78b841b7e7c5f927f96ff593a4cd3b2fe5195e5869f7e8d839d5646e70`
- generated view: listed, not counted
- cited in: record TFQ-0389
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pg-gen-ongoing-fewest-changes.md`

- file: [dag/derivations/independent/pg-gen-ongoing-fewest-changes.md](../../../dag/derivations/independent/pg-gen-ongoing-fewest-changes.md)
- sha256 (`lf-normalised`): `7a3c0b747d97291cf969cdae28b57cb9324ba1ae7a99cfcf6eced5a9c9cbd8f8`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0389 lean4: declaration obligation: fewest_changes_A for one legal well-formed writing
- TFQ-0389 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/H3V7N5QF/Paths.lean
- TFQ-0389 python: missing obligation: a cost column under genesis_ongoing/evidence that is checked only inside the declared term bound
- TFQ-0389 rust: missing obligation: no Rust cost module was listed for the ongoing package; the formula still needs an explicit finite checker or a stated absence

## Routes

Incoming (1):

- `PG-R-ONGOING-COST` `DERIVED_LEAN`: [PG-GEN-ONGOING-OBSTRUCTION](PG-GEN-ONGOING-OBSTRUCTION.md) (PROVED_LEAN)

Outgoing (3):

- `PG-R-REWRITING` `DERIVED_LEAN`: [PG-GEN-REWRITING-COMMUTATION](PG-GEN-REWRITING-COMMUTATION.md) (PROVED_LEAN)
- `PG-R-SAMENESS` `COMPUTED`: [PG-GEN-SAMENESS-REFINEMENTS](PG-GEN-SAMENESS-REFINEMENTS.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-GO-REACH-CEILING` `DERIVED_LEAN`: [PGW-GO-REACH-CEILING](PGW-GO-REACH-CEILING.md) (PROVED_LEAN)
