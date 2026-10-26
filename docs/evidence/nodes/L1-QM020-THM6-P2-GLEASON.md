# L1-QM020-THM6-P2-GLEASON

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Born-quadratic uniqueness holds only under imported assumptions: finite additive weights, complex linear Hilbert representation, phase-blind positive descent map, orthogonal additivity, reversible lifted dynamics by linear isometries, interference as bilinear cross terms, projection-measure / frame-function structure. For dim \>= 3 Gleason gives Tr(rho Pi); dim 2 needs a POVM variant. This is the Born-uniqueness firewall.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gleason theorem: assumption
- complex Hilbert space of dim \>= 3: assumption
- orthogonal additivity / frame functions: assumption
- reversible linear isometric dynamics: assumption

## Bottleneck

Gleason is cited, not proved here. GleasonTheorem.lean states it is NOT a proof of Gleason's theorem. native/src/campaigns/born_gleason.rs exists under 006_finite_qm (accept dim3 / refuse dim2 / refuse real scalars per ledger; test names not checked).

## Source status

Thm 6 Part 2 STANDARD + citation \[1,2\] (Gleason route), CONDITIONAL on imported assumptions 1-7; GTOC-8 OPEN; OracleNeeded

## Review

- PFP review: [dag/results/L1-QM020-THM6-P2-GLEASON/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM6-P2-GLEASON/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact quadratic-frame resolution, positivity determinant and coefficient reconstruction, plus general quadratic frame identity and known-ansatz reconstruction in Lean.
  - does not support: Discharge full Gleason or POVM uniqueness with its dimension and measure hypotheses. A source named Gleason or a quadratic ansatz is not that theorem.
  - next test: Discharge full Gleason or POVM uniqueness with its dimension and measure hypotheses. A source named Gleason or a quadratic ansatz is not that theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornNormalization.lean`

- file: [lean4/BornNormalization.lean](../../../lean4/BornNormalization.lean)
- sha256 (`bytes`): `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8`
- cited in: record TFQ-0307 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornNormalization`): recorded sha256 `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornNormalization`
- counts toward the grade: no

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0307 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/GleasonTheorem.lean`

- file: [lean4/GleasonTheorem.lean](../../../lean4/GleasonTheorem.lean)
- sha256 (`bytes`): `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `GleasonTheorem`): recorded sha256 `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonTheorem`
- counts toward the grade: yes

### Lean: `lean4/H017Gleason.lean`

- file: [lean4/H017Gleason.lean](../../../lean4/H017Gleason.lean)
- sha256 (`bytes`): `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H017Gleason`): recorded sha256 `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H017Gleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gleason_pack_uniqueness_still_imported` | yes | yes | yes | none | `#print axioms gleason_pack_uniqueness_still_imported` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md](../../../dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md)
- sha256 (`lf-normalised`): `7c6c2498ae3a8a9ca89f986289680fec7db4936bceccc852ebc20ab3cc2f76c5`
- generated view: listed, not counted
- cited in: record TFQ-0307 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/qm_020_born_normalization_and_conditional_hilbert_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/qm_020_born_normalization_and_conditional_hilbert_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE), [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL), [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL), [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)

Outgoing (1):

- `UDG-R-TFQ-0308` `GAP_NO_DERIVATION`: [TFQ-0308](TFQ-0308.md) (OPEN)
