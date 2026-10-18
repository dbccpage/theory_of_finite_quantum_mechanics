# Comprehensive Survey & Audit Report: Fermion Sign Problem (`papers/core/fsp`)

**Author:** Explorer Survey 2  
**Date:** 2026-10-18  
**Working Directory:** `papers/core/fsp` & target trees (`code/python/src/fsp`, `code/rust/src/`, `lean4/`)  
**AuthorityEffect:** None  

---

## 1. Observation

### 1.1 Structure & Package Assets of `papers/core/fsp`
Direct directory inspection of `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\papers\core\fsp` reveals:
- **Manuscripts & Core Governance:**
  - `the_problem_of_the_fermion_sign.md` (128,269 bytes, 1,166 lines, 17 sections): Master manuscript covering normal-form laws, Hamiltonian provenance, model-derived meron SQL cancellation, Hubbard determinant constructions, and Troyer-Wiese complexity.
  - `the_problem_of_the_fermion_sign_claim_ledger.md` (15,031 bytes): Markdown companion ledger.
  - `the_problem_of_the_fermion_sign_change_log.md` (34,982 bytes): Version 2.4.0 revision changelog.
  - `fermion_sign_problem.md` (7,823 bytes): Canonical relational foundation note framing FSP as CTEs, window quotients, and physical sharding.
  - `theory_of_finite_fsp.md` (80,517 bytes, 806 lines): Complete derivation DAG containing 56 stage-by-stage derivations (`FSP-DERIV-001` through `FSP-DERIV-056`) across 14 stages.
  - `theory_of_finite_fsp.jsonl` (58,401 bytes): 56 machine-readable EADC JSON records.
  - `verification.md` (4,843 bytes): Execution and replay commands.
  - `claim_ledger.yaml` (38,111 bytes, 747 lines): 35 declared claims with scope fences, tests, and Lean 4 references.
  - `verify_deposit.py` (12,846 bytes, 357 lines): Zenodo pre-print deposit verification gate.
  - `.zenodo.json` (1,007 bytes) & `SHA256SUMS` (20,164 bytes): Package deposit metadata and manifest.

- **Subpackages:**
  - `000_meron_sign_problem/`: Self-contained package (v0.1.0) with `paper.md`, `paper_claim_ledger.md`, `code/` (exact oracle, 256 breakup graphs, $Z = 912$), `lean4/` (`MeronCharacter.lean`, `MeronClusterInvolution.lean`), and its own `verify_deposit.py`.
  - `001_hubbard_sign_problem/`: Self-contained package (v0.1.0) with `paper.md`, `paper_claim_ledger.md`, `code/` (`hubbard_exact_model.py`, `hubbard_schema.sql`), and `verify_deposit.py`.

- **Normal Forms (`normal_forms/`):**
  - Contains 32 YAML contract schemas:
    - Classical: `0nf` through `6nf`, `bcnf`, `dknf`, `eknf`, `etnf`, `nf2`.
    - Derivation: `aonf`, `obnf`, `pdnf`, `rpnf`, `scnf`.
    - Physics: `cdt_fermion_sign`, `cdt_kd_doubling`, `cdt_overlap_fermions`, `cdt_susy_witten`, `cdt_topological_charge`, `cdt_zolotarev_overlap`, `wdwnf`.
    - Bridge/Change: `wir_relvar`, `bqnf.fermion_sign`, `bqnf`, `rational_quotient`, `sign_switching`, `gauge`.
  - `fermion_sign_nf_evaluator.py` (595 bytes): Compatibility shim importing `code/fermion_sign_nf_evaluator.py`.

- **Databases (`databases/`):**
  - 8 SQL files: `meron_hubbard.sql` (4,787 bytes), `fermion_gin_index_schema.sql` (6,397 bytes), `regge_wdw_schema.sql` (45,270 bytes), `chiral_superconductor_schema.sql` (7,842 bytes), `kitaev_honeycomb_schema.sql` (8,559 bytes), `fermion_sign_problem.sql` (5,416 bytes), `schema.sql` (963 bytes), and `README.md`.

---

