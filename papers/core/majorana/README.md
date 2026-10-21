# 026_microsoft_majorana_problem: Majorana Parity Obstruction Calculus & Topological Computing Apparatus

**AuthorityEffect:** None  
**Paper Key:** `002_projection_obstruction/026_microsoft_majorana_problem`  
**Live directory:** `009_ms_majorana`. Lean `gaussian_elimination_cubic_bound` is `Nat.le_refl` of `n * n * n`. Enum `rfl` declarations are not measured tetron homology.  
**Provenance:** Ingested from `https://github.com/dbccpage/anomalon` at commit `2fa585182063433950bdf513a5b0f3562c08aa76`  
**Date:** 2026-09-19  

---

## 1. Overview and Apparatus Contents

This directory aggregates the Python and Rust Majorana parity obstruction diagnostics, GF(2) boundary complex readout schedules, and topological computing benchmarks originally developed for the Anomalon Omega Engine and Microsoft Azure Quantum topological computing group.

### Directory Layout

0. **Paper Manuscripts & Ledgers**:
   - [`the_majorana_problem.md`](the_majorana_problem.md): Master research monograph on the Microsoft Majorana Problem.
   - [`the_majorana_problem_claim_ledger.md`](the_majorana_problem_claim_ledger.md): Epistemic claim ledger (`MAJ-C1` through `MAJ-C20`; corrected 2026-10-21, this line previously read `MAJ-C17`).
   - [`the_majorana_problem_change_log.md`](the_majorana_problem_change_log.md): Research change log.
   - [`claim_ledger.yaml`](claim_ledger.yaml): Machine-readable YAML claim specifications.

1. **[`omega_majorana`](../../../../omega_engine/crates_rs/omega_majorana)**:
   - Standalone Rust crate for high-throughput GF(2) parity terminalization and topological complex diagnostics.
   - Modules include `classify.rs`, `complexes.rs`, `gf2_terminalizer.rs`, `harmonic.rs`, `holonomy.rs`, `tetron.rs`, and the migrated `braid_action.rs`, `sparse_kitaev.rs`, `multiqubit_braid.rs`, `pauli_noise.rs`.

2. **`code/`**:
   - Python computational engine (`majorana_evaluator.py`, `tests/unit/`, `tests/integration/`, `tests/e2e/`).
   - Consolidated homology and residual calculus engines directly in `code/` (formerly under `math_references/homology_theory` and `math_references/residuals`):
     - Homology theory: `boundary_map.py`, `chain_complex.py`, `cochain_complex.py`, `smith_normal_form.py`, `lefschetz_thimble.py`, `vietoris_rips.py`, `gf2_matrix.py`, etc.
     - Residual calculus: `network_residual.py`, `residuals.py`, `residual_composition.py`.

3. **`lean4/`**:
   - Formal Lake package `po026` containing `MajoranaCore.lean`.
   - Formally verifies $\mathbb{F}_2$ boundary nilpotency, residual trichotomy exclusivity, norm equivalence, and boundary Majorana isolation with zero synthetic axioms.

4. **`contracts/`**:
   - `majorana_operator.contract.yaml`: Operator governance contract for Majorana topological readout.

5. **`docs/`**:
   - Consolidated research memoranda, evidence notes, and certificate artifacts:
     - `microsoft_bridge_note.md`: Technical memorandum for Microsoft Azure Quantum & Topological Computing Group.
     - `majorana_problem_overview.md`: Architectural synthesis and problem boundaries.
     - Certificate ledgers & verification reports: `certificate_ledger.jsonl`, `tetron_homology_report.json`, `ledger_verification.json`, `local_test_receipt.json`, `demo_output.json`.
     - Adversarial dialogues & evidence: `adversarial_trio_deutsch_rovelli_albert_20260801.md`, `finite_qc_repair_wall_code_demo_20260801.md`, `holonomy_plaquette_play_20260801.md`, `kill_criteria_impl_and_archive_sample_20260801.md`, `majorana_play_qc_bridge_20260801.md`, `play_projection_obstruction_downfall_of_llms_and_qc_20260801.md`.

### Native computation

The migrated Python entry points retain their data carriers, receipt formatting,
and experiment orchestration. Their mathematical operations execute in the
canonical Rust crates through `RustSymbolGameHost`. There is no Python solver
fallback when the native host is missing, refuses an input, or times out.

