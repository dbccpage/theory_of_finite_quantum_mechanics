# COMP-C2-LETTER-RENAME-COMMUTES

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every letter map f, a step or reach on words gives a step or reach of the f-image rule predicate on the f-image words; for an injective f a reach of the image comes from a reach of the original (Reach.of_map).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is the word-side analogue of Genesis Step.rename and Reach.rename, not an instance of them.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C2b claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1287
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach.exists_of_map` | yes | yes | yes | Quot.sound, propext | `#print axioms Reach.exists_of_map` |
| `Reach.map` | yes | yes | yes | propext | `#print axioms Reach.map` |
| `Reach.of_map` | yes | yes | yes | Quot.sound, propext | `#print axioms Reach.of_map` |
| `Step.exists_of_map` | yes | yes | yes | Quot.sound, propext | `#print axioms Step.exists_of_map` |
| `Step.map` | yes | yes | yes | propext | `#print axioms Step.map` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1287
- check: `cd code/rust && cargo test -p tfqm_wdp letter_map_commutes_with_steps`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `letter_map_commutes_with_steps` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp letter_map_commutes_with_steps` |
| `map_marks` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1287_comp_c2_letter_rename_commutes.md`

- file: [dag/derivations/29_computation/tfq_1287_comp_c2_letter_rename_commutes.md](../../../dag/derivations/29_computation/tfq_1287_comp_c2_letter_rename_commutes.md)
- sha256 (`lf-normalised`): `4d7972f430d77e5435956fec6f92c23f3eac76d05ed6f8b3bfb83f49b8ab48ab`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1287
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C2-LETTER-RENAME-COMMUTES` `DERIVED_LEAN`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION), [PG-GEN-REWRITING-COMMUTATION](PG-GEN-REWRITING-COMMUTATION.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C2-STEP3-NOT-WORD-STEP` `GAP_NO_DERIVATION`: [COMP-C2-STEP3-NOT-WORD-STEP](COMP-C2-STEP3-NOT-WORD-STEP.md) (OPEN)
