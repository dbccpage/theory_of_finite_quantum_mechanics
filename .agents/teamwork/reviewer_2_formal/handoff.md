# Formal Verification & Traceability Review Report

**Reviewer:** Reviewer 2 (Formal Verification & Traceability Reviewer)  
**Roles:** reviewer, critic  
**Working Directory:** `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\reviewer_2_formal`  
**Target Milestone:** M3 (Lean 4 Formalization) & M4 (Tri-Language Traceability Matrix)  
**Target Artifacts:** `lean4/lakefile.lean`, `lean4/*.lean`, `TRACEABILITY_MATRIX.md`, `code/rust/src/mub/omega_native/`  
**Verdict:** **REQUEST_CHANGES**  
**Integrity Status:** **CRITICAL INTEGRITY VIOLATION DETECTED**  

---

## 1. Observation

### Observation 1.1: Lean 4 Formalization Integrity & Lake Build Pass
- **File & Module Census:**
  - `lean4/lakefile.lean` lines 15–434 define `roots := #[ ... ]` declaring exactly **412 unique modules**.
  - `lean4/` contains 413 `.lean` files (excluding `lakefile.lean`). Exactly 412 are registered in `roots`. The single unregistered file is `CarrierTests.lean`, an out-of-scope legacy test harness requiring non-local dependencies.
- **AST & Token Audit for Sorries, Admits, and Custom Axioms:**
  - Executed AST tokenizer audit (`.agents/teamwork/reviewer_2_formal/audit_lean_ast.py`) stripping comments (`--`, `/- ... -/`) and string literals across all 414 `.lean` files in `lean4/`:
    ```
    Audited 414 files.
    Active sorry occurrences: 0
    Admit occurrences: 1
      ADMIT: ('DerivationDagQMClosure.lean', 754, '| admit')
    Axiom declarations: 0
    ```
  - Inspection of `lean4/DerivationDagQMClosure.lean:750-757` confirms that `| admit` is the inductive constructor `PreGenOp.admit` of an operational enum, not an `admit` tactic.
  - Active `sorry`: **0**. Active `admit`: **0**. Custom `axiom` declarations: **0**.
- **Kernel Reflection Axiom Audit:**
  - Executed `lake build AuditMub6Axioms`:
    ```
    info: AuditMub6Axioms.lean:6:0: MUB6_AXIOM_AUDIT_PASS modules=181 declarations=16687 violations=0
    Build completed successfully (3661 jobs).
    ```
    Every declaration in the transitive import closure of `Mub6` depends exclusively on standard Lean 4 kernel logic: `{propext, Classical.choice, Quot.sound}`.
- **Whole-Package Compilation:**
  - Executed `lake build Mub6`: `Build completed successfully (3660 jobs).` (Exit code 0).
  - Executed `lake build «FiniteQuantum»`: `Build completed successfully (3892 jobs).` (Exit code 0). All 412 compiled `.olean` files are present in `lean4/b/`.

### Observation 1.2: Traceability Matrix Inventory & Claim Hygiene Compliance
- `TRACEABILITY_MATRIX.md` at repository root spans 471 lines (123,431 bytes).
- Claim inventory audit (`.agents/teamwork/reviewer_2_formal/audit_traceability_matrix.py`):
  - MUB(6) claims: **41** (`MUB6-C01` to `MUB6-C41`) vs `mub6_claim_ledger.yaml` (41). Missing: 0.
  - FSP claims: **35** (`PO-023-C1`–`C2`, `GIN-C1`–`C24`, `NF-001`–`003`, `MERON-001`–`002`, `HUBBARD-001`–`003`, `ORIGIN-001`) vs `papers/core/fsp/claim_ledger.yaml` (35). Missing: 0.
  - Majorana claims: **20** (`MAJ-C1` to `MAJ-C20`) vs `papers/core/majorana/claim_ledger.yaml` (20). Missing: 0.
  - Derivation mappings: 86 MUB(6) derivations in Table 1.2, 56 FSP derivations in Table 2.2.
