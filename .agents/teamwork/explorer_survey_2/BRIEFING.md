# BRIEFING — 2026-10-18T17:21:00Z

## Mission
Conduct a comprehensive, read-only survey of `papers/core/fsp` (Fermion Sign Problem) and all FSP-related assets across Python, Rust, and Lean 4 codebases to support clean architecture migration.

## 🔒 My Identity
- Archetype: explorer
- Roles: explorer, investigator, synthesist
- Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\explorer_survey_2
- Original parent: 2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22
- Milestone: milestone_1_survey

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Claim Hygiene: narrow claims scoped to declared finite/algebraic assumptions, no hype verbs
- Write only to .agents/teamwork/explorer_survey_2/

## Current Parent
- Conversation ID: 2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22
- Updated: 2026-10-18T17:21:00Z

## Investigation State
- **Explored paths**:
  - `papers/core/fsp/` (manuscripts, code, databases, normal_forms, lean4, 000_meron, 001_hubbard)
  - `code/python/src/fsp/` and `code/python/tests/`
  - `code/rust/` (Cargo.toml, src/lib.rs, src/wdp/derivation_controls/wdp_21_16_fsp.rs)
  - `lean4/` (lakefile.lean, root files)
- **Key findings**:
  1. Python duplicate code: `code/python/src/fsp` has identical copies of all 37 library files in `papers/core/fsp/code/`, but `exact_models.py` has a hardcoded path bug looking for `BASE/databases/meron_hubbard.sql` which fails in `src/`.
  2. Python test location: 46 test files in `papers/core/fsp/code/tests` are duplicated in `code/python/src/fsp/tests/`, but missing from `code/python/tests/`, meaning root `pytest` does not discover them.
  3. Python stdlib shadowing: `papers/core/fsp/code/__init__.py` shadows python's `code` module under pytest debugging in Python 3.14.
  4. Rust crate gap: `code/rust` does not have an `fsp` subcrate (`tfqm_fsp`); only a single control file `wdp_21_16_fsp.rs` exists. Full crate must be built and wired.
  5. Lean 4 formalization gap: `papers/core/fsp/lean4/` has 26 `.lean` files (75 theorems, 0 sorry, 0 admit, 0 synthetic axioms), but ZERO are in root `lean4/` or declared in root `lean4/lakefile.lean`.
  6. Deposit verification: `papers/core/fsp/verify_deposit.py` runs 460 tests and lake build cleanly, but flags 3 SHA256 checksum mismatches (CRLF line ending issue for theory_of_finite_fsp.md and 2 sql files).
- **Unexplored areas**: none (all assigned areas surveyed)

## Key Decisions Made
- Document the exact 5-component handoff report with full inventories and actionable recommendations for migration.

## Artifact Index
- DISPATCH.md — dispatch record
- BRIEFING.md — persistent state memory
- progress.md — liveness heartbeat
- handoff.md — comprehensive survey report (TBD)
