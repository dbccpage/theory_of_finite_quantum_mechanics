# L1-IMP-LINEAR-ISOMETRIC-DYNAMICS

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Derived part (dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner): on the exact Born carrier Q(i)^n with the inner product fixed up to scale by the sector-form run, every ray map preserving Born transition probabilities between rays is induced by a Q(i)-linear similarity (F^H F = d * 1, d \> 0) or by conjugation followed by one; the map is invertible, so the dynamics is reversible and linear or antilinear, isometric up to the positive scale d, with no continuity hypothesis. The scale is a unit choice only when d is a norm from Q(i): the scale-3 countermodel F3 preserves transition probabilities yet is no unitary nor antiunitary ray map, so the imported form "reversible linear isometries" is strictly stronger than what the finite carrier supports; the finite statement is "reversible linear or antilinear similarities". Imported part: that the dynamics acts on the rays of the lift and preserves the Born transition probabilities (node L1-IMP-TRANSITION-PROBABILITY-LAW); the carrier, the scalar field Q(i) and the quadratic readout. QM_122 H003 still shows that deterministic report dynamics do not by themselves give reversibility, and H006 supplies the permutation envelope, now a special (unitary) case.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 26
- distinct cited Lean declarations covered by a current replay receipt: 22
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- ray dynamics preserving Born transition probabilities: assumption (node L1-IMP-TRANSITION-PROBABILITY-LAW)
- sector carrier, scalar field Q(i) and quadratic readout: assumption
- unitarity (scale a norm from Q(i)): extra arithmetic condition, not derived (countermodel F3)

## Bottleneck

Transition-probability preservation of the ray dynamics is supplied as an operational law (node L1-IMP-TRANSITION-PROBABILITY-LAW), not derived from primitive difference; the carrier, the scalar field and the quadratic readout remain imports; the similarity scale is a norm from Q(i) only under an extra arithmetic condition, and continuous time remains the Stone gap. The earlier Lean references under lean4/quantum_mechanics/ are retained as source annotations.

## Source status

Finite exact Wigner theorem kernel-checked in dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner (Lean 4.35.0): a map of the exact Born carrier Q(i)^n that sends nonzero vectors to nonzero vectors and preserves the transition probability tp x y = |\<x,y\>|^2/(|x|^2 |y|^2) (the normalised Born readout of rank-one effects, Kernel.tp_eq_born) is induced on rays by a Q(i)-linear similarity F^H F = d * 1 with a positive rational scale d, composed with the identity or with componentwise conjugation (Theorem.finite_wigner, finite_wigner_cases); the converse holds (tpPreserving_of_similarity) and the induced map is a bijection with inverse (1/d) F^H (similarity_bijective, Kernel.Similarity.inverse), so the dynamics is reversible and linear or antilinear, and no continuity hypothesis is used. The scale is removable (F = c * U with U unitary) iff d is a sum of two rational squares (Similarity.exists_unitary_iff); the countermodel F3 = \[\[1, -1+i\], \[1+i, 1\]\] with F3^H F3 = 3 * 1 preserves transition probabilities but is induced by no Q(i)-unitary and no Q(i)-antiunitary (F3_not_induced_by_unitary, F3_not_induced_by_antiunitary, three_not_sum_two_sq), so over the exact carrier the honest statement is similarity, not unitarity. The H006 permutation envelope is the unitary permMatrix (permMatrix_unitary). Aut Q(i) = {id, conjugation} (GaussRatAut.ringHom_eq_id_or_star). Exact replays: code/python/src/qm/finite_wigner.py (24 tests), code/rust/src/qm/finite_wigner.rs (29 tests). Earlier: Thm 6 assumption 5: reversible lifted dynamics by linear isometries; QM_122 H002/H003 determinism does not give reversibility

## Review

