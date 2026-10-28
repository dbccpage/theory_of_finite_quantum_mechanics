# FGAUGE-MEDNYKH-2D-YANG-MILLS

Stage: [FINITE_GAUGE](../stages/FINITE_GAUGE.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite group G and a closed orientable surface of genus g, |Hom(pi_1(Sigma_g), G)| / |G| equals the sum over irreducible complex representations R of G of (|G| / dim R)^(2g-2); this number is the zero-area partition function of two-dimensional lattice gauge theory with gauge group G and does not depend on the cellulation of the surface.

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

Prove the formula in Lean from the column orthogonality of characters, and the cellulation independence under the Pachner moves. Two-dimensional gauge theory has no propagating gluons, so the node models finite gauge structure and not four-dimensional confinement.

## Source status

Added 2026-10-27 with maintainer approval as a precisely stated target; no Lean, Rust or Python evidence exists in this checkout.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FiniteGroupPachner.lean`

- file: [lean4/FiniteGroupPachner.lean](../../../lean4/FiniteGroupPachner.lean)
- sha256 (`bytes`): `2f4916b1ac6b688304948b5ad00aa570a0a2cae0770ab80587307f6acffda82e`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json) (module `FiniteGroupPachner`): recorded sha256 `2f4916b1ac6b688304948b5ad00aa570a0a2cae0770ab80587307f6acffda82e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteGroupPachner`
- counts toward the grade: yes

### Documents and data: `dag/derivations/14_finite_gauge/tfq_1051_fgauge_mednykh_2d_yang_mills.md`

- file: [dag/derivations/14_finite_gauge/tfq_1051_fgauge_mednykh_2d_yang_mills.md](../../../dag/derivations/14_finite_gauge/tfq_1051_fgauge_mednykh_2d_yang_mills.md)
- sha256 (`lf-normalised`): `c27dccdeab07dc199ea11202f7269e8524060898d7c792cb5569f59f341cdd63`
- generated view: listed, not counted
- cited in: record TFQ-1051
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `23dbe23bf9913bed6b5ea2428aae9f15b82a0e260a1a8894a23aa1d3d301475f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FGAUGE-R-MEDNYKH-2D-YANG-MILLS` `GAP_NO_DERIVATION`: [TFQ-0009](TFQ-0009.md) (OPEN)

Outgoing (0):

