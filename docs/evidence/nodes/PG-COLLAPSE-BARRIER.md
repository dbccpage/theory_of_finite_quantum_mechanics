# PG-COLLAPSE-BARRIER

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If two data have equal profiles (a collapsed observation quotient), no function of the quotient separates them; separation needs an added instance or tag outside the quotient.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/CollapseBarrier.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

Choice and existence of the added tag for the actual inscription strings \<a\>, \<ab\>, \<aa\> of the Pre-Genesis paper under the supplied decoder; the empty-alphabet case (empty X) and Z empty are native conventions, not kernel theorems.

## Source status

Proposition 1 - separation cannot be recovered from a collapsed quotient

## Review

- PFP review: [dag/results/PG-COLLAPSE-BARRIER/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-COLLAPSE-BARRIER/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For maps p : X -\> Y and s : X -\> Z, no function of p reproduces s as soon as one fibre of p contains two points with different s values; with Z inhabited this is the only obstruction, and for finite X a nonempty tag alphabet of size k recovers s through (p, t) exactly when every fibre has at most k distinct s values.
  - does not support: Which tag or instance is added (the node does not select one, and the paper only exhibits predicates under a supplied decoder); the barrier for the inscription strings of the Pre-Genesis paper; infinite or non-function observation structures; universes above Type; any claim that an added tag exists in the physical or inscription regime; the source aggregate pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed, which is a bundle of fixed instances proved by rfl and decide.
  - next test: Confirm by exhaustive enumeration over the inscription strings \<a\>, \<ab\>, \<aa\> of the Pre-Genesis paper under the supplied decoder that the least tag alphabet equals the max-fibre value predicted by tag_alphabet_iff, and that the paper predicates "contains b" and "payload length \> 1" achieve it.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CollapseBarrier.lean`

- file: [lean4/CollapseBarrier.lean](../../../lean4/CollapseBarrier.lean)
- sha256 (`bytes`): `2e19515baccbf10fe7fb8b82c5c58490ba6808cd877924acdef7eb56606e7561`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (CollapseBarrier)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `CollapseBarrier`): recorded sha256 `2e19515baccbf10fe7fb8b82c5c58490ba6808cd877924acdef7eb56606e7561` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CollapseBarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CollapseBarrier.barrier` | yes | yes | yes | none | `#print axioms CollapseBarrier.barrier` |
| `CollapseBarrier.factorsImage_iff` | yes | yes | yes | Classical.choice | `#print axioms CollapseBarrier.factorsImage_iff` |
| `CollapseBarrier.factors_iff_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CollapseBarrier.factors_iff_exact` |
| `CollapseBarrier.factors_iff_fails_without_nonempty` | yes | yes | yes | none | `#print axioms CollapseBarrier.factors_iff_fails_without_nonempty` |
| `CollapseBarrier.factors_iff_of_nonempty` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CollapseBarrier.factors_iff_of_nonempty` |
| `CollapseBarrier.refine_separates` | yes | yes | yes | none | `#print axioms CollapseBarrier.refine_separates` |
| `CollapseBarrier.tag_alphabet_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CollapseBarrier.tag_alphabet_iff` |
| `CollapseBarrier.tag_card_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CollapseBarrier.tag_card_lower_bound` |
| `CollapseBarrier.tag_exists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CollapseBarrier.tag_exists` |
| `CollapseBarrier.tag_separates` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CollapseBarrier.tag_separates` |
| `CollapseBarrier.two_point_no_factor` | yes | yes | yes | none | `#print axioms CollapseBarrier.two_point_no_factor` |
| `CollapseBarrier.two_point_one_bit` | yes | yes | yes | none | `#print axioms CollapseBarrier.two_point_one_bit` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0365_collapsed_observation_barrier.md`

- file: [dag/derivations/01_pregenesis/tfq_0365_collapsed_observation_barrier.md](../../../dag/derivations/01_pregenesis/tfq_0365_collapsed_observation_barrier.md)
- sha256 (`lf-normalised`): `22ff7f2bd53230484f4d90f9f89b79d8f1cf6915b13c8b3f859f3701959f4f4c`
- generated view: listed, not counted
- cited in: record TFQ-0365
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0365 lean4: declaration obligation: collapsed_observation_barrier stays tied to equal profiles and does not invent a separating tag
- TFQ-0365 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0365 python: missing obligation: a counterexample beside preservation.refine where equal reports yield no separating function
- TFQ-0365 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py
- TFQ-0365 rust: missing obligation: a quotient-barrier check in crate pre_mssn_preservation
- TFQ-0365 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs

## Routes

Incoming (1):

- `PG-R-COLLAPSE` `DERIVED_LEAN`: [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)

Outgoing (5):

- `PG-R-FIRST-SEPARATION` `COMPUTED`: [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)
- `PG-R-HISTORY-CRITERION` `DERIVED_LEAN`: [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)
- `PG-R-REFINE` `DERIVED_LEAN`: [PG-REFINE-SEPARATES](PG-REFINE-SEPARATES.md) (PROVED_LEAN)
- `PGW-R-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `DERIVED_LEAN`: [PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE](PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE.md) (PROVED_LEAN)
- `PGW-R-REPLAY-NECESSITY` `DERIVED_LEAN`: [PGW-REPLAY-NECESSITY](PGW-REPLAY-NECESSITY.md) (PROVED_LEAN)
