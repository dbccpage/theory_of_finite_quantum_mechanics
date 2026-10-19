---
trigger: always_on
description: Run scripts/verify_qm_atlas_loc.py and code/python/tests/test_qm_atlas_loc.py whenever Lean, Rust, Python, or manuscript files are edited so line ranges and symbol bindings remain synchronized.
---

# QM Atlas Line-of-Code & Symbol Synchronization Rule

Whenever any Lean (`lean4/*.lean`), Rust (`code/rust/**/*.rs`), Python (`code/python/**/*.py`), or manuscript (`papers/**/*.md`, `docs/**/*.md`) file is edited:

1. Run `python scripts/verify_qm_atlas_loc.py` to check all 65 QM question bindings (`Q01`–`Q65`), all `#Lstart-Lend` line ranges, in-window symbol definitions, 1-to-1 Rust/Python `build_qm_question_atlas()` parity, and Claim Hygiene compliance in `docs/QM_PROBLEM_AND_PROOF_ATLAS.md`.
2. Run `python -m pytest code/python/tests/test_qm_atlas_loc.py` to verify all textbook problem receipts (`Q58`–`Q65`) and atlas synchronization tests.
3. If an edit shifts line ranges or renames a symbol referenced in `docs/QM_PROBLEM_AND_PROOF_ATLAS.md`, `code/python/src/qm/textbook_problems.py`, or `code/rust/src/qm/textbook_problems.rs`, update the corresponding line ranges or symbol bindings before committing.
