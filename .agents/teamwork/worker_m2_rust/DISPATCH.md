## 2026-10-18T17:25:53Z
You are Worker M2 (Rust Derivation Worker).
Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_m2_rust
Authoritative User Request: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\ORIGINAL_REQUEST.md
Master Project Plan: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\PROJECT.md

READ ORIGINAL_REQUEST.md and PROJECT.md first. Also read:
- .agents/teamwork/explorer_survey_2/handoff.md (FSP findings)
- code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs

Exclusive File Ownership: `code/rust/` (`code/rust/Cargo.toml`, `code/rust/src/lib.rs`, `code/rust/src/fsp/`, `code/rust/tests/`).

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:
1. Create crate `tfqm_fsp` under `code/rust/src/fsp/` with `Cargo.toml` and complete native implementations:
   - Fock space CAR algebra: creation/annihilation operators, Jordan-Wigner signs, path-sum expansions.
   - BQNF terminal routing: 5-fold classification matching `BqnfSignPacket.lean`.
   - GIN posting lists: mode indexing, Kitaev chain Majorana zero modes, and involution doublet cancellation.
   - Exact rational Hubbard determinants: $4\times 4$ plaquette, attractive Hubbard square-root symmetry, and palindromic spectra.
   - Normal form solvers: RREF over $\mathbb{Q}$ and graph switching invariants.
   - Dual-face witness interface matching `wdp_21_16_fsp.rs` and `code/python/src/fsp/__init__.py`.
2. Wire `tfqm_fsp` into `code/rust/Cargo.toml`:
   - Add `"src/fsp"` to `[workspace.members]`.
   - Add `tfqm_fsp = { path = "src/fsp" }` to dependencies.
3. Wire into `code/rust/src/lib.rs`:
   - Export `pub use tfqm_fsp as fsp;`.
   - Update module inventory in `crate_root_inventory_holds()`.
4. Verify existing `tfqm_mub` and `tfqm_majorana` in `code/rust/` compile cleanly.
5. Implement unit tests in `code/rust/src/fsp/` and integration tests in `code/rust/tests/test_fsp.rs`.
6. Run `cargo test` across `code/rust/` and confirm 100% clean compilation and test passes with zero failures.
7. Deliverables:
   - Write your comprehensive completion report to `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_m2_rust\handoff.md`. Include exact verification commands and full outputs.
   - Send a completion message via `send_message` to the parent orchestrator with a summary of changes and test results.


## 2026-10-18T20:28:55Z
**Context**: Server restart recovery for Milestone M2 (Rust Derivation Completion).
**Content**: A server restart occurred which marked subagents idle and stopped background tasks. Please resume your execution from where you left off:
1. Complete implementation of crate `tfqm_fsp` under `code/rust/src/fsp/` (Fock space CAR, Jordan-Wigner signs, GIN posting lists, BQNF terminal routing, exact rational Hubbard determinants, normal form solvers, and dual-face witness).
2. Wire `tfqm_fsp` into `code/rust/Cargo.toml` and export `pub use tfqm_fsp as fsp;` in `code/rust/src/lib.rs`.
3. Add unit and integration tests under `code/rust/src/fsp/` and `code/rust/tests/test_fsp.rs`.
4. Run `cargo test` and verify 0 failures across the workspace.
5. Write `handoff.md` and report completion.
**Action**: Resume execution and drive M2 to completion.
