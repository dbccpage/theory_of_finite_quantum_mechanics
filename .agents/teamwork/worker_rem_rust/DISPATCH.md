# DISPATCH — Rust Remediation Worker (worker_rem_rust)

## Task Assignment
Working Directory: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_rust`
Authoritative User Request: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md`
Project Architecture: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md`

### Reference Audit Reports:
- Reviewer 2 Report (Finding 3, mock receipts): `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\reviewer_2_formal\handoff.md`
- Reviewer 1 Report (Finding 4 & 5, disk space and claim hygiene): `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\reviewer_1_code\handoff.md`
- Challenger 1 Report (Finding 2, dummy check): `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\challenger_1_empirical\handoff.md`

### Exclusive File Ownership:
`code/rust/` (`code/rust/src/`, `code/rust/Cargo.toml`, `code/rust/tests/`). Concurrent workers will NOT touch these files.

### Mandatory Integrity Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

### Specific Tasks:
1. **Reclaim Disk Space**:
   - Run `cargo clean` inside `code/rust/` to remove the 11.9 GB `code/rust/target/` build cache on drive `C:`.
2. **Eliminate Facade Mock Receipts (CRITICAL INTEGRITY VIOLATION)**:
   - In `code/rust/src/mub/omega_native/mub6_fourier_landing_verifier.rs:14-24`:
     Replace the hardcoded `status: "PASS"` struct with genuine verification of the Fourier cross-ratio invariant across the constituent triples using real rational arithmetic (`BigRational`).
   - In `code/rust/src/mub/omega_native/mub6_rectangular_exclusion_solver.rs:67-85`:
     Replace the hardcoded `RectangularExclusionReceipt` with genuine rectangular exclusion verification logic using the interval arithmetic / `SparseTerm` / equation solver components already defined in that module or its sibling exact modules.
3. **Harden Top-Level MUB Invariant Verification**:
   - In `code/rust/src/mub/mod.rs:18-25` (`verify_mub_crate_invariants()`):
     Replace the trivial `1/6 == 1/6` check with genuine algebraic verification calls (e.g. validating pairwise mutual unbiasedness or checking the Dita seed / Fourier landing invariant).
4. **Enforce Claim Hygiene in Rust**:
   - Eliminate forbidden hype verbs ("proves", "guarantees") in comments and docstrings:
     - `code/rust/src/category_theory/finite_continuation.rs:128` ("proves" -> "supports" or "shows in this model")
     - `code/rust/src/category_theory/finite_moore.rs:201` ("proves" -> "supports" or "shows in this model")
     - `code/rust/src/homology/simplicial.rs:339` ("proves" -> "supports" or "shows in this model")
     - `code/rust/src/mub/src/omega_native/mub6_f6_chart.rs:85` ("proves" -> "supports" or "shows in this model")
5. **Verify Full Rust Workspace**:
   - Run `cargo test -p tfqm_fsp` -> must pass 100%.
   - Run `cargo test -p tfqm_majorana` -> must pass 100%.
   - Run `cargo test -p tfqm_wdp --lib` -> must compile and pass cleanly now that disk space is freed.
   - Run `cargo test -p tfqm_mub --lib --release -- --skip test_solve_continuous_manifold_residue_smoke` -> must pass cleanly.
6. **Deliverables**:
   - Write full report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_rust\handoff.md`.
   - Send completion message to orchestrator via `send_message`.


## 2026-10-19T04:01:01Z
[Message] timestamp=2026-10-19T04:01:01Z sender=2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22 priority=MESSAGE_PRIORITY_HIGH content=You are the Rust Remediation Worker (worker_rem_rust).
Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_rust
Authoritative User Request: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md
Project Plan: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md
Detailed Task Instructions: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_rust\DISPATCH.md

READ original_request.md, PROJECT.md, and DISPATCH.md first. Also read:
- .agents/teamwork/reviewer_2_formal/handoff.md (Finding 3: mock receipts in Rust)
- .agents/teamwork/reviewer_1_code/handoff.md (Finding 4 & 5: disk space and claim hygiene in Rust)
- .agents/teamwork/challenger_1_empirical/handoff.md (Finding 2: dummy verify_mub_crate_invariants check)

Exclusive File Ownership:
`code/rust/` (`code/rust/src/`, `code/rust/Cargo.toml`, `code/rust/tests/`).

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:
1. Run `cargo clean` inside `code/rust/` to immediately free ~12 GB disk space on drive `C:`.
2. Eliminate facade mock receipts in `code/rust/src/mub/omega_native/mub6_fourier_landing_verifier.rs:14-24` and `mub6_rectangular_exclusion_solver.rs:67-85`, replacing them with genuine verification logic using real rational arithmetic (`BigRational`) and real constraint validation.
3. Harden `verify_mub_crate_invariants()` in `code/rust/src/mub/mod.rs:18-25` to execute genuine algebraic checks instead of the trivial `1/6 == 1/6` check.
4. Clean up forbidden hype verbs ("proves", "guarantees") in `code/rust/src/category_theory/finite_continuation.rs:128`, `finite_moore.rs:201`, `homology/simplicial.rs:339`, and `mub/src/omega_native/mub6_f6_chart.rs:85`.
5. Run tests to confirm 100% clean passes:
   - `cargo test -p tfqm_fsp`
   - `cargo test -p tfqm_majorana`
   - `cargo test -p tfqm_wdp --lib`
   - `cargo test -p tfqm_mub --lib --release -- --skip test_solve_continuous_manifold_residue_smoke`
6. Write completion report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_rem_rust\handoff.md` and send a completion message via `send_message` to parent orchestrator.
