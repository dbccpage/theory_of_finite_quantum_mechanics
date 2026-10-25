# MUB6-WORD-PROJECTOR-EXTRACTION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> From normalized word values with positive semidefinite degree-two moments of the same rank as degree one and contextual idempotence equations, one constructs a space of dimension rank M_1, a normalized state and symmetric idempotent actions reproducing all degree-two moments; with contextual same-basis and completeness relations they form orthogonal resolutions of I.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

Dimension six, nonzero rank-one outcomes, cross-basis MU conclusions and transport to the coordinate variety are not derived for arbitrary word data.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C32 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FlatMomentBasisRelations.lean`

- file: [lean4/FlatMomentBasisRelations.lean](../../../lean4/FlatMomentBasisRelations.lean)
- sha256 (`bytes`): `bf4ba4e84287be003d95729e6ce870b0189bb1c6b9b7a733720e9df3c4470ec8`
- cited in: node.lean, record TFQ-1278
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `FlatMomentBasisRelations`): recorded sha256 `bf4ba4e84287be003d95729e6ce870b0189bb1c6b9b7a733720e9df3c4470ec8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FlatMomentBasisRelations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `extract_word_basis` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms extract_word_basis` |
| `zero_action_moments_reject_completeness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms zero_action_moments_reject_completeness` |

- counts toward the grade: yes

### Lean: `lean4/FlatMomentProjectorExtraction.lean`

- file: [lean4/FlatMomentProjectorExtraction.lean](../../../lean4/FlatMomentProjectorExtraction.lean)
- sha256 (`bytes`): `46a1f2c66be5cc14899da49af63a0c3ae7d41a79260dbda333016f7e60e0c6fc`
- cited in: node.lean, record TFQ-1278
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `FlatMomentProjectorExtraction`): recorded sha256 `46a1f2c66be5cc14899da49af63a0c3ae7d41a79260dbda333016f7e60e0c6fc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FlatMomentProjectorExtraction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `extract_word_projectors` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms extract_word_projectors` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1278_mub6_word_projector_extraction.md`

- file: [dag/derivations/25_mub/tfq_1278_mub6_word_projector_extraction.md](../../../dag/derivations/25_mub/tfq_1278_mub6_word_projector_extraction.md)
- sha256 (`lf-normalised`): `7afdd7025df1b5c972eb1079887d55dbd8c7fef209a176bbbe969bbada2c284d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1278
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

- `APP-R-MUB6-WORD-PROJECTOR-EXTRACTION` `DERIVED_LEAN`: [MUB6-CONCRETE-MOMENT-FLATNESS](MUB6-CONCRETE-MOMENT-FLATNESS.md) (PROVED_LEAN)

Outgoing (0):

