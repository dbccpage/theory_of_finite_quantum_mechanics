# ADS-CFT-DUALITY-IMPORT

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported as an assumption, not as a result of this repository: a quantum gravity theory on an asymptotically anti-de Sitter spacetime has the same observables as a conformal field theory on its boundary. The duality is a conjecture. It presupposes continuum quantum field theory (a Hilbert space, unitary evolution, operator algebras) and a continuum gravity theory; the repository records both as open or held outside the programme.

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

- continuum quantum field theory and gravity (assumption)
- large-N limit (assumption)

## Bottleneck

The continuum inputs are not constructed: FQ-GAP-CONTINUUM-HILBERT-LIFT and the finite-to-continuum interface TFQ-0085 are open.

## Source status

Audited against arXiv:hep-th/9711200, arXiv:hep-th/9802109 and arXiv:hep-th/9802150 on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md`

- file: [dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md](../../../dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md)
- sha256 (`lf-normalised`): `4b7c0d1645c7ed98cbdd3026f028e7583a413f707f9c54af58003f62fbd0f285`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2202
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:hep-th/9711200`
- `external:arXiv:hep-th/9802109`
- `external:arXiv:hep-th/9802150`

## Routes

Incoming (1):

- `FRO-R-ADS-CFT-DUALITY-IMPORT` `CONDITIONAL_ON_IMPORT`: [ADS-GKPW-DICTIONARY-SOURCE](ADS-GKPW-DICTIONARY-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-HAPPY-TOY-NOT-DUALITY-GAP` `GAP_NO_DERIVATION`: [ADS-HAPPY-TOY-NOT-DUALITY-GAP](ADS-HAPPY-TOY-NOT-DUALITY-GAP.md) (OPEN)
- `FRO-R-BACK-ADS-DUALITY-TO-CONTINUUM-INTERFACE` `GAP_NO_DERIVATION`: [TFQ-0085](TFQ-0085.md) (OPEN)