### 1.2 Python Inspection & Duplication Analysis
- **`papers/core/fsp/code/` vs `code/python/src/fsp/`:**
  - `papers/core/fsp/code/` contains 38 Python modules:
    `bf_linked_flux_braiding.py`, `bf_nonabelian_3loop_braiding.py`, `bf_topological_braiding.py`, `bqnf_sign_evaluator.py`, `cdt_fermion_sign_evaluator.py`, `cdt_kd_doubling_evaluator.py`, `cdt_overlap_evaluator.py`, `cdt_susy_witten_evaluator.py`, `cdt_topological_charge_evaluator.py`, `cdt_zolotarev_evaluator.py`, `chiral_anomaly_inflow.py`, `chiral_superconductor_bisimulation_bridge.py`, `chiral_superconductor_evaluator.py`, `cobordism_5d_higher_anomaly.py`, `ct_aux_streaming_gin_engine.py`, `fermion_boson_germ.py`, `fermion_gin_index.py`, `fermion_sign_nf_evaluator.py`, `fermionic_hamiltonian.py`, `fibonacci_anyon_braiding.py`, `foliated_fracton_2gauge_defects.py`, `fqh_laughlin_braiding.py`, `gin_cluster_scaling_benchmark.py`, `hamiltonian_gin_bridge.py`, `higher_2group_gauge_bf.py`, `instanton_dyon_gas_braiding.py`, `ising_majorana_braiding.py`, `kitaev_honeycomb_bisimulation_bridge.py`, `kitaev_honeycomb_evaluator.py`, `pfp_fsp_bridge.py`, `regge_pachner_wdw.py`, `su2_cluster_benchmark_4d.py`, `su2_lattice_gauge.py`, `su2_link_holonomy_4d.py`, `su3_baryon_triality.py`, `su3_polyakov_loop.py`, `su_nc_adjoint_flux.py`, and `__init__.py`.
  - Subdirectories: `sign_sql/` (7 files: `exact_models.py`, `exact_models_receipt.json`, `queries.sql`, `run_sign_sql.py`, `schema.sql`, `seed.sql`, and `tests/`) and `tests/` (15 root test files, plus `e2e/`, `integration/`, `unit/`).
  - **Direct File Comparison via `filecmp`:**
    All 37 non-init Python modules in `papers/core/fsp/code/` and all files in `sign_sql/` and `tests/` are 100% byte-for-byte identical to the corresponding files in `code/python/src/fsp/`.
  - **Key Difference in `__init__.py`:**
    `papers/core/fsp/code/__init__.py` is a 5-line stub (64 bytes).
    `code/python/src/fsp/__init__.py` (138 lines, 4,050 bytes) implements the dual-face interface: `Witness`, `refuse_removed_holonomy`, `refuse_foreign_fixture`, `_star_exchange`, and `_orbit`, precisely matching `code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs`.

- **Critical Python Path Bug in `exact_models.py`:**
  - In `code/python/src/fsp/sign_sql/exact_models.py:19`:
    `BASE = Path(__file__).resolve().parents[2]`
    When located at `code/python/src/fsp/sign_sql/exact_models.py`, `parents[2]` is `code/python/src/`.
  - At line 53:
    `con.executescript((BASE / "databases" / "meron_hubbard.sql").read_text(encoding="utf-8"))`
  - Observation from direct execution:
    ```text
    FileNotFoundError: [Errno 2] No such file or directory: 'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\code\python\src\databases\meron_hubbard.sql'
    ```
    The database file was never migrated to `code/python/src/fsp/databases/` or loaded via `importlib.resources`.

- **Python 3.14 Standard Library Shadowing Bug:**
  - Running pytest directly from `papers/core/fsp` results in:
    ```text
    AttributeError: module 'code' has no attribute 'InteractiveConsole' (consider renaming '.../papers/core/fsp/code/__init__.py' since it has the same name as the standard library module named 'code' and prevents importing that standard library module)
    ```
    This occurs because `pdb.py` in Python 3.14 imports the standard library module `code`. When pytest runs with `code/` in the path, it imports `papers/core/fsp/code/__init__.py` instead.

- **Test Suite Location Mismatch:**
  - `pyproject.toml:18` declares `testpaths = ["code/python/tests"]`.
  - `code/python/tests/` contains only `test_dual_face_majorana_mub_fsp.py` (which passed 8/8 tests in 2.79s).
  - None of the 46 FSP test files in `papers/core/fsp/code/tests` or `code/python/src/fsp/tests/` are currently executed by the root `pytest` command.

---

### 1.3 Rust Inspection & Workspace Status
- **`code/rust/Cargo.toml`:**
  - Lines 1-22 list `workspace.members`:
    `["." , "src/category_theory", "src/combinatorics", "src/finite_probability", "src/functional", "src/fusion_categories", "src/general_relativity", "src/higher_category_theory", "src/holonomy", "src/homotopy_type_theory", "src/lie_theory", "src/local_green_global_red_lggr", "src/majorana", "src/mub", "src/number_theory", "src/operad_theory", "src/sheaf_theory", "src/wdp"]`.
  - `"src/fsp"` is **absent** from `workspace.members`.
  - Lines 57-73 list internal dependencies (`tfqm_majorana`, `tfqm_mub`, `tfqm_wdp`, etc.); `tfqm_fsp` is **absent**.