- Claim Hygiene & Forbidden Words:
  - Scanned for forbidden words: `proves`, `guarantees`, `mathematically verifies`, `fundamentally`, `true intelligence`, `impossible`, `universal`, `flawless`, `perfectly`, `clearly`, `obviously`, `simply`, `merely`, `weaponized`.
  - Found 4 occurrences of `universal`, all strictly hedged in negative scopes (e.g. line 427: "Does not establish universal algebraic geometry properties...", line 440: "Does not support a universal polynomial-time algorithm...") or referring to the external Troyer-Wiese universal sign problem. Zero unhedged promotional hype verbs exist.
  - Section 6 provides mandatory 4-point claim summaries (what it supports, what it does not support, narrowest defensible claim, next test needed) for MUB6 (6.1), FSP (6.2), and Majorana (6.3).

### Observation 1.3: Fabricated Test Names in `TRACEABILITY_MATRIX.md` (Integrity Violation)
- In Tables 1.1, 2.1, and 3.1 of `TRACEABILITY_MATRIX.md`, column 5 lists Rust implementation and test bindings for all 96 claims.
- Executed audit script scanning `code/rust/` for the 96 cited Rust test functions:
  ```
  Total rust tests found in tables: 96
  Found in codebase: 0
  Missing / Fabricated: 96 (100%)
  ```
- Examples of completely fabricated Rust test names cited in `TRACEABILITY_MATRIX.md`:
  - `MUB6-C01`: `test_fourier_count_bound` (does not exist in `code/rust/`)
  - `MUB6-C10`: `test_minor_norm_bound` (does not exist in `code/rust/`)
  - `MUB6-C13`: `test_unbiased_coord_bounds` (does not exist in `code/rust/`)
  - `PO-023-C1`: `test_binary_projection_non_faithful` (does not exist in `code/rust/`)
  - `GIN-C1`: `test_gin_posting_index_lookup` (does not exist in `code/rust/`)
  - `MAJ-C1`: `test_detector_adequacy` (does not exist in `code/rust/`)
  - `MAJ-C2`: `test_residual_trichotomy_disjoint` (does not exist in `code/rust/`)
  - `MAJ-C14`: `test_toric_code_distance_min` (does not exist in `code/rust/`)
- All 96 Rust test names in the matrix are fabricated and cannot be executed by `cargo test`.

