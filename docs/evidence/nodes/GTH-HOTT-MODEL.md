# GTH-HOTT-MODEL

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No deep embedding of a dependent type theory, and no finite model of such a theory, is constructed. The fragment in view has identity types and does not include univalence. Lean's impredicative proof-irrelevant Prop is a different theory; this node does not add univalence to that theory and does not interpret it. An intended interpretation would send contexts to finite sets or to finite semi-simplicial data and would send identity types to a stated path relation. No such interpretation is defined, and no soundness statement is derived.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No deep embedding, no finite model and no soundness statement. The fragment excludes univalence. Lean Prop is a different theory.

## Source status

Open. No deep embedding and no finite identity-type model is constructed. Univalence is not part of the fragment.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2403_gth_hott_model.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2403_gth_hott_model.md](../../../dag/derivations/34_genesis_to_higher/tfq_2403_gth_hott_model.md)
- sha256 (`lf-normalised`): `5674e8d4ab0e2d95c393d0c939c507915294fbc573e8a9a72a0aeb38284ac742`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2403
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_hott_model.md`

- file: [dag/derivations/independent/gth_hott_model.md](../../../dag/derivations/independent/gth_hott_model.md)
- sha256 (`lf-normalised`): `01a7a24051c0b9e7ff4e7d627a2ce01b69d8552522f224df0aa15bf5f0031c83`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:book:The-Univalent-Foundations-Program-2013-Homotopy-Type-Theory`

## Routes

Incoming (1):

- `GTH-R-GTH-HOTT-MODEL` `GAP_NO_DERIVATION`: [GTH-HORNS](GTH-HORNS.md) (OPEN)

Outgoing (3):

- `GTH-R-GTH-IMPORT-INFTY-1-CATEGORY` `GAP_NO_DERIVATION`: [GTH-IMPORT-INFTY-1-CATEGORY](GTH-IMPORT-INFTY-1-CATEGORY.md) (IMPORTED_ASSUMPTION)
- `GTH-R-GTH-IMPORT-INFTY-GROUPOID` `GAP_NO_DERIVATION`: [GTH-IMPORT-INFTY-GROUPOID](GTH-IMPORT-INFTY-GROUPOID.md) (IMPORTED_ASSUMPTION)
- `GTH-R-GTH-IMPORT-UNIVALENT-UNIVERSE` `GAP_NO_DERIVATION`: [GTH-IMPORT-UNIVALENT-UNIVERSE](GTH-IMPORT-UNIVALENT-UNIVERSE.md) (IMPORTED_ASSUMPTION)
