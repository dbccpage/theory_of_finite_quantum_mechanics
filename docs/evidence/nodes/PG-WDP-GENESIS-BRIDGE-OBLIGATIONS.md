# PG-WDP-GENESIS-BRIDGE-OBLIGATIONS

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Five open bridge obligations (register rows GEN-WDP-O01..O05): O01 carrier/signature/law/challenge-generation floor; O02 source transition/admission systems to the WDP bridge by preservation/reflection maps; O03 dynamic carrier transport and higher fillers; O04 effect/probability, scalar and Hilbert choices; O05 governance refinement. Narrowed finite case, status left OPEN: on any finite window, symmetrised adjacency is false at a pair exactly when both directed adjacencies are false; on two vertices that symmetrisation is not a directed-step certificate, since edge01 and edge10 differ as directed steps and both have pair-defect true at (0,1); the identity on adjacency is a directed-step certificate on every finite window; and no positive integers p, q satisfy p * p = 2 * q * q, with the numerical case 1 * 1 = 1 and 2 * 1 * 1 = 2. O01, O03, O04, O05, and the existence of an O02 map from a source admission system stay open.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 33
- cited Lean declaration references covered by a current replay receipt: 32
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 4
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (4 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/WdpBridgeObligations.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

O01..O05 remain open in the register. CampaignPgwWdpBridgeObligations records the symmetrised-adjacency candidate only: it is not a directed-step certificate, while the identity on adjacency is one, so O02 is not refuted. The integer relation p * p = 2 * q * q has no positive solution and is not the O04 scalar or Hilbert choice. No source admission system is given a preservation map.

## Source status

GEN-WDP-O01..O05 five-obligation Genesis-to-WDP bridge gate, GEN-WDP-46/70 observer completion dimension decomposition, GEN-WDP-42/45 two-event causal diamond price-curl flatness vs assertion-fee curl, and GEN-WDP-68 rational scalar norm obstruction mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/PG-WDP-GENESIS-BRIDGE-OBLIGATIONS/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-WDP-GENESIS-BRIDGE-OBLIGATIONS/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: In a three-status ledger model in which end-to-end is defined as all five discharged, scoped controls passing for all five obligations do not make the end-to-end claim hold, which holds exactly when all five are discharged; the node reading (all five control-only) is therefore not end-to-end; ledger bookkeeping only, no obligation is discharged.
  - does not support: That any of O01..O05 is discharged, dischargeable or refutable; the truth of any end-to-end bridge claim; any independent semantics of "end-to-end" beyond the definitional conjunction; that the register status of O01..O05 is control-only: the register labels each OPEN, and Open/ControlOnly/Discharged and the all-ControlOnly vector 11111 are this node's reading of the node statement (scoped controls done, end-to-end not); that no_sq_eq_two_sq bears on O04; the programme order as a logical dependency; Hilbert, Born, scalar or governance choices; any physical or institutional interpretation.
  - next test: For O02, the only concrete candidate map in hand is the symmetrised adjacency of a finite window: choose an orientation-sensitive source transition system on FiniteGenesisWindow and prove or refute that wdpPairDefect is a preservation-and-reflection morphism for it (pairDefect_forgets_orientation already refutes it for orientation-sensitive transitions); record the outcome as the first falsifier on the O02 row.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpBridgeObligations.lean`

- file: [lean4/CampaignPgwWdpBridgeObligations.lean](../../../lean4/CampaignPgwWdpBridgeObligations.lean)
- sha256 (`bytes`): `8d3358fa30d4b9a910101b4e49d925725239f47ecce5dec3f8de1ab238b6d026`
- cited in: node.lean, node.source, receipt dag/research/campaign_pg-wdp-genesis-bridge-obligations_lean_replay.json (CampaignPgwWdpBridgeObligations)
- replay: `verified`
  - receipt [dag/research/campaign_pg-wdp-genesis-bridge-obligations_lean_replay.json](../../../dag/research/campaign_pg-wdp-genesis-bridge-obligations_lean_replay.json) (module `CampaignPgwWdpBridgeObligations`): recorded sha256 `8d3358fa30d4b9a910101b4e49d925725239f47ecce5dec3f8de1ab238b6d026` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpBridgeObligations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignPgwWdpBridgeObligations.idAdj_is_certificate` | yes | yes | yes | none | `#print axioms CampaignPgwWdpBridgeObligations.idAdj_is_certificate` |
| `CampaignPgwWdpBridgeObligations.no_sq_at_one` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpBridgeObligations.no_sq_at_one` |
| `CampaignPgwWdpBridgeObligations.no_sq_eq_two_sq` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpBridgeObligations.no_sq_eq_two_sq` |
| `CampaignPgwWdpBridgeObligations.one_sq_ne_two` | yes | yes | yes | none | `#print axioms CampaignPgwWdpBridgeObligations.one_sq_ne_two` |
| `CampaignPgwWdpBridgeObligations.one_sq_values` | yes | yes | yes | none | `#print axioms CampaignPgwWdpBridgeObligations.one_sq_values` |
| `CampaignPgwWdpBridgeObligations.pairDefect_false_iff` | yes | yes | yes | propext | `#print axioms CampaignPgwWdpBridgeObligations.pairDefect_false_iff` |
| `CampaignPgwWdpBridgeObligations.pairDefect_not_directed_step_certificate` | yes | yes | yes | propext | `#print axioms CampaignPgwWdpBridgeObligations.pairDefect_not_directed_step_certificate` |
| `CampaignPgwWdpBridgeObligations.some_certificate_exists` | yes | yes | yes | none | `#print axioms CampaignPgwWdpBridgeObligations.some_certificate_exists` |
| `CampaignPgwWdpBridgeObligations.witness_orientation_swap` | yes | yes | yes | propext | `#print axioms CampaignPgwWdpBridgeObligations.witness_orientation_swap` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor` |
| `QuantumMechanics.DerivationDagQMClosure.genesis_to_wdp_bridge_preserves_and_reflects` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.genesis_to_wdp_bridge_preserves_and_reflects` |
| `QuantumMechanics.DerivationDagQMClosure.pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl` |
| `QuantumMechanics.DerivationDagQMClosure.pg_wdp_genesis_bridge_o03_o05_coherence_readout_and_standing_separation` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_wdp_genesis_bridge_o03_o05_coherence_readout_and_standing_separation` |

- counts toward the grade: yes

### Lean: `lean4/WdpBridgeObligations.lean`

- file: [lean4/WdpBridgeObligations.lean](../../../lean4/WdpBridgeObligations.lean)
- sha256 (`bytes`): `7993025b4054eac17f890e5f07649f18ef8adbf9826d86015667d4f10dcbfbc5`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (WdpBridgeObligations)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `WdpBridgeObligations`): recorded sha256 `7993025b4054eac17f890e5f07649f18ef8adbf9826d86015667d4f10dcbfbc5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WdpBridgeObligations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WdpBridgeObligations.bool_and_iff` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.bool_and_iff` |
| `WdpBridgeObligations.card_vectors` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.card_vectors` |
| `WdpBridgeObligations.control_only_not_discharged` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.control_only_not_discharged` |
| `WdpBridgeObligations.endToEnd_five` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.endToEnd_five` |
| `WdpBridgeObligations.endToEnd_iff_controls_and_no_control` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.endToEnd_iff_controls_and_no_control` |
| `WdpBridgeObligations.endToEnd_iff_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.endToEnd_iff_count` |
| `WdpBridgeObligations.endToEnd_mono` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.endToEnd_mono` |
| `WdpBridgeObligations.endToEnd_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.endToEnd_unique` |
| `WdpBridgeObligations.le_raise` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.le_raise` |
| `WdpBridgeObligations.no_sq_eq_two_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.no_sq_eq_two_sq` |
| `WdpBridgeObligations.not_endToEnd_of_not_discharged` | yes | yes | yes | none | `#print axioms WdpBridgeObligations.not_endToEnd_of_not_discharged` |
| `WdpBridgeObligations.pairDefect_forgets_orientation` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.pairDefect_forgets_orientation` |
| `WdpBridgeObligations.pairDefect_preserves_and_reflects` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.pairDefect_preserves_and_reflects` |
| `WdpBridgeObligations.prefixOrder_of_endToEnd` | yes | yes | yes | none | `#print axioms WdpBridgeObligations.prefixOrder_of_endToEnd` |
| `WdpBridgeObligations.prefixOrder_violation` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.prefixOrder_violation` |
| `WdpBridgeObligations.raise_completes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.raise_completes` |
| `WdpBridgeObligations.raise_preserves_endToEnd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpBridgeObligations.raise_preserves_endToEnd` |
| `WdpBridgeObligations.update_sharp` | yes | yes | yes | propext | `#print axioms WdpBridgeObligations.update_sharp` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/examples/genesis_construction.rs`

- file: [code/rust/src/wdp/examples/genesis_construction.rs](../../../code/rust/src/wdp/examples/genesis_construction.rs)
- sha256 (`bytes`): `b081678e9e6b6d570108536cb8dceb80f85fa6bc63b5dd7e4899f334bbf02277`
- cited in: record TFQ-0343
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_admission_execution.rs`

- file: [code/rust/src/wdp/genesis_admission_execution.rs](../../../code/rust/src/wdp/genesis_admission_execution.rs)
- sha256 (`bytes`): `8a4f92fda652d2311116b3aa81b4294d5004c705634966eb6a234be79cb9a475`
- cited in: record TFQ-0343
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pg-wdp-genesis-bridge-obligations.py`

- file: [checks/independent/pg-wdp-genesis-bridge-obligations.py](../../../checks/independent/pg-wdp-genesis-bridge-obligations.py)
- sha256 (`bytes`): `2f064918320e3bf12e04d3702d29335b693d89183030474ab9365f3dd93c632a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0343_leave_gen_wdp_o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md`

- file: [dag/derivations/06_wdp/tfq_0343_leave_gen_wdp_o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md](../../../dag/derivations/06_wdp/tfq_0343_leave_gen_wdp_o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md)
- sha256 (`lf-normalised`): `b2881fb2ff31e99f8713ff8fcfbfd2424cce534a3a348dc5b475bc4db7679cc4`
- generated view: listed, not counted
- cited in: record TFQ-0343
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pg-wdp-genesis-bridge-obligations.md`

- file: [dag/derivations/independent/pg-wdp-genesis-bridge-obligations.md](../../../dag/derivations/independent/pg-wdp-genesis-bridge-obligations.md)
- sha256 (`lf-normalised`): `c73e22aad58838d6fddae46fd9b2789df0daa1c6a051aa0c5c238f8f44c636d4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/plans/goal_dag.jsonl`

- file: `omega_engine_atlas/coda_atlas/F004_papers/plans/goal_dag.jsonl`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `PG-R-GENESIS-TO-WDP` `GAP_NO_DERIVATION`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PG-SN-CARRIER](PG-SN-CARRIER.md) (PROVED_LEAN), [PG-OBLIGATION-MONOID](PG-OBLIGATION-MONOID.md) (PROVED_LEAN)

Outgoing (2):

- `PG-R-GAP-GENESIS-TO-WINDOW` `DERIVED_LEAN`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)
- `PGW-R-WDP-GENESIS-BRIDGES-LEDGER` `DERIVED_PROSE`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION)
