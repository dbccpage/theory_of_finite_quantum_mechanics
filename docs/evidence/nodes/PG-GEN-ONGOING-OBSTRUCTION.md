# PG-GEN-ONGOING-OBSTRUCTION

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> An attempted change is obstructed exactly when it adds some xrx or identifies two related terms; the three answers are refuse, remove the obstruction, build structure.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not covered by the PFP review: Formalize the full Legal/WF/Reach refinement and the build-structure answer with its minimality theorem. The illegal intermediate image is diagnostic, not an authorized performed change.

## Source status

Obstruction: adding xrx, or identifying related terms, is obstructed (Genesis Ongoing)

## Review

- PFP review: [dag/results/PG-GEN-ONGOING-OBSTRUCTION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-ONGOING-OBSTRUCTION/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: All stated finite merge/addition/refusal controls and the remove-first/remove-last image equality are exact, with literal loop/Boolean kernel statements.
  - does not support: Formalize the full Legal/WF/Reach refinement and the build-structure answer with its minimality theorem. The illegal intermediate image is diagnostic, not an authorized performed change.
  - next test: Formalize the full Legal/WF/Reach refinement and the build-structure answer with its minimality theorem. The illegal intermediate image is diagnostic, not an authorized performed change.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Answers.lean`

- file: [lean4/Imported/GenesisOngoing/H3V7N5QF/Answers.lean](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Answers.lean)
- sha256 (`bytes`): `2251e4188422c85595f3d9008098ea59306fcb583e81de00080a8b36650e0b3b`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.H3V7N5QF.Answers`): recorded sha256 `2251e4188422c85595f3d9008098ea59306fcb583e81de00080a8b36650e0b3b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/H3V7N5QF/Answers.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `remove_obstruction_first_or_last` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms remove_obstruction_first_or_last` |
- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Finite.lean`

- file: [lean4/Imported/GenesisOngoing/H3V7N5QF/Finite.lean](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Finite.lean)
- sha256 (`bytes`): `4549d09889693c3cf5f962d29057f4fad3028e55bd48a12dbded4feef446aa1d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.H3V7N5QF.Finite`): recorded sha256 `4549d09889693c3cf5f962d29057f4fad3028e55bd48a12dbded4feef446aa1d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/H3V7N5QF/Finite.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `adding_xrx_always_obstructed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms adding_xrx_always_obstructed` |
| `identify_legal_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms identify_legal_iff` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0388_ongoing_obstruction_answers.md`

- file: [dag/derivations/02_genesis/tfq_0388_ongoing_obstruction_answers.md](../../../dag/derivations/02_genesis/tfq_0388_ongoing_obstruction_answers.md)
- sha256 (`lf-normalised`): `124d3f24d08a42e85ff8033bcc7250f54161b138117e3845d4debe86ffe66b15`
- generated view: listed, not counted
- cited in: record TFQ-0388
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0388 lean4: declaration obligation: identify_legal_iff and adding_xrx_always_obstructed
- TFQ-0388 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Answers.lean
- TFQ-0388 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Finite.lean
- TFQ-0388 python: missing obligation: an answer triple refuse, remove, build under 001_genesis_ongoing_h3v7n5qf/code, not a Phi1 residual
- TFQ-0388 rust: missing obligation: the ongoing package listing showed no Rust crate; a later crate must not reuse this obstruction as an L1 weight

## Routes

Incoming (1):

- `PG-R-ONGOING-OBSTRUCTION` `DERIVED_LEAN`: [PG-GEN-IRREFLEXIVE-DISTINCT](PG-GEN-IRREFLEXIVE-DISTINCT.md) (PROVED_LEAN)

Outgoing (2):

- `FRO-R-CT-REFUSAL-OBSTRUCTION-ANALOGY` `GAP_NO_DERIVATION`: [CT-REFUSAL-OBSTRUCTION-ANALOGY](CT-REFUSAL-OBSTRUCTION-ANALOGY.md) (OPEN)
- `PG-R-ONGOING-COST` `DERIVED_LEAN`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)
