# FQ-IMPL-REALIFICATION-ADAPTER

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A declared finite complex realization over Q(i) is mapped to its balanced real tensor (realify operator/density, product operator/density), in both tfqm_wdp (Genesis side) and quantum_physics (quantum owner). State admission stays with the quantum owner and balancing with the math owner; this is the Rust site where a Genesis result meets a declared complex structure, and the code states it chooses none.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- declared complex structure over Q(i) (assumption)

## Bottleneck

The claims describe Rust code and are backed by its native exact tests. The cited Lean is integer arithmetic and does not state the claims.

## Source status

2x2 realification multiplication/transpose homomorphism and Hermitian trace balance mechanized in DerivationDagQMClosure.lean and WdpBatch8.lean

## Review

- PFP review: [evidence/results/FQ-IMPL-REALIFICATION-ADAPTER/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../evidence/results/FQ-IMPL-REALIFICATION-ADAPTER/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual scalar realification products, multiplication quotient, balancing kernel and normalization factor are exact; literal algebraic product/balancing identities are kernel checked.
  - does not support: Prove the full operator/density adapter, balanced tensor metric and positivity/admission transport for arbitrary finite matrices. No derivation or selection of the complex structure is supplied.
  - next test: Prove the full operator/density adapter, balanced tensor metric and positivity/admission transport for arbitrary finite matrices. No derivation or selection of the complex structure is supplied.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean)
- sha256 (`bytes`): `42063910b1edb4aa7f509fb0310b262235a7ce77dd5d2e3a5cf03556ecb175b1`
- cited in: node.lean, record TFQ-1027
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch8.realify2x2_mul_and_transpose_hom` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch8.realify2x2_mul_and_transpose_hom` |
| `WitnessedDifference.WdpBatch8.realify2x2_trace_and_hermitian_balance` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch8.realify2x2_trace_and_hermitian_balance` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1027
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_finite_qm_structure.json](../../../evidence/lean_receipts/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/21_implementation_core/tfq_1027_fq_impl_realification_adapter.md`

- file: [dag/derivations/21_implementation_core/tfq_1027_fq_impl_realification_adapter.md](../../../dag/derivations/21_implementation_core/tfq_1027_fq_impl_realification_adapter.md)
- sha256 (`lf-normalised`): `ec0760c627ce1cbf06bfe054feb1c9e257efd8653b741c7ae02e1aec1958f7a4`
- generated view: listed, not counted
- cited in: record TFQ-1027
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1ae9121daca3f6d1f5cb700a325bc1aaa0d5a6988db99eee907e24ca729e876e::realify_density_with_limits`
- `external:sha256:1ae9121daca3f6d1f5cb700a325bc1aaa0d5a6988db99eee907e24ca729e876e::realify_operator_with_limits`
- `external:sha256:1ae9121daca3f6d1f5cb700a325bc1aaa0d5a6988db99eee907e24ca729e876e:1`
- `external:sha256:3dab36e238ec5c724db50e333358961506db6e3c22a04fbd6a26402ffe48f7fc::DeclaredRealComposite`
- `external:sha256:3dab36e238ec5c724db50e333358961506db6e3c22a04fbd6a26402ffe48f7fc:1`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`

## Routes

Incoming (2):

- `FQ-R-REALIFICATION` `DERIVED_LEAN`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)
- `X-R-REALIFICATION-TO-ADAPTER` `DERIVED_LEAN`: [L1-WDP-REALIFICATION-J](L1-WDP-REALIFICATION-J.md) (DEFINITION)

Outgoing (1):

- `FQ-R-AMPLITUDE-BRIDGE` `DERIVED_LEAN`: [FQ-IMPL-WDP-AMPLITUDE-BRIDGE](FQ-IMPL-WDP-AMPLITUDE-BRIDGE.md) (PROVED_LEAN)
