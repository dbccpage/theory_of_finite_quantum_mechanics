# FQ-TRACE-ZERO-DUALITY-K23

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual diagonal K23 primal/dual arrays have equal objectives6 and9/2 at unit defect scale, with correct polar balls and divergence. Native certificates bind each edge and potential. Lean checks scalar-shift invariance under a trace-zero hypothesis and the exact objective arithmetic.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

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
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap` |
| `QuantumMechanics.DerivationDagQMClosure.k23_uncentered_zero_duality_gap` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.k23_uncentered_zero_duality_gap` |
- counts toward the grade: yes

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DualWitness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dual_witness_certifies_trace_distance` | yes | yes | yes | - | `#print axioms dual_witness_certifies_trace_distance` |
- counts toward the grade: yes

### Lean: `lean4/TraceZeroDuality.lean`

- file: [lean4/TraceZeroDuality.lean](../../../lean4/TraceZeroDuality.lean)
- sha256 (`bytes`): `faafda639fbe1ea89ef890d9fe55577695627a4062e33127a749aee1cb0ce091`
- cited in: node.lean, record TFQ-0186 (shared)
- replay: `none`
- check: `cd lean4 && lake build TraceZeroDuality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `trace_zero_duality_gap_zero` | yes | yes | yes | - | `#print axioms trace_zero_duality_gap_zero` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/trace_distance_quotient.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/trace_distance_quotient.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md](../../../dag/derivations/22_implementation_sibling/tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md)
- sha256 (`lf-normalised`): `d60490d4c67592c93f72cba05072726c9657e000e7cdab45b5009b8d3d440858`
- generated view: listed, not counted
- cited in: record TFQ-0185
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md](../../../dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md)
- sha256 (`lf-normalised`): `44bcbd75b0e24dcdcbe8b82a195f42348b96cea4d9023e77dd3f166352315e23`
- generated view: listed, not counted
- cited in: record TFQ-0186 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0185 lean4: not located
- TFQ-0185 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code/tests/test_trace_zero_quotient_duality.py
- TFQ-0185 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code/trace_zero_quotient_duality_core.py
- TFQ-0185 rust: not located
- TFQ-0186 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code/trace_zero_quotient_duality_core.py
- TFQ-0186 rust: not located

## Routes

Incoming (1):

- `FQ-R-TRACE-ZERO-DUAL` `COMPUTED`: [FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY](FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY.md) (PROVED_LEAN), [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)

Outgoing (1):

- `GP-R-EXACT-DUALITY-CERT` `COMPUTED`: [GP-GAP-EXACT-DUALITY](GP-GAP-EXACT-DUALITY.md) (COMPUTATIONALLY_CHECKED)