- **`code/rust/src/lib.rs`:**
  - Exports `pub use tfqm_majorana as majorana;` and `pub use tfqm_mub as mub;`.
  - `fsp` is **not exported**.
  - `crate_root_inventory_holds()` audits `MODULES = &["linear_algebra", "homology", "qm", "dag_witnesses"]`.
- **Existing FSP Implementation in Rust:**
  - Search across `code/rust/` found only one FSP module: `code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs` (323 lines).
  - This file implements Carrier A (4-site star exchange cycle, Jordan-Wigner signs `[-1, 1, 1, -1, 1, 1]`, product `-1`) and Carrier B (one $k=1$ orbit, $Z_u = 0$, $N_u = 2$).
  - There is currently **no `code/rust/src/fsp/` crate** implementing the wider FSP algorithms (Fock space CAR algebra, GIN posting lists, Trotter path generation, BQNF terminal routing, exact Hubbard determinants, or normal form solvers).

---

### 1.4 Lean 4 Inspection & Formalization Status
- **Root `lean4/lakefile.lean`:**
  - Declares package `«FiniteQuantum»` with 147 roots (lines 25-215).
  - **Zero** FSP modules from `papers/core/fsp/lean4/` are declared in `lean4/lakefile.lean`.
- **Root `lean4/` directory:**
  - Contains 196 `.lean` files.
  - Exactly **zero** of the 26 FSP proof files in `papers/core/fsp/lean4/` exist in root `lean4/`.
- **`papers/core/fsp/lean4/` Assets:**
  - Contains 26 `.lean` files:
    1. `BfLinkedFluxBraiding.lean`
    2. `BqnfSignPacket.lean`
    3. `ChiralAnomalyInflow.lean`
    4. `ChiralSuperconductorCore.lean`
    5. `Cobordism5dAnomaly.lean`
    6. `FermionGinCore.lean`
    7. `FermionSignAll.lean`
    8. `FermionSignCore.lean`
    9. `FibonacciAnyonBraiding.lean`
    10. `FoliatedFracton2Gauge.lean`
    11. `FqhLaughlinBraiding.lean`
    12. `FrustratedSpectrumObstruction.lean`
    13. `GenesisFspBridge.lean`
    14. `HaltingQuotient.lean`
    15. `Higher2GroupBraiding.lean`
    16. `InstantonDyonGas.lean`
    17. `IsingMajoranaBraiding.lean`
    18. `KitaevHoneycombCore.lean`
    19. `MajoranaGinCore.lean`
    20. `MeronCharacter.lean`
    21. `MeronClusterInvolution.lean`
    22. `NonAbelianBfBraiding.lean`
    23. `NonAbelianGaugeSigns.lean`
    24. `NormalFormLaws.lean`
    25. `ReggePachnerWdw.lean`
    26. `regge_wdw_core.lean` (842 lines)
- **Axiom and Sorry/Admit Audit in `papers/core/fsp/lean4/`:**
  - `grep_search` for `sorry` across all `.lean` files: **0 occurrences**.
  - `grep_search` for `admit` (tactic): **0 occurrences** (only English prose like "admitting").
  - `grep_search` for `axiom `: **0 occurrences**.
  - `lake build` executed in `papers/core/fsp/lean4/`:
    ```text
    Build completed successfully (24 jobs).
    ```
  - Independent compilation of standalone files (`ChiralSuperconductorCore.lean`, `KitaevHoneycombCore.lean`, `MajoranaGinCore.lean`, `regge_wdw_core.lean`) via `lean <file>`: all exit with code 0.
  - `AXIOM_REPORT.txt` confirms:
    - Total Theorems Audited: 75.
    - Zero axioms: 60.
    - Whitelisted `[propext]`: 7.
    - Whitelisted `[propext, Quot.sound]`: 8.
    - `Classical.choice`: 0.
    - Unproved sorry obligations: 0.
    - Synthetic axioms: 0.

---

