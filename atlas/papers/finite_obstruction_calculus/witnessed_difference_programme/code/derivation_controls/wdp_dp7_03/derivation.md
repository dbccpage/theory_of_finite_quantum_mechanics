# WDP-DP7-03: DP7-03: Export-clean verification in a fresh directory

**AuthorityEffect:** None.

## Scope

Finite clean-export verification gate: checks that every declared release manifest entry exists inside the extracted bundle with matching SHA-256 digest and zero parent-directory traversal.

- Python witness: `witness_wdp_dp7_03` in `witness.py`
- Rust witness test: `test_wdp_dp7_03_` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/wdp_dp7_03.rs`
