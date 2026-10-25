# COMP-C2-WORD-REWRITING

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Words are lists over the marks; Step R holds between w and w2 when w = u ++ l ++ v and w2 = u ++ r ++ v for a rule l -\> r of R; Reach is the reflexive-transitive closure; step_iff_plug reads a step as a rule applied under a one-hole context.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- cited Lean declaration references covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The rule predicate is supplied by the regime; Genesis Step3 is a different relation (COMP-C2e).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C2a claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1286
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Ctx.plug` | yes | yes | yes | none | `#print axioms Ctx.plug` |
| `Reach` | yes | yes | yes | none | `#print axioms Reach` |
| `Reach.context` | yes | yes | yes | propext | `#print axioms Reach.context` |
| `Step` | yes | yes | yes | none | `#print axioms Step` |
| `Step.context` | yes | yes | yes | propext | `#print axioms Step.context` |
| `step_iff_plug` | yes | yes | yes | none | `#print axioms step_iff_plug` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1286

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Rule` (rust_symbol) | yes | yes | yes | - | - |
| `Srs` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1286

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `successors` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1286_comp_c2_word_rewriting.md`

- file: [dag/derivations/29_computation/tfq_1286_comp_c2_word_rewriting.md](../../../dag/derivations/29_computation/tfq_1286_comp_c2_word_rewriting.md)
- sha256 (`lf-normalised`): `b83bd9038600964c230c543f592527b814fb3725a23edddacb9eebaccf40aad3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1286
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C2-WORD-REWRITING` `DERIVED_PROSE`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN), [PG-FREE-MONOID-NONISO](PG-FREE-MONOID-NONISO.md) (PROVED_LEAN)

Outgoing (4):

- `APP-R-COMP-C2-LETTER-RENAME-COMMUTES` `DERIVED_LEAN`: [COMP-C2-LETTER-RENAME-COMMUTES](COMP-C2-LETTER-RENAME-COMMUTES.md) (PROVED_LEAN)
- `APP-R-COMP-C2-ONE-HOLE-CONTEXTS` `DERIVED_LEAN`: [COMP-C2-ONE-HOLE-CONTEXTS](COMP-C2-ONE-HOLE-CONTEXTS.md) (PROVED_LEAN)
- `APP-R-COMP-C3-BOUNDED-REACH-DECIDABLE` `DERIVED_LEAN`: [COMP-C3-BOUNDED-REACH-DECIDABLE](COMP-C3-BOUNDED-REACH-DECIDABLE.md) (PROVED_LEAN)
- `APP-R-COMP-C5-TM0-STEP-SIMULATION` `DERIVED_LEAN`: [COMP-C5-TM0-STEP-SIMULATION](COMP-C5-TM0-STEP-SIMULATION.md) (PROVED_LEAN)