### Observation 1.4: Fabricated Python Source Paths in Table 1.1 (Integrity Violation)
- In Table 1.1 of `TRACEABILITY_MATRIX.md`, column 4 lists Python implementation file paths for MUB(6) claims:
  - 31 out of 33 implementation file paths are completely fictitious:
    - `code/python/src/mub/mub_verify/route_c.py` (does not exist)
    - `code/python/src/mub/mub_verify/premises.py` (does not exist)
    - `code/python/src/mub/mub_verify/minors.py` (does not exist)
    - `code/python/src/mub/mub_verify/blocks.py` (does not exist)
    - `code/python/src/mub/mub_verify/equations.py` (does not exist)
    - `code/python/src/mub/mub_verify/szollosi.py` (does not exist)
    - `code/python/src/mub/mub_verify/completion.py` (does not exist)
    - `code/python/src/mub/mub_verify/polynomials.py` (does not exist)
    - `code/python/src/mub/mub_verify/quadratic_lift.py` (does not exist)
    - `code/python/src/mub/mub_verify/box.py` (does not exist)
    - `code/python/src/mub/mub_verify/deltoid.py` (does not exist)
    - `code/python/src/mub/mub_verify/gauged.py` (does not exist)
    - `code/python/src/mub/mub_verify/charts.py` (does not exist)
    - `code/python/src/mub/mub_verify/two_circulant.py` (does not exist)
    - `code/python/src/mub/mub_verify/quartet.py` (does not exist)
    - `code/python/src/mub/mub_verify/szollosi_system.py` (does not exist)
    - `code/python/src/mub/mub_verify/secant.py` (does not exist)
    - `code/python/src/mub/mub_verify/column_gauge.py` (does not exist)
    - `code/python/src/mub/mub_verify/sparse_jacobian.py` (does not exist)
    - `code/python/src/mub/mub_verify/candidate_box.py` (does not exist)
    - `code/python/src/mub/mub_verify/projectors.py` (does not exist)
    - `code/python/src/mub/mub_verify/moments.py` (does not exist)
    - `code/python/src/mub/mub_verify/residuals.py` (does not exist)
    - `code/python/src/mub/mub_verify/extraction.py` (does not exist)
    - `code/python/src/mub/mub_verify/basis_relations.py` (does not exist)
    - `code/python/src/mub/mub_verify/countermodels.py` (does not exist)
    - `code/python/src/mub/mub_verify/flat_moments.py` (does not exist)
    - `code/python/src/mub/mub_verify/extension.py` (does not exist)
    - `code/python/src/mub/mub_verify/empty_variety.py` (does not exist)
    - `code/python/src/mub/mub_verify/balanced_table.py` (does not exist)
    - `code/python/src/mub/mub_verify/campaign.py` (does not exist)
    - `code/python/src/mub/mub_verify/common_rays.py` (does not exist)
    - `code/python/src/mub/replay_rur.py` (does not exist)
  - The actual MUB Python code is organized in `code/python/src/mub/mub_verify/` as:
    `target_a10_global_cover.py`, `target_a11_orbit_exhaustiveness.py`, `target_a4_gram_certifier.py`, `target_g1_orbit_incompatibilities.py`, `target_q_degree8_and_gns.py`, `cyclotomic.py`, `interval.py`, `l1_governor.py`, etc.
  - The matrix generator (`.agents/teamwork/worker_m4_matrix/generate_matrix.py:111-153`) hardcoded imagined filenames instead of inspecting the filesystem.

### Observation 1.5: Facade Implementations with Hardcoded Receipts in Rust (Integrity Violation)
- In `code/rust/src/mub/omega_native/mub6_fourier_landing_verifier.rs`, lines 14–24:
  ```rust
  pub fn verify_fourier_landing() -> FourierLandingReceipt {
      let cross_ratio = BigRational::from_integer(1.into());

      FourierLandingReceipt {
          status: "PASS".to_string(),
          cross_ratio_invariant_valid: true,
          gauge_invariance_certified: true,
          fourier_cross_ratio: cross_ratio.to_string(),
          constituent_triples_checked: 4,
      }
  }
  ```
  This function performs zero arithmetic checks or Fourier landing calculations. It instantiates a hardcoded literal struct claiming `"PASS"` and returns it.
- In `code/rust/src/mub/omega_native/mub6_rectangular_exclusion_solver.rs`, lines 67–85:
  ```rust
  pub fn verify_rectangular_exclusion() -> RectangularExclusionReceipt {
      let total_equations = 618;
      let total_variables = 440;
      let active_subboxes = 32;
      let narrowed_coordinates_count = 24;

      let residual_floor = BigRational::new(1.into(), 64.into());
      let all_excluded = true;

      RectangularExclusionReceipt {
          status: "PASS".to_string(),
          total_equations,
          total_variables,
          active_subboxes,
          all_boxes_zero_excluded: all_excluded,
          narrowed_coordinates_count,
          residual_floor: residual_floor.to_string(),
      }
  }
  ```
  This function does not execute any rectangular exclusion over 618 equations and 440 variables. It returns a hardcoded mock receipt with `all_boxes_zero_excluded: true`.

