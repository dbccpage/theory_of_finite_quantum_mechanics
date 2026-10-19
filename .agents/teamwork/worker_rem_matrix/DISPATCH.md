# DISPATCH — Traceability Matrix Remediation Worker (worker_rem_matrix)

## Task Assignment
Working Directory: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_matrix`
Authoritative User Request: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md`
Project Architecture: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md`

### Reference Audit Reports:
- Reviewer 2 Report (Finding 1, 2, 4, 5 — fabricated symbols and paths): `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\reviewer_2_formal\handoff.md`

### Exclusive File Ownership:
`TRACEABILITY_MATRIX.md` at repository root, `.agents/teamwork/worker_rem_matrix/`. Concurrent workers will NOT touch these files.

### Mandatory Integrity Warning:
DO NOT CHEAT. All implementations, claims, file paths, and test symbols must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or invent fictitious test names or file paths. A teamwork_preview_auditor will independently verify your matrix. Integrity violations WILL be detected and your work WILL be rejected.

### Specific Tasks:
1. **Inspect Real Files and Real Test Symbols in the Codebase**:
   - Inspect `code/rust/src/` for actual test function names:
     - `tfqm_mub` has 374+ real unit tests (e.g. in `tests/`, `src/omega_native/`, etc.).
     - `tfqm_fsp` has 13 real unit tests and 9 integration tests in `code/rust/tests/test_fsp.rs`.
     - `tfqm_majorana` has 126 real unit/integration tests.
   - Inspect `code/python/src/mub/mub_verify/` for actual Python source files:
     - Real files: `target_a10_global_cover.py`, `target_a11_orbit_exhaustiveness.py`, `target_a4_gram_certifier.py`, `target_g1_orbit_incompatibilities.py`, `target_q_degree8_and_gns.py`, `cyclotomic.py`, `interval.py`, `l1_governor.py`, `mub_triples.py`, `exact_cross_ratio.py`, etc.
   - Inspect `code/python/tests/fsp/` and `code/python/tests/majorana/` (or `code/python/src/majorana/tests/`) for actual test paths:
     - FSP tests are located under `code/python/tests/fsp/` or `code/python/tests/fsp/integration/test_*.py`.
     - Majorana tests are located under `code/python/tests/majorana/` or `code/python/src/majorana/tests/unit/test_*.py`.
   - Inspect `lean4/` for actual Lean 4 module names (all 412 registered modules in `lean4/lakefile.lean`).
2. **Remediate `generate_matrix.py` (or Author New Remediation Generator)**:
   - Eliminate all 96 fabricated Rust test names from `TRACEABILITY_MATRIX.md`. Map every claim (`MUB6-C01` to `C41`, `PO-023-C1`–`C2`, `GIN-C1`–`C24`, `NF-001`–`003`, `MERON`, `HUBBARD`, `ORIGIN`, `MAJ-C1`–`C20`) to real, existing Rust test function names.
   - Eliminate all 31 fictitious Python file paths in Table 1.1 (`route_c.py`, `minors.py`, `blocks.py`, etc.). Map all MUB(6) claims to real Python source files in `code/python/src/mub/mub_verify/`.
   - Fix test paths in Table 2.1 and Table 3.1 so that `pytest <path>` resolves directly to existing files.
   - Fix Table 2.2 external paths (replace `WitnessedDifference/GenesisConstruction.lean` with the actual consolidated modules in `lean4/` such as `OntologyBasic.lean` or `GenesisFspBridge.lean`).
3. **Regenerate and Verify `TRACEABILITY_MATRIX.md`**:
   - Write a standalone verification script that checks EVERY referenced Python file, Rust test symbol, and Lean 4 module in `TRACEABILITY_MATRIX.md`.
   - Ensure 100% of referenced files and symbols exist on disk.
4. **Preserve Claim Hygiene Discipline**:
   - Maintain narrow claims scoped to declared finite/algebraic premises.
   - Forbid hype verbs ("proves", "guarantees", "fundamentally", "universal", etc.).
   - Preserve the mandatory 4-point claim hygiene summaries for MUB6 (6.1), FSP (6.2), and Majorana (6.3).
5. **Deliverables**:
   - Write updated `TRACEABILITY_MATRIX.md` at repository root.
   - Write full report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_matrix\handoff.md`. Include verification commands and outputs proving 100% symbol existence.
   - Send completion message to orchestrator via `send_message`.


## 2026-10-19T04:01:01Z
You are the Traceability Matrix Remediation Worker (worker_rem_matrix).
Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_matrix
Authoritative User Request: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md
Project Plan: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md
Detailed Task Instructions: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_matrix\DISPATCH.md
