# COMP-C3-CONTEXT-DECISION-PARTIAL

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The earlier GenesisComputation module decides only unary hole-only separability, collapse and pairwise separation on a finite regime. CampaignGenesisContextDecision now supplies complete finite slot-context decisions with multiple holes, arbitrary finite admitted arities and uniform-rule coverage in the existing Regime. TFQ-0497 remains open for first-count existence, Y-2 history-level necessity and external implementation refinement.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declaration references covered by a current replay receipt: 4
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

dag/research/genesis_to_universal_computation.md record COMP-C3c claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGenesisContextDecision.lean`

- file: [lean4/CampaignGenesisContextDecision.lean](../../../lean4/CampaignGenesisContextDecision.lean)
- sha256 (`bytes`): `621d2d700649c84f955bd44669cd180b35fa86e3d78ccc3ea12b71e5d5dc43f6`
- cited in: node.lean, record TFQ-1293
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `CampaignGenesisContextDecision`): recorded sha256 `621d2d700649c84f955bd44669cd180b35fa86e3d78ccc3ea12b71e5d5dc43f6` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGenesisContextDecision`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGenesisContextDecision.collapseTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.collapseTest_correct` |

- counts toward the grade: yes

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1293
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pairwiseSeparated_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms pairwiseSeparated_iff` |
| `two_marks_without_forms_collapsed` | yes | yes | yes | Quot.sound, propext | `#print axioms two_marks_without_forms_collapsed` |
| `unarySep_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms unarySep_iff` |

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

### Documents and data: `dag/derivations/29_computation/tfq_1293_comp_c3_context_decision_partial.md`

- file: [dag/derivations/29_computation/tfq_1293_comp_c3_context_decision_partial.md](../../../dag/derivations/29_computation/tfq_1293_comp_c3_context_decision_partial.md)
- sha256 (`lf-normalised`): `d5096df113159d1be9025cd6d5ade2edebfa4fc85894fbc18d1bfc675c01f23b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1293
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C3-CONTEXT-DECISION-PARTIAL` `GAP_NO_DERIVATION`: [COMP-C3-BOUNDED-REACH-DECIDABLE](COMP-C3-BOUNDED-REACH-DECIDABLE.md) (PROVED_LEAN), [PGW-CONTEXT-DECISION-PROCEDURE](PGW-CONTEXT-DECISION-PROCEDURE.md) (OPEN)

Outgoing (0):

