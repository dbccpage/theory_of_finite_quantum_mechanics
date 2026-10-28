# Project: Theory of Finite Quantum Mechanics — Tri-Language Paper Consolidation

## Architecture
The Theory of Finite Quantum Mechanics repository maintains exact, computationally certified, and formally verified representations of quantum kinematics, algebraic varieties, topological phases, and discrete dynamics across three target languages:
1. **Python (`code/python/src/`)**: Pure algebraic, symbolic, exact arithmetic, and SQL relational evaluators with tests under `code/python/tests/`.
2. **Rust (`code/rust/src/`)**: High-performance, zero-unsafe, exact rational and discrete algebra crates (`tfqm_mub`, `tfqm_majorana`, `tfqm_fsp`, `tfqm_wdp`) unified under `code/rust/src/lib.rs` and workspace `code/rust/Cargo.toml`.
3. **Lean 4 (`lean4/`)**: Formal constructive proofs in a flat module structure verified with zero `sorry`, zero `admit`, and zero unapproved custom axioms, built via `lake build` in `lean4/lakefile.lean`.
4. **Deposit Verification**: Per-paper gates in `papers/core/{mub6,fsp,majorana}/verify_deposit.py` enforcing manifest checksum integrity, claim ledger synchronization, and test pass rates.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---|---|---|---|
| F01 | MUB6 Python Library Migration | Remove duplicate library trees in `papers/core/mub6/code/` (`mub_verify`, `conj2_symbolic_verification`); clean up `code/python/src/mub/`. | M1 | Survey E1 |
| F02 | MUB6 Python Path Normalization | Fix path lookups in `papers/core/mub6/tests/` to eliminate external `omega_engine` and relative Lean path failures. | M1 | Survey E1 |
| F03 | MUB6 Deposit Checksum Refresh | Update `sha256sums` and `manifest.sha256` via `regen_sha256sums.py` so `verify_deposit.py` passes cleanly. | M1 | Survey E1 |
| F04 | FSP Python SQL Path Fix | Fix `exact_models.py` database path to load `meron_hubbard.sql` from package resources. | M1 | Survey E2 |
| F05 | FSP Python Test Relocation | Move 46 test files from `papers/core/fsp/code/tests` and `code/python/src/fsp/tests` into `code/python/tests/fsp/`. | M1 | Survey E2 |
| F06 | FSP Python Code De-duplication | Purge duplicate library code from `papers/core/fsp/code/` and resolve Python 3.14 `code` package shadowing. | M1 | Survey E2 |
| F07 | FSP Deposit Checksum Refresh | Update `papers/core/fsp/sha256sums` (including line ending normalization) to ensure `verify_deposit.py` passes cleanly. | M1 | Survey E2 |
| F08 | Majorana Python Library Migration | Purge 103 duplicate library files from `papers/core/majorana/code/`, retaining evaluators/shims importing from `code/python/src/majorana/`. | M1 | Survey E3 |
| F09 | Majorana Legacy Import Decoupling | Decouple `majorana_evaluator.py` and `gf2_matrix.py` from nonexistent `omega_engine_operating_system` to native `gf2_terminalizer.py`. | M1 | Survey E3 |
| F10 | Majorana Deposit Checksum Refresh | Refresh `papers/core/majorana/sha256sums` for updated `README.md` and test configs so `verify_deposit.py` passes cleanly. | M1 | Survey E3 |
| F11 | MUB6 Rust Crate Verification | Verify that crate `tfqm_mub` in `code/rust/src/mub/` (109 modules) and 52 tests in `code/rust/tests/mub/` compile and pass. | M2 | Survey E1 |
| F12 | Majorana Rust Crate Verification | Verify that crate `tfqm_majorana` in `code/rust/src/majorana/` (20 modules) compiles and passes tests under `code/rust/`. | M2 | Survey E3 |
| F13 | FSP Rust Crate Creation (`tfqm_fsp`) | Implement `code/rust/src/fsp/` subcrate covering Fock space CAR, GIN posting lists, BQNF terminal routing, exact Hubbard determinants, and normal forms. | M2 | Survey E2 |
| F14 | Rust Workspace Root Wiring | Register `src/fsp` in `code/rust/Cargo.toml` and export `pub use tfqm_fsp as fsp;` in `code/rust/src/lib.rs`. | M2 | Survey E2, E3 |
| F15 | Rust Full Workspace Test Pass | Run `cargo test` across all crates with zero failures. | M2 | Survey E1-E3 |
| F16 | MUB6 Lean 4 Consolidation | Copy 184 sorry-free `.lean` files from upstream corpus into root `lean4/` and register in `lean4/lakefile.lean`. | M3 | Survey E1 |
| F17 | FSP Lean 4 Consolidation | Copy 26 sorry-free `.lean` files (75 theorems) from `papers/core/fsp/lean4/` into root `lean4/` and register in `lakefile.lean`. | M3 | Survey E2 |
| F18 | Majorana Lean 4 Consolidation | Copy `MajoranaCore.lean` and `MajoranaGinCore.lean` into root `lean4/` and register in `lakefile.lean`. | M3 | Survey E3 |
| F19 | Lean 4 Lake Build Verification | Verify `lake build` exits 0 with zero `sorry`, zero `admit`, and zero custom axioms across all consolidated modules. | M3 | Survey E1-E3 |
| F20 | MUB6 Derivation Traceability | Map all 41 claims (`MUB6-C01`–`C41`) and 86 derivations to exact Python, Rust, and Lean 4 symbols. | M4 | Survey E1 |
| F21 | FSP Derivation Traceability | Map all 35 claims (`PO-023-C1`–`C2`, `GIN-C1`–`C24`, `NF-001`–`003`, `MERON`, `HUBBARD`, `ORIGIN`) and 56 derivations to exact symbols. | M4 | Survey E2 |
| F22 | Majorana Derivation Traceability | Map all 20 claims (`MAJ-C1`–`MAJ-C20`) to exact Python, Rust, and Lean 4 symbols. | M4 | Survey E3 |
| F23 | Comprehensive Traceability Matrix | Synthesize the tri-paper, tri-language traceability matrix adhering strictly to Claim Hygiene rules. | M4 | Survey E1-E3 |
| F24 | E2E Test Infrastructure | Implement test runner, harness, and test tiers in `tests/e2e/`. | E2E | Dual Track |
| F25 | E2E Tier 1: Feature Coverage | >= 5 test cases per core feature verifying isolated functionality. | E2E | Dual Track |
| F26 | E2E Tier 2: Boundary & Corner Cases | >= 5 test cases per feature covering boundary limits, zero/negative, empty inputs. | E2E | Dual Track |
| F27 | E2E Tier 3: Cross-Feature Combinations | Pairwise feature combinations testing cross-module interactions. | E2E | Dual Track |
| F28 | E2E Tier 4: Real-World Scenarios | Realistic end-to-end physics workflows exercising full tri-paper algebra. | E2E | Dual Track |
| F29 | E2E Test Suite Validation & `TEST_READY.md` | Execute and publish `TEST_READY.md`. | E2E | Dual Track |
| F30 | Implementation Track Final Verification | Pass 100% of E2E tests (Tiers 1-4) against updated codebases. | Final | Dual Track |
| F31 | Tier 5 Adversarial Coverage Hardening | White-box adversarial testing by Challengers, resolving code gaps. | Final | Dual Track |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1 | Python Consolidation & Verification | Migrate library code to `code/python/src/`, fix SQL/Lean paths, relocate tests to `code/python/tests/`, update `verify_deposit.py` and checksums for all 3 papers. | None | DONE (All tests & 3 deposits pass) |
| M2 | Rust Tri-Paper Derivation Crate Completion | Create `tfqm_fsp` crate, wire `src/fsp` into `code/rust/Cargo.toml` and `code/rust/src/lib.rs`, verify `tfqm_mub` and `tfqm_majorana`, pass `cargo test`. | None | DONE (`tfqm_fsp` created, `lib.rs` wired, `cargo test` passed) |
| M3 | Lean 4 Root Project Consolidation | Consolidate MUB6 (184 files), FSP (26 files), and Majorana (2 files) into root `lean4/`, register in `lakefile.lean`, pass `lake build` with zero `sorry`/`admit`. | None | IN_PROGRESS (5385c5b6) |
| M4 | Tri-Language Traceability Matrix | Generate comprehensive verification report and traceability matrix mapping every claim and derivation across Python, Rust, and Lean 4 under strict claim hygiene. | M1, M2, M3 | DONE (TRACEABILITY_MATRIX.md created, Claim Hygiene compliant) |
| E2E | E2E Testing Track | Design and build opaque-box E2E test suite (Tiers 1-4) derived from `original_request.md` and publish `TEST_READY.md`. | None | DONE (45/45 tests pass, TEST_READY.md) |
| Final | Final Milestone & Adversarial Hardening | Pass 100% of E2E test suite (Tiers 1-4) and complete Tier 5 white-box adversarial hardening with Challengers. | M1, M2, M3, M4, E2E | PLANNED |

