# L1-QM020-C10-BRANCH-LOCALIZATION

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Branch-localization and many-worlds readings of the lifted phases are conjectures, not part of the QM_020 theorems.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Interpretive readings (branch localization, many worlds) are not formalised. The cited Lean has 2x2 pinching and sign identities, which bear on dephasing but not on the readings.

## Source status

Z-decoherence pinching off-diagonal annihilation, Hadamard branch indistinguishability under diagonal shadows, and X-observable trace separation (2 != -2) mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-QM020-C10-BRANCH-LOCALIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-C10-BRANCH-LOCALIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact coherence/dephasing arrays and the resulting dynamical non-descent counterexample; literal sign/readout obstruction identities in Lean.
  - does not support: Provide any branching or many-worlds interpretation and its empirical criteria separately; mathematical non-descent neither establishes nor refutes an interpretation.
  - next test: Provide any branching or many-worlds interpretation and its empirical criteria separately; mathematical non-descent neither establishes nor refutes an interpretation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1004
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust, record TFQ-1004

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1004_l1_qm020_c10_branch_localization.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1004_l1_qm020_c10_branch_localization.md](../../../dag/derivations/08_l1_to_l2/tfq_1004_l1_qm020_c10_branch_localization.md)
- sha256 (`lf-normalised`): `4ae9dbb6c41eb42164e22b2f44020457c8073b861f40cfff2c67487a0bdeda83`
- generated view: listed, not counted
- cited in: record TFQ-1004
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:c061ef7e709a4bfb47b1bca1c4182aba033ca07cf550c24aac6d9efed6b9f41f#C10`

## Routes

Incoming (1):

- `L1-R-C10-BRANCH-PINCHING` `GAP_NO_DERIVATION`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE)

Outgoing (0):

