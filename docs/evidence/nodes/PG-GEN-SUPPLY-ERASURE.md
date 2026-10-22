# PG-GEN-SUPPLY-ERASURE

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Genesis supply erasure: removing supply events from a history leaves the replayed regime unchanged (SupplyErasure.replayE_filter_supply).

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

Not covered by the PFP review: Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements.

## Source status

MECHANIZED in SupplyErasure.lean (replayE_filter_supply and replayE_supply_only) with Rust witness

## Review

- PFP review: [dag/results/PG-GEN-SUPPLY-ERASURE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-SUPPLY-ERASURE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Full guarded replay states agree after supply erasure on the retained histories; generic erasure/filterMap and supply-prefix identities are kernel checked.
  - does not support: Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements.
  - next test: Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Erasure.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Erasure.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Lean: `omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean`

- file: `omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

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

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:prompts/fable_theorems_2026-10-17/03_genesis_supply_erasure.md`

## Absences recorded by the TFQ records

- TFQ-0386 lean4: declaration obligation: erase_replay against ledger row WDP-P000-013, education filter file left unread
- TFQ-0386 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Erasure.lean
- TFQ-0386 python: missing obligation: a replay filter in 000_genesis_19l57g1/code/derivation/engine.py, listed and not opened, that drops supply events and compares regimes
- TFQ-0386 rust: missing obligation: replay.rs must show supply-deletion leaves the core regime unchanged, file listed and not opened
- TFQ-0386 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs

## Routes

Incoming (1):

- `PG-R-SUPPLY-ERASURE` `DERIVED_LEAN`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)

Outgoing (0):

