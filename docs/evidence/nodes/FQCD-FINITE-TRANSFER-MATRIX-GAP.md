# FQCD-FINITE-TRANSFER-MATRIX-GAP

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite group G with a unitary representation, a finite periodic spatial lattice with edge set E and finite real beta, construct the temporal-gauge Wilson transfer matrix on functions on G^E and prove strict entrywise positivity and gauge equivariance. Its Perron eigenvalue lambda_0 is positive and simple, its normalized Perron vector is gauge invariant, and the non-Perron spectral-radius ratio q in the gauge-invariant sector satisfies 0 \<= q \< 1. Set q = 0 when that sector has no non-Perron eigenvalues. For q \> 0 the logarithmic gap -log(q) is positive; q = 0 represents an infinite spectral decay rate, not a finite logarithm.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Construct the transfer matrix and its gauge action, prove the required positivity and equivariance, and apply Perron-Frobenius in Lean. Handle zero subleading eigenvalues and the one-dimensional physical sector explicitly. Correlation-decay bounds require the relevant self-adjointness or operator estimates. No bound uniform in volume or lattice spacing, or continuum Yang-Mills mass gap, follows from the finite-volume statement.

## Source status

Added 2026-10-27 with maintainer approval as a precisely stated target; no Lean, Rust or Python evidence exists in this checkout.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/17_finite_qcd/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [dag/derivations/17_finite_qcd/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../dag/derivations/17_finite_qcd/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `8a802a811b96cbe022372b44d51b43396f36bc54c8f2302bb76716383ad5e11c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1049_fqcd_finite_transfer_matrix_gap.md`

- file: [dag/derivations/17_finite_qcd/tfq_1049_fqcd_finite_transfer_matrix_gap.md](../../../dag/derivations/17_finite_qcd/tfq_1049_fqcd_finite_transfer_matrix_gap.md)
- sha256 (`lf-normalised`): `ac395f85d0c75518718687954724aad2ff831d3d4b78b0141a4ed10ad5bcbed7`
- generated view: listed, not counted
- cited in: record TFQ-1049
- counts toward the grade: no

## Routes

Incoming (1):

- `FQCD-R-FINITE-TRANSFER-MATRIX-GAP` `GAP_NO_DERIVATION`: [TFQ-0011](TFQ-0011.md) (OPEN), [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)

Outgoing (0):

