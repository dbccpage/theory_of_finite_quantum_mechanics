# FSP-QCD-CHEMICAL-POTENTIAL-DET

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For lattice Dirac operators with chemical potential, gamma5 D(mu) gamma5 = D(-mu*)^dagger, hence det D(mu)^* = det D(-mu*); for real mu != 0 this relates D(mu) to D(-mu) only and det D(mu) is in general complex.

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

- lattice QCD with staggered quarks at chemical potential (standard)

## Bottleneck

Standard identity imported; the checkout has no SU(3) staggered operator and no computation of det D(mu).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-037 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md`

- file: [dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md](../../../dag/derivations/26_fsp/tfq_1201_fsp_qcd_chemical_potential_det.md)
- sha256 (`lf-normalised`): `3c9ccc4d667d3780a4c102212544290707166e263dc383020d17a6298f66d6aa`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1201
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3268ac1be0222f75b9b9238508325cab337a6f767114e2d25afff56163a42cf4`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-QCD-CHEMICAL-POTENTIAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-IMAGINARY-MU-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-IMAGINARY-MU-REAL-DET](FSP-IMAGINARY-MU-REAL-DET.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-TRIALITY-CENTER-PROJECTION` `GAP_NO_DERIVATION`: [FSP-TRIALITY-CENTER-PROJECTION](FSP-TRIALITY-CENTER-PROJECTION.md) (OPEN)
