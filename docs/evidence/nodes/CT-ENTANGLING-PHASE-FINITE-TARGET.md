# CT-ENTANGLING-PHASE-FINITE-TARGET

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement over Q(i), checked in Lean 4 for (a) to (c); (d) is not proved. For u in Q(i) (the Lean proofs of (a) and (b) do not use |u|=1), the two-qubit vector psi_u = (1,1,1,u)/2 has coefficient matrix M_u = \[\[1,1\],\[1,u\]\]/2 of determinant (u-1)/4. (a) psi_u is a product vector if and only if u=1. (b) The squared concurrence, defined as 4|det M|^2, equals |u-1|^2/4 for M_u; for u=(3+4i)/5, where |u|=1, it equals 1/5. (c) For all 2x2 matrices A and B over Q(i), det(A M B^T) = det(A) det(M) det(B), so det M = 0 implies det(A M B^T) = 0: local operations cannot raise a product vector to Schmidt rank 2; and diag(1,1,1,u) applied to the product vector (1,1,1,1)/2 gives psi_u. The physical inference from such entanglement to a non-classical mediator is imported, not part of this target.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_not_current`: lean4/DualWitness.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

None recorded.

## Bottleneck

Statement (d), an exact separating functional on the 4x4 density matrix relative to the product family in the form of DS-QM071, is not proved. The Lean module defines schmidtWitnessExpectation(M) = |det M|^2, a quadratic function of the amplitude matrix that vanishes on product vectors and is positive on psi_u for u != 1; that is a restatement of (a), not a linear functional on density matrices, and it is not shown to vanish on mixtures of product states or tied to DS-QM071. The rank inequality rank(A M B^T) \<= rank(M) for general rank is stated only through the 2x2 determinant identity (preservation of det M = 0). No physical claim is attached.

## Source status

Exact Gaussian-rational value C^2 = 1/5 at u = (3+4i)/5 verified with Python fractions.Fraction on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierEntanglingPhase (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `det_M_u`, `psi_u_isProduct_iff`, `concurrenceSq_M_u`, `u_pythagorean_unit_and_concurrence`, `det2_local_action`, `local_op_cannot_raise_product_rank`, `diag_phase_maps_psi1_to_psiu`, `schmidtWitness_*`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.source
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DualWitness`): recorded sha256 `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build DualWitness`
- counts toward the grade: yes

### Lean: `lean4/Entanglement.lean`

- file: [lean4/Entanglement.lean](../../../lean4/Entanglement.lean)
- sha256 (`bytes`): `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_constructor_theory.json](../../../dag/research/lean_replay_campaign_constructor_theory.json) (module `Entanglement`): recorded sha256 `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Entanglement`
- counts toward the grade: yes

### Lean: `lean4/FrontierEntanglingPhase.lean`

- file: [lean4/FrontierEntanglingPhase.lean](../../../lean4/FrontierEntanglingPhase.lean)
- sha256 (`bytes`): `94bccd3a1bf1ca1b05533ff9b812cdd5089395a731c0257140ae63dccbb87d2d`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierEntanglingPhase)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierEntanglingPhase`): recorded sha256 `94bccd3a1bf1ca1b05533ff9b812cdd5089395a731c0257140ae63dccbb87d2d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierEntanglingPhase`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierEntanglingPhase.concurrenceSq_M_u` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.concurrenceSq_M_u` |
| `FrontierEntanglingPhase.det2_local_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.det2_local_action` |
| `FrontierEntanglingPhase.det_M_u` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.det_M_u` |
| `FrontierEntanglingPhase.diag_phase_maps_psi1_to_psiu` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.diag_phase_maps_psi1_to_psiu` |
| `FrontierEntanglingPhase.local_op_cannot_raise_product_rank` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.local_op_cannot_raise_product_rank` |
| `FrontierEntanglingPhase.productState2_det_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.productState2_det_zero` |
| `FrontierEntanglingPhase.psi_u_isProduct_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.psi_u_isProduct_iff` |
| `FrontierEntanglingPhase.schmidtWitness_strictly_positive_for_u_ne_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.schmidtWitness_strictly_positive_for_u_ne_one` |
| `FrontierEntanglingPhase.schmidtWitness_vanishes_on_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.schmidtWitness_vanishes_on_product` |
| `FrontierEntanglingPhase.u_pythagorean_unit_and_concurrence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierEntanglingPhase.u_pythagorean_unit_and_concurrence` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2014_ct_entangling_phase_finite_target.md`

- file: [dag/derivations/30_constructor_theory/tfq_2014_ct_entangling_phase_finite_target.md](../../../dag/derivations/30_constructor_theory/tfq_2014_ct_entangling_phase_finite_target.md)
- sha256 (`lf-normalised`): `9be6bec593ec9708e4b747d89ae5ed21a25697856dbddf3c0efa2915f5d3d73e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2014
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-CT-ENTANGLING-PHASE-FINITE-TARGET` `DERIVED_LEAN`: [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) (PROVED_LEAN), [CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT](CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