### 1.5 Deposit Gate Verification (`verify_deposit.py`)
Execution of `python verify_deposit.py` inside `papers/core/fsp/` yielded:
- `[1/7]` Required files present: PASS
- `[2/7]` SHA256 checksums: **FAIL** (3 mismatches)
  1. `databases\chiral_superconductor_schema.sql`: expected `8fc84...`, got `06129...`
  2. `databases\fermion_sign_problem.sql`: expected `ade17...`, got `04ed5...`
  3. `theory_of_finite_fsp.md`: expected `b6a06...`, got `af392...` (Exact hash analysis confirmed the expected hash matches CRLF line endings, while the file on disk has LF endings).
- `[3/7]` `.zenodo.json` valid: PASS
- `[4/7]` Declared claim evidence references resolve: PASS
- `[5/7]` Claim Hygiene checks: PASS
- `[6/7]` Python test suite: PASS (460 passed in 60.06s)
- `[7/7]` Lean 4 lake build: PASS (Cleanly, zero sorries)

---

## 2. Logic Chain

1. **Premise 1 (Code duplication):** All 37 non-init Python files in `papers/core/fsp/code/` and subdirectories exist as byte-for-byte identical duplicates in `code/python/src/fsp/`.
   - *Inference:* Migrating library code to `code/python/src/fsp/` has already been largely staged, but duplicate library copies remain in `papers/core/fsp/code/`. Once migrated, the duplicate modules in `papers/core/fsp/code/` can be removed in accordance with Requirement R2.

2. **Premise 2 (Broken dependency path):** `code/python/src/fsp/sign_sql/exact_models.py:53` attempts to load `BASE / "databases" / "meron_hubbard.sql"` where `BASE = parents[2]`, resolving to `code/python/src/databases/meron_hubbard.sql` (which does not exist).
   - *Inference:* `databases/meron_hubbard.sql` (and associated SQL schema assets) must be placed in a package-accessible directory (e.g. `code/python/src/fsp/databases/` or loaded relative to `__file__`) to make `src/fsp` self-contained and importable without `FileNotFoundError`.

3. **Premise 3 (Test suite isolation):** `pyproject.toml` specifies `testpaths = ["code/python/tests"]`. `code/python/src/fsp/tests/` contains 46 test files that are never run during root `pytest`.
   - *Inference:* The 46 test files must be relocated or symlinked into `code/python/tests/fsp/` (or `testpaths` augmented) so that running `pytest` from the root executes the full FSP test suite.

4. **Premise 4 (Missing Rust Crate):** `code/rust/Cargo.toml` contains no `fsp` member or dependency, and `code/rust/src/` has no `fsp/` crate directory. Only `code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs` exists.
   - *Inference:* In order to fulfill Requirement R3.2 and Acceptance Criteria, a dedicated subcrate `tfqm_fsp` must be created under `code/rust/src/fsp/`, implementing the core derivations and certifiers, wired into `Cargo.toml` and `lib.rs`, and tested with unit/integration tests.

5. **Premise 5 (Lean 4 Disconnection):** `papers/core/fsp/lean4/` has 26 verified `.lean` files with 75 theorems, 0 sorries, and 0 custom axioms, but 0 of these files exist in root `lean4/` and none are registered in `lean4/lakefile.lean`.
   - *Inference:* To satisfy Requirement R3.3, all 26 `.lean` files must be copied to root `lean4/`, and their root modules added to `lean4/lakefile.lean`. Because all proofs are already complete and sorry-free, integration will preserve `lake build` exit code 0.

6. **Premise 6 (Verification Gate Resilience):** `verify_deposit.py` checks both package manifest checksums and local test execution. Removing duplicate code from `papers/core/fsp/code/` and updating imports to `from src.fsp import ...` requires updating `REQUIRED_FILES`, `manifest_sources()`, and `SHA256SUMS` in `papers/core/fsp/`.
   - *Inference:* The migration plan must include a step to regenerate `SHA256SUMS` and verify that `python papers/core/fsp/verify_deposit.py` exits with 0.

---

## 3. Caveats

1. **Historical Fixtures vs. General Claims:**
   - As emphasized in `the_problem_of_the_fermion_sign.md` and `claim_ledger.yaml`, many historical models (e.g., SU(2) plaquettes, SU(3) baryons, instanton-dyon gases, 5D cobordism) evaluate finite illustrative fixtures. They are verified as finite algebraic computations, not universal mathematical solutions to the NP-hard sign problem in continuous or arbitrary physical regimes.
2. **Lean 4 Mathlib Dependency:**
   - Root `lean4/lakefile.lean` requires `mathlib` (`0df444a3...`). In contrast, `papers/core/fsp/lean4/lakefile.lean` compiles without external dependencies. Integrating FSP modules into root `lean4/` must ensure no naming collisions with Mathlib or existing root modules.
