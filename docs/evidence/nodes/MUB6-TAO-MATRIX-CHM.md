# MUB6-TAO-MATRIX-CHM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Tao matrix S6 with entries in {1, w, w^2}, w = exp(2 pi i/3), has unit-modulus entries and S6 S6* = 6I.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: stale 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `receipt_not_current`: lean4/MasterClassification.lean: replay stale against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

None recorded.

## Bottleneck

The source claims that S6 is isolated and that the CHM(6) moduli space is disconnected are cited literature facts, not formalized here.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-061 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6`
- cited in: node.lean, record TFQ-1230
- replay: `stale`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MasterClassification`): recorded sha256 `cbfd11e4e0038f1a3deb5c51c8079d1c28f7e5fad3d189b3296239b50507ccc3` differs from the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `taoMatrix_isCH6` | yes | yes | yes | - | `#print axioms taoMatrix_isCH6` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1230_mub6_tao_matrix_chm.md`

- file: [dag/derivations/25_mub/tfq_1230_mub6_tao_matrix_chm.md](../../../dag/derivations/25_mub/tfq_1230_mub6_tao_matrix_chm.md)
- sha256 (`lf-normalised`): `2dc8079fd2bc30078876c7545194c9e3f31681df64c8701dcd26ca25379d3f44`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1230
- counts toward the grade: no

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

- `APP-R-MUB6-TAO-MATRIX-CHM` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-MUB6-CONJECTURE2-PREMISE` `GAP_NO_DERIVATION`: [MUB6-CONJECTURE2-PREMISE](MUB6-CONJECTURE2-PREMISE.md) (OPEN)
- `APP-R-MUB6-TAO-LAURENT-NORM-NINE` `DERIVED_LEAN`: [MUB6-TAO-LAURENT-NORM-NINE](MUB6-TAO-LAURENT-NORM-NINE.md) (PROVED_LEAN)
