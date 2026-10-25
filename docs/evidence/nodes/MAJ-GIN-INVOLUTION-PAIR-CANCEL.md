# MAJ-GIN-INVOLUTION-PAIR-CANCEL

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a natural weight w and integer signs with s1 + s2 = 0, w s1 + w s2 = 0 in Int.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Single pair only; no global involution on a configuration space is constructed.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-GIN-INVOLUTION-CANCEL claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaGinCore.lean`

- file: [papers/core/majorana/lean4/MajoranaGinCore.lean](../../../papers/core/majorana/lean4/MajoranaGinCore.lean)
- sha256 (`bytes`): `33ca2d4ec9a96398a74c96207caf0aa46d91b15ff4f10d245f394440a5102102`
- cited in: node.lean, record TFQ-1175
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaGinCore`): recorded sha256 `33ca2d4ec9a96398a74c96207caf0aa46d91b15ff4f10d245f394440a5102102` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaGinCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `involution_pair_cancels_sign` | yes | yes | yes | propext | `#print axioms involution_pair_cancels_sign` |
| `is_exact_involution_partner` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms is_exact_involution_partner` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1175_maj_gin_involution_pair_cancel.md`

- file: [dag/derivations/28_majorana/tfq_1175_maj_gin_involution_pair_cancel.md](../../../dag/derivations/28_majorana/tfq_1175_maj_gin_involution_pair_cancel.md)
- sha256 (`lf-normalised`): `5a3baca2fd3a6560709d18f1d8bd26cc6518e846097611dfee2571c7e21e9a44`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1175
- counts toward the grade: no

### Documents and data: `papers/core/majorana/lean4/axiom_report.txt`

- file: [papers/core/majorana/lean4/axiom_report.txt](../../../papers/core/majorana/lean4/axiom_report.txt)
- sha256 (`lf-normalised`): `ec4465011fdd2b18f2c9df263004e9050f8c394dece1841835ff0bcd1e00df79`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-GIN-INVOLUTION-PAIR-CANCEL` `DERIVED_LEAN`: [FSP-EFFICIENT-SAMPLING-OBLIGATIONS](FSP-EFFICIENT-SAMPLING-OBLIGATIONS.md) (OPEN), [FSP-MERON-CHARACTER-CANCELLATION](FSP-MERON-CHARACTER-CANCELLATION.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MAJ-GIN-TERMINAL-ROUTING` `DERIVED_PROSE`: [MAJ-GIN-TERMINAL-ROUTING](MAJ-GIN-TERMINAL-ROUTING.md) (DEFINITION)
