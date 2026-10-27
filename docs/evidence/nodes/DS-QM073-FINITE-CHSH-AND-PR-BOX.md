# DS-QM073-FINITE-CHSH-AND-PR-BOX

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Bare joint tables are always separable (P8-C3); under a single global joint table the finite CHSH bound is 2; the PR box reaches 4 and has no joint table. The load-bearing hypothesis is the existence of one global joint table. Tsirelson ceiling is not derived (P8-C8 OPEN).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Lean checks that every deterministic +/-1 assignment has CHSH value of square 4 and the PR-box value 4. The bound 2 for a single joint table follows by convexity, which is not in Lean; separability of bare tables is a native check.

## Source status

P8-C3 single-table local rank-1 decomposition, P8-C6 16-vertex deterministic CHSH ceiling (|S|=2), P8-C7 PR-box S=4 non-extension, and P8-C8 rational/Tsirelson CHSH hierarchy (100 \< 196 \< 200 \< 400) mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM073-FINITE-CHSH-AND-PR-BOX/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM073-FINITE-CHSH-AND-PR-BOX/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Every deterministic row, weighted correlation and PR entry is exact; deterministic CHSH and generic convex absolute bound are kernel checked.
  - does not support: Formalize the concrete table-to-general convex theorem transport and any full Fine converse or quantum realization. Product/separable for a bare classical table has a different meaning from quantum separability.
  - next test: Formalize the concrete table-to-general convex theorem transport and any full Fine converse or quantum realization. Product/separable for a bare classical table has a different meaning from quantum separability.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContextualityObstruction.lean`

- file: [lean4/ContextualityObstruction.lean](../../../lean4/ContextualityObstruction.lean)
- sha256 (`bytes`): `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `ContextualityObstruction`): recorded sha256 `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContextualityObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `x1_has_no_global_section` | yes | yes | yes | Quot.sound, propext | `#print axioms x1_has_no_global_section` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0259 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md](../../../dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md)
- sha256 (`lf-normalised`): `b2177f05c11715d1dec037d5488c6c1e891d6c536e6fb4c875616087051c4c65`
- generated view: listed, not counted
- cited in: record TFQ-0259 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:61609b22b375884b1a8c378d7d78eceb7893320a83140c73f97d21e042ed9247#P8-C3`
- `external:sha256:61609b22b375884b1a8c378d7d78eceb7893320a83140c73f97d21e042ed9247#P8-C6`
- `external:sha256:61609b22b375884b1a8c378d7d78eceb7893320a83140c73f97d21e042ed9247#P8-C7`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`
- `external:sha256:b51b4e31d573db4525e5f4bba75d849b974db31a3eb30756ff0208f62dd48c3e::finite_bell_extension`

## Absences recorded by the TFQ records

- TFQ-0259 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0259 rust: no local rust twin located for external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4

## Routes

Incoming (1):

- `DS-R-ENTANGLEMENT-TO-BELL` `COMPUTED`: [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) (PROVED_LEAN)

Outgoing (2):

- `DS-R-BELL-THEOREM` `GAP_NO_DERIVATION`: [DS-QM073-BELL-THEOREM-OBSTRUCTED](DS-QM073-BELL-THEOREM-OBSTRUCTED.md) (OPEN)
- `DS-R-BELL-TO-NOSIGNALING` `COMPUTED`: [DS-QM074-NO-SIGNALING-MARGINAL](DS-QM074-NO-SIGNALING-MARGINAL.md) (COMPUTATIONALLY_CHECKED)
