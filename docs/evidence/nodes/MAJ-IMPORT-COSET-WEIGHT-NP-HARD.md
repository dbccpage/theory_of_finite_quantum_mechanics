# MAJ-IMPORT-COSET-WEIGHT-NP-HARD

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Minimum-weight coset decoding of a binary linear code given by its matrix is NP-hard (Berlekamp, McEliece and van Tilborg 1978).

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

- Berlekamp-McEliece-van Tilborg 1978 hardness of coset weights

## Bottleneck

Literature result; no reduction is formalized or replayed here.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-IMPORT-BMVT claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md`

- file: [dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md](../../../dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md)
- sha256 (`lf-normalised`): `894d77b6f0e0bb14f85b84436be15c13b62344715eb7ed63b7fd95e987b745ee`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1157
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-IMPORT-COSET-WEIGHT-NP-HARD` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-PHI1-SYNDROME-DECODING` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-SYNDROME-DECODING](MAJ-PHI1-SYNDROME-DECODING.md) (CONDITIONAL)
