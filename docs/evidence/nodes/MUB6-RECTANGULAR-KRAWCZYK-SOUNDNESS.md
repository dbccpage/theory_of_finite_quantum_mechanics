# MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For finite quadratic coded rows, a box containing the rational centre and any rational preconditioner, every zero in the box lies in the rectangular Krawczyk image, and a successful strict coordinate-separation check excludes all zeros in the box.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Soundness only: no successful check on a quartet domain is supplied, and strict inclusion gives no root conclusion for overdetermined systems.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C25 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RectangularQuadraticExclusion.lean`

- file: [lean4/RectangularQuadraticExclusion.lean](../../../lean4/RectangularQuadraticExclusion.lean)
- sha256 (`bytes`): `e7723f9114caacc35e8ada60c9b8295edf87c094b86ec83612c4916d4a98fccf`
- cited in: node.lean, record TFQ-1271
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `RectangularQuadraticExclusion`): recorded sha256 `e7723f9114caacc35e8ada60c9b8295edf87c094b86ec83612c4916d4a98fccf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RectangularQuadraticExclusion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exclusion_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exclusion_sound` |
| `list_secant_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms list_secant_identity` |
| `root_in_image` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms root_in_image` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiRectangularExclusion.lean`

- file: [lean4/SzollosiRectangularExclusion.lean](../../../lean4/SzollosiRectangularExclusion.lean)
- sha256 (`bytes`): `0709a45031ecb050772d9e52a57a7d6068b7f4aeea6fa712ad9374390c924173`
- cited in: node.lean, record TFQ-1271
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiRectangularExclusion`): recorded sha256 `0709a45031ecb050772d9e52a57a7d6068b7f4aeea6fa712ad9374390c924173` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiRectangularExclusion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_quartet_of_check` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_quartet_of_check` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1271_mub6_rectangular_krawczyk_soundness.md`

- file: [dag/derivations/25_mub/tfq_1271_mub6_rectangular_krawczyk_soundness.md](../../../dag/derivations/25_mub/tfq_1271_mub6_rectangular_krawczyk_soundness.md)
- sha256 (`lf-normalised`): `7a5578cf976e1fb40df1867757a4ec9c4cc02f137644e7893148b711a8f46d04`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1271
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

- `APP-R-MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS` `DERIVED_LEAN`: [MUB6-SZOLLOSI-618-SYSTEM](MUB6-SZOLLOSI-618-SYSTEM.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM` `GAP_NO_DERIVATION`: [MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM](MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM.md) (OPEN)
- `APP-R-MUB6-SZOLLOSI-FULLBOX-UNRESOLVED` `COMPUTED`: [MUB6-SZOLLOSI-FULLBOX-UNRESOLVED](MUB6-SZOLLOSI-FULLBOX-UNRESOLVED.md) (COMPUTATIONALLY_CHECKED)
