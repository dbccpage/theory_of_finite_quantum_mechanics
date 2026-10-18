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
   - [`the_majorana_problem_claim_ledger.md`](the_majorana_problem_claim_ledger.md): Epistemic claim ledger (`MAJ-C1` through `MAJ-C17`).
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
