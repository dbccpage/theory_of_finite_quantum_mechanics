# COMP-C3-CONTEXT-DECISION-PARTIAL

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The earlier GenesisComputation module decides only unary hole-only separability, collapse and pairwise separation on a finite regime. GenesisContextDecision now supplies complete finite slot-context decisions with multiple holes, arbitrary finite admitted arities and uniform-rule coverage in the existing Regime. TFQ-0497 remains open for first-count existence, Y-2 history-level necessity and external implementation refinement.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Use the general finite context procedure for the remaining TFQ-0497 history claims under their declared predicates; keep operational refinement separate.

## Source status

dag/derivations/29_computation/genesis_to_universal_computation.md record COMP-C3c claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1293
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_pgw-context-decision-procedure_lean_replay.json](../../../evidence/lean_receipts/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [evidence/lean_receipts/lean_replay_campaign_computation.json](../../../evidence/lean_receipts/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pairwiseSeparated_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms pairwiseSeparated_iff` |
| `two_marks_without_forms_collapsed` | yes | yes | yes | Quot.sound, propext | `#print axioms two_marks_without_forms_collapsed` |
| `unarySep_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms unarySep_iff` |

- counts toward the grade: yes

### Lean: `lean4/GenesisContextDecision.lean`

- file: [lean4/GenesisContextDecision.lean](../../../lean4/GenesisContextDecision.lean)
- sha256 (`bytes`): `b7d4a08565d18dacd9f3d4f82aa953360601a80ed7ede33392b9d477622f81ed`
- cited in: node.lean, record TFQ-1293
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_pgw-context-decision-procedure_lean_replay.json](../../../evidence/lean_receipts/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisContextDecision`): recorded sha256 `b7d4a08565d18dacd9f3d4f82aa953360601a80ed7ede33392b9d477622f81ed` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisContextDecision`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisContextDecision.collapseTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.collapseTest_correct` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1293

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed` (rust_symbol) | yes | yes | yes | - | - |
| `unary_sep` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1293

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed` (python_symbol) | yes | yes | yes | - | - |
| `unary_sep` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/genesis_to_universal_computation.md`

- file: [dag/derivations/29_computation/genesis_to_universal_computation.md](../../../dag/derivations/29_computation/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `27c7822177fe483a605b87cb9927dd1909001331834df7ed9d0b60ec1ad3108d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1293_comp_c3_context_decision_partial.md`

- file: [dag/derivations/29_computation/tfq_1293_comp_c3_context_decision_partial.md](../../../dag/derivations/29_computation/tfq_1293_comp_c3_context_decision_partial.md)
- sha256 (`lf-normalised`): `ae83b594032436f68067b13af818147ac277275e9bdb51596a10f72413cc1ec2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1293
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-COMP-C3-CONTEXT-DECISION-PARTIAL` `GAP_NO_DERIVATION`: [COMP-C3-BOUNDED-REACH-DECIDABLE](COMP-C3-BOUNDED-REACH-DECIDABLE.md) (PROVED_LEAN), [PGW-CONTEXT-DECISION-PROCEDURE](PGW-CONTEXT-DECISION-PROCEDURE.md) (OPEN)

Outgoing (0):

