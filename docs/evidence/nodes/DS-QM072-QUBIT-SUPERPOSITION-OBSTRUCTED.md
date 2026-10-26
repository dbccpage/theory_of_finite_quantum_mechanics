# DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The bit shadow is derived (P7-C1..C4) but the qubit and superposition are obstructed: the Q1-Q4 import price list names what must be added; completeness of that list is only an interpretive reading (P7-C7, fenced). The generalized Bloch-contraction statement (P7-C10) is a CONJECTURE and the ledger records a computation refuting a sharpened form.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The obstruction is a record of what must be imported, not a theorem. The cited Lean consists of integer identities for fixed 2x2 matrices.

## Source status

P7-C1..C4 classical bit-shadow diagonal collapse, P7-C6/C8 Q1-Q4 off-diagonal X-trace separation, and P7-C10 Bloch-contraction refutation without complete positivity mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
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

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

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

- TFQ-0258 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (1):

- `DS-R-QUBIT` `GAP_NO_DERIVATION`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `DS-R-BELL-THEOREM` `GAP_NO_DERIVATION`: [DS-QM073-BELL-THEOREM-OBSTRUCTED](DS-QM073-BELL-THEOREM-OBSTRUCTED.md) (OPEN)
