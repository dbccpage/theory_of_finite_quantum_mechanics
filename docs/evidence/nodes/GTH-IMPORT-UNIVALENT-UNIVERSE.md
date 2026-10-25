# GTH-IMPORT-UNIVALENT-UNIVERSE

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Assumed, and not derived from Genesis admission or from any finite model: a univalent universe in the sense of the Homotopy Type Theory book (The Univalent Foundations Program, Institute for Advanced Study, 2013), a type U together with a map from the identity type Id_U(A, B) to the type of equivalences between A and B that is itself an equivalence. Such a universe is not a finite set and is not a finite semi-simplicial set of bounded dimension. A finite model of a fragment with identity types, were one later defined, would be only an approximation of this assumption: the assumption is an infinite object, and the finite model would not contain it.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- univalent universe (assumption; not finite; finite model is only an approximation)

## Bottleneck

The assumption is a univalent universe. It is not finite, it is not derived, and any finite identity-type model is only an approximation of it.

## Source status

Imported assumption. The cited book is the name of the assumption. This repository does not derive a univalent universe, and a finite model would be only an approximation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2404_gth_import_univalent_universe.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2404_gth_import_univalent_universe.md](../../../dag/derivations/34_genesis_to_higher/tfq_2404_gth_import_univalent_universe.md)
- sha256 (`lf-normalised`): `209d5e33a92ac19a496508143989f135281b97e2e160de278e45fcf5857e17a4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2404
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_import_univalent_universe.md`

- file: [dag/derivations/independent/gth_import_univalent_universe.md](../../../dag/derivations/independent/gth_import_univalent_universe.md)
- sha256 (`lf-normalised`): `5700a5c86ea56b6738318a915cfa093c42bf0cff508767b65c37d18dd668c728`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:book:The-Univalent-Foundations-Program-2013-Homotopy-Type-Theory`

## Routes

Incoming (1):

- `GTH-R-GTH-IMPORT-UNIVALENT-UNIVERSE` `GAP_NO_DERIVATION`: [GTH-HOTT-MODEL](GTH-HOTT-MODEL.md) (OPEN)

Outgoing (0):

