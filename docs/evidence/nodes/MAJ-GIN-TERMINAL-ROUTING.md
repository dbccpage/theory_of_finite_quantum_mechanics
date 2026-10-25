# MAJ-GIN-TERMINAL-ROUTING

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> evaluate_gin_fermion_recovery routes an invalid index to ClosureFailure, a valid index with zero uncancelled sign mass to Repair, and positive mass to SplitBrainRefusal.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The three lemmas unfold this rule; the Repair label is a routing tag, not a sign-problem solution.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-GIN-ROUTING claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaGinCore.lean`

- file: [papers/core/majorana/lean4/MajoranaGinCore.lean](../../../papers/core/majorana/lean4/MajoranaGinCore.lean)
- sha256 (`bytes`): `33ca2d4ec9a96398a74c96207caf0aa46d91b15ff4f10d245f394440a5102102`
- cited in: node.lean, record TFQ-1176
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaGinCore`): recorded sha256 `33ca2d4ec9a96398a74c96207caf0aa46d91b15ff4f10d245f394440a5102102` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaGinCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluate_gin_fermion_recovery` | yes | yes | yes | none | `#print axioms evaluate_gin_fermion_recovery` |
| `exact_gin_cancellation_routes_to_repair` | yes | yes | yes | none | `#print axioms exact_gin_cancellation_routes_to_repair` |
| `invalid_gin_routes_to_closure_failure` | yes | yes | yes | none | `#print axioms invalid_gin_routes_to_closure_failure` |
| `residual_sign_routes_to_refusal` | yes | yes | yes | Quot.sound, propext | `#print axioms residual_sign_routes_to_refusal` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1176_maj_gin_terminal_routing.md`

- file: [dag/derivations/28_majorana/tfq_1176_maj_gin_terminal_routing.md](../../../dag/derivations/28_majorana/tfq_1176_maj_gin_terminal_routing.md)
- sha256 (`lf-normalised`): `7b111c82efdc54f8cf127ba3e28b83b2e84753dc6d4289872c502ea85367caa0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1176
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-GIN-TERMINAL-ROUTING` `DERIVED_PROSE`: [MAJ-GIN-INVOLUTION-PAIR-CANCEL](MAJ-GIN-INVOLUTION-PAIR-CANCEL.md) (PROVED_LEAN)

Outgoing (0):