- PFP review: [dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Every Boolean map has an exact linear-extension control; only the two bijections have identity Gram matrices. Lean establishes swap preservation and collapse loss.
  - does not support: Refine the native extension to the source carrier and justify linearity/reversibility/isometry of physical dynamics. No permutation envelope derives a complex Hilbert unitary.
  - next test: Refine the native extension to the source carrier and justify linearity/reversibility/isometry of physical dynamics. No permutation envelope derives a complex Hilbert unitary.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/FiniteWignerKernel.lean`

- file: [lean4/FiniteWignerKernel.lean](../../../lean4/FiniteWignerKernel.lean)
- sha256 (`bytes`): `4a8cb01b2b211c84c8f0630d0a7716e75740731887e2ca9f8c400f3deb361814`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerKernel`): recorded sha256 `4a8cb01b2b211c84c8f0630d0a7716e75740731887e2ca9f8c400f3deb361814` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerKernel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.Kernel.Similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.Similarity` |
| `WignerFinite.Kernel.eq_smul_of_normSq_ip_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.eq_smul_of_normSq_ip_eq` |
| `WignerFinite.Kernel.expansion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.expansion` |
| `WignerFinite.Kernel.tp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.tp` |
| `WignerFinite.Kernel.tp_eq_born` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Kernel.tp_eq_born` |

- counts toward the grade: yes

### Lean: `lean4/FiniteWignerSimilarity.lean`

- file: [lean4/FiniteWignerSimilarity.lean](../../../lean4/FiniteWignerSimilarity.lean)
- sha256 (`bytes`): `1358d7bfd2451add737744d0fc685cd5454dbb78f821b2261d14e8161be65a1e`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerSimilarity`): recorded sha256 `1358d7bfd2451add737744d0fc685cd5454dbb78f821b2261d14e8161be65a1e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerSimilarity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.Similarity.F3_not_induced_by_antiunitary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.F3_not_induced_by_antiunitary` |
| `WignerFinite.Similarity.F3_not_induced_by_unitary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.F3_not_induced_by_unitary` |
| `WignerFinite.Similarity.F3_similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.F3_similarity` |
| `WignerFinite.Similarity.F3_tpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.F3_tpPreserving` |
| `WignerFinite.Similarity.exists_unitary_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.exists_unitary_iff` |
| `WignerFinite.Similarity.permMatrix_unitary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.permMatrix_unitary` |
| `WignerFinite.Similarity.three_not_sum_two_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.three_not_sum_two_sq` |
| `WignerFinite.Similarity.tpPreserving_iff_born` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Similarity.tpPreserving_iff_born` |

- counts toward the grade: yes

### Lean: `lean4/FiniteWignerTheorem.lean`

- file: [lean4/FiniteWignerTheorem.lean](../../../lean4/FiniteWignerTheorem.lean)
- sha256 (`bytes`): `77ae8e0eb904a0c1fa22dbbfdfd12e3504ab7424424c10beecd6a8173da63527`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `FiniteWignerTheorem`): recorded sha256 `77ae8e0eb904a0c1fa22dbbfdfd12e3504ab7424424c10beecd6a8173da63527` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteWignerTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.Theorem.TpPreserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.TpPreserving` |
| `WignerFinite.Theorem.coord_rigidity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.coord_rigidity` |
| `WignerFinite.Theorem.finite_wigner` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.finite_wigner` |
| `WignerFinite.Theorem.finite_wigner_cases` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.finite_wigner_cases` |
| `WignerFinite.Theorem.sgn_consistent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.sgn_consistent` |
| `WignerFinite.Theorem.similarity_bijective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.similarity_bijective` |
| `WignerFinite.Theorem.tpPreserving_of_similarity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.Theorem.tpPreserving_of_similarity` |

- counts toward the grade: yes

### Lean: `lean4/GaussRatAutomorphisms.lean`

- file: [lean4/GaussRatAutomorphisms.lean](../../../lean4/GaussRatAutomorphisms.lean)
- sha256 (`bytes`): `9d44ef37e63ef81c2c065116f1355ff405b8d62345314d23702fc937c84c2d3c`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `GaussRatAutomorphisms`): recorded sha256 `9d44ef37e63ef81c2c065116f1355ff405b8d62345314d23702fc937c84c2d3c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GaussRatAutomorphisms`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WignerFinite.GaussRatAut.ringHom_eq_id_or_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WignerFinite.GaussRatAut.ringHom_eq_id_or_star` |

