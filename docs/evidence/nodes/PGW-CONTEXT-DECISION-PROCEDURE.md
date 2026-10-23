# PGW-CONTEXT-DECISION-PROCEDURE

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite Genesis context decision procedure in the existing Regime enumerates every admitted form with all arity-matched slot tuples containing a hole, including multiple holes and uniform all-tuples rule coverage. Collapse and separability are decidable; returned witnesses distinguish, and no witness is equivalent to collapse. Computed profiles coincide exactly for collapsed data, their finite image cardinality equals the cardinality of the observational quotient, holding two is equivalent to at least two classes, and form exhaustion is decidable. First-count existence, Y-2 history-level uniformity necessity and external implementation refinement remain open.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- cited Lean declarations covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

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

### Lean: `lean4/CampaignGenesisContextDecision.lean`

- file: [lean4/CampaignGenesisContextDecision.lean](../../../lean4/CampaignGenesisContextDecision.lean)
- sha256 (`bytes`): `621d2d700649c84f955bd44669cd180b35fa86e3d78ccc3ea12b71e5d5dc43f6`
- cited in: node.lean, receipt dag/research/campaign_pgw-context-decision-procedure_lean_replay.json (CampaignGenesisContextDecision), record TFQ-0497
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `CampaignGenesisContextDecision`): recorded sha256 `621d2d700649c84f955bd44669cd180b35fa86e3d78ccc3ea12b71e5d5dc43f6` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGenesisContextDecision`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGenesisContextDecision.binary_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.binary_separation` |
| `CampaignGenesisContextDecision.classCount_eq_quotient_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.classCount_eq_quotient_card` |
| `CampaignGenesisContextDecision.collapseTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.collapseTest_correct` |
| `CampaignGenesisContextDecision.exhaustionTest_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.exhaustionTest_correct` |
| `CampaignGenesisContextDecision.explicit_class_counts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.explicit_class_counts` |
| `CampaignGenesisContextDecision.full_context_decides_holding` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.full_context_decides_holding` |
| `CampaignGenesisContextDecision.holdsTwo_iff_classCount` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.holdsTwo_iff_classCount` |
| `CampaignGenesisContextDecision.mem_classes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.mem_classes` |
| `CampaignGenesisContextDecision.mem_contexts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.mem_contexts` |
| `CampaignGenesisContextDecision.mem_options` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.mem_options` |
| `CampaignGenesisContextDecision.mem_profile` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.mem_profile` |
| `CampaignGenesisContextDecision.mem_slotTuples` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.mem_slotTuples` |
| `CampaignGenesisContextDecision.multi_hole_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.multi_hole_witness` |
| `CampaignGenesisContextDecision.profile_eq_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.profile_eq_iff` |
| `CampaignGenesisContextDecision.quotientProfile_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.quotientProfile_injective` |
| `CampaignGenesisContextDecision.separable_iff_not_collapsed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.separable_iff_not_collapsed` |
| `CampaignGenesisContextDecision.uniform_rule_exhausted` | yes | yes | yes | propext | `#print axioms CampaignGenesisContextDecision.uniform_rule_exhausted` |
| `CampaignGenesisContextDecision.uniform_rule_merges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.uniform_rule_merges` |
| `CampaignGenesisContextDecision.witness_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.witness_none_iff` |
| `CampaignGenesisContextDecision.witness_sound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGenesisContextDecision.witness_sound` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-context-decision-procedure.py`

- file: [checks/independent/pgw-context-decision-procedure.py](../../../checks/independent/pgw-context-decision-procedure.py)
- sha256 (`bytes`): `5330a7fb0d052d5438055f0ed034e7d2f82872d9845558a3ed09e325d9b020fa`
- cited in: record TFQ-0497

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0497_context_decision_procedure.md`

- file: [dag/derivations/02_genesis/tfq_0497_context_decision_procedure.md](../../../dag/derivations/02_genesis/tfq_0497_context_decision_procedure.md)
- sha256 (`lf-normalised`): `e417e63b8844da817ad8244f22355070406390f3aa1d7d5389d8bf2d4e1afbd8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0497
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-context-decision-procedure.md`

- file: [dag/derivations/independent/pgw-context-decision-procedure.md](../../../dag/derivations/independent/pgw-context-decision-procedure.md)
- sha256 (`lf-normalised`): `36b426be2b4a346e353993091ed47d351606bfebd15f58877e9f13e14f424224`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::separable`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::contexts`

## Routes

Incoming (1):

- `PGW-R-CONTEXT-DECISION-PROCEDURE` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (3):

- `APP-R-AUTHF-CLASS-RELATIVE-TRANSPORT` `DERIVED_LEAN`: [AUTHF-CLASS-RELATIVE-TRANSPORT](AUTHF-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN)
- `APP-R-AUTHF-RICE-GODEL-OPEN` `GAP_NO_DERIVATION`: [AUTHF-RICE-GODEL-OPEN](AUTHF-RICE-GODEL-OPEN.md) (OPEN)
- `APP-R-COMP-C3-CONTEXT-DECISION-PARTIAL` `GAP_NO_DERIVATION`: [COMP-C3-CONTEXT-DECISION-PARTIAL](COMP-C3-CONTEXT-DECISION-PARTIAL.md) (OPEN)
