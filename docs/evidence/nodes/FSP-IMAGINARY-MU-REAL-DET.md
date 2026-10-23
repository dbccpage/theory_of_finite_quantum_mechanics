# FSP-IMAGINARY-MU-REAL-DET

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At mu = i mu_I with real mu_I, gamma5 D(i mu_I) gamma5 = D(i mu_I)^dagger, so det D(i mu_I) is real; nonnegativity needs two degenerate flavors (or a staggered operator m + K with K anti-Hermitian, m \> 0), and Z(mu_I) has Roberge-Weiss periodicity 2 pi T / 3.

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

- imaginary chemical potential and Roberge-Weiss periodicity (literature)

## Bottleneck

Analytic continuation from imaginary to real mu is an extrapolation, not a sign-free route to real mu; not established in this checkout.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-039 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1203_fsp_imaginary_mu_real_det.md`

- file: [dag/derivations/26_fsp/tfq_1203_fsp_imaginary_mu_real_det.md](../../../dag/derivations/26_fsp/tfq_1203_fsp_imaginary_mu_real_det.md)
- sha256 (`lf-normalised`): `ac2647c3b3b9ad8360fff38c46c8a361167df805ce0ca1de6df0ae176c927fd3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1203
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3268ac1be0222f75b9b9238508325cab337a6f767114e2d25afff56163a42cf4`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-IMAGINARY-MU-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-QCD-CHEMICAL-POTENTIAL-DET](FSP-QCD-CHEMICAL-POTENTIAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-LATTICE-WESS-ZUMINO-SUSY` `GAP_NO_DERIVATION`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
