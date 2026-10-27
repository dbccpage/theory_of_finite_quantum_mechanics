# PGW-CONTEXT-DECISION-PROCEDURE

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite Genesis context decision procedure in the existing Regime enumerates every admitted form with all arity-matched slot tuples containing a hole, including multiple holes and uniform all-tuples rule coverage. Collapse and separability are decidable; returned witnesses distinguish, and no witness is equivalent to collapse. Computed profiles coincide exactly for collapsed data, their finite image cardinality equals the cardinality of the observational quotient, holding two is equivalent to at least two classes, and form exhaustion is decidable. First-count existence, Y-2 history-level uniformity necessity and external implementation refinement remain open.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 23
- distinct cited Lean declarations covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The finite context, class-count, holding-two and exhaustion clauses have local Lean evidence for arbitrary finite regimes in the declared slot/all-tuples-rule language. The bundled node remains OPEN for first-count existence, Y-2 necessity and the external Python/Rust refinement; the earlier unary-only mirror is not used as a full context decider.

## Source status

continuation.txt §13 decision procedure over contexts (X-1); §7 count of observational classes

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisContextDecision.lean`

- file: [lean4/GenesisContextDecision.lean](../../../lean4/GenesisContextDecision.lean)
- sha256 (`bytes`): `b7d4a08565d18dacd9f3d4f82aa953360601a80ed7ede33392b9d477622f81ed`
- cited in: node.lean, receipt dag/research/campaign_pgw-context-decision-procedure_lean_replay.json (GenesisContextDecision), record TFQ-0497
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisContextDecision`): recorded sha256 `b7d4a08565d18dacd9f3d4f82aa953360601a80ed7ede33392b9d477622f81ed` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisContextDecision`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GenesisContextDecision.binary_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisContextDecision.binary_separation` |
| `GenesisContextDecision.classCount_eq_quotient_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.classCount_eq_quotient_card` |
| `GenesisContextDecision.collapseTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.collapseTest_correct` |
| `GenesisContextDecision.exhaustionTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.exhaustionTest_correct` |
| `GenesisContextDecision.explicit_class_counts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.explicit_class_counts` |
| `GenesisContextDecision.full_context_decides_holding` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.full_context_decides_holding` |
| `GenesisContextDecision.holdsTwo_iff_classCount` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.holdsTwo_iff_classCount` |
| `GenesisContextDecision.mem_classes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.mem_classes` |
| `GenesisContextDecision.mem_contexts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.mem_contexts` |
| `GenesisContextDecision.mem_options` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisContextDecision.mem_options` |
| `GenesisContextDecision.mem_profile` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.mem_profile` |
| `GenesisContextDecision.mem_slotTuples` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.mem_slotTuples` |
| `GenesisContextDecision.multi_hole_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms GenesisContextDecision.multi_hole_witness` |
| `GenesisContextDecision.profile_eq_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.profile_eq_iff` |
| `GenesisContextDecision.quotientProfile_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.quotientProfile_injective` |
| `GenesisContextDecision.separable_iff_not_collapsed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.separable_iff_not_collapsed` |
| `GenesisContextDecision.uniform_rule_exhausted` | yes | yes | yes | propext | `#print axioms GenesisContextDecision.uniform_rule_exhausted` |
| `GenesisContextDecision.uniform_rule_merges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.uniform_rule_merges` |
| `GenesisContextDecision.witness_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.witness_none_iff` |
| `GenesisContextDecision.witness_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms GenesisContextDecision.witness_sound` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs)
- sha256 (`bytes`): `f64df9adecf931d7b57907b47c03240742cd710230500c561b4ce14bba7c4d8f`
- cited in: node.rust, record TFQ-0497

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contexts` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0497

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `separable` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-context-decision-procedure.py`

- file: [checks/independent/pgw-context-decision-procedure.py](../../../checks/independent/pgw-context-decision-procedure.py)
- sha256 (`bytes`): `5330a7fb0d052d5438055f0ed034e7d2f82872d9845558a3ed09e325d9b020fa`
- cited in: record TFQ-0497

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0497_context_decision_procedure.md`

- file: [dag/derivations/02_genesis/tfq_0497_context_decision_procedure.md](../../../dag/derivations/02_genesis/tfq_0497_context_decision_procedure.md)
- sha256 (`lf-normalised`): `54bdf76bda2f1126b1961c3c546c3297a11333f878fa37c0b25002ef1ac91bd4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0497
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-context-decision-procedure.md`

- file: [dag/derivations/independent/pgw-context-decision-procedure.md](../../../dag/derivations/independent/pgw-context-decision-procedure.md)
- sha256 (`lf-normalised`): `ac5d9323f037ea3d8fc9250f3458ecd6f7ab53d7d804f75993998cfd8a430940`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `PGW-R-CONTEXT-DECISION-PROCEDURE` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (3):

- `APP-R-AUTHF-CLASS-RELATIVE-TRANSPORT` `DERIVED_LEAN`: [AUTHF-CLASS-RELATIVE-TRANSPORT](AUTHF-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN)
- `APP-R-AUTHF-RICE-GODEL-OPEN` `GAP_NO_DERIVATION`: [AUTHF-RICE-GODEL-OPEN](AUTHF-RICE-GODEL-OPEN.md) (OPEN)
- `APP-R-COMP-C3-CONTEXT-DECISION-PARTIAL` `GAP_NO_DERIVATION`: [COMP-C3-CONTEXT-DECISION-PARTIAL](COMP-C3-CONTEXT-DECISION-PARTIAL.md) (OPEN)
