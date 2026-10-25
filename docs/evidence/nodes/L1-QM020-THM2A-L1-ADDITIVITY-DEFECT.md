# L1-QM020-THM2A-L1-ADDITIVITY-DEFECT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact scalar and disjoint-vector defect arrays, with a general disjoint-sign identity and the opposite-sign counterexample in Lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove source/list refinement and extend any l^p statement only under its real/natural exponent hypotheses. The false disjoint-same-sign biconditional is explicitly rejected. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Thm 2a MECHANIZED / finite (rational l1 additivity defect kernel, natural-exponent proxy)

## Review

- PFP review: [dag/results/L1-QM020-THM2A-L1-ADDITIVITY-DEFECT/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM2A-L1-ADDITIVITY-DEFECT/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact scalar and disjoint-vector defect arrays, with a general disjoint-sign identity and the opposite-sign counterexample in Lean.
  - does not support: Prove source/list refinement and extend any l^p statement only under its real/natural exponent hypotheses. The false disjoint-same-sign biconditional is explicitly rejected.
  - next test: Prove source/list refinement and extend any l^p statement only under its real/natural exponent hypotheses. The false disjoint-same-sign biconditional is explicitly rejected.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean, record TFQ-0291 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `D1_zero_iff_mul_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms D1_zero_iff_mul_nonneg` |
| `D1_zero_iff_same_sign` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms D1_zero_iff_same_sign` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md](../../../dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md)
- sha256 (`lf-normalised`): `c25a241ae8b5db2d245e43a14c242df7c4e5d32c7225e8cfc95d3dbefaa2f835`
- generated view: listed, not counted
- cited in: record TFQ-0291 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-THM2A` `DERIVED_LEAN`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (4):

- `L1-R-INNER-PRODUCT-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL)
- `L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)
- `L1-R-THM2B` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM2B-MINKOWSKI](L1-QM020-THM2B-MINKOWSKI.md) (PROVED_LEAN)
- `L1-R-THM6-P1` `DERIVED_LEAN`: [L1-QM020-THM6-P1-SCOPE-FENCE](L1-QM020-THM6-P1-SCOPE-FENCE.md) (PROVED_LEAN)
