# DS-QM073-BELL-THEOREM-OBSTRUCTED

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Bell theorem is obstructed clause by clause with three named admissions; no derivation of quantum violation or of the Tsirelson bound from the finite tables.

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

A record of three admissions, not a theorem. The cited Lean has finite CHSH identities and a Boolean conjunction.

## Source status

P8-C9 (PL-GTOC-20) diagonal exchange suppression in characteristic-zero integral domains vs Z/4Z zero-divisor countermodel, P8-C10 three-clause Bell nature-claim obstruction, and P8-C8 four-tier squared CHSH hierarchy mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM073-BELL-THEOREM-OBSTRUCTED/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM073-BELL-THEOREM-OBSTRUCTED/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual contextual arrays and all marginal residuals are computed; 4v readout and the v=1 algebraic countermodel are kernel checked.
  - does not support: Admit or derive the global-joint, quantum operator/tensor, measurement and source assumptions separately before claiming a Bell/quantum/Tsirelson derivation.
  - next test: Admit or derive the global-joint, quantum operator/tensor, measurement and source assumptions separately before claiming a Bell/quantum/Tsirelson derivation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0260 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md](../../../dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md)
- sha256 (`lf-normalised`): `8e74bdeb1880d57c749bbd6b57d2a038c234d7f96f014f15ccd1d5d5ea06c7a7`
- generated view: listed, not counted
- cited in: record TFQ-0260 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:61609b22b375884b1a8c378d7d78eceb7893320a83140c73f97d21e042ed9247#P8-C10`
- `external:sha256:61609b22b375884b1a8c378d7d78eceb7893320a83140c73f97d21e042ed9247#P8-C8`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`

## Absences recorded by the TFQ records

- TFQ-0260 rust: no local rust twin located for external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4

## Routes

Incoming (1):

- `DS-R-BELL-THEOREM` `GAP_NO_DERIVATION`: [DS-QM073-FINITE-CHSH-AND-PR-BOX](DS-QM073-FINITE-CHSH-AND-PR-BOX.md) (COMPUTATIONALLY_CHECKED), [DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED](DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED.md) (OPEN)

Outgoing (0):

