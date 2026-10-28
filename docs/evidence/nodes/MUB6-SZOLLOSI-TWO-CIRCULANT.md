# MUB6-SZOLLOSI-TWO-CIRCULANT

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For unit phase triples a, b with a0 a2* + a1 a0* + a2 a1* + b0 b2* + b1 b0* + b2 b1* = 0, the block matrix \[\[A, B\], \[B*, -A*\]\] of circulants has H H* = 6I and H/sqrt 6 is unitary with squared entry moduli 1/6; alpha is in both phase-sum images x + y + conj(xy) and -alpha iff some real solution of the six parameter equations has first phase sum alpha.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Transport to a dephased representative, classification of arbitrary CHM(6), the source cusp rank-degeneration claim, and Conjecture 3 (no quartet contains a family member) are not established.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-059 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6`
- cited in: node.lean, record TFQ-1228
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MasterClassification`): recorded sha256 `33931a23852e3d1a0743bc4a4c49dc07bac3a389f3a019b1c90cf244aacda0e6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `szollosiMatrix_isCH6` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms szollosiMatrix_isCH6` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiTwoCirculant.lean`

- file: [lean4/SzollosiTwoCirculant.lean](../../../lean4/SzollosiTwoCirculant.lean)
- sha256 (`bytes`): `3fbccf8c7db925ebb7701725fc57562ac29df7f2dfb63a78c385d121954b60ac`
- cited in: node.lean, record TFQ-1228
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiTwoCirculant`): recorded sha256 `3fbccf8c7db925ebb7701725fc57562ac29df7f2dfb63a78c385d121954b60ac` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiTwoCirculant`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalized_entry_modulus` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms normalized_entry_modulus` |
| `normalized_unitary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms normalized_unitary` |
| `parameter_covers_intersection` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms parameter_covers_intersection` |
| `rawSix_gram` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms rawSix_gram` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1228_mub6_szollosi_two_circulant.md`

- file: [dag/derivations/25_mub/tfq_1228_mub6_szollosi_two_circulant.md](../../../dag/derivations/25_mub/tfq_1228_mub6_szollosi_two_circulant.md)
- sha256 (`lf-normalised`): `54660a8d7271e4c61da27a5bab798009b9f8b472fa1ba88d3c200397a414b327`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1228
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `6708883b9f1ed33cc93d794d2c7c50484f0f8e075e4576c2eaa74fadf6fbf842`
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

- `APP-R-MUB6-SZOLLOSI-TWO-CIRCULANT` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (6):

- `APP-R-MUB6-COVER56-CURVATURE-PREMISE` `DERIVED_LEAN`: [MUB6-COVER56-CURVATURE-PREMISE](MUB6-COVER56-CURVATURE-PREMISE.md) (PROVED_LEAN)
- `APP-R-MUB6-CUSP-PUISEUX-CLAIM` `GAP_NO_DERIVATION`: [MUB6-CUSP-PUISEUX-CLAIM](MUB6-CUSP-PUISEUX-CLAIM.md) (OPEN)
- `APP-R-MUB6-DELTOID-COVER-BOX-DEFECT` `DERIVED_PROSE`: [MUB6-DELTOID-COVER-BOX-DEFECT](MUB6-DELTOID-COVER-BOX-DEFECT.md) (PROVED_PROSE)
- `APP-R-MUB6-RESIDUAL-FENCE-CLAIM` `GAP_NO_DERIVATION`: [MUB6-RESIDUAL-FENCE-CLAIM](MUB6-RESIDUAL-FENCE-CLAIM.md) (OPEN)
- `APP-R-MUB6-SZOLLOSI-618-SYSTEM` `DERIVED_LEAN`: [MUB6-SZOLLOSI-618-SYSTEM](MUB6-SZOLLOSI-618-SYSTEM.md) (PROVED_LEAN)
- `APP-R-MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS` `COMPUTED`: [MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS](MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS.md) (COMPUTATIONALLY_CHECKED)