## Interface Contracts
### `mub` ↔ `majorana` ↔ `fsp` Cross-Module Contracts
- **Dual-Face Invariants**:
  - `code/python/src/mub/__init__.py`: `verify_mub_crate_invariants() -> bool`, `authority_effect() -> str`, `Cyc24` arithmetic.
  - `code/python/src/majorana/__init__.py`: `classify(omega: List[int]) -> ResidualClassification`, `build_tetron_carrier(t_count: int) -> TetronReport`.
  - `code/python/src/fsp/__init__.py`: `Witness(carrier: str, orbit_signs: List[int])`, `_star_exchange()`, `_orbit()`.
  - Cross-cutting test: `code/python/tests/test_dual_face_majorana_mub_fsp.py` asserts mutual consistency across all three domain interfaces.
- **Rust Crate API Contracts**:
  - `code/rust/src/lib.rs`:
    ```rust
    pub use tfqm_majorana as majorana;
    pub use tfqm_mub as mub;
    pub use tfqm_fsp as fsp;
    pub use tfqm_wdp as wdp;
    ```
  - `tfqm_fsp::fock::FockSpace`: standard creation/annihilation operators with anticommutation relations $\{c_i, c_j^\dagger\} = \delta_{ij}$.
  - `tfqm_fsp::bqnf::terminal_route`: 5-fold classification matching `BqnfSignPacket.lean`.
