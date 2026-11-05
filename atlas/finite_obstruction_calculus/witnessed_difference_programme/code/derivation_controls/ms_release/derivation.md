# MS-RELEASE: WDP release gates, residual splits and re-certification

**AuthorityEffect:** None.

## Scope

Finite milestone closure control for MS-RELEASE: verifies all 12 release-gate dependencies (DEC-WDP-REPIN, WDP-DP*, PLAN-7D-DAY-7, PLAN-WDP-*) are done with paired code/test custody.

- Python witness: `witness_ms_release` in `witness.py`
- Rust witness test: `test_ms_release_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/ms_release.rs`
