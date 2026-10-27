# MUB6-HAAGERUP-MATRIX-CHM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The explicit 6x6 matrix haagerupMatrix with entries in {1, -1, i} has unit-modulus entries and H H* = 6I.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

The source one-parameter family H6(q) without 2x2 or 3x3 Hadamard sub-blocks is not constructed; matching this matrix to the Haagerup source and to any exclusion theorem is an open step.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-058 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6`
- cited in: node.lean, record TFQ-1227
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MasterClassification`): recorded sha256 `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `haagerupMatrix_isCH6` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms haagerupMatrix_isCH6` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md`

- file: [dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md](../../../dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md)
- sha256 (`lf-normalised`): `ddeb32d44f6a62e96bb153f3a052348bd6d8967aaa4c4bc383035d055b47d8e3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1227
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `b515bf981d6c3a339c2b0a7937d54d9deb05f3b53186c584b83f5fa3419dc902`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-HAAGERUP-MATRIX-CHM` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

