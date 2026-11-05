# WDP-21-8-LEAN-EXTENSION: Extend partial Lean bindings to the complete prose results

**AuthorityEffect:** None.

## Scope

Finite scope-accounting control for Chapter 21.8 partial Lean bindings: verifies that every canonical row explicitly declares its mechanized vs prose-only premise boundary without silent whole-row promotion.

- Python witness: `witness_wdp_21_8_lean_extension` in `witness.py`
- Rust witness test: `test_wdp_21_8_lean_extension_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/wdp_21_8_lean_extension.rs`
