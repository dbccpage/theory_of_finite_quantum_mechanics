Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-TROYER-WIESE-REDUCTION` (`TFQ-1192`)

AuthorityEffect: None.

## 1. Scope and Narrowed Target

Node `FSP-TROYER-WIESE-REDUCTION` (`TFQ-1192` / `FSP-DERIV-026`, stage `FERMION_SIGN`, status `IMPORTED_ASSUMPTION`) records the worst-case complexity reduction of Troyer and Wiese (2005), *Phys. Rev. Lett.* 94, 170201 (`cond-mat/0408370`, Eqs. (10)-(11) and footnote 9), built on Barahona's NP-completeness theorem for the 3D $\pm J$ Ising spin-glass ground-state energy decision problem.

While keeping the node status at `IMPORTED_ASSUMPTION` (since Barahona's 3D Ising spin-glass NP-completeness theorem is an imported external result), this note and its local witnesses ([`lean4/CampaignFspTroyerWieseReduction.lean`](../../../lean4/CampaignFspTroyerWieseReduction.lean) and [`checks/independent/fsp-troyer-wiese-reduction.py`](../../../checks/independent/fsp-troyer-wiese-reduction.py)) replace the missing `HaltingQuotient.lean::troyer_wiese_np_hardness` and trivial `GenesisFspBridge` product fixtures with the exact quantitative thermal-tail, threshold-separation, Hadamard-conjugation, and sign-variance identities of the reduction, together with explicit scope fences.

## 2. Quantitative Mechanics of the Troyer-Wiese Thermal Reduction

1. **Integer Ising energy gap and frustrated triangle spectrum (`ising_energy_integer_gap_ge_two`, `frustrated_triangle_minimum_energy_and_degeneracy`)**:
   In a $\pm J$ Ising spin glass ($J > 0$), flipping a spin $s \mapsto -s$ changes each incident bond product $s s'$ by $-2 s s' \in \{-2, +2\}$, and integer energy level differences $E - E_0 \ge 1$ scale by $J$ to $E J - E_0 J \ge J$. On an antiferromagnetic triangle $H = J (s_0 s_1 + s_1 s_2 + s_2 s_0)$, the $6$ frustrated configurations have ground energy $-J$ and the $2$ ferromagnetic configurations have excited energy $+3 J$ (gap $4 J > 0$).
2. **Boltzmann excited-state tail suppression (`thermal_excited_state_boltzmann_tail_bound`)**:
   Following Troyer-Wiese Eqs. (10)-(11), when at most $2^N$ excited configurations lie at gap $\Delta E \ge J$ above $E_0$ with energy deviation bounded by $3 N J$, choosing $\beta$ so that $W = e^{\beta J} \ge 12 N \cdot 2^N$ ($\beta J \ge N \ln 2 + \ln(12 N)$) bounds the thermal excited-state contribution strictly below $J / 4$:
   $$\frac{3 N J \cdot 2^N}{1 + W} < \frac{J}{4}.$$
3. **Decision threshold separation (`ground_energy_threshold_decision_window_separation`)**:
   Whenever $E_0 \le \langle H \rangle_\beta < E_0 + J / 4$ and an estimator $\hat{E}$ satisfies $|\hat{E} - \langle H \rangle_\beta| \le J / 4$, YES instances ($E_0 \le E_{\text{th}}$) satisfy $\hat{E} < E_{\text{th}} + J / 2$ whereas NO instances ($E_0 \ge E_{\text{th}} + J$) satisfy $\hat{E} \ge E_{\text{th}} + 3 J / 4 > E_{\text{th}} + J / 2$.
4. **Hadamard basis rotation and frustrated off-diagonal closed walks (`hadamard_basis_rotation_maps_sigma_z_glass_to_off_diagonal_sigma_x`, `frustrated_triangle_sigma_x_closed_walk_negative_weight`)**:
   Conjugation by $U_H = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$ satisfies $U_H \sigma_z U_H = 2 \sigma_x$ and $U_H \sigma_x U_H = 2 \sigma_z$, mapping the diagonal $\sigma_z$ spin glass to the off-diagonal quantum model $\sum J_{ij} \sigma_i^x \sigma_j^x$ in the $\sigma_z$ basis, where an antiferromagnetic triangle has length-3 closed-walk weight $(-J)^3 = -J^3 < 0$.
5. **Sign-estimator relative variance amplification (`sign_estimator_variance_amplification_identity`)**:
   For average sign $0 < s_1 < s_2 \le 1$, the relative sign variance $\operatorname{Var}(\sigma) / s^2 = 1 / s^2 - 1$ satisfies $0 \le 1 / s_2^2 - 1 < 1 / s_1^2 - 1$.

## 3. Scope Fences

- **Basis dependence (`troyer_wiese_is_basis_dependent_not_intrinsic_fence`)**: Under Hadamard rotation back to the $\sigma_x$ eigenbasis, $U_H \sigma_x U_H = 2 \sigma_z$ is purely diagonal with zero off-diagonal entries, showing that path-integral sign negativity is a property of the chosen basis representation rather than an basis-independent invariant.
- **Not a reduction to Hubbard or fixed $N$ (`troyer_wiese_does_not_reduce_to_hubbard_or_fixed_N_fence`)**: The worst-case spin-glass reduction does not make fixed finite system sizes $N$ intractable ($2^4 = 16$) and does not apply to bipartite half-filled Hubbard models where spin-balanced determinant weights $(\det A)^2 \ge 0$ are non-negative.
- **Withdrawn fixture audit (`withdrawn_halting_and_cochain_arity_fixtures_fence`)**: Pigeonhole collisions on `Fin 3 -> Bool` and positivity of $\beta V_4 \Delta f > 0$ do not encode a polynomial-time reduction (`IMPORTED_ASSUMPTION` preserved).
