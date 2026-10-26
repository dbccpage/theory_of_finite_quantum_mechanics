# FQ-IMPL-REALIFICATION-ADAPTER

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A declared finite complex realization over Q(i) is mapped to its balanced real tensor (realify operator/density, product operator/density), in both omega_wdp (Genesis side) and omega_quantum_physics (quantum owner). State admission stays with the quantum owner and balancing with the math owner; this is the Rust site where a Genesis result meets a declared complex structure, and the code states it chooses none.

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

- declared complex structure over Q(i) (assumption)

## Bottleneck

The claims describe Rust code and are backed by its native exact tests. The cited Lean is integer arithmetic and does not state the claims.

## Source status

module docs: "preserve a supplied operational model; they select no scalar/Born axioms from the primitive mark and grant no execution permission"

## Review

- PFP review: [dag/results/FQ-IMPL-REALIFICATION-ADAPTER/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/FQ-IMPL-REALIFICATION-ADAPTER/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual scalar realification products, multiplication quotient, balancing kernel and normalization factor are exact; literal algebraic product/balancing identities are kernel checked.
  - does not support: Prove the full operator/density adapter, balanced tensor metric and positivity/admission transport for arbitrary finite matrices. No derivation or selection of the complex structure is supplied.
  - next test: Prove the full operator/density adapter, balanced tensor metric and positivity/admission transport for arbitrary finite matrices. No derivation or selection of the complex structure is supplied.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1027
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, node.source, record TFQ-1027
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1027
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, node.source, record TFQ-1027
- counts toward the grade: no

### Documents and data: `dag/derivations/21_implementation_core/tfq_1027_fq_impl_realification_adapter.md`

- file: [dag/derivations/21_implementation_core/tfq_1027_fq_impl_realification_adapter.md](../../../dag/derivations/21_implementation_core/tfq_1027_fq_impl_realification_adapter.md)
- sha256 (`lf-normalised`): `022f4b13894fde85257aa86a4ad774320bef701aaae7b9236574da207f2ba575`
- generated view: listed, not counted
- cited in: record TFQ-1027
- counts toward the grade: no

## Routes

Incoming (2):

- `FQ-R-REALIFICATION` `COMPUTED`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)
- `X-R-REALIFICATION-TO-ADAPTER` `COMPUTED`: [L1-WDP-REALIFICATION-J](L1-WDP-REALIFICATION-J.md) (DEFINITION)

Outgoing (1):

- `FQ-R-AMPLITUDE-BRIDGE` `COMPUTED`: [FQ-IMPL-WDP-AMPLITUDE-BRIDGE](FQ-IMPL-WDP-AMPLITUDE-BRIDGE.md) (COMPUTATIONALLY_CHECKED)
