# FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If norms N_n on Herm_0(n,C) satisfy N_m(Phi(X)) \<= N_n(X) for every CPTP map Phi : M_n(C) -\> M_m(C), then there is one c \> 0 with N_n = c ||.||_1 on every nonzero space. Holds on the full stated channel and matrix domain; not a selection of that domain from primitive difference.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex matrices and full CPTP class (assumption)

## Bottleneck

Not in Lean. The cited Lean states a duality equality for a 2x2 eigenvalue pair and that diagonal pinching does not increase -det on 2x2 trace-zero integer matrices. The characterization of CPTP-monotone norms on Herm_0(n, C) is a cited result, not derived here.

## Source status

paper s11.3 theorem with proof; scale-only version also in TraceZeroDuality.lean

## Review

- PFP review: [dag/results/FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact squared trace norms for the stated 2x2 trace-zero Hermitian family contract under the admitted diagonal pinching; the scalar inequality and positive rescaling implication are kernel checked.
  - does not support: Prove the norm-family uniqueness theorem over all dimensions and the full CPTP class. Diagonal pinching and a scale family are necessary controls, not that theorem.
  - next test: Prove the norm-family uniqueness theorem over all dimensions and the full CPTP class. Diagonal pinching and a scale family are necessary controls, not that theorem.

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
| `QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction` |

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

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0186 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code/trace_zero_quotient_duality_core.py
- TFQ-0186 rust: not located
- TFQ-0263 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0263 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs
- TFQ-0263 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs

## Routes

Incoming (1):

- `FQ-R-TRACE-NORM` `GAP_NO_DERIVATION`: [FQ-CPTP-CLASS-DEFINITION](FQ-CPTP-CLASS-DEFINITION.md) (DEFINITION)

Outgoing (1):

- `FQ-R-TRACE-ZERO-DUAL` `COMPUTED`: [FQ-TRACE-ZERO-DUALITY-K23](FQ-TRACE-ZERO-DUALITY-K23.md) (COMPUTATIONALLY_CHECKED)