- **Lean 4 Root Module Contracts**:
  - Package `«FiniteQuantum»` declared in `lean4/lakefile.lean`.
  - Flat module imports: modules import siblings directly (e.g. `import MajoranaCore`, `import FermionSignCore`, `import RouteCFourierLandingBypass`).
  - Zero tolerance for `sorry`, `admit`, or synthetic axioms. Standard whitelist: `{propext, Classical.choice, Quot.sound}`.

## Code Layout
- Python source: `code/python/src/`
  - `mub/`: MUB(6) exact algorithms, verify modules, symbolic systems
  - `fsp/`: Fermion sign problem, normal forms, GIN index, exact models, `databases/`
  - `majorana/`: Majorana problem, GF(2) terminalizer, tetron carriers, transfer envelopes
- Python tests: `code/python/tests/`
  - `test_dual_face_majorana_mub_fsp.py`
  - `mub/`
  - `fsp/`
  - `majorana/`
- Rust source: `code/rust/`
  - `Cargo.toml`: workspace containing `src/mub`, `src/majorana`, `src/fsp`, `src/wdp`, etc.
  - `src/lib.rs`: root re-exports
  - `src/mub/`: `tfqm_mub` crate
  - `src/majorana/`: `tfqm_majorana` crate
  - `src/fsp/`: `tfqm_fsp` crate
- Lean 4 source: `lean4/`
  - `lakefile.lean`: master build configuration
  - `lean-toolchain`: Lean 4 toolchain version
  - Flat module files (`MajoranaCore.lean`, `FermionSignCore.lean`, etc.)
- Paper packages: `papers/core/{mub6,fsp,majorana}/`
  - Manuscripts, claim ledgers, deposit verification scripts (`verify_deposit.py`)
