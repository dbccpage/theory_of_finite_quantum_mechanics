# MUB6-MOMENT-EVALUATION-FLAT

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any real point x, the evaluation functional p -\> p(x) is normalized, its degree-two coordinate moment matrix is positive semidefinite, and its degree-two and degree-one moment ranks are equal.

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

This is the necessity direction only; the source Lasserre hierarchy at every order t is not formalized, and feasibility of a relaxation gives no solution without flatness and compatibility.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-069 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CommutativeFlatMoments.lean`

- file: [lean4/CommutativeFlatMoments.lean](../../../lean4/CommutativeFlatMoments.lean)
- sha256 (`bytes`): `a093bd73ebaa1453cd2c08d014f9f5dbeca97f0b254c1e0a8f130deaa79677ea`
- cited in: node.lean, record TFQ-1251
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `CommutativeFlatMoments`): recorded sha256 `a093bd73ebaa1453cd2c08d014f9f5dbeca97f0b254c1e0a8f130deaa79677ea` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CommutativeFlatMoments`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluation_moment_positive_flat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms evaluation_moment_positive_flat` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1251_mub6_moment_evaluation_flat.md`

- file: [dag/derivations/25_mub/tfq_1251_mub6_moment_evaluation_flat.md](../../../dag/derivations/25_mub/tfq_1251_mub6_moment_evaluation_flat.md)
- sha256 (`lf-normalised`): `d5e1bbc6a98928cd8c7b671faff4fa0c18f8ddf3e6edeabbc742f25f7e68d0e4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1251
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `79a8e74d457a2c236999a6a1dcd1ff010f0f878b245c205f5f049add18ae2234`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `4df95e7f697d7ab11bfa44f282353267197198f74bcfb535e5f10c18ffbeabf5`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-MOMENT-EVALUATION-FLAT` `DERIVED_LEAN`: [MUB6-FIXED-TRIPLE-VARIETY](MUB6-FIXED-TRIPLE-VARIETY.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-MUB6-COMMUTATIVE-FLAT-REAL-POINT` `DERIVED_LEAN`: [MUB6-COMMUTATIVE-FLAT-REAL-POINT](MUB6-COMMUTATIVE-FLAT-REAL-POINT.md) (PROVED_LEAN)
- `APP-R-MUB6-DEGREE2-SDP-GAP-CLAIM` `GAP_NO_DERIVATION`: [MUB6-DEGREE2-SDP-GAP-CLAIM](MUB6-DEGREE2-SDP-GAP-CLAIM.md) (OPEN)
- `APP-R-MUB6-FLAT-EXTENSION-FAILURE-CLAIM` `GAP_NO_DERIVATION`: [MUB6-FLAT-EXTENSION-FAILURE-CLAIM](MUB6-FLAT-EXTENSION-FAILURE-CLAIM.md) (OPEN)
