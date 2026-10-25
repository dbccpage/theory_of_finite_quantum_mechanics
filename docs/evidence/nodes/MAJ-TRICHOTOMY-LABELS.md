# MAJ-TRICHOTOMY-LABELS

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a residual w in C1: Exact means w = d0 a for some a in C0; ClosedResidual means d1 w = 0 and w is not Exact; OpenObstruction means d1 w is nonzero.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

These are diagnostic schedule classes only; their relation to FOC terminals is fenced by TFQ-0181.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-DEF-TRICHOTOMY-LABELS claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1139
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `TrichotomyClass` | yes | yes | yes | none | `#print axioms TrichotomyClass` |
| `is_closed_residual` | yes | yes | yes | none | `#print axioms is_closed_residual` |
| `is_cocycle` | yes | yes | yes | none | `#print axioms is_cocycle` |
| `is_exact` | yes | yes | yes | none | `#print axioms is_exact` |
| `is_open_obstruction` | yes | yes | yes | none | `#print axioms is_open_obstruction` |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1139

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `TrichotomyClass` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1139_maj_trichotomy_labels.md`

- file: [dag/derivations/28_majorana/tfq_1139_maj_trichotomy_labels.md](../../../dag/derivations/28_majorana/tfq_1139_maj_trichotomy_labels.md)
- sha256 (`lf-normalised`): `5bf725e110fd487246b9d79ae260855d6aea274818685d6e916d9ef9fae54983`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1139
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-TRICHOTOMY-LABELS` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION` `DERIVED_LEAN`: [MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION](MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION.md) (PROVED_LEAN)
