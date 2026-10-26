# PG-GEN-REWRITING-COMMUTATION

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Changes commute with injective rewriting of terms (Step.rename, Reach.rename, fewest_changes_every_writing_A/B for O3), and asserted obstructions persist across multi-step ReachNoRemove sequences (obstruction_persists_reach for O6).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 28
- distinct cited Lean declarations covered by a current replay receipt: 28
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

General source step/history rewriting, exact costs and wire transports for injective natural term writings, and multi-step tracked obstruction persistence now compile via an explicit compatibility proof port. The original Second/Rename remains unchanged and fails its old proof scripts; no finite permutation census is promoted into the general result.

## Source status

O3 and O6 MECHANIZED in Second/Rename.lean and DerivationDagQMClosure.lean (pg_gen_rewriting_commutation_and_obstruction_persistence)

## Review

- PFP review: [dag/results/PG-GEN-REWRITING-COMMUTATION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-REWRITING-COMMUTATION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Full six-permutation merge squares and legality invariance are exact; general injective merge rewriting and map composition are kernel checked.
  - does not support: Prove source Step/ReachNoRemove and cost-potential transports for all term writings and the multi-step obstruction persistence theorem. Do not promote a finite permutation test into that source-wide result.
  - next test: Prove source Step/ReachNoRemove and cost-potential transports for all term writings and the multi-step obstruction persistence theorem. Do not promote a finite permutation test into that source-wide result.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGenesisOngoingRefinement.lean`

- file: [lean4/CampaignGenesisOngoingRefinement.lean](../../../lean4/CampaignGenesisOngoingRefinement.lean)
- sha256 (`bytes`): `ab9d805468e84391bbc0ee142bec028d1ac27b0a5d16e159eda3196b6b50f8ac`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json](../../../dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json) (module `CampaignGenesisOngoingRefinement`): recorded sha256 `ab9d805468e84391bbc0ee142bec028d1ac27b0a5d16e159eda3196b6b50f8ac` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/genesis_merged_20261023_lean_replay.json](../../../dag/research/genesis_merged_20261023_lean_replay.json) (module `CampaignGenesisOngoingRefinement`): recorded sha256 `ab9d805468e84391bbc0ee142bec028d1ac27b0a5d16e159eda3196b6b50f8ac` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGenesisOngoingRefinement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGenesisOngoingRefinement.decode_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisOngoingRefinement.decode_rename` |
| `CampaignGenesisOngoingRefinement.renaming_costs` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisOngoingRefinement.renaming_costs` |
| `CampaignGenesisOngoingRefinement.source_reach_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisOngoingRefinement.source_reach_rename` |
| `CampaignGenesisOngoingRefinement.source_step_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisOngoingRefinement.source_step_rename` |
| `CampaignGenesisOngoingRefinement.tracked_obstruction_persists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisOngoingRefinement.tracked_obstruction_persists` |
| `CampaignGenesisOngoingRefinement.wire_reach_rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisOngoingRefinement.wire_reach_rename` |

- counts toward the grade: yes

### Lean: `lean4/CampaignGenesisOngoingRename.lean`

- file: [lean4/CampaignGenesisOngoingRename.lean](../../../lean4/CampaignGenesisOngoingRename.lean)
- sha256 (`bytes`): `971377d196cba3ab5b36d0dad1ff0f2ba9c951634c944f6607f6c344aeac5cc2`
- cited in: node.lean, receipt dag/research/genesis_merged_20261023_lean_replay.json (CampaignGenesisOngoingRename)
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json](../../../dag/research/campaign_pg-gen-ongoing-fewest-changes_lean_replay.json) (module `CampaignGenesisOngoingRename`): recorded sha256 `971377d196cba3ab5b36d0dad1ff0f2ba9c951634c944f6607f6c344aeac5cc2` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/genesis_merged_20261023_lean_replay.json](../../../dag/research/genesis_merged_20261023_lean_replay.json) (module `CampaignGenesisOngoingRename`): recorded sha256 `971377d196cba3ab5b36d0dad1ff0f2ba9c951634c944f6607f6c344aeac5cc2` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGenesisOngoingRename`

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

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Second/Carry.lean`

- file: [lean4/Imported/GenesisOngoing/Second/Carry.lean](../../../lean4/Imported/GenesisOngoing/Second/Carry.lean)
- sha256 (`bytes`): `6d7c19d48be69a2d3294f8a35763d53e0f77733e1bae5c83eb319df2e50ab65e`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Second.Carry`): recorded sha256 `6d7c19d48be69a2d3294f8a35763d53e0f77733e1bae5c83eb319df2e50ab65e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Second/Carry.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach3.obstruction_persists` | yes | yes | yes | module-level | `#print axioms Reach3.obstruction_persists` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Second/Rename.lean`

- file: [lean4/Imported/GenesisOngoing/Second/Rename.lean](../../../lean4/Imported/GenesisOngoing/Second/Rename.lean)
- sha256 (`bytes`): `557a06c16167db9492980b4c2df8777285c43ffc8272f8f80d5c3437e5e80491`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/genesis_rename_compatibility_lean_replay.json](../../../dag/research/genesis_rename_compatibility_lean_replay.json) (module `Imported.GenesisOngoing.Second.Rename`): recorded sha256 `557a06c16167db9492980b4c2df8777285c43ffc8272f8f80d5c3437e5e80491` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Second.Rename`): recorded sha256 `557a06c16167db9492980b4c2df8777285c43ffc8272f8f80d5c3437e5e80491` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Second/Rename.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach3.rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach3.rename` |
| `Step3.rename` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Step3.rename` |
| `fewest_changes3_every_writing_A` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fewest_changes3_every_writing_A` |
| `fewest_changes3_every_writing_B` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fewest_changes3_every_writing_B` |

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

