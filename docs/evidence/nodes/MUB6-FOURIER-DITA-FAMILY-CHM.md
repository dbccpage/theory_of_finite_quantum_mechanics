# MUB6-FOURIER-DITA-FAMILY-CHM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For unit phases a, b, c the explicit matrix fourierDitaMatrix(a,b,c), built from w = exp(2 pi i/3) blocks with rows signed by a, b, c, has unit-modulus entries and H H* = 6I.

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

The defect value 4 of F_6, the equivalence F_6 ~ F_2 tensor F_3, the Jaming et al. nonextension theorem for this family, and exhaustion of the Fourier orbit by the displayed matrices are cited or open, not formalized here.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-057 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6`
- cited in: node.lean, record TFQ-1226
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MasterClassification`): recorded sha256 `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fourierDitaMatrix_isCH6` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fourierDitaMatrix_isCH6` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1226_mub6_fourier_dita_family_chm.md`

- file: [dag/derivations/25_mub/tfq_1226_mub6_fourier_dita_family_chm.md](../../../dag/derivations/25_mub/tfq_1226_mub6_fourier_dita_family_chm.md)
- sha256 (`lf-normalised`): `d671d6177b7a8a5fd3b4ebd9c998c019e8d31ca0032d27f11834782058fee47c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1226
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

- `APP-R-MUB6-FOURIER-DITA-FAMILY-CHM` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-AFFINE-FIBER-THIRD-BASIS` `DERIVED_PROSE`: [MUB6-AFFINE-FIBER-THIRD-BASIS](MUB6-AFFINE-FIBER-THIRD-BASIS.md) (REFUTED)
