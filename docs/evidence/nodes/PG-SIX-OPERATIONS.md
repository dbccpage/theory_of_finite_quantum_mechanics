# PG-SIX-OPERATIONS

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Mention, Supply, Designate, Admit, Retain, Operate are kept as six distinct operations; only Admit changes admitted state. Conflating them (supply with admission, designation with retention) is the source of the Reading L / Reading F split in Genesis.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/SixOperations.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

Definitional separation; the model-level frame and separation theorems are kernel-checked for an author-built machine and are not bridged to the Genesis event model (stepE has a token-less counter admitDatum and a whole-regime supply_no_op).

## Source status

Six operations that must remain distinct (Pre-Genesis §3)

## Review

- PFP review: [dag/results/PG-SIX-OPERATIONS/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-SIX-OPERATIONS/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `DEFINITION`; qualifies for E4: no.
  - narrowest claim: By construction of its six state components, only Admit writes the admitted component of the six-operation state machine, and it changes it iff the item is new; the Reading L / Reading F pair has different admitted states in this machine and the same admitted state in the machine in which Supply also admits (a two-machine comparison for every token).
  - does not support: That these six operations or state fields match any host, the Genesis Python model or the Genesis event semantics (forms, instances, requirements); that the six operations are distinct beyond writing distinct fields of this machine (Retain and Operate are gated on admission by definition); that conflating operations is the source of the Reading L / Reading F split of Genesis (a causal reading; only the model-level two-machine comparison is checked); more than two items or traces longer than 4 natively (the Lean statements are general, the Lean instances are Nat items); the inert-inscription model of PG-INERT-DIAMOND (cross-referenced, not imported); any physical or interpretive reading.
  - next test: Bridge this machine to the Genesis event model: define a simulation from the six operations to Derivation/Basic.lean stepE (supply a no-op, admitDatum an admission) and prove it preserves the admitted regime on the histories of the theorems historyL_replays and historyF_replays of Inertia.lean (external Genesis files, read but not bound and without a pinned sha256).

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` |
| `QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate` |
- counts toward the grade: yes

### Lean: `lean4/SixOperations.lean`

- file: [lean4/SixOperations.lean](../../../lean4/SixOperations.lean)
- sha256 (`bytes`): `a05c568c76bd1e1a4b574171bf80fb2980e661d7f5d1f42d4f9ea826c1a849a1`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (SixOperations)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `SixOperations`): recorded sha256 `a05c568c76bd1e1a4b574171bf80fb2980e661d7f5d1f42d4f9ea826c1a849a1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SixOperations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SixOperations.designate_retains_conflation_separates` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.designate_retains_conflation_separates` |
| `SixOperations.designation_is_overwritten` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.designation_is_overwritten` |
| `SixOperations.readings_collapse_when_supply_admits` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.readings_collapse_when_supply_admits` |
| `SixOperations.readings_separated_six_ops` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.readings_separated_six_ops` |
| `SixOperations.repeated_admit_does_not_grow_set` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.repeated_admit_does_not_grow_set` |
| `SixOperations.run_admitted` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.run_admitted` |
| `SixOperations.run_changes_admitted_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.run_changes_admitted_iff` |
| `SixOperations.run_without_admit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.run_without_admit` |
| `SixOperations.six_results_pairwise_distinct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.six_results_pairwise_distinct` |
| `SixOperations.step_admitted_of_ne_admit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.step_admitted_of_ne_admit` |
| `SixOperations.step_changes_admitted_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.step_changes_admitted_iff` |
| `SixOperations.supply_admits_conflation_separates` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.supply_admits_conflation_separates` |
| `SixOperations.supply_keeps_admitted` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SixOperations.supply_keeps_admitted` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0363_six_distinct_operations.md`

- file: [dag/derivations/01_pregenesis/tfq_0363_six_distinct_operations.md](../../../dag/derivations/01_pregenesis/tfq_0363_six_distinct_operations.md)
- sha256 (`lf-normalised`): `35b22999b32cd5540237f96b544b91d0e3a266731345bce1eb377290670b2a89`
- generated view: listed, not counted
- cited in: record TFQ-0363
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0363 lean4: missing declaration obligation: six operation names beside supply_no_op in Derivation/Inertia.lean
- TFQ-0363 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean
- TFQ-0363 python: missing obligation: six operation constructors in 000_genesis_19l57g1/code/derivation/model.py, listed but not opened, kept distinct from one another
- TFQ-0363 rust: missing obligation: six named operations in omega_ooutwire_primitives rather than one event enum that merges them
- TFQ-0363 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs
- TFQ-0363 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/supply.rs

## Routes

Incoming (0):


Outgoing (4):

- `PG-R-MSS0-TO-REGIME` `DERIVED_LEAN`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)
- `PG-R-SIX-OPS-TO-SUPPLY` `DERIVED_LEAN`: [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)
- `PGW-R-ADMISSION-BEFORE-DISTINCTION` `DERIVED_PROSE`: [PGW-ADMISSION-BEFORE-DISTINCTION](PGW-ADMISSION-BEFORE-DISTINCTION.md) (DEFINITION)
- `UDG-R-TFQ-0364` `RECORD_PARENT`: [TFQ-0364](TFQ-0364.md) (SOURCE_RECORD)

No incoming route.
