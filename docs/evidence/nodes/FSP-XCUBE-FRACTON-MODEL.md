# FSP-XCUBE-FRACTON-MODEL

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Vijay-Haah-Fu (2016): the X-cube model on an Lx x Ly x Lz periodic cubic lattice has pairwise commuting vertex and cube terms and ground-state degeneracy 2^(2Lx + 2Ly + 2Lz - 3).

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

- X-cube stabilizer model (Vijay, Haah, Fu 2016)

## Bottleneck

Imported literature result; the checkout has no X-cube stabilizer computation, and it has no fermion-sign consequence by itself.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-053 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1217_fsp_xcube_fracton_model.md`

- file: [dag/derivations/26_fsp/tfq_1217_fsp_xcube_fracton_model.md](../../../dag/derivations/26_fsp/tfq_1217_fsp_xcube_fracton_model.md)
- sha256 (`lf-normalised`): `d9db4e96a94d47467776f881e9d1f0e408b311c52dd10abe11bcbfeeb47c4fb0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1217
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3268ac1be0222f75b9b9238508325cab337a6f767114e2d25afff56163a42cf4`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-BF-2GROUP-SIGN-CLAIM](FSP-BF-2GROUP-SIGN-CLAIM.md) (OPEN), [FSP-DIRAC-KAHLER-SPINFOAM-CLAIM](FSP-DIRAC-KAHLER-SPINFOAM-CLAIM.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-FRACTON-MOBILITY` `CONDITIONAL_ON_IMPORT`: [FSP-FRACTON-MOBILITY](FSP-FRACTON-MOBILITY.md) (IMPORTED_ASSUMPTION)
