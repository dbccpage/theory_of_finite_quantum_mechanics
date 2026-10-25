# ADS-GKPW-DICTIONARY-SOURCE

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Gubser, Klebanov and Polyakov (1998, arXiv:hep-th/9802109, Section 2 eq. (2.5) p. 4 and Section 3 eq. (3.14) p. 8) and Witten (1998, arXiv:hep-th/9802150, Section 2.3 eq. (2.11) p. 11 and Section 2.5 eqs. (2.32)-(2.33) p. 17) formulate the AdS/CFT prescription identifying the CFT generating functional of boundary operators O coupled to boundary sources phi_0 with the bulk partition function \<exp int phi_0 O\>_CFT = Z_string(phi_0) (approximated at large N by exp(-I_sugra(phi)) on AdS_{d+1}), with conformal dimension Delta(Delta - d) = (m R)^2, Delta = (d + sqrt(d^2 + 4(m R)^2))/2 for a scalar of mass m. This node records the two papers.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Record only. The dictionary is not reproduced.

## Source status

Audited against the full texts of arXiv:hep-th/9802109 (Section 2 eq. (2.5) p. 4, Section 3 eq. (3.14) p. 8) and arXiv:hep-th/9802150 (Section 2.3 eq. (2.11) p. 11, Section 2.5 eqs. (2.32)-(2.33) p. 17) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/32_ads_cft/tfq_2201_ads_gkpw_dictionary_source.md`

- file: [dag/derivations/32_ads_cft/tfq_2201_ads_gkpw_dictionary_source.md](../../../dag/derivations/32_ads_cft/tfq_2201_ads_gkpw_dictionary_source.md)
- sha256 (`lf-normalised`): `12185b54ca4e171f6c99b129bcb7d6c0ec55c5fa9cd64ab419c1ab5079bc4ec8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2201
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:hep-th/9802109`
- `external:arXiv:hep-th/9802150`

## Routes

Incoming (1):

- `FRO-R-ADS-GKPW-DICTIONARY-SOURCE` `RECORD_PARENT`: [ADS-MALDACENA-1997-SOURCE](ADS-MALDACENA-1997-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-CFT-DUALITY-IMPORT` `CONDITIONAL_ON_IMPORT`: [ADS-CFT-DUALITY-IMPORT](ADS-CFT-DUALITY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `FRO-R-ADS-RT-2006-SOURCE` `RECORD_PARENT`: [ADS-RT-2006-SOURCE](ADS-RT-2006-SOURCE.md) (SOURCE_RECORD)
