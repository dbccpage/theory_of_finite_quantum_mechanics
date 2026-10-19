# DISPATCH — Python & Deposit Remediation Worker (worker_rem_python)

## Task Assignment
Working Directory: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_python`
Authoritative User Request: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md`
Project Architecture: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md`

### Reference Audit Reports:
- Forensic Auditor Report: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\auditor_1_integrity\handoff.md`
- Reviewer 1 Report: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\reviewer_1_code\handoff.md`
- Challenger 1 Report: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\challenger_1_empirical\handoff.md`

### Exclusive File Ownership:
`code/python/src/`, `code/python/tests/`, `papers/core/mub6/`, `papers/core/fsp/`, `papers/core/majorana/`, `TEST_READY.md`. Concurrent workers will NOT touch these files.

### Mandatory Integrity Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

### Specific Tasks:
1. **Fix Broken Import in FSP Normal Form Evaluator**:
   - In `code/python/src/fsp/fermion_sign_nf_evaluator.py:11`, change:
     `from bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex`
     to:
     `from .bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex`
   - Verify `python -c "import sys; sys.path.insert(0, 'code/python'); import src.fsp.fermion_sign_nf_evaluator"` succeeds cleanly without `ModuleNotFoundError`.
2. **Harden Top-Level MUB Invariant Verification**:
   - In `code/python/src/mub/__init__.py:57-63` (`verify_mub_crate_invariants()`):
     Replace the dummy `Fraction(1, 6) == Fraction(1, 6)` check with genuine algebraic verification:
     ```python
     from .mub_verify.mub_triples import dita_seed_triple_columns, verify_triple_pairwise_mu
     cols = dita_seed_triple_columns(0, 8)
     if not verify_triple_pairwise_mu(cols):
         raise ValueError("MUB triple pairwise mutual unbiasedness failed")
     return True
     ```
3. **Fix Cyclotomic Docstring**:
   - In `code/python/src/mub/mub_verify/cyclotomic.py:140`:
     Update docstring of `abs_sq()` from `"which is in Q"` to `"which is in the maximal totally real subfield Q(zeta_24 + zeta_24^-1) = Q(sqrt(2), sqrt(3))"`.
4. **Fix MUB Publication Release Tests & Two-Tier Manifest Agreement**:
   - In `papers/core/mub6/zenodo/preprint/sha256sums`: fix casing of `MANIFEST.sha256` to lowercase `manifest.sha256` (matching `papers/core/mub6/zenodo/preprint/manifest.sha256`) and ensure payload hashes agree.
   - Run `pytest code/python/tests/mub/test_publication_release.py` -> must pass 16/16 tests.
5. **Fix Stale Paths in Root Python Tests**:
   - In `code/python/tests/test_pseudoinverse.py:229`, `test_second_jet.py:100`, and `test_image_kernel.py`:
     Update stale path references from `papers/derivations/mub6/...` to `papers/core/mub6/...`.
6. **Clean Legacy Majorana Unit Tests**:
   - In `papers/core/majorana/code/tests/`: ensure unneeded broken tests importing purged legacy packages are pruned or fixed, so running `pytest papers/core/majorana/code/tests` or the canonical test suites in `code/python/tests/` succeeds with 0 collection errors.
7. **Enforce Claim Hygiene in Python**:
   - Replace forbidden hype verbs ("proves", "guarantees") in:
     - `code/python/src/mub/conj2_symbolic_verification/szollosi_2circulant_proof.md:171`
     - `code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py:576-577`
     - `code/python/src/fsp/cdt_susy_witten_evaluator.py:432`
     - `code/python/src/majorana/retraction_geometry.py:318`
8. **Fix All 3 Paper Deposit Verifiers (CRITICAL AUDIT BLOCKER)**:
   - **MUB6**:
     - Normalize file casing (e.g. `agents.md` vs `AGENTS.md`, `manifest.sha256` vs `MANIFEST.sha256`, `patched_rust_checks.rs` vs `PatchedRustChecks.rs`).
     - Make `papers/core/mub6/verify_deposit.py` fail gracefully with a warning when optional external `omega_engine_atlas` is not installed, or use `--skip-header-schema`.
     - Run `python papers/core/mub6/scripts/regen_sha256sums.py`.
     - Confirm `python papers/core/mub6/verify_deposit.py --skip-header-schema` passes with exit code 0.
   - **FSP**:
     - In `papers/core/fsp/`: update `sha256sums` for `lean4/AXIOM_REPORT.txt`, `lean4/PROVENANCE.md`, `lean4/README.md`, `the_problem_of_the_fermion_sign_change_log.md`, and `verify_deposit.py`. Ensure consistent line endings (LF/CRLF) and case sensitivity.
     - Confirm `python papers/core/fsp/verify_deposit.py --skip-lake` (and standard `verify_deposit.py`) passes with exit code 0.
   - **Majorana**:
     - In `papers/core/majorana/`: update `sha256sums` for `code/tests/conftest.py` (via `python papers/core/majorana/verify_deposit.py --update-sums`).
     - Confirm `python papers/core/majorana/verify_deposit.py` passes with exit code 0.
