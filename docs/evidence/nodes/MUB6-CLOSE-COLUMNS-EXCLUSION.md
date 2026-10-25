# MUB6-CLOSE-COLUMNS-EXCLUSION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the 386-coordinate system no solution has a column i of W_0 and a column j of W_1 whose six real parts lie in \[9/10, 11/10\] and whose imaginary parts lie within 1/20 of common centres, since sum_k |(W_0)_ki - (W_1)_kj|^2 = 72 - 12 Re(W_2)_ij \>= 43623/1024.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This excludes one family of regions; the full box remains unresolved and no complete cover is claimed.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-PAPER-CLOSE-COLUMNS claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubQuadraticTransitionSeparation.lean`

- file: [lean4/MubQuadraticTransitionSeparation.lean](../../../lean4/MubQuadraticTransitionSeparation.lean)
- sha256 (`bytes`): `3a85b6f0aeb2658077d77a0d8a0ef23a0be5e05765fd9e812409aea3bd25e61e`
- cited in: node.lean, record TFQ-1263
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubQuadraticTransitionSeparation`): recorded sha256 `3a85b6f0aeb2658077d77a0d8a0ef23a0be5e05765fd9e812409aea3bd25e61e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubQuadraticTransitionSeparation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `close_columns_box_excluded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms close_columns_box_excluded` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1263_mub6_close_columns_exclusion.md`

- file: [dag/derivations/25_mub/tfq_1263_mub6_close_columns_exclusion.md](../../../dag/derivations/25_mub/tfq_1263_mub6_close_columns_exclusion.md)
- sha256 (`lf-normalised`): `c1081b8c461c698cb8180fcb0302514733f56d9a68dbd838ffa6a318a52ce93c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1263
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-CLOSE-COLUMNS-EXCLUSION` `DERIVED_LEAN`: [MUB6-QUADRATIC-LIFT-386](MUB6-QUADRATIC-LIFT-386.md) (PROVED_LEAN)

Outgoing (0):

