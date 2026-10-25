# MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Quartet existence in C^6 is equivalent to admissible bounded block data (E, B, C) whose completion with D = -C E* (B^-1)* has a raw quartet, and to a solution of the division-free equations obtained by clearing the nonzero determinant of B.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Infeasibility of these equations is open; the positive determinant bound is needed for reconstruction and for the MU-factor cancellation.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C12 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubBoundedBlockChart.lean`

- file: [lean4/MubBoundedBlockChart.lean](../../../lean4/MubBoundedBlockChart.lean)
- sha256 (`bytes`): `2a29801d5f787f2e63f4c06d1df18e37d773d1fee3472cf8c529a894a3fb4917`
- cited in: node.lean, record TFQ-1260
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubBoundedBlockChart`): recorded sha256 `2a29801d5f787f2e63f4c06d1df18e37d773d1fee3472cf8c529a894a3fb4917` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubBoundedBlockChart`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_quartet_iff_bounded_completion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_quartet_iff_bounded_completion` |

- counts toward the grade: yes

### Lean: `lean4/MubBoundedMUFactor.lean`

- file: [lean4/MubBoundedMUFactor.lean](../../../lean4/MubBoundedMUFactor.lean)
- sha256 (`bytes`): `732189950dec5044fedb0f3b2f541e0eac714e3419099cdc5198a256c01c3dd6`
- cited in: node.lean, record TFQ-1260
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubBoundedMUFactor`): recorded sha256 `732189950dec5044fedb0f3b2f541e0eac714e3419099cdc5198a256c01c3dd6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubBoundedMUFactor`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_quartet_iff_reduced` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_quartet_iff_reduced` |

- counts toward the grade: yes

### Lean: `lean4/MubBoundedQuartetEquations.lean`

- file: [lean4/MubBoundedQuartetEquations.lean](../../../lean4/MubBoundedQuartetEquations.lean)
- sha256 (`bytes`): `7d37ce93c1612b0c6636c7111fb434a4e4149f8053b954b0c910692fbe2e467b`
- cited in: node.lean, record TFQ-1260
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubBoundedQuartetEquations`): recorded sha256 `7d37ce93c1612b0c6636c7111fb434a4e4149f8053b954b0c910692fbe2e467b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubBoundedQuartetEquations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_quartet_iff_equations` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_quartet_iff_equations` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1260_mub6_bounded_block_quartet_equations.md`

- file: [dag/derivations/25_mub/tfq_1260_mub6_bounded_block_quartet_equations.md](../../../dag/derivations/25_mub/tfq_1260_mub6_bounded_block_quartet_equations.md)
- sha256 (`lf-normalised`): `2736d8047d00a3f1471b19cb65ce33c1e9055ec31c688086e3f5def1e4444a11`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1260
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS` `DERIVED_LEAN`: [MUB6-CAUCHY-BINET-MINOR-BOUND](MUB6-CAUCHY-BINET-MINOR-BOUND.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-FINITE-CORNER-REDUCTION` `CONDITIONAL_ON_IMPORT`: [MUB6-FINITE-CORNER-REDUCTION](MUB6-FINITE-CORNER-REDUCTION.md) (IMPORTED_ASSUMPTION)
