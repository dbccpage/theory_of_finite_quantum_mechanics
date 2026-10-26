# FSP-SIGN-ESTIMATOR-VARIANCE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For M_s independent samples from |W|/Z_abs, the sign mean has variance (1 - \<Sign\>^2)/M_s, so relative error epsilon needs M_s \>= (1 - \<Sign\>^2)/(epsilon^2 \<Sign\>^2); if \<Sign\> = exp(-beta N Delta f) this is Omega(exp(2 beta N Delta f)).

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

- independent sampling from the absolute-weight distribution (assumption)

## Bottleneck

Correlated Markov-chain samples, observable numerators and the extensive-gap hypothesis need separate treatment; this bound concerns direct reweighting only, not every estimator or representation.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-024 claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1190_fsp_sign_estimator_variance.md`

- file: [dag/derivations/26_fsp/tfq_1190_fsp_sign_estimator_variance.md](../../../dag/derivations/26_fsp/tfq_1190_fsp_sign_estimator_variance.md)
- sha256 (`lf-normalised`): `8bacf83482edb225ddb1e58afc2c705a59c8dfe66035fa9d64a7e206bdfbad67`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1190
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-SIGN-ESTIMATOR-VARIANCE` `DERIVED_PROSE`: [FSP-AVERAGE-SIGN-DEFINITION](FSP-AVERAGE-SIGN-DEFINITION.md) (DEFINITION)

Outgoing (1):

- `APP-R-FSP-TROYER-WIESE-REDUCTION` `CONDITIONAL_ON_IMPORT`: [FSP-TROYER-WIESE-REDUCTION](FSP-TROYER-WIESE-REDUCTION.md) (IMPORTED_ASSUMPTION)
