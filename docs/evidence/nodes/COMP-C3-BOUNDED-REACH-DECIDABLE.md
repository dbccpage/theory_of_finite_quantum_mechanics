# COMP-C3-BOUNDED-REACH-DECIDABLE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For k marks, a finite rule list and a length bound L, ReachB is decided by an explicit closure of at most card(wordsLE L) rounds (decideReachB_iff); the configuration space has exactly 1 + k + ... + k^L words (card_wordsLE); Step on a finite rule list is decidable (mem_succList).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This decides rewriting reachability in a declared bound; the decision procedure over all Genesis contexts of the sealed regime asked by TFQ-0497 is not built (COMP-C3c).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C3a claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1291
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `card_wordsLE` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms card_wordsLE` |
| `decideReachB_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms decideReachB_iff` |
| `mem_succList` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms mem_succList` |
| `reachB_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reachB_iff` |
| `reachSet_card_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reachSet_card_le` |
| `rtg_iff_mem_reachN_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms rtg_iff_mem_reachN_card` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1291
- check: `cd code/rust && cargo test -p tfqm_wdp bounded_decider_is_exact_on_a_closed_system`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bounded_decider_is_exact_on_a_closed_system` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp bounded_decider_is_exact_on_a_closed_system` |
| `config_space_size` (rust_symbol) | yes | yes | yes | - | - |
| `decide_reach` (rust_symbol) | yes | yes | yes | - | - |
| `reach_set_bounded` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1291

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bounded_reach` (python_symbol) | yes | yes | yes | - | - |
| `config_space_size` (python_symbol) | yes | yes | yes | - | - |
| `decide_reach` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1291_comp_c3_bounded_reach_decidable.md`

- file: [dag/derivations/29_computation/tfq_1291_comp_c3_bounded_reach_decidable.md](../../../dag/derivations/29_computation/tfq_1291_comp_c3_bounded_reach_decidable.md)
- sha256 (`lf-normalised`): `06b55c284e6b33daff554769cbddde32845f360260bbf11bc54e63ef3e2ef580`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1291
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C3-BOUNDED-REACH-DECIDABLE` `DERIVED_LEAN`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION), [PGW-RUNS-PAST-DECLARED-BOUNDS](PGW-RUNS-PAST-DECLARED-BOUNDS.md) (OPEN)

Outgoing (2):

- `APP-R-COMP-C3-CONTEXT-DECISION-PARTIAL` `GAP_NO_DERIVATION`: [COMP-C3-CONTEXT-DECISION-PARTIAL](COMP-C3-CONTEXT-DECISION-PARTIAL.md) (OPEN)
- `APP-R-COMP-C3-VERDICT-SOUND` `DERIVED_LEAN`: [COMP-C3-VERDICT-SOUND](COMP-C3-VERDICT-SOUND.md) (PROVED_LEAN)
