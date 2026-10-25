# PG-GEN-SUPPLY-NO-OP

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Supplying an item does not change the regime (supply is a no-op); only an admission event does. Reading L: \<\> supplied but not admitted; Reading F: \<\> admitted as datum 0. Both readings are kept.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declaration references covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The five-field array/copy/source representation, all finite partial histories, both readings and state-dependent token erasure now have local Lean evidence. Runtime/compiler refinement of Python and Rust and the Alpha responder license protocol remain separate.

## Source status

supply_no_op (Genesis inertia); Reading L vs Reading F

## Review

- PFP review: [dag/results/PG-GEN-SUPPLY-NO-OP/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-SUPPLY-NO-OP/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact supply-only and supply-plus-admission regimes are distinct; no-op supply and nontrivial admission are kernel checked on the generic event model.
  - does not support: Prove the exact source Regime representation bridge and retain both Reading L and Reading F. An external presentation cannot license an unrecorded admission.
  - next test: Prove the exact source Regime representation bridge and retain both Reading L and Reading F. An external presentation cannot license an unrecorded admission.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGenesisReplayRefinement.lean`

- file: [lean4/CampaignGenesisReplayRefinement.lean](../../../lean4/CampaignGenesisReplayRefinement.lean)
- sha256 (`bytes`): `d32660cc6a9710571cf7bb9a85403ed58889ae2a6a89c6e4a61689b519e3fa8e`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-supply-erasure_lean_replay.json](../../../dag/research/campaign_pg-gen-supply-erasure_lean_replay.json) (module `CampaignGenesisReplayRefinement`): recorded sha256 `d32660cc6a9710571cf7bb9a85403ed58889ae2a6a89c6e4a61689b519e3fa8e` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGenesisReplayRefinement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGenesisReplayRefinement.array_supply_no_op` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGenesisReplayRefinement.array_supply_no_op` |
| `CampaignGenesisReplayRefinement.copy_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGenesisReplayRefinement.copy_step_commutes` |
| `CampaignGenesisReplayRefinement.reading_arrays` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGenesisReplayRefinement.reading_arrays` |
| `CampaignGenesisReplayRefinement.source_supply_no_op` | yes | yes | yes | propext | `#print axioms CampaignGenesisReplayRefinement.source_supply_no_op` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- sha256 (`bytes`): `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Inertia`): recorded sha256 `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_of_no_insts` | yes | yes | yes | propext | `#print axioms collapsed_of_no_insts` |
| `supply_no_op` | yes | yes | yes | propext | `#print axioms supply_no_op` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0379_supply_does_not_admit.md`

- file: [dag/derivations/02_genesis/tfq_0379_supply_does_not_admit.md](../../../dag/derivations/02_genesis/tfq_0379_supply_does_not_admit.md)
- sha256 (`lf-normalised`): `9a6eb883fea650a6987a0b89ef7d4e447e392da606dd06fb04ba720b9920d462`
- generated view: listed, not counted
- cited in: record TFQ-0379
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0380_readings_left_unselected.md`

- file: [dag/derivations/02_genesis/tfq_0380_readings_left_unselected.md](../../../dag/derivations/02_genesis/tfq_0380_readings_left_unselected.md)
- sha256 (`lf-normalised`): `64d254d176c715a7c5025ff767d2edb6ac08f8103a88bb8bfc35c0153723adde`
- generated view: listed, not counted
- cited in: record TFQ-0380
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pg-gen-supply-erasure.md`

- file: [dag/derivations/independent/pg-gen-supply-erasure.md](../../../dag/derivations/independent/pg-gen-supply-erasure.md)
- sha256 (`lf-normalised`): `125f661fc6acf060ee4939ef9ac1c759a7d4ddd0f71920dcc3e8bf0a173b741f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0379 lean4: declaration obligation: supply_no_op on Regime and a supply event, readings left unselected
- TFQ-0379 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean
- TFQ-0379 python: missing obligation: a supply step in 000_genesis_19l57g1/code/derivation/model.py that returns the same regime and does not set a reading flag
- TFQ-0379 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/reading.rs
- TFQ-0379 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/supply.rs
- TFQ-0380 lean4: missing declaration obligation: both readings remain parameters of the first-separation statements
- TFQ-0380 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean
- TFQ-0380 python: missing obligation: 000_genesis_19l57g1/code/derivation/model.py must be able to store both readings without a default choice
- TFQ-0380 rust: missing obligation: reading.rs was listed and not opened; it must not collapse L and F if both are represented
- TFQ-0380 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/reading.rs

## Routes

Incoming (1):

- `PG-R-SIX-OPS-TO-SUPPLY` `DERIVED_LEAN`: [PG-SIX-OPERATIONS](PG-SIX-OPERATIONS.md) (DEFINITION), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (5):

- `APP-R-COMP-C4-STEPE-UNCAPPED` `DERIVED_LEAN`: [COMP-C4-STEPE-UNCAPPED](COMP-C4-STEPE-UNCAPPED.md) (PROVED_LEAN)
- `PG-R-COLLAPSE` `DERIVED_LEAN`: [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN)
- `PG-R-SUPPLY-ERASURE` `DERIVED_LEAN`: [PG-GEN-SUPPLY-ERASURE](PG-GEN-SUPPLY-ERASURE.md) (PROVED_LEAN)
- `PGW-R-CHALLENGE0-INERTIA-SECOND-TOKEN` `DERIVED_LEAN`: [PGW-CHALLENGE0-INERTIA-SECOND-TOKEN](PGW-CHALLENGE0-INERTIA-SECOND-TOKEN.md) (PROVED_LEAN)
- `PGW-R-CHALLENGE2-ADMITTED-BUT-COLLAPSED` `DERIVED_LEAN`: [PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED](PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED.md) (PROVED_LEAN)
