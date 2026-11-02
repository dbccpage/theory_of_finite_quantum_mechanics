# FSP-FRACTON-MOBILITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the X-cube model isolated fractons are immobile, fracton dipoles move within planes (planons) and lineons move only along lattice axes.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- X-cube excitation mobility (literature)

## Bottleneck

The claim that these constraints suppress sign-inducing braids has no evidence here and is left open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-054 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1218_fsp_fracton_mobility.md`

- file: [dag/derivations/26_fsp/tfq_1218_fsp_fracton_mobility.md](../../../dag/derivations/26_fsp/tfq_1218_fsp_fracton_mobility.md)
- sha256 (`lf-normalised`): `179498a884b3207743f3f449aea5a00cd1a855bb88571f2608637ad6d6aae87e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1218
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `5f5dfaa7a3794d1fee0299865df221b6db1c14ebf6f3925b1729e784a28e3194`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-FRACTON-MOBILITY` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-HINGE-LINEON-SIGN-CLAIM` `COMPUTED`: [FSP-HINGE-LINEON-SIGN-CLAIM](FSP-HINGE-LINEON-SIGN-CLAIM.md) (COMPUTATIONALLY_CHECKED)
