# CQFT-LOCAL-NET-AXIOMS-IMPORT

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported structure: a spacetime with a causal order, and a family of unital star-algebras A(O) indexed by regions O with isotony (O1 inside O2 gives A(O1) inside A(O2)) and commutation of A(O1) and A(O2) when O1 and O2 are spacelike separated. The repository has finite strict posets (lean4/CausalOrder.lean) and finite matrix algebras, but no net over regions of a continuum and no Minkowski light cone; DS-QM033-064-074-083-QHELD-CONTINUUM records the light-cone causality as an external L2 lift.

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

- spacetime with causal order (assumption)
- net of local algebras with isotony and locality (assumption)

## Bottleneck

Held outside the programme by declaration, as recorded for the light cone in the trunk node named in the gap route.

## Source status

Taken from the cited source as an assumption of this branch; the source's own hypotheses and exact wording are not audited here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/31_causal_qft/tfq_2103_cqft_local_net_axioms_import.md`

- file: [dag/derivations/31_causal_qft/tfq_2103_cqft_local_net_axioms_import.md](../../../dag/derivations/31_causal_qft/tfq_2103_cqft_local_net_axioms_import.md)
- sha256 (`lf-normalised`): `11b16b9b6c47df1fc9978e42b56e6e3b6b939c649b4a8cd5b4fe3bbf40e11fb0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2103
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1063/1.1704187`

## Routes

Incoming (1):

- `FRO-R-CQFT-LOCAL-NET-AXIOMS-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-HAAG-KASTLER-1964-SOURCE](CQFT-HAAG-KASTLER-1964-SOURCE.md) (SOURCE_RECORD)

Outgoing (4):

- `FRO-R-BACK-CQFT-NET-TO-QHELD` `GAP_NO_DERIVATION`: [DS-QM033-064-074-083-QHELD-CONTINUUM](DS-QM033-064-074-083-QHELD-CONTINUUM.md) (IMPORTED_ASSUMPTION)
- `FRO-R-CQFT-EPSTEIN-GLASER-1973-SOURCE` `RECORD_PARENT`: [CQFT-EPSTEIN-GLASER-1973-SOURCE](CQFT-EPSTEIN-GLASER-1973-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CQFT-FINITE-POSET-NET-TARGET` `DERIVED_LEAN`: [CQFT-FINITE-POSET-NET-TARGET](CQFT-FINITE-POSET-NET-TARGET.md) (PROVED_LEAN)
- `FRO-R-CQFT-REEH-SCHLIEDER-1961-SOURCE` `RECORD_PARENT`: [CQFT-REEH-SCHLIEDER-1961-SOURCE](CQFT-REEH-SCHLIEDER-1961-SOURCE.md) (SOURCE_RECORD)
