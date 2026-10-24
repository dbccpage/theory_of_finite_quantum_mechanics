# Pre-Commit Statement-Match & Overclaim Review: `TFQ-0006` (`L1_TO_L2`)

- **Date**: `2026-10-24`
- **Reviewer**: `automated+human-audit`
- **Target Node**: `TFQ-0006`
- **Stage**: `L1_TO_L2`
- **Verdict**: `PASS`
- **AuthorityEffect**: `None`

## 1. Statement-Match Audit

- **Node Statement**: The pass from L1 weights to a finite Hilbert carrier imports structure the finite papers do not derive: a square-root field, a complex field, U(1) phases, an inner product, orthogonal additivity, Haar-independent phases, and linear isometric dynamics. `QM_020` states that it does not derive quantum mechanics. `QM_122` recovers matrices over the Gaussian integers and leaves ordinary matrix algebras over the complex numbers unrecovered. Python, Rust, and Lean 4 must name each import and keep it imported. A finite matrix calculation is not a discharge of the import list.
- **Lean 4 Module (`lean4/CampaignTfq0006L1ToL2.lean`)**:
  - `gauss_int_norm_multiplicative`, `qm122_pauli_gaussian_integer_commutators_and_squares`, and `qm122_and_qm020_cochain_syndrome_and_shadow_replay` formalize the finite $\mathbb{Z}[i]$ matrix recovery of `QM_122` and the cochain syndromes of `QM_122` / `QM_020`.
  - `import_fence_sqrt_two_parity_obstruction`, `import_fence_gaussian_integers_not_a_field_hadamard_unnormalized`, `import_fence_gaussian_units_vs_u1_phases`, `import_fence_l1_norm_fails_parallelogram_law`, `import_fence_orthogonal_additivity_and_phase_averaging`, `import_fence_l1_stochastic_not_l2_isometry`, and `seven_hilbert_lift_imports_audit_fence` explicitly name and fence all 7 imported structures.
- **Independent Verification (`checks/independent/tfq-0006.py`)**:
  - Runs 1202 checks (`qm122_qm020=240`, `field_phase_fences=532`, `hilbert_lift_fences=430`, `failures=0`).

## 2. Claim Hygiene Summary

1. **What it supports**: Supports exact verification of the finite $\mathbb{Z}[i]$ matrix algebra (`QM_122`), `QM_020` cochain syndromes, and the 7 structural non-discharge fences keeping the Hilbert-lift import list explicit.
2. **What it does not support**: Does not support discharging the 7 Hilbert-lift imports or deriving quantum mechanics from L1 weights.
3. **Narrowest defensible claim**: Within `CampaignTfq0006L1ToL2.lean` (`L4D`, 10 theorems, 0 sorrys) and `checks/independent/tfq-0006.py` (1202 checks, 0 failures), the finite $\mathbb{Z}[i]$ recovery is verified while all 7 Hilbert-lift imports remain explicitly imported.
4. **Next test needed**: Proceed to `TFQ-0008` (`FINITE_QM_DYNAMICS`).
