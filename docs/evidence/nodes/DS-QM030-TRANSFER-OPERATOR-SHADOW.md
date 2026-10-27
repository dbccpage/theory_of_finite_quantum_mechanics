# DS-QM030-TRANSFER-OPERATOR-SHADOW

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: All coefficients of AB, (AB)v, A(Bv), fA, f(Av), and (fA)v agree on exact retained inputs.

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

- ring structure (subtraction) (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN, CONDITIONAL-DERIVED + H2\] (QM-030-C6)

## Review

- PFP review: [dag/results/DS-QM030-TRANSFER-OPERATOR-SHADOW/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM030-TRANSFER-OPERATOR-SHADOW/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All coefficients of AB, (AB)v, A(Bv), fA, f(Av), and (fA)v agree on exact retained inputs.
  - does not support: Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied.
  - next test: Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1039
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_1039_ds_qm030_transfer_operator_shadow.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_1039_ds_qm030_transfer_operator_shadow.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_1039_ds_qm030_transfer_operator_shadow.md)
- sha256 (`lf-normalised`): `fef2d167124468d066875caeea5cf064483a7568de54bd4a08b6dfafc808cffe`
- generated view: listed, not counted
- cited in: record TFQ-1039
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:e5ae08fbe8e7f3276392db13249b8444caff1fa746dec306f66e0a26fbbf9d2e#QM-030-C6`
- `external:sha256:e5ae08fbe8e7f3276392db13249b8444caff1fa746dec306f66e0a26fbbf9d2e#QM-030-C8`

## Routes

Incoming (1):

- `DS-R-PATHSUM` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `DS-R-LGPT-GAUGE` `COMPUTED`: [DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS](DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-FROM-PATHSUM` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