### Documents and data: `dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md`

- file: [dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md](../../../dag/derivations/02_genesis/tfq_0390_rewriting_and_persistence_reconcile.md)
- sha256 (`lf-normalised`): `5d76448b3433e04b7ff13bea15c487f93dd03ac705cd86c8b3643c5c6671f105`
- generated view: listed, not counted
- cited in: record TFQ-0390
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pg-gen-ongoing-fewest-changes.md`

- file: [dag/derivations/independent/pg-gen-ongoing-fewest-changes.md](../../../dag/derivations/independent/pg-gen-ongoing-fewest-changes.md)
- sha256 (`lf-normalised`): `264aa3c3529be579b7ad1ad06c76d916ca59ad832c0507d4be41d216640bcbcc`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `bb38e1e763dba36d1194fde3c597b73c19f651ec9b4137eeb694fd92fed6f8fb`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0390 lean4: declaration obligation: compare fewest_changes_every_writing_A and obstruction_persists_reach with ledger rows O3 and O6
- TFQ-0390 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Second/Rename.lean
- TFQ-0390 python: missing obligation: a witness table under genesis_ongoing that cites rows O3 and O6 beside the Rename.lean declaration names without a status change
- TFQ-0390 rust: missing obligation: no Rust renaming module was listed for the ongoing package; do not invent one to close O3

## Routes

Incoming (1):

- `PG-R-REWRITING` `DERIVED_LEAN`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)

Outgoing (4):

- `APP-R-AUTH-DTM0-FINITE-RULE-MACHINE` `DERIVED_PROSE`: [AUTH-DTM0-FINITE-RULE-MACHINE](AUTH-DTM0-FINITE-RULE-MACHINE.md) (DEFINITION)
- `APP-R-AUTHF-DTM0-RULE-MACHINE` `DERIVED_PROSE`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)
- `APP-R-COMP-C2-LETTER-RENAME-COMMUTES` `DERIVED_LEAN`: [COMP-C2-LETTER-RENAME-COMMUTES](COMP-C2-LETTER-RENAME-COMMUTES.md) (PROVED_LEAN)
- `APP-R-COMP-C2-STEP3-NOT-WORD-STEP` `GAP_NO_DERIVATION`: [COMP-C2-STEP3-NOT-WORD-STEP](COMP-C2-STEP3-NOT-WORD-STEP.md) (OPEN)