3. **Line Ending Sensitivities:**
   - Windows CRLF vs. Unix LF line endings caused the observed checksum mismatch for `theory_of_finite_fsp.md`. Checksum verification scripts must account for git newline normalization policies (`core.autocrlf`).
4. **Authority Effect:**
   - All claims are scoped under `AuthorityEffect: None`. No mathematical claims beyond the declared finite/algebraic premises are asserted.

---

## 4. Conclusion & Actionable Implementation Plan

The Fermion Sign Problem package (`papers/core/fsp`) is exceptionally mature, mathematically grounded, and accompanied by exhaustive formal verification:
- 35 Claims in `claim_ledger.yaml`
- 56 Derivations in `theory_of_finite_fsp.md`
- 75 Verified Lean 4 Theorems (0 sorries, 0 custom axioms)
- 32 Normal Form YAML contracts
- 460 Passing Python tests

However, it is currently isolated from the sovereign clean architecture trees:
1. **Python:** Reusable library code is duplicated in `code/python/src/fsp`, but broken by a hardcoded relative path to `meron_hubbard.sql`. Tests are not run by the root `pytest` configuration.
2. **Rust:** No `code/rust/src/fsp` crate exists.
3. **Lean 4:** No FSP `.lean` files exist in root `lean4/`.

### Prioritized Action Items for Implementers

| Area | Priority | Concrete Action |
|---|---|---|
| **Python** | P0 | Fix `meron_hubbard.sql` path in `code/python/src/fsp/sign_sql/exact_models.py` (copy SQL files to `code/python/src/fsp/databases/` or resolve relative to package). |
| **Python** | P1 | Move the 46 test files from `papers/core/fsp/code/tests` and `code/python/src/fsp/tests` into `code/python/tests/fsp/`. Update imports to `from src.fsp import ...`. |
| **Python** | P1 | Remove duplicate library files from `papers/core/fsp/code/` while leaving shims/scripts that import from `code/python/src/fsp/`. |
| **Rust** | P0 | Create subcrate `code/rust/src/fsp/` (`Cargo.toml`, `src/lib.rs`). |
| **Rust** | P1 | Implement Rust equivalents of: (1) Fock space CAR & Trotter path generation, (2) GIN posting lists & Kitaev MZM, (3) BQNF 5-fold routing, (4) Exact rational Hubbard determinants & palindromic symmetries, (5) Normal form RREF & graph switching solvers. |
| **Rust** | P1 | Add `"src/fsp"` to `code/rust/Cargo.toml` (`workspace.members` and `dependencies`), export `pub use tfqm_fsp as fsp;` in `code/rust/src/lib.rs`. |
| **Rust** | P2 | Add comprehensive unit and integration tests in `code/rust/src/fsp/` and `code/rust/tests/test_fsp.rs`. Verify `cargo test`. |
| **Lean 4** | P0 | Copy all 26 `.lean` files from `papers/core/fsp/lean4/` to root `lean4/`. |
| **Lean 4** | P1 | Add the 22+ root modules to `lean4/lakefile.lean`. |
| **Lean 4** | P1 | Run `lake build` in `lean4/` and verify clean build with 0 sorries. |
| **Deposit** | P2 | Update `papers/core/fsp/verify_deposit.py` and `SHA256SUMS` to account for migrated code and fix the 3 checksum mismatches (including line ending normalization). |

---

## 5. Verification Method

To independently verify the observations and findings in this report, execute the following commands:

1. **Verify Python Code Identity:**
   ```powershell
   python -c "import os, filecmp; diffs = [f for f in os.listdir('papers/core/fsp/code') if f.endswith('.py') and f != '__init__.py' and not filecmp.cmp(os.path.join('papers/core/fsp/code', f), os.path.join('code/python/src/fsp', f), shallow=False)]; print('Mismatches:', diffs)"
   ```
   *Expected:* `Mismatches: []`

2. **Verify `exact_models.py` Path Bug:**
   ```powershell
   python -c "from src.fsp.sign_sql import exact_models; exact_models.connection()"
   ```
   *Expected:* `FileNotFoundError: ... code/python/src/databases/meron_hubbard.sql`

3. **Verify Dual-Face Test Passes:**
   ```powershell
   python -m pytest code/python/tests/test_dual_face_majorana_mub_fsp.py
   ```
   *Expected:* `8 passed`

4. **Verify Lean 4 Absence in Root:**
   ```powershell
   python -c "import os; fsp = [f for f in os.listdir('papers/core/fsp/lean4') if f.endswith('.lean') and f != 'lakefile.lean']; in_root = [f for f in fsp if os.path.exists(os.path.join('lean4', f))]; print('In root:', in_root)"
   ```
   *Expected:* `In root: []`

