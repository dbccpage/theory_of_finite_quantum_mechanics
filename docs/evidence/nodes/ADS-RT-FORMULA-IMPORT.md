# ADS-RT-FORMULA-IMPORT

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported formula, as the source states it at leading order in Newton's constant: S(A) = Area(minimal surface anchored on the boundary of A) / (4 G). It presupposes the von Neumann entropy of a boundary reduced state on a continuum Hilbert space and the area of a surface in a bulk geometry. The repository has an exact von Neumann entropy dichotomy for algebraic spectra and an exact rational Regge area proxy that is not the Einstein-Hilbert action; neither is a minimal-surface area in a bulk geometry.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- von Neumann entropy of boundary regions on a continuum Hilbert space (assumption)
- bulk geometry with minimal surfaces (assumption)

## Bottleneck

No source supplies a dictionary from the repository's finite areas to the surface areas of the formula.

## Source status

Audited against arXiv:hep-th/0603001 Section 1 eq. (1.5) p. 2 on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/32_ads_cft/tfq_2204_ads_rt_formula_import.md`

- file: [dag/derivations/32_ads_cft/tfq_2204_ads_rt_formula_import.md](../../../dag/derivations/32_ads_cft/tfq_2204_ads_rt_formula_import.md)
- sha256 (`lf-normalised`): `a5fef1fd468860146e898d96f892c210a0d0bf6283d37ed5e0f91c6d54251a61`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2204
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:hep-th/0603001`

## Routes

Incoming (1):

- `FRO-R-ADS-RT-FORMULA-IMPORT` `CONDITIONAL_ON_IMPORT`: [ADS-RT-2006-SOURCE](ADS-RT-2006-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-HAPPY-ENTROPY-MINCUT-TARGET` `DERIVED_LEAN`: [ADS-HAPPY-ENTROPY-MINCUT-TARGET](ADS-HAPPY-ENTROPY-MINCUT-TARGET.md) (PROVED_LEAN)
- `FRO-R-ADS-REGGE-AREA-RT-GAP` `GAP_NO_DERIVATION`: [ADS-REGGE-AREA-RT-GAP](ADS-REGGE-AREA-RT-GAP.md) (OPEN)