9. **Update `TEST_READY.md` Invocation Path**:
   - Update `TEST_READY.md` line 4 runner command to `python -m pytest code/python/tests/e2e -v`.
10. **Deliverables**:
    - Write full report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_python\handoff.md`.
    - Send completion message to orchestrator via `send_message`.


## 2026-10-19T04:01:01Z
You are the Python & Deposit Remediation Worker (worker_rem_python).
Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_python
Authoritative User Request: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md
Project Plan: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md
Detailed Task Instructions: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_python\DISPATCH.md

READ original_request.md, PROJECT.md, and DISPATCH.md first. Also read:
- .agents/teamwork/auditor_1_integrity/handoff.md (Finding 1: 3 paper deposit verifiers fail)
- .agents/teamwork/reviewer_1_code/handoff.md (Finding 1, 2, 3, 5: deposit checksums, test_publication_release, legacy majorana tests, claim hygiene)
- .agents/teamwork/challenger_1_empirical/handoff.md (Finding 1, 2, 4: broken relative import in fermion_sign_nf_evaluator, dummy verify_mub_crate_invariants, cyclotomic docstring)

Exclusive File Ownership:
`code/python/src/`, `code/python/tests/`, `papers/core/mub6/`, `papers/core/fsp/`, `papers/core/majorana/`, `TEST_READY.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:
1. Fix broken import in `code/python/src/fsp/fermion_sign_nf_evaluator.py:11` to `from .bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex`. Verify `python -c "import sys; sys.path.insert(0, 'code/python'); import src.fsp.fermion_sign_nf_evaluator"` succeeds.
2. Harden `verify_mub_crate_invariants()` in `code/python/src/mub/__init__.py:57-63` with genuine algebraic checks:
   `from .mub_verify.mub_triples import dita_seed_triple_columns, verify_triple_pairwise_mu`
   `cols = dita_seed_triple_columns(0, 8)`
   `if not verify_triple_pairwise_mu(cols): raise ValueError(...)`
3. Fix docstring in `code/python/src/mub/mub_verify/cyclotomic.py:140`.
4. Fix casing of `manifest.sha256` in `papers/core/mub6/zenodo/preprint/sha256sums` and run `pytest code/python/tests/mub/test_publication_release.py` (must pass 16/16).
5. Fix stale paths in `test_pseudoinverse.py:229`, `test_second_jet.py:100`, `test_image_kernel.py` from `papers/derivations/mub6` to `papers/core/mub6`.
6. Prune or fix broken unneeded legacy tests in `papers/core/majorana/code/tests/` to eliminate collection errors.
7. Clean up forbidden hype verbs ("proves", "guarantees") in Python files cited in DISPATCH.md.
8. Fix all 3 paper deposit verifiers (CRITICAL BLOCKER):
   - MUB6: normalize case (`agents.md`, `manifest.sha256`, `patched_rust_checks.rs`), make atlas import fail gracefully with a warning, run `python papers/core/mub6/scripts/regen_sha256sums.py`, verify `python papers/core/mub6/verify_deposit.py --skip-header-schema` exits 0.
   - FSP: update `sha256sums` for `AXIOM_REPORT.txt`, `PROVENANCE.md`, `README.md`, `change_log.md`, `verify_deposit.py`, verify `python papers/core/fsp/verify_deposit.py` exits 0.
   - Majorana: update `sha256sums` via `python papers/core/majorana/verify_deposit.py --update-sums`, verify `python papers/core/majorana/verify_deposit.py` exits 0.
9. Update `TEST_READY.md` line 4 to `python -m pytest code/python/tests/e2e -v`.
10. Run and verify `python -m pytest code/python/tests/` passes 100%.
11. Write completion report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_python\handoff.md` and send a completion message via `send_message` to parent orchestrator.
