# MUB6-FINITE-CORNER-REDUCTION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Using the external finite-corner classification of single 6x6 complex Hadamard matrices, quartet existence in C^6 is equivalent to raw quartet completion of some retained finite-corner reconstruction with D = -C E* (B^-1)*.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Cardenes Wuttig and Tindall, finite-corner classification of CHM(6), arXiv:2608.18053v2, external Lean pin 57b03025

## Bottleneck

This record is that one integer block identity. It does not classify complex Hadamard matrices, does not list retained finite corners, and does not equate quartet existence with completion of an external reconstruction. The complex adjoint is not identified with this integer transpose. Exclusion over every retained reconstruction stays open. AuthorityEffect: None.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-PAPER-FINITE-CORNER claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMub6FiniteCornerReduction.lean`

- file: [lean4/CampaignMub6FiniteCornerReduction.lean](../../../lean4/CampaignMub6FiniteCornerReduction.lean)
- sha256 (`bytes`): `79d7009cc56587e368459720d501a80ae327f07cd87206aeb526161856964401`
- cited in: node.lean, receipt dag/research/campaign_mub6-finite-corner-reduction_lean_replay.json (CampaignMub6FiniteCornerReduction), record TFQ-1261
- replay: `verified`
  - receipt [dag/research/campaign_mub6-finite-corner-reduction_lean_replay.json](../../../dag/research/campaign_mub6-finite-corner-reduction_lean_replay.json) (module `CampaignMub6FiniteCornerReduction`): recorded sha256 `79d7009cc56587e368459720d501a80ae327f07cd87206aeb526161856964401` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMub6FiniteCornerReduction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `b_inv_left` | yes | yes | yes | Quot.sound, propext | `#print axioms b_inv_left` |
| `b_inv_right` | yes | yes | yes | Quot.sound, propext | `#print axioms b_inv_right` |
| `cross_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms cross_zero` |
| `d_formula` | yes | yes | yes | Quot.sound, propext | `#print axioms d_formula` |
| `zero_cross_ne` | yes | yes | yes | propext | `#print axioms zero_cross_ne` |

- counts toward the grade: yes

### Python: `checks/independent/mub6-finite-corner-reduction.py`

- file: [checks/independent/mub6-finite-corner-reduction.py](../../../checks/independent/mub6-finite-corner-reduction.py)
- sha256 (`bytes`): `3bcf96d6a717db0ee88a94c51c52ccc3241bae29957cdb7f4e16473c5d34cfb2`
- cited in: record TFQ-1261

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md`

- file: [dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md](../../../dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md)
- sha256 (`lf-normalised`): `0c24a970b0b32ff5761cfc2d085886f309ffc7c9646de253ca766f0f0ea4539d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1261
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-FINITE-CORNER-REDUCTION` `CONDITIONAL_ON_IMPORT`: [MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS](MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS.md) (PROVED_LEAN)

Outgoing (0):

