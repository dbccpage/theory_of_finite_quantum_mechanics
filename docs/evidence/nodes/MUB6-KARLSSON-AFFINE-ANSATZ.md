# MUB6-KARLSSON-AFFINE-ANSATZ

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For unit phases x, y the explicit matrix karlssonMatrix(x,y), with rows built from +-1, w, w^2 (w = exp(2 pi i/3)) and the phases x, y, has unit-modulus entries and H H* = 6I.

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

No equivalence to the full three-parameter Karlsson family is supplied; the source claim that the CHM(6) moduli space has real dimension at most 4 with a finite chart cover is open.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-060 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `cbfd11e4e0038f1a3deb5c51c8079d1c28f7e5fad3d189b3296239b50507ccc3`
- cited in: node.lean, record TFQ-1229
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MasterClassification`): recorded sha256 `cbfd11e4e0038f1a3deb5c51c8079d1c28f7e5fad3d189b3296239b50507ccc3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `karlssonMatrix_isCH6` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms karlssonMatrix_isCH6` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1229_mub6_karlsson_affine_ansatz.md`

- file: [dag/derivations/25_mub/tfq_1229_mub6_karlsson_affine_ansatz.md](../../../dag/derivations/25_mub/tfq_1229_mub6_karlsson_affine_ansatz.md)
- sha256 (`lf-normalised`): `2f728561f6a591578fb897d66168242f89620ee4aa2844d5bb96344e48487444`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1229
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

- `APP-R-MUB6-KARLSSON-AFFINE-ANSATZ` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

