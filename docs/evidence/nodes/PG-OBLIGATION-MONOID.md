# PG-OBLIGATION-MONOID

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Obligation counter vectors Fin k -\> Nat under pointwise sum form the free commutative monoid on k obligation ids (cancellative, not a group for k \>= 1); with a count bound the checked combine is associative with equal definedness on both bracketings; a re-declared copy of the source four-event, three-counter trace is a monoid homomorphism from event lists, and in an unbounded k-id ledger model every successful generate/discharge run from the empty ledger ends valid. That Genesis events or S(n) maps carry generated/discharged vectors as monoid morphisms (TFQ-0342) is not established.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 28
- distinct cited Lean declarations covered by a current replay receipt: 28
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Genesis events and S(n) maps carrying context-independent generated/discharged vectors (PG-GAP-EVENT-OBLIGATION, TFQ-0342); Ev/evOb is a copy of the source table, not derived, and is unlinked by any theorem to PrimGenEvent/eventObligation; the Lean abstract-k ledger is unlinked to the three-id u64 Python/Rust ledger.

## Source status

WDP-CH03-P02, P03 MECHANIZED in DerivationDagQMClosure.lean and Rust witness

## Review

- PFP review: [dag/results/PG-OBLIGATION-MONOID/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-OBLIGATION-MONOID/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Obligation counters under pointwise sum are the free commutative monoid on the ids (cancellative, not a group); the re-declared copy of the source four-event three-counter trace is a homomorphism from event lists with total cost equal to length; in the abstract unbounded k-id model every successful generate/discharge run from the empty ledger keeps discharged within generated and a discharge succeeds exactly when it fits the outstanding count; Genesis events and S(n) maps being morphisms remains unproved.
  - does not support: That Genesis events or S(n) maps are monoid morphisms into the obligation monoid (TFQ-0342, PG-GAP-EVENT-OBLIGATION): the event-to-vector table evOb is copied from the source, not derived, and only lists of the four declared events are covered; any theorem tying Ev/evOb/trace to PrimGenEvent/eventObligation/traceObligation of DerivationDagQMClosure.lean (they are a re-declaration); any theorem connecting the Lean abstract-k unbounded ledger to the three-id u64 Python/Rust ledger; the Rust crate itself (nothing in omega_kernel is executed); unbounded or string-keyed ids; any claim that the 3-counter vector equals the free monoid on the real obligation ids.
  - next test: Derive from the actual Genesis event and S(n)-map definitions (not the four-event table) that each step adds a fixed generated and discharged vector independent of context, i.e. that sequential composition maps to combine, or exhibit an event whose vector depends on the preceding trace.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor` |
| `QuantumMechanics.DerivationDagQMClosure.traceObligation_append` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.traceObligation_append` |

- counts toward the grade: yes

### Lean: `lean4/ObligationMonoid.lean`

- file: [lean4/ObligationMonoid.lean](../../../lean4/ObligationMonoid.lean)
- sha256 (`bytes`): `b5afec8bddd5021a809a91368fa00e26538962fce7a27f1e1acd08f3e79ac1c5`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (ObligationMonoid)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `ObligationMonoid`): recorded sha256 `b5afec8bddd5021a809a91368fa00e26538962fce7a27f1e1acd08f3e79ac1c5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ObligationMonoid`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ObligationMonoid.combineB_assoc` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.combineB_assoc` |
| `ObligationMonoid.combine_assoc` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.combine_assoc` |
| `ObligationMonoid.combine_cancel` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.combine_cancel` |
| `ObligationMonoid.combine_comm` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.combine_comm` |
| `ObligationMonoid.combine_empty` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.combine_empty` |
| `ObligationMonoid.cost_floor` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.cost_floor` |
| `ObligationMonoid.discharge_never_generated` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.discharge_never_generated` |
| `ObligationMonoid.discharge_ok_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.discharge_ok_iff` |
| `ObligationMonoid.discharge_valid` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.discharge_valid` |
| `ObligationMonoid.event_table_not_injective` | yes | yes | yes | propext | `#print axioms ObligationMonoid.event_table_not_injective` |
| `ObligationMonoid.genB_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ObligationMonoid.genB_none_iff` |
| `ObligationMonoid.genB_valid` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.genB_valid` |
| `ObligationMonoid.lift_single` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ObligationMonoid.lift_single` |
| `ObligationMonoid.lift_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ObligationMonoid.lift_unique` |
| `ObligationMonoid.no_inverse` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.no_inverse` |
| `ObligationMonoid.over_discharge_needs_generated` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.over_discharge_needs_generated` |
| `ObligationMonoid.overdischarge_instance` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.overdischarge_instance` |
| `ObligationMonoid.run_from_empty_valid` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.run_from_empty_valid` |
| `ObligationMonoid.run_valid` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.run_valid` |
| `ObligationMonoid.trace_append` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.trace_append` |
| `ObligationMonoid.trace_assertions` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.trace_assertions` |
| `ObligationMonoid.trace_destructive` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.trace_destructive` |
| `ObligationMonoid.trace_swap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ObligationMonoid.trace_swap` |
| `ObligationMonoid.trace_terms` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.trace_terms` |
| `ObligationMonoid.trace_total` | yes | yes | yes | Quot.sound, propext | `#print axioms ObligationMonoid.trace_total` |
| `ObligationMonoid.valid_fresh_order_blind` | yes | yes | yes | propext | `#print axioms ObligationMonoid.valid_fresh_order_blind` |

- counts toward the grade: yes

### Documents and data: `.claude/rules/authority/rl_gtla_rules_rubric.md`

- file: `.claude/rules/authority/rl_gtla_rules_rubric.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md`

- file: [dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md](../../../dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md)
- sha256 (`lf-normalised`): `3c5506026eeada78ccc327f0bd2ee297d044bb4e3c6fc875975ee080d25bacb1`
- generated view: listed, not counted
- cited in: record TFQ-0342 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:5c5cb8a52c5879da00a72654ee0c47e551e4839cb3b2cee5daa00557af3c58d8::ObligationError`
- `external:sha256:5c5cb8a52c5879da00a72654ee0c47e551e4839cb3b2cee5daa00557af3c58d8::ObligationId`
- `external:sha256:5c5cb8a52c5879da00a72654ee0c47e551e4839cb3b2cee5daa00557af3c58d8::Obligations`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_wdp_obligations_and_growth_witness`
- `external:sha256:7728578ae5d0dac8e95aa86964e9d32cb0db2b72757ba9460b7aad180d489780`

## Absences recorded by the TFQ records

- TFQ-0342 rust: no local rust twin located for external:sha256:5c5cb8a52c5879da00a72654ee0c47e551e4839cb3b2cee5daa00557af3c58d8

## Routes

Incoming (1):

- `PG-R-GAP-EVENT-OBLIGATION` `DERIVED_LEAN`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PG-SN-CARRIER](PG-SN-CARRIER.md) (PROVED_LEAN)

Outgoing (1):

- `PG-R-GENESIS-TO-WDP` `GAP_NO_DERIVATION`: [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN)
