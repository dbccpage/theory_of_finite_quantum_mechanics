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

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0263_trace_norm_under_a_supplied_cptp_family.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0263_trace_norm_under_a_supplied_cptp_family.md](../../../dag/derivations/12_finite_qm_structure/tfq_0263_trace_norm_under_a_supplied_cptp_family.md)
- sha256 (`lf-normalised`): `57ea05eb68d72f3982fa7f5d2fb129fa8b62e6e047dfd05bcce347ec9a6c38d3`
- generated view: listed, not counted
- cited in: record TFQ-0263 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:60cc18d70e290afb3a082e12f6a048f625b9e9dcc24a29b10c25a023ac4e39ec#QM-081-C3`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:e05e7d68110a90beb2a67174e7808e5b974d46860e234edcd8b5bf329f70482e#C4`

## Absences recorded by the TFQ records

- TFQ-0263 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0263 rust: no local rust twin located for external:sha256:19f735a77b55e8182884060c73a1c66ccc64e14b24e1c3d5a173d64f8fe5b024
- TFQ-0263 rust: no local rust twin located for external:sha256:8de9a137f60908341dba42d28fa768bf1da772772d76f839787a5fcc9b56f170

## Routes

Incoming (1):

- `DS-R-TRACE-NORM-SELECTION` `GAP_NO_DERIVATION`: [DS-CPTP-COMPLETE-POSITIVITY-IMPORT](DS-CPTP-COMPLETE-POSITIVITY-IMPORT.md) (IMPORTED_ASSUMPTION), [DS-QM081-CPTP-MONOTONE-NOT-SELECTING](DS-QM081-CPTP-MONOTONE-NOT-SELECTING.md) (PROVED_LEAN)

Outgoing (0):

