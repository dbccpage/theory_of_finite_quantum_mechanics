# FSP-PACHNER-INVARIANCE-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a discrete topological partition function on 4D triangulations is invariant under the 1-5, 2-4 and 3-3 Pachner moves; the source names no state-sum model, and the Regge action itself is not Pachner invariant.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fix a state-sum model (for example a Crane-Yetter type sum) and check its move invariance; nothing here bears on fermion signs.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-050 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md`

- file: [dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md](../../../dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md)
- sha256 (`lf-normalised`): `fa67a2e467d0c126ad137131c195a0696ccbba529bdf46c39524c64a7b82a393`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1214
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-PACHNER-INVARIANCE-CLAIM` `GAP_NO_DERIVATION`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)
