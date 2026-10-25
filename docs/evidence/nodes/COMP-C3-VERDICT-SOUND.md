# COMP-C3-VERDICT-SOUND

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The three-valued verdict returns reachable only for a true Reach, returns unreachable only when the bounded search is closed so no longer path exists, and otherwise returns a witness step that leaves the bound; every Reach is a ReachB for some bound.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declaration references covered by a current replay receipt: 7
- counted in-repo runnable tests: 3
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Soundness only; the verdict boundExceeded does not decide the unbounded question.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C3b claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1292
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach.exists_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach.exists_bound` |
| `ReachB.reach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReachB.reach` |
| `closed_reach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms closed_reach` |
| `reach_iff_reachB_of_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach_iff_reachB_of_closed` |
| `verdict_boundExceeded_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms verdict_boundExceeded_witness` |
| `verdict_reachable_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms verdict_reachable_sound` |
| `verdict_unreachable_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms verdict_unreachable_sound` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1292

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Verdict` (rust_symbol) | yes | yes | yes | - | - |
| `bounded_decider_reports_bound_exceeded` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp bounded_decider_reports_bound_exceeded` |
| `start_outside_bound_is_refused` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp start_outside_bound_is_refused` |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1292

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decide_reach` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/test_genesis_tm.py`

- file: [code/python/tests/test_genesis_tm.py](../../../code/python/tests/test_genesis_tm.py)
- sha256 (`bytes`): `6aefb990bc7d69e26cf22c1fe85301a5d07e73b85e2da39de613765242f30f60`
- cited in: record TFQ-1292
- check: `python -m pytest code/python/tests/test_genesis_tm.py::test_growth_rule_is_refused_with_bound_exceeded`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_growth_rule_is_refused_with_bound_exceeded` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_genesis_tm.py::test_growth_rule_is_refused_with_bound_exceeded` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1292_comp_c3_verdict_sound.md`

- file: [dag/derivations/29_computation/tfq_1292_comp_c3_verdict_sound.md](../../../dag/derivations/29_computation/tfq_1292_comp_c3_verdict_sound.md)
- sha256 (`lf-normalised`): `c3cec34b119f3c43107b13bc60f30baf794ba5d4ff607848ca65d9df1b06dc9e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1292
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C3-VERDICT-SOUND` `DERIVED_LEAN`: [COMP-C3-BOUNDED-REACH-DECIDABLE](COMP-C3-BOUNDED-REACH-DECIDABLE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C3-RUNNER-NEEDS-BLANKS` `DERIVED_LEAN`: [COMP-C3-RUNNER-NEEDS-BLANKS](COMP-C3-RUNNER-NEEDS-BLANKS.md) (PROVED_LEAN)
