# MUB6-ROUTE-C-CONDITIONAL

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over the opaque interface types Basis and is_mutually_unbiased, the premise that every pairwise MU seven-basis family contains a triple in InFourierDitaChart implies NoCompleteMUB6; so does a landing map CompleteMUB6 -\> RouteCCompleteMUBFamily.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- FourierTripleLandingPremise (open)
- InFourierDitaChart certified-domain membership with analytic soundness of the global partition tree (supplied)
- Concrete interpretation of the opaque Basis and MU predicates (absent)

## Bottleneck

Discharge the landing premise from concrete complex MU data and give the opaque Basis type a concrete interpretation; earlier unconditional Route C statements are withdrawn.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C05 claims CONDITIONAL; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RouteCFourierLandingBypass.lean`

- file: [lean4/RouteCFourierLandingBypass.lean](../../../lean4/RouteCFourierLandingBypass.lean)
- sha256 (`bytes`): `5995fdeb97e3357af1d91ebc67f5b14a573468c58480c748fef5e805fc87c149`
- cited in: node.lean, record TFQ-1257
- replay: `none`
- check: `cd lean4 && lake build RouteCFourierLandingBypass`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_complete_mub6_of_fourier_triple_landing` | yes | yes | yes | - | `#print axioms no_complete_mub6_of_fourier_triple_landing` |
| `no_complete_mub6_via_route_c` | yes | yes | yes | - | `#print axioms no_complete_mub6_via_route_c` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1257_mub6_route_c_conditional.md`

- file: [dag/derivations/25_mub/tfq_1257_mub6_route_c_conditional.md](../../../dag/derivations/25_mub/tfq_1257_mub6_route_c_conditional.md)
- sha256 (`lf-normalised`): `627169b5e5b3ab062e33c354a572b7b3a2847dd222c6cd2e9c79d423c155f446`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1257
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

- `APP-R-MUB6-ROUTE-C-CONDITIONAL` `CONDITIONAL_ON_IMPORT`: [MUB6-GLUING-G3-OPAQUE](MUB6-GLUING-G3-OPAQUE.md) (PROVED_LEAN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (1):

- `APP-R-MUB6-ROUTE-C-LANDING-CLAIM` `GAP_NO_DERIVATION`: [MUB6-ROUTE-C-LANDING-CLAIM](MUB6-ROUTE-C-LANDING-CLAIM.md) (OPEN)
