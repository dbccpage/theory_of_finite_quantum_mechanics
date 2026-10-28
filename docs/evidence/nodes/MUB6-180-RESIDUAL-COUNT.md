# MUB6-180-RESIDUAL-COUNT

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fixed-triple system indexes exactly 180 real constraints in 72 coordinates: 108 MU residuals (36 per basis of the triple) and 72 real and imaginary components of U* U - I; the count is not an independence or dimension claim.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
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

The source split (36 normalization, 36 against I_6, 108 against F_6 and B_3) does not match the Lean indexing; no rank or overdetermination statement is established.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-065 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ConcreteMubPolynomials.lean`

- file: [lean4/ConcreteMubPolynomials.lean](../../../lean4/ConcreteMubPolynomials.lean)
- sha256 (`bytes`): `bbb3720eb5391c9fdd3ac7f2781cff250dde03931f564befc2472e7c92080955`
- cited in: node.lean, record TFQ-1234
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `ConcreteMubPolynomials`): recorded sha256 `bbb3720eb5391c9fdd3ac7f2781cff250dde03931f564befc2472e7c92080955` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ConcreteMubPolynomials`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `coordinate_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms coordinate_count` |
| `mu_equation_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms mu_equation_count` |
| `total_equation_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms total_equation_count` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1234_mub6_180_residual_count.md`

- file: [dag/derivations/25_mub/tfq_1234_mub6_180_residual_count.md](../../../dag/derivations/25_mub/tfq_1234_mub6_180_residual_count.md)
- sha256 (`lf-normalised`): `6b3ca8cc846a8dee5869bfb5f1ff19c047b914acc44fd11e32991731f7acfc05`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1234
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

- `APP-R-MUB6-180-RESIDUAL-COUNT` `DERIVED_LEAN`: [MUB6-FIXED-TRIPLE-VARIETY](MUB6-FIXED-TRIPLE-VARIETY.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-MUB6-GRAM-NULLSTELLENSATZ-CLAIM` `GAP_NO_DERIVATION`: [MUB6-GRAM-NULLSTELLENSATZ-CLAIM](MUB6-GRAM-NULLSTELLENSATZ-CLAIM.md) (OPEN)
- `APP-R-MUB6-GROEBNER-ELIMINATION-CLAIM` `GAP_NO_DERIVATION`: [MUB6-GROEBNER-ELIMINATION-CLAIM](MUB6-GROEBNER-ELIMINATION-CLAIM.md) (OPEN)
- `APP-R-MUB6-TORUS-CAD-EMPTINESS-CLAIM` `GAP_NO_DERIVATION`: [MUB6-TORUS-CAD-EMPTINESS-CLAIM](MUB6-TORUS-CAD-EMPTINESS-CLAIM.md) (OPEN)
