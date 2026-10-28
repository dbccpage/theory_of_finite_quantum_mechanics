# FQCD-STRONG-COUPLING-AREA-LAW

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite gauge group G, a nontrivial irreducible unitary representation R and dimension d \>= 2, there are explicit beta_0 \> 0, K and sigma \> 0 depending on G, R and d such that for 0 \<= beta \< beta_0 the Wilson-action expectation of the R-character of every rectangular Wilson loop C on a finite periodic lattice much larger than C satisfies |\<W_R(C)\>| \<= K exp(-sigma Area(C)), with Area(C) the minimal spanning area.

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

Prove the bound by a convergent strong-coupling (cluster) expansion in the style of Osterwalder-Seiler (1978), with explicit constants. The bound would replace the declared area-law formula of TFQ-0024 by a derived inequality at strong coupling; it says nothing about weak coupling or the continuum.

## Source status

Added 2026-10-27 with maintainer approval as a precisely stated target; no Lean, Rust or Python evidence exists in this checkout.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md`

- file: [dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md](../../../dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md)
- sha256 (`lf-normalised`): `5bedbce5d93a9929faf60f54e37ffb7c0e3be53db4ebcda6fb7ad38a7af65830`
- generated view: listed, not counted
- cited in: record TFQ-1052
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `23dbe23bf9913bed6b5ea2428aae9f15b82a0e260a1a8894a23aa1d3d301475f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQCD-R-STRONG-COUPLING-AREA-LAW` `GAP_NO_DERIVATION`: [TFQ-0030](TFQ-0030.md) (COMPUTATIONALLY_CHECKED), [TFQ-0024](TFQ-0024.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

