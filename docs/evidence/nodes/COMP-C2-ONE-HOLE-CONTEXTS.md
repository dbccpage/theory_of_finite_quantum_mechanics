# COMP-C2-ONE-HOLE-CONTEXTS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A Genesis-style context (a slot tuple with holes, one datum plugged into every hole) has exactly one hole iff it is ofSplit u v for a unique pair of letter lists, and plugging d gives u ++ d :: v; so the one-hole contexts of arity a are the word contexts (u,v) with |u| + |v| = a - 1.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Genesis plugs one datum into every hole while a word rule plugs a word into one hole, which is the wider operation; the sealed regime contexts with forms and rules are not modelled.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C2c claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1288
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `holes_ofSplit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms holes_ofSplit` |
| `ofSplit_injective` | yes | yes | yes | propext | `#print axioms ofSplit_injective` |
| `oneHole_iff_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms oneHole_iff_split` |
| `plug1_ofSplit` | yes | yes | yes | Quot.sound, propext | `#print axioms plug1_ofSplit` |
| `plug1_ofSplit_eq_plug` | yes | yes | yes | Quot.sound, propext | `#print axioms plug1_ofSplit_eq_plug` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1288

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contexts` (rust_symbol) | yes | yes | yes | - | - |
| `plug1` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1288

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `context_counts` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1288_comp_c2_one_hole_contexts.md`

- file: [dag/derivations/29_computation/tfq_1288_comp_c2_one_hole_contexts.md](../../../dag/derivations/29_computation/tfq_1288_comp_c2_one_hole_contexts.md)
- sha256 (`lf-normalised`): `7ce9dae5a891bca0bec872c98c5894fc4dafb238bf805018b1ba6b4edabb2721`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1288
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C2-ONE-HOLE-CONTEXTS` `DERIVED_LEAN`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION), [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (1):

- `APP-R-COMP-C2-CONTEXT-COUNTS-CHECKED` `COMPUTED`: [COMP-C2-CONTEXT-COUNTS-CHECKED](COMP-C2-CONTEXT-COUNTS-CHECKED.md) (COMPUTATIONALLY_CHECKED)
