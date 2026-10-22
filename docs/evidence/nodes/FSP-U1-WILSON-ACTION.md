# FSP-U1-WILSON-ACTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With link phases U_ij = exp(i A_ij) and oriented plaquette products U_p, the Wilson action S = beta_g sum_p (1 - Re U_p) is invariant under local U(1) gauge transformations and nonnegative.

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

- compact lattice U(1) gauge theory with Wilson action (Wilson 1974)

## Bottleneck

Standard lattice-gauge fact imported, not established in this checkout; the source supplies no fermion-sign consequence for it.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-032 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1196_fsp_u1_wilson_action.md`

- file: [dag/derivations/26_fsp/tfq_1196_fsp_u1_wilson_action.md](../../../dag/derivations/26_fsp/tfq_1196_fsp_u1_wilson_action.md)
- sha256 (`lf-normalised`): `c50b048187479b448a2a907e70a4c1e023cb07d81b3058f117804b47021402ea`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1196
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-U1-WILSON-ACTION` `CONDITIONAL_ON_IMPORT`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (PROVED_LEAN), [FSP-HUBBARD-PROTECTED-REPRESENTATIONS](FSP-HUBBARD-PROTECTED-REPRESENTATIONS.md) (CONDITIONAL)

Outgoing (3):

- `APP-R-FSP-SU2-ADJOINT-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-THETA-TERM-COMPLEX-WEIGHT` `CONDITIONAL_ON_IMPORT`: [FSP-THETA-TERM-COMPLEX-WEIGHT](FSP-THETA-TERM-COMPLEX-WEIGHT.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-WILSON-DIRAC-GAMMA5` `CONDITIONAL_ON_IMPORT`: [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION)
