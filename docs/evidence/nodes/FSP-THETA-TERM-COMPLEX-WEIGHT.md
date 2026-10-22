# FSP-THETA-TERM-COMPLEX-WEIGHT

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Adding S_theta = i theta Q_top with real lattice charge Q_top multiplies the Boltzmann weight by exp(-i theta Q_top), which is nonreal unless theta Q_top lies in pi Z for every configuration, so positive-weight importance sampling is lost for generic theta != 0.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- lattice topological charge Q_top and theta vacuum term (standard)

## Bottleneck

Severity of the resulting sign problem is phenomenology from the literature; the checkout has no theta-term model.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-034 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md`

- file: [dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md](../../../dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md)
- sha256 (`lf-normalised`): `a1f146ef22167ae88cdbe416433f8f44bfe77aec1b0b2dca2cccc68610836b93`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1198
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-THETA-TERM-COMPLEX-WEIGHT` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

