# FSP-AVERAGE-SIGN-DEFINITION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a declared path representation with weights W(c), \<Sign\> = Z / Z_abs with Z = sum sigma(c)|W(c)| and Z_abs = sum |W(c)|; when Z \> 0, Delta f := -(1/(beta N)) log \<Sign\> \>= 0, so \<Sign\> = exp(-beta N Delta f) holds by definition.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- declared path representation (basis and operator expansion)

## Bottleneck

Exponential decay in beta N is a hypothesis (Delta f bounded below by a positive constant uniformly in N and beta), not a theorem; Z_abs is an operational absolute ensemble, not in general a physical bosonic system.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-023 claims PROVED_LEAN; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1189_fsp_average_sign_definition.md`

- file: [dag/derivations/26_fsp/tfq_1189_fsp_average_sign_definition.md](../../../dag/derivations/26_fsp/tfq_1189_fsp_average_sign_definition.md)
- sha256 (`lf-normalised`): `e1d6fe1f195ecc664d1e8a3b187f9c0846370979b067fe6ddd32e7f404ce2de7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1189
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

- `APP-R-FSP-AVERAGE-SIGN-DEFINITION` `DERIVED_PROSE`: [FSP-SIGNED-HOPPING-PATH-SERIES](FSP-SIGNED-HOPPING-PATH-SERIES.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-FSP-SIGN-ESTIMATOR-VARIANCE` `DERIVED_PROSE`: [FSP-SIGN-ESTIMATOR-VARIANCE](FSP-SIGN-ESTIMATOR-VARIANCE.md) (PROVED_PROSE)
