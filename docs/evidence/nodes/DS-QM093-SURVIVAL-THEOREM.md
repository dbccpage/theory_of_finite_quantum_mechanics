# DS-QM093-SURVIVAL-THEOREM

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The declared three-field antecedent (imported interface, verified finite replay, sealed replay terminalization) has the expected truth table and a missing seal is refused; this is a Boolean conjunction. The real survival antecedent, in particular the sealed external replay, is undischarged.

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

- sealed external replay terminalizer (assumption)
- quantum interface F_Q (assumption)

## Bottleneck

Unmet after the PFP review: Obtain and validate the imported interface, replay evidence and sealed external terminalizer. A true input flag is not that evidence and does not terminalize anything. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Idempotent quotient predicate survival P(pi(pi(x))) = P(pi(x)) and fiber-constant lift invariance mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM093-SURVIVAL-THEOREM/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM093-SURVIVAL-THEOREM/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The declared three-field antecedent truth table and missing-seal refusal are kernel/native checked; the real survival antecedent remains undischarged.
  - does not support: Obtain and validate the imported interface, replay evidence and sealed external terminalizer. A true input flag is not that evidence and does not terminalize anything.
  - next test: Obtain and validate the imported interface, replay evidence and sealed external terminalizer. A true input flag is not that evidence and does not terminalize anything.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0273 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md](../../../dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md)
- sha256 (`lf-normalised`): `1463ba1ada7b6d51c89a0588d1ffffb7bc50584dcebf8eda5434b97e3fd2f715`
- generated view: listed, not counted
- cited in: record TFQ-0273 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:a2f7562df5b5aeb03fb8dbd451d2007e85bf133ddf4d625c5b59f92b37ab489e#QM-093-C18`

## Routes

Incoming (1):

- `DS-R-SURVIVAL` `COMPUTED`: [DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY](DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY.md) (PROVED_LEAN), [DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO](DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

