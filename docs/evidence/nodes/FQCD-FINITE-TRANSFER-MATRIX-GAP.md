# FQCD-FINITE-TRANSFER-MATRIX-GAP

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite group G with a unitary representation, a finite periodic spatial lattice with edge set E and finite real beta, the temporal-gauge transfer matrix of the Wilson action acting on functions on G^E has strictly positive entries, so it has a simple largest eigenvalue lambda_0, a gauge-invariant Perron eigenvector, and every other eigenvalue satisfies |lambda| \< lambda_0; the finite-volume gap log(lambda_0/|lambda_1|) is positive on the gauge-invariant subspace.

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

Prove the statement in Lean from the Perron-Frobenius theorem for positive matrices. The node is the automatic finite-volume gap only: it gives no bound uniform in volume or lattice spacing and is not the Yang-Mills mass gap of the Clay problem.

## Source status

Added 2026-10-27 with maintainer approval as a precisely stated target; no Lean, Rust or Python evidence exists in this checkout.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1049_fqcd_finite_transfer_matrix_gap.md`

- file: [dag/derivations/17_finite_qcd/tfq_1049_fqcd_finite_transfer_matrix_gap.md](../../../dag/derivations/17_finite_qcd/tfq_1049_fqcd_finite_transfer_matrix_gap.md)
- sha256 (`lf-normalised`): `ee35a2cf25babed25f9f114c8f88e6e01bea110328a6398fcc0fdf2f1692a467`
- generated view: listed, not counted
- cited in: record TFQ-1049
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `23dbe23bf9913bed6b5ea2428aae9f15b82a0e260a1a8894a23aa1d3d301475f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQCD-R-FINITE-TRANSFER-MATRIX-GAP` `GAP_NO_DERIVATION`: [TFQ-0011](TFQ-0011.md) (OPEN), [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)

Outgoing (0):

