# CT-INFORMATION-MEDIA-INTEROPERABILITY

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported principles, audited and corrected against Deutsch and Marletto (2015, arXiv:1405.5563, Sections 3-6 pp. 9-12): a computation variable is a set S of at least two possible attributes for which all permutation tasks are possible with side-effects (Section 3 p. 9); a variable S is clonable if the cloning task R_S(x0) = union_{x in S} {(x, x0) -\> (x, x)} is possible with side-effects for some preparable blank attribute x0 (Section 4 eq. (3) p. 10); an information variable is a clonable computation variable, and an information medium is a substrate with at least one information variable (Section 4 p. 10). Distinguishability is defined afterward in Section 5 (eq. (4) p. 11) by mapping into an information variable, avoiding circularity, and every information variable is then shown to be distinguishable. Principle III (interoperability, Section 6 p. 12) states that the composite S1 + S2 of two substrates with information variables S1 and S2 is an information medium with information variable S1 x S2.

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

- information medium and interoperability principle (assumption)

## Bottleneck

The interoperability principle (Principle III, Section 6 p. 12) constrains composite information variables to include S1 x S2 in the source's framework. It is not shown to select the Hilbert tensor product, local tomography or any positive cone, so it does not discharge FQ-GAP-TENSOR-UNIQUENESS.

## Source status

Audited and corrected against the full text of arXiv:1405.5563 (Sections 3-6, eqs. (3)-(4), Principle III, pp. 9-12) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md`

- file: [dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md](../../../dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md)
- sha256 (`lf-normalised`): `df0aabf17d37d88bba24f6754060aa1c7c220f393449927c48b5e2ed6a84bd98`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2006
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1405.5563`

## Routes

Incoming (1):

- `FRO-R-CT-INFORMATION-MEDIA-INTEROPERABILITY` `CONDITIONAL_ON_IMPORT`: [CT-DEUTSCH-MARLETTO-2015-SOURCE](CT-DEUTSCH-MARLETTO-2015-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-BACK-CT-INTEROP-TO-TENSOR` `GAP_NO_DERIVATION`: [FQ-GAP-TENSOR-UNIQUENESS](FQ-GAP-TENSOR-UNIQUENESS.md) (CONDITIONAL)
- `FRO-R-CT-SUPERINFORMATION-MEDIUM-DEFINITION` `CONDITIONAL_ON_IMPORT`: [CT-SUPERINFORMATION-MEDIUM-DEFINITION](CT-SUPERINFORMATION-MEDIUM-DEFINITION.md) (IMPORTED_ASSUMPTION)
