# PG-GEN-SUPPLY-ERASURE

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Genesis supply erasure: removing supply events from a history leaves the replayed regime unchanged (SupplyErasure.replayE_filter_supply).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
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

The five-field array/copy/source representation, all finite partial histories, both readings and state-dependent token erasure now have local Lean evidence. Runtime/compiler refinement of Python and Rust and the Alpha responder license protocol remain separate.

## Source status

MECHANIZED in SupplyErasure.lean (replayE_filter_supply and replayE_supply_only) with Rust witness

## Review

- PFP review: [dag/results/PG-GEN-SUPPLY-ERASURE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-SUPPLY-ERASURE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Full guarded replay states agree after supply erasure on the retained histories; generic erasure/filterMap and supply-prefix identities are kernel checked.
  - does not support: Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements.
  - next test: Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisReplayRefinement.lean`

- file: [lean4/GenesisReplayRefinement.lean](../../../lean4/GenesisReplayRefinement.lean)
- sha256 (`bytes`): `1fd113d89dc5cb36bf2638cd761c5fb02043d1f4f5476a0f6ffc5b6cc6f24c2c`
- cited in: node.lean, receipt dag/research/campaign_pg-gen-supply-erasure_lean_replay.json (GenesisReplayRefinement)
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-supply-erasure_lean_replay.json](../../../dag/research/campaign_pg-gen-supply-erasure_lean_replay.json) (module `GenesisReplayRefinement`): recorded sha256 `1fd113d89dc5cb36bf2638cd761c5fb02043d1f4f5476a0f6ffc5b6cc6f24c2c` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisReplayRefinement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisReplayRefinement.arrayInsert_toList` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.arrayInsert_toList` |
| `GenesisReplayRefinement.array_failure_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.array_failure_exact` |
| `GenesisReplayRefinement.array_replay_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.array_replay_commutes` |
| `GenesisReplayRefinement.array_replay_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.array_replay_exact` |
| `GenesisReplayRefinement.array_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.array_step_commutes` |
| `GenesisReplayRefinement.array_supply_erasure` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.array_supply_erasure` |
| `GenesisReplayRefinement.array_supply_no_op` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.array_supply_no_op` |
| `GenesisReplayRefinement.copy_replay_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.copy_replay_commutes` |
| `GenesisReplayRefinement.copy_source` | yes | yes | yes | none | `#print axioms GenesisReplayRefinement.copy_source` |
| `GenesisReplayRefinement.copy_source_event` | yes | yes | yes | none | `#print axioms GenesisReplayRefinement.copy_source_event` |
| `GenesisReplayRefinement.copy_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.copy_step_commutes` |
| `GenesisReplayRefinement.decode_encode` | yes | yes | yes | propext | `#print axioms GenesisReplayRefinement.decode_encode` |
| `GenesisReplayRefinement.decode_injective` | yes | yes | yes | propext | `#print axioms GenesisReplayRefinement.decode_injective` |
| `GenesisReplayRefinement.encode_decode` | yes | yes | yes | propext | `#print axioms GenesisReplayRefinement.encode_decode` |
| `GenesisReplayRefinement.invalid_after_supply` | yes | yes | yes | propext | `#print axioms GenesisReplayRefinement.invalid_after_supply` |
| `GenesisReplayRefinement.reading_arrays` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.reading_arrays` |
| `GenesisReplayRefinement.secondRegime_injective` | yes | yes | yes | propext | `#print axioms GenesisReplayRefinement.secondRegime_injective` |
| `GenesisReplayRefinement.second_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.second_step_commutes` |
| `GenesisReplayRefinement.sourceRegime_injective` | yes | yes | yes | none | `#print axioms GenesisReplayRefinement.sourceRegime_injective` |
| `GenesisReplayRefinement.source_change_strict` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.source_change_strict` |
| `GenesisReplayRefinement.source_copy` | yes | yes | yes | none | `#print axioms GenesisReplayRefinement.source_copy` |
| `GenesisReplayRefinement.source_copy_event` | yes | yes | yes | none | `#print axioms GenesisReplayRefinement.source_copy_event` |
| `GenesisReplayRefinement.source_step_nondecreasing` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.source_step_nondecreasing` |
| `GenesisReplayRefinement.source_supply_erasure` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.source_supply_erasure` |
| `GenesisReplayRefinement.source_supply_no_op` | yes | yes | yes | propext | `#print axioms GenesisReplayRefinement.source_supply_no_op` |
| `GenesisReplayRefinement.token_array_replay` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisReplayRefinement.token_array_replay` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Erasure.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Erasure.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Erasure.lean)
- sha256 (`bytes`): `1206da12f2f523d901faf328b459b6831933ce7b911b552ce1d30e46355ba1c4`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Erasure`): recorded sha256 `1206da12f2f523d901faf328b459b6831933ce7b911b552ce1d30e46355ba1c4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Erasure.lean`
- counts toward the grade: yes

### Lean: `lean4/Imported/OeGenPrimitives/SupplyErasure.lean`

- file: [lean4/Imported/OeGenPrimitives/SupplyErasure.lean](../../../lean4/Imported/OeGenPrimitives/SupplyErasure.lean)
- sha256 (`bytes`): `8082e6a7fbb1f10b59c53bec87af703b6957ca0cfb34aef1d9722fd57b3d794d`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.OeGenPrimitives.SupplyErasure`): recorded sha256 `8082e6a7fbb1f10b59c53bec87af703b6957ca0cfb34aef1d9722fd57b3d794d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeGenPrimitives/SupplyErasure.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisPrimitives.SupplyErasure.replayE_filter_supply` | yes | yes | yes | propext | `#print axioms GenesisPrimitives.SupplyErasure.replayE_filter_supply` |
| `GenesisPrimitives.SupplyErasure.replayE_supply_only` | yes | yes | yes | propext | `#print axioms GenesisPrimitives.SupplyErasure.replayE_supply_only` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0386_supply_erasure_on_replay.md`

- file: [dag/derivations/02_genesis/tfq_0386_supply_erasure_on_replay.md](../../../dag/derivations/02_genesis/tfq_0386_supply_erasure_on_replay.md)
- sha256 (`lf-normalised`): `177ddbe518707e496190d09e40cacef558db69494982647b88dbd354fb41d65d`
- generated view: listed, not counted
- cited in: record TFQ-0386
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pg-gen-supply-erasure.md`

- file: [dag/derivations/independent/pg-gen-supply-erasure.md](../../../dag/derivations/independent/pg-gen-supply-erasure.md)
- sha256 (`lf-normalised`): `add9d5680c4e88f25cd10db8bb36c3c02f858cab3e166a4aa6317b6611f878f2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `bb38e1e763dba36d1194fde3c597b73c19f651ec9b4137eeb694fd92fed6f8fb`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:prompts/fable_theorems_2026-10-17/03_genesis_supply_erasure.md`

## Absences recorded by the TFQ records

- TFQ-0386 lean4: declaration obligation: erase_replay against ledger row WDP-P000-013, education filter file left unread
- TFQ-0386 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/genesis/lean4/Derivation/Erasure.lean
- TFQ-0386 python: missing obligation: a replay filter in genesis/code/derivation/engine.py, listed and not opened, that drops supply events and compares regimes
- TFQ-0386 rust: missing obligation: replay.rs must show supply-deletion leaves the core regime unchanged, file listed and not opened
- TFQ-0386 rust: no local rust twin located for atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/replay.rs

## Routes

Incoming (1):

- `PG-R-SUPPLY-ERASURE` `DERIVED_LEAN`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)

Outgoing (0):

