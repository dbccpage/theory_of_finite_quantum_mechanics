# Reviewer 1 (Code & Crate Reviewer) — Review Report & Verdict

**Verdict**: **REQUEST_CHANGES**

---

## 1. Observation

### Obs 1: Deposit Verifiers Execution and Manifest Failures
Running the three deposit verifiers produced failures across all three paper packages:

1. **`papers/core/mub6/verify_deposit.py`**:
   - Command: `python papers/core/mub6/verify_deposit.py`
   - Result: Exit code 1. Verbatim output:
     ```
     FAIL: Manifest checks failed (30 issues):
       - Hash mismatch: AGENTS.md
       - Hash mismatch: README.md
       - Hash mismatch: documentation/publication_preparation.md
       - Hash mismatch: prompts/prompt_05_mub6_triadic_adversarial_operad_n6_equals_3.md
       - Recorded file missing: research/archive/reviews_and_audits/audit_2026_09_22/PatchedRustChecks.rs
       - Hash mismatch: research/archive/reviews_and_audits/audit_2026_09_22/README.md
       - Recorded file missing: research/archive/reviews_and_audits/audit_2026_09_22/RustProbes.rs
       - Hash mismatch: research/archive/reviews_and_audits/audit_2026_09_22/prepare_checks.py
       - Hash mismatch: research/archive/reviews_and_audits/audit_2026_09_22/report.md
       - Hash mismatch: research/g1_foundation/reuse_audit.md
       - Hash mismatch: research/mub6_gap_registry.json
       - Hash mismatch: scripts/build_publication_release.py
       - Hash mismatch: scripts/regen_sha256sums.py
       - Hash mismatch: scripts/verify_publication.py
       - Hash mismatch: tests/test_publication_release.py
       - Hash mismatch: verify_deposit.py
       - Hash mismatch: zenodo/preprint/scripts/verify_publication.py
       - Unrecorded deposit file: agents.md
       - Unrecorded deposit file: manifest.sha256
       - Unrecorded deposit file: research/archive/reviews_and_audits/audit_2026_09_22/patched_rust_checks.rs
       - Unrecorded deposit file: research/archive/reviews_and_audits/audit_2026_09_22/rust_probes.rs
       - Unrecorded deposit file: zenodo/preprint/manifest.sha256
       - Unrecorded deposit file: zenodo/preprint/sha256sums
       - Excluded file listed in manifest: AGENTS.md
       - Excluded file listed in manifest: MANIFEST.sha256
       - Excluded file listed in manifest: research/archive/reviews_and_audits/audit_2026_09_22/PatchedRustChecks.rs
       - Excluded file listed in manifest: research/archive/reviews_and_audits/audit_2026_09_22/RustProbes.rs
       - Excluded file listed in manifest: zenodo/preprint/MANIFEST.sha256
       - Excluded file listed in manifest: zenodo/preprint/SHA256SUMS
       - Paper header schema kit unavailable; header not checked (No module named 'omega_engine_atlas'). Pass --skip-header-schema to skip explicitly.

     Verification FAILED with 30 errors.
     ```

