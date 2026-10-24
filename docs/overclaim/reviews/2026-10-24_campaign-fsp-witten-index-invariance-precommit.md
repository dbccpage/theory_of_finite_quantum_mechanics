# Pre-Commit Statement-Match & Overclaim Review: `FSP-WITTEN-INDEX-INVARIANCE` (`TFQ-1206`)

- **Date**: `2026-10-24`
- **Reviewer**: `automated+human-audit`
- **Target Node**: `FSP-WITTEN-INDEX-INVARIANCE` (`TFQ-1206`, `FSP-DERIV-042`)
- **Stage**: `FERMION_SIGN`
- **Verdict**: `PASS`
- **AuthorityEffect**: `None`

## 1. Statement-Match Audit

- **Node Statement**: On a finite-dimensional graded Hilbert space with an exact supercharge `Q` and `H = {Q, Q^dagger}`, positive-energy levels pair bosons with fermions, so `W = Tr[(-1)^F exp(-beta H)] = n_B(E=0) - n_F(E=0)` for every `beta`, and unbroken supersymmetry has ground energy `0`.
- **Lean 4 Module (`lean4/CampaignFspWittenIndexInvariance.lean`)**:
  - `susyHamiltonian_eq_fromBlocks`, `boson_fermion_block_pow_intertwine`, `susyHamiltonian_pow_eq_fromBlocks`, `boson_eq_fermion_pow_succ_trace`, `supertrace_susyHamiltonian_pow_succ_eq_zero`, `supertrace_fermionParity_fin_eq_sub`, and `supertrace_cubic_boltzmann_poly_independent_of_beta` establish that every positive power $H(A, B)^{k+1}$ has vanishing supertrace $\mathrm{Tr}(\Gamma_F H^{k+1}) = 0$ and any polynomial Boltzmann weight has supertrace $c_0 (n_B - n_F)$.
  - `wittenIndexPaired_eq_zero_mode_diff_for_all_weights`, `nonzero_witten_index_implies_zero_mode_ground_state`, and `rectangular_2x1_supercharge_forced_zero_mode_and_index_one` establish exact $\beta$-independence of $W(\beta) = n_B^{(0)} - n_F^{(0)}$, forced $E = 0$ ground states when $W \ne 0$, and the rectangular $(2, 1)$ forced bosonic zero mode.
  - `witten_index_vs_partition_function_and_average_sign_fence` and `broken_lattice_susy_destroys_supertrace_cancellation_fence` fence the Witten index from sign-free sampling of $Z(\beta)$ and from broken lattice supersymmetry.
- **Independent Verification (`checks/independent/fsp-witten-index-invariance.py`)**:
  - Runs 1171 checks (`supertrace=690`, `spectral=256`, `fences=225`, `failures=0`).

## 2. Claim Hygiene Summary

1. **What it supports**: Supports exact finite-dimensional verification of $\mathrm{Tr}(\Gamma_F H(A,B)^{k+1}) = 0$, $\beta$-independence of $W(\beta) = n_B^{(0)} - n_F^{(0)}$, forced $E = 0$ zero modes when $W \ne 0$, and non-equivalence fences against sign-free sampling of $Z(\beta)$ and broken lattice supersymmetry.
2. **What it does not support**: Does not support sign-free Monte Carlo sampling of $Z(\beta)$ or automatic preservation of exact lattice supersymmetry without an exact lattice supercharge.
3. **Narrowest defensible claim**: Within `CampaignFspWittenIndexInvariance.lean` (`L4D`, 12 theorems, 0 sorrys) and `checks/independent/fsp-witten-index-invariance.py` (1171 checks, 0 failures), the finite graded Witten index and its scope fences are verified.
4. **Next test needed**: Proceed to `FSP-KITAEV-HONEYCOMB-SOLUTION` (`TFQ-1207`, Rank 25).
