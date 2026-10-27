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

Gleason is cited, not proved here. GleasonTheorem.lean states it is NOT a proof of Gleason's theorem. native/src/campaigns/born_gleason.rs exists under finite_quantum_mechanics (accept dim3 / refuse dim2 / refuse real scalars per ledger; test names not checked).

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

### Lean: `lean4/HilbertWalkGleason.lean`

- file: [lean4/HilbertWalkGleason.lean](../../../lean4/HilbertWalkGleason.lean)
- sha256 (`bytes`): `42c9d771c0f1c717bcf7673918fe0ee69046418ca70c1f6fd8ee9972977f9d30`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleason`): recorded sha256 `42c9d771c0f1c717bcf7673918fe0ee69046418ca70c1f6fd8ee9972977f9d30` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gleason_pack_uniqueness_still_imported` | yes | yes | yes | none | `#print axioms gleason_pack_uniqueness_still_imported` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md](../../../dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md)
- sha256 (`lf-normalised`): `cbdaa44b0fba859fe8fe7dd5ada4b13dbeb9c1e39728690a396b044f7798a6ff`
- generated view: listed, not counted
- cited in: record TFQ-0307 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:780`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:831`
- `external:sha256:ae888a69f68011cf2bdbe26b173cbe6cf818f2a9c044b25aa7b39f5592b688c5`
- `external:sha256:c061ef7e709a4bfb47b1bca1c4182aba033ca07cf550c24aac6d9efed6b9f41f#GTOC-8`
- `external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e`

## Routes

Incoming (1):

- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE), [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL), [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL), [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)

Outgoing (1):

- `UDG-R-TFQ-0308` `GAP_NO_DERIVATION`: [TFQ-0308](TFQ-0308.md) (OPEN)
