# MAJ-TRICHOTOMY-EXHAUSTIVE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Since im d0 is contained in ker d1, C1 is the disjoint union of im d0, ker d1 minus im d0, and C1 minus ker d1, so each residual carries exactly one of the three labels.

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

None recorded.

## Bottleneck

A Lean exhaustiveness lemma (a classical case split on d1 w = 0 and on membership in im d0) is absent from MajoranaCore.lean.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-THM-TRICHOTOMY-EXHAUSTIVE claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/28_majorana/tfq_1142_maj_trichotomy_exhaustive.md`

- file: [dag/derivations/28_majorana/tfq_1142_maj_trichotomy_exhaustive.md](../../../dag/derivations/28_majorana/tfq_1142_maj_trichotomy_exhaustive.md)
- sha256 (`lf-normalised`): `69c386eeb1f8ec7a6da84138cd32849d755fa70a619d568aec998a9d07b51e9f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1142
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-TRICHOTOMY-EXHAUSTIVE` `DERIVED_PROSE`: [MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION](MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-MAJ-TORUS-2X2-WORKED-GRID` `COMPUTED`: [MAJ-TORUS-2X2-WORKED-GRID](MAJ-TORUS-2X2-WORKED-GRID.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-MAJ-TRICHOTOMY-ELIMINATION-DECISION` `DERIVED_PROSE`: [MAJ-TRICHOTOMY-ELIMINATION-DECISION](MAJ-TRICHOTOMY-ELIMINATION-DECISION.md) (PROVED_PROSE)