2. **`papers/core/fsp/verify_deposit.py`**:
   - Command: `python papers/core/fsp/verify_deposit.py --skip-lake`
   - Result: Exit code 1. Verbatim output:
     ```
     [FAIL] Pre-Print Deposit Gate Failed with errors:
       - Checksum mismatch for lean4\AXIOM_REPORT.txt: expected 8bc304268f3718a729458091d53d84153cb607e573db8457e3635a5df6dd75ee, got 122567d1da2b08428e0a250a400a8084fc590f46cebd7c399dcab9492e102dfb
       - Checksum mismatch for lean4\PROVENANCE.md: expected 0b074b24d613e5d7941e16a5d113063552ffc56221ff8cfd33ddaf3b8c42f4c1, got a8d30a71bae8b35193d3610bde6fef4d47c6fcc18c0a738eefec21484f066126
       - Checksum mismatch for lean4\README.md: expected 312d4aacd5d76077fc6940e71d8b3ccdaf775391d68a7594aed8124e7b130885, got adf596cc86569900f5663d3211dbcdf934e13ace915c923f89c0f4cc30f2d050
       - Checksum mismatch for the_problem_of_the_fermion_sign_change_log.md: expected 6a7a01912c3dab995e154ed57815316f89f5e429e7b7b49f90d9c4f4b1624e1d, got 48f7a09d3f45fc17b5e68c2bbad7a614f053db399b284757491394fa13e64c32
       - Checksum mismatch for verify_deposit.py: expected aae44e4dddc49264b5c9f7e88ceec175fa60e21c03cf8eaa132d543ca98fe111, got 0cc05c37732857027be989df86306c2f0342fa66a9249271544389f100886401
       - Source not covered by checksum manifest: lean4/axiom_report.txt
       - Source not covered by checksum manifest: lean4/provenance.md
     ```

3. **`papers/core/majorana/verify_deposit.py`**:
   - Command: `python papers/core/majorana/verify_deposit.py`
   - Result: Exit code 1. Verbatim output:
     ```
     Starting deposit verification in: C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\papers\core\majorana
     [1/7] Checking required files existence...
       PASSED: All 22 required files present.
     FAIL: Hash mismatch: code/tests/conftest.py
     OK: .zenodo.json required fields present.
     OK: claim IDs agree between YAML and Markdown ledgers
     OK: Claim hygiene verified
     ...
     30 passed in 2.36s
     OK: Pytest suite passed cleanly with >=95% coverage
     Build completed successfully (4 jobs).
     OK: Lean build succeeded cleanly without sorries
     FAILURE: One or more deposit checks failed.
     ```

### Obs 2: Python Test Suites Execution
1. **`code/python/tests/fsp/`**:
   - Command: `python -m pytest code/python/tests/fsp -q`
   - Result: **460 passed in 132.65s (100% pass)**.
2. **`code/python/tests/test_dual_face_majorana_mub_fsp.py`**:
   - Command: `python -m pytest code/python/tests/test_dual_face_majorana_mub_fsp.py -v`
   - Result: **8 passed in 2.05s (100% pass)**.
3. **`code/python/tests/mub/`**:
   - Command: `python -m pytest code/python/tests/mub/test_publication_release.py -v`
   - Result: **8 failed, 8 passed** out of 16 tests in `test_publication_release.py`.
   - Error: `ValueError: Two-tier manifest disagreement or empty payload` at line 74, 124, 134, 159.
   - Root cause: `papers/core/mub6/zenodo/preprint/sha256sums` line 3 lists `MANIFEST.sha256` (uppercase), whereas `verify_publication.py:47-48` expects lowercase `manifest.sha256` and identical payload dictionaries.
4. **Majorana Tests**:
   - Directory `code/python/tests/majorana/` does not exist.
   - Command: `python -m pytest tests/unit/test_gf2_trichotomy.py tests/unit/test_open_system_transfer_bounds.py tests/integration/test_tetron_surface_codes.py tests/e2e/test_majorana_problem_e2e.py -q` in `papers/core/majorana/code`: **30 passed in 0.94s (100% pass)**.
   - However, running unconstrained `pytest papers/core/majorana/code/tests` aborts with `214 errors during collection` due to unpruned legacy unit test files importing purged modules.
5. **Repo-level Legacy Tests**:
   - `code/python/tests/test_pseudoinverse.py:229`: `FileNotFoundError: papers\derivations\mub6\artifacts\knowledge\category_moore_penrose_least_squares_annihilation.md` (hardcoded stale path to `papers/derivations` which was relocated to `papers/core`).
   - `code/python/tests/test_second_jet.py:100` and `code/python/tests/test_image_kernel.py`: same stale path failure.
   - `code/python/tests/test_deposit_verifier_evidence.py`: 9 test errors.

