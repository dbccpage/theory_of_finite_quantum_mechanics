# WDP-CH23-NEXT-TEST: Calibrated instance study for observer completion

**AuthorityEffect:** None.

## Scope

Finite calibrated observer-completion instance control: evaluates detector chain (E, B, D) primal/dual threshold against held-out finite fault patterns; refuses uncalibrated readout laws or mismatched syndrome dimensions.

- Python witness: `witness_wdp_ch23_next_test` in `witness.py`
- Rust witness test: `test_wdp_ch23_next_test_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/wdp_ch23_next_test.rs`
