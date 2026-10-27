# DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For M_2 packets, trace cyclicity gives d1_Q d0_Q = 0 (Born/trace invariance under exact unitary gauge); Born is a defect face at C^2, invariance not selection; classical gluing fails for contextual observables (Phi_Q\>0). Packet-specific.

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

- M_2 packet with trace and unitary gauge (assumption)

## Bottleneck

Lean states only the scalar telescoping identity (fj - fi) + (fk - fj) - (fk - fi) = 0. The M_2 trace-cyclicity statement is checked natively on fixed matrices.

## Source status

\[PROVEN — packet-specific\] (QM-093-C15, C16); QM-092-C13 \[PROVEN\] (algebraic)

## Review

- PFP review: [dag/results/DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:a2f7562df5b5aeb03fb8dbd451d2007e85bf133ddf4d625c5b59f92b37ab489e#QM-093-C15`
- `external:sha256:a2f7562df5b5aeb03fb8dbd451d2007e85bf133ddf4d625c5b59f92b37ab489e#QM-093-C16`
- `external:sha256:e3654d5e92fe9c522754b597ad0a8e2464822e0dad0b6711be0b971b1c967c9a#QM-092-C13`

## Absences recorded by the TFQ records

- TFQ-0052 lean4: not located
- TFQ-0052 python: not located
- TFQ-0052 rust: no local rust twin located for external:sha256:1716598040aa40ee83bed4fdf0e76ab6111debd683decf50bbbe5df6dbc71b65

## Routes

Incoming (2):

- `DS-R-COCHAIN-D1D0` `COMPUTED`: [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)
- `DS-R-D1D0-COCHAIN` `COMPUTED`: [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (1):

- `DS-R-SURVIVAL` `COMPUTED`: [DS-QM093-SURVIVAL-THEOREM](DS-QM093-SURVIVAL-THEOREM.md) (COMPUTATIONALLY_CHECKED)
