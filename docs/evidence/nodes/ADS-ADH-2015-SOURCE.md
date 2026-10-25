# ADS-ADH-2015-SOURCE

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Almheiri, Dong and Harlow (2015, arXiv:1411.7041) resolve the radial-commutativity puzzle of bulk local operators by formulating the low-energy bulk Hilbert space as a code subspace H_code inside the boundary CFT Hilbert space: a bulk operator phi(x) in the causal wedge (or entanglement wedge, Section 3.4) of a boundary subregion A can be reconstructed as an operator O_A supported on A that acts identically to phi(x) on H_code (Section 3.1 eq. (3.3) p. 11, equivalent to \[O, E_a P E_b^dagger\] = 0 on the erasure errors of A^c in Section 3.2 eqs. (3.10), (3.15) pp. 13-15, illustrated by the three-qutrit code in Section 2.2 eq. (2.4) p. 8). This node records the paper as published.

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

Record only. Audited against the full text of arXiv:1411.7041 on 2026-10-22; the finite 5-qubit reconstruction instance is the separate target ADS-LOGICAL-RECONSTRUCTION-TARGET.

## Source status

Audited against the full text of arXiv:1411.7041 (Section 2.2 eq. (2.4) p. 8, Section 3.1 eq. (3.3) p. 11, Section 3.2 eqs. (3.10), (3.15) pp. 13-15, Section 3.5 eq. (3.30) p. 19) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/32_ads_cft/tfq_2205_ads_adh_2015_source.md`

- file: [dag/derivations/32_ads_cft/tfq_2205_ads_adh_2015_source.md](../../../dag/derivations/32_ads_cft/tfq_2205_ads_adh_2015_source.md)
- sha256 (`lf-normalised`): `a9350e6ce487d6010685307e0e0ea3f0e10c4f7cc13ccc8f629eb508d6e26a3c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2205
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1411.7041`

## Routes

Incoming (1):

- `FRO-R-ADS-ADH-2015-SOURCE` `RECORD_PARENT`: [ADS-RT-2006-SOURCE](ADS-RT-2006-SOURCE.md) (SOURCE_RECORD)

Outgoing (3):

- `FRO-R-ADS-HAPPY-2015-SOURCE` `RECORD_PARENT`: [ADS-HAPPY-2015-SOURCE](ADS-HAPPY-2015-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-ADS-HARLOW-2016-SOURCE` `RECORD_PARENT`: [ADS-HARLOW-2016-SOURCE](ADS-HARLOW-2016-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-ADS-LOGICAL-RECONSTRUCTION-TARGET` `DERIVED_LEAN`: [ADS-LOGICAL-RECONSTRUCTION-TARGET](ADS-LOGICAL-RECONSTRUCTION-TARGET.md) (PROVED_LEAN)