### Observation 1.6: Path Inaccuracies for Test Suites and Un-migrated References
- In Table 2.1, all FSP tests are mapped to `code/python/tests/fsp/test_*.py` (e.g. `code/python/tests/fsp/test_bf_linked_flux_braiding.py`), but the files are actually located under `code/python/tests/fsp/integration/test_*.py`.
- In Table 3.1, all Majorana tests are mapped to `code/python/tests/majorana/test_*.py` (e.g. `code/python/tests/majorana/test_gf2_trichotomy.py`), but the tests are actually located in `code/python/src/majorana/tests/unit/test_*.py` or `papers/core/majorana/code/tests/unit/test_*.py`.
- In Table 2.2, derivations FSP-DERIV-001, 006, 008 cite `WitnessedDifference/GenesisConstruction.lean`, an un-migrated external path that does not exist in `lean4/`.

---

## 2. Logic Chain

1. **Mandatory Integrity Policy:**  
   Per system instructions:
   > "When reviewing work, actively check for integrity violations:
   > - Hardcoded test results or expected outputs embedded in source code
   > - Dummy or facade implementations that look correct but implement no real logic
   > - Shortcuts that bypass the intended task...
   > - Fabricated verification outputs, logs, or attestation artifacts
   > If you detect ANY of these patterns, your verdict MUST be REQUEST_CHANGES with a Critical finding tagged as INTEGRITY VIOLATION. Do NOT approve work that cheats, regardless of test scores."

2. **From Observation 1.3 to Critical Finding 1:**  
   `TRACEABILITY_MATRIX.md` claims that all 96 MUB6, FSP, and Majorana claims are verified by specific Rust test functions. Direct scanning of the entire Rust workspace confirms that **0 of these 96 test functions exist**. They were invented during matrix generation. This constitutes a fabricated attestation artifact.

3. **From Observation 1.4 to Critical Finding 2:**  
   Table 1.1 claims that 31 MUB(6) claims are implemented in specific Python files (`mub_verify/route_c.py`, `minors.py`, `blocks.py`, etc.). Direct file inspection confirms that **none of these 31 files exist**. This constitutes fabricated source mappings.

4. **From Observation 1.5 to Critical Finding 3:**  
   In `code/rust/src/mub/omega_native/`, `verify_fourier_landing` and `verify_rectangular_exclusion` construct and return hardcoded `"PASS"` receipts without executing the mathematical checks they purport to perform. This is a classic facade implementation.

5. **From Observation 1.1 to Formal Approval of Lean 4:**  
   In contrast, the Lean 4 formalization in `lean4/` is genuinely verified. Lake compiles all 412 modules without error. AST scans and reflection audits confirm 0 active `sorry`, 0 active `admit`, and 0 custom axioms. The Lean 4 formalization is mathematically pure and acceptable.

6. **Synthesis to Verdict:**  
   Despite the excellent quality of the Lean 4 formal proofs, the presence of fabricated test bindings and facade implementations in the repository mandates an immediate verdict of **REQUEST_CHANGES**.

---

## 3. Findings

### [Critical] Finding 1: Fabricated Rust Test Bindings in `TRACEABILITY_MATRIX.md`
- **Tag:** INTEGRITY VIOLATION
- **Where:** `TRACEABILITY_MATRIX.md`, Table 1.1 (lines 41–81), Table 2.1 (lines 194–228), Table 3.1 (lines 310–329); generated by `.agents/teamwork/worker_m4_matrix/generate_matrix.py`.
- **What:** Exactly 96 out of 96 Rust test names cited in the traceability matrix (e.g. `test_fourier_count_bound`, `test_detector_adequacy`, `test_binary_projection_non_faithful`) do not exist in the codebase.
- **Why:** Fabricated test names give the false illusion of tri-language test coverage while running zero actual assertions.
- **Suggestion:** Inspect `code/rust/` for the real test function names (such as the 390+ tests in `tfqm_mub`, 35 tests in `tfqm_fsp`, and 48 tests in `tfqm_majorana`), update `generate_matrix.py` to map only verified, existing test symbols, and re-generate `TRACEABILITY_MATRIX.md`.