- counts toward the grade: yes

### Lean: `lean4/PermutationUnitary.lean`

- file: [lean4/PermutationUnitary.lean](../../../lean4/PermutationUnitary.lean)
- sha256 (`bytes`): `7c4292b84dd988a7f220c8910579a0d6e4f8bf47fd2baf5ed66a49edf632c263`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `PermutationUnitary`): recorded sha256 `7c4292b84dd988a7f220c8910579a0d6e4f8bf47fd2baf5ed66a49edf632c263` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PermutationUnitary`
- counts toward the grade: yes

### Lean: `lean4/ReversibilityGate.lean`

- file: [lean4/ReversibilityGate.lean](../../../lean4/ReversibilityGate.lean)
- sha256 (`bytes`): `2bfb9adde035f1c6480b5561afd988cfc9e3c60eed5ba3ae09c27f3d0a4aa677`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `ReversibilityGate`): recorded sha256 `2bfb9adde035f1c6480b5561afd988cfc9e3c60eed5ba3ae09c27f3d0a4aa677` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build ReversibilityGate`
- counts toward the grade: yes

### Rust: `code/rust/src/qm/finite_wigner.rs`

- file: [code/rust/src/qm/finite_wigner.rs](../../../code/rust/src/qm/finite_wigner.rs)
- sha256 (`bytes`): `4bb3ada0b37f7eb54f994c358eb477c1fd32b5cc57ce801de2f926bc4c33995f`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `f3` (rust_symbol) | yes | yes | yes | - | - |
| `reconstruct` (rust_symbol) | yes | yes | yes | - | - |
| `similarity_certificate` (rust_symbol) | yes | yes | yes | - | - |
| `unitary_normalisation` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/finite_report_dynamics.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/finite_report_dynamics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0303_linear_isometric_dynamics_are_an_import.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0303_linear_isometric_dynamics_are_an_import.md](../../../dag/derivations/08_l1_to_l2/tfq_0303_linear_isometric_dynamics_are_an_import.md)
- sha256 (`lf-normalised`): `0f739ba559f00f23b62c9f2b7b9c67b79fc74048195b124e6b9d9deed7910029`
- generated view: listed, not counted
- cited in: record TFQ-0303
- counts toward the grade: no

### Documents and data: `dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/README.md`

- file: [dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/README.md](../../../dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner/README.md)
- sha256 (`lf-normalised`): `8b5050fbb9f1e046b3f6fbde489956734d5e6d4b5f1ef936ad56cdd6abf82a49`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0303 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs

## Routes

Incoming (2):

- `L1-R-DYNAMICS-FINITE-WIGNER` `CONDITIONAL_ON_IMPORT`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-IMP-TRANSITION-PROBABILITY-LAW](L1-IMP-TRANSITION-PROBABILITY-LAW.md) (IMPORTED_ASSUMPTION)
- `L1-R-DYNAMICS-GAP` `CONDITIONAL_ON_IMPORT`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-IMP-TRANSITION-PROBABILITY-LAW](L1-IMP-TRANSITION-PROBABILITY-LAW.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM6-P2-GLEASON](L1-QM020-THM6-P2-GLEASON.md) (IMPORTED_ASSUMPTION)
- `L1-R-THM7` `COMPUTED`: [L1-QM020-THM7-REPRESENTATION-CAPACITY](L1-QM020-THM7-REPRESENTATION-CAPACITY.md) (COMPUTATIONALLY_CHECKED)
