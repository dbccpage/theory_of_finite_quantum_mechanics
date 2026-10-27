# PG-GEN-NO-RETURN

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Along the admitted closure rounds the element count is cumulative and a regime once left is not returned to; cycle regimes are constant (cycle_regime_const).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- distinct cited Lean declarations covered by a current replay receipt: 24
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The complete five-field array and Boolean-mode source interpreter refinement, all finite partial histories, and strict source potential increase on actual regime changes now have local Lean proofs. External Python/Rust runtime/compiler and responder/license refinement remain separate.

## Source status

Rounds / no-return / cumulative element count (Genesis §8-§9)

## Review

- PFP review: [dag/results/PG-GEN-NO-RETURN/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-NO-RETURN/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual guarded regime traces, duplicate/no-op controls and two-switch mode cycles are retained; conditional count no-return/cycle lemmas are kernel checked.
  - does not support: Prove the complete array-to-source Regime interpreter refinement and that every real source regime change strictly raises the source potential. A count comparison alone is not that refinement.
  - next test: Prove the complete array-to-source Regime interpreter refinement and that every real source regime change strictly raises the source potential. A count comparison alone is not that refinement.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisNoReturn.lean`

- file: [lean4/GenesisNoReturn.lean](../../../lean4/GenesisNoReturn.lean)
- sha256 (`bytes`): `81b3ae2cc8bc285ce3ff5f1342edbb4a983f4af56d68c3758f4cdd4dd32c3a7b`
- cited in: node.lean, receipt dag/research/campaign_pg-gen-no-return_lean_replay.json (GenesisNoReturn)
- replay: `verified`
  - receipt [dag/research/campaign_pg-gen-no-return_lean_replay.json](../../../dag/research/campaign_pg-gen-no-return_lean_replay.json) (module `GenesisNoReturn`): recorded sha256 `81b3ae2cc8bc285ce3ff5f1342edbb4a983f4af56d68c3758f4cdd4dd32c3a7b` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisNoReturn`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisNoReturn.arrayEvent_sourceEvent` | yes | yes | yes | none | `#print axioms GenesisNoReturn.arrayEvent_sourceEvent` |
| `GenesisNoReturn.array_failure_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.array_failure_exact` |
| `GenesisNoReturn.array_replay_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.array_replay_exact` |
| `GenesisNoReturn.array_source` | yes | yes | yes | propext | `#print axioms GenesisNoReturn.array_source` |
| `GenesisNoReturn.array_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.array_step_commutes` |
| `GenesisNoReturn.cumulative_potential` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.cumulative_potential` |
| `GenesisNoReturn.cycle_regime_const` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.cycle_regime_const` |
| `GenesisNoReturn.decode_encode` | yes | yes | yes | propext | `#print axioms GenesisNoReturn.decode_encode` |
| `GenesisNoReturn.encode_decode` | yes | yes | yes | propext | `#print axioms GenesisNoReturn.encode_decode` |
| `GenesisNoReturn.engine_replay_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.engine_replay_commutes` |
| `GenesisNoReturn.engine_replay_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.engine_replay_exact` |
| `GenesisNoReturn.engine_replay_failure_exact` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.engine_replay_failure_exact` |
| `GenesisNoReturn.engine_replay_source` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.engine_replay_source` |
| `GenesisNoReturn.engine_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.engine_step_commutes` |
| `GenesisNoReturn.no_return` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.no_return` |
| `GenesisNoReturn.second_step_commutes` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.second_step_commutes` |
| `GenesisNoReturn.sourceEvent_arrayEvent` | yes | yes | yes | none | `#print axioms GenesisNoReturn.sourceEvent_arrayEvent` |
| `GenesisNoReturn.sourceState_injective` | yes | yes | yes | propext | `#print axioms GenesisNoReturn.sourceState_injective` |
| `GenesisNoReturn.source_array` | yes | yes | yes | propext | `#print axioms GenesisNoReturn.source_array` |
| `GenesisNoReturn.strict_potential` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.strict_potential` |
| `GenesisNoReturn.two_switches_return` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisNoReturn.two_switches_return` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/SecondRun/Run.lean`

- file: [lean4/Imported/GenesisDerivation/SecondRun/Run.lean](../../../lean4/Imported/GenesisDerivation/SecondRun/Run.lean)
- sha256 (`bytes`): `74bbd43c3bc787180bf03028156f587570e5268ca8998fd72d312214cd72f6bd`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.SecondRun.Run`): recorded sha256 `74bbd43c3bc787180bf03028156f587570e5268ca8998fd72d312214cd72f6bd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/SecondRun/Run.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cycle_regime_const` | yes | yes | yes | Quot.sound, propext | `#print axioms cycle_regime_const` |
| `ereplay_elems_lt_of_ne` | yes | yes | yes | Quot.sound, propext | `#print axioms ereplay_elems_lt_of_ne` |
| `no_return` | yes | yes | yes | Quot.sound, propext | `#print axioms no_return` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0384_cumulative_count_no_return.md`

- file: [dag/derivations/02_genesis/tfq_0384_cumulative_count_no_return.md](../../../dag/derivations/02_genesis/tfq_0384_cumulative_count_no_return.md)
- sha256 (`lf-normalised`): `87319e2ba3f4033aa40fa531d480ba409fc5ea34c38738a555025c94963259d3`
- generated view: listed, not counted
- cited in: record TFQ-0384
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pg-gen-no-return.md`

- file: [dag/derivations/independent/pg-gen-no-return.md](../../../dag/derivations/independent/pg-gen-no-return.md)
- sha256 (`lf-normalised`): `05df9c79673528ca235e6777b70ff7f571a3be2e52d02f281ef5b04592593f60`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0384 lean4: declaration obligation: no_return and cycle_regime_const on EEvent histories
- TFQ-0384 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/genesis/lean4/SecondRun/Run.lean
- TFQ-0384 python: missing obligation: an element-count trace in genesis/code/derivation/engine.py that can show a constant cycle regime
- TFQ-0384 rust: missing obligation: replay history must record non-decrease of element count on the defined events
- TFQ-0384 rust: no local rust twin located for atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/replay.rs

## Routes

Incoming (1):

- `PG-R-NO-RETURN` `DERIVED_LEAN`: [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (4):

- `PG-R-DEMAND` `DERIVED_LEAN`: [PG-DEMAND-ACCOUNTING](PG-DEMAND-ACCOUNTING.md) (PROVED_LEAN)
- `PG-R-HISTORY-CRITERION` `DERIVED_LEAN`: [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)
- `PGW-R-C2-RUN-FORWARD-EVERY-HISTORY` `DERIVED_LEAN`: [PGW-C2-RUN-FORWARD-EVERY-HISTORY](PGW-C2-RUN-FORWARD-EVERY-HISTORY.md) (PROVED_LEAN)
- `UDG-R-TFQ-0385` `GAP_NO_DERIVATION`: [TFQ-0385](TFQ-0385.md) (OPEN)
