# MUB6-FOURTH-BASIS-FLAT-MOMENTS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a fixed triple T, a fourth basis exists iff some normalized real moment functional has positive semidefinite degree-two moment matrix, equal degree-two and degree-one ranks, and finite relation compatibility with all 180 residuals.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This restates the problem as an equivalent moment question without deciding it; nonflat truncations are not addressed.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C36 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ConcreteMubFlatExtension.lean`

- file: [lean4/ConcreteMubFlatExtension.lean](../../../lean4/ConcreteMubFlatExtension.lean)
- sha256 (`bytes`): `d953e80582cc32abe39d7a40690d11a968e5d198a2f20195f7d3455646e55c00`
- cited in: node.lean, record TFQ-1281
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `ConcreteMubFlatExtension`): recorded sha256 `d953e80582cc32abe39d7a40690d11a968e5d198a2f20195f7d3455646e55c00` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ConcreteMubFlatExtension`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fourth_basis_iff_positive_flat_moments` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fourth_basis_iff_positive_flat_moments` |
| `fourth_basis_of_positive_flat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fourth_basis_of_positive_flat` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1281_mub6_fourth_basis_flat_moments.md`

- file: [dag/derivations/25_mub/tfq_1281_mub6_fourth_basis_flat_moments.md](../../../dag/derivations/25_mub/tfq_1281_mub6_fourth_basis_flat_moments.md)
- sha256 (`lf-normalised`): `00fc011d18c36cca96b214de1ea20ad4dc23e74616221731e46c730529ec4bcc`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1281
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-FOURTH-BASIS-FLAT-MOMENTS` `DERIVED_LEAN`: [MUB6-COMMUTATIVE-FLAT-REAL-POINT](MUB6-COMMUTATIVE-FLAT-REAL-POINT.md) (PROVED_LEAN), [MUB6-FIXED-TRIPLE-VARIETY](MUB6-FIXED-TRIPLE-VARIETY.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-EMPTY-VARIETY-MOMENT-NONPSD` `DERIVED_LEAN`: [MUB6-EMPTY-VARIETY-MOMENT-NONPSD](MUB6-EMPTY-VARIETY-MOMENT-NONPSD.md) (PROVED_LEAN)