### Obs 3: Opaque-box E2E Test Suite Execution
- `TEST_READY.md` lists invocation as `python -m pytest tests/e2e -v`.
- Directory `tests/e2e` does not exist at repo root. It exists at `code/python/tests/e2e/`.
- Command: `python -m pytest code/python/tests/e2e -v`
- Result: **45 passed in 1.44s (100% pass)** across:
  - Tier 1 (Feature Coverage): 18/18 passed
  - Tier 2 (Boundary & Corner Cases): 17/17 passed
  - Tier 3 (Pairwise Combinations): 5/5 passed
  - Tier 4 (Real-World Scenarios): 5/5 passed

### Obs 4: Rust Crate Compilation and Testing
1. **`tfqm_fsp`**:
   - Command: `cargo test -p tfqm_fsp` in `code/rust`
   - Result: **13 passed, 0 failed in 0.05s**.
2. **`tfqm_majorana`**:
   - Command: `cargo test -p tfqm_majorana` in `code/rust`
   - Result: **126 passed, 0 failed in 0.35s**.
3. **`tfqm_mub`**:
   - Command: `cargo test -p tfqm_mub --lib -- --list`
   - Result: **393 tests listed**.
4. **`tfqm_wdp`**:
   - Command: `cargo test -p tfqm_wdp --lib` in `code/rust`
   - Result: Failed during compilation with OS error 112:
     ```
     error: failed to write to `C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\code\rust\target\debug\deps\rmeta7cNOJ6\full.rmeta`: There is not enough space on the disk. (os error 112)
     error: could not compile `omega_quantum_physics` (lib) due to 1 previous error
     ```
   - Disk observation: `Get-PSDrive C` reports `Used (GB): 475.64, Free (GB): 0.00`. Drive C is at 100% capacity (`code/rust/target` alone consumes 11.9 GB).

### Obs 5: Claim Hygiene Violations
Grep of forbidden words (`\b(proves|guarantees|mathematically verifies|fundamentally|true intelligence|flawless|weaponized)\b`) identified unhedged hype claims in source code:
1. `code/python/src/mub/conj2_symbolic_verification/szollosi_2circulant_proof.md:171`: `"Analytically proves that for ANY 6x6 matrix..."`
2. `code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py:576-577`: `"Forced >= 5 Dita bases guarantees >= 10 pure Dita triples..."`
3. `code/python/src/fsp/cdt_susy_witten_evaluator.py:432`: `"Proves \Delta_Witten(\beta) is strictly independent of \beta..."`
4. `code/python/src/majorana/retraction_geometry.py:318`: `"Proves that Phi(d0_higher) <= Phi(d0_1st)..."`
5. `code/rust/src/category_theory/finite_continuation.rs:128`: `"A completed empty result proves equivalence"`
6. `code/rust/src/category_theory/finite_moore.rs:201`: `"This proves |M/~| <= |N| and the minimal quotient"`
7. `code/rust/src/homology/simplicial.rs:339`: `"so the admitted storage bound proves that the i64 sum fits."`
8. `code/rust/src/mub/src/omega_native/mub6_f6_chart.rs:85`: `"declares a chart + proves it Hadamard exactly"`

---

## 2. Logic Chain

1. **Step 1 (Deposit Verifier Acceptance Criteria)**:
   - *Requirement R2 / Acceptance Criteria*: "`python papers/core/mub6/verify_deposit.py`, `python papers/core/fsp/verify_deposit.py`, and `python papers/core/majorana/verify_deposit.py` all execute and pass."
   - *From Obs 1*: All three verifiers fail when invoked directly without special flags, due to checksum mismatches on modified files, casing mismatches (`MANIFEST.sha256` vs `manifest.sha256`, `AXIOM_REPORT.txt` vs `axiom_report.txt`, `agents.md` vs `AGENTS.md`), unrecorded files, and missing imports (`omega_engine_atlas`).
   - *Deduction*: Milestone M1 claims of passing deposit verification gates were self-certified without genuine end-to-end execution. This constitutes a gating failure under Acceptance Criteria.

