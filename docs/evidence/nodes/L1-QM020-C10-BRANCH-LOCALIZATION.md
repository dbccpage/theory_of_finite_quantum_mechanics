# L1-QM020-C10-BRANCH-LOCALIZATION

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact coherence/dephasing arrays and the resulting dynamical non-descent counterexample; literal sign/readout obstruction identities in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Provide any branching or many-worlds interpretation and its empirical criteria separately; mathematical non-descent neither establishes nor refutes an interpretation. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Z-decoherence pinching off-diagonal annihilation, Hadamard branch indistinguishability under diagonal shadows, and X-observable trace separation (2 != -2) mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/L1-QM020-C10-BRANCH-LOCALIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-C10-BRANCH-LOCALIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact coherence/dephasing arrays and the resulting dynamical non-descent counterexample; literal sign/readout obstruction identities in Lean.
  - does not support: Provide any branching or many-worlds interpretation and its empirical criteria separately; mathematical non-descent neither establishes nor refutes an interpretation.
  - next test: Provide any branching or many-worlds interpretation and its empirical criteria separately; mathematical non-descent neither establishes nor refutes an interpretation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1004
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` |
- counts toward the grade: yes

### Lean: `sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: [sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean](../../../sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `a2ec0a203277c5c7b4bd71067351c574509c655c18bf0e08fe3c05a8005fc497`
- cited in: node.lean, record TFQ-1004
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1004
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1004
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust, record TFQ-1004

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1004_l1_qm020_c10_branch_localization.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1004_l1_qm020_c10_branch_localization.md](../../../dag/derivations/08_l1_to_l2/tfq_1004_l1_qm020_c10_branch_localization.md)
- sha256 (`lf-normalised`): `9c8df2df8667000f1be608d0bfbd54ebf8bfbb99e2cee95176423343ad3656e1`
- generated view: listed, not counted
- cited in: record TFQ-1004
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/qm_020_born_normalization_and_conditional_hilbert_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/qm_020_born_normalization_and_conditional_hilbert_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-C10-BRANCH-PINCHING` `DERIVED_LEAN`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_LEAN)

Outgoing (0):

