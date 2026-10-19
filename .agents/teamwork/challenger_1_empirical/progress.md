# Progress — Challenger 1 (Python & Rust Stress Challenger)

Last visited: 2026-10-19T03:52:50Z

## Status
Empirical adversarial stress testing completed across Python and Rust targets. Four test suites authored and executed in `code/python/tests/`:
- `test_adversarial_mub6_stress.py` (11 tests passed)
- `test_adversarial_fsp_stress.py` (9 tests passed)
- `test_adversarial_majorana_stress.py` (12 tests passed)
- `test_adversarial_cross_cutting_stress.py` (6 tests passed)
- Baseline `test_dual_face_majorana_mub_fsp.py` (8 tests passed)
Total 46/46 adversarial tests passing in 0.97s.

Rust crates verified:
- `cargo test -p tfqm_fsp`: 13/13 passed in 0.03s
- `cargo test -p tfqm_majorana`: 126/126 passed in 0.20s
- `cargo test -p tfqm_mub --lib --release`: 374 passed (0 failed, 18 ignored, 1 filtered out) in release mode. Windows file lock cleared (`write_registry_artifact` passed).

Critical Empirical Findings Identified:
1. `code/python/src/fsp/fermion_sign_nf_evaluator.py:11` has broken un-prefixed relative import (`from bqnf_sign_evaluator ...` instead of `from .bqnf_sign_evaluator ...`), crashing on external import. Masked by `code/python/tests/fsp/conftest.py` path injection.
2. `verify_mub_crate_invariants()` in Python and Rust is a dummy mock/tautology checking `1/6 == 1/6` with zero algebraic MUB verification.
3. `code/python/src/fsp/__init__.py:72` hardcodes `checked = 64` and `removing = 0` in `_star_exchange()` and `_orbit()` rather than computing the 64 gauge transformations dynamically like Rust `wdp_21_16_fsp.rs`.
4. `code/python/src/mub/mub_verify/cyclotomic.py:140` docstring erroneously claims `Cyc24.abs_sq()` is always in Q; property-based stress tests proved it is in Q(sqrt(2), sqrt(3)).

## Step Checklist
- [x] Step 1: Inbound dispatch recorded, BRIEFING.md and progress.md initialized
- [x] Step 2: Survey test suites, existing tests, and target modules in Python and Rust
- [x] Step 3: Run existing baseline test suites (`pytest`, `cargo test`)
- [x] Step 4: Design and execute empirical stress tests & property-based oracles:
  - [x] 4a: MUB(6) stress harness (`test_adversarial_mub6_stress.py`)
  - [x] 4b: FSP stress harness (`test_adversarial_fsp_stress.py`)
  - [x] 4c: Majorana stress harness (`test_adversarial_majorana_stress.py`)
  - [x] 4d: Cross-cutting dual-face stress harness (`test_adversarial_cross_cutting_stress.py`)
- [x] Step 5: Rust crate empirical stress testing (`code/rust/`)
- [x] Step 6: Mock/stub inspection (verify non-trivial, non-mocked execution)
- [ ] Step 7: Compile empirical findings and challenge report in `handoff.md`
- [ ] Step 8: Send completion message with verdict to orchestrator
