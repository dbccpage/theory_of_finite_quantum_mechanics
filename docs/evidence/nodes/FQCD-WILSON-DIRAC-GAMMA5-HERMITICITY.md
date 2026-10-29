# FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite periodic hypercubic lattice in dimension 2 or 4 with arbitrary unitary link matrices U_mu(x), Hermitian Euclidean gamma matrices and gamma5 anticommuting with each gamma_mu, the Wilson-Dirac operator D_W = m + sum_mu \[gamma_mu (nabla_mu + nabla*_mu)/2 - (r/2) nabla*_mu nabla_mu\] with real m and r satisfies gamma5 D_W gamma5 = D_W^dagger.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
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

Prove the operator identity in Lean for the finite lattice. A proof would supply the hypothesis that FSP-WILSON-DIRAC-GAMMA5 now imports; lean4/FermionSignWilsonDiracGamma5.lean states only the Clifford and determinant lemmas, not this identity.

## Source status

Added 2026-10-27 with maintainer approval as a precisely stated target; no Lean, Rust or Python evidence exists in this checkout.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FermionSignWilsonDiracGamma5.lean`

- file: [lean4/FermionSignWilsonDiracGamma5.lean](../../../lean4/FermionSignWilsonDiracGamma5.lean)
- sha256 (`bytes`): `ff846e497a572038d084022f188dfb1ec05affba46ff2c8c652a2c4f1cd3664e`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json](../../../dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json) (module `FermionSignWilsonDiracGamma5`): recorded sha256 `ff846e497a572038d084022f188dfb1ec05affba46ff2c8c652a2c4f1cd3664e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignWilsonDiracGamma5`
- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md`

- file: [dag/derivations/17_finite_qcd/tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md](../../../dag/derivations/17_finite_qcd/tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md)
- sha256 (`lf-normalised`): `70a1bfb0fa2819b8217b48686fe64618001cf1d86a8945c7c297e0f6ed271707`
- generated view: listed, not counted
- cited in: record TFQ-1050
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `8a7a3be8a63e3712d9ab4f9846017c540fad454c328a9c94b79dff8317af75d7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQCD-R-WILSON-DIRAC-GAMMA5-HERMITICITY` `GAP_NO_DERIVATION`: [TFQ-0026](TFQ-0026.md) (OPEN), [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

