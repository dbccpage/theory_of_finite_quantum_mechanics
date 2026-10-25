# GTH-IMPORT-INFTY-GROUPOID

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Assumed, and not derived: an infinity-groupoid in the sense of a Kan complex, a simplicial set in which every horn has a filler, as used for infinity-groupoids in Lurie, Higher Topos Theory, arXiv:math/0608040. An infinity-groupoid has cells in every finite dimension. It is not a finite semi-simplicial set of bounded dimension. A finite n-type presentation is only an approximation of this assumption: it stops at a fixed dimension and does not supply fillers in all higher dimensions.

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

- infinity-groupoid as a Kan complex (assumption; not finite; finite truncation is only an approximation)

## Bottleneck

The assumption is an infinity-groupoid (Kan complex, fillers for every horn). It is not finite, it is not derived, and a finite n-type is only an approximation.

## Source status

Imported assumption. The cited book is the name of the assumption. An infinity-groupoid is not finite and is not derived here. A finite truncation is only an approximation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2405_gth_import_infty_groupoid.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2405_gth_import_infty_groupoid.md](../../../dag/derivations/34_genesis_to_higher/tfq_2405_gth_import_infty_groupoid.md)
- sha256 (`lf-normalised`): `0c73dc6943c563e9332108534d4cf1259659e0f14bda066d130a79a57184ef0a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2405
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_import_infty_groupoid.md`

- file: [dag/derivations/independent/gth_import_infty_groupoid.md](../../../dag/derivations/independent/gth_import_infty_groupoid.md)
- sha256 (`lf-normalised`): `2e9bcf302a1fd3165f98aca1876d34904e2bacdee34a38424b7189e680162108`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:math/0608040`

## Routes

Incoming (1):

- `GTH-R-GTH-IMPORT-INFTY-GROUPOID` `GAP_NO_DERIVATION`: [GTH-HOTT-MODEL](GTH-HOTT-MODEL.md) (OPEN)

Outgoing (0):

