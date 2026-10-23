# GTH-HORNS

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The horn Lambda^k\[n\] is the union of all faces of the standard n-simplex except the face opposite vertex k. The horn is inner when 0 \< k \< n and outer when k = 0 or k = n. A Kan condition asks for a filler of every horn. A quasicategory asks for a filler of every inner horn, in the sense of Joyal, Journal of Pure and Applied Algebra 175 (2002) 207-222. Which of these fillers a finite object derived from Genesis admission would have is open. No filler is exhibited and no counterexample is exhibited, because no such finite object is constructed.

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

Which horns would have fillers is open. There is no object of which a filler or a missing filler could be shown.

## Source status

Open. No horn filler and no counterexample is derived, because no shadow is constructed. The inner-horn notion is the one in the Joyal citation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2402_gth_horns.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2402_gth_horns.md](../../../dag/derivations/34_genesis_to_higher/tfq_2402_gth_horns.md)
- sha256 (`lf-normalised`): `23a214ff327e02294c8519eae8baadb581f297396a71d735f4e942b4394562a9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2402
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_horns.md`

- file: [dag/derivations/independent/gth_horns.md](../../../dag/derivations/independent/gth_horns.md)
- sha256 (`lf-normalised`): `5422717b8a9e77333dc2e48151bc5be552188470c4b8812b8856399957f6c532`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1016/S0022-4049(02)00135-4`

## Routes

Incoming (1):

- `GTH-R-GTH-HORNS` `GAP_NO_DERIVATION`: [GTH-TRUNC](GTH-TRUNC.md) (OPEN)

Outgoing (1):

- `GTH-R-GTH-HOTT-MODEL` `GAP_NO_DERIVATION`: [GTH-HOTT-MODEL](GTH-HOTT-MODEL.md) (OPEN)
