# GTH-SHADOW

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No construction turns PGW-GO-ADMISSION-GATE into a finite semi-simplicial set or a finite globular set. That gate keeps a two-valued admission record with a reached result: reaching leaves not-admitted, and admission is not one of the four kinds of change. A finite semi-simplicial set of dimension at most N is finite sets X_0, ..., X_N and face maps d_i from X_n to X_{n-1} such that d_i composed with d_j equals d_{j-1} composed with d_i whenever i \< j. It carries no degeneracy maps. A finite globular set is finite sets with source and target maps s, t from X_{n+1} to X_n such that s composed with s equals s composed with t, and t composed with t equals t composed with s. Neither family is defined from the admission record.

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

Missing parent construction: PGW-GO-ADMISSION-GATE is a two-valued admission record, and no source builds a finite semi-simplicial set or a finite globular set from it.

## Source status

Open. No finite semi-simplicial or globular set is defined from PGW-GO-ADMISSION-GATE.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2400_gth_shadow.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2400_gth_shadow.md](../../../dag/derivations/34_genesis_to_higher/tfq_2400_gth_shadow.md)
- sha256 (`lf-normalised`): `34cc81312b95c41aab6c6f9ca4febc37e15d735b80ef2845026563be91ebd78e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2400
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_shadow.md`

- file: [dag/derivations/independent/gth_shadow.md](../../../dag/derivations/independent/gth_shadow.md)
- sha256 (`lf-normalised`): `932e35ee3d7753416702705b963c5a82670c40147a796fda721b00b14803837b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `GTH-R-GTH-SHADOW` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (1):

- `GTH-R-GTH-TRUNC` `GAP_NO_DERIVATION`: [GTH-TRUNC](GTH-TRUNC.md) (OPEN)
