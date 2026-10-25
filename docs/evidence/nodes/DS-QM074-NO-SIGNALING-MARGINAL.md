# DS-QM074-NO-SIGNALING-MARGINAL

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact contextual marginals distinguish nonsignaling correlated tables from the signaling control; scalar PR-family marginal and nonproduct controls are kernel checked.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- admitted composition rule for subsystems (assumption)
- input independence of remote setting (assumption)

## Bottleneck

Unmet after the PFP review: Prove full admitted-composition/channel-to-table transport and justify physical subsystem/setting independence; no causality law is derived. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[DERIVED\] stub-style rows (QM_074-C1,C2); C3 \[SCOPE FENCE\]

## Review

- PFP review: [dag/results/DS-QM074-NO-SIGNALING-MARGINAL/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM074-NO-SIGNALING-MARGINAL/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact contextual marginals distinguish nonsignaling correlated tables from the signaling control; scalar PR-family marginal and nonproduct controls are kernel checked.
  - does not support: Prove full admitted-composition/channel-to-table transport and justify physical subsystem/setting independence; no causality law is derived.
  - next test: Prove full admitted-composition/channel-to-table transport and justify physical subsystem/setting independence; no causality law is derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0261
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal` |

- counts toward the grade: yes

### Lean: `lean4/Entanglement.lean`

- file: [lean4/Entanglement.lean](../../../lean4/Entanglement.lean)
- sha256 (`bytes`): `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_constructor_theory.json](../../../dag/research/lean_replay_campaign_constructor_theory.json) (module `Entanglement`): recorded sha256 `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Entanglement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `non_signaling_under_local_b_flip` | yes | yes | yes | Quot.sound, propext | `#print axioms non_signaling_under_local_b_flip` |

- counts toward the grade: yes

### Lean: `lean4/NoSignalling.lean`

- file: [lean4/NoSignalling.lean](../../../lean4/NoSignalling.lean)
- sha256 (`bytes`): `8ed77c83d7025f24c76b0e38bd24d7eaa86f5a6569ef414a0321bad6efb182b2`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `NoSignalling`): recorded sha256 `8ed77c83d7025f24c76b0e38bd24d7eaa86f5a6569ef414a0321bad6efb182b2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build NoSignalling`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_signalling_under_admitted_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms no_signalling_under_admitted_composition` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/no_signalling.rs`

- file: [code/rust/src/qm/campaigns/no_signalling.rs](../../../code/rust/src/qm/campaigns/no_signalling.rs)
- sha256 (`bytes`): `5a035ae66c474423a8e76300b37934385a76b60788a8d4c1ca680dda7c82ea4f`
- cited in: record TFQ-0261
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/no_signalling.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/no_signalling.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0261_no_signalling_marginals_under_an_admitted_composition.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0261_no_signalling_marginals_under_an_admitted_composition.md](../../../dag/derivations/12_finite_qm_structure/tfq_0261_no_signalling_marginals_under_an_admitted_composition.md)
- sha256 (`lf-normalised`): `9711db6e414bdb26e12927b2fe00e63c56a498a6641e835efe841e9b23f3cfc3`
- generated view: listed, not counted
- cited in: record TFQ-0261
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0261 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-BELL-TO-NOSIGNALING` `DERIVED_LEAN`: [DS-QM073-FINITE-CHSH-AND-PR-BOX](DS-QM073-FINITE-CHSH-AND-PR-BOX.md) (PROVED_LEAN)

Outgoing (2):

- `FRO-R-CQFT-FINITE-STRICT-POSET-SPACELIKE` `RECORD_PARENT`: [CQFT-FINITE-STRICT-POSET-SPACELIKE](CQFT-FINITE-STRICT-POSET-SPACELIKE.md) (PROVED_LEAN)
- `FRO-R-CQFT-NO-SIGNALLING-PRODUCT-LEAN` `RECORD_PARENT`: [CQFT-NO-SIGNALLING-PRODUCT-LEAN](CQFT-NO-SIGNALLING-PRODUCT-LEAN.md) (PROVED_LEAN)
