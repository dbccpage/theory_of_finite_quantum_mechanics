# MUB6-CAUCHY-BINET-MINOR-BOUND

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Every 6x6 matrix H with unit-modulus entries and H H* = 6I has a 3x3 minor of its first three rows with |det|^2 \>= 54/5, which is invertible and whose inverse has squared entry moduli at most 10/27.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
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

The bound gives a chart, not nonextension; the selected minor need not be the external finite-corner minor.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C10 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubMinorChart.lean`

- file: [lean4/MubMinorChart.lean](../../../lean4/MubMinorChart.lean)
- sha256 (`bytes`): `3379f7033335fabf69871324b9aab57771e453d3e5e0843ca66d3fed594ea581`
- cited in: node.lean, record TFQ-1259
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MubMinorChart`): recorded sha256 `3379f7033335fabf69871324b9aab57771e453d3e5e0843ca66d3fed594ea581` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MubMinorChart`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_bounded_inverse_minor` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_bounded_inverse_minor` |
| `exists_minor_norm_ge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_minor_norm_ge` |
| `inverse_entry_normSq_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms inverse_entry_normSq_le` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1259_mub6_cauchy_binet_minor_bound.md`

- file: [dag/derivations/25_mub/tfq_1259_mub6_cauchy_binet_minor_bound.md](../../../dag/derivations/25_mub/tfq_1259_mub6_cauchy_binet_minor_bound.md)
- sha256 (`lf-normalised`): `2d2cf72a5120153187c879f28cb09899911e2af0281ad1b23e62fc1d3accaf4f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1259
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

- `APP-R-MUB6-CAUCHY-BINET-MINOR-BOUND` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS` `DERIVED_LEAN`: [MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS](MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS.md) (PROVED_LEAN)
