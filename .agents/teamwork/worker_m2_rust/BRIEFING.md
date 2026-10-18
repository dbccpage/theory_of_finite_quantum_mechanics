# BRIEFING — 2026-10-18T17:27:00Z

## Mission
Build and thoroughly test `tfqm_fsp` in `code/rust/src/fsp/`, wire it into workspace and root lib, satisfy wdp_21_16_fsp.rs dual-face witness, and ensure 100% clean test passes.

## 🔒 My Identity
- Archetype: implementer
- Roles: implementer, qa, specialist
- Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_m2_rust
- Original parent: 2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22
- Milestone: M2 - Complete Native Rust Derivation Worker for FSP (tfqm_fsp)

## 🔒 Key Constraints
- Strict Claim Discipline (User Global Rule): prefer narrow claims, no hype verbs, state what it supports/does not support.
- Integrity Mandate: DO NOT CHEAT, no hardcoded results, real mathematical logic.
- Exclusive file ownership: `code/rust/` (`code/rust/Cargo.toml`, `code/rust/src/lib.rs`, `code/rust/src/fsp/`, `code/rust/tests/`).
- Minimal changes outside `tfqm_fsp` (only wire `Cargo.toml`, `lib.rs`, and add integration tests in `tests/test_fsp.rs`).
- 100% clean compilation and test passes with zero failures across `code/rust/`.

## Current Parent
- Conversation ID: 2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22
- Updated: 2026-10-18T17:25:53Z

## Task Summary
- **What to build**: Crate `tfqm_fsp` under `code/rust/src/fsp/` implementing Fock space CAR algebra, BQNF terminal routing, GIN posting lists, exact rational Hubbard determinants, normal form solvers, and dual-face witness interface matching `wdp_21_16_fsp.rs`.
- **Success criteria**: All units pass, integration tests pass, zero cargo test failures, dual witness contracts satisfied.
- **Interface contracts**: `code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs`, Lean 4 `BqnfSignPacket.lean`, and Python `code/python/src/fsp/`.
- **Code layout**: `code/rust/src/fsp/` (`Cargo.toml`, `src/lib.rs`, etc.), `code/rust/tests/test_fsp.rs`.

## Key Decisions Made
- Initializing workspace context and reading all upstream reference documents before coding.

## Artifact Index
- `.agents/teamwork/worker_m2_rust/BRIEFING.md` — persistent memory
- `.agents/teamwork/worker_m2_rust/progress.md` — liveness heartbeat
- `.agents/teamwork/worker_m2_rust/DISPATCH.md` — dispatch instructions
- `.agents/teamwork/worker_m2_rust/handoff.md` — completion report (upon completion)

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pending initial cargo test
- **Lint status**: Clean
- **Tests added/modified**: Pending

## Loaded Skills
- None
