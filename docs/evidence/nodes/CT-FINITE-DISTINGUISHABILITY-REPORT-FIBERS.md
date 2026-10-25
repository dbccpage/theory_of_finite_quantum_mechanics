# CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Formalized finite statement. For a finite set X and a report map q from X to R, two attributes A and B of X (nonemptiness is not needed) are separated by a deterministic task, meaning a function f from R to {0,1} with f(q(a))=0 on A and f(q(b))=1 on B, if and only if q(A) and q(B) are disjoint. Checked in Lean 4 over Finset for arbitrary types X and R with decidable equality on R: both directions and the biconditional; when q(A) and q(B) are disjoint the indicator of B on the union of A and B is constant on the fibers of q (HistoryReport.FiberConstant, the form PG-HISTORY-REPORT-CRITERION takes); and an exhaustive bitmask decision check over all (q, A, B) with nonempty attributes for 1\<=|X|\<=4 and 1\<=|R|\<=3. This matches the constructor-theoretic notion of distinguishable attributes only on its deterministic finite fragment: accuracy, repeatability and constructor existence are not modelled.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Checked in Lean 4 on Finset for all finite carriers and by the exhaustive check for |X|\<=4, |R|\<=3. Whether the finite condition deserves the name "distinguishable attributes" in the source's sense depends on the imported definition, which this repository does not adopt.

## Source status

Source definition of distinguishability audited against arXiv:1405.5563 Section 5 eq. (4) p. 11 on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierDistinguishability (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `FULL`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `separatedByTask_iff_disjoint_image` (and both directions), `fiberConstant_indicator_of_disjoint_image`, `exhaustive_distinguishability_check_le4_le3`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierDistinguishability.lean`

- file: [lean4/FrontierDistinguishability.lean](../../../lean4/FrontierDistinguishability.lean)
- sha256 (`bytes`): `5599a6efaac3ebd3e3006e03464cc71cff77b459ce32207572243e2a7aa496f2`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierDistinguishability)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierDistinguishability`): recorded sha256 `5599a6efaac3ebd3e3006e03464cc71cff77b459ce32207572243e2a7aa496f2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierDistinguishability`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierDistinguishability.disjoint_image_imp_separatedByTask` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierDistinguishability.disjoint_image_imp_separatedByTask` |
| `FrontierDistinguishability.exhaustive_distinguishability_check_le4_le3` | yes | yes | yes | propext | `#print axioms FrontierDistinguishability.exhaustive_distinguishability_check_le4_le3` |
| `FrontierDistinguishability.fiberConstant_indicator_of_disjoint_image` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierDistinguishability.fiberConstant_indicator_of_disjoint_image` |
| `FrontierDistinguishability.separatedByTask_iff_disjoint_image` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierDistinguishability.separatedByTask_iff_disjoint_image` |
| `FrontierDistinguishability.separatedByTask_imp_disjoint_image` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierDistinguishability.separatedByTask_imp_disjoint_image` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2004_ct_finite_distinguishability_report_fibers.md`

- file: [dag/derivations/30_constructor_theory/tfq_2004_ct_finite_distinguishability_report_fibers.md](../../../dag/derivations/30_constructor_theory/tfq_2004_ct_finite_distinguishability_report_fibers.md)
- sha256 (`lf-normalised`): `f4f02250816f96a4f38a0fc794923450535d1c2283f0676d756ccc61aa059683`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2004
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS` `DERIVED_LEAN`: [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN), [CT-TASK-CONSTRUCTOR-POSSIBILITY](CT-TASK-CONSTRUCTOR-POSSIBILITY.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

