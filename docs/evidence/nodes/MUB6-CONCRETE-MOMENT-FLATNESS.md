# MUB6-CONCRETE-MOMENT-FLATNESS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a supplied MUB family, a state v_{b0,l0} and a distinct basis b1, the complex word-moment matrices of degree one and two are Gram matrices, positive semidefinite, and of equal rank.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Forward theorem for moments induced by a supplied family; no reverse extraction from arbitrary positive flat data.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C30 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ConcreteMubMoments.lean`

- file: [lean4/ConcreteMubMoments.lean](../../../lean4/ConcreteMubMoments.lean)
- sha256 (`bytes`): `d21b5473fcf73cdebafb14c690c72615af4684ea945c419af18204784e85dd57`
- cited in: node.lean, record TFQ-1277
- replay: `none`
- check: `cd lean4 && lake build ConcreteMubMoments`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `complexMomentMatrix_eq_gram` | yes | yes | yes | - | `#print axioms complexMomentMatrix_eq_gram` |
| `complexMomentMatrix_posSemidef` | yes | yes | yes | - | `#print axioms complexMomentMatrix_posSemidef` |
| `concrete_mub_moment_flatness` | yes | yes | yes | - | `#print axioms concrete_mub_moment_flatness` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1277_mub6_concrete_moment_flatness.md`

- file: [dag/derivations/25_mub/tfq_1277_mub6_concrete_moment_flatness.md](../../../dag/derivations/25_mub/tfq_1277_mub6_concrete_moment_flatness.md)
- sha256 (`lf-normalised`): `e1a184e573575312c82d8667e493c522617249ffa91da5edd103c5547b4bb023`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1277
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

- `APP-R-MUB6-CONCRETE-MOMENT-FLATNESS` `DERIVED_LEAN`: [MUB6-CONCRETE-PROJECTORS](MUB6-CONCRETE-PROJECTORS.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-WORD-PROJECTOR-EXTRACTION` `DERIVED_LEAN`: [MUB6-WORD-PROJECTOR-EXTRACTION](MUB6-WORD-PROJECTOR-EXTRACTION.md) (PROVED_LEAN)