5. **Verify Lean 4 Zero-Sorry Build in FSP Package:**
   ```powershell
   cd papers/core/fsp/lean4
   lake build
   ```
   *Expected:* `Build completed successfully`, zero `sorry` warnings, exit code 0.

6. **Verify Rust Workspace Status:**
   Inspect `code/rust/Cargo.toml` and confirm `"src/fsp"` is not present in `workspace.members`.

---

## Appendix: Complete Inventory

### A.1 Claim Ledger Inventory (`claim_ledger.yaml`)

| Claim ID | Name | Claim Type | Target Symbol / Module | Verification / Proof Source |
|---|---|---|---|---|
| `PO-023-C1` | Binary Observation Non-Faithfulness | Theorem | `HaltingQuotient` | `binary_projection_not_injective`, `binary_projection_has_collision` |
| `PO-023-C2` | Halting Pigeonhole Collision | ConditionalTheorem | `HaltingQuotient` | `binary_projection_has_collision`, `binary_projection_no_left_inverse` |
| `GIN-C1` | Mode Posting List Query Efficiency | ImplementationBound | `MockFermionGinIndex` | `MockFermionGinIndex.query_by_modes`, `test_gin_posting_index_creation_and_fast_lookup` |
| `GIN-C2` | Jordan-Wigner Permutation Sign Preservation | FiniteExactComputation | `DiscreteFermionicHamiltonian` | `generate_sample_paths`, `FrustratedSpectrumObstruction.bipartite_pair_exact_cancellation` |
| `GIN-C3` | Bipartite Hubbard GIN Involution Cancellation | FiniteExactComputation | `HamiltonianGinBridge` | `index_hamiltonian_paths`, `test_bipartite_hamiltonian_indexing_and_sign_repair` |
| `GIN-C4` | Frustrated Geometry Disjoint Spectrum Obstruction | ConditionalTheoremAndFixture | `HamiltonianGinBridge` | `audit_sign_resolution`, `disjoint_spectra_obstructs_involution` |
| `GIN-C5` | 1D Kitaev Chain Majorana Zero Mode Isolation | ConditionalFiniteFixture | `MockFermionGinIndex` | `verify_majorana_zero_modes`, `FermionGinCore.edge_mode_1_not_in_bulk` |
| `GIN-C6` | Banach Quotient and Involution Sign Cancellation Identity | ConditionalAlgebraicLemma | `BQNFSignEvaluator` | `FermionGinCore.involution_pair_cancels_sign` |
| `GIN-C7` | Majorana Zero Mode Boundary Non-Bulk Membership | ConditionalFiniteFixture | `MockFermionGinIndex` | `edge_mode_1_not_in_bulk`, `edge_mode_2L_not_in_bulk` |
| `GIN-C8` | Relational SQL CTE Audits | ImplementationScope | `databases/fermion_gin_index_schema.sql` | `test_sign_sql.py::test_fermion_gin_index_schema_instantiation` |
| `GIN-C9` | SU(2) Lattice Gauge Action Gap at Theta = Pi | HistoricalIllustrativeFixture | `SU2GinBridge` | `NonAbelianGaugeSigns.su2_action_gap_forces_weight_inequality` |
| `GIN-C10` | SU(3) Color Gauge Baryon Triality Cochain Curvature | HistoricalIllustrativeFixture | `SU3BaryonGinEngine` | `NonAbelianGaugeSigns.baryon_cochain_is_open`, `meson_cochain_is_closed` |
| `GIN-C11` | SU(3) Polyakov Loop Deconfinement Action Gap | HistoricalIllustrativeFixture | `SU3PolyakovGinBridge` | `NonAbelianGaugeSigns.polyakov_deconfinement_action_gap` |
| `GIN-C12` | SU(N_c) Adjoint Zero N-ality String Breaking | HistoricalIllustrativeFixture | `SUNCAdjointEngine` | `NonAbelianGaugeSigns.adjoint_matter_zero_n_ality` |
| `GIN-C13` | 4D Simplicial Regge Wheeler-DeWitt Pachner Defect Mass | HistoricalIllustrativeFixture | `ReggeWheelerDeWittEngine` | `ReggePachnerWdw.flat_vertex_wdw_closure`, `curved_pachner_induces_positive_defect` |
| `GIN-C14` | Genesis-to-FSP Discrete Deductive Ladder | WithdrawnPhysicalInterpretation | `GenesisFspBridge` | `swap_invariant_blind`, `discrete_stokes_cancellation`, `involution_doublet_exact_cancellation` |
| `GIN-C15` | 3D Weyl Semimetal Callan-Harvey Anomaly Inflow | HistoricalIllustrativeFixture | `ChiralAnomalyInflowEngine` | `ChiralAnomalyInflow.callan_harvey_cancellation`, `chiral_asymmetry_energy_split` |
| `GIN-C16` | 2D Fractional Quantum Hall Laughlin Monodromy Order Clash | HistoricalIllustrativeFixture | `FQHLaughlinBraidingEngine` | `FqhLaughlinBraiding.involution_coprime_to_laughlin_phase` |
| `GIN-C17` | Fibonacci Anyon Non-Abelian Braiding and State Leakage | HistoricalIllustrativeFixture | `FibonacciAnyonBraidingEngine` | `FibonacciAnyonBraiding.artin_braid_relation_holds`, `fibonacci_leakage_is_positive` |
| `GIN-C18` | Ising Majorana Clifford Stability and Non-Clifford Magic Defect | HistoricalIllustrativeFixture | `IsingMajoranaBraidingEngine` | `IsingMajoranaBraiding.stabilizer_sector_cochain_closed`, `magic_state_punctures_octahedron` |
| `GIN-C19` | 3D Topological BF Linked Flux Loop Level Parity Trichotomy | HistoricalIllustrativeFixture | `BFLinkedFluxBraidingEngine` | `BfLinkedFluxBraiding.level2_symmetric_orientation_cancels` |
| `GIN-C20` | Non-Abelian BF 3-Loop Braiding and Drinfeld Double Trace Positivity | HistoricalIllustrativeFixture | `NonAbelianBfEngine` | `NonAbelianBfBraiding.quantum_double_trace_nonnegative` |
| `GIN-C21` | Higher 2-Group Braiding and Higher 2-Double Trace Positivity | HistoricalIllustrativeFixture | `Higher2GroupEngine` | `Higher2GroupBraiding.higher_2double_restores_sign_positivity` |
| `GIN-C22` | 5D Spin Cobordism Global Gravitational Anomaly Obstruction | HistoricalIllustrativeFixture | `CobordismAnomalyEngine` | `Cobordism5dAnomaly.gravitational_anomaly_obstructs_sign_cancellation` |
| `GIN-C23` | Semiclassical Instanton-Dyon Gas Clustering and Monopole Braiding Obstruction | HistoricalIllustrativeFixture | `InstantonDyonEngine` | `InstantonDyonGas.molecular_cluster_nullifies_defect`, `monopole_braiding_obstructs_sign` |
| `GIN-C24` | Foliated Fracton Order and Higher-Form 2-Gauge Defect Networks | HistoricalIllustrativeFixture | `FoliatedFractonEngine` | `FoliatedFracton2Gauge.planon_dipole_neutrality`, `subsystem_extensive_gap_positive` |
| `NF-001` | Rational quotient normal form | ConditionalTheoremAndFiniteEvidence | `fermion_sign_nf_evaluator` | `the_problem_of_the_fermion_sign.md`, Sections 13-16; `test_rational_completeness_against_independent_annihilator` |
| `NF-002` | Binary graph switching normal form | ConditionalTheoremAndFiniteEvidence | `NormalFormLaws.lean` | `NormalFormLaws.triangle_sound`, `triangle_complete`, `test_sign_section_exhaustive_soundness_idempotence_completeness` |
| `NF-003` | Exact quotient L1 reference solver | ConditionalTheoremAndFiniteEvidence | `test_normal_form_laws` | `test_l1_section_is_not_l1_minimizer_and_exact_distance_is` |
| `MERON-001` | Boolean character orbit compression | ConditionalTheoremAndFiniteEvidence | `MeronCharacter.lean` | `meron_orbit_cancels`, `zero_meron_orbit_positive`, `compression_preserves_partition` |
| `MERON-002` | Physical meron SQL reconstruction | ConditionalTheoremAndFiniteEvidence | `sign_sql/exact_models.py` | `test_real_meron_partition_replays_independent_transfer` ($Z = 912$, num $= 36864$) |
| `HUBBARD-001` | Protected determinant representations | ConditionalTheoremAndFiniteEvidence | `sign_sql/exact_models.py` | `test_half_filled_hubbard_all_fields_have_paired_determinants`, `test_attractive_frustrated_doped_hubbard_is_a_square` |
| `HUBBARD-002` | Hubbard reconstruction and negative field witnesses | ConditionalTheoremAndFiniteEvidence | `sign_sql/exact_models.py` | `test_hs_sum_replays_full_fock_transfer_including_charge_prefactor`, `test_negative_hubbard_fields_have_independently_replayed_determinants` |
| `ORIGIN-001` | Conditional signed-transport Hamiltonian | ConditionalTheoremAndFiniteEvidence | `sign_sql/exact_models.py` | `test_hubbard_configuration_cycles_reconstruct_negative_gauge_holonomy` |
| `HUBBARD-003` | Exact particle-number numerator | ConditionalIdentityAndFiniteEvidence | `sign_sql/exact_models.py` | `test_hs_sum_replays_full_fock_transfer_including_charge_prefactor` |

