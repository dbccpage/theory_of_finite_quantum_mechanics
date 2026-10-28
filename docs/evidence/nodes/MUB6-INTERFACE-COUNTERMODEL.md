# MUB6-INTERFACE-COUNTERMODEL

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The legacy projector-realization interface has a zero-action model on a Boolean carrier for every size label, so the interface-level exclusion predicate is false for every number of bases and dimension.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The interface lacks completeness, rank-one, dimension, linearity and cross-basis MU constraints; exclusions stated over it do not express the physical theorem.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C34 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MomentPositivityObligation.lean`

- file: [lean4/MomentPositivityObligation.lean](../../../lean4/MomentPositivityObligation.lean)
- sha256 (`bytes`): `2e30aeed4fb8b3bf7b2ac1a7d033d7ddca6d3f038918499779b27757420c1632`
- cited in: node.lean, record TFQ-1279
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MomentPositivityObligation`): recorded sha256 `2e30aeed4fb8b3bf7b2ac1a7d033d7ddca6d3f038918499779b27757420c1632` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build MomentPositivityObligation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `not_universal_interface_exclusion` | yes | yes | yes | none | `#print axioms not_universal_interface_exclusion` |
| `zeroActionInterfaceModel` | yes | yes | yes | none | `#print axioms zeroActionInterfaceModel` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1279_mub6_interface_countermodel.md`

- file: [dag/derivations/25_mub/tfq_1279_mub6_interface_countermodel.md](../../../dag/derivations/25_mub/tfq_1279_mub6_interface_countermodel.md)
- sha256 (`lf-normalised`): `4909aa1fa31306fa76d1344f2a5a190516a5b232d440936560623cc6bdfcc549`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1279
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

## Routes

Incoming (1):

- `APP-R-MUB6-INTERFACE-COUNTERMODEL` `DERIVED_LEAN`: [MUB6-FLAT-EXTENSION-FAILURE-CLAIM](MUB6-FLAT-EXTENSION-FAILURE-CLAIM.md) (OPEN)

Outgoing (0):