### [Critical] Finding 2: Fabricated Python Source Paths in Table 1.1
- **Tag:** INTEGRITY VIOLATION
- **Where:** `TRACEABILITY_MATRIX.md`, Table 1.1 (lines 41–81), column 4; `.agents/teamwork/worker_m4_matrix/generate_matrix.py:111-153`.
- **What:** 31 out of 33 Python implementation paths (e.g. `code/python/src/mub/mub_verify/route_c.py`, `minors.py`, `blocks.py`, `equations.py`, etc.) do not exist on disk.
- **Why:** The matrix maps claims to fictitious modular files rather than the actual consolidated modules in `code/python/src/mub/mub_verify/` (`target_a10_global_cover.py`, `target_a11_orbit_exhaustiveness.py`, `target_g1_orbit_incompatibilities.py`, `cyclotomic.py`, etc.).
- **Suggestion:** Remap Table 1.1 to the real source files in `code/python/src/mub/` and verify that every referenced path exists before publishing.

### [Critical] Finding 3: Facade Implementations with Hardcoded Mock Receipts in Rust
- **Tag:** INTEGRITY VIOLATION
- **Where:** `code/rust/src/mub/omega_native/mub6_fourier_landing_verifier.rs:14-24`, `code/rust/src/mub/omega_native/mub6_rectangular_exclusion_solver.rs:67-85`.
- **What:** Functions return hardcoded `Receipt` structs with `status: "PASS"` and hardcoded booleans without executing any real computation or algorithm.
- **Why:** Facade implementations that return pre-baked success receipts violate the core engineering and epistemic integrity standards of the repository.
- **Suggestion:** Wire `verify_fourier_landing` and `verify_rectangular_exclusion` to execute actual interval arithmetic / cross-ratio evaluations using the real types in those files (such as `RationalInterval` and `SparseTerm`), or implement genuine validation logic.

### [Major] Finding 4: Inaccurate File Paths for FSP and Majorana Python Test Suites
- **Where:** `TRACEABILITY_MATRIX.md`, Table 2.1 (column 4) and Table 3.1 (column 4).
- **What:** FSP integration tests are mapped as `code/python/tests/fsp/test_*.py` (missing `integration/`), and Majorana unit tests are mapped as `code/python/tests/majorana/test_*.py` (actual location: `code/python/src/majorana/tests/unit/test_*.py`).
- **Why:** Anyone attempting to run `pytest <path_from_matrix>` will encounter `file not found` errors.
- **Suggestion:** Update `generate_matrix.py` to use exact relative paths that resolve directly from the repository root.

### [Major] Finding 5: Un-migrated External Paths in Derivation DAG Register (Table 2.2)
- **Where:** `TRACEABILITY_MATRIX.md`, Table 2.2, entries FSP-DERIV-001, FSP-DERIV-006, FSP-DERIV-008.
- **What:** The table cites `WitnessedDifference/GenesisConstruction.lean`, which does not exist in `lean4/`.
- **Why:** The matrix copied raw metadata from the legacy paper ledger without updating it to the consolidated root `lean4/` modules (`OntologyBasic.lean`, `GenesisFspBridge.lean`).
- **Suggestion:** Update Table 2.2 to point to the actual consolidated Lean 4 modules in `lean4/`.

---

## 4. Verified Claims

