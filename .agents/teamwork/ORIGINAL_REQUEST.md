# Original User Request

## Initial Request — 2026-10-18T17:07:43Z

Use a very large team of agents. Review the three newly added core paper packages (`papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana`), migrate their library Python code into `code/python/src`, and ensure that every derivation, theorem, algorithm, and functionality described in the three papers is fully implemented and verified across Python (`code/python/src`), Rust (`code/rust/src`), and Lean 4 (`lean4/`).

Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics
Integrity mode: development

## Reference Material & Verification Resources

- **Core Paper Packages:**
  - `papers/core/mub6/` (`mub6.md`, `theory_of_finite_mub6.md`, `mub6_claim_ledger.yaml`, `verify_deposit.py`, `lean4/`, `rust/`, `code/`, `scripts/`, `tests/`)
  - `papers/core/fsp/` (`the_problem_of_the_fermion_sign.md`, `fermion_sign_problem.md`, `claim_ledger.yaml`, `verify_deposit.py`, `000_meron_sign_problem/`, `001_hubbard_sign_problem/`, `normal_forms/`, `lean4/`, `code/`)
  - `papers/core/majorana/` (`the_majorana_problem.md`, `claim_ledger.yaml`, `verify_deposit.py`, `lean4/`, `code/`, `contracts/`)
- **Canonical Target Trees:**
  - Python source: `code/python/src/` (`mub/`, `fsp/`, `majorana/`, and shared domain packages) and tests in `code/python/tests/` (including `code/python/tests/test_dual_face_majorana_mub_fsp.py`)
  - Rust workspace/crate: `code/rust/` (`code/rust/Cargo.toml`, `code/rust/src/mub/`, `code/rust/src/majorana/`, and `fsp` modules)
  - Lean 4 root project: `lean4/` (`lean4/lakefile.lean`, flat `.lean` module structure)
- **Existing Verification Runners:**
  - `pytest` (configured via root `pyproject.toml`)
  - `cargo test` (in `code/rust/`)
  - `lake build` (in `lean4/`)
  - `verify_deposit.py` (root and per-paper in `papers/core/{mub6,fsp,majorana}/verify_deposit.py`)

## Requirements

### R1. Comprehensive Paper & Derivation Audit (`mub6`, `fsp`, `majorana`)
Review all manuscripts, claim ledgers, companion scripts, and formal files in `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana`. Produce a complete inventory of every derivation, theorem, lemma, exact certifier, and computational check stated in the three papers, and identify all gaps across `code/python/src/`, `code/rust/src/`, and `lean4/`. Maintain claim discipline (narrow claims scoped to declared finite/algebraic assumptions; no hype verbs).

### R2. Consolidate Python Code into `code/python/src`
Move reusable Python modules from `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana` into `code/python/src/` (under `code/python/src/mub`, `code/python/src/fsp`, `code/python/src/majorana`, or appropriate domain packages), removing duplicate library modules from `papers/core/*`. Update the paper scripts, tests, `SHA256SUMS`/manifests where applicable, and each paper's `verify_deposit.py` so they import directly from `code/python/src/` and continue to pass cleanly.

### R3. Complete Tri-Language Derivations & Functionality (`Python`, `Rust`, `Lean 4`)
Ensure that the full derivations and computational functionality described in `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana` exist and are verified in all three target directories:
1. **Python (`code/python/src/`):** Complete exact arithmetic/symbolic/combinatorial derivations and certifiers for all three papers, with comprehensive tests in `code/python/tests/`.
2. **Rust (`code/rust/src/`):** Implement and wire all derivations and certifiers from `mub6`, `fsp`, and `majorana` (including migrating/integrating any standalone `.rs` files in `papers/core/mub6/rust/` and implementing full `fsp`, `mub`, and `majorana` modules in `code/rust/src/`) with unit and integration tests.
3. **Lean 4 (`lean4/`):** Consolidate and complete all Lean 4 formalizations from `papers/core/{mub6,fsp,majorana}/lean4/` and any missing paper theorems into the root `lean4/` directory (`lean4/lakefile.lean`), adhering to a flat module layout with zero `sorry`, zero `admit`, and zero unapproved custom axioms.

## Acceptance Criteria

### Python Migration & Verification
- [ ] Reusable Python library code from `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana` resides in `code/python/src/` with duplicate library copies removed from `papers/core/*`.
- [ ] `pytest` passes across `code/python/tests/` and the paper test suites with zero failures.
- [ ] `python papers/core/mub6/verify_deposit.py`, `python papers/core/fsp/verify_deposit.py`, and `python papers/core/majorana/verify_deposit.py` all execute and pass.

### Rust Implementation & Verification
- [ ] `code/rust/src/` contains complete modules covering the derivations and functionality of `mub6`, `fsp`, and `majorana` (all wired into `code/rust/src/lib.rs`).
- [ ] `cargo test` in `code/rust/` compiles cleanly and passes all unit and integration tests with zero failures.

### Lean 4 Formalization & Verification
- [ ] All Lean 4 theorems and derivations for `mub6`, `fsp`, and `majorana` are integrated into root `lean4/` and registered in `lean4/lakefile.lean`.
- [ ] `lake build` in `lean4/` succeeds with exit code 0.
- [ ] Zero `sorry` or `admit` tokens and zero custom `axiom` declarations exist in any of the target `.lean` files.

### Traceability & Claim Hygiene
- [ ] A verification report / traceability matrix maps each derivation/claim across `mub6`, `fsp`, and `majorana` to its exact file and symbol in `code/python/src/`, `code/rust/src/`, and `lean4/`, adhering strictly to the repository's Claim Hygiene rules.

## Follow-up — 2026-10-18T20:27:18Z

Server restart occurred, stopping active subagents and background crons. Please revive your Project Orchestrator (`2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22`) and resume monitoring until all milestones (M1 Python, M2 Rust, M3 Lean 4, M4 Traceability) and the Victory Audit complete.

Also note two directory updates requested by the user:
1. `lean/DerivationDagQMClosure.lean` has been moved into `lean4/DerivationDagQMClosure.lean` and `lean/` has been deleted.
2. `research/lean4/` has been merged into root `lean4/` and `research/` has been deleted.
Make sure the Orchestrator and Lean 4 worker use root `lean4/` exclusively and do not recreate `lean/` or `research/`.
