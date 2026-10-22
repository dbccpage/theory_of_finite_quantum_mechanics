# FSP-WILSON-DIRAC-GAMMA5

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Wilson-Dirac operator satisfies gamma5 D_W gamma5 = D_W^dagger, so its nonreal eigenvalues come in conjugate pairs and det D_W is real; for two degenerate flavors det(D_W)^2 \>= 0.

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

- Wilson-Dirac lattice fermion operator with r = 1 (standard lattice QCD)

## Bottleneck

A single-flavor det D_W can be negative; the JSONL claim that det D_W is nonnegative is only the two-flavor square. Not established in this checkout.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-033 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1197_fsp_wilson_dirac_gamma5.md`

- file: [dag/derivations/26_fsp/tfq_1197_fsp_wilson_dirac_gamma5.md](../../../dag/derivations/26_fsp/tfq_1197_fsp_wilson_dirac_gamma5.md)
- sha256 (`lf-normalised`): `2224f9e8b406bc700e1be6fca93f4fad1eba3c2cdc8425a0206f616432c8ce56`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1197
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-WILSON-DIRAC-GAMMA5` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (IMPORTED_ASSUMPTION), [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (2):

- `APP-R-FSP-LATTICE-ANOMALY-INFLOW` `GAP_NO_DERIVATION`: [FSP-LATTICE-ANOMALY-INFLOW](FSP-LATTICE-ANOMALY-INFLOW.md) (OPEN)
- `APP-R-FSP-SU2-ADJOINT-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)