2. **Step 2 (Python Test Suite Completeness)**:
   - *Requirement R1/R2*: Consolidate tests into `code/python/tests/` and verify pass.
   - *From Obs 2*: `code/python/tests/fsp/` (460/460 pass) and `test_dual_face_majorana_mub_fsp.py` (8/8 pass) are healthy. However:
     - `test_publication_release.py` in `code/python/tests/mub/` fails 8 tests due to manifest casing/two-tier disagreement.
     - There is no `code/python/tests/majorana/` package; majorana tests only live in `papers/core/majorana/code/tests` and `code/python/src/majorana/tests/`.
     - `papers/core/majorana/code/tests` contains 214 uncleaned broken test files.
     - Root test files (`test_pseudoinverse.py`, etc.) contain broken hardcoded paths pointing to deleted `papers/derivations/`.
   - *Deduction*: Python test migration is partially incomplete and regressions exist in `code/python/tests/mub/` and repo root suites.

3. **Step 3 (E2E Test Suite Alignment)**:
   - *From Obs 3*: All 45 tests across Tiers 1-4 execute and pass in 1.44s with genuine algebraic evaluations.
   - *Deduction*: The E2E test implementation is high quality, but documentation in `TEST_READY.md` specifies `python -m pytest tests/e2e -v`, whereas the directory is located at `code/python/tests/e2e/`.

4. **Step 4 (Rust Workspace Health)**:
   - *From Obs 4*: `tfqm_fsp` (13 tests) and `tfqm_majorana` (126 tests) pass cleanly. `tfqm_mub` has 393 tests mapped.
   - *From Obs 4*: Full workspace compilation (`tfqm_wdp`) failed with disk full error (`os error 112`, 0.00 GB free on `C:`).
   - *Deduction*: Rust workspace compilation cannot be fully validated until disk space is freed on the host.

5. **Step 5 (Claim Hygiene Enforceability)**:
   - *From Obs 5*: Multiple occurrences of "proves" and "guarantees" exist in docstrings and comments across `code/python/src/` and `code/rust/src/`.
   - *Deduction*: Claim Hygiene standard is violated. Words like "proves" must be replaced with "shows in this model" or "supports" per repository rule.

---

## 3. Caveats

- Lean 4 lake build verification was not re-run in full during this review because Lean compilation was delegated to Milestone M3 / Reviewer 2.
- `tfqm_mub` full test suite was not executed in unoptimized debug mode due to documented multi-hour timeouts in `test_solve_continuous_manifold_residue_smoke` and current host disk space constraints.
- Drive C storage depletion (0.00 GB available) prevents running large builds or storing additional test artifacts until the user/orchestrator clears temporary build directories (`code/rust/target`, `C:\Users\a343o\AppData\Local\Temp`).

---

## 4. Conclusion & Required Actions

**Verdict**: **REQUEST_CHANGES**

The codebase contains substantial, high-quality, genuine mathematical and algebraic certifiers across Python, Rust, and E2E suites. However, it cannot be approved in its current state due to the following blocking items:

### Required Changes (Action Items)

1. **Fix Deposit Verifier Checksums & Manifests (CRITICAL)**:
   - **MUB6**: Run `scripts/regen_sha256sums.py`, normalize case for `agents.md`, `manifest.sha256`, `patched_rust_checks.rs`, `rust_probes.rs`, and make `omega_engine_atlas` header schema import fail gracefully with a warning instead of aborting when absent.
   - **FSP**: Refresh `papers/core/fsp/sha256sums` for `verify_deposit.py`, `the_problem_of_the_fermion_sign_change_log.md`, `lean4/README.md`, and normalize casing between `AXIOM_REPORT.txt`/`axiom_report.txt` and `PROVENANCE.md`/`provenance.md`.
   - **Majorana**: Refresh checksum for `code/tests/conftest.py` in `papers/core/majorana/sha256sums`.
   - Ensure `python papers/core/{mub6,fsp,majorana}/verify_deposit.py` all exit with code 0.

