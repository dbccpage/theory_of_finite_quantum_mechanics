# FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact squared trace norms for the stated 2x2 trace-zero Hermitian family contract under the admitted diagonal pinching; the scalar inequality and positive rescaling implication are kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- complex matrices and full CPTP class (assumption)

## Bottleneck

Unmet after the PFP review: Prove the norm-family uniqueness theorem over all dimensions and the full CPTP class. Diagonal pinching and a scale family are necessary controls, not that theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

paper s11.3 theorem with proof; scale-only version also in TraceZeroDuality.lean

## Review

- PFP review: [dag/results/FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact squared trace norms for the stated 2x2 trace-zero Hermitian family contract under the admitted diagonal pinching; the scalar inequality and positive rescaling implication are kernel checked.
  - does not support: Prove the norm-family uniqueness theorem over all dimensions and the full CPTP class. Diagonal pinching and a scale family are necessary controls, not that theorem.
  - next test: Prove the norm-family uniqueness theorem over all dimensions and the full CPTP class. Diagonal pinching and a scale family are necessary controls, not that theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0263 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction` |
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

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0263_trace_norm_under_a_supplied_cptp_family.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0263_trace_norm_under_a_supplied_cptp_family.md](../../../dag/derivations/12_finite_qm_structure/tfq_0263_trace_norm_under_a_supplied_cptp_family.md)
- sha256 (`lf-normalised`): `57ea05eb68d72f3982fa7f5d2fb129fa8b62e6e047dfd05bcce347ec9a6c38d3`
- generated view: listed, not counted
- cited in: record TFQ-0263 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md](../../../dag/derivations/22_implementation_sibling/tfq_0186_do_not_treat_tracezeroduality_lean_as_a_lean_formalization_of_the_k_2_3_quotients.md)
- sha256 (`lf-normalised`): `44bcbd75b0e24dcdcbe8b82a195f42348b96cea4d9023e77dd3f166352315e23`
- generated view: listed, not counted
- cited in: record TFQ-0186 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0186 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code/trace_zero_quotient_duality_core.py
- TFQ-0186 rust: not located
- TFQ-0263 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0263 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs
- TFQ-0263 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs

## Routes

Incoming (1):

- `FQ-R-TRACE-NORM` `DERIVED_LEAN`: [FQ-CPTP-CLASS-DEFINITION](FQ-CPTP-CLASS-DEFINITION.md) (DEFINITION)

Outgoing (1):

- `FQ-R-TRACE-ZERO-DUAL` `COMPUTED`: [FQ-TRACE-ZERO-DUALITY-K23](FQ-TRACE-ZERO-DUALITY-K23.md) (COMPUTATIONALLY_CHECKED)
