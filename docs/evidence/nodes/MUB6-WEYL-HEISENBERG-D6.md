# MUB6-WEYL-HEISENBERG-D6

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On C^6 with shift X|j\> = |j+1 mod 6\> and clock Z|j\> = w^j |j\>, w = exp(2 pi i/6), one has Z X = w X Z, and the 36 operators X^p Z^q are pairwise orthogonal for the trace pairing tr(A* B).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Complex exponential and its identification with the integer pair w (not constructed in this checkout)

## Bottleneck

This record is the 6 by 6 integer-pair table above. It does not construct a complex exponential, does not identify w with exp(2 pi i / 6), and does not count mutually unbiased bases. The source commutation X Z = w Z X is the opposite clock convention. AuthorityEffect: None.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-053 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Mub6WeylHeisenbergD6.lean`

- file: [lean4/Mub6WeylHeisenbergD6.lean](../../../lean4/Mub6WeylHeisenbergD6.lean)
- sha256 (`bytes`): `564ce28dadfd8bf892353d8c1b2dd302e67af184f69c8a42d9140909f4fb4279`
- cited in: node.lean, receipt dag/research/campaign_mub6-weyl-heisenberg-d6_lean_replay.json (Mub6WeylHeisenbergD6), record TFQ-1223
- replay: `verified`
  - receipt [dag/research/campaign_mub6-weyl-heisenberg-d6_lean_replay.json](../../../dag/research/campaign_mub6-weyl-heisenberg-d6_lean_replay.json) (module `Mub6WeylHeisenbergD6`): recorded sha256 `564ce28dadfd8bf892353d8c1b2dd302e67af184f69c8a42d9140909f4fb4279` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Mub6WeylHeisenbergD6`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `clock_entry` | yes | yes | yes | propext | `#print axioms clock_entry` |
| `conj_pair` | yes | yes | yes | none | `#print axioms conj_pair` |
| `hs_orth` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms hs_orth` |
| `shift_entry` | yes | yes | yes | propext | `#print axioms shift_entry` |
| `w_cube` | yes | yes | yes | none | `#print axioms w_cube` |
| `w_six` | yes | yes | yes | none | `#print axioms w_six` |
| `w_sq` | yes | yes | yes | none | `#print axioms w_sq` |
| `xz_ne` | yes | yes | yes | propext | `#print axioms xz_ne` |
| `zx_eq` | yes | yes | yes | propext | `#print axioms zx_eq` |

- counts toward the grade: yes

### Python: `checks/independent/mub6-weyl-heisenberg-d6.py`

- file: [checks/independent/mub6-weyl-heisenberg-d6.py](../../../checks/independent/mub6-weyl-heisenberg-d6.py)
- sha256 (`bytes`): `be2f11c024631e0f2d30c198d0e72fb0386e339ad74dc4cf99ce8eac7d372b3f`
- cited in: record TFQ-1223

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md`

- file: [dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md](../../../dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md)
- sha256 (`lf-normalised`): `64a03449e0daf576f84aa0c47cdc7cf86a7f81e357324920748c68286d88134f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1223
- counts toward the grade: no

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

- `APP-R-MUB6-WEYL-HEISENBERG-D6` `CONDITIONAL_ON_IMPORT`: [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-WEYL-STABILIZER-BOUND` `GAP_NO_DERIVATION`: [MUB6-WEYL-STABILIZER-BOUND](MUB6-WEYL-STABILIZER-BOUND.md) (OPEN)
