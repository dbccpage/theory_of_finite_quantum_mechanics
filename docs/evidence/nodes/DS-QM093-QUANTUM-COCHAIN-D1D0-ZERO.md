# DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Full conjugated arrays, composition control and trace-pairing/coboundary identities are checked exactly with a general rational conditional kernel identity.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- M_2 packet with trace and unitary gauge (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the array-to-matrix interpretation, full complex unitary packet and contextual gluing/physical readout. Gauge invariance alone is not selection. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN — packet-specific\] (QM-093-C15, C16); QM-092-C13 \[PROVEN\] (algebraic)

## Review

- PFP review: [dag/results/DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Full conjugated arrays, composition control and trace-pairing/coboundary identities are checked exactly with a general rational conditional kernel identity.
  - does not support: Formalize the array-to-matrix interpretation, full complex unitary packet and contextual gluing/physical readout. Gauge invariance alone is not selection.
  - next test: Formalize the array-to-matrix interpretation, full complex unitary packet and contextual gluing/physical readout. Gauge invariance alone is not selection.

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
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |
| `QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md](../../../dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md)
- sha256 (`lf-normalised`): `1463ba1ada7b6d51c89a0588d1ffffb7bc50584dcebf8eda5434b97e3fd2f715`
- generated view: listed, not counted
- cited in: record TFQ-0273 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md`

- file: [dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md](../../../dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)
- sha256 (`lf-normalised`): `24435b37027494cea1e6541393a74dfaa720915fdab89c57efcf22685a0d8568`
- generated view: listed, not counted
- cited in: record TFQ-0052 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite/qm_092_qm_typed_authority_boundary_suite_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite/qm_092_qm_typed_authority_boundary_suite_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0052 lean4: not located
- TFQ-0052 python: not located
- TFQ-0052 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs

## Routes

Incoming (2):

- `DS-R-COCHAIN-D1D0` `DERIVED_LEAN`: [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)
- `DS-R-D1D0-COCHAIN` `DERIVED_LEAN`: [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (1):

- `DS-R-SURVIVAL` `COMPUTED`: [DS-QM093-SURVIVAL-THEOREM](DS-QM093-SURVIVAL-THEOREM.md) (COMPUTATIONALLY_CHECKED)
