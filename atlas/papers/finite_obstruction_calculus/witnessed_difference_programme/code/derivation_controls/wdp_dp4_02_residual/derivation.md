# WDP-DP4-02-RESIDUAL: Lean statement for contractive complements (DP-4)

**AuthorityEffect:** None.

## Scope

Finite DP-4 contractive-complement control: checks operator-norm contractivity (||T|| <= 1) and complementary defect positivity (I - T^T T >= 0) on the 4 rational sample matrices of P.4.a; refuses super-unity singular values.

- Python witness: `witness_wdp_dp4_02_residual` in `witness.py`
- Rust witness test: `test_wdp_dp4_02_residual_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/wdp_dp4_02_residual.rs`