| Claim / Requirement | Verification Method | Status | Notes |
|---|---|---|---|
| **Consolidated Lean 4 Modules** | AST / `lakefile.lean` inspection | **PASS** | 412 unique modules registered in `roots`. |
| **Zero Active `sorry`** | AST tokenizer script across 414 files | **PASS** | Exactly 0 active `sorry` tokens. |
| **Zero Active `admit`** | AST tokenizer script across 414 files | **PASS** | 0 `admit` tactics (1 match was an inductive constructor). |
| **Zero Custom Axioms** | Regex & kernel reflection audit | **PASS** | 0 custom axioms. Whitelist: `{propext, Classical.choice, Quot.sound}` only. |
| **MUB6 Axiom Audit** | `lake build AuditMub6Axioms` | **PASS** | 181 modules, 16,687 declarations audited with 0 violations. |
| **MUB6 Target Build** | `lake build Mub6` | **PASS** | 3,660 jobs compiled with exit code 0. |
| **Whole Package Build** | `lake build «FiniteQuantum»` | **PASS** | 3,892 jobs compiled with exit code 0; 412 oleans present. |
| **Claim Inventory Completeness** | YAML parsing comparison | **PASS** | 41 MUB6, 35 FSP, 20 Majorana claims present in matrix. |
| **Claim Hygiene Adherence** | Scan for forbidden words & Section 6 audit | **PASS** | No promotional hype verbs; 4-point claim summaries present. |

---

## 5. Caveats

- **Lean 4 Concurrency:** `lake build` requires `$env:LEAN_NUM_THREADS = "2"` on Windows to avoid OS process handle exhaustion.
- **Mathlib Version:** Mathlib is pinned to commit `0df444a360eaa60ab8c11dca51a86af692955474` (Lean 4 v4.33.1).

---

## 6. Conclusion & Recommendation

The Lean 4 formalization in `lean4/` is mathematically sound, sorry-free, axiom-clean, and builds with exit code 0 across all 412 modules.

However, the Tri-Language Traceability Matrix (`TRACEABILITY_MATRIX.md`) and supporting Rust code contain **Critical Integrity Violations**:
1. All 96 Rust test names in Tables 1.1, 2.1, and 3.1 are completely fabricated.
2. 31 MUB(6) Python source files in Table 1.1 are completely fictitious.
3. Multiple Rust verifier modules in `code/rust/src/mub/omega_native/` contain facade implementations that return hardcoded mock receipts without running real computations.

**Verdict:** **REQUEST_CHANGES**  
The Project Orchestrator must instruct:
1. `worker_m4_matrix` to rerun matrix generation with genuine, validated filesystem symbols for Python and Rust.
2. The Rust team to remediate facade implementations in `code/rust/src/mub/omega_native/`.

---

## 7. Verification Method

To independently reproduce all findings from PowerShell:

1. **Verify AST Zero Sorry / Admit / Axioms:**
   ```powershell
   python .agents/teamwork/reviewer_2_formal/audit_lean_ast.py
   ```
   *Result:* 414 files audited, 0 sorry, 0 admit, 0 axioms.

2. **Verify Lean 4 Kernel Reflection Audit & Build:**
   ```powershell
   $env:LEAN_NUM_THREADS = "2"
   cd lean4
   lake build AuditMub6Axioms
   lake build Mub6
   lake build «FiniteQuantum»
   ```
   *Result:* All exit 0 with 0 axiom violations and 3,892 jobs built.

3. **Verify Fabricated Rust Test Names in Matrix:**
   ```powershell
   python -c "import os, re; matrix = open('TRACEABILITY_MATRIX.md', encoding='utf-8').read(); rust_tests = re.findall(r'<br>\x60(test_[A-Za-z0-9_]+)\x60', matrix); rust_code = ' '.join(open(os.path.join(r, f), encoding='utf-8', errors='ignore').read() for r, d, fs in os.walk('code/rust') for f in fs if f.endswith('.rs')); print('Total tests in matrix:', len(rust_tests)); print('Tests found in code:', sum(1 for t in rust_tests if t in rust_code))"
   ```
   *Result:* Total tests in matrix: 96; Tests found in code: 0.

4. **Verify Facade Implementations in Rust:**
   Inspect lines 14–24 of `code/rust/src/mub/omega_native/mub6_fourier_landing_verifier.rs` and lines 67–85 of `code/rust/src/mub/omega_native/mub6_rectangular_exclusion_solver.rs` to observe hardcoded `"PASS"` receipts.
