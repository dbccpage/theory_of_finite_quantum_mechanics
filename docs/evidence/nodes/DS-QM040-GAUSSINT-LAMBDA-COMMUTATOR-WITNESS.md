# DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: All cyclic identities \[Li,Lj\]=2ir Lk hold entrywise at retained scales, and declared coordinate projectors are idempotent.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Gaussian integer entries Z\[i\] (assumption); Z\[i\] is not a field

## Bottleneck

Unmet after the PFP review: Formalize every Gaussian matrix entry and projector relation in Lean, then transport to the proposed Lambda mechanism. No dynamics is selected by these witnesses. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[DERIVED\], evidence LEAN_BOUND (QM_040-C2..C5)

## Review

- PFP review: [dag/results/DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All cyclic identities \[Li,Lj\]=2ir Lk hold entrywise at retained scales, and declared coordinate projectors are idempotent.
  - does not support: Formalize every Gaussian matrix entry and projector relation in Lean, then transport to the proposed Lambda mechanism. No dynamics is selected by these witnesses.
  - next test: Formalize every Gaussian matrix entry and projector relation in Lean, then transport to the proposed Lambda mechanism. No dynamics is selected by these witnesses.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0249
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` |
| `QuantumMechanics.DerivationDagQMClosure.qm040_commutator_nonzero_and_trace_zero` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm040_commutator_nonzero_and_trace_zero` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0249_trace_zero_summaries_do_not_fix_commutation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0249_trace_zero_summaries_do_not_fix_commutation.md](../../../dag/derivations/12_finite_qm_structure/tfq_0249_trace_zero_summaries_do_not_fix_commutation.md)
- sha256 (`lf-normalised`): `bc74a3f21862d383fb923fb0274303d4661470ceba2b8c7beddb8d727234145c`
- generated view: listed, not counted
- cited in: record TFQ-0249
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/040_matrix_vs_diffeq_representation/qm_040_matrix_vs_diffeq_representation_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/040_matrix_vs_diffeq_representation/qm_040_matrix_vs_diffeq_representation_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-LGPT-GAUGE` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

