# Progress — Python & Deposit Remediation Worker (worker_rem_python)

Last visited: 2026-10-19T04:52:00Z

## Current Status
- [x] Task 1: Fix broken import in `code/python/src/fsp/fermion_sign_nf_evaluator.py:11` (Clean package import and standalone fallback verified)
- [x] Task 2: Harden `verify_mub_crate_invariants()` in `code/python/src/mub/__init__.py:57-63` (Genuine Dita seed triple algebraic verification verified)
- [x] Task 3: Fix docstring in `code/python/src/mub/mub_verify/cyclotomic.py:140` (Maximal totally real subfield documented)
- [x] Task 4: Fix casing of `manifest.sha256` in `papers/core/mub6/zenodo/preprint/sha256sums` and verify `test_publication_release.py` (16/16 passed)
- [x] Task 5: Fix stale paths in root python tests (`test_pseudoinverse.py`, `test_second_jet.py`, `test_image_kernel.py`) (All 18 tests passed)
- [x] Task 6: Prune/fix unneeded legacy tests in `papers/core/majorana/code/tests/` (30/30 passed with 0 collection errors; added canonical suite in `code/python/tests/majorana/`)
- [x] Task 7: Clean up forbidden hype verbs ("proves", "guarantees") in Python files (All 4 files updated with compliant claim hygiene)
- [x] Task 8: Fix all 3 paper deposit verifiers:
  - [x] MUB6: `python papers/core/mub6/verify_deposit.py` passes cleanly with exit code 0
  - [x] FSP: `python papers/core/fsp/verify_deposit.py` passes cleanly with exit code 0 (460 tests passed, lake build clean)
  - [x] Majorana: `python papers/core/majorana/verify_deposit.py` passes cleanly with exit code 0 (30 tests passed, 95.38% coverage, lake build clean)
- [x] Task 9: Update `TEST_READY.md` line 4 (`python -m pytest code/python/tests/e2e -v` updated, 45/45 passed in 0.76s)
- [x] Task 10: Run and verify `python -m pytest code/python/tests/` passes 100% (1,492 / 1,492 passed in 185.84s, 0 failed, 0 errors)
- [x] Task 11: Write handoff.md and send message to parent orchestrator
