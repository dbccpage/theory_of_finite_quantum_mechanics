# DS-QM081-CPTP-MONOTONE-NOT-SELECTING

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> CPTP-monotonicity of a functional j does not pin j = half trace norm: j and 2j are both monotone. Many monotone measures exist (relative entropy, fidelity-based); breadth upgrade (norm not proportional to trace norm) not constructed.

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

Scalar-family non-selection only.

## Source status

\[PROVEN — Lean-mechanized\] ENC-0247 MECHANIZED-PARTIAL (QM-081-C1, C2)

## Review

- PFP review: [dag/results/DS-QM081-CPTP-MONOTONE-NOT-SELECTING/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM081-CPTP-MONOTONE-NOT-SELECTING/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact stochastic contraction controls, nonnegative rescaling and distinct positive-scale values are kernel/native checked.
  - does not support: Admit a full channel class and prove a full quantum monotonicity theorem or a nonproportional counterexample if that broader selection question is pursued.
  - next test: Admit a full channel class and prove a full quantum monotonicity theorem or a nonproportional counterexample if that broader selection question is pursued.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0264 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/TraceZeroDuality.lean`

- file: [lean4/TraceZeroDuality.lean](../../../lean4/TraceZeroDuality.lean)
- sha256 (`bytes`): `faafda639fbe1ea89ef890d9fe55577695627a4062e33127a749aee1cb0ce091`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build TraceZeroDuality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `monotone_metric_distinct` | yes | yes | yes | - | `#print axioms monotone_metric_distinct` |
| `scaleMetric_monotone` | yes | yes | yes | - | `#print axioms scaleMetric_monotone` |
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

## Absences recorded by the TFQ records

- TFQ-0264 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0264 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs
- TFQ-0264 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs

## Routes

Incoming (1):

- `DS-R-MONOTONE-NONSELECTION` `DERIVED_LEAN`: [DS-CPTP-COMPLETE-POSITIVITY-IMPORT](DS-CPTP-COMPLETE-POSITIVITY-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `DS-R-TRACE-NORM-SELECTION` `DERIVED_LEAN`: [DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION](DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION.md) (PROVED_LEAN)
