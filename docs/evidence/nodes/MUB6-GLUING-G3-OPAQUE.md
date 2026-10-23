# MUB6-GLUING-G3-OPAQUE

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For opaque Basis and MU predicates, every constituent triple of a pairwise MU seven-basis family has a fourth MU basis in the family, and if no MU triple has a fourth MU basis then no MU four-basis family exists.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Combinatorial facts over uninterpreted predicates; a concrete interpretation in complex matrices is needed before they apply to C^6.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-LEDGER-G3-GLUING claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Gluing.lean`

- file: [lean4/Gluing.lean](../../../lean4/Gluing.lean)
- sha256 (`bytes`): `bc1f160caa99139792dfb8b769a913dd1f713fdc5012ce66ab697895b5ac5b73`
- cited in: node.lean, record TFQ-1258
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `Gluing`): recorded sha256 `bc1f160caa99139792dfb8b769a913dd1f713fdc5012ce66ab697895b5ac5b73` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build Gluing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `g3_theorem` | yes | yes | yes | propext | `#print axioms g3_theorem` |
| `no_four_mub6_of_no_triple_extension` | yes | yes | yes | propext | `#print axioms no_four_mub6_of_no_triple_extension` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1258_mub6_gluing_g3_opaque.md`

- file: [dag/derivations/25_mub/tfq_1258_mub6_gluing_g3_opaque.md](../../../dag/derivations/25_mub/tfq_1258_mub6_gluing_g3_opaque.md)
- sha256 (`lf-normalised`): `e3d904d32a7cc24c47243ae85a9f195eb9c76323fec21bbe9cc1f29c240b646a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1258
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-GLUING-G3-OPAQUE` `DERIVED_LEAN`: [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (2):

- `APP-R-MUB6-PSI-GLUING-CLAIM` `GAP_NO_DERIVATION`: [MUB6-PSI-GLUING-CLAIM](MUB6-PSI-GLUING-CLAIM.md) (OPEN)
- `APP-R-MUB6-ROUTE-C-CONDITIONAL` `CONDITIONAL_ON_IMPORT`: [MUB6-ROUTE-C-CONDITIONAL](MUB6-ROUTE-C-CONDITIONAL.md) (CONDITIONAL)
