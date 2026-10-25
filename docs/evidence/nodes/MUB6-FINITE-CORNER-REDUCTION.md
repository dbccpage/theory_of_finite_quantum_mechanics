# MUB6-FINITE-CORNER-REDUCTION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Using the external finite-corner classification of single 6x6 complex Hadamard matrices, quartet existence in C^6 is equivalent to raw quartet completion of some retained finite-corner reconstruction with D = -C E* (B^-1)*.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Cardenes Wuttig and Tindall, finite-corner classification of CHM(6), arXiv:2608.18053v2, external Lean pin 57b03025

## Bottleneck

MubFiniteCornerReduction.lean is not in this checkout; exclusion over every retained reconstruction is open, and finite fibres over continuous seeds give no finite global list.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-PAPER-FINITE-CORNER claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md`

- file: [dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md](../../../dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md)
- sha256 (`lf-normalised`): `c06c2e49408ff683256c44e7042c07f3ce126907c07a9fe98a63572362482d1c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1261
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-FINITE-CORNER-REDUCTION` `CONDITIONAL_ON_IMPORT`: [MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS](MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS.md) (PROVED_LEAN)

Outgoing (0):

