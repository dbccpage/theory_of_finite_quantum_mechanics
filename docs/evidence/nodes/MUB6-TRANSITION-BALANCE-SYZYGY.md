# MUB6-TRANSITION-BALANCE-SYZYGY

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For 6x6 matrices A, B over a commutative star ring with W = A* B, sum_k W_jk - 6 equals an explicit combination of the row-Gram residuals of B and the first-row gauge residuals of A and B, with a conjugate column identity; on solutions all row and column sums of W are six.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

An ideal-membership redundancy only; it gives no Jacobian rank or nonextension result.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-PAPER-BALANCE-SYZYGY claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubGaugeSyzygy.lean`

- file: [lean4/MubGaugeSyzygy.lean](../../../lean4/MubGaugeSyzygy.lean)
- sha256 (`bytes`): `f2596552a3a94f1ab0410172a31ae89a9ce480f5e9fb716104f04d8382bc9b7b`
- cited in: node.lean, record TFQ-1265
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubGaugeSyzygy`): recorded sha256 `f2596552a3a94f1ab0410172a31ae89a9ce480f5e9fb716104f04d8382bc9b7b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubGaugeSyzygy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `balanceResidual_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms balanceResidual_zero` |
| `column_balance_syzygy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms column_balance_syzygy` |
| `row_balance_syzygy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms row_balance_syzygy` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1265_mub6_transition_balance_syzygy.md`

- file: [dag/derivations/25_mub/tfq_1265_mub6_transition_balance_syzygy.md](../../../dag/derivations/25_mub/tfq_1265_mub6_transition_balance_syzygy.md)
- sha256 (`lf-normalised`): `d8e7470cfc639794ff33f8df888b2b577a6921d9692a13ac56f4670f591e518d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1265
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-TRANSITION-BALANCE-SYZYGY` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

