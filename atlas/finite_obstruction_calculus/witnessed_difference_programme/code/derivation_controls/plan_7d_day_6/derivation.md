# Derivation Control: PLAN-7D-DAY-6

**AuthorityEffect:** None.

## Scope and Claim

This finite control (`PLAN-7D-DAY-6`) certifies the Day 6 scope freeze, built Rust executable provenance, hostile changed-input controls, and checkpoint resume discipline:

1. **Scope Freeze & Child Gate Completion**:
   - Verifies that `PLAN-7D-DAY-4` (Lanes B/C native-reference correspondence + Lanes A/D scoped reuse) and `PLAN-7D-DAY-5` (staged `SG-40`/`SG-48` non-reset campaign + Lane E `PQ-1`..`PQ-6`) pass without adding new scope items.
2. **Built Rust Executable Provenance (`native_build_receipt_guarded_2026_10_06.json`)**:
   - Verifies the native build receipt (`schema: "wdp-causal-native-build-v1"`, `binary_sha256: "b37105dc9c58603b239bf1678af641c4f23bf5f23738642a97fd420853e27dcf"`, `cargo_lock_sha256: "8d7f43fa07f11af9502924843a56e74b3e8064365c2e29347dea4d8fc89900c1"`) and the declared Rust binary entrypoints `omega_engine/crates_rs/omega_wdp/src/bin/genesis_extension.rs` and `omega_engine/crates_rs/omega_wdp/src/bin/wdp_guarded_history.rs`.
3. **Anti-Wrapper, Changed-Input, and Checkpoint Resume Controls**:
   - Rejects any static-label wrapper that emits `"PASS"` without recomputing from problem inputs.
   - Replays changed-task, changed-coefficient, and changed-witness refusal controls across the frozen capabilities.
   - Verifies interrupted/resumed checkpoint execution (`pre_interrupt_spent = 11`, `post_resume_spent = 3`, `total_spent = 14 <= 20`), refusing any tampered checkpoint digest or fuel-reset attempt.

## Non-Claims

- This finite control does not claim empirical LLM behavior or unbounded continuous-time verification.
