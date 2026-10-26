# MUB6-ROUTE-C-LABEL-ARITHMETIC

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For natural numbers with 6 = n_D + n_T + n_S + n_H, n_T + n_S \<= 1 and n_H \<= 0, one has n_D \>= 5, C(n_D,2) \>= 10 and n_D + C(n_D,2) \>= 15.

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

These are label counts in MUB6OrbitConfiguration; the structure has no matrices and no map from counts to Fourier transition edges.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C01 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RouteCFourierLandingBypass.lean`

- file: [lean4/RouteCFourierLandingBypass.lean](../../../lean4/RouteCFourierLandingBypass.lean)
- sha256 (`bytes`): `5995fdeb97e3357af1d91ebc67f5b14a573468c58480c748fef5e805fc87c149`
- cited in: node.lean, record TFQ-1256
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `RouteCFourierLandingBypass`): recorded sha256 `5995fdeb97e3357af1d91ebc67f5b14a573468c58480c748fef5e805fc87c149` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RouteCFourierLandingBypass`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fourier_count_ge_five` | yes | yes | yes | Quot.sound, propext | `#print axioms fourier_count_ge_five` |
| `fourier_landing_edges_lower_bound` | yes | yes | yes | Quot.sound, propext | `#print axioms fourier_landing_edges_lower_bound` |
| `fourier_pairs_ge_ten` | yes | yes | yes | Quot.sound, propext | `#print axioms fourier_pairs_ge_ten` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1256_mub6_route_c_label_arithmetic.md`

- file: [dag/derivations/25_mub/tfq_1256_mub6_route_c_label_arithmetic.md](../../../dag/derivations/25_mub/tfq_1256_mub6_route_c_label_arithmetic.md)
- sha256 (`lf-normalised`): `44bc5183caaf37f40a807ae7e1e05fba4f9efdcaf0ed00f58f7f18002d0e6cae`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1256
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-ROUTE-C-LABEL-ARITHMETIC` `DERIVED_LEAN`: [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (0):

