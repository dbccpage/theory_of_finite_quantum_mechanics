# ADS-RT-2006-SOURCE

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Ryu and Takayanagi (2006, arXiv:hep-th/0603001, Section 1 eq. (1.5) p. 2) propose that the entanglement entropy S_A of a spatial subregion A in a (d+1)-dimensional CFT dual to static AdS_{d+2} is given by S_A = Area(gamma_A) / (4 G_N^(d+2)), where gamma_A is the static minimal bulk d-surface anchored on partial A, and check in Section 2 (eqs. (2.1), (2.5)-(2.6) p. 3) that in AdS_3/CFT_2 the geodesic length reproduces S_A = (c/3) log((L/(pi a)) sin(pi l / L)) under the Brown-Henneaux relation c = 3R / (2 G_N^(3)). This node records the proposal as published.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Record only.

## Source status

Audited against the full text of arXiv:hep-th/0603001 (Section 1 eq. (1.5) p. 2, Section 2 eqs. (2.1), (2.5)-(2.6) p. 3) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/32_ads_cft/tfq_2203_ads_rt_2006_source.md`

- file: [dag/derivations/32_ads_cft/tfq_2203_ads_rt_2006_source.md](../../../dag/derivations/32_ads_cft/tfq_2203_ads_rt_2006_source.md)
- sha256 (`lf-normalised`): `05a3cac3ede82f2f0adb382de0289af94102b7ec408f90d9fcb0d8e2208957fe`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2203
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:hep-th/0603001`

## Routes

Incoming (1):

- `FRO-R-ADS-RT-2006-SOURCE` `RECORD_PARENT`: [ADS-GKPW-DICTIONARY-SOURCE](ADS-GKPW-DICTIONARY-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-ADH-2015-SOURCE` `RECORD_PARENT`: [ADS-ADH-2015-SOURCE](ADS-ADH-2015-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-ADS-RT-FORMULA-IMPORT` `CONDITIONAL_ON_IMPORT`: [ADS-RT-FORMULA-IMPORT](ADS-RT-FORMULA-IMPORT.md) (IMPORTED_ASSUMPTION)
