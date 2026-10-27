# DS-QM030-GRADED-PATHSUM

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact two-state path enumeration, matrix powers and graded composition agree on retained lengths, including zero.

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

- grading / time-slicing of the category (assumption)
- commutative semiring of weights (assumption)
- finite fibers (assumption)

## Bottleneck

Unmet after the PFP review: Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN, CONDITIONAL-DERIVED + H1\] (QM-030-C3); QM-031-C5 \[PROVEN, MECHANIZED ENC-1128\]

## Review

- PFP review: [dag/results/DS-QM030-GRADED-PATHSUM/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM030-GRADED-PATHSUM/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact two-state path enumeration, matrix powers and graded composition agree on retained lengths, including zero.
  - does not support: Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs.
  - next test: Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0239, record TFQ-0240 (shared), record TFQ-0242
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md)
- sha256 (`lf-normalised`): `2f474eb6d5d4c39560339bcffa1d75d35a4c2e173987ad7ee807b07edda3c138`
- generated view: listed, not counted
- cited in: record TFQ-0239
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md)
- sha256 (`lf-normalised`): `aa5a173b172190b393d85768d9f179e3d8a593da450bc5485d055b06c89ce133`
- generated view: listed, not counted
- cited in: record TFQ-0240 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0242_graded_path_sum_as_finite_transport.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0242_graded_path_sum_as_finite_transport.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0242_graded_path_sum_as_finite_transport.md)
- sha256 (`lf-normalised`): `ca6d79f457df035d3e635b0c9f43eca7c0907040e0d8b3cc28c711c0badc9dba`
- generated view: listed, not counted
- cited in: record TFQ-0242
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:8b651bc7f47a6021985dd235362573dd4b5d92943b82749b13242b6ca35d4709#QM-031-C5`
- `external:sha256:e5ae08fbe8e7f3276392db13249b8444caff1fa746dec306f66e0a26fbbf9d2e#QM-030-C3`
- `external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1::TimeSlicedTransport`

## Absences recorded by the TFQ records

- TFQ-0239 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0239 rust: no local rust twin located for external:sha256:4b48c2e282a2ea334c8e4d0c1fca71cdf5555a374d1aebd974794cd6dd92b489
- TFQ-0239 rust: no local rust twin located for external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1
- TFQ-0240 rust: no local rust twin located for external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1
- TFQ-0242 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0242 rust: no local rust twin located for external:sha256:4b48c2e282a2ea334c8e4d0c1fca71cdf5555a374d1aebd974794cd6dd92b489
- TFQ-0242 rust: no local rust twin located for external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1

## Routes

Incoming (1):

- `DS-R-GRADED-PATHSUM-FROM-CARRIER` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [DS-QM030-UNGRADED-OVERCOUNT](DS-QM030-UNGRADED-OVERCOUNT.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `DS-R-DYNAMICS-FROM-L1` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FEYNMAN-SHADOW` `COMPUTED`: [DS-QM032-FINITE-FEYNMAN-SHADOW](DS-QM032-FINITE-FEYNMAN-SHADOW.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PATHSUM` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED)
