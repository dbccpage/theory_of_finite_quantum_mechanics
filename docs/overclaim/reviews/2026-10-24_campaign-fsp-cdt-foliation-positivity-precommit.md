# Pre-Commit Claim Hygiene & Scope Review: `FSP-CDT-FOLIATION-POSITIVITY` (`TFQ-1215`)

AuthorityEffect: None.

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-cdt-foliation-positivity`
- **Target Node**: `FSP-CDT-FOLIATION-POSITIVITY` (`TFQ-1215` / `FSP-DERIV-051`, stage `FERMION_SIGN`, grade `E2 -> E3`)

## 1. What This Artifact Supports
- Formalizes in [`lean4/CampaignFspCdtFoliationPositivity.lean`](../../../lean4/CampaignFspCdtFoliationPositivity.lean) (10 theorems, 0 `sorry`) and checks in [`checks/independent/fsp-cdt-foliation-positivity.py`](../../../checks/independent/fsp-cdt-foliation-positivity.py) (`checks=52525 failures=0`):
  1. Proper-time foliation $\tau : V \to \mathbb{N}$ strict causal ordering and absence of causal $2$-cycles and $3$-cycles (`proper_time_foliation_strict_order_and_no_cycles`).
  2. 4D CDT causal 4-simplex vertex partition classification $(n_t, n_{t+1}) \in \{(4,1), (3,2), (2,3), (1,4)\}$, exclusion of purely spatial $(5,0)$ and $(0,5)$ simplices, boundary tetrahedra matching, and rejection of disconnected spatial branching (`cdt_4simplex_slice_partition_classification`, `cdt_boundary_tetrahedra_and_no_spatial_branching`).
  3. Exact rational Wick-rotated Boltzmann weight positivity $W = w_0^{n_0} w_{41}^{n_{41}} w_{32}^{n_{32}} > 0$ (`wick_rotated_cdt_boltzmann_weight_positivity`).
  4. Reflection positivity $\langle \psi, T \psi \rangle = \sum_k d_k (B \psi)_k^2 \ge 0$ of the symmetric CDT slice transfer matrix $T = B^T D B$ (`reflection_positive_transfer_matrix_symm_and_psd`) and strict positivity of multi-slice partition traces $Z_1 = 7, Z_2 = 47, Z_3 = 322$ on the explicit 2-state transfer matrix witness $T_{\text{cdt}} = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}$ (`two_state_cdt_transfer_matrix_trace_and_det_pos`).
  5. BQNF sign-reversing weight-preserving involution pair cancellation vs the frustrated 3-configuration chiral ensemble obstruction (`bqnf_involution_cancels_pairs_vs_chiral_obstruction`).

## 2. What This Artifact Does Not Support
- Does not derive Wick rotation from Lorentzian quantum gravity (`lorentzian_vs_euclidean_wick_rotation_fence`).
- Does not derive a continuum 4D de Sitter spacetime or spectral dimension $d_s = 4$ from finite triangulations; on any finite connected complex of $N$ vertices, the stationary random-walk return probability saturates at $1/N$ with zero step increment (`finite_complex_stationary_return_probability_saturates_fence`).
- Does not eliminate fermionic Grassmann determinant sign problems on CDT backgrounds (`bosonic_cdt_positivity_independent_of_fermion_determinant_sign_fence`).

## 3. Narrowest Defensible Claim
- On a finite vertex set with a declared proper-time slicing $\tau : V \to \mathbb{N}$ and positive Wick-rotated monomer fugacities, the causal 4-simplex partition condition restricts adjacent-slice simplices to types $(4,1), (3,2), (2,3), (1,4)$, and the symmetric half-step transfer matrix $T = B^T D B$ satisfies reflection positivity $\langle \psi, T \psi \rangle \ge 0$, while Lorentzian phase oscillations, infinite-volume 4D de Sitter emergence, and fermionic determinant signs remain outside the scope of bosonic CDT foliation positivity.

## 4. Next Test Needed
- Proceed to Rank 45 `FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` (`TFQ-1216`) to formalize the 4D Dirac-Kähler exterior-algebra taste count $\sum_{k=0}^4 \binom{4}{k} = 16 = 4 \times 4$ and evaluate explicit finite boundary spin-network contraction signs.
