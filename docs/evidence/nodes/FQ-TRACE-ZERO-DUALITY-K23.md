# FQ-TRACE-ZERO-DUALITY-K23

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual diagonal K23 primal/dual arrays have equal objectives6 and9/2 at unit defect scale, with correct polar balls and divergence. Native certificates bind each edge and potential. Lean checks scalar-shift invariance under a trace-zero hypothesis and the exact objective arithmetic.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.
- `receipt_not_current`: lean4/DualWitness.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- Hermitian trace-zero defects on a declared graph (assumption)

## Bottleneck

Unmet after the PFP review: Transport the explicit matrix/graph certificates to a full Lean matrix-norm duality/LP theorem. No scalar4/12 substitution, no general strong-duality theorem, and no publication correction is inferred from these local certificates. The broader source statement is kept in pfp_review.prior_statement.

## Source status

paper s11.2; exact primal/dual witnesses; Lean trace_zero_duality_gap_zero on spectra; DualWitness.lean is a 2-integer pairing bound

## Review

- PFP review: [dag/results/FQ-TRACE-ZERO-DUALITY-K23/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-TRACE-ZERO-DUALITY-K23/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual diagonal K23 primal/dual arrays have equal objectives6 and9/2 at unit defect scale, with correct polar balls and divergence. Native certificates bind each edge and potential. Lean checks scalar-shift invariance under a trace-zero hypothesis and the exact objective arithmetic.
  - does not support: Transport the explicit matrix/graph certificates to a full Lean matrix-norm duality/LP theorem. No scalar4/12 substitution, no general strong-duality theorem, and no publication correction is inferred from these local certificates.
  - next test: Transport the explicit matrix/graph certificates to a full Lean matrix-norm duality/LP theorem. No scalar4/12 substitution, no general strong-duality theorem, and no publication correction is inferred from these local certificates.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap` |
| `QuantumMechanics.DerivationDagQMClosure.k23_uncentered_zero_duality_gap` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.k23_uncentered_zero_duality_gap` |

- counts toward the grade: yes

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.lean
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DualWitness`): recorded sha256 `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build DualWitness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dual_witness_certifies_trace_distance` | yes | yes | yes | - | `#print axioms dual_witness_certifies_trace_distance` |

- counts toward the grade: yes

### Lean: `lean4/TraceZeroDuality.lean`

- file: [lean4/TraceZeroDuality.lean](../../../lean4/TraceZeroDuality.lean)
- sha256 (`bytes`): `faafda639fbe1ea89ef890d9fe55577695627a4062e33127a749aee1cb0ce091`
- cited in: node.lean, record TFQ-0186 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `TraceZeroDuality`): recorded sha256 `faafda639fbe1ea89ef890d9fe55577695627a4062e33127a749aee1cb0ce091` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build TraceZeroDuality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `trace_zero_duality_gap_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms trace_zero_duality_gap_zero` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md](../../../dag/derivations/22_implementation_sibling/tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md)
- sha256 (`lf-normalised`): `02deb04973e1958be662ae1c6a6e089c6aea82e67dbebf7d2fc1a25e68c9c036`
- generated view: listed, not counted
- cited in: record TFQ-0185
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md](../../../dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md)
- sha256 (`lf-normalised`): `f855bdb3f8ad490606f9ed83eaaca9115c7c126bde955420a58ccc0dab83c747`
- generated view: listed, not counted
- cited in: record TFQ-0186 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- `external:sha256:6d5d5d60c5905f79d67d8a8bc365e337b56a0ffb2270da01f2589b4c1a2620f0::PrimalCertificate`

## Absences recorded by the TFQ records

- TFQ-0185 lean4: not located
- TFQ-0185 python: no local python twin located for external:sha256:15a047e84ecf1f2b166b471588781c72f32ce161a9222455b4fa786878f364ed
- TFQ-0185 python: no local python twin located for external:sha256:268cb7c97325e28274aeeb256645a51550ea6e687fa42b12343e4c63215430ad
- TFQ-0185 rust: not located
- TFQ-0186 python: no local python twin located for external:sha256:268cb7c97325e28274aeeb256645a51550ea6e687fa42b12343e4c63215430ad
- TFQ-0186 rust: not located

## Routes

Incoming (1):

- `FQ-R-TRACE-ZERO-DUAL` `COMPUTED`: [FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY](FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY.md) (OPEN), [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)

Outgoing (1):

- `GP-R-EXACT-DUALITY-CERT` `COMPUTED`: [GP-GAP-EXACT-DUALITY](GP-GAP-EXACT-DUALITY.md) (COMPUTATIONALLY_CHECKED)
