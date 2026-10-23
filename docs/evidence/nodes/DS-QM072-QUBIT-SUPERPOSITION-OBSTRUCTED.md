# DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact phase-reversed pure densities and their dephased mixture share populations but differ under an admitted coherent readout; scalar readout/purity differences are kernel checked.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Construct or admit the qubit/coherence carrier, transformations and measurement rule; no generalized Bloch-contraction conjecture is accepted. The broader source statement is kept in pfp_review.prior_statement.

## Source status

P7-C1..C4 classical bit-shadow diagonal collapse, P7-C6/C8 Q1-Q4 off-diagonal X-trace separation, and P7-C10 Bloch-contraction refutation without complete positivity mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact phase-reversed pure densities and their dephased mixture share populations but differ under an admitted coherent readout; scalar readout/purity differences are kernel checked.
  - does not support: Construct or admit the qubit/coherence carrier, transformations and measurement rule; no generalized Bloch-contraction conjecture is accepted.
  - next test: Construct or admit the qubit/coherence carrier, transformations and measurement rule; no generalized Bloch-contraction conjecture is accepted.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0258
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0258_qubit_not_derived_from_the_bit_shadow.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0258_qubit_not_derived_from_the_bit_shadow.md](../../../dag/derivations/12_finite_qm_structure/tfq_0258_qubit_not_derived_from_the_bit_shadow.md)
- sha256 (`lf-normalised`): `ae403c65587ee541146357fde141b0ebabe4b7fb6b7e39a3120a18e9f09fd7ee`
- generated view: listed, not counted
- cited in: record TFQ-0258
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/072_bit_shadow_and_qubit/bit_shadow_and_qubit.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/072_bit_shadow_and_qubit/bit_shadow_and_qubit.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/072_bit_shadow_and_qubit/qm_072_bit_shadow_and_qubit_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/072_bit_shadow_and_qubit/qm_072_bit_shadow_and_qubit_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0258 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-QUBIT` `DERIVED_LEAN`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (PROVED_LEAN)

Outgoing (1):

- `DS-R-BELL-THEOREM` `DERIVED_LEAN`: [DS-QM073-BELL-THEOREM-OBSTRUCTED](DS-QM073-BELL-THEOREM-OBSTRUCTED.md) (PROVED_LEAN)
