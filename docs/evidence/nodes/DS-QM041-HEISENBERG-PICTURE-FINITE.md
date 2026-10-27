# DS-QM041-HEISENBERG-PICTURE-FINITE

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: The two exact expectation pairings agree on the declared two-state carrier.

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

- unitary family U(t) and generator H (assumption)
- complex matrices (assumption)

## Bottleneck

Unmet after the PFP review: Transport the expanded quadratic identity to full Gaussian matrices, and supply any selected time law, Hamiltonian and physical readout. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Schrodinger-Heisenberg trace cyclicity Tr(A B) = Tr(B A) and 1-step unitary conjugation duality Tr(U^T A U rho) = Tr(A U rho U^T) mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM041-HEISENBERG-PICTURE-FINITE/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM041-HEISENBERG-PICTURE-FINITE/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The two exact expectation pairings agree on the declared two-state carrier.
  - does not support: Transport the expanded quadratic identity to full Gaussian matrices, and supply any selected time law, Hamiltonian and physical readout.
  - next test: Transport the expanded quadratic identity to full Gaussian matrices, and supply any selected time law, Hamiltonian and physical readout.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0247
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0247_heisenberg_picture_on_a_finite_carrier.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0247_heisenberg_picture_on_a_finite_carrier.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0247_heisenberg_picture_on_a_finite_carrier.md)
- sha256 (`lf-normalised`): `bee0972c21f69583f78c960d7e44622792f6d55d7732f1ad81a9e84f64ff8cc8`
- generated view: listed, not counted
- cited in: record TFQ-0247
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:7b0b2660ad891bea3744bbbc03f975cba7fbffe08950bf591beebcde7d5cfacc#QM_041-C3`
- `external:sha256:7b0b2660ad891bea3744bbbc03f975cba7fbffe08950bf591beebcde7d5cfacc#QM_041-C4`
- `external:sha256:d425fe2c91956b215477384bfdbca9273ec86548579684941d9656cc15f3659a::heisenberg_observable`

## Routes

Incoming (1):

- `DS-R-HEISENBERG` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

