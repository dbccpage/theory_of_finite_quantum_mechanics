# COMP-C5-TM0-STEP-SIMULATION

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a Mathlib TM0 machine encoded on configuration words lend, left cells, q, a, right cells, rend, a machine step from a represented configuration is matched by a rewrite step to a word representing the next configuration, and every rewrite step of a represented word is the machine step; a word represents at most one configuration.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Mathlib Turing.TM0.Machine, step, Reaches, Tape, ListBlank

## Bottleneck

Machines in the TM0 form only (one write or one move per transition); representations allow blank padding at the far ends; the end rules write a fresh blank, the only place where words grow.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C5a claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompTM.lean`

- file: [lean4/GenesisCompTM.lean](../../../lean4/GenesisCompTM.lean)
- sha256 (`bytes`): `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c`
- cited in: node.lean, node.source, record TFQ-1299
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompTM`): recorded sha256 `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompTM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Rules` | yes | yes | yes | none | `#print axioms Rules` |
| `cfgWord` | yes | yes | yes | none | `#print axioms cfgWord` |
| `rep_exists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms rep_exists` |
| `rep_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms rep_unique` |
| `split_st` | yes | yes | yes | propext | `#print axioms split_st` |
| `step_bwd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms step_bwd` |
| `step_fwd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms step_fwd` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1299

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check_step_simulation` (rust_symbol) | yes | yes | yes | - | - |
| `decode` (rust_symbol) | yes | yes | yes | - | - |
| `encode` (rust_symbol) | yes | yes | yes | - | - |
| `rules_of` (rust_symbol) | yes | yes | yes | - | - |
| `tm_step` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1299

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decode` (python_symbol) | yes | yes | yes | - | - |
| `encode` (python_symbol) | yes | yes | yes | - | - |
| `rules_for` (python_symbol) | yes | yes | yes | - | - |
| `run_checked` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1299_comp_c5_tm0_step_simulation.md`

- file: [dag/derivations/29_computation/tfq_1299_comp_c5_tm0_step_simulation.md](../../../dag/derivations/29_computation/tfq_1299_comp_c5_tm0_step_simulation.md)
- sha256 (`lf-normalised`): `a8331ef32a78a7908aaa95636c15ec9929265b852180118dfbba6b81ca990df2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1299
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C5-TM0-STEP-SIMULATION` `DERIVED_LEAN`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION), [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-COMP-C3-RUNNER-NEEDS-BLANKS` `DERIVED_LEAN`: [COMP-C3-RUNNER-NEEDS-BLANKS](COMP-C3-RUNNER-NEEDS-BLANKS.md) (PROVED_LEAN)
- `APP-R-COMP-C5-CLOSURES-HALTING` `DERIVED_LEAN`: [COMP-C5-CLOSURES-HALTING](COMP-C5-CLOSURES-HALTING.md) (PROVED_LEAN)
- `APP-R-COMP-C5-MARK-BUDGET-RULE-LIST` `DERIVED_LEAN`: [COMP-C5-MARK-BUDGET-RULE-LIST](COMP-C5-MARK-BUDGET-RULE-LIST.md) (PROVED_LEAN)
