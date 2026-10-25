# CT-SUPERINFORMATION-MEDIUM-DEFINITION

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported definition, audited and corrected against Deutsch and Marletto (2015, arXiv:1405.5563, Section 6 pp. 14-18 and Section 7 p. 20): an information observable is an information variable X whose attributes satisfy double-complement closure x = u_x under distinguishability (Section 6, Principle VIII p. 16); a superinformation medium is an information medium with at least two information observables X and Y that contain only mutually disjoint attributes and whose union X union Y is not an information observable (Section 7 p. 20). Sections 8.1 and 8.3 (pp. 20-22) show under Principles III, IV, VI, VII, VIII and IX that X union Y is neither distinguishable nor clonable. The repository neither adopts this definition as a primitive nor claims that its finite carriers satisfy Principles I-IX.

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

- superinformation medium (assumption)

## Bottleneck

The definition (Section 7 p. 20) is an assumption of this branch. Whether the repository's declared finite quantum interface meets its finite cloning shadow is the content of CT-QUBIT-NO-CLONING-FINITE-TARGET, which is checked in Lean only in the narrowed form recorded there (explicit clone maps, the Z-union-X obstruction for additive maps, the pairwise equal-or-orthogonal classification); the fidelity argument and complete positivity are not formalised.

## Source status

Audited and corrected against the full text of arXiv:1405.5563 (Section 6 pp. 14-18, Section 7 p. 20, Sections 8.1-8.3 pp. 20-22) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2007_ct_superinformation_medium_definition.md`

- file: [dag/derivations/30_constructor_theory/tfq_2007_ct_superinformation_medium_definition.md](../../../dag/derivations/30_constructor_theory/tfq_2007_ct_superinformation_medium_definition.md)
- sha256 (`lf-normalised`): `4b9f17157c36092978d75e1a2bba99312ad6b53b9abd565c3a6f99962e8f494f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2007
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1405.5563`

## Routes

Incoming (1):

- `FRO-R-CT-SUPERINFORMATION-MEDIUM-DEFINITION` `CONDITIONAL_ON_IMPORT`: [CT-INFORMATION-MEDIA-INTEROPERABILITY](CT-INFORMATION-MEDIA-INTEROPERABILITY.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `FRO-R-CT-NO-CLONING-COMPLEMENTARITY-SOURCE-CLAIM` `RECORD_PARENT`: [CT-NO-CLONING-COMPLEMENTARITY-SOURCE-CLAIM](CT-NO-CLONING-COMPLEMENTARITY-SOURCE-CLAIM.md) (SOURCE_RECORD)
- `FRO-R-CT-QUBIT-NO-CLONING-FINITE-TARGET` `DERIVED_LEAN`: [CT-QUBIT-NO-CLONING-FINITE-TARGET](CT-QUBIT-NO-CLONING-FINITE-TARGET.md) (PROVED_LEAN)
