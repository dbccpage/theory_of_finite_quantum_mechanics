# DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The half trace norm is the distinguishability metric under four imports: quantum interface M_n(C), trace-distance axioms (unitary invariance, classical total-variation reduction, homogeneity), CPTP compatibility and edge additivity. Does not survive removal of those imports.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- density matrices and M_n(C) (assumption)
- CPTP maps (assumption)
- tensor product (assumption)
- spectral theorem (assumption)

## Bottleneck

Not in Lean. The cited Lean is integer arithmetic and the 2x2 pinching inequality.

## Source status

\[PROVEN, CONDITIONAL\] (QM-080-C4); QM-081-C3 \[conditionally admitted under H1-H4\]; ENC-0246 Lean NOT-STARTED

## Review

- PFP review: [dag/results/DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact diagonal half-trace/total-variation identity is kernel checked; rescaling controls retain normalization ambiguity.
  - does not support: Supply spectral/matrix interface, unitary invariance, CPTP compatibility, edge additivity and the actual uniqueness proof before promoting to full quantum half trace norm.
  - next test: Supply spectral/matrix interface, unitary invariance, CPTP compatibility, edge additivity and the actual uniqueness proof before promoting to full quantum half trace norm.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0263 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction` |

- counts toward the grade: yes

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

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/080_cptp_trace_norm_geometry_and_quantum_dual_witnesses/qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/080_cptp_trace_norm_geometry_and_quantum_dual_witnesses/qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/081_trace_norm_cptp_transport_audit/qm_081_trace_norm_cptp_transport_audit_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/081_trace_norm_cptp_transport_audit/qm_081_trace_norm_cptp_transport_audit_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0263 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0263 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs
- TFQ-0263 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs

## Routes

Incoming (1):

- `DS-R-TRACE-NORM-SELECTION` `GAP_NO_DERIVATION`: [DS-CPTP-COMPLETE-POSITIVITY-IMPORT](DS-CPTP-COMPLETE-POSITIVITY-IMPORT.md) (IMPORTED_ASSUMPTION), [DS-QM081-CPTP-MONOTONE-NOT-SELECTING](DS-QM081-CPTP-MONOTONE-NOT-SELECTING.md) (PROVED_LEAN)

Outgoing (0):

