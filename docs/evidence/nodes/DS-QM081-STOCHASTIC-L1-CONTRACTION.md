# DS-QM081-STOCHASTIC-L1-CONTRACTION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A column-stochastic kernel does not increase the L1 norm: |Sx|_1 \<= |x|_1 (finite classical shadow of trace-norm contraction).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Operator trace-norm contractivity on M_n(C) not mechanized (upgrade row QM-081-C4).

## Source status

\[MECHANIZED\] ENC-1055 (QM-081-C5)

## Review

- PFP review: [dag/results/DS-QM081-STOCHASTIC-L1-CONTRACTION/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM081-STOCHASTIC-L1-CONTRACTION/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Generic finite rational column-stochastic L1 contraction is kernel checked; retained three-state outputs and triangle budgets are exact.
  - does not support: Transport the array implementation to the formal finite sums and any supplied quantum/CPTP interface. Classical contraction does not derive a quantum carrier.
  - next test: Transport the array implementation to the formal finite sums and any supplied quantum/CPTP interface. Classical contraction does not derive a quantum carrier.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0264 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |
| `QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0264_monotonicity_does_not_select_the_trace_norm.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0264_monotonicity_does_not_select_the_trace_norm.md](../../../dag/derivations/12_finite_qm_structure/tfq_0264_monotonicity_does_not_select_the_trace_norm.md)
- sha256 (`lf-normalised`): `f7afb5c8b184d4faf8cc11f6f08962e178251d4f34f7578c72c09ddb80d85458`
- generated view: listed, not counted
- cited in: record TFQ-0264 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/081_trace_norm_cptp_transport_audit/qm_081_trace_norm_cptp_transport_audit_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/081_trace_norm_cptp_transport_audit/qm_081_trace_norm_cptp_transport_audit_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0264 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0264 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs
- TFQ-0264 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs

## Routes

Incoming (1):

- `DS-R-STOCHASTIC-CONTRACTION` `DERIVED_LEAN`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (PROVED_LEAN)

Outgoing (1):

- `DS-R-TRACE-NORM-CORE-FROM-CARRIER` `DERIVED_LEAN`: [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) (PROVED_LEAN)