| Paper source | Native owner |
|---|---|
| `code/majorana_braid_exact.py` | `omega_majorana::braid_action`; general rational matrix operations use `linear_algebra::exact_field` |
| `code/kitaev_chain_exact.py` | `omega_majorana::sparse_kitaev` |
| `code/majorana_multiqubit_noise.py` | `omega_majorana::{multiqubit_braid,pauli_noise}` |
| `code/majorana_noise_sweep.py` | `omega_majorana::pauli_noise::DeterministicRationalNoiseGenerator`; sweep orchestration remains in Python |
| `code/{qmatrix,exact_solve}.py` and the HPT matrix carrier | `linear_algebra::exact_field::{matrix,elimination}` |
| `code/gf2_matrix.py` and `code/majorana/core/gf2_matrix.py` | `omega_number_theory::gf2`; the two Python entry points share one adapter |
| `code/homological_perturbation.py` | `omega_homology::homological_perturbation` |
| `code/transfer.py` | `omega_functional::projection_transfer` |
| `code/family_bound.py` | `omega_functional::finite_family_bound` |
| `code/majorana_evaluator.py` schedule and tetron report; `code/majorana/core/gf2_diagnostic.py` | `omega_majorana::{classify, tetron, lggr, repair_capacity}` through host action `majorana_gf2_diagnostic` |

`majorana_gf2_diagnostic` is dispatched from `omega_symbol_game` `invoke/majorana_math.rs`. The crate terminal `TypedHarmonic` stays spelled that way. The evaluator's public trichotomy reports that certified class as `ClosedResidual` and keeps `native_terminal`. `TetronCarrier.code_distance` is the paper's declared label (`rows + 1` on a cylinder, `min(rows, cols)` on a torus), not a measured distance. Float phenomenological probes in `majorana_evaluator.py` stay Python and are not crate theorems. The manuscript text is unchanged. AuthorityEffect: None.

The existing ooutwire transfer and finite-family programs also consume these
functional owners. Their public program receipts stay in ooutwire, while the
shared rational calculations have one implementation in `omega_functional`.

Build the host from `omega_engine/crates_rs` before running these Python entry
points:

```sh
cargo build -j 1 -p omega_symbol_game --bin omega_symbol_game
```

The canonical process adapter finds the workspace binary, or accepts its path
through `OMEGA_SYMBOL_GAME_HOST`. Inputs and coefficient outputs use canonical
rational strings. Malformed exact values and exhausted resource bounds produce
typed refusals. The wire limits dense matrices to dimension 256 and synthesized
braid words to 4,096 steps. Functional requests allow at most 4,096 family
members, rates, or vector entries; the sparse Rust APIs have their own declared
bounds.

The migration preserves the paper's braid row convention, seeded random draw
order, rational noise thresholds, and arbitrary rational noise transforms.
The Kitaev API's historical real-valued `commutator_with_mode` returns
`i[H,gamma]`; the sparse owner and independent Fock comparisons use that
convention explicitly. Isolated coordinate modes and the historical diagnostic
field names describe the declared finite model.

Homological perturbation now checks both differentials, both chain maps, the
homotopy equation, and all normalized side conditions before transfer. Legacy
flags cannot bypass these checks. Successful transfer returns the complete
checked perturbed contraction. Contraction hashes include the target
differentials; Python receipt digests also include the retained native outcome.
Invalid normalization, a non-square-zero perturbation, and singular resolvents
remain distinct outcomes. A zero sampling scale yields exact zero noise;
negative scales and tolerances refuse.

This migration does not retire the whole paper source tree. The evaluator,
Lefschetz, graph/residual, replica, and presentation programs outside the table
still require a separate ownership and caller audit. Structural Python mirrors
that already refer to native modules are not new computational ports.

The scoped build, test commands, and source hashes are recorded in
[`docs/native_migration_receipt.json`](docs/native_migration_receipt.json).

---

## 2. Epistemic Claim Hygiene Discipline

Under the repository Claim Hygiene Rule:

- All theorems and algorithms operate strictly on declared, finite, simulated chain complexes over $\mathbb{GF}(2)$ and algebraic number fields $\mathbb{Q}(\zeta_{16})$.
- These algebraic certificates do not constitute empirical or hardware performance assertions regarding physical NISQ or topological devices.
- `AuthorityEffect: None`.

<!-- BEGIN UNIFIED-DAG-BACKLINKS -->
<!-- Generated by papers/core/tools/build_corpus_dag_backlinks.py; edit the tool, not this region. -->

## Unified DAG

