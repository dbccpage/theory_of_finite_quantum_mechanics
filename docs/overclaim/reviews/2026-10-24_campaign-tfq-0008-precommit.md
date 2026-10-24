# Pre-Commit Statement-Match & Overclaim Review: `TFQ-0008` (`FINITE_QM_DYNAMICS`)

- **Date**: `2026-10-24`
- **Reviewer**: `automated+human-audit`
- **Target Node**: `TFQ-0008`
- **Stage**: `FINITE_QM_DYNAMICS`
- **Verdict**: `PASS`
- **AuthorityEffect**: `None`

## 1. Statement-Match Audit

- **Node Statement**: After the finite carrier, the required dynamics are finite: an instrument or measurement update, a path sum on a finite graph, a unitary or Hamiltonian shadow on a finite matrix, and a channel that is either exact or explicitly imported. The derivation note leaves the step from stochastic kernels to completely positive maps as a gap. Python, Rust, and Lean 4 must each state the finite map and the hypothesis it uses. A numerical CPTP check at a fixed tolerance is a diagnostic. It does not authorize the exact channel.
- **Lean 4 Module (`lean4/CampaignTfq0008FiniteQmDynamics.lean`)**:
  - `finite_instrument_trace_preservation_and_idempotence` and `diamond_path_sum_interference_identities` formalize finite projective instruments and 2-branch finite graph path sums.
  - `cayley_unitary_norm_conservation_exact`, `euler_first_order_generator_norm_inflation_fence`, and `fq_dynamics_cochain_syndromes_and_shadow_replay` formalize the finite Cayley unitary shadow vs. first-order generator inflation and replay the `FINITE_QM_DYNAMICS` cochain syndromes.
  - `transpose_map_preserves_trace_det_and_diagonal_states`, `stochastic_to_cp_gap_partial_transpose_bell_witness`, `numerical_cptp_tolerance_false_green_trace_drift_fence`, `numerical_cptp_tolerance_false_green_negative_choi_eigenvalue_fence`, and `exact_kraus_bit_flip_channel_trace_identity` formalize the stochastic-to-CP gap and numerical CPTP tolerance fences.
- **Independent Verification (`checks/independent/tfq-0008.py`)**:
  - Runs 1233 checks (`instrument_path=343`, `cayley_euler=491`, `cp_tolerance_fences=399`, `failures=0`).

## 2. Claim Hygiene Summary

1. **What it supports**: Supports exact rational verification of finite projective instruments, finite graph path sums, Cayley unitary norm conservation, the transpose countermodel separating stochastic/positive maps from CP maps, and the numerical CPTP tolerance false-green fences.
2. **What it does not support**: Does not support deriving CP maps from stochastic kernels, authorizing exact channels from numerical tolerances, or deriving continuum generators.
3. **Narrowest defensible claim**: Within `CampaignTfq0008FiniteQmDynamics.lean` (`L4D`, 10 theorems, 0 sorrys) and `checks/independent/tfq-0008.py` (1233 checks, 0 failures), the finite dynamical maps and non-equivalence fences hold over $\mathbb{Q}$.
4. **Next test needed**: Proceed to `TFQ-0009` (`FINITE_GAUGE`).
