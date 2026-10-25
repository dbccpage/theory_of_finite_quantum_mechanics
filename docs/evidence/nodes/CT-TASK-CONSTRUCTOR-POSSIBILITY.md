# CT-TASK-CONSTRUCTOR-POSSIBILITY

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported vocabulary, audited against Deutsch (2013, Section 1.1 eqs. (1)-(2) pp. 2-4) and Deutsch-Marletto (2015, Section 2 pp. 6-8): a task is a set of ordered input/output attribute pairs of a substrate; a constructor causes the transformation and retains its ability to do so again; a task is possible when the laws of nature impose no limit short of perfection on how accurately it can be performed and how well a constructor can retain its ability to perform it again, and not possible otherwise; Principle I (Section 2 p. 8) states that the state of a composite substrate S1 + S2 is the pair of states on S1 and S2 and a construction on S1 changes only the S1 state. The repository uses none of this vocabulary as a primitive.

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

- task / constructor / possible-task vocabulary (assumption)

## Bottleneck

Taking the possible and not-possible partition of tasks as primitive is a different foundational choice from the repository's admitted primitive PG-ROOT-DIFF-STRUCTURE and its replayed refusal predicates. No source derives either from the other.

## Source status

Audited against the full text of arXiv:1210.7439 (Section 1.1 eqs. (1)-(2) pp. 2-4) and arXiv:1405.5563 (Section 2 pp. 6-8) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2001_ct_task_constructor_possibility.md`

- file: [dag/derivations/30_constructor_theory/tfq_2001_ct_task_constructor_possibility.md](../../../dag/derivations/30_constructor_theory/tfq_2001_ct_task_constructor_possibility.md)
- sha256 (`lf-normalised`): `824724df867d564527a485a4eb47ea46cd0d208e9b7b0f45171cf31030e26855`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2001
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1210.7439`
- `external:arXiv:1405.5563`

## Routes

Incoming (1):

- `FRO-R-CT-TASK-CONSTRUCTOR-POSSIBILITY` `CONDITIONAL_ON_IMPORT`: [CT-DEUTSCH-2013-SOURCE](CT-DEUTSCH-2013-SOURCE.md) (SOURCE_RECORD)

Outgoing (3):

- `FRO-R-CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS` `DERIVED_LEAN`: [CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS](CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS.md) (PROVED_LEAN)
- `FRO-R-CT-GENESIS-SEPARATION-TASK-ANALOGY` `GAP_NO_DERIVATION`: [CT-GENESIS-SEPARATION-TASK-ANALOGY](CT-GENESIS-SEPARATION-TASK-ANALOGY.md) (OPEN)
- `FRO-R-CT-REFUSAL-OBSTRUCTION-ANALOGY` `GAP_NO_DERIVATION`: [CT-REFUSAL-OBSTRUCTION-ANALOGY](CT-REFUSAL-OBSTRUCTION-ANALOGY.md) (OPEN)