Audit of 2026-10-21. The unified derivation DAG (`dag/fragments/unified_dag.json`) folds the records of this corpus into one graph: a record with no trunk counterpart is a NEW application-branch node with its own TFQ record; a restatement of a trunk step is an ALIAS row that points to the trunk node. *Source claimed* is the status the source asserted; *Audited* is the status the audit assigned against what is actually in this checkout (Lean declarations resolved, replays rerun, statements compared). The original claims, labels and text of this document are kept unchanged. A status below the source claim means the claim is not established as stated; it does not mean the underlying mathematics is false (only REFUTED means that). For an ALIAS row the audited column is the status of the trunk node, which is the authority for the restated step. Regenerate with `python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py`.

46 NEW records and 3 ALIAS rows; 29 same, 13 lowered, 1 raised, 3 reclassified.

| Source id | Kind | TFQ record | DAG node | Source claimed | Audited | Reconciliation |
|---|---|---|---|---|---|---|
| `MAJ-C1` | NEW | [TFQ-1162](../../../dag/derivations/28_majorana/tfq_1162_maj_realization_packet_gap.md) | `MAJ-REALIZATION-PACKET-GAP` | DEFINITION | **DEFINITION** | same |
| `MAJ-C2` | NEW | [TFQ-1141](../../../dag/derivations/28_majorana/tfq_1141_maj_trichotomy_pairwise_exclusion.md) | `MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-C3` | NEW | [TFQ-1143](../../../dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md) | `MAJ-TRICHOTOMY-ELIMINATION-DECISION` | COMPUTATIONALLY_CHECKED | **PROVED_PROSE** | raised |
| `MAJ-C4` | NEW | [TFQ-1144](../../../dag/derivations/28_majorana/tfq_1144_maj_nilpotency_refusal.md) | `MAJ-NILPOTENCY-REFUSAL` | PROVED_LEAN | **DEFINITION** | reclassified |
| `MAJ-C5` | NEW | [TFQ-1150](../../../dag/derivations/28_majorana/tfq_1150_maj_surface_shadow_fence.md) | `MAJ-SURFACE-SHADOW-FENCE` | DEFINITION | **DEFINITION** | same |
| `MAJ-C6` | NEW | [TFQ-1167](../../../dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md) | `MAJ-IMPORT-KITAEV-CHAIN` | DEFINITION | **IMPORTED_ASSUMPTION** | reclassified |
| `MAJ-C7` | NEW | [TFQ-1170](../../../dag/derivations/28_majorana/tfq_1170_maj_import_ising_anyons.md) | `MAJ-IMPORT-ISING-ANYONS` | DEFINITION | **IMPORTED_ASSUMPTION** | reclassified |
| `MAJ-C8` | NEW | [TFQ-1173](../../../dag/derivations/28_majorana/tfq_1173_maj_parity_observable_fence.md) | `MAJ-PARITY-OBSERVABLE-FENCE` | DEFINITION | **DEFINITION** | same |
| `MAJ-C9` | ALIAS | [TFQ-0409](../../../dag/derivations/26_fsp/tfq_0409_fsp_efficient_sampling_obligations.md) | `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` | FENCED | **OPEN** | restated in trunk |
| `MAJ-C10` | NEW | [TFQ-1165](../../../dag/derivations/28_majorana/tfq_1165_maj_hardware_narrative_quarantine.md) | `MAJ-HARDWARE-NARRATIVE-QUARANTINE` | DEFINITION | **DEFINITION** | same |
| `MAJ-C11` | NEW | [TFQ-1146](../../../dag/derivations/28_majorana/tfq_1146_maj_lggr_torus_instance.md) | `MAJ-LGGR-TORUS-INSTANCE` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MAJ-C12` | ALIAS | [TFQ-0184](../../../dag/derivations/22_implementation_sibling/tfq_0184_do_not_read_paper_009_reflexivity_declarations_as_measured_tetron_homology.md) | `TFQ-0184` | VERIFIED | **OPEN** | restated in trunk |
| `MAJ-C13` | NEW | [TFQ-1154](../../../dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md) | `MAJ-LEGACY-CARRIER-RETRACTION` | PROVED_LEAN | **CONDITIONAL** | lowered |
| `MAJ-C14` | NEW | [TFQ-1155](../../../dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md) | `MAJ-TORUS-3X4-COSET-WEIGHTS` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-C15` | NEW | [TFQ-1158](../../../dag/derivations/28_majorana/tfq_1158_maj_phi1_syndrome_decoding.md) | `MAJ-PHI1-SYNDROME-DECODING` | PROVED_LEAN | **CONDITIONAL** | lowered |
| `MAJ-C16` | NEW | [TFQ-1160](../../../dag/derivations/28_majorana/tfq_1160_maj_torus_6x6_benchmark.md) | `MAJ-TORUS-6X6-BENCHMARK` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-C17` | NEW | [TFQ-1161](../../../dag/derivations/28_majorana/tfq_1161_maj_lp_invariance_binary.md) | `MAJ-LP-INVARIANCE-BINARY` | PROVED_LEAN | **PROVED_PROSE** | lowered |
| `MAJ-C18` | NEW | [TFQ-1177](../../../dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md) | `MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` | PROVED_LEAN | **OPEN** | lowered |
| `MAJ-C19` | NEW | [TFQ-1178](../../../dag/derivations/28_majorana/tfq_1178_maj_open_non_markovian_envelope.md) | `MAJ-OPEN-NON-MARKOVIAN-ENVELOPE` | PROVED_LEAN | **OPEN** | lowered |
| `MAJ-C20` | NEW | [TFQ-1179](../../../dag/derivations/28_majorana/tfq_1179_maj_open_multiterminal_envelope.md) | `MAJ-OPEN-MULTITERMINAL-ENVELOPE` | PROVED_LEAN | **OPEN** | lowered |
| `MAJ-CLAIM-DISTANCE-FAMILY` | NEW | [TFQ-1156](../../../dag/derivations/28_majorana/tfq_1156_maj_open_distance_family.md) | `MAJ-OPEN-DISTANCE-FAMILY` | PROVED_PROSE | **OPEN** | lowered |
| `MAJ-COMP-BUDGET-CAP` | NEW | [TFQ-1159](../../../dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md) | `MAJ-CAPPED-COSET-SEARCH` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-COMP-SYNDROME-READOUT` | NEW | [TFQ-1164](../../../dag/derivations/28_majorana/tfq_1164_maj_syndrome_readout_inadequate.md) | `MAJ-SYNDROME-READOUT-INADEQUATE` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-COMP-TETRON-BETTI` | NEW | [TFQ-1152](../../../dag/derivations/28_majorana/tfq_1152_maj_tetron_betti_computed.md) | `MAJ-TETRON-BETTI-COMPUTED` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-COR-DISTANCE-WEIGHT` | NEW | [TFQ-1148](../../../dag/derivations/28_majorana/tfq_1148_maj_distance_weight_correction.md) | `MAJ-DISTANCE-WEIGHT-CORRECTION` | PROVED_PROSE | **OPEN** | lowered |
| `MAJ-DEF-DETECTOR-INADEQUATE` | NEW | [TFQ-1163](../../../dag/derivations/28_majorana/tfq_1163_maj_detector_inadequate.md) | `MAJ-DETECTOR-INADEQUATE` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-PARITY-SCHEDULE` | NEW | [TFQ-1138](../../../dag/derivations/28_majorana/tfq_1138_maj_f2_parity_schedule.md) | `MAJ-F2-PARITY-SCHEDULE` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-PHI1-F2` | NEW | [TFQ-1140](../../../dag/derivations/28_majorana/tfq_1140_maj_phi1_hamming_coset.md) | `MAJ-PHI1-HAMMING-COSET` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-TETRON-CARRIER` | NEW | [TFQ-1151](../../../dag/derivations/28_majorana/tfq_1151_maj_tetron_array_carrier.md) | `MAJ-TETRON-ARRAY-CARRIER` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-TRICHOTOMY-LABELS` | NEW | [TFQ-1139](../../../dag/derivations/28_majorana/tfq_1139_maj_trichotomy_labels.md) | `MAJ-TRICHOTOMY-LABELS` | DEFINITION | **DEFINITION** | same |
| `MAJ-EX-TORUS-2X2` | NEW | [TFQ-1145](../../../dag/derivations/28_majorana/tfq_1145_maj_torus_2x2_worked_grid.md) | `MAJ-TORUS-2X2-WORKED-GRID` | PROVED_PROSE | **COMPUTATIONALLY_CHECKED** | lowered |
| `MAJ-FENCE-DIAGNOSTIC-LABELS` | ALIAS | - | `DS-QM212-MAJORANA-PROBLEM` | - | **PROVED_LEAN** | restated in trunk |
| `MAJ-FENCE-NONCLAIMS` | NEW | [TFQ-1166](../../../dag/derivations/28_majorana/tfq_1166_maj_binding_nonclaims.md) | `MAJ-BINDING-NONCLAIMS` | DEFINITION | **DEFINITION** | same |
| `MAJ-GIN-INVOLUTION-CANCEL` | NEW | [TFQ-1175](../../../dag/derivations/28_majorana/tfq_1175_maj_gin_involution_pair_cancel.md) | `MAJ-GIN-INVOLUTION-PAIR-CANCEL` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-GIN-ROUTING` | NEW | [TFQ-1176](../../../dag/derivations/28_majorana/tfq_1176_maj_gin_terminal_routing.md) | `MAJ-GIN-TERMINAL-ROUTING` | DEFINITION | **DEFINITION** | same |
| `MAJ-IMPORT-BMVT` | NEW | [TFQ-1157](../../../dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md) | `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` | IMPORTED_ASSUMPTION | **IMPORTED_ASSUMPTION** | same |
| `MAJ-ISING-BRAID-CHECK` | NEW | [TFQ-1171](../../../dag/derivations/28_majorana/tfq_1171_maj_ising_braid_exact_open.md) | `MAJ-ISING-BRAID-EXACT-OPEN` | COMPUTATIONALLY_CHECKED | **OPEN** | lowered |
| `MAJ-KITAEV-EDGE-INDEX` | NEW | [TFQ-1168](../../../dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md) | `MAJ-KITAEV-EDGE-INDEX-DISJOINT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-KITAEV-SWEETSPOT-EXACT` | NEW | [TFQ-1169](../../../dag/derivations/28_majorana/tfq_1169_maj_kitaev_sweetspot_exact.md) | `MAJ-KITAEV-SWEETSPOT-EXACT` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MAJ-LEAN-ENVELOPE-NAT` | NEW | [TFQ-1180](../../../dag/derivations/28_majorana/tfq_1180_maj_envelope_nat_arithmetic.md) | `MAJ-ENVELOPE-NAT-ARITHMETIC` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-LEMMA-TRIVIAL-H1` | NEW | [TFQ-1153](../../../dag/derivations/28_majorana/tfq_1153_maj_trivial_h1_no_closed.md) | `MAJ-TRIVIAL-H1-NO-CLOSED` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-MAJORANA-BRAID-YB` | NEW | [TFQ-1172](../../../dag/derivations/28_majorana/tfq_1172_maj_majorana_braid_yb_exact.md) | `MAJ-MAJORANA-BRAID-YB-EXACT` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-OPEN-EVIDENCE-ADEQUACY` | NEW | [TFQ-1182](../../../dag/derivations/28_majorana/tfq_1182_maj_open_evidence_adequacy.md) | `MAJ-OPEN-EVIDENCE-ADEQUACY` | OPEN | **OPEN** | same |
| `MAJ-OPEN-LOCALITY-VIABILITY` | NEW | [TFQ-1149](../../../dag/derivations/28_majorana/tfq_1149_maj_open_lieb_robinson_locality.md) | `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` | OPEN | **OPEN** | same |
| `MAJ-OPEN-LP-DUAL-CEILING` | NEW | [TFQ-1181](../../../dag/derivations/28_majorana/tfq_1181_maj_open_lp_dual_certified_ceiling.md) | `MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING` | OPEN | **OPEN** | same |
| `MAJ-OPEN-POISSON-SCHRODINGER` | NEW | [TFQ-1183](../../../dag/derivations/28_majorana/tfq_1183_maj_open_poisson_schrodinger.md) | `MAJ-OPEN-POISSON-SCHRODINGER` | OPEN | **OPEN** | same |
| `MAJ-PARITY-SECTOR-EXACT` | NEW | [TFQ-1174](../../../dag/derivations/28_majorana/tfq_1174_maj_parity_sector_split_exact.md) | `MAJ-PARITY-SECTOR-SPLIT-EXACT` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-THM-SYNDROME-RECOVERY` | NEW | [TFQ-1147](../../../dag/derivations/28_majorana/tfq_1147_maj_syndrome_recovery_criterion.md) | `MAJ-SYNDROME-RECOVERY-CRITERION` | PROVED_PROSE | **PROVED_PROSE** | same |
| `MAJ-THM-TRICHOTOMY-EXHAUSTIVE` | NEW | [TFQ-1142](../../../dag/derivations/28_majorana/tfq_1142_maj_trichotomy_exhaustive.md) | `MAJ-TRICHOTOMY-EXHAUSTIVE` | PROVED_LEAN | **PROVED_PROSE** | lowered |

<!-- END UNIFIED-DAG-BACKLINKS -->