---

### A.2 Derivation Stages Inventory (`theory_of_finite_fsp.md`)

- **Stage 1: Pre-Genesis (`FSP-DERIV-001` - `005`):** Inert root `<>`, Lone mark, Directed cut $D_2$, Symmetrized link $S_2$, Swap-invariant predicate blindness.
- **Stage 2: Genesis & Discrete Stratification (`FSP-DERIV-006` - `008`):** 19-category substrate, $S(n)$ manifold architecture & Bianchi identities, MSS-N retractions.
- **Stage 3: Witnessed Difference Programme & Cochains (`FSP-DERIV-009` - `012`):** Rational cochain complex, Banach quotient $Q^1$, LGGR residual dichotomy, 5-fold terminal routing.
- **Stage 4: Finite Quantum Mechanics & Hilbert Lift (`FSP-DERIV-013` - `016`):** Admitted $U(1)$ phase fiber, Born normalization, Gell-Mann-Hartle decoherence positivity, Stinespring dilation.
- **Stage 5: Canonical Anticommutation Relations & Fock Algebra (`FSP-DERIV-017` - `021`):** Exterior algebra over $\mathbb{Q}$, CAR Clifford algebra, Jordan-Wigner transformation, Discrete fermionic Hamiltonian, Non-uniqueness of dynamics.
- **Stage 6: Finite Fermion Sign Problem Core & Troyer-Wiese (`FSP-DERIV-022` - `026`):** Trotter path-sum expansion, Average sign ratio $\langle \text{Sign} \rangle = e^{-\beta N \Delta f}$, Exponential sample variance, Representation dependence, Troyer-Wiese theorem.
- **Stage 7: Solvability & Involution Cancellation (`FSP-DERIV-027` - `031`):** Involution symmetry pairings, Meron cluster solutions, CT-AUX streaming GIN index, BQNF bounded quotient normal forms, Protected determinant positivity for bipartite Hubbard.
- **Stage 8: Finite Lattice QED (`FSP-DERIV-032` - `035`):** Lattice $U(1)$ gauge invariance, Wilson Dirac $\gamma_5$-Hermiticity, Compact QED vacuum angle $\theta$, Chiral anomaly inflow.
- **Stage 9: Non-Abelian Gauge Theory & QCD (`FSP-DERIV-036` - `039`):** $SU(2)$ link holonomy & adjoint fermions, $4D$ $SU(3)$ staggered quarks at non-zero $\mu$, Baryon triality, Imaginary chemical potential analytic continuation.
- **Stage 10: Supersymmetric Field Theories & Nicolai Maps (`FSP-DERIV-040` - `042`):** 2D Wess-Zumino lattice SUSY, Nicolai map Jacobian identity, Witten index beta-independence.
- **Stage 11: Topological States & Higher Gauge Theories (`FSP-DERIV-043` - `047`):** Kitaev honeycomb exact Majorana solution, FQH Laughlin braiding phase, Fibonacci anyon fusion & pentagon equations, BF gauge theory & higher 2-group anomaly cancellation, 5D cobordism invariants.
- **Stage 12: Simplicial Quantum Gravity (`FSP-DERIV-048` - `052`):** 4D Regge calculus & deficit angles, Wheeler-DeWitt Hamiltonian constraint operator, Pachner moves $2 \to 4$ and $3 \to 3$, CDT causal foliation positivity, Dirac-Kähler doubling.
- **Stage 13: Fractons & Sub-Dimensional Gauge Foliations (`FSP-DERIV-053` - `055`):** X-cube fracton model, Sub-dimensional mobility constraints (lineons/planons), Sub-dimensional sign elimination along hinge lines.
- **Stage 14: Grand Synthesis (`FSP-DERIV-056`):** Master Theorem of the Finite Fermion Sign Problem (`FermionSignAll.lean::master_finite_fermion_sign_problem_theorem`).
