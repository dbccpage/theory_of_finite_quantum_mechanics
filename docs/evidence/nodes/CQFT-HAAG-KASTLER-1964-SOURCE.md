# CQFT-HAAG-KASTLER-1964-SOURCE

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Haag and Kastler (1964) formulate quantum field theory through a net that assigns to bounded spacetime regions the algebras of observables localized there, with the standard structural requirements later grouped as isotony (larger regions have larger algebras), locality (algebras of spacelike separated regions commute) and Poincare covariance, and with states as positive functionals. This node records the framework; the paper's own list of postulates is not reproduced.

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

None recorded.

## Bottleneck

Record only. The checkout holds no copy of the 1964 print article; the standard postulate list is checked in secondary sources (arXiv:math-ph/9903028 Section 1 pp. 2-3; arXiv:1607.03901 Section 6 pp. 28-30), while the primary 1964 numbering remains to be audited against the print text.

## Source status

Published source cited by title, authors and identifier (checked against the arXiv, DOI or Numdam record on 2026-10-21); no derivation from it is read, audited or reproduced in this repository.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/31_causal_qft/tfq_2102_cqft_haag_kastler_1964_source.md`

- file: [dag/derivations/31_causal_qft/tfq_2102_cqft_haag_kastler_1964_source.md](../../../dag/derivations/31_causal_qft/tfq_2102_cqft_haag_kastler_1964_source.md)
- sha256 (`lf-normalised`): `5b25afcebc5336ef5b728ad0c891505b0fccc2d5c6060a457b8e0cf9ff74001d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2102
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1063/1.1704187`

## Routes

Incoming (1):

- `FRO-R-CQFT-HAAG-KASTLER-1964-SOURCE` `RECORD_PARENT`: [CQFT-FINITE-STRICT-POSET-SPACELIKE](CQFT-FINITE-STRICT-POSET-SPACELIKE.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-CQFT-LOCAL-NET-AXIOMS-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-LOCAL-NET-AXIOMS-IMPORT](CQFT-LOCAL-NET-AXIOMS-IMPORT.md) (IMPORTED_ASSUMPTION)