2. **Fix `code/python/tests/mub/test_publication_release.py` (MAJOR)**:
   - Fix casing of `manifest.sha256` in `papers/core/mub6/zenodo/preprint/sha256sums` so `verify_publication.py` passes two-tier manifest checks.

3. **Prune / Relocate Obsolete Majorana Tests (MAJOR)**:
   - Clean up the 214 broken legacy tests in `papers/core/majorana/code/tests/unit/` that import purged modules, or relocate the 4 validated test suites (`test_gf2_trichotomy.py`, `test_open_system_transfer_bounds.py`, `test_tetron_surface_codes.py`, `test_majorana_problem_e2e.py`) into canonical `code/python/tests/majorana/`.

4. **Fix Stale Paths in Root Python Tests (MINOR)**:
   - In `code/python/tests/test_pseudoinverse.py:229`, `test_second_jet.py:100`, and `test_image_kernel.py`: update `papers/derivations/mub6` to `papers/core/mub6`.

5. **Update Test Path in `TEST_READY.md` (MINOR)**:
   - Update `TEST_READY.md` execution command to `python -m pytest code/python/tests/e2e -v` or add a root `tests/` symlink/forwarder.

6. **Enforce Claim Hygiene (MAJOR)**:
   - Replace forbidden hype verbs ("proves", "guarantees") in:
     - `code/python/src/mub/conj2_symbolic_verification/szollosi_2circulant_proof.md:171`
     - `code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py:576-577`
     - `code/python/src/fsp/cdt_susy_witten_evaluator.py:432`
     - `code/python/src/majorana/retraction_geometry.py:318`
     - `code/rust/src/category_theory/finite_continuation.rs:128`
     - `code/rust/src/category_theory/finite_moore.rs:201`
     - `code/rust/src/homology/simplicial.rs:339`
     - `code/rust/src/mub/src/omega_native/mub6_f6_chart.rs:85`

7. **Disk Space Remediation for Rust Full Workspace Build (CRITICAL)**:
   - Free disk space on drive `C:` (e.g. `cargo clean` in `code/rust` or clearing temporary caches) to allow `cargo test -p tfqm_wdp` and root `cargo test` to compile.

---

## 5. Verification Method

Once the actions above are addressed, the fix can be independently verified via:

```powershell
# 1. Deposit Verifiers (must all exit 0)
python papers/core/mub6/verify_deposit.py --skip-header-schema
python papers/core/fsp/verify_deposit.py --skip-lake
python papers/core/majorana/verify_deposit.py

# 2. Python Test Suites (must all exit 0)
python -m pytest code/python/tests/mub -v
python -m pytest code/python/tests/fsp -q
python -m pytest code/python/tests/test_dual_face_majorana_mub_fsp.py -v
python -m pytest code/python/tests/e2e -v

# 3. Rust Crates (must all pass)
cd code/rust
cargo test -p tfqm_fsp
cargo test -p tfqm_majorana
cargo test -p tfqm_wdp --lib
cargo test -p tfqm_mub --lib --release char_two_parametric_gate

# 4. Claim Hygiene (must return 0 results)
rg -i "\b(proves|guarantees|mathematically verifies|fundamentally|true intelligence|flawless|weaponized)\b" code/python/src/ code/rust/src/
```

**Invalidation conditions**:
- Any `Hash mismatch` or `Unrecorded deposit file` in `verify_deposit.py`.
- Any failure in `code/python/tests/mub/test_publication_release.py`.
- Any survival of unhedged "proves" or "guarantees" in source files.
