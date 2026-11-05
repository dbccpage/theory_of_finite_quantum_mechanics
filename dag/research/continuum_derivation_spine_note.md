# Phase 5 Research Note: The 8-Stage Inherited Continuum Derivation Spine

## 1. Scope and 8-Stage Architecture

This note documents the Phase 5 formalization in `lean4/ContinuumDerivationSpine.lean` and its exact-arithmetic verification suite (`scripts/verify_continuum_derivation_spine.py`, `scripts/test_continuum_derivation_spine.py`, `dag/research/continuum_derivation_spine_receipt.json`).

Integrating the Phase 2 finite Gleason model (`lean4/BornGaussianFiniteModel.lean`), the Phase 3 continuum shadow and bridge (`lean4/GleasonContinuumShadow.lean`), and the Phase 4 continuum Gleason development (`lean4/GleasonContinuumDevelopment.lean`), Phase 5 formalizes the 8-stage mathematical derivation spine toward continuum quantum mechanics:

| Spine Stage | Lean 4 Section / Theorems | Mathematical Content & Explicit Hypotheses |
| :--- | :--- | :--- |
| **Stage 1: Scalar Field Emergence** | `gaussRat_normSq_mul`, `gaussRat_interference_cross_term`, `gaussRat_phase_shifted_interference`, `gaussRat_re_from_normSq`, `gaussRat_im_from_normSq` | Brahmagupta–Fibonacci norm composition $(zw).\text{normSq} = z.\text{normSq} \cdot w.\text{normSq}$ over $\mathbb{Q}(i)$, symmetric interference cross-term, $i$-shifted symplectic cross-term, and recovery of both $\operatorname{Re}(\bar{z}w)$ and $\operatorname{Im}(\bar{z}w)$ from quadratic norms. |
| **Stage 2: Inner Products & Parallelogram Law** | `parallelogram_law_nsq`, `dotC_re_polarization`, `dotC_im_polarization`, `dotC_eq_zero_iff_polarized_norms_eq` | Jordan–von Neumann parallelogram law $\|u+v\|^2 + \|u-v\|^2 = 2(\|u\|^2 + \|v\|^2)$ on $\mathbb{C}^3$, complex polarization identity, and characterization of orthogonality $\langle u, v \rangle = 0$ purely via polarized norms. |
| **Stage 3: State & Effect Cone Duality** | `normSqVec_mulConjTransposeVec_le`, `factorizedState3_quadRay_in_unit_interval`, `factorizedState3_frame_prob_sum_eq_one` | Exact Cauchy–Schwarz Gram bound $\|B^* v\|^2 \le \operatorname{tr}(B B^*)\|v\|^2$, unit-interval Born bounds $0 \le \operatorname{quadRay}(\rho(B), v) \le 1$, and orthomodular 3-frame probability sum $= 1$. |
| **Stage 4: Composite Tensor Products & Local Tomography** | `complexHermitianDim_mul`, `real_symmetric_local_tomography_deficit`, `real_symmetric_fails_local_tomography`, `tensor_diag_trace_mul` | Multiplicativity of complex Hermitian parameter count $(d_A d_B)^2 = d_A^2 d_B^2$ versus strict real symmetric parameter excess $d_A d_B (d_A - 1)(d_B - 1)/4 > 0$ for $d_A, d_B \ge 2$, and tensor trace multiplicativity $\operatorname{tr}(A \otimes B) = \operatorname{tr}(A)\operatorname{tr}(B)$. |
| **Stage 5: Wigner/Stone Symmetry & Unitary Dynamics** | `dotC_mulVec_mulVec`, `unitary_preserves_dotC`, `unitary_preserves_nsq`, `unitary_preserves_born_transition`, `skewHermitian_re_dotC_self_zero`, `cayley_transform_nsq_eq` | Unitary transformations $U^* U = I$ preserve $\langle u, v \rangle$, $\|u\|^2$, and $|\langle u, v \rangle|^2$; skew-Hermitian generators $K^* = -K$ satisfy $\operatorname{Re}\langle v, K v \rangle = 0$ and the exact Cayley isometric identity $\|v + K v\|^2 = \|v - K v\|^2$. |
| **Stage 6: CPTP Kraus Channels & Lüders Update** | `IsKrausComplete`, `krausQuadForm`, `krausQuadForm_nonneg_of_posSemidef`, `nsq_mulVec_eq_re_dotC`, `luders_conditional_weight_normalized` | Positivity preservation of quadratic forms under Kraus maps $\Phi(\rho) = \sum_a K_a \rho K_a^*$, branch norm identity $\|M v\|^2 = \operatorname{Re}\langle v, M^* M v \rangle$, and Lüders post-measurement normalization. |
| **Stage 7: Directed Continuum Limits** | `IsCauchyRefinement`, `cauchyRefinement_limit_error_le`, `tight_window_observable_tail_le` | Quantitative finite-stage to continuum expectation error bound $|E_{\lim} - E_N| \le \operatorname{err}_N + \delta$ and tight-window bounded-observable tail estimate $|\sum_{k < M} w(N+k) O(N+k)| \le C \varepsilon$. |
| **Stage 8: Discrete Lattice Hamiltonian Bridge** | `latticeDirichletEnergy_nonneg`, `latticeDirichletEnergy_const_zero`, `discrete_laplacian_exact_on_quadratic`, `discrete_laplacian_quartic_taylor_remainder` | Nonnegativity and constant-mode kernel of discrete lattice Dirichlet energy $\sum_k (\psi(k+1)-\psi(k))^2$, exact second-difference Laplacian scaling on quadratic modes, and explicit $2 c_4 a^2$ Taylor remainder on quartic modes. |

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - Supports in Lean 4 (using only standard axioms `propext`, `Classical.choice`, `Quot.sound`) the 8-stage algebraic and analytic spine connecting Gaussian-rational amplitudes, inner-product polarization, Gram-factorized state/effect cones, composite local-tomography dimension counting, unitary/skew-Hermitian dynamics, Kraus/Lüders updates, tight directed continuum limits, and discrete lattice Laplacian scaling.
   - Supports via exact rational arithmetic in `scripts/verify_continuum_derivation_spine.py` all 8 stage witnesses recorded in `dag/research/continuum_derivation_spine_receipt.json`.
2. **What it does not support**:
   - Does not claim an unconditional derivation of continuum regularity, $\sigma$-additivity, or continuum differentiability from finite algebra alone; each continuum bridge stage explicitly declares its regularity, tightness (`IsTightState`), or polynomial smoothness hypothesis.
3. **The narrowest defensible claim**:
   - All theorems in `lean4/ContinuumDerivationSpine.lean` are kernel-checked without `sorry` or non-standard axioms, and all finite-arithmetic witnesses in `dag/research/continuum_derivation_spine_receipt.json` are independently verified by `scripts/verify_continuum_derivation_spine.py`.
4. **The next test needed**:
   - Extend the infinite-dimensional tightness and discrete lattice Laplacian stages to interacting multi-particle lattice gauge models and non-commutative $C^*$-algebraic inductive limits.
